"""Writes radio22_lines.luau: the line that stands for each text mission 22 prints as its radio.

usage: python3 make_radio22.py <mission22.dte> <sltool> <mission22.md> <out.luau>

Mission 22 prints its draft radio with PrintDebugMessage. A text's argument, as the `vm_command`
hook gives it, is where the text's first character lies in the mission's file: the script
section's offset, plus its `push_string`'s offset in the script, plus the opcode and the length
byte. Each text is matched to the row of the document's radio table whose draft it is, and the
table gives the line's name, its speaker and the speaker's face film. A text with no row, such as
"Timer 4 Detroyed", is left out.
"""

import re
import subprocess
import sys

dte, sltool, document, out = sys.argv[1:5]
data = open(dte, "rb").read()

sections = subprocess.run([sltool, "dte", "sections", dte], capture_output=True, text=True, check=True).stdout
script_base = int(re.search(r"^\s*\d+\s+\d+\s+\S+\s+([0-9a-f]{8})\s+script$", sections, re.M).group(1), 16)

listing = subprocess.run([sltool, "dte", "script", dte], capture_output=True, text=True, check=True).stdout.splitlines()
printed = []
for at, line in enumerate(listing):
    text = re.match(r'\s*(\d+)\s+2[ab]\s.*push_string(?:_alt)?\s+"(.*)"$', line)
    if not text or at + 1 >= len(listing) or "command   PrintDebugMessage" not in listing[at + 1]:
        continue
    place = script_base + int(text.group(1)) + 2
    words = text.group(2)
    # The file holds the text there, ended by a zero.
    held = data[place:data.index(b"\0", place)].decode("latin-1")
    assert held == words.replace('\\"', '"'), (place, held, words)
    printed.append((place, held))


def normal(text):
    """A draft as compared: without the dashes that lead some, its spaces and its case."""
    return re.sub(r"\s+", " ", text.lstrip("-").replace("\\|", "|")).strip().lower()


rows = {}
for line in open(document):
    cells = [cell.strip() for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
    if len(cells) == 5 and cells[0].startswith("`ms"):
        face = re.search(r"`([^`]+)`", cells[1])
        speaker = cells[1].split(" (")[0].strip()
        rows.setdefault(normal(cells[4]), (cells[0].strip("`"), speaker, face.group(1) if face else None))

matched, unmatched = [], []
for place, text in printed:
    row = rows.get(normal(text))
    (matched if row else unmatched).append((place, text, row))

with open(out, "w") as lua:
    lua.write("-- radio22_lines.luau, made by make_radio22.py: the line that stands for each text mission 22\n")
    lua.write("-- prints as its radio, by the text's place in the mission's file, with its speaker and the\n")
    lua.write("-- speaker's face film.\n")
    lua.write("return {\n")
    for place, text, (name, speaker, face) in matched:
        quoted = speaker.replace('"', '\\"')
        lua.write(f'    [{place}] = {{ line = "{name}", speaker = "{quoted}", face = "{face}" }},\n')
    lua.write("}\n")

print(f"{len(printed)} texts printed, {len(matched)} matched to {len({r[2][0] for r in matched})} lines of {len(rows)}")
for place, text, _ in unmatched:
    print(f"  no line: {place}: {text}")
