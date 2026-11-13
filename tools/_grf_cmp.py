
import struct, re, io, os, glob, collections, sys
grfs = sys.argv[1:] or ["generated/cirs.grf"]
expect = set()
for f in glob.glob("src/grf/lang/*.toml"):
    m = re.search(r'grflangid\s*=\s*"(0x[0-9A-Fa-f]+)"', io.open(f, encoding="utf-8").read())
    if m: expect.add(int(m.group(1), 16))
for grf in grfs:
    b = open(grf, "rb").read()
    ids = collections.Counter(); i = 15; n = 0
    while i + 5 <= len(b):
        size = struct.unpack_from("<I", b, i)[0]
        if size == 0 or i + 5 + size > len(b) or b[i+4] != 0xFF: break
        d = b[i+5:i+5+size]
        if len(d) > 2 and d[0] == 0x04: ids[d[2] & 0x7F] += 1
        i += 5 + size; n += 1
    have = set(ids) - {0x7F}
    print("%-24s bytes=%-10d action4_recs=%-6d langs=%d expected=%d missing=%s extra=%s default=%d" % (
        os.path.basename(grf), len(b), n, len(have), len(expect),
        sorted("%02X" % x for x in expect - have), sorted("%02X" % x for x in have - expect), ids.get(0x7F, 0)))
