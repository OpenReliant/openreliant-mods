#!/bin/sh
# Makes Mars's texture from Mars Express's HRSC mosaics, MGS's TES albedo map and Hubble's frames, and
# prints its limb's exponents, as the mod's README.md describes. Run it from this folder, with Python
# 3, numpy, scipy and ImageMagick 7. It downloads about 790 MB into data.
set -eu
python3 fetch.py data
# The limb's exponents for planets.luau, and how strongly the markings follow the TES map's and how
# bright the south cap is at each of Hubble's wavelengths, for compose.py's CONTRAST and CAP.
python3 hubble.py data
# For the game: a mean luminance of 0.072, the same share of Mars's true brightness as Jupiter's 0.3
# is of Jupiter's.
python3 compose.py data ../../../mods/environment/realistic-planets/realistic_planets_mars.png 0.072
