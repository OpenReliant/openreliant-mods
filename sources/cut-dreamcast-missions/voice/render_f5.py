"""Renders the cut missions' lines with F5-TTS, each from its voice's reference clip.

usage: python render_f5.py <scripts-dir> <reference-dir> <out-dir> <seed> [<line>...]

Without lines, renders every line of the four documents that has no render yet; with lines, renders
those again. Each goes to <out-dir>/raw/<line>.wav, and <out-dir>/lines.json lists every line's
voice and words, which check_f5.py reads.
"""

import json
import os
import re
import sys

from f5_tts.api import F5TTS

scripts_dir, ref_dir, out_dir, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
again = sys.argv[5:]
raw_dir = os.path.join(out_dir, "raw")
os.makedirs(raw_dir, exist_ok=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voices  # noqa: E402


def script_lines():
    lines = {}
    for mission in ("12", "13", "17", "22"):
        for row in open(os.path.join(scripts_dir, f"mission{mission}.md")):
            if not row.startswith("| `"):
                continue
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            name = cells[0].strip("`")
            speaker = re.sub(r"\s*\(.*\)$", "", cells[1]).replace(", dying", "").strip()
            words = re.sub(r"\*\(.*?\)\*", "", cells[3])
            words = re.sub(r"^\(.*?\)\s*", "", words).strip()
            if name not in lines:
                lines[name] = {"voice": voices.speakers[speaker], "words": words}
    return lines


lines = script_lines()
json.dump(lines, open(os.path.join(out_dir, "lines.json"), "w"), indent=1)
todo = again or [name for name in lines if not os.path.exists(os.path.join(raw_dir, f"{name}.wav"))]
print(len(todo), "lines to render", flush=True)
model = F5TTS(model="F5TTS_v1_Base", device="mps")
references = {}
for name in todo:
    voice = lines[name]["voice"]
    if voice not in references:
        references[voice] = (os.path.join(ref_dir, f"{voice}.wav"), open(os.path.join(ref_dir, f"{voice}.txt")).read())
    ref_file, ref_text = references[voice]
    model.infer(ref_file=ref_file, ref_text=ref_text, gen_text=lines[name]["words"],
                file_wave=os.path.join(raw_dir, f"{name}.wav"), seed=seed, remove_silence=False)
    print("rendered", name, flush=True)
