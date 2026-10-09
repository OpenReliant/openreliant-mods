"""Renders lines again until Whisper hears all their words, keeping each line's best render.

usage: python retry_f5.py <render-dir> <reference-dir> [<line>...]

Without lines, takes every line whose render misses words. A line's score is the share of its
words, other than the game's names, that Whisper hears: Whisper can't spell "Gegarin" or "Berijev",
but a word it doesn't hear at all is missing from the render. Each try uses another seed, and a
short line gets more time than F5 would give it, since F5 squeezes short lines and drops their
first words. Updates checks.json with the best try of each line.
"""

import json
import os
import re
import shutil
import sys

import librosa
import whisper
from f5_tts.api import F5TTS

from speech_text import heard_share, spoken

render_dir, ref_dir = sys.argv[1], sys.argv[2]
lines = json.load(open(os.path.join(render_dir, "lines.json")))
checks_path = os.path.join(render_dir, "checks.json")
checks = json.load(open(checks_path))

def score_all():
    for name, check in checks.items():
        check["share"] = round(heard_share(check["heard"], check["words"]), 3)


asr = whisper.load_model("small.en")
score_all()
forced = sys.argv[3:]
todo = forced or [n for n, c in checks.items() if c["share"] < 0.9]
print(len(todo), "lines to render again:", " ".join(todo), flush=True)
model = F5TTS(model="F5TTS_v1_Base", device="mps")

for name in todo:
    line = lines[name]
    ref = os.path.join(ref_dir, f"{line['voice']}.wav")
    ref_text = open(os.path.join(ref_dir, f"{line['voice']}.txt")).read()
    ref_seconds = librosa.get_duration(path=ref)
    per_word = ref_seconds / max(1, len(ref_text.split()))
    words = len(line["words"].split())
    raw = os.path.join(render_dir, "raw", f"{name}.wav")
    attempt = os.path.join(render_dir, "raw", f"{name}.try.wav")
    # Lines named on the command line are rendered again whatever their old render's score.
    best = {**checks[name], "share": 0} if forced else checks[name]
    for number, seed in enumerate((11, 23, 37, 41, 53, 67)):
        # Short lines get room for a pause: F5 times a line by its share of the reference's words.
        stretch = 1.35 if words <= 6 else 1.15
        duration = ref_seconds + max(1.2, words * per_word * stretch) if number % 2 else None
        model.infer(ref_file=ref, ref_text=ref_text, gen_text=spoken(line["words"]), file_wave=attempt, seed=seed,
                    remove_silence=False, fix_duration=duration)
        heard = asr.transcribe(attempt, fp16=False)["text"].strip()
        share = heard_share(heard, line["words"])
        if share > best.get("share", 0):
            shutil.copy(attempt, raw)
            best = {**best, "heard": heard, "share": round(share, 3), "seed": seed, "fixed": duration is not None}
        if best["share"] >= 0.95:
            break
    os.remove(attempt)
    checks[name] = best
    json.dump(checks, open(checks_path, "w"), indent=1)
    print(f"{name}\t{best['share']:.2f}\t{best['heard']}", flush=True)

score_all()
json.dump(checks, open(checks_path, "w"), indent=1)
print("still missing words:", " ".join(n for n, c in checks.items() if c["share"] < 0.9))
