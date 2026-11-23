"""Fixes flaws of the Dreamcast's missions 12, 13 and 17 that leave them with no way to finish,
without the end their scripts give them, or with ships flying through rock, and writes the files
the mod ships.

    python3 patch_missions.py <the Dreamcast's mission files> <out folder>

The first folder holds the disc's mission12.dte, mission13.dte and mission17.dte, as `sltool hog
extract RESOURCE.HOG` writes them. Mission 22 needs no change.

The missions were made for older models of capital ships, which numbered their components
differently. The Dreamcast's own models number them as the PC's do, so the missions' numbers belong
to neither release. Older mission files on the PC's disc show some of the old numbers: mission 271,
an older version of mission 27, names the Pukov's shield generator 4 and aims torpedoes at its 0,
where mission 27 names the generator 6 and aims those torpedoes at 4, the hull.

Mission 17, the Pukov (the Gegarin):
- The shield generator was 4. The PC's Pukov numbers its hull 4 and its generator 6, so the script
  waited for the hull to go, made the hull invulnerable, and pointed the player at the hull. Every
  place the script names component 4 names 6: the two triggers on it, and the five commands that
  make it invulnerable, arm its ShotAt trigger and make it the player's target. One torpedo of the
  Cougars' first run is aimed at the old model's component 6, which on the PC is the generator,
  destroyed by then, so it's aimed at 4, the hull.
- The hull was 0. Two torpedoes are aimed at it, one of the first run and the one of the second run
  whose hit destroys the Gegarin. On the PC, 0 is the belly engine, which the first run can destroy,
  and a torpedo aimed at a destroyed component flies on without a target, so the Gegarin was never
  destroyed. Both are aimed at 4, the hull. `fixes17.luau` re-aims the torpedoes whose targets the
  old numbering leaves unknown.
- The part that counts the destroyed fighters ends with InterruptTriggerCode, which makes a
  trigger's code wait until its trigger fires again. The part runs on a thread of its own that no
  trigger started, so it waits forever and keeps its thread. The script has 32 threads, which the
  mission's other waiting code uses too. Once they run out, no new thread starts: kills go
  uncounted, the count can stop short of 11, and the generator's trigger can't run either. The
  original game runs the script the same way. Here MultiPlayerSync takes the command's place:
  outside a network game the thread yields once, then goes on to its return, and its thread ends.

Mission 22 names the Krasnaya's components by the old numbers too, her shield generator 7 and her
turrets 8 to 18 where the PC's model has 3 and 4 to 14. She takes the convoy cruisers' place where
she got away in mission 8, but the script sets `krasnaya_alive` to 0 as it starts, before it reads
it, so she never comes and her numbers are left as they are.

Mission 12: the part that plays the Reliant's lines as Kamov torpedoes hit her, and destroys her at
the fourth, waits between hits with InterruptTriggerCode. Each hit runs it on a thread of its own
that no trigger started, so each thread stops at its first wait: only the first hit's line plays,
and the fourth hit doesn't destroy her. MultiPlayerSync takes each wait's place, so each hit's
thread plays the line for the count of hits so far and ends.

Mission 13: the two Kurgans that patrol the Kafelnikof start beside the base, either side of it.
As they attack the 45th, they chase its fighters across the base, and the game's avoidance gives
up once a ship is inside the base's box, which is far larger than its rock: two ships that list
components never collide, so the Kurgans flew through the rock. They start 60000 nearer the
45th's jump-in point instead, ahead of the base, where they meet the wing on its way in. The waypoint the wing escorts the
boarding ship's second run to moves to the service hatch, where the mod's model has the port that
run docks at.

Mission 13 also sends the wing after the squad "(AI)Critical Kafelnikof defence", the satellites
and mines round the boarding ship's way in, but not the base's 16 turrets, which the mod's model
lets fire at it (`patch_kafelnikof.py`). A squad can hold single components of a ship, so the
turrets join the squad: 16 membership records after its own, the records after them moved down
into the section's spare room, the later squads' first records moved with them, and the section's
count raised.

Each byte is checked before it's changed, so the script refuses any other file.
"""
import os
import struct
import sys

# The sections' places in each file, from its directory (`sltool dte sections`): the same in both.
TRIGGERS = 0x3BBF7
SCRIPT = 0x47BF7
# A trigger's record and its component's place in it.
TRIGGER_SIZE = 0x30
TRIGGER_COMPONENT = 0x15
# `push_component`, and the commands that wait for a trigger and yield once.
PUSH_COMPONENT = 0x47
INTERRUPT_TRIGGER_CODE = bytes([0x21, 0x17])
MULTIPLAYER_SYNC = bytes([0x21, 0x2D])

# Mission 17: the Pukov's operand in the script; the triggers on its generator; the script's pushes
# of its components by their places in the script (`sltool dte script`), with the old number and the
# new; and the fighter count's InterruptTriggerCode.
PUKOV = 0x07
MISSION17_TRIGGERS = ((21, 4, 6), (22, 4, 6))
MISSION17_PUSHES = (
    (3226, 4, 6), (3734, 4, 6), (4380, 4, 6), (4933, 4, 6), (5038, 4, 6),
    # The first run's torpedo at the old generator, and the two at the old hull.
    (2528, 6, 4), (2624, 0, 4), (2704, 0, 4),
)
MISSION17_WAITS = (5043,)

# Mission 13: the Kurgans' and a waypoint's records, by the place of their positions in the file: the position the
# mission gives, and the copy the loader keeps, 0x14 bytes before it; and where each starts.
MISSION13_SHIP_POSITIONS = (
    (0x32D2B, (-72533.328125, 0.0, 98055.7578125), (-72533.328125, 0.0, 38055.7578125)),
    (0x32D77, (58466.66015625, 0.0, 98578.53125), (58466.66015625, 0.0, 38578.53125)),
    # "Limpet Dock Point 2", where the wing escorts the boarding ship's second run: over the
    # service hatch, where the mod's Kafelnikof has the port it docks at (`patch_kafelnikof.py`),
    # rather than over the bottom vent.
    (0x3357B, (5290.1875, 19731.9609375, 109207.015625), (11709.85, -26249.21, 95252.07)),
)
LOADER_COPY = -0x14

# Mission 13's squads and their membership records (sections 12 and 13, a record of 0x0C bytes
# each): a squad's first record at +0x08; a record's member's object ID at +0x00, its squad at
# +0x04 and its component at +0x08. The directory's entry for a section holds its count at +0 and
# its place at +4.
DIRECTORY_ENTRY = 8
SQUADS = 12
SQUAD_MEMBERS = 13
RECORD = 0x0C
SQUAD_FIRST = 0x08
MEMBER_SQUAD = 0x04
MEMBER_COMPONENT = 0x08
# The defence squad, its records, the Kafelnikof's object ID and its turrets' components.
DEFENCE = 6
DEFENCE_RECORDS = range(26, 35)
KAFELNIKOF = 19
TURRETS = range(8, 24)
SQUAD_COUNT = 21
MEMBER_COUNT = 95

# Mission 12: the Reliant's torpedo lines' three InterruptTriggerCodes.
MISSION12_WAITS = (4366, 4430, 4494)


class Mission:
    def __init__(self, name):
        self.name = name
        self.image = None

    def change(self, at, old, new):
        if self.image[at] != old:
            sys.exit(f"byte {at:#x} of {self.name} is {self.image[at]}, not {old}: this isn't the Dreamcast's {self.name}")
        self.image[at] = new

    def triggers(self, changes):
        for trigger, old, new in changes:
            self.change(TRIGGERS + trigger * TRIGGER_SIZE + TRIGGER_COMPONENT, old, new)

    def pushes(self, operand, changes):
        for at, old, new in changes:
            if self.image[SCRIPT + at:SCRIPT + at + 2] != bytes([PUSH_COMPONENT, operand]):
                sys.exit(f"the script at {at} isn't a push of the ship's component: this isn't the Dreamcast's {self.name}")
            self.change(SCRIPT + at + 2, old, new)

    def positions(self, changes):
        for at, old, new in changes:
            for place in (at, at + LOADER_COPY):
                if struct.unpack_from('<3f', self.image, place) != old:
                    sys.exit(f"the ship's position at {place:#x} isn't {old}: this isn't the Dreamcast's {self.name}")
                struct.pack_into('<3f', self.image, place, *new)

    def section(self, number):
        """The count and the place of section `number`."""
        count, = struct.unpack_from('<H', self.image, number * DIRECTORY_ENTRY)
        place, = struct.unpack_from('<I', self.image, number * DIRECTORY_ENTRY + 4)
        return count, place

    def squad_turrets(self):
        """The Kafelnikof's turrets join the defence squad."""
        squads, squads_at = self.section(SQUADS)
        members, members_at = self.section(SQUAD_MEMBERS)
        if (squads, members) != (SQUAD_COUNT, MEMBER_COUNT):
            sys.exit(f"{self.name} has {squads} squads and {members} squad members: this isn't the Dreamcast's {self.name}")
        record = lambda n: members_at + n * RECORD
        for n in DEFENCE_RECORDS:
            if struct.unpack_from('<H', self.image, record(n) + MEMBER_SQUAD)[0] != DEFENCE:
                sys.exit(f"squad member {n} of {self.name} isn't the defence squad's: this isn't the Dreamcast's {self.name}")
        after = DEFENCE_RECORDS.stop
        moved = bytes(self.image[record(after):record(members)])
        model = bytes(self.image[record(DEFENCE_RECORDS.start):record(DEFENCE_RECORDS.start + 1)])
        added = bytearray()
        for component in TURRETS:
            turret = bytearray(model)
            struct.pack_into('<H', turret, 0, KAFELNIKOF)
            turret[MEMBER_COMPONENT] = component
            added += turret
        self.image[record(after):record(members + len(TURRETS))] = added + moved
        struct.pack_into('<H', self.image, SQUAD_MEMBERS * DIRECTORY_ENTRY, members + len(TURRETS))
        for squad in range(DEFENCE + 1, squads):
            at = squads_at + squad * RECORD + SQUAD_FIRST
            first, = struct.unpack_from('<H', self.image, at)
            struct.pack_into('<H', self.image, at, first + len(TURRETS))

    def waits(self, places):
        for at in places:
            for offset, (old, new) in enumerate(zip(INTERRUPT_TRIGGER_CODE, MULTIPLAYER_SYNC)):
                self.change(SCRIPT + at + offset, old, new)


def patch(source, out, name, changes):
    mission = Mission(name)
    mission.image = bytearray(open(os.path.join(source, name), 'rb').read())
    changes(mission)
    open(os.path.join(out, name.lower()), 'wb').write(mission.image)


def main():
    source, out = sys.argv[1], sys.argv[2]
    patch(source, out, 'mission12.dte', lambda m: m.waits(MISSION12_WAITS))
    def mission13(m):
        m.positions(MISSION13_SHIP_POSITIONS)
        m.squad_turrets()
    patch(source, out, 'mission13.dte', mission13)

    def mission17(m):
        m.triggers(MISSION17_TRIGGERS)
        m.pushes(PUKOV, MISSION17_PUSHES)
        m.waits(MISSION17_WAITS)
    patch(source, out, 'mission17.dte', mission17)


if __name__ == '__main__':
    main()
