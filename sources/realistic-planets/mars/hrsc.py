"""Mars Express's HRSC global mosaics, shared by Mars's scripts.

The mosaics hold reflectance as 32-bit floats, 2 km a pixel in a simple cylindrical projection of a
sphere of 3,396 km: planetocentric latitude from 90 north at the top, east longitude from -180 at
the left edge, so 0 degrees east is the middle column, as `sphere.py`'s spheres map it. Each filter's
mosaic is scaled to one well-calibrated observation, so the filters' ratios hold Mars's colour (G. G.
Michael and others, Icarus 425, 2025). The filters' wavelengths are R. Jaumann and others's
(Planetary and Space Science 55, 2007).
"""
import subprocess

import numpy as np
from scipy import ndimage

# Each filter's file and wavelength, nm.
FILTERS = {'03-bl': 440.0, '02-gr': 530.0, '01-re': 750.0}
WIDTH, HEIGHT = 10669, 5334


def read(path):
    """A mosaic as an array of rows, through ImageMagick. The few pixels without data, -1e32, take
    the value of the nearest pixel with data."""
    raw = subprocess.run(['magick', path, '-define', 'quantum:format=floating-point', '-depth', '32', '-endian', 'LSB', 'gray:-'],
                         capture_output=True, check=True).stdout
    m = np.frombuffer(raw, '<f4').reshape(HEIGHT, WIDTH).astype(np.float64)
    missing = ~(m > 0)
    if missing.any():
        nearest = ndimage.distance_transform_edt(missing, return_distances=False, return_indices=True)
        m = m[tuple(nearest)]
    return m


def latitudes(height):
    """The planetocentric latitude of the middle of each of a map's rows, degrees."""
    return 90 - (np.arange(height) + 0.5) * 180 / height


class Maps:
    """The mosaics of the blue, green and red filters, averaged to `step` degrees a pixel, or at
    full size without one."""

    def __init__(self, data, step=None):
        self.wavelengths = sorted(FILTERS.values())
        self.maps = {}
        for name, wavelength in FILTERS.items():
            m = read(f"{data}/{name}-eqc.tif")
            if step is not None:
                # A box the size of the new pixel, wrapped round in longitude, then sampled at the
                # middle of each new pixel.
                box = int(round(step / (180 / HEIGHT)))
                m = ndimage.uniform_filter(m, size=box, mode=('nearest', 'wrap'))
                height, width = int(round(180 / step)), int(round(360 / step))
                rows = (np.arange(height) + 0.5) * HEIGHT / height - 0.5
                columns = (np.arange(width) + 0.5) * WIDTH / width - 0.5
                m = ndimage.map_coordinates(m, np.meshgrid(rows, columns, indexing='ij'), order=1, mode='nearest')
            self.maps[wavelength] = m
        self.height, self.width = next(iter(self.maps.values())).shape

    def at(self, wavelength):
        """A function of planetocentric latitude and east longitude, degrees, that gives the
        reflectance at `wavelength`: straight between the filters' on the logarithm, and the
        nearest filter's beyond them."""
        w = np.clip(wavelength, self.wavelengths[0], self.wavelengths[-1])
        upper = min(np.searchsorted(self.wavelengths, w), len(self.wavelengths) - 1)
        lower = max(upper - 1, 0)
        a, b = self.wavelengths[lower], self.wavelengths[upper]
        t = 0.0 if a == b else (w - a) / (b - a)
        logged = (1 - t) * np.log(self.maps[a]) + t * np.log(self.maps[b])
        padded = np.concatenate([logged[:, -2:], logged, logged[:, :2]], axis=1)

        def sample(lat, lon):
            row = (90 - lat) / 180 * self.height - 0.5
            column = (np.mod(lon + 180, 360)) / 360 * self.width - 0.5 + 2
            return np.exp(ndimage.map_coordinates(padded, [row, column], order=1, mode='nearest'))
        return sample
