#!/usr/bin/env python3
"""Adds traced panel layouts (`layout` + `layoutSource`) to catalogue entries. Format: catalogue/README.md, "Panel layout".

Each layout is traced from the maker's published rear (or front) panel picture. Coordinates are fractions of the
full 19-inch panel (482.6 mm wide, rack ears included; a part-width unit uses its own widthCols share of it),
origin top-left; rear is as seen from behind the rack.
For an ear-less rear view the chassis is centred in the 19-inch frame before tracing.

Run after any generator (generators rewrite their brand files without layouts), then tools/manifest.py:
    python3 tools/layouts.py && python3 tools/manifest.py
"""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
W_MM = 482.6


def r4(v): return round(v, 4)


class Panel:
    """Helpers that turn traced connector centres into layout blocks for a panel `ru` units high.
    With `chassis` (mm), rear x values given to the helpers are fractions of an ear-less chassis of that width,
    centred in the 19-inch frame (front views include the ears, so front x values are used as given);
    y values are always fractions of the panel height."""
    def __init__(self, ru, source, chassis=None, width=W_MM):
        self.h = ru * 44.45; self.w = width; self.source = source
        self.k = (chassis or width) / width; self.off = (1 - self.k) / 2
        self.out = {'rear': [], 'front': [], 'fixtures': []}

    def X(self, x, face='rear'): return self.off + x * self.k if face == 'rear' else x
    def fx(self, mm, axis): return mm / (self.w if axis == 'x' else self.h)

    def _blk(self, g, x0, y0, x1, y1, rows=1, cols=1, start=None, count=None, order='row', frm='tl', size=None, face='rear'):
        b = dict(g=g)
        if start is not None: b['start'] = start
        if count is not None: b['count'] = count
        b.update(x0=r4(x0), y0=r4(y0), x1=r4(x1), y1=r4(y1), rows=rows, cols=cols, order=order)
        b['from'] = frm
        if size: b['size'] = r4(size)
        self.out[face].append(b); return self

    def blk(self, g, x0, y0, x1, y1, rows=1, cols=1, face='rear', **kw):
        """A block given by its rectangle."""
        return self._blk(g, self.X(x0, face), y0, self.X(x1, face), y1, rows, cols, face=face, **kw)

    def one(self, g, cx, cy, wmm=12, hmm=12, start=None, face='rear'):
        """A single connector centred at (cx, cy), wmm x hmm footprint."""
        cx = self.X(cx, face); w, h = self.fx(wmm, 'x') / 2, self.fx(hmm, 'y') / 2
        n = None if start is None else 1
        return self._blk(g, cx - w, cy - h, cx + w, cy + h, start=start, count=n, face=face)

    def line(self, g, cx0, cx1, cy, n, hmm=None, start=None, frm='tl', face='rear'):
        """n connectors in one row, first centre cx0, last centre cx1 (x order as drawn; use frm='tr' for right-to-left numbering)."""
        cx0, cx1 = self.X(cx0, face), self.X(cx1, face)
        p = (cx1 - cx0) / (n - 1) if n > 1 else self.fx(14, 'x')
        h = self.fx(hmm, 'y') / 2 if hmm else min(p * self.w / self.h, 0.9) / 2
        cnt = None if start is None else n
        return self._blk(g, cx0 - p / 2, cy - h, cx1 + p / 2, cy + h, 1, n, start=start, count=cnt, frm=frm, face=face)

    def grid(self, g, cx0, cy0, cx1, cy1, rows, cols, start=None, order='row', frm='tl', face='rear'):
        """rows x cols connectors; (cx0, cy0) first-row-first-column centre, (cx1, cy1) last-row-last-column centre."""
        cx0, cx1 = self.X(cx0, face), self.X(cx1, face)
        px = (cx1 - cx0) / (cols - 1) if cols > 1 else self.fx(14, 'x')
        py = (cy1 - cy0) / (rows - 1) if rows > 1 else self.fx(14, 'y')
        cnt = None if start is None else rows * cols
        return self._blk(g, cx0 - px / 2, cy0 - py / 2, cx1 + px / 2, cy1 + py / 2, rows, cols, start=start, count=cnt,
                         order=order, frm=frm, face=face)

    def fixture(self, kind, x0, y0, x1, y1, text=None, face='rear'):
        f = dict(face=face, kind=kind, x0=r4(self.X(x0, face)), y0=r4(y0), x1=r4(self.X(x1, face)), y1=r4(y1))
        if text: f['text'] = text
        self.out['fixtures'].append(f); return self

    def done(self):
        return {k: v for k, v in self.out.items() if v}, self.source


LAYOUTS = {}


def layout(pid, ru, source, chassis=None, cols=12):
    p = Panel(ru, source, chassis, W_MM * cols / 12); LAYOUTS[pid] = p; return p


# ---------------- AJA ----------------
# KUMO 3232-12G: rear photo on the product page. Groups: 0 SDI In, 1 SDI Out, 2 Ref, 3 Ref Loop, 4 Ethernet, 5 RS-422,
# 6 USB, 7 12V DC (2).
p = layout('aja-kumo-3232-12g', 2, 'AJA KUMO 3232-12G product page rear photo')
for g, ys in ((0, (0.137, 0.384)), (1, (0.632, 0.884))):
    for row, cy in enumerate(ys):
        p.line(g, 0.369, 0.611, cy, 8, hmm=18, start=row * 16 + 1)
        p.line(g, 0.691, 0.937, cy, 8, hmm=18, start=row * 16 + 9)
p.one(2, 0.316, 0.139).one(3, 0.317, 0.387)
p.one(4, 0.166, 0.22, 16, 14).one(5, 0.126, 0.29, 12.5, 31).one(6, 0.207, 0.21, 8, 5)
p.one(7, 0.07, 0.214, 10, 10, start=1).one(7, 0.07, 0.41, 10, 10, start=2)
p.fixture('label', 0.06, 0.78, 0.29, 0.95, 'KUMO 3232-12G')

# FS4: rear drawing on the product page (ear-less chassis, 444.5 mm wide, centred). Groups: 0 SDI In, 1 SDI Out,
# 2 12G In (SFP), 3 12G Out (SFP), 4 Monitor Out, 5 HDMI, 6 Ref, 7 Ref Loop, 8 AES In, 9 AES Out, 10 MADI In,
# 11 MADI In Fibre, 12 MADI Out, 13 MADI Out Fibre, 14 GPI, 15 Ethernet, 16 PSU (2).
p = layout('aja-fs4', 1, 'AJA FS4 product page rear drawing')
p.line(0, 0.594, 0.703, 0.345, 4, hmm=15).line(1, 0.594, 0.703, 0.757, 4, hmm=15)
p.blk(2, 0.426, 0.15, 0.457, 0.40, 1, 2, start=1, count=2, frm='tr').blk(2, 0.469, 0.15, 0.499, 0.40, 1, 2, start=3, count=2, frm='tr')
p.blk(3, 0.426, 0.53, 0.457, 0.82, 1, 2, start=1, count=2).blk(3, 0.469, 0.53, 0.499, 0.82, 1, 2, start=3, count=2)
p.one(4, 0.820, 0.344).one(5, 0.813, 0.74, 15, 6).one(6, 0.862, 0.28).one(7, 0.862, 0.646)
p.one(8, 0.18, 0.25, 40, 11).one(9, 0.18, 0.69, 40, 11)
p.one(10, 0.321, 0.27).one(12, 0.279, 0.27).one(11, 0.393, 0.27, 9, 9).one(13, 0.368, 0.27, 9, 9)
p.one(14, 0.301, 0.69, 40, 11).one(15, 0.383, 0.65, 16, 13)
p.one(16, 0.086, 0.53, 24, 24, start=1).one(16, 0.916, 0.53, 24, 24, start=2)


# ---------------- Ross ----------------
# Ultrix FR1 / FR2: rear-panel line drawings, Ultrix Installation Guide (2101DR-003) figures 8 and 9 (ear-less chassis,
# x as chassis fractions). Groups: 0 SDI In, 1 SDI Out, 2 AUX (SFP), 3 Ref A, 4 Ref Loop, 5 ENET, 6 USB, 7 PSU 15V (4).
# Only the built-in bottom row is ported; the blade slots above are drawn as fixtures.
for fr, ru, ys in (('fr1', 1, dict(base=0.806, aux=0.74, e1=0.293, e2=0.764, usb=0.73, slots=[(0, 0.49)])),
                   ('fr2', 2, dict(base=0.909, aux=0.90, e1=0.667, e2=0.872, usb=0.86, slots=[(0, 0.272), (0.272, 0.511), (0.511, 0.761)]))):
    p = layout(f'ross-ultrix-{fr}', ru, 'Ross Ultrix Installation Guide (2101DR-003), rear panel figure', chassis=440)
    b = ys['base']; hm = 9 if ru == 1 else 10
    p.line(1, 0.3007, 0.6328, b, 16, hmm=hm).line(0, 0.6564, 0.9885, b, 16, hmm=hm)
    p.one(3, 0.1743, b, 9, hm).one(4, 0.2020, b, 9, hm)
    p.one(2, 0.238, ys['aux'], 14, 9, start=1).one(2, 0.269, ys['aux'], 14, 9, start=2)
    p.one(5, 0.0235, ys['e1'], 16, 13, start=1).one(5, 0.0235, ys['e2'], 16, 13, start=2)
    p.one(6, 0.0485, ys['usb'], 6, 13)
    p.line(7, 0.0752, 0.1442, b, 4, hmm=9)
    for i, (y0, y1) in enumerate(ys['slots']):
        p.fixture('slot', 0.063, y0 + 0.01, 0.999, y1 - 0.01, f'Slot {i + 1} (I/O blade)')

# ---------------- Dell ----------------
# PowerEdge R660: technical guide figure 1 (front, 8 x 2.5-inch) and figure 5 (rear, 3 x LP slots). Rear chassis 434 mm.
# Groups: 0-2 front VGA, USB 2.0, iDRAC Direct; 3 VGA, 4 USB 2.0, 5 USB 3.0, 6 iDRAC,
# 7 1GbE LOM (2), 8 OCP 3.0, 9 PCIe slot (3), 10 PSU (2, PSU 1 assumed left as seen from the rear). The optional
# serial port is not shown in Dell's views, so the R660/R760 entries leave it out.
p = layout('dell-poweredge-r660', 1, 'Dell PowerEdge R660 Technical Guide, chassis views', chassis=434)
p.one(0, 0.922, 0.49, 11, 15, face='front').one(1, 0.959, 0.45, 6, 13, face='front').one(2, 0.959, 0.77, 7, 4, face='front')
p.one(3, 0.7335, 0.735, 17, 9).one(5, 0.6755, 0.639, 14, 6).one(4, 0.6755, 0.865, 14, 6).one(6, 0.6303, 0.768, 15, 13)
p.one(7, 0.2787, 0.768, 15, 13, start=1).one(7, 0.3284, 0.768, 15, 13, start=2).one(8, 0.4497, 0.768, 73, 15)
p.line(9, 0.3626, 0.7174, 0.284, 3, hmm=13)
p.one(10, 0.169, 0.51, 24, 20, start=1).one(10, 0.943, 0.51, 24, 20, start=2)
p.fixture('psu', 0.082, 0.05, 0.217, 0.95, 'PSU 1').fixture('psu', 0.843, 0.05, 0.989, 0.95, 'PSU 2')
p.fixture('slot', 0.011, 0.08, 0.066, 0.92, 'BOSS')

# PowerEdge R760: technical guide figure 6 (front, 16 x E3.S) and figure 7 (rear, 8 slots). Rear chassis 434 mm.
# Same groups as the R660, with 8 PCIe slots per Dell's riser map: riser 1 (left) slots 1-2, riser 2 (middle) 3 and 6,
# riser 3 (lower middle) 4-5, riser 4 (right) 7-8. Which slot is upper in each riser is assumed.
p = layout('dell-poweredge-r760', 2, 'Dell PowerEdge R760 Technical Guide, chassis views and riser map', chassis=434)
p.one(1, 0.9586, 0.305, 6, 13, face='front').one(0, 0.9858, 0.305, 11, 15, face='front').one(2, 0.9599, 0.796, 5, 9, face='front')
p.one(3, 0.728, 0.871, 17, 9).one(5, 0.6739, 0.838, 14, 6).one(4, 0.6739, 0.937, 14, 6).one(6, 0.6333, 0.894, 15, 13)
p.one(7, 0.2781, 0.894, 15, 13, start=1).one(7, 0.3288, 0.894, 15, 13, start=2).one(8, 0.4675, 0.894, 73, 15)
p.one(9, 0.1495, 0.156, 70, 15, start=1).one(9, 0.1495, 0.374, 70, 15, start=2)
p.one(9, 0.359, 0.656, 60, 15, start=4).one(9, 0.5386, 0.656, 60, 15, start=5)
p.one(9, 0.508, 0.156, 70, 15, start=3).one(9, 0.508, 0.374, 70, 15, start=6)
p.one(9, 0.853, 0.189, 70, 15, start=7).one(9, 0.853, 0.407, 70, 15, start=8)
p.one(10, 0.1664, 0.762, 24, 20, start=1).one(10, 0.9445, 0.762, 24, 20, start=2)
p.fixture('psu', 0.0142, 0.53, 0.2104, 0.977, 'PSU 1').fixture('psu', 0.789, 0.53, 0.985, 0.977, 'PSU 2')

# ---------------- Sony ----------------
# PDW-F1600 / PDW-HD1500 (half-rack, 3RU box; 210 mm face centred in it): rear-panel drawing, PDW-HD1500/F1600
# Operation Manual, "Rear Panel". Groups: 0 SDI In, 1 HD-SDI Out, 2 SD-SDI Out, 3 Composite Out, 4 Ref In, 5 Ref Loop,
# 6 TC In, 7 TC Out, 8 Audio In, 9 Audio Out, 10 Monitor Out, 11 AES In, 12 AES Out, 13 Remote (9-pin), 14 Video Control,
# 15 i.LINK, 16 Ethernet, 17 USB (maint), 18 Headphones (front), 19 AC In, 20 DC In 12V, 21 DC Out 12V (REMOTE 4-pin).
for pid in ('sony-pdw-f1600', 'sony-pdw-hd1500'):
    p = layout(pid, 3, 'Sony PDW-HD1500/F1600 Operation Manual, rear panel drawing', chassis=210, cols=6)
    p.one(19, 0.2615, 0.140, 27, 20).one(21, 0.5705, 0.189, 9, 9).one(20, 0.6883, 0.129, 19, 19)
    p.line(8, 0.1057, 0.2182, 0.398, 2, hmm=20).line(9, 0.336, 0.4444, 0.413, 2, hmm=20).line(10, 0.5569, 0.6707, 0.413, 2, hmm=20)
    p.line(11, 0.0894, 0.1870, 0.6065, 2, hmm=12).line(12, 0.0894, 0.1870, 0.7269, 2, hmm=12)
    p.one(0, 0.3198, 0.6065).line(1, 0.4065, 0.4892, 0.6065, 2, hmm=12).line(2, 0.336, 0.4648, 0.731, 2, hmm=12)
    p.line(3, 0.6369, 0.7263, 0.7204, 2, hmm=12).one(4, 0.813, 0.7204).one(5, 0.8916, 0.7204)
    p.one(6, 0.813, 0.8925).one(7, 0.8916, 0.8925)
    p.one(15, 0.1057, 0.8817, 11, 7).one(14, 0.271, 0.8925, 31, 12.5).one(13, 0.4743, 0.8925, 31, 12.5)
    p.line(17, 0.5867, 0.6274, 0.8925, 2, hmm=14).one(16, 0.7114, 0.8817, 16, 13)

# ---------------- apply ----------------
def check(e, lay):
    groups = e['portGroups']; placed = {}
    for face in ('rear', 'front'):
        for b in lay.get(face, []):
            g = b['g']; assert 0 <= g < len(groups), (e['id'], 'bad g', g)
            n = groups[g]['count']; s = b.get('start', 1); c = b.get('count', n)
            assert s >= 1 and s + c - 1 <= n, (e['id'], 'slice past group end', b)
            assert c <= b['rows'] * b['cols'], (e['id'], 'more ports than cells', b)
            assert 0 <= b['x0'] < b['x1'] <= 1 and 0 <= b['y0'] < b['y1'] <= 1, (e['id'], 'rect outside panel', b)
            assert groups[g]['face'] == face, (e['id'], 'block face differs from group face', b)
            placed[g] = placed.get(g, 0) + c
    for g, c in placed.items():
        assert c == groups[g]['count'], (e['id'], 'group', g, groups[g]['prefix'], 'placed', c, 'of', groups[g]['count'])


def main():
    todo = {k: v.done() for k, v in LAYOUTS.items()}
    seen = set()
    for f in json.load(open(os.path.join(CAT, 'index.json'))):
        path = os.path.join(CAT, f); raw = open(path, encoding='utf-8').read(); data = json.loads(raw)
        ascii_ok = json.dumps(data, indent=1) == raw
        changed = False
        for e in data:
            if e['id'] in todo:
                lay, src = todo[e['id']]; check(e, lay); seen.add(e['id'])
                if e.get('layout') != lay or e.get('layoutSource') != src:
                    e['layout'] = lay; e['layoutSource'] = src; changed = True
        if changed:
            open(path, 'w', encoding='utf-8').write(json.dumps(data, indent=1, ensure_ascii=ascii_ok))
            print('updated', f)
    missing = set(todo) - seen
    if missing: raise SystemExit(f'layouts for unknown ids: {sorted(missing)}')
    print(len(seen), 'layouts applied')


if __name__ == '__main__':
    main()
