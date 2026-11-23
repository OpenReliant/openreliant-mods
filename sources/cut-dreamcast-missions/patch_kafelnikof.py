"""Finishes the Kafelnikof's turrets, and writes the model the mod ships.

    sltool shp gltf Kafelnikof.SHP kafelnikof.gltf
    python3 patch_kafelnikof.py Kafelnikof.SHP kafelnikof.gltf <out folder>

`Kafelnikof.SHP` is the game's, out of its `resource.hog` (`sltool hog extract resource.hog
<folder>`), and the glTF file is `sltool`'s export of it, which gives the script the model's
geometry. The Kafelnikof is the base of mission 13, a mission cut from the PC's campaign, and no
released mission places it. The Dreamcast's model has the same parts, mounts and arcs.

The base carries 16 turrets, the components after its own eight. A Coalition turret stands up from
its mount along its own -Y axis, its two barrels point along its -Z, and it can only raise them,
turning about its X axis: it fires across one plane through its mount. Three of the base's turrets
are finished, those on the comms tower's first mount and the landing platform's second and third:
each stands on the rock and has a firing arc, the directions it may fire in. The other 13 aren't:

- 10 of them stand upside down, their bodies sunk in the rock;
- their arcs are empty, so the game never lets them fire;
- and the fighters' attack runs on them pull out along no direction.

For each of those 13, the script stands the turret on the rock, its Y axis into it, and turns it
about that axis so that its barrels face along the 45th's approach, the base's +Z, or across it,
in turn, so that each side of the base covers both. Its arc is open in the directions where its
line of fire is clear of the base, cast from just above it against the faces the base shows while
it is whole, and its attack runs pull out away from the rock. The three finished turrets keep what they have.

The base's two docking ports, where the boarding ship docks, point out of the rock. The boarding
ship slides in along a port's Z axis, nose first, and stands turned as the port is, so it docked
with its body sunk in the rock. Each port turns over, its Z axis into the rock. The second run
docks at the first port, on the bottom vent, though the mission has the wing blow the service
hatch, the top vent, for it, and the top vent has no port. A port on the hatch would go with it, so
the bottom vent's port moves to the hatch instead: the hatch is sunk in the rock, so the port
stands where the line out across the hatch's faces leaves the rock, its Z axis back down it. The bottom vent stays whole in the mission, so its port stays.

The machinery the mission points the player at has no part class, so the target display shows no
name or icon for it. The cloak generator, "Kaf shield gen", becomes a shield generator, the comms
tower a comms transmitter, and the top vent, the service hatch, a vent hatch. A shield generator
brings the game's rules for one: while it stands, a light hit on the base does a quarter of its
damage, and a hit on a component flares the base's shield.

The script checks the game's file's SHA-256 first, so it refuses any other file.
"""
import hashlib
import json
import math
import os
import struct
import sys

# The game's file, which the script expects.
SHA256 = '035e1358da3d65af23faf12199f3cf489d06dd669fa3f666fcfe0fa93bb3f15f'

# The attachment record: its kind, its position on its part, and its axes, a row-major 3x3 whose
# columns are the turret's X, Y and Z axes in the part's frame. The parts of this model stand in
# the model's own frame, unturned.
KIND = 0x00
POSITION = 0x04
ORIENTATION = 0x10
GUN = 1

# The docking ports, attachments of kind 9, by their positions on their parts as whole numbers: the
# bottom vent's, which moves to the hatch, and the landing platform's.
DOCK = 9
BOTTOM_VENT_PORT = (148, -1796, 116)
LANDING_PORT = (708, -3067, -3629)
HATCH = 'Kaf top vent'
# How finely the way out of the rock over the hatch is measured.
HATCH_STEP = 50
BOTTOM_VENT = 'Kaf bot vent'

# The parts' chunk: its tag, record size and count. A part record holds its name, 64 bytes, then
# its class, and its flags, of which one marks a damaged model, hidden while its part is whole.
PARTS = 23
PART_SIZE = 312
PART_CHUNK = struct.pack('<3H', 0x01, PART_SIZE, PARTS)
PART_CLASS = 0x40
PART_FLAGS = 0xF0
DAMAGED = 0x04
# The classes the machinery takes (`shp.Part.Class`), by its parts' names.
CLASSES = (("Kaf shield gen", 6), ("Kaf comms twr", 7), ("Kaf top vent", 17))

# The firing arcs' chunk: its tag, record size and count, then a record for each component: the
# way an attack run pulls out, then 32 rows of 16 bits.
ARC_CHUNK = struct.pack('<3H', 0x10, 76, 24)
ARC_SIZE = 76
ARC_ROWS = 0x0C

# The turret mounts, in the model's order of parts and attachments, by their positions on their
# parts as whole numbers. The first turret is the base's component 8, and the rest follow.
MOUNTS = (
    # Kaf BODY
    (-9421, 22487, -8436), (10309, 20852, -4506), (30788, 12884, -5570), (-17270, -19969, -1580),
    (-9185, 5517, -21657), (24100, -19089, -1466), (-7606, -20861, -3212),
    # Kaf comms twr
    (-2083, 1748, -1119), (5698, -1517, 903), (2484, 13209, 412),
    # Kaf ext vent
    (-102, -896, 758),
    # Kaf land plat
    (2278, -12447, 2049), (5163, 4671, -8499), (-8176, 4825, -8650), (-3501, -8851, 2221),
    # Kaf shield gen
    (-1145, 7497, -2765),
)
FIRST_TURRET = 8
FINISHED = {7, 12, 13}

# Where the 45th comes from, in the model's frame as glTF has it.
APPROACH = (0.0, 0.0, 1.0)

# How far above its mount a turret's line of fire starts, and how far it reaches.
TURRET_HEIGHT = 600.0
REACH = 200000.0

# How many directions each turret's arc is cast in.
SAMPLES = 1500

# The game's arc cells (`turret_aim_angles`): 32 rows about Y, and columns from Y.
ROWS_PER_RADIAN = 32 / math.tau
COLUMNS_PER_RADIAN = 64 / math.tau


# --- Vectors ---------------------------------------------------------------------------------------

def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def unit(a):
    return scale(a, 1 / math.sqrt(dot(a, a)))


def turn(q, v):
    """`v` turned by the quaternion `q`, as glTF gives it (x, y, z, w)."""
    axis, w = q[:3], q[3]
    t = scale(cross(axis, v), 2)
    return add(add(v, scale(t, w)), cross(axis, t))


def from_gltf(v):
    """`sltool shp gltf` turns the model a half turn about Z (`Vec3.toYUp`); this turns a direction
    back."""
    return (-v[0], -v[1], v[2])


def axes_from_gltf(x, y, z):
    """A mount's axes, as columns of its record's matrix, from its axes in glTF. The export turns
    the mount's own frame with the model's, so its X and Y axes come back the other way round."""
    return [scale(from_gltf(x), -1), scale(from_gltf(y), -1), from_gltf(z)]


# --- The geometry ----------------------------------------------------------------------------------

def shells_and_mounts(path, drawn):
    """The faces of the base's parts named in `drawn`, a list for each; each turret mount's part's
    place, its own place and its Y axis; and those parts' places and faces by their names; in the
    model's frame as glTF has it."""
    gltf = json.load(open(path))
    folder = os.path.dirname(path)
    buffers = [open(os.path.join(folder, b['uri']), 'rb').read() for b in gltf['buffers']]

    def accessor(index):
        a = gltf['accessors'][index]
        view = gltf['bufferViews'][a['bufferView']]
        start = view.get('byteOffset', 0) + a.get('byteOffset', 0)
        width = {'SCALAR': 1, 'VEC3': 3}[a['type']]
        code = {5126: 'f', 5125: 'I', 5123: 'H'}[a['componentType']]
        stride = view.get('byteStride', struct.calcsize(code) * width)
        data = buffers[view['buffer']]
        return [struct.unpack_from('<' + code * width, data, start + k * stride) for k in range(a['count'])]

    nodes = gltf['nodes']
    shells, mounts, parts = [], [], {}
    for node in nodes:
        name = node.get('name', '')
        at = tuple(node.get('translation', (0, 0, 0)))
        if 'mesh' in node and name in drawn:
            shell = []
            for primitive in gltf['meshes'][node['mesh']]['primitives']:
                points = [add(at, p) for p in accessor(primitive['attributes']['POSITION'])]
                order = [i[0] for i in accessor(primitive['indices'])] if 'indices' in primitive else list(range(len(points)))
                shell += [(points[order[k]], points[order[k + 1]], points[order[k + 2]]) for k in range(0, len(order), 3)]
            shells.append(shell)
            parts[name] = (at, shell)
        for child in node.get('children', []):
            mount = nodes[child]
            if mount.get('name', '').startswith('gun'):
                place = add(at, tuple(mount.get('translation', (0, 0, 0))))
                mounts.append((at, place, turn(mount.get('rotation', (0, 0, 0, 1)), (0, 1, 0))))
    if len(mounts) != len(MOUNTS):
        sys.exit(f'the glTF file has {len(mounts)} turret mounts, not {len(MOUNTS)}')
    return shells, mounts, parts


def crossings(faces, origin, direction, reach):
    """How many of `faces` the ray from `origin` along `direction` crosses within `reach`."""
    return len(distances(faces, origin, direction, reach))


def blocked(shells, origin, direction, reach):
    """Whether the ray from `origin` along `direction` meets the base within `reach`."""
    return any(crossings(shell, origin, direction, reach) for shell in shells)


def distances(faces, origin, direction, reach):
    """How far along the ray from `origin` along `direction` it crosses each of `faces` it crosses
    within `reach`."""
    found = []
    for a, b, c in faces:
        e1, e2 = sub(b, a), sub(c, a)
        h = cross(direction, e2)
        det = dot(e1, h)
        if abs(det) < 1e-9:
            continue
        s = sub(origin, a)
        u = dot(s, h) / det
        if u < 0 or u > 1:
            continue
        q = cross(s, e1)
        v = dot(direction, q) / det
        if v < 0 or u + v > 1:
            continue
        t = dot(e2, q) / det
        if 1 < t < reach:
            found.append(t)
    return found


def inside(shells, point):
    """Whether `point` is inside the base: inside one of its parts, where most of three rays cross
    the part's faces an odd number of times. The parts overlap, so each is tested on its own."""
    rays = ((0.577, 0.577, 0.577), (-0.3, 0.9, 0.31), (0.8, -0.2, 0.56))
    return any(sum(crossings(shell, point, unit(r), math.inf) % 2 for r in rays) >= 2 for shell in shells)


# --- The turrets -----------------------------------------------------------------------------------

def standing(shells, place, y, across):
    """The axes of a turret mounted at `place`, its old Y axis `y`: Y into the rock, and the barrels
    along the approach, or `across` it. Each in the model's frame as glTF has it."""
    inward = scale(y, -1) if inside(shells, add(place, scale(y, -TURRET_HEIGHT))) else y
    along = sub(APPROACH, scale(inward, dot(APPROACH, inward)))
    along = unit(along) if dot(along, along) > 1e-6 else (1.0, 0.0, 0.0)
    barrels = unit(cross(inward, along)) if across else along
    z = scale(barrels, -1)
    return cross(inward, z), inward, z


def cell(w):
    """The arc cell the game reads first for the direction `w` in the model's frame
    (`turret_aim_angles`): its row, and its column, which the game takes the other way round."""
    around = math.atan2(w[0], w[2])
    upward = math.atan2(math.sqrt(w[0] * w[0] + w[2] * w[2]), w[1])
    row = round((around + math.tau) * ROWS_PER_RADIAN - 0.5) & 31
    column = round((upward + math.tau) * COLUMNS_PER_RADIAN - 0.5)
    return row, -column & 15


def directions(count):
    """`count` directions spread evenly over the sphere."""
    golden = math.pi * (3 - math.sqrt(5))
    for k in range(count):
        y = 1 - 2 * (k + 0.5) / count
        r = math.sqrt(1 - y * y)
        yield (r * math.cos(golden * k), y, r * math.sin(golden * k))


def arc(shells, place, inward):
    """The rows of the firing arc of a turret at `place` standing on the rock along `inward`: a
    cell is open where most of the directions in it are clear of the base."""
    origin = add(place, scale(inward, -TURRET_HEIGHT))
    clear = [[0] * 16 for _ in range(32)]
    seen = [[0] * 16 for _ in range(32)]
    for d in directions(SAMPLES):
        row, column = cell(from_gltf(d))
        seen[row][column] += 1
        if not blocked(shells, origin, d, REACH):
            clear[row][column] += 1
    return [sum(1 << c for c in range(16) if seen[r][c] and 2 * clear[r][c] >= seen[r][c]) for r in range(32)]


# --- The file --------------------------------------------------------------------------------------

def position_at(data, at, kind=GUN):
    """The position of an attachment of kind `kind` at `at`, as whole numbers, or None."""
    if struct.unpack_from('<I', data, at + KIND)[0] != kind:
        return None
    values = struct.unpack_from('<3f', data, at + POSITION)
    if not all(math.isfinite(v) for v in values):
        return None
    return tuple(round(v) for v in values)


def find_attachment(data, position, kind):
    """The offset of the one attachment of kind `kind` at `position`. The file's chunks follow one
    another unaligned, so every byte is a place to look."""
    places = [at for at in range(len(data) - ORIENTATION - 36) if position_at(data, at, kind) == position]
    if len(places) != 1:
        sys.exit(f'the attachment at {position} is in the file {len(places)} times, not once')
    return places[0]


def find_mounts(data):
    """The offset of each mount's record, in the order of `MOUNTS`."""
    return [find_attachment(data, position, GUN) for position in MOUNTS]


def turn_port_over(data, at):
    """A half turn of the port at `at` about its own X axis: its Y and Z axes, the last two columns
    of its axes, point the other way."""
    axes = list(struct.unpack_from('<9f', data, at + ORIENTATION))
    for column in (1, 2):
        for row in range(3):
            axes[row * 3 + column] = -axes[row * 3 + column]
    struct.pack_into('<9f', data, at + ORIENTATION, *axes)


def sum_of(vectors):
    total = (0.0, 0.0, 0.0)
    for v in vectors:
        total = add(total, v)
    return total


def hatch_port(shells, parts):
    """Where the hatch's port stands, and its axes: over the middle of the hatch, where its line
    across the hatch's faces comes out of the rock, the hatch being sunk in it, and its Z axis back
    down that line. Each in the model's frame as glTF has it."""
    _, faces = parts[HATCH]
    corners = [corner for face in faces for corner in face]
    middle = scale(sum_of(corners), 1 / len(corners))
    across = unit(sum_of([cross(sub(b, a), sub(c, a)) for a, b, c in faces]))
    rock = [shell for shell in shells if shell is not faces]
    reach = {}
    for way in (across, scale(across, -1)):
        reach[way] = next((t for t in range(0, int(REACH), HATCH_STEP) if not inside(rock, add(middle, scale(way, t)))), None)
    out = min((way for way in reach if reach[way] is not None), key=lambda way: reach[way])
    middle = add(middle, scale(out, reach[out]))
    z = scale(out, -1)
    across = (1.0, 0.0, 0.0) if abs(z[0]) < 0.9 else (0.0, 1.0, 0.0)
    y = unit(cross(z, across))
    return middle, (cross(y, z), y, z)


def move_ports(data, shells, parts):
    """Turns the landing platform's port over, and moves the bottom vent's to the hatch."""
    turn_port_over(data, find_attachment(data, LANDING_PORT, DOCK))
    record = find_attachment(data, BOTTOM_VENT_PORT, DOCK)
    place, (x, y, z) = hatch_port(shells, parts)
    vent, _ = parts[BOTTOM_VENT]
    axes = axes_from_gltf(x, y, z)
    struct.pack_into('<3f', data, record + POSITION, *from_gltf(sub(place, vent)))
    struct.pack_into('<9f', data, record + ORIENTATION, *(axes[c][r] for r in range(3) for c in range(3)))


def find_arcs(data):
    """The offset of the first firing arc."""
    at = data.find(ARC_CHUNK)
    if at < 0 or data.find(ARC_CHUNK, at + 1) >= 0:
        sys.exit('the firing arcs are not in the file once')
    return at + len(ARC_CHUNK)


def drawn_parts(data):
    """The names of the parts drawn while the base is whole: those without the flag of a damaged
    model (`shp.Part.Flags.damaged`), such as the body's damaged model, Line01, and the
    machinery's DEST parts."""
    start = data.find(PART_CHUNK)
    if start < 0 or data.find(PART_CHUNK, start + 1) >= 0:
        sys.exit('the parts are not in the file once')
    names = set()
    for number in range(PARTS):
        at = start + len(PART_CHUNK) + number * PART_SIZE
        name = bytes(data[at:at + 64]).split(b'\0')[0].decode('latin1')
        if not struct.unpack_from('<I', data, at + PART_FLAGS)[0] & DAMAGED:
            names.add(name)
    return names


def give_classes(data):
    """Gives the machinery the mission points the player at its classes (`CLASSES`)."""
    for name, part_class in CLASSES:
        key = name.encode() + b'\0'
        at = data.find(key)
        if at < 0 or data.find(key, at + 1) >= 0:
            sys.exit(f'the part {name} is not in the file once')
        if struct.unpack_from('<I', data, at + PART_CLASS)[0] != 0:
            sys.exit(f'the part {name} already has a class')
        struct.pack_into('<I', data, at + PART_CLASS, part_class)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    source, exported, out = sys.argv[1:]
    data = bytearray(open(source, 'rb').read())
    if hashlib.sha256(data).hexdigest() != SHA256:
        sys.exit(f'{source} is not the game\'s Kafelnikof.SHP')
    shells, mounts, parts = shells_and_mounts(exported, drawn_parts(data))
    arcs = find_arcs(data)
    unfinished = 0
    for number, ((part, place, y), record) in enumerate(zip(mounts, find_mounts(data))):
        if number in FINISHED:
            continue
        x, inward, z = standing(shells, place, y, unfinished % 2 == 1)
        unfinished += 1
        axes = axes_from_gltf(x, inward, z)
        struct.pack_into('<9f', data, record + ORIENTATION, *(axes[c][r] for r in range(3) for c in range(3)))
        component = arcs + (FIRST_TURRET + number) * ARC_SIZE
        struct.pack_into('<3f', data, component, *from_gltf(scale(inward, -1)))
        struct.pack_into('<32H', data, component + ARC_ROWS, *arc(shells, place, inward))
    move_ports(data, shells, parts)
    give_classes(data)
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'Kafelnikof.SHP'), 'wb') as file:
        file.write(data)


if __name__ == '__main__':
    main()
