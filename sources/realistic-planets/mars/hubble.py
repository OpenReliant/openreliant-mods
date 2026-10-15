"""Measures Mars from Hubble's WFPC2 frames of 26 and 27 August 2003, against the HRSC mosaics and the
TES albedo map: the limb's exponents for the mod's `planets.luau`, and for `compose.py` how strongly
the broad markings follow the TES map's and how bright the south polar cap is, at each frame's
wavelength.

    python3 hubble.py data

- Each frame's planetary camera, PC1, holds Mars about 550 pixels across, at 5 degrees of phase. The
  geometry of each frame is JPL Horizons's at the middle of its exposure (`FRAMES`): the sub-Earth
  and sub-solar points, and the position angle of Mars's north pole. The frame's own `ORIENTAT`
  turns the sky into the frame.
- The disk's middle is fitted to its edge (`globe.circle`), and its radius is Horizons's angular
  diameter over the camera's scale. Then the frame's offset and twist are fitted to the HRSC
  mosaics' markings, by the cross-correlation of the two with their broad trends taken off.
- Each pixel of the disk is mapped to Mars's latitude and longitude, and divided by the mosaics'
  reflectance there, at the frame's wavelength, interpolated between their filters on the
  logarithm. What is left is the law of the light: Minnaert's, `B * mu0^k * mu^(k - 1)`, fitted by
  least squares on the logarithm where the cosines of the light, `mu0`, and the view, `mu`, are at
  least `LEAST`, away from the polar caps. The mosaics hold Mars's markings of 2015 to 2017, and
  Hubble saw those of 2003, so their changes are noise the fit averages over.
- With the law taken out, the frame's brightness blurred over `BROAD` pixels is fitted, on the
  logarithm, to the TES albedo's, blurred the same way: the slope is how strongly Mars's broad
  markings show at that wavelength.
- The south polar cap's brightness over the ground's, the law taken out, is taken over the cap's
  core, where the mosaics' blue passes `ICE` of their red.
- Each filter's numbers are the means of the two visits', and the exponents for the red, green and
  blue channels are taken at the wavelengths of the channels for Mars's spectrum (`spectrum.py`),
  straight between the filters' and flat beyond them.
"""
import os
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fits  # noqa: E402
import globe  # noqa: E402
import hrsc  # noqa: E402
import spectrum  # noqa: E402
import tes  # noqa: E402
import truecolour as tc  # noqa: E402

# Mars's radii, km (IAU), for planetocentric latitudes.
EQUATOR, POLE = 3396.2, 3376.2
# The planetary camera's scale, arcseconds a pixel.
SCALE = 0.04554
# Each frame's filter wavelength, nm, and its geometry from JPL Horizons, seen from the Earth's
# centre at the middle of its exposure: Mars's angular diameter, arcseconds; the sub-Earth and
# sub-solar points, planetodetic latitude and west longitude, degrees; and the position angle of the
# north pole, degrees east of north. Mars turns 0.7 degrees between one frame and the next.
FRAMES = {
    'u8ta0104m': (410, {'diameter': 25.12597, 'earth': (-19.021315, 319.385517), 'sun': (-23.623784, 321.889236), 'pole': 346.1021}),
    'u8ta0105m': (631, {'diameter': 25.12598, 'earth': (-19.021273, 320.115252), 'sun': (-23.624007, 322.616973), 'pole': 346.1024}),
    'u8ta0106m': (502, {'diameter': 25.12599, 'earth': (-19.021231, 320.850606), 'sun': (-23.624232, 323.350313), 'pole': 346.1027}),
    'u8ta0107m': (588, {'diameter': 25.12600, 'earth': (-19.021189, 321.578234), 'sun': (-23.624455, 324.075949), 'pole': 346.1031}),
    'u8ta0108m': (673, {'diameter': 25.12601, 'earth': (-19.021147, 322.309725), 'sun': (-23.624679, 324.805437), 'pole': 346.1034}),
    'u8ta0204m': (410, {'diameter': 25.12699, 'earth': (-19.012171, 123.509671), 'sun': (-23.673688, 125.563694), 'pole': 346.1774}),
    'u8ta0205m': (502, {'diameter': 25.12699, 'earth': (-19.012131, 124.243270), 'sun': (-23.673910, 126.295282), 'pole': 346.1778}),
    'u8ta0206m': (588, {'diameter': 25.12699, 'earth': (-19.012092, 124.970548), 'sun': (-23.674129, 127.020566), 'pole': 346.1781}),
    'u8ta0207m': (673, {'diameter': 25.12699, 'earth': (-19.012052, 125.702392), 'sun': (-23.674350, 127.750403), 'pole': 346.1784}),
}
# The least cosines of the light and the view where a pixel counts, and the latitudes beyond which
# the polar caps and their frost are left out, degrees.
LEAST = 0.2
CAPS = (-60.0, 60.0)
# The twists, degrees, and the shifts, up to `SEARCH` pixels, that the pointing is searched over, and
# the width of the broad trends taken off before the markings are matched, pixels.
TWISTS = (-1.0, -0.5, 0.0, 0.5, 1.0)
SEARCH = 15
BLUR = 12.0
# The blur, pixels, over which the frame's broad markings are compared with the TES map's, and the
# ratio of the HRSC mosaics' blue to their red above which a texel is ice.
BROAD = 3.0
ICE = 1.15


def centric(detic):
    """Planetocentric latitude from planetodetic, degrees."""
    return np.degrees(np.arctan((POLE / EQUATOR) ** 2 * np.tan(np.radians(detic))))


def frame(path):
    """The frame's planetary camera, less its sky, and its position angle, degrees east of north."""
    primary, header, image = fits.extension(path, 1)
    sky = np.median(np.concatenate([image[:60, :60].ravel(), image[-60:, -60:].ravel(), image[:60, -60:].ravel(), image[-60:, :60].ravel()]))
    return image - sky, float(header['ORIENTAT'])


def edge(image):
    """The disk's middle, (x, y) pixels, fitted to where each ray from its rough middle falls to half
    the brightness it has inside the edge."""
    bright = image > 0.3 * np.percentile(image, 99)
    ys, xs = np.nonzero(bright)
    cx, cy = xs.mean(), ys.mean()
    rough = np.sqrt(bright.sum() / np.pi)
    points = []
    for angle in np.radians(np.arange(0, 360, 2)):
        r = np.arange(0.8 * rough, 1.2 * rough, 0.25)
        profile = ndimage.map_coordinates(image, [cy + r * np.sin(angle), cx + r * np.cos(angle)], order=1)
        inside = np.median(profile[(r > 0.85 * rough) & (r < 0.92 * rough)])
        below = np.nonzero(profile < 0.5 * inside)[0]
        below = below[r[below] > 0.9 * rough]
        if len(below):
            points.append((cx + r[below[0]] * np.cos(angle), cy + r[below[0]] * np.sin(angle)))
    x, y, radius = globe.circle(np.array(points))
    return x, y, radius


def basis(g, orientat):
    """The frame's axes and the body's, as vectors in the sky's frame (right, up, toward the Earth),
    seen with north up: x, y of the frame; toward the Earth; and Mars's x (0 degrees east), y (90
    east) and z (the north pole), and toward the sun, from the frame's geometry `g`."""
    north, east, out = np.array([0.0, 1, 0]), np.array([-1.0, 0, 0]), np.array([0.0, 0, 1])
    o = np.radians(orientat)
    y_axis = np.cos(o) * north + np.sin(o) * east
    x_axis = np.sin(o) * north - np.cos(o) * east
    lat, west = g['earth']
    lat, lon = np.radians(centric(lat)), np.radians(-west)
    p = np.radians(g['pole'])
    z = np.cos(lat) * (np.cos(p) * north + np.sin(p) * east) + np.sin(lat) * out
    q = (out - np.sin(lat) * z) / np.cos(lat)
    r = np.cross(z, q)
    x = np.cos(lon) * q - np.sin(lon) * r
    y = np.sin(lon) * q + np.cos(lon) * r
    slat, swest = g['sun']
    sun = globe.unit(centric(slat), -swest)
    sun = sun[0] * x + sun[1] * y + sun[2] * z
    return x_axis, y_axis, out, (x, y, z), sun


def geometry(shape, middle, radius, axes, twist=0.0):
    """Each pixel's cosines of the view and the light, latitude and east longitude, degrees; NaN off
    the disk."""
    x_axis, y_axis, out, (bx, by, bz), sun = axes
    t = np.radians(twist)
    x_axis, y_axis = np.cos(t) * x_axis + np.sin(t) * y_axis, -np.sin(t) * x_axis + np.cos(t) * y_axis
    rows, columns = np.indices(shape, dtype=float)
    u, v = (columns - middle[0]) / radius, (rows - middle[1]) / radius
    w = np.sqrt(np.clip(1 - u * u - v * v, 0, None))
    on = u * u + v * v < 1
    n = u[..., None] * x_axis + v[..., None] * y_axis + w[..., None] * out
    mu = np.where(on, n @ out, np.nan)
    mu0 = np.where(on, n @ sun, np.nan)
    lat = np.where(on, np.degrees(np.arcsin(np.clip(n @ bz, -1, 1))), np.nan)
    lon = np.where(on, np.degrees(np.arctan2(n @ by, n @ bx)), np.nan)
    return mu, mu0, lat, lon


def markings(logged, weight):
    """What is left of a logarithm of brightness once its broad trends, wider than `BLUR` pixels,
    are taken off, weighted by `weight`."""
    smooth = ndimage.gaussian_filter(logged * weight, BLUR) / np.maximum(ndimage.gaussian_filter(weight, BLUR), 1e-6)
    return (logged - smooth) * weight


def pointing(image, reference_at, middle, radius, axes):
    """The middle and twist at which the frame's markings best match the map's: for each twist in
    `TWISTS`, the shift at the peak of their cross-correlation, refined to a fraction of a pixel by a
    parabola through the peak, and its correlation."""
    best = None
    for twist in TWISTS:
        mu, mu0, lat, lon = geometry(image.shape, middle, radius, axes, twist)
        inner = (mu >= 0.4) & (lat > CAPS[0]) & (lat < CAPS[1]) & (image > 0)
        weight = np.where(inner, np.clip((mu - 0.4) / 0.2, 0, 1), 0.0)
        predicted = np.zeros(image.shape)
        predicted[inner] = np.log(reference_at(lat[inner], lon[inner]))
        seen = markings(np.where(inner, np.log(np.where(image > 0, image, 1)), 0.0), weight)
        expected = markings(predicted, weight)
        cross = np.fft.irfft2(np.fft.rfft2(seen) * np.conj(np.fft.rfft2(expected)), s=image.shape)
        cross = np.fft.fftshift(cross)
        c = np.array(image.shape) // 2
        window = cross[c[0] - SEARCH:c[0] + SEARCH + 1, c[1] - SEARCH:c[1] + SEARCH + 1]
        r, k = np.unravel_index(np.argmax(window), window.shape)
        r, k = min(max(r, 1), 2 * SEARCH - 1), min(max(k, 1), 2 * SEARCH - 1)

        def vertex(left, centre, right):
            return 0.5 * (left - right) / (left - 2 * centre + right)
        dy = r - SEARCH + vertex(window[r - 1, k], window[r, k], window[r + 1, k])
        dx = k - SEARCH + vertex(window[r, k - 1], window[r, k], window[r, k + 1])
        score = window[r, k] / np.sqrt((seen ** 2).sum() * (expected ** 2).sum())
        if best is None or score > best[3]:
            best = (middle[0] + dx, middle[1] + dy, twist, score)
    return best


def fit(image, reference, mu, mu0, lat):
    """Minnaert's exponent k and the residual's spread, on the logarithm."""
    use = (mu >= LEAST) & (mu0 >= LEAST) & (lat > CAPS[0]) & (lat < CAPS[1]) & (image > 0) & (reference > 0)
    y = np.log(image[use] / reference[use]) + np.log(mu[use])
    x = np.log(mu0[use] * mu[use])
    slope, intercept = np.polyfit(x, y, 1)
    return slope, np.std(y - (slope * x + intercept)), use.sum()


def corrected(image, k, mu, mu0):
    """The logarithm of the frame's brightness with Minnaert's law of exponent `k` taken out."""
    return np.log(np.where(image > 0, image, 1)) - k * np.log(np.where(mu0 > 0, mu0, 1)) - (k - 1) * np.log(np.where(mu > 0, mu, 1))


def contrast(logged, tes_at, mu, mu0, lat, lon):
    """How strongly the frame's broad markings follow the TES map's: the slope of the logarithm of
    its brightness, the law of the light taken out, against that of the TES albedo, both blurred over
    `BROAD` pixels, where the cosines of the light and the view are at least 0.4, away from the polar
    caps; and their correlation."""
    use = (mu >= 0.4) & (mu0 >= 0.4) & (lat > CAPS[0]) & (lat < CAPS[1])
    weight = use.astype(float)
    albedo = np.zeros(logged.shape)
    albedo[use] = np.log(tes_at(lat[use], lon[use]))

    def blurred(m):
        return ndimage.gaussian_filter(np.where(use, m, 0) * weight, BROAD) / np.maximum(ndimage.gaussian_filter(weight, BROAD), 1e-6)
    seen, expected = blurred(logged)[use], blurred(albedo)[use]
    return np.polyfit(expected, seen, 1)[0], np.corrcoef(expected, seen)[0, 1]


def ice(logged, blue_over_red, mu, mu0, lat, lon):
    """The south polar cap's brightness over the ground's, the law of the light taken out: the cap's
    texels are those south of 80 degrees that the HRSC mosaics show as ice, where the cosines are at
    least `LEAST`, and the ground's those where they are at least 0.4, away from the caps."""
    cap = (lat < -80) & (mu >= LEAST) & (mu0 >= LEAST)
    cap[cap] = blue_over_red(lat[cap], lon[cap]) > ICE
    ground = (mu >= 0.4) & (mu0 >= 0.4) & (lat > CAPS[0]) & (lat < CAPS[1])
    return np.exp(np.mean(logged[cap]) - np.mean(logged[ground])), cap.sum()


def main():
    data = sys.argv[1]
    maps = hrsc.Maps(data, step=0.25)
    tes_at = tes.sampler(tes.read(data))
    blue, _, red = maps.wavelengths
    blue_at, red_at = maps.at(blue), maps.at(red)

    def blue_over_red(lat, lon):
        return blue_at(lat, lon) / red_at(lat, lon)
    results = {}
    for name, (wavelength, g) in FRAMES.items():
        image, orientat = frame(f"{data}/{name}_c0m.fits")
        x, y, edge_radius = edge(image)
        radius = g['diameter'] / 2 / SCALE
        axes = basis(g, orientat)
        reference_at = maps.at(wavelength)

        # The pointing that best matches the map, found twice so that the second search starts
        # where the first one ended.
        mx, my, twist, correlation = pointing(image, reference_at, (x, y), radius, axes)
        mx, my, twist, correlation = pointing(image, reference_at, (mx, my), radius, axes)
        dx, dy = mx - x, my - y
        mu, mu0, lat, lon = geometry(image.shape, (mx, my), radius, axes, twist)
        reference = np.full(image.shape, np.nan)
        on = np.isfinite(lat)
        reference[on] = reference_at(lat[on], lon[on])
        k, spread, count = fit(image, reference, mu, mu0, lat)
        logged = corrected(image, k, mu, mu0)
        slope, follows = contrast(logged, tes_at, mu, mu0, lat, lon)
        brighter, cap = ice(logged, blue_over_red, mu, mu0, lat, lon)
        results.setdefault(wavelength, []).append((k, slope, brighter))
        print(f"{name} {wavelength} nm: edge radius {edge_radius:.1f} px against {radius:.1f}, offset ({dx:+.2f}, {dy:+.2f}) px, "
              f"twist {twist:+.1f} degrees, correlation {correlation:.3f}; k {k:.3f}, spread {spread:.3f} over {count} pixels; "
              f"contrast against TES {slope:.3f}, correlation {follows:.2f}; cap {brighter:.2f} times the ground over {cap} pixels")
    wavelengths = sorted(results)
    ks = [np.mean([r[0] for r in results[w]]) for w in wavelengths]
    for w, k in zip(wavelengths, ks):
        slopes, caps = [r[1] for r in results[w]], [r[2] for r in results[w]]
        print(f"{w} nm: k {k:.3f}, contrast against TES {np.mean(slopes):.3f}, cap {np.mean(caps):.2f} times the ground")
    lam, albedo = spectrum.mars()
    channels = tc.channels(lam, albedo, tc.matrix(lam))
    print("channels at", ", ".join(f"{c:.0f}" for c in channels), "nm: k", ", ".join(f"{np.interp(c, wavelengths, ks):.3f}" for c in channels))


if __name__ == '__main__':
    main()
