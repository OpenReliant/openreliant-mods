# Worn textures for the Viper's hull: colour, metal and roughness, and a normal map.
# Run from sources/viper/worn; writes hull_color.png, hull_mr.png and hull_normal.png, which
# go in ../textures. Needs Python 3 and ImageMagick 7.
import random, subprocess, math, array
W, H = 2048, 4096
S = W / 512
def sh(*a): subprocess.run(a, check=True)
src = '../textures/09_-_Default.001_baseColor.png'
random.seed(11)

# Panel seams, in the 512 by 1024 picture's pixels, along the projections' sections.
seams = [
    # side view, top section
    ((0, 178), (420, 178)), ((0, 246), (330, 246)), ((110, 150), (110, 285)), ((205, 145), (205, 290)), ((330, 150), (330, 290)),
    # top view, middle section
    ((60, 425), (470, 415)), ((60, 590), (470, 600)), ((118, 400), (118, 615)), ((237, 385), (237, 625)), ((355, 378), (355, 635)), ((470, 376), (470, 640)),
    # side view, bottom section
    ((40, 800), (410, 800)), ((40, 862), (420, 862)), ((140, 760), (140, 990)), ((260, 770), (260, 990)), ((385, 765), (385, 1000)),
]
def svg(name, body, width):
    open(name, 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="black"/><g stroke="white" stroke-width="{width}" stroke-linecap="round" fill="none">{body}</g></svg>')
seam_body = ''.join(f'<line x1="{a[0]*S}" y1="{a[1]*S}" x2="{b[0]*S}" y2="{b[1]*S}"/>' for a, b in seams)
# rivets along the seams, every 24 texels
rivets = ''
for a, b in seams:
    n = int(math.dist(a, b) * S / 28)
    for i in range(1, n):
        t = i / n
        x, y = a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t
        dx, dy = b[0]-a[0], b[1]-a[1]; l = math.hypot(dx, dy)
        ox, oy = -dy/l*6, dx/l*6
        rivets += f'<circle cx="{x*S+ox:.1f}" cy="{y*S+oy:.1f}" r="1.6"/>'
# Hatches and access panels: rounded outlines, finer than the seams, each a little lighter or
# darker than the hull. Vents: rows of short slots. All in the 512 by 1024 picture's pixels, clear
# of the stripes and the lettering.
hatches = [
    # side view, top section
    (40, 190, 95, 236), (125, 252, 195, 282), (220, 186, 288, 238), (22, 140, 100, 170),
    # top view, middle section
    (130, 432, 222, 470), (262, 430, 340, 468), (130, 572, 222, 584), (262, 574, 340, 588), (392, 470, 455, 560),
    # side view, bottom section
    (60, 812, 130, 852), (60, 880, 180, 960), (400, 810, 470, 856),
]
vents = [
    # left, top, right, slots
    (300, 254, 330, 5), (400, 880, 470, 8), (150, 760, 200, 4),
]
hatch_body = ''.join(f'<rect x="{l*S}" y="{t*S}" width="{(r-l)*S}" height="{(b-t)*S}" rx="{3*S}"/>' for l, t, r, b in hatches)
vent_body = ''
for l, t, r, n in vents:
    for i in range(n):
        y = (t + i * 6) * S
        vent_body += f'<line x1="{l*S}" y1="{y}" x2="{r*S}" y2="{y}" stroke-width="{2.2*S}"/>'
svg('seams.svg', seam_body + f'<g stroke-width="2">{hatch_body}</g>' + vent_body, 3)
tones = ''.join(f'<rect x="{l*S}" y="{t*S}" width="{(r-l)*S}" height="{(b-t)*S}" rx="{3*S}" fill="{random.choice(["#606060", "#a0a0a0", "#707070", "#909090"])}"/>' for l, t, r, b in hatches)
open('tones.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="#808080"/>{tones}</svg>')
sh('magick', 'tones.svg', '-colorspace', 'gray', 'tones.png')
open('rivets.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" fill="black"/><g fill="white">{rivets}</g></svg>')
# Scratches: short, mostly along the hull, thin.
lines = []
for _ in range(500):
    x, y = random.uniform(0, W), random.uniform(0, H)
    angle = random.gauss(0, 0.35) + (math.pi if random.random() < 0.5 else 0)
    length = random.expovariate(1 / 40) + 6
    bend = random.uniform(-0.15, 0.15)
    pts = []
    for i in range(6):
        t = i / 5
        a = angle + bend * t
        pts.append(f'{x + math.cos(a)*length*t:.1f},{y + math.sin(a)*length*t:.1f}')
    lines.append(f'<polyline points="{" ".join(pts)}" stroke-opacity="{random.uniform(0.3, 1):.2f}"/>')
svg('scratches.svg', ''.join(lines), 1.3)
sh('magick', '-background', 'black', 'seams.svg', '-colorspace', 'gray', 'seams.png')
sh('magick', '-background', 'black', 'rivets.svg', '-colorspace', 'gray', 'rivets.png')
sh('magick', '-background', 'black', 'scratches.svg', '-colorspace', 'gray', 'scratches.png')

# The livery, four times as large.
sh('magick', src, '-filter', 'Lanczos', '-resize', f'{W}x{H}!', '-alpha', 'off', 'base.png')
# Grime: broad blotches, and finer dirt.
sh('magick', '-size', f'{W//8}x{H//8}', '-seed', '3', 'plasma:grey50-grey50', '-colorspace', 'gray', '-resize', f'{W}x{H}!', '-blur', '0x24', '-auto-level', '-level', '35%,100%', 'grime.png')
sh('magick', '-size', f'{W//2}x{H//2}', '-seed', '5', 'plasma:grey50-grey50', '-colorspace', 'gray', '-resize', f'{W}x{H}!', '-blur', '0x2', '-auto-level', 'dirt.png')
# Streaks along the hull: noise stretched along x, which the projections lay along the ship.
sh('magick', '-size', f'64x{H}', '-seed', '9', 'xc:', '+noise', 'Random', '-colorspace', 'gray', '-blur', '0x1.2', '-resize', f'{W}x{H}!', '-blur', '0x4', '-auto-level', '-level', '45%,100%', 'streaks.png')
# Chips: where fine noise peaks, more often round the stripes' edges and the seams.
# The stripes: where red stands well above green, which the lettering's grey edges don't.
sh('magick', 'base.png', '(', '-clone', '0', '-channel', 'R', '-separate', '+channel', ')', '(', '-clone', '0', '-channel', 'G', '-separate', '+channel', ')', '-delete', '0', '-compose', 'MinusSrc', '-composite', '-threshold', '12%', 'stripes.png')
# The stripes a deeper, cleaner red than the source's brownish one.
sh('magick', 'base.png', '(', '-size', f'{W}x{H}', 'xc:#80201D', ')', '(', 'stripes.png', '-blur', '0x1', ')', '-composite', 'base_red0.png')
# Faded red: the stripes rubbed lighter and greyer in patches, streaked along the hull.
sh('magick', '-size', f'{W//16}x{H//16}', '-seed', '29', 'plasma:grey50-grey50', '-colorspace', 'gray', '-resize', f'{W}x{H}!', '-blur', '0x10', '-auto-level', '-level', '35%,90%', '(', 'stripes.png', '-blur', '0x1', ')', '-compose', 'Multiply', '-composite', '+level', '0,60%', 'fade.png')
sh('magick', 'base_red0.png', '(', '-size', f'{W}x{H}', 'xc:#9c6e6a', ')', 'fade.png', '-composite', 'base_red.png')
sh('magick', 'stripes.png', '-morphology', 'EdgeIn', 'Disk:3', '-blur', '0x10', '-auto-level', 'edges.png')
sh('magick', 'seams.png', '-blur', '0x14', '-auto-level', 'seamband.png')
sh('magick', '-size', f'{W//2}x{H//2}', '-seed', '13', 'xc:', '+noise', 'Random', '-colorspace', 'gray', '-blur', '0x1.6', '-auto-level', '-resize', f'{W}x{H}!', 'chipfine.png')
sh('magick', '-size', f'{W//16}x{H//16}', '-seed', '17', 'plasma:grey50-grey50', '-colorspace', 'gray', '-resize', f'{W}x{H}!', '-blur', '0x20', '-auto-level', 'chipbroad.png')
sh('magick', 'chipfine.png', 'chipbroad.png', '-compose', 'Mathematics', '-define', 'compose:args=0,0.35,0.65,0', '-composite', 'chipnoise.png')
sh('magick', 'edges.png', 'seamband.png', '-compose', 'Lighten', '-composite', '-level', '0,100%', 'wearband.png')
# a chip shows where the noise rises above a threshold that the wear band lowers
sh('magick', 'chipnoise.png', 'wearband.png', '-compose', 'Mathematics', '-define', 'compose:args=0,0.3,1,0', '-composite', '-threshold', '84%', '-morphology', 'Open', 'Disk:1', '-blur', '0x0.7', 'chips.png')

# Scuffs: dark smears, each a blot dragged in a direction of its own.
scuffs = []
for _ in range(140):
    x, y = random.uniform(0, W), random.uniform(0, H)
    length = random.uniform(20, 140)
    angle = random.gauss(0, 0.5) + random.choice((0, math.pi))
    width = random.uniform(3, 14)
    dx, dy = math.cos(angle) * length, math.sin(angle) * length
    scuffs.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+dx:.0f}" y2="{y+dy:.0f}" stroke-width="{width:.1f}" stroke-opacity="{random.uniform(0.25, 0.8):.2f}"/>')
svg('scuffs.svg', ''.join(scuffs), 6)
sh('magick', '-background', 'black', 'scuffs.svg', '-colorspace', 'gray', '-blur', '0x4', '(', 'dirt.png', '-level', '20%,80%', ')', '-compose', 'Multiply', '-composite', '-negate', '+level', '72%,100%', 'scuffmul.png')

# Colour: the livery dimmed by grime and streaks, seams darker, chips bare metal, scratches bright.
sh('magick', 'grime.png', '-negate', '+level', '84%,100%', 'grimemul.png')
sh('magick', 'streaks.png', 'grime.png', '-compose', 'Multiply', '-composite', '-negate', '+level', '86%,100%', 'streakmul.png')
sh('magick', 'dirt.png', '-negate', '+level', '93%,100%', 'dirtmul.png')
sh('magick', 'seams.png', '-blur', '0x1', '-negate', '+level', '62%,100%', 'seammul.png')
sh('magick', 'rivets.png', '-negate', '+level', '75%,100%', 'rivetmul.png')
sh('magick', 'tones.png', '-evaluate', 'Multiply', '0.24', '-evaluate', 'Add', '88%', 'tonemul.png')
sh('magick', 'base_red.png', 'grimemul.png', '-compose', 'Multiply', '-composite',
   'streakmul.png', '-compose', 'Multiply', '-composite',
   'dirtmul.png', '-compose', 'Multiply', '-composite',
   'seammul.png', '-compose', 'Multiply', '-composite',
   'rivetmul.png', '-compose', 'Multiply', '-composite',
   'tonemul.png', '-compose', 'Multiply', '-composite',
   'scuffmul.png', '-compose', 'Multiply', '-composite', 'painted.png')
sh('magick', '-size', f'{W}x{H}', 'xc:#6c6f72', 'metal.png')
# The lettering flakes, showing the hull's paint under it: dark texels away from the stripes,
# where the chip noise is high, take the paint's colour.
sh('magick', 'base.png', '-colorspace', 'gray', '-threshold', '30%', '-negate', '(', 'stripes.png', '-morphology', 'Dilate', 'Disk:4', '-negate', ')', '-compose', 'Multiply', '-composite', 'text.png')
sh('magick', '-size', f'{W//6}x{H//6}', '-seed', '23', 'xc:', '+noise', 'Random', '-colorspace', 'gray', '-blur', '0x1', '-auto-level', '-resize', f'{W}x{H}!', '-threshold', '63%', 'text.png', '-compose', 'Multiply', '-composite', '-blur', '0x0.6', 'textchips.png')
sh('magick', '-size', f'{W}x{H}', 'xc:#b9bbbd', 'underpaint.png')
sh('magick', 'painted.png', 'underpaint.png', 'textchips.png', '-composite', 'painted_text.png')
sh('magick', 'painted_text.png', 'metal.png', 'chips.png', '-composite', 'chipped.png')
sh('magick', '-size', f'{W}x{H}', 'xc:#aeb2b6', 'bright.png')
sh('magick', 'scratches.png', '+level', '0,30%', 'scratchmask.png')
sh('magick', 'chipped.png', 'bright.png', 'scratchmask.png', '-composite', '-depth', '8', 'hull_color.png')

# Metal and roughness (glTF's: roughness green, metalness blue): satin paint, rougher where
# grimy, bare metal where chipped or scratched.
sh('magick', 'grime.png', '+level', '55%,75%', '(', 'scuffmul.png', '-negate', '+level', '0,40%', ')', '-compose', 'Plus', '-composite', 'rough_paint.png')
sh('magick', 'chips.png', 'scratchmask.png', '-compose', 'Lighten', '-composite', 'bare.png')
sh('magick', 'rough_paint.png', '(', '-size', f'{W}x{H}', 'xc:gray38', ')', 'bare.png', '-composite', 'rough.png')
sh('magick', '-size', f'{W}x{H}', 'xc:gray12', '(', '-size', f'{W}x{H}', 'xc:gray88', ')', 'bare.png', '-composite', 'metal_amount.png')
sh('magick', '(', '-size', f'{W}x{H}', 'xc:white', ')', 'rough.png', 'metal_amount.png', '-combine', '-depth', '8', 'hull_mr.png')

# Height: seams and rivets sunk and raised, chips a paint layer deep, scratches shallow.
sh('magick', 'seams.png', '-blur', '0x1.5', '-negate', 'seamh.png')
sh('magick', 'seamh.png', '+level', '40%,85%',
   '(', 'rivets.png', '-blur', '0x0.8', ')', '-compose', 'Mathematics', '-define', 'compose:args=0,0.12,1,0', '-composite',
   '(', 'tones.png', '-fill', 'white', '+opaque', 'gray50', '-fill', 'black', '-opaque', 'gray50', '-blur', '0x1', ')', '-compose', 'Mathematics', '-define', 'compose:args=0,0.05,1,0', '-composite',
   '(', 'chips.png', ')', '-compose', 'Mathematics', '-define', 'compose:args=0,-0.05,1,0', '-composite',
   '(', 'scratches.png', ')', '-compose', 'Mathematics', '-define', 'compose:args=0,-0.04,1,0', '-composite', '-depth', '16', 'height.gray')

# Normals from the height, in OpenGL's convention: green toward the picture's top.
height = array.array('H'); height.frombytes(open('height.gray', 'rb').read())
k = 5.0 / 65535
out = bytearray(W * H * 3)
for y in range(H):
    up = (y - 1 if y > 0 else y) * W
    row = y * W
    down = (y + 1 if y < H - 1 else y) * W
    for x in range(W):
        left = x - 1 if x > 0 else x
        right = x + 1 if x < W - 1 else x
        dx = (height[row + right] - height[row + left]) * k / 2
        dy = (height[down + x] - height[up + x]) * k / 2
        nx, ny = -dx, dy
        inv = 1 / math.sqrt(nx * nx + ny * ny + 1)
        at = (row + x) * 3
        out[at] = int(127.5 + 127.5 * nx * inv)
        out[at + 1] = int(127.5 + 127.5 * ny * inv)
        out[at + 2] = int(127.5 + 127.5 * inv)
open('normal.rgb', 'wb').write(out)
sh('magick', '-size', f'{W}x{H}', '-depth', '8', 'rgb:normal.rgb', 'hull_normal.png')
