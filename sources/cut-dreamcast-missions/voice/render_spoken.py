"""Renders the briefings Enriquez speaks over the briefing room, with F5-TTS or Chatterbox, and
joins the pieces with pauses like those of her own spoken briefing at the campaign's end.

usage: python render_spoken.py <f5|chatterbox[:exaggeration:cfg-weight]> <documents-dir> <speech-wav-dir> <reference-dir> <out-dir> <mission>...

Chatterbox's exaggeration sets how expressive she is, and its weight how eager her pace; lower is
more measured. Both are 0.5 by default.

Chatterbox renders a paragraph at a time, which keeps her intonation across its sentences. F5
crashes on the Mac's GPU when it splits a text into batches, so it renders as much of a paragraph
as fits in one batch. Whisper checks each piece, and a piece that isn't right is rendered again
with another seed, keeping the best. Each piece is trimmed to its speech, which drops the silence
or noise a model pads it with, and the pieces are joined with pauses measured from her spoken
briefing (`enddebriefing`). Writes <out-dir>/raw/dreamcast_brief<mission>.wav, its pieces beside
it, and lines.json and checks.json for finish.py.
"""

import json
import os
import re
import sys

import librosa
import numpy as np
import scipy.signal
import soundfile
import whisper

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voices  # noqa: E402
from speech_text import heard_share, right, score, spoken  # noqa: E402

engine_given, docs, speech_dir, ref_dir, out_dir = sys.argv[1:6]
engine, *settings = engine_given.split(":")
exaggeration, cfg_weight = (float(settings[0]), float(settings[1])) if settings else (0.5, 0.5)
missions = sys.argv[6:]
os.makedirs(os.path.join(out_dir, "raw"), exist_ok=True)
# The voice the briefings are finished as, her spoken briefing's, and the clean clip of it that both
# models take as their reference.
VOICE = "enriquez_spoken"
ref = os.path.join(ref_dir, "enriquez_room.wav")
ref_text = open(os.path.join(ref_dir, "enriquez_room.txt")).read()
SEEDS = (7, 11, 23, 37, 41, 53)
# The pauses after a piece, from her spoken briefing's: a median of 0.42 s between sentences.
PAUSE = {"comma": 0.15, "sentence": 0.40, "paragraph": 0.65}

if engine == "f5":
    from f5_tts.api import F5TTS

    model = F5TTS(model="F5TTS_v1_Base", device="mps")
    ref_seconds = librosa.get_duration(path=ref)
    # The longest text F5 renders in one batch with this reference (`infer_process`), with a margin.
    MOST = int(0.9 * (len(ref_text) + 1) / ref_seconds * (22 - ref_seconds))

    def generate(text, seed, path):
        model.infer(ref_file=ref, ref_text=ref_text, gen_text=spoken(text), file_wave=path, seed=seed, remove_silence=False)
        return soundfile.read(path)
else:
    import torch
    from chatterbox.models.s3gen import S3GEN_SR
    from chatterbox.models.s3tokenizer import S3_SR

    import clone

    model = clone.load_model()
    MOST = 10_000
    # Her voice: the mean speaker embedding of everything she says in person and of her briefings'
    # narration, and the clean clip of her spoken briefing as the acoustic prompt.
    files = voices.files_of(speech_dir, "enriquez_room") + voices.files_of(speech_dir, "enriquez_brief")
    recordings = [w for w in (clone.trimmed(f, S3_SR) for f in files) if len(w) > S3_SR // 2]
    embed = model.ve.embeds_from_wavs(recordings, sample_rate=S3_SR).mean(axis=0)
    prompt, _ = librosa.load(ref, sr=S3GEN_SR)
    clone.condition(model, embed, prompt, exaggeration=exaggeration)

    def generate(text, seed, path):
        torch.manual_seed(seed)
        wav = clone.render(model, spoken(text), exaggeration=exaggeration, cfg_weight=cfg_weight)
        soundfile.write(path, wav, model.sr)
        return wav, model.sr

asr = whisper.load_model("small.en")


def pieces_of(paragraph):
    """The paragraph's pieces, each with the pause after it: sentences grouped up to `MOST`
    characters, a sentence longer than that split at its commas."""
    clauses = []
    for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
        if len(sentence) <= MOST:
            clauses.append((sentence, "sentence"))
        else:
            parts = [c.strip() for c in re.split(r"(?<=,)\s+", sentence)]
            clauses += [(part, "comma") for part in parts[:-1]] + [(parts[-1], "sentence")]
    pieces, text, pause = [], "", "sentence"
    for clause, after in clauses:
        if text and len(text) + 1 + len(clause) > MOST:
            pieces.append((text, pause))
            text = clause
        else:
            text = f"{text} {clause}".strip()
        pause = after
    pieces.append((text, "paragraph"))
    return pieces


def speech_only(wav, rate):
    """`wav` from its first to its last stretch of speech, with 30 ms either side: the frames within
    32 dB of its loudest, which leaves out the quiet noise a model pads a piece with."""
    frame = int(0.02 * rate)
    level = np.sqrt(np.convolve(wav**2, np.ones(frame) / frame, mode="same"))
    loud = np.flatnonzero(level > level.max() * 10 ** (-32 / 20))
    if len(loud) == 0:
        return wav
    margin = int(0.03 * rate)
    return wav[max(0, loud[0] - margin): loud[-1] + margin]


def render(text, path):
    """Renders a piece until Whisper hears it right, or the seeds run out, keeping the best try."""
    best = None
    attempt = path + ".try.wav"
    for tries, seed in enumerate(SEEDS, 1):
        wav, rate = generate(text, seed, attempt)
        heard = asr.transcribe(attempt, fp16=False)["text"].strip()
        mark = score(heard, text)
        if best is None or mark > best[0]:
            best = (mark, heard)
            os.replace(attempt, path)
        if right(best[0]):
            break
    if os.path.exists(attempt):
        os.remove(attempt)
    print(f"  {'ok' if right(best[0]) else 'BEST'} after {tries}: {best[1]}", flush=True)


lines, checks = {}, {}
for mission in missions:
    text = open(os.path.join(docs, f"mission{mission}.md")).read()
    section = text[text.index("## Enriquez's briefing"):]
    section = section[: section.index("\n## ", 5)]
    quote = "\n".join(re.sub(r"^> ?", "", line) for line in section.splitlines() if line.startswith(">"))
    paragraphs = [" ".join(p.split()) for p in quote.split("\n\n") if p.strip()]
    name = f"dreamcast_brief{mission}"
    pieces_dir = os.path.join(out_dir, "raw", f"{name}.pieces")
    os.makedirs(pieces_dir, exist_ok=True)
    parts, rate = [], None
    number = 0
    for paragraph in paragraphs:
        for piece, pause in pieces_of(paragraph):
            number += 1
            path = os.path.join(pieces_dir, f"{number:02d}.wav")
            print(piece, flush=True)
            render(piece, path)
            wav, rate = soundfile.read(path)
            parts += [speech_only(wav, rate), np.zeros(int(PAUSE[pause] * rate))]
    raw = os.path.join(out_dir, "raw", f"{name}.wav")
    joined = np.concatenate(parts[:-1])
    if engine == "chatterbox":
        # Chatterbox's vocoder leaves a faint, steady tone at a quarter of its rate, 6 kHz, now and
        # again: a narrow notch takes it out.
        notch, poles = scipy.signal.iirnotch(model.sr / 4, 15, fs=rate)
        joined = scipy.signal.filtfilt(notch, poles, joined)
    soundfile.write(raw, joined, rate)
    words = " ".join(paragraphs)
    heard = asr.transcribe(raw, fp16=False)["text"].strip()
    lines[name] = {"voice": VOICE, "words": words}
    checks[name] = {"voice": VOICE, "words": words, "heard": heard, "share": round(heard_share(heard, words), 3)}
    print(name, checks[name]["share"], f"{len(np.concatenate(parts)) / rate:.1f} s", flush=True)
json.dump(lines, open(os.path.join(out_dir, "lines.json"), "w"), indent=1)
json.dump(checks, open(os.path.join(out_dir, "checks.json"), "w"), indent=1)
