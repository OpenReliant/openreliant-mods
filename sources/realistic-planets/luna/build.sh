#!/bin/sh
# Makes the Moon's texture from LROC's colour mosaic and LOLA's albedo, and its normal map from LOLA's
# heights, as the mod's README.md describes. Run it from this folder, with Python 3, numpy, scipy and
# ImageMagick 7. It downloads about 3.6 GB into data.
set -eu
mod=../../../mods/environment/realistic-planets
python3 fetch.py data
# For the game: a mean luminance of 0.047, the same share of the Moon's true brightness as Jupiter's
# 0.3 is of Jupiter's.
python3 compose.py data "$mod/realistic_planets_luna.png" 0.047
python3 normals.py data "$mod/realistic_planets_luna_normal.png" 4096
