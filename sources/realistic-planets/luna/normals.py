"""Makes the Moon's normal map from LOLA's heights, as a 16-bit PNG of `width` by half as many: north
at the top and east to the right, with 0 degrees east in the middle column, as the texture is.

    python3 normals.py data out.png <width>

- The heights are averaged over each texel (`maps.py`), and each texel's slope toward the east and
  toward the north is the difference of its neighbours' heights over the distance between them on
  a sphere of 1,737.4 km, at the relief's true height. Toward the poles a texel spans less and less
  of a degree's distance east to west, so the neighbours east and west are taken as many texels
  away as keep them about as far apart as the neighbours north and south.
- The normal leans against each slope, and is kept as OpenGL's normal maps keep it, the texture's
  right as x and its top as y, as OpenReliant reads it (`*_normal.png`), at 16 bits, so that the
  maria's gentle slopes light smoothly.
"""
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maps  # noqa: E402

data, out, width = sys.argv[1], sys.argv[2], int(sys.argv[3])

# The Moon's radius, m, the sphere LOLA's heights stand on.
RADIUS = 1737400.0

h = maps.heights(data, width)
height = width // 2
lats = np.radians(maps.latitudes(height))
step = 2 * np.pi / width

# Toward the north: the neighbours above and below, the first and last rows' own height standing in
# beyond the pole.
padded = np.concatenate([h[:1], h, h[-1:]], axis=0)
north = (padded[:-2] - padded[2:]) / (2 * step * RADIUS)
# Toward the east, over neighbours as many texels away as keep them about one texel's distance north
# to south apart.
east = np.empty_like(h)
for row in range(height):
    span = max(1, int(round(1 / max(np.cos(lats[row]), 1e-3))))
    span = min(span, width // 4)
    distance = 2 * span * step * RADIUS * np.cos(lats[row])
    east[row] = (np.roll(h[row], -span) - np.roll(h[row], span)) / distance

normal = np.stack([-east, -north, np.ones_like(h)], axis=-1)
normal /= np.linalg.norm(normal, axis=-1, keepdims=True)
print(f"the slopes' median {np.degrees(np.median(np.arccos(normal[..., 2]))):.2f} degrees, 99th percentile "
      f"{np.degrees(np.percentile(np.arccos(normal[..., 2]), 99)):.2f}")
pixels = np.round((normal * 0.5 + 0.5) * 65535).astype('<u2')
subprocess.run(['magick', '-size', f'{width}x{height}', '-depth', '16', '-endian', 'LSB', 'rgb:-', '-set', 'colorspace', 'RGB',
                '-define', 'png:exclude-chunks=date,time', out], input=pixels.tobytes(), check=True)
print('wrote', out)
