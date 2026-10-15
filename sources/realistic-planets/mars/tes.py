"""Mars Global Surveyor's TES albedo map (P. R. Christensen and others, Journal of Geophysical Research
106, 2001), shared by Mars's scripts.

The map holds the bolometric Lambert albedo as 32-bit floats, 8 pixels a degree in a simple
cylindrical projection: planetocentric latitude from 90 north at the top, east longitude from -180
at the left edge, as the HRSC mosaics (`hrsc.py`). It has no data within about 2.5 degrees of
either pole, where it holds 0.06, and it stops at 0.32.
"""
import numpy as np
from scipy import ndimage

WIDTH, HEIGHT = 2880, 1440
# The value of the cells without data.
MISSING = 0.061


def read(data):
    """The map. Each row that misses data near a pole takes, there, the mean of the nearest row that
    has it all, so that the pole is filled evenly in every direction; any other cell without data
    takes the value of the nearest cell with data."""
    m = np.fromfile(f"{data}/global_albedo_8ppd.img", '<f4').reshape(HEIGHT, WIDTH).astype(np.float64)
    missing = m < MISSING
    whole = np.nonzero(~missing.any(axis=1))[0]
    for pole, nearest_row in ((slice(0, whole[0]), whole[0]), (slice(whole[-1] + 1, HEIGHT), whole[-1])):
        m[pole] = np.where(missing[pole], m[nearest_row].mean(), m[pole])
    missing = m < MISSING
    if missing.any():
        nearest = ndimage.distance_transform_edt(missing, return_distances=False, return_indices=True)
        m = m[tuple(nearest)]
    return m


def sampler(m):
    """A function of planetocentric latitude and east longitude, degrees, that gives the map's value
    there."""
    padded = np.concatenate([m[:, -2:], m, m[:, :2]], axis=1)

    def sample(lat, lon):
        row = (90 - lat) / 180 * HEIGHT - 0.5
        column = np.mod(lon + 180, 360) / 360 * WIDTH - 0.5 + 2
        return ndimage.map_coordinates(padded, [row, column], order=1, mode='nearest')
    return sample
