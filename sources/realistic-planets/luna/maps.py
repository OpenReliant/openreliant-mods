"""The Moon's maps, shared by its scripts, each read onto a texture's grid: `width` by half as many
rows, planetocentric latitude from 90 north at the top, and east longitude from -180 at the left
edge, so 0 degrees east is the middle column, as `sphere.py`'s spheres map it.

- LROC's photometrically normalised mosaic (H. Sato and others, Icarus 296, 2017) holds the radiance
  factor I/F at incidence and phase angles of 60 degrees and an emission angle of 0, from 70 north
  to 70 south, 76 pixels a degree, as 32-bit floats in eight tiles of 70 degrees of latitude by 90 of
  longitude, each with its label before it. Each texel takes the mean of the tiles' pixels whose
  middles fall in it, leaving out those below `SHADOW` of their tile's median, which lay in shadow
  in the pictures, mostly near 70 degrees.
- LOLA's elevation map holds the height above a sphere of 1,737.4 km as 16-bit integers of half a
  metre, and its albedo map the normal albedo at 1064 nm as 32-bit floats, both from 90 north to 90
  south and from 0 to 360 degrees east.
"""
import numpy as np
from scipy import ndimage

BANDS = (415, 566, 643)
# The share of a tile's median below which a pixel of the mosaic is taken as shadow.
SHADOW = 0.25
TILES = [(side, centre) for side in ('N', 'S') for centre in ('0450', '1350', '2250', '3150')]


def _label(path):
    """The values of the PDS label at the start of `path`, as strings."""
    values = {}
    with open(path, 'rb') as f:
        text = f.read(65536).decode('latin-1')
    for line in text.splitlines():
        if line.strip() == 'END':
            break
        if '=' in line:
            key, value = line.split('=', 1)
            values.setdefault(key.strip(), value.split('/*')[0].split('<')[0].strip().strip('"'))
    return values


def wac(data, band, width):
    """The mosaic at `band` nm on the texture's grid, NaN where it has no data."""
    height = width // 2
    total = np.zeros(height * width)
    count = np.zeros(height * width)
    for side, centre in TILES:
        path = f"{data}/WAC_HAPKE_{band}NM_E350{side}{centre}.IMG"
        label = _label(path)
        lines, samples = int(label['LINES']), int(label['LINE_SAMPLES'])
        start = int(label['RECORD_BYTES']) * (int(label['^IMAGE']) - 1)
        resolution = float(label['MAP_RESOLUTION'])
        image = np.memmap(path, dtype='<f4', mode='r', offset=start, shape=(lines, samples))
        # The middle of each line and sample, as PDS's simple cylindrical projection places them.
        lats = float(label['CENTER_LATITUDE']) + (float(label['LINE_PROJECTION_OFFSET']) - np.arange(lines)) / resolution
        lons = float(label['CENTER_LONGITUDE']) + (np.arange(samples) - float(label['SAMPLE_PROJECTION_OFFSET'])) / resolution
        sample = np.asarray(image[::16, ::16])
        least = SHADOW * np.median(sample[np.isfinite(sample) & (sample > 0) & (sample < 10)])
        rows = np.clip(((90 - lats) / 180 * height).astype(int), 0, height - 1)
        columns = (np.mod(lons + 180, 360) / 360 * width).astype(int) % width
        for at in range(0, lines, 512):
            block = np.asarray(image[at:at + 512], dtype=np.float64)
            valid = np.isfinite(block) & (block > least) & (block < 10)
            index = (rows[at:at + 512, None] * width + columns[None, :]).ravel()
            total += np.bincount(index, weights=np.where(valid, block, 0).ravel(), minlength=height * width)
            count += np.bincount(index, weights=valid.ravel(), minlength=height * width)
    with np.errstate(invalid='ignore'):
        return (total / count).reshape(height, width)


def _lola(raw, scale, width):
    """A LOLA map, rows from 90 north and columns east from 0, on the texture's grid: averaged over
    the texture's texels, or interpolated where they are finer."""
    m = np.roll(raw, raw.shape[1] // 2, axis=1)
    height = width // 2
    factor = m.shape[1] / width
    if factor > 1:
        m = ndimage.uniform_filter(m, size=int(round(factor)), mode=('nearest', 'wrap'))
    rows = (np.arange(height) + 0.5) * m.shape[0] / height - 0.5
    columns = (np.arange(width) + 0.5) * m.shape[1] / width - 0.5
    return ndimage.map_coordinates(m, np.meshgrid(rows, columns, indexing='ij'), order=1, mode='nearest') * scale


def heights(data, width):
    """LOLA's heights, m, on the texture's grid."""
    raw = np.fromfile(f"{data}/ldem_16.img", '<i2').reshape(2880, 5760).astype(np.float64)
    return _lola(raw, 0.5, width)


def albedo(data, width):
    """LOLA's normal albedo at 1064 nm on the texture's grid, NaN where it has none."""
    raw = np.fromfile(f"{data}/ldam_10_float.img", '<f4').reshape(1800, 3600).astype(np.float64)
    raw[~(raw > 0)] = np.nan
    return _lola(raw, 1.0, width)


def latitudes(height):
    """The planetocentric latitude of the middle of each of a map's rows, degrees."""
    return 90 - (np.arange(height) + 0.5) * 180 / height
