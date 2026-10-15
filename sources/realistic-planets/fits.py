"""Reads FITS files: a header of 80-character cards in blocks of 2880 bytes, ending at the card END,
then its data, padded to a whole block, and after it any extensions, each a header and data of its
own. `image` reads the one image of a file, as Hubble's OPAL maps hold it, and `extension` the image
of an extension, as Hubble's WFPC2 frames hold the picture of each of their four cameras."""
import numpy as np

BLOCK = 2880
CARD = 80
TYPES = {8: '>u1', 16: '>i2', 32: '>i4', -32: '>f4', -64: '>f8'}


def _header(f, path):
    """The header at the file's position, its values as strings, quotes and comments taken off;
    None at the end of the file."""
    header = {}
    while True:
        block = f.read(BLOCK)
        if not block:
            return None
        if len(block) < BLOCK:
            raise ValueError(f"{path}: the header ends without END")
        for at in range(0, BLOCK, CARD):
            card = block[at:at + CARD].decode('ascii')
            key = card[:8].strip()
            if key == 'END':
                return header
            if card[8:10] == '= ':
                header[key] = card[10:].split('/')[0].strip().strip("'").strip()


def _shape(header):
    return [int(header[f'NAXIS{n}']) for n in range(int(header['NAXIS']), 0, -1)]


def _skip(f, header):
    """Moves past the data that follows `header`, and its padding."""
    size = abs(int(header['BITPIX'])) // 8 * int(np.prod(_shape(header))) if int(header['NAXIS']) else 0
    size += abs(int(header['BITPIX'])) // 8 * int(header.get('PCOUNT', 0))
    f.seek((size + BLOCK - 1) // BLOCK * BLOCK, 1)


def _read(f, header):
    shape = _shape(header)
    data = np.fromfile(f, dtype=TYPES[int(header['BITPIX'])], count=int(np.prod(shape)))
    return data.reshape(shape).astype(np.float64) * float(header.get('BSCALE', 1)) + float(header.get('BZERO', 0))


def image(path):
    """The image at `path`, a 2-dimensional array of 32-bit floats, as an array of rows."""
    with open(path, 'rb') as f:
        header = _header(f, path)
        if header is None or int(header['BITPIX']) != -32 or int(header['NAXIS']) != 2:
            raise ValueError(f"{path}: not a 2-dimensional image of 32-bit floats")
        return _read(f, header)


def extension(path, number):
    """The primary header, and the header and the image of extension `number`, counted from 1."""
    with open(path, 'rb') as f:
        primary = _header(f, path)
        _skip(f, primary)
        for _ in range(number - 1):
            header = _header(f, path)
            if header is None:
                raise ValueError(f"{path}: fewer than {number} extensions")
            _skip(f, header)
        header = _header(f, path)
        if header is None:
            raise ValueError(f"{path}: fewer than {number} extensions")
        return primary, header, _read(f, header)
