"""Renumbers the Gegarin's components in mission 17, so that its script names the PC's Pukov's
parts, ends the part that counts the destroyed fighters properly, and writes the mission the mod
ships.

    python3 patch_mission17.py <the Dreamcast's mission17.dte> <out.dte>

The Dreamcast's file was made for an older Pukov model, which numbered its shield generator 4. The
PC's Pukov numbers its hull 4 and its shield generator 6, as mission 27 does, while mission 271, an
older version of mission 27 on the PC's disc, still names the generator 4. So the script waited for
the hull to go, made the hull invulnerable, and pointed the player at the hull, and destroying the
generator moved nothing on.

Here, every place the script names the Pukov's component 4 names 6: the two triggers on it, and the
five commands that make it invulnerable, arm its ShotAt trigger and make it the player's target.
One torpedo of the Cougars' first run is aimed at the old model's component 6, which on the PC is
the generator, destroyed by then, so it's aimed at 4, the hull, instead. The old model's other
numbers aren't known, so the torpedoes aimed at 0, 2 and 5 keep them.

The part that counts the destroyed fighters ends with InterruptTriggerCode, which makes a trigger's
code wait until its trigger fires again. The part runs on a thread of its own that no trigger
started, so it waits forever and keeps its thread. The script has 32 threads, which the mission's
other waiting code uses too. Once they run out, no new thread starts: kills go uncounted, the count
can stop short of 11, and the generator's trigger can't run either. The original game runs the
script the same way. Here MultiPlayerSync takes the
command's place: outside a network game the thread yields once, then goes on to its return, and its
thread ends.

Each byte is checked before it's changed, so the script refuses any other file.
"""
import sys

# The sections' places in the file, from its directory (`sltool dte sections`).
TRIGGERS = 0x3BBF7
SCRIPT = 0x47BF7
# A trigger's record, its component's place in it, and the triggers on the Pukov's component.
TRIGGER_SIZE = 0x30
COMPONENT = 0x15
TRIGGERS_ON_GENERATOR = (21, 22)
# `push_component`, and the operand that names the Pukov in the script.
PUSH_COMPONENT = 0x47
PUKOV = 0x07
# The script's commands that push the Pukov's component 4, and the torpedo's target, component 6,
# by their places in the script (`sltool dte script`).
PUSHES_OF_GENERATOR = (3226, 3734, 4380, 4933, 5038)
TORPEDO_AT_GENERATOR = 2528
OLD_GENERATOR, NEW_GENERATOR = 4, 6
# The fighter count's InterruptTriggerCode, by its place in the script, and the MultiPlayerSync
# that replaces it.
COUNT_WAIT = 5043
INTERRUPT_TRIGGER_CODE = bytes([0x21, 0x17])
MULTIPLAYER_SYNC = bytes([0x21, 0x2D])


def change(image, at, old, new):
    if image[at] != old:
        sys.exit(f"byte {at:#x} is {image[at]}, not {old}: this isn't the Dreamcast's mission17.dte")
    image[at] = new


def main():
    image = bytearray(open(sys.argv[1], 'rb').read())
    for trigger in TRIGGERS_ON_GENERATOR:
        change(image, TRIGGERS + trigger * TRIGGER_SIZE + COMPONENT, OLD_GENERATOR, NEW_GENERATOR)
    for at in PUSHES_OF_GENERATOR + (TORPEDO_AT_GENERATOR,):
        old = OLD_GENERATOR if at != TORPEDO_AT_GENERATOR else NEW_GENERATOR
        new = NEW_GENERATOR if at != TORPEDO_AT_GENERATOR else OLD_GENERATOR
        if image[SCRIPT + at:SCRIPT + at + 2] != bytes([PUSH_COMPONENT, PUKOV]):
            sys.exit(f"the script at {at} isn't a push of the Pukov's component: this isn't the Dreamcast's mission17.dte")
        change(image, SCRIPT + at + 2, old, new)
    for offset, (old, new) in enumerate(zip(INTERRUPT_TRIGGER_CODE, MULTIPLAYER_SYNC)):
        change(image, SCRIPT + COUNT_WAIT + offset, old, new)
    open(sys.argv[2], 'wb').write(image)


if __name__ == '__main__':
    main()
