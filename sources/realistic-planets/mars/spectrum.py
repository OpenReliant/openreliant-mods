"""Mars's geometric albedo over the visible range, from A. Mallama, B. Krobusek and H. Pavlov's
wide-band albedos (Icarus 282, 2017, table 7), in the Johnson-Cousins and Sloan filters, each at its
effective wavelength (tables 1 and 2), joined by a monotone cubic curve."""
import numpy as np
from scipy import interpolate

# Each filter's effective wavelength, nm, and Mars's geometric albedo in it.
ALBEDOS = {
    'U': (360, 0.060), 'B': (436, 0.088), 'V': (549, 0.170), 'R': (700, 0.288), 'I': (900, 0.330),
    'Rc': (641, 0.250), 'Ic': (798, 0.285),
    "u'": (355, 0.061), "g'": (469, 0.111), "r'": (616, 0.245), "i'": (748, 0.298), "z'": (893, 0.325),
}


def mars(step=1.0):
    """The wavelengths from 380 to 780 nm, `step` apart, and Mars's geometric albedo at each."""
    points = sorted(ALBEDOS.values())
    curve = interpolate.PchipInterpolator([w for w, _ in points], [a for _, a in points])
    lam = np.arange(380.0, 780.0 + step / 2, step)
    return lam, curve(lam)
