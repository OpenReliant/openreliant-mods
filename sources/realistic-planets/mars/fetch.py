"""Downloads what Mars's texture and limb are made from into a folder of its own: Mars Express's HRSC
global mosaics in its blue, green and red filters, from the HRSC team at the Freie Universität
Berlin, MGS's TES albedo map and its label, from Arizona State University's TES node, and Hubble's
calibrated WFPC2 frames of Mars of 26 and 27 August 2003, at 410, 502, 588, 631 and 673 nm, from
MAST.

    python3 fetch.py data
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import download  # noqa: E402

HRSC = 'https://hrscteam.dlr.de/public/data/global_mosaic/extra/{}-eqc.tif'
TES = 'http://tes.asu.edu/mineral_map/global_albedo_8ppd.{}'
MAST = 'https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:HST/product/{}_c0m.fits'
# Programme 10065's two visits: the first one's F410M, F631N, F502N, F588N and F673N frames, and the
# second one's F410M, F502N, F588N and F673N.
FRAMES = ['u8ta0104m', 'u8ta0105m', 'u8ta0106m', 'u8ta0107m', 'u8ta0108m',
          'u8ta0204m', 'u8ta0205m', 'u8ta0206m', 'u8ta0207m']

download.fetch([HRSC.format(f) for f in ('03-bl', '02-gr', '01-re')], sys.argv[1])
download.fetch([TES.format(e) for e in ('img', 'lbl')], sys.argv[1])
download.fetch([MAST.format(f) for f in FRAMES], sys.argv[1])
