"""Composes Mars's texture from Mars Express's HRSC mosaics, MGS's TES albedo map and what
`hubble.py` measures in Hubble's frames, as a 4096x2048 sRGB PNG: north at the top and east to the
right, with 0 degrees east in the middle column, as `sphere.py`'s spheres map it.

    python3 compose.py data out.png <brightness>

- The HRSC mosaics hold reflectance in the blue, green and red filters, at 440, 530 and 750 nm, 2 km
  a pixel (`hrsc.py`), and the texture is made on their grid. They keep Mars's detail, but their
  markings wider than a few hundred kilometres are weak: across the globe they vary a third as much
  as the TES map's, and Hubble's frames of 2003 follow the TES map's far better than theirs. So the
  ground keeps the mosaics' detail finer than `BROAD` degrees, and takes its broad markings from the
  TES map (`tes.py`), each wavelength's brightness following the TES albedo raised to the power
  Hubble measured at it (`CONTRAST`): Mars's markings are faint in violet and strong in red.
- The texture's spectrum is taken at Hubble's five wavelengths, 410 to 673 nm. At each, the mosaics'
  detail is interpolated between their filters on the logarithm, and the ground is divided by its
  mean over the globe, weighted by area.
- The polar caps are ice, which the ground's law would tint red: in the north where the TES map is
  brighter than `NORTH_ICE` north of 70 degrees, as the HRSC mosaics barely show the north cap, and
  in the south where the mosaics' blue is more than `SOUTH_ICE` of their red. The ice is `CAP` times
  as bright as the ground at each wavelength, as Hubble saw the south cap in 2003, with the mosaics'
  detail. The north cap takes the south cap's colour, as Hubble saw only the south.
- The colour is true colour (`truecolour.py`) of Mars's geometric albedo spectrum (`spectrum.py`),
  bent at each place through its brightness at the five wavelengths over the globe's mean, as
  Uranus's is through Hubble's maps.
- `brightness` is the texture's mean luminance in linear light, for the game. The texture holds the
  body's own colour, as the mod lights the planets with white light (`records.planet_light` in
  `records.luau`). If its brightest texels pass 1, the whole map is scaled down until all but
  `CLIPPED` of them fit. The map is scaled to the texture's size in linear light, by ImageMagick.
"""
import os
import subprocess
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import globe  # noqa: E402
import hrsc  # noqa: E402
import spectrum  # noqa: E402
import tes  # noqa: E402
import truecolour as tc  # noqa: E402

data, out, brightness = sys.argv[1], sys.argv[2], float(sys.argv[3])

# From `hubble.py`, at each of Hubble's wavelengths, nm: the power of the TES albedo that the
# ground's broad markings follow, and the south polar cap's brightness over the ground's.
CONTRAST = {410: 0.088, 502: 0.215, 588: 0.420, 631: 0.494, 673: 0.540}
CAP = {410: 2.82, 502: 2.13, 588: 1.67, 631: 1.63, 673: 1.55}
# The width of the broad markings the TES map gives, degrees: the blur's standard deviation.
BROAD = 1.5
# Where the ice begins and where it is whole: the TES albedo in the north, and the mosaics' blue over
# their red in the south.
NORTH_ICE = (0.26, 0.31)
SOUTH_ICE = (0.6, 1.0)
# The share of texels allowed past 1, and so clipped, if the map has to be scaled down to fit.
CLIPPED = 0.001
SIZE = (4096, 2048)


def smoothstep(x, edges):
    t = np.clip((x - edges[0]) / (edges[1] - edges[0]), 0, 1)
    return t * t * (3 - 2 * t)


maps = hrsc.Maps(data)
for w in maps.wavelengths:
    maps.maps[w] = np.log(maps.maps[w]).astype(np.float32)
height, width = maps.height, maps.width
lats = hrsc.latitudes(height)
everywhere = np.ones_like(lats, dtype=bool)
sigma = (BROAD * height / 180, BROAD * width / 360)


def broad(m):
    """`m` blurred over `BROAD` degrees, wrapping round in longitude."""
    return ndimage.gaussian_filter(m, sigma, mode=('nearest', 'wrap')).astype(np.float32)


# The TES albedo on the mosaics' grid, its logarithm's broad markings about their mean, and the ice.
rows = (np.arange(height) + 0.5) * tes.HEIGHT / height - 0.5
columns = (np.arange(width) + 0.5) * tes.WIDTH / width - 0.5
albedo = ndimage.map_coordinates(tes.read(data).astype(np.float32), np.meshgrid(rows, columns, indexing='ij'), order=1, mode='nearest')
markings = broad(np.log(albedo))
markings -= globe.area_mean(markings, everywhere, lats)
blue, _, red = maps.wavelengths
ice = np.where(lats[:, None] > 70, smoothstep(albedo, NORTH_ICE), 0) + \
    np.where(lats[:, None] < -70, smoothstep(np.exp(maps.maps[blue] - maps.maps[red]), SOUTH_ICE), 0)
ice = ice.astype(np.float32)
del albedo
print(f"ice covers {globe.area_mean(ice, everywhere, lats) * 100:.2f}% of the globe")

lam, curve = spectrum.mars()
M = tc.matrix(lam)
nodes = sorted(CONTRAST)
hats = dict(zip(nodes, tc.hats(lam, nodes)))
texture = np.zeros((height, width, 3), np.float32)
for node in nodes:
    # The mosaics' logarithm at this wavelength, its detail, the ground and the ice.
    w = np.clip(node, blue, red)
    upper = min(np.searchsorted(maps.wavelengths, w), 2)
    a, b = maps.wavelengths[upper - 1], maps.wavelengths[upper]
    t = (w - a) / (b - a)
    logged = (1 - t) * maps.maps[a] + t * maps.maps[b]
    detail = logged - broad(logged)
    del logged
    ground = np.exp(detail + CONTRAST[node] * markings)
    ground /= globe.area_mean(ground, everywhere, lats)
    ratio = (1 - ice) * ground + ice * CAP[node] * np.exp(detail)
    del ground, detail
    ratio /= globe.area_mean(ratio, everywhere, lats)
    K = ((curve * hats[node])[:, None] * M).sum(axis=0).astype(np.float32)
    texture += ratio[..., None] * K
    print(f"{node} nm: from the 10th to the 90th percentile, {np.percentile(ratio[::7, ::7], 10):.3f} to "
          f"{np.percentile(ratio[::7, ::7], 90):.3f} times the mean")
    del ratio
del maps, markings, ice

geometric = sum(((curve * h)[:, None] * M).sum(axis=0) for h in hats.values())
texture *= brightness / globe.area_mean(tc.luminance(texture), everywhere, lats)
print(f"geometric albedo, linear sRGB {np.round(geometric, 4)}, as 8-bit sRGB {np.round(tc.encode(geometric) * 255).astype(int)}; "
      f"at the texture's mean luminance of {brightness:.3f}, "
      f"{np.round(tc.encode(geometric * brightness / tc.luminance(geometric)) * 255).astype(int)}")
fit = max(1.0, float(np.quantile(texture[::7, ::7], 1 - CLIPPED)))
texture /= fit
print(f"scaled down by {fit:.3f} to fit")

w, h = SIZE
pixels = (np.clip(texture, 0, 1) * 65535 + 0.5).astype('<u2')
del texture
subprocess.run(['magick', '-size', f'{width}x{height}', '-depth', '16', '-endian', 'LSB', 'rgb:-', '-set', 'colorspace', 'RGB',
                '-resize', f'{w}x{h}!', '-colorspace', 'sRGB', '-depth', '8', '-define', 'png:exclude-chunks=date,time', out],
               input=pixels.tobytes(), check=True)
print('wrote', out)
