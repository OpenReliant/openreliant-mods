"""Composes the Moon's texture from LROC's photometrically normalised colour mosaic, with LOLA's
albedo at the poles, as a 4096x2048 sRGB PNG: north at the top and east to the right, with 0 degrees
east in the middle column, as `sphere.py`'s spheres map it.

    python3 compose.py data out.png <brightness>

- The mosaic holds the ground's radiance factor at 415, 566 and 643 nm, each pixel normalised to the
  same angles with the slopes of the ground under it, so it holds the ground's albedo and colour
  without the shading of its relief, which the normal map adds (`normals.py`). Each texel is the
  mean of the mosaic's pixels in it (`maps.py`).
- The mosaic stops at 70 degrees north and south. Beyond, each band is LOLA's normal albedo at 1064
  nm, which reaches the poles, raised to the power and scaled by the factor that fit the mosaic to
  it on the logarithm between 60 and 69 degrees, in each hemisphere; between `BLEND` degrees and the
  mosaic's edge, the two are blended.
- Each texel's spectrum runs straight through the three bands, and on with the same slope beyond
  them, as the Moon's spectrum rises almost in a straight line across the visible, and is taken
  through the CIE 1931 observer (`truecolour.py`), as for the other bodies.
- `brightness` is the texture's mean luminance in linear light, for the game. The texture holds the
  body's own colour, as the mod lights the planets with white light (`records.planet_light` in
  `records.luau`). If its brightest texels pass 1, the whole map is scaled down until all but
  `CLIPPED` of them fit.
"""
import os
import subprocess
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import globe  # noqa: E402
import maps  # noqa: E402
import truecolour as tc  # noqa: E402

data, out, brightness = sys.argv[1], sys.argv[2], float(sys.argv[3])

WIDTH = 4096
# Where the mosaic and LOLA's albedo are blended, and the band of latitudes LOLA's albedo is fitted
# to the mosaic over, degrees from the equator.
BLEND = 67.0
FIT = (60.0, 69.0)
# The share of texels allowed past 1, and so clipped, if the map has to be scaled down to fit.
CLIPPED = 0.001

lats = maps.latitudes(WIDTH // 2)
everywhere = np.ones_like(lats, dtype=bool)
albedo = np.log(maps.albedo(data, WIDTH))
bands = {}
for band in maps.BANDS:
    m = maps.wac(data, band, WIDTH)
    filled = np.log(m)
    for sign in (1, -1):
        rows = (sign * lats >= FIT[0]) & (sign * lats <= FIT[1])
        use = np.isfinite(filled[rows]) & np.isfinite(albedo[rows])
        slope, intercept = np.polyfit(albedo[rows][use], filled[rows][use], 1)
        print(f"{band} nm, {'north' if sign > 0 else 'south'}: the mosaic is {np.exp(intercept):.4f} times LOLA's albedo "
              f"to the power {slope:.3f}, correlation {np.corrcoef(albedo[rows][use], filled[rows][use])[0, 1]:.2f}")
        polar = (sign * lats)[:, None] > BLEND
        t = np.clip((sign * lats[:, None] - BLEND) / (70.0 - BLEND), 0, 1)
        fitted = intercept + slope * albedo
        blended = np.where(np.isfinite(filled), (1 - t) * filled + t * fitted, fitted)
        filled = np.where(polar, blended, filled)
    # A texel the mosaic left empty within its latitudes takes its nearest neighbour's value.
    missing = ~np.isfinite(filled)
    if missing.any():
        filled = filled[tuple(ndimage.distance_transform_edt(missing, return_distances=False, return_indices=True))]
    bands[band] = np.exp(filled)
    print(f"{band} nm: mean radiance factor {globe.area_mean(bands[band], everywhere, lats):.4f}")

# Each band's share of linear sRGB: each wavelength takes the line through the two bands nearest it,
# the first two below the second band and the last two above it, so the line goes on beyond them.
lam = np.arange(380.0, 781.0)
M = tc.matrix(lam)
w = sorted(bands)
segment = np.clip(np.searchsorted(w, lam) - 1, 0, len(w) - 2)
weights = {}
for i, band in enumerate(w):
    lower, upper = np.array(w)[segment], np.array(w)[segment + 1]
    t = (lam - lower) / (upper - lower)
    share = np.where(segment == i, 1 - t, 0.0) + np.where(segment + 1 == i, t, 0.0)
    weights[band] = (share[:, None] * M).sum(axis=0)
texture = sum(bands[band][..., None] * weights[band] for band in w)
mean = np.array([globe.area_mean(texture[..., c], everywhere, lats) for c in range(3)])
print(f"mean colour at the mosaic's angles, linear sRGB {np.round(mean, 4)}, as 8-bit sRGB {np.round(tc.encode(mean) * 255).astype(int)}")

texture *= brightness / globe.area_mean(tc.luminance(texture), everywhere, lats)
print(f"at the texture's mean luminance of {brightness:.3f}, {np.round(tc.encode(mean * brightness / tc.luminance(mean)) * 255).astype(int)}")
fit = max(1.0, float(np.quantile(texture, 1 - CLIPPED)))
texture /= fit
print(f"scaled down by {fit:.3f} to fit")

h, width = texture.shape[:2]
pixels = (np.clip(texture, 0, 1) * 65535 + 0.5).astype('<u2')
subprocess.run(['magick', '-size', f'{width}x{h}', '-depth', '16', '-endian', 'LSB', 'rgb:-', '-set', 'colorspace', 'RGB',
                '-colorspace', 'sRGB', '-depth', '8', '-define', 'png:exclude-chunks=date,time', out],
               input=pixels.tobytes(), check=True)
print('wrote', out)
