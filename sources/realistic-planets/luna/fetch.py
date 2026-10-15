"""Downloads what the Moon's texture and normal map are made from into a folder of its own: LROC's
photometrically normalised colour mosaic at 415, 566 and 643 nm, in its eight tiles from 70 north to
70 south, from the LROC team at Arizona State University, and LOLA's elevation map at 16 pixels a
degree and its normal albedo map at 1064 nm, 10 pixels a degree, from the PDS Geosciences Node.

    python3 fetch.py data
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import download  # noqa: E402

WAC = 'https://pds.lroc.im-ldi.com/data/LRO-L-LROC-5-RDR-V1.0/LROLRC_2001/DATA/MDR/WAC_HAPKE/WAC_HAPKE_{}_E350{}{}.IMG'
LOLA = 'https://pds-geosciences.wustl.edu/lro/lro-l-lola-3-rdr-v1/lrolol_1xxx/data/lola_gdr/cylindrical/{}'
BANDS = ('415NM', '566NM', '643NM')
TILES = [(side, centre) for side in ('N', 'S') for centre in ('0450', '1350', '2250', '3150')]

download.fetch([WAC.format(band, side, centre) for band in BANDS for side, centre in TILES], sys.argv[1])
download.fetch([LOLA.format(name) for name in ('img/ldem_16.img', 'img/ldem_16.lbl', 'float_img/ldam_10_float.img',
                                               'float_img/ldam_10_float.lbl')], sys.argv[1])
