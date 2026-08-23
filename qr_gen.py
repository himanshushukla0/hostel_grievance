"""
qr_gen.py — a tiny, dependency-free QR Code generator.

Pure standard-library Python. Encodes text in byte mode with Reed-Solomon
error correction and renders a scannable QR as an inline SVG string (or a
data: URI), so it works 100% offline with no external packages or network.

Supports QR versions 1–10 at EC levels L and M — far more than enough for a
short gate-pass code. Public API:

    matrix = qr_matrix("GP-2026-ABC123")          # list[list[bool]]
    svg    = qr_svg("GP-2026-ABC123", scale=6)    # <svg ...>...</svg>
    uri    = qr_data_uri("GP-2026-ABC123")        # data:image/svg+xml;...

If the payload is too large for version 10 at level L, ValueError is raised.
"""

# ----------------------------------------------------------------------------
# Galois field GF(256) for Reed-Solomon (primitive polynomial 0x11d)
# ----------------------------------------------------------------------------
_EXP = [0] * 512
_LOG = [0] * 256
_x = 1
for _i in range(255):
    _EXP[_i] = _x
    _LOG[_x] = _i
    _x <<= 1
    if _x & 0x100:
        _x ^= 0x11d
for _i in range(255, 512):
    _EXP[_i] = _EXP[_i - 255]


def _gf_mul(a, b):
    if a == 0 or b == 0:
        return 0
    return _EXP[_LOG[a] + _LOG[b]]


def _rs_generator(nsym):
    g = [1]
    for i in range(nsym):
        g2 = [0] * (len(g) + 1)
        for j in range(len(g)):
            g2[j] ^= _gf_mul(g[j], 1)
            g2[j + 1] ^= _gf_mul(g[j], _EXP[i])
        g = g2
    return g


def _rs_encode(data, nsym):
    gen = _rs_generator(nsym)
    res = list(data) + [0] * nsym
    for i in range(len(data)):
        coef = res[i]
        if coef != 0:
            for j in range(len(gen)):
                res[i + j] ^= _gf_mul(gen[j], coef)
    return res[len(data):]


# ----------------------------------------------------------------------------
# Version / EC tables (versions 1–10, levels L and M)
# Each entry: (ec_codewords_per_block, [(num_blocks, data_cw_per_block), ...])
# ----------------------------------------------------------------------------
_BLOCK_TABLE = {
    ('L', 1): (7,  [(1, 19)]),
    ('M', 1): (10, [(1, 16)]),
    ('L', 2): (10, [(1, 34)]),
    ('M', 2): (16, [(1, 28)]),
    ('L', 3): (15, [(1, 55)]),
    ('M', 3): (26, [(1, 44)]),
    ('L', 4): (20, [(1, 80)]),
    ('M', 4): (18, [(2, 32)]),
    ('L', 5): (26, [(1, 108)]),
    ('M', 5): (24, [(2, 43)]),
    ('L', 6): (18, [(2, 68)]),
    ('M', 6): (16, [(4, 27)]),
    ('L', 7): (20, [(2, 78)]),
    ('M', 7): (18, [(4, 31)]),
    ('L', 8): (24, [(2, 97)]),
    ('M', 8): (22, [(2, 38), (2, 39)]),
    ('L', 9): (30, [(2, 116)]),
    ('M', 9): (22, [(3, 36), (2, 37)]),
    ('L', 10): (18, [(2, 68), (2, 69)]),
    ('M', 10): (26, [(4, 43), (1, 44)]),
}

_ALIGN = {
    1: [], 2: [6, 18], 3: [6, 22], 4: [6, 26], 5: [6, 30],
    6: [6, 34], 7: [6, 22, 38], 8: [6, 24, 42], 9: [6, 26, 46], 10: [6, 28, 50],
}


def _data_capacity_bytes(version, ecl):
    ecw, groups = _BLOCK_TABLE[(ecl, version)]
    data_cw = sum(n * c for n, c in groups)
    # subtract mode (4 bits) + char-count indicator, then bytes
    cc_bits = 8 if version <= 9 else 16
    return (data_cw * 8 - 4 - cc_bits) // 8


def _choose_version(nbytes, ecl):
    for v in range(1, 11):
        if nbytes <= _data_capacity_bytes(v, ecl):
            return v
    raise ValueError("Data too long for QR versions 1–10 at level %s" % ecl)


# ----------------------------------------------------------------------------
# Bit buffer
# ----------------------------------------------------------------------------
class _Bits:
    def __init__(self):
        self.bits = []

    def put(self, value, length):
        for i in range(length - 1, -1, -1):
            self.bits.append((value >> i) & 1)

    def __len__(self):
        return len(self.bits)


def _encode_data(text, version, ecl):
    data = text.encode("utf-8")
    ecw, groups = _BLOCK_TABLE[(ecl, version)]
    total_data_cw = sum(n * c for n, c in groups)

    bb = _Bits()
    bb.put(0b0100, 4)                          # byte mode
    cc_bits = 8 if version <= 9 else 16
    bb.put(len(data), cc_bits)                 # char count
    for byte in data:
        bb.put(byte, 8)

    # terminator
    capacity_bits = total_data_cw * 8
    remaining = capacity_bits - len(bb)
    bb.put(0, min(4, max(0, remaining)))
    # pad to byte boundary
    while len(bb) % 8 != 0:
        bb.bits.append(0)
    # pad codewords
    pad = [0xEC, 0x11]
    i = 0
    while len(bb) < capacity_bits:
        bb.put(pad[i % 2], 8)
        i += 1

    # to codewords
    codewords = []
    for k in range(0, len(bb), 8):
        byte = 0
        for b in bb.bits[k:k + 8]:
            byte = (byte << 1) | b
        codewords.append(byte)

    # split into blocks and compute ECC
    blocks = []
    ptr = 0
    for num, cnt in groups:
        for _ in range(num):
            blk = codewords[ptr:ptr + cnt]
            ptr += cnt
            blocks.append((blk, _rs_encode(blk, ecw)))

    # interleave data codewords
    result = []
    max_data = max(len(b[0]) for b in blocks)
    for i in range(max_data):
        for blk, _ in blocks:
            if i < len(blk):
                result.append(blk[i])
    # interleave ec codewords
    for i in range(ecw):
        for _, ec in blocks:
            result.append(ec[i])

    return result


# ----------------------------------------------------------------------------
# Matrix construction
# ----------------------------------------------------------------------------
def _new_matrix(size):
    return [[None] * size for _ in range(size)]


def _place_finder(m, r, c):
    for dr in range(-1, 8):
        for dc in range(-1, 8):
            rr, cc = r + dr, c + dc
            if 0 <= rr < len(m) and 0 <= cc < len(m):
                if 0 <= dr <= 6 and 0 <= dc <= 6:
                    on = (dr in (0, 6) or dc in (0, 6) or (2 <= dr <= 4 and 2 <= dc <= 4))
                    m[rr][cc] = on
                else:
                    m[rr][cc] = False  # separator


def _place_alignment(m, version):
    centers = _ALIGN.get(version, [])
    size = len(m)
    for r in centers:
        for c in centers:
            # skip if overlapping finder patterns
            if (r < 8 and c < 8) or (r < 8 and c > size - 9) or (r > size - 9 and c < 8):
                continue
            for dr in range(-2, 3):
                for dc in range(-2, 3):
                    on = (abs(dr) == 2 or abs(dc) == 2 or (dr == 0 and dc == 0))
                    m[r + dr][c + dc] = on


def _place_timing(m):
    size = len(m)
    for i in range(8, size - 8):
        v = (i % 2 == 0)
        if m[6][i] is None:
            m[6][i] = v
        if m[i][6] is None:
            m[i][6] = v


def _reserve_format(m):
    size = len(m)
    for i in range(9):
        if m[8][i] is None:
            m[8][i] = False
        if m[i][8] is None:
            m[i][8] = False
    for i in range(size - 8, size):
        m[8][i] = False
        m[i][8] = False
    m[size - 8][8] = True  # dark module


def _reserve_version(m, version):
    if version < 7:
        return
    size = len(m)
    for i in range(6):
        for j in range(3):
            m[i][size - 11 + j] = False
            m[size - 11 + j][i] = False


def _mask_func(mask):
    return [
        lambda r, c: (r + c) % 2 == 0,
        lambda r, c: r % 2 == 0,
        lambda r, c: c % 3 == 0,
        lambda r, c: (r + c) % 3 == 0,
        lambda r, c: (r // 2 + c // 3) % 2 == 0,
        lambda r, c: (r * c) % 2 + (r * c) % 3 == 0,
        lambda r, c: ((r * c) % 2 + (r * c) % 3) % 2 == 0,
        lambda r, c: ((r + c) % 2 + (r * c) % 3) % 2 == 0,
    ][mask]


def _place_data(m, data_bits, mask):
    size = len(m)
    mf = _mask_func(mask)
    idx = 0
    up = True
    col = size - 1
    while col > 0:
        if col == 6:
            col -= 1
        cols = [col, col - 1]
        rng = range(size - 1, -1, -1) if up else range(size)
        for r in rng:
            for c in cols:
                if m[r][c] is None:
                    bit = data_bits[idx] if idx < len(data_bits) else 0
                    idx += 1
                    if mf(r, c):
                        bit ^= 1
                    m[r][c] = bool(bit)
        up = not up
        col -= 2


_FORMAT_ECL = {'L': 0b01, 'M': 0b00, 'Q': 0b11, 'H': 0b10}


def _format_value(ecl, mask):
    """Return the 15-bit format information value (bit 0 = LSB)."""
    data = (_FORMAT_ECL[ecl] << 3) | mask
    rem = data << 10
    gen = 0b10100110111
    for i in range(4, -1, -1):
        if rem & (1 << (i + 10)):
            rem ^= gen << i
    return ((data << 10) | rem) ^ 0b101010000010010


def _place_format(m, ecl, mask):
    fmt = _format_value(ecl, mask)
    size = len(m)

    def gb(j):
        return bool((fmt >> j) & 1)

    # Copy 1 — around the top-left finder (row, col) = bit index
    m[0][8] = gb(0); m[1][8] = gb(1); m[2][8] = gb(2)
    m[3][8] = gb(3); m[4][8] = gb(4); m[5][8] = gb(5)
    m[7][8] = gb(6); m[8][8] = gb(7); m[8][7] = gb(8)
    m[8][5] = gb(9); m[8][4] = gb(10); m[8][3] = gb(11)
    m[8][2] = gb(12); m[8][1] = gb(13); m[8][0] = gb(14)

    # Copy 2 — split across bottom-left and top-right
    for i in range(8):
        m[8][size - 1 - i] = gb(i)
    for i in range(8, 15):
        m[size - 15 + i][8] = gb(i)

    m[size - 8][8] = True  # dark module


def _version_bits(version):
    rem = version << 12
    gen = 0b1111100100101
    for i in range(5, -1, -1):
        if rem & (1 << (i + 12)):
            rem ^= gen << i
    return (version << 12) | rem


def _place_version(m, version):
    if version < 7:
        return
    bits = _version_bits(version)
    size = len(m)
    for i in range(18):
        bit = bool((bits >> i) & 1)
        r, c = i // 3, i % 3
        m[size - 11 + c][r] = bit
        m[r][size - 11 + c] = bit


def _penalty(m):
    size = len(m)
    score = 0
    # Rule 1: runs of 5+
    for line in (m, list(zip(*m))):
        for row in line:
            run = 1
            for i in range(1, size):
                if row[i] == row[i - 1]:
                    run += 1
                else:
                    if run >= 5:
                        score += 3 + (run - 5)
                    run = 1
            if run >= 5:
                score += 3 + (run - 5)
    # Rule 2: 2x2 blocks
    for r in range(size - 1):
        for c in range(size - 1):
            if m[r][c] == m[r][c + 1] == m[r + 1][c] == m[r + 1][c + 1]:
                score += 3
    # Rule 3: finder-like patterns
    pat1 = [True, False, True, True, True, False, True, False, False, False, False]
    pat2 = list(reversed(pat1))
    for row in (m + list(map(list, zip(*m)))):
        for c in range(size - 10):
            seg = list(row[c:c + 11])
            if seg == pat1 or seg == pat2:
                score += 40
    # Rule 4: dark ratio
    dark = sum(1 for row in m for v in row if v)
    ratio = dark * 100 // (size * size)
    score += 10 * (abs(ratio - 50) // 5)
    return score


def qr_matrix(text, ecl='M'):
    """Return the QR code as a matrix of booleans (True = dark module)."""
    nbytes = len(text.encode("utf-8"))
    version = _choose_version(nbytes, ecl)
    size = version * 4 + 17
    data = _encode_data(text, version, ecl)
    data_bits = []
    for byte in data:
        for i in range(7, -1, -1):
            data_bits.append((byte >> i) & 1)

    best = None
    best_score = None
    for mask in range(8):
        m = _new_matrix(size)
        _place_finder(m, 0, 0)
        _place_finder(m, 0, size - 7)
        _place_finder(m, size - 7, 0)
        _place_alignment(m, version)
        _place_timing(m)
        _reserve_format(m)
        _reserve_version(m, version)
        _place_data(m, data_bits, mask)
        _place_format(m, ecl, mask)
        _place_version(m, version)
        score = _penalty(m)
        if best_score is None or score < best_score:
            best_score = score
            best = m
    return best


def qr_svg(text, ecl='M', scale=6, quiet=4, dark="#0f172a", light="#ffffff"):
    """Render the QR code as a standalone SVG string."""
    m = qr_matrix(text, ecl)
    n = len(m)
    dim = (n + quiet * 2) * scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{dim}" height="{dim}" '
        f'viewBox="0 0 {dim} {dim}" shape-rendering="crispEdges" role="img" '
        f'aria-label="Gate pass QR code">',
        f'<rect width="{dim}" height="{dim}" fill="{light}"/>',
    ]
    for r in range(n):
        for c in range(n):
            if m[r][c]:
                x = (c + quiet) * scale
                y = (r + quiet) * scale
                parts.append(f'<rect x="{x}" y="{y}" width="{scale}" height="{scale}" fill="{dark}"/>')
    parts.append('</svg>')
    return "".join(parts)


def qr_data_uri(text, ecl='M', scale=6, quiet=4):
    """Render the QR code as a base64 data: URI (image/svg+xml)."""
    import base64
    svg = qr_svg(text, ecl, scale, quiet)
    b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return "data:image/svg+xml;base64," + b64


if __name__ == "__main__":
    print(qr_svg("GP-2026-ABC123")[:120], "...")
