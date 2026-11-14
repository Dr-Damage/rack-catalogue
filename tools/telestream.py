#!/usr/bin/env python3
"""Generates catalogue/telestream.json: Telestream (formerly Tektronix) sync gear, also sold by Ross Video as the SPG-9000 and ECO-8000.
Added 2026-11-14. Rear panels from Telestream's product sheets and photos (SPG9000 rear photo on rossvideo.com, ECO8000 rear drawing in
product sheet D00013331A)."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
M = []
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, **kw):
    m = dict(id='telestream-' + id, manufacturer='Telestream', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=12,
             fullDepth=True, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

add('spg9000', 'SPG9000', 'SPG9000 master reference and test signal generator (Ross SPG-9000)', 'SPG9000', 'other', 1,
    [F('io', 'USB', 'USB-A', 1, 'USB'),
     R('in', 'Power', 'IEC C14', 2, 'PSU'), R('out', '12G-SDI', 'HD-BNC', 4, 'SDI'), R('io', 'SFP', 'SFP28', 2, 'IP (10/25G)'),
     R('io', 'Ethernet', 'SFP+', 2, 'PTP (1/10G)'), R('out', 'AES/EBU', 'BNC', 1, 'DARS'), R('out', 'Reference', 'BNC', 1, 'Word Clock'),
     R('in', 'Other', 'SMA', 1, 'GNSS Antenna'), R('io', 'Ethernet', 'RJ45', 1, 'MGMT / NTP'), R('io', 'GPI', 'D-sub', 1, 'GPI'),
     R('io', 'Timecode', 'DB15', 1, 'LTC / GPI'), R('out', 'Reference', 'BNC', 6, 'Black'),
     R('in', 'Reference', 'BNC', 1, 'Genlock Ref In'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop')],
    'Master sync and timing: 6 black outputs (black burst, tri-level, 10 MHz or 1 PPS), genlock in with passive loop, word clock and '
    'DARS (AES/EBU) BNCs, 4 LTC outs (or 3 out and 1 in) on a 15-pin D-sub (XLR breakout SPG9000-XLR), GPI, GNSS receiver (SMA antenna '
    'input, option GNSS), 2 PTP ports on SFP+ (1/10G, ST 2059 / AES67, option PTP), 2 IP test signal ports on SFP28 (10/25G, ST 2110 '
    'with 2022-7, option IP), 4 SD to 12G-SDI test signal outputs on HD-BNC (option SDI), RJ45 management and NTP. Front: display, keypad, '
    'USB. Hot-swap power supplies: one (SPG9000-SPW) or two (SPG9000-DPW), IEC C14, 100-240V AC, 130 VA typical and 180 VA max. '
    '482.6 x 44 x 516 mm, 4.85 kg; rack kit SPG9000-RACK. Sold by Ross Video as the SPG-9000 '
    '(https://www.rossvideo.com/products/signal-processing/spg-9000/). Pairs with the ECO8000 changeover.',
    'Telestream SPG9000 product sheet and rear photo', 'https://www.telestream.com/SPG9000/', powerW=180, weightKg=4.85)

ECO = []
for ch in range(1, 10):
    t = 'Reference' if ch <= 6 else '3G-SDI'
    ECO += [R('in', t, 'BNC', 1, f'Ch {ch} Primary In'), R('in', t, 'BNC', 1, f'Ch {ch} Backup In'), R('out', t, 'BNC', 1, f'Ch {ch} Out')]
add('eco8000', 'ECO8000', 'ECO8000 automatic changeover unit (Ross ECO-8000)', 'SPG9000', 'other', 1,
    [R('in', 'Power', 'IEC C14', 2, 'AC In')] + ECO +
    [R('io', 'Ethernet', 'RJ45', 1, 'MGMT'), R('io', 'GPI', 'DE-15', 1, 'GPI'), R('in', 'Timecode', 'DE-15', 1, 'Primary LTC/SPG'),
     R('out', 'Timecode', 'DE-15', 1, 'LTC Out'), R('in', 'Timecode', 'DE-15', 1, 'Backup LTC/SPG')],
    'Automatic changeover between a primary and a backup SPG9000 (or SPG8000A). 9 BNC channels, each with primary in, backup in and '
    'output: channels 1-6 are 50 MHz electronic fast-switch channels for black burst, tri-level, AES/DARS and word clock; channels 7-9 are '
    '3 GHz relay channels that also pass SD/HD/3G-SDI. 4 LTC channels on DE-15 connectors (primary and backup LTC/SPG in, LTC out; XLR '
    'breakout ECO8000 XLR), GPI, RJ45 management (web UI, SNMP). Front: LCD, auto/manual and source buttons, per-channel fault LEDs, and '
    'two hot-swap power supplies that pull out from the front; IEC C14 inlets at the back, 100-240V AC, 50 VA max. 483 x 43.7 x 557 mm, '
    '4.5 kg; rack slides ECO8000 RACK, 12 inch cable set ECO8000 CBL. Sold by Ross Video as the ECO-8000 '
    '(https://www.rossvideo.com/products/signal-processing/eco-8000/), whose page lists a 3-channel base unit with REF, HREF and LTC '
    'options; Telestream\'s current sheet lists all 9 channels and 4 LTC as standard.',
    'Telestream ECO8000 product sheet D00013331A (rear panel drawing)',
    'https://www.telestream.com/wp-content/uploads/2025/12/eco8000-automatic-changeover-Unit-Datasheet-D00013331A.pdf', powerW=50, weightKg=4.5)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(os.path.join(CAT, 'telestream.json'), 'w'), indent=1)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'telestream.json' not in idx: idx.append('telestream.json'); json.dump(idx, open(ip, 'w'))
print('telestream.json', len(M), 'entries')
