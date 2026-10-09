"""Picks each voice's cleanest recorded lines as a reference clip for F5-TTS, with their words.

usage: python ref_select.py <speech-wav-dir> <out-dir> <voice>...

A line is clean when few of its samples sit at full scale (the game's lines are limited hard, and
some clip), it lasts two to seven seconds, and Whisper hears it confidently. The best lines are
joined, with short pauses, into about nine seconds: <out-dir>/<voice>.wav, and their words in
<out-dir>/<voice>.txt.
"""

import os
import sys

import librosa
import numpy as np
import soundfile
import whisper

import voices

speech_dir, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
RATE = 24000
asr = whisper.load_model("small.en")

for voice in sys.argv[3:]:
    candidates = []
    for path in voices.files_of(speech_dir, voice):
        wav, _ = librosa.load(path, sr=RATE)
        wav, _ = librosa.effects.trim(wav, top_db=35)
        seconds = len(wav) / RATE
        if not 1 <= seconds <= 9:
            continue
        clipped = float(np.mean(np.abs(wav) > 0.97))
        # Lines of two to seven seconds first; a voice with few lines takes what it has.
        candidates.append((clipped + (0 if 2 <= seconds <= 7 else 1), path, wav))
    # The least clipped first, then let Whisper judge how clearly each says its words.
    candidates.sort(key=lambda c: c[0])
    scored = []
    for clipped, path, wav in candidates[:20]:
        result = asr.transcribe(path, fp16=False)
        segments = result["segments"]
        if not segments:
            continue
        confidence = float(np.mean([s["avg_logprob"] for s in segments]))
        scored.append((confidence - 20 * clipped, path, wav, result["text"].strip()))
    scored.sort(key=lambda s: -s[0])
    clip, words, total = [], [], 0.0
    for _, path, wav, text in scored:
        if total + len(wav) / RATE > 10:
            continue
        clip += [wav, np.zeros(int(0.35 * RATE), dtype=np.float32)]
        words.append(text)
        total += len(wav) / RATE + 0.35
        if total >= 8:
            break
    peak = np.max(np.abs(np.concatenate(clip)))
    soundfile.write(os.path.join(out_dir, f"{voice}.wav"), np.concatenate(clip) * (0.7 / peak), RATE)
    open(os.path.join(out_dir, f"{voice}.txt"), "w").write(" ".join(words))
    print(f"{voice}: {total:.1f} s from {len(words)} lines: {' '.join(words)}", flush=True)
