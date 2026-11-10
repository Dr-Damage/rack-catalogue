#!/usr/bin/env python3
"""Generates catalogue/grassvalley.json (Grass Valley rack-mount products) from GV datasheets."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'grassvalley.json')
M = []
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=True, **kw):
    m = dict(id='gv-' + id, manufacturer='Grass Valley', partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

# ---------------- K-Frame XP switchers ----------------
KF = 'https://www.grassvalley.com/wp-content/uploads/2025/01/K-Frame_Switchers_DS-PUB-3-0572E-EN.pdf'
for code, ru, i, o, mv, gpi_i, tally, psu, psu_pn in [('VXP', 5, 48, 24, 3, 8, 24, 2, 'K-FRM-PSU-VXP'),
                                                      ('CXP', 8, 80, 40, 4, 8, 32, 2, 'K-FRM-PSU-XP'),
                                                      ('SXP', 15, 192, 96, 5, 8, 32, 3, 'K-FRM-PSU-XP')]:
    add(f'k-frame-{code.lower()}', f'K-Frame {code}', f'K-Frame {code} switcher engine', 'K-Frame', 'switcher', ru,
        [R('in', '3G-SDI', 'BNC', i, 'SDI In'), R('out', '3G-SDI', 'BNC', o, 'SDI Out'),
         R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('io', 'RS-422', 'DB9', 1, 'Serial'),
         R('in', 'Other', 'DB25', 1, f'GPI In ({gpi_i})'), R('out', 'Other', 'DB25', 1, f'GPI Out ({gpi_i})'),
         R('out', 'Other', 'DB25', 1, f'Tally ({tally})'), R('in', 'Power', 'IEC', psu, 'PSU')],
        f'{ru}RU K-Frame {code} video production engine, up to {i} in x {o} out on SDI and/or IP I/O cards '
        '(IP ports are 25 or 100 GbE, SFP/QSFP ordered separately), up to ' + str(mv) + ' multiviewers. '
        f'{gpi_i} GPI in / {gpi_i} out, {tally} tallies, serial and Ethernet machine control. {psu} x {psu_pn} hot-swap supplies'
        + (' in a separate 1RU external power frame.' if code == 'SXP' else ' (internal).') +
        ' Shown fully loaded with SDI. Check: connector types (BNC vs HD-BNC), reference and control port details, and your card fit.',
        'GV K-Frame switchers datasheet (DS-PUB-3-0572E)', KF, verified=False)
add('k-frame-sxp-psu', 'K-Frame SXP power frame', 'K-Frame SXP external power frame', 'K-Frame', 'power', 1,
    [R('in', 'Power', 'IEC', 3, 'AC In'), R('out', 'Power', 'Other', 1, 'DC to frame')],
    '1RU external power frame that sits with the 15RU K-Frame SXP and holds its K-FRM-PSU-XP supplies. Check: inlet count and DC link.',
    'GV K-Frame switchers datasheet', KF, verified=False)

# ---------------- Sirius routers ----------------
SC = 'https://grassvalley.com/products/routing/sirius-12g-compact-routers'
for code, ru, n in [('SCR 1616-12G', 1, 16), ('SCR 3232-12G', 2, 32)]:
    add(code.lower().replace(' ', '-'), code, f'Sirius {n}x{n} 12G compact router', 'Sirius', 'router', ru,
        [R('in', '12G-SDI', 'BNC', n, 'SDI In'), R('out', '12G-SDI', 'BNC', n, 'SDI Out'),
         R('in', 'Reference', 'BNC', 1, 'Ref'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
         R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'DB9', 1, 'RS-422'), R('io', 'USB', 'Mini-USB', 1, 'USB'),
         R('in', 'Power', 'DC barrel', 2, '12V DC')],
        f'{ru}RU {n}x{n} single-link 12G-SDI router, BNC, 39 mm deep. Two looping non-terminating reference BNCs (black burst or tri-level), '
        'gigabit Ethernet, RS-422 on DB9 (GV Native protocol), Mini-USB for setup. 10-14V DC from an external AC adapter, '
        'two DC inputs for the optional redundant supply (SCRPS1A). Check: DC connector type.',
        'GV Sirius compact routers datasheet (DS-PUB-3-1006C)', SC, full=False)
S8 = 'https://gvcmsumb.grassvalley.com/products/routing/sirius-800-series'
for code, ru, mx in [('830', 17, '288x288'), ('840', 29, '576x576'), ('850', 38, '576x1152')]:
    add(f'sirius-{code}', f'Sirius {code}', f'Sirius {code} router frame ({mx})', 'Sirius', 'router', ru,
        [R('in', 'Reference', 'BNC', 4, 'Video Ref'), R('io', 'Ethernet', 'RJ45', 2, 'Controller'), R('in', 'Power', 'IEC', 4, 'PSU')],
        f'{ru}RU including redundant PSUs, {mx} video, coax and fibre I/O cards, integrated audio processing, dual redundant controllers '
        'with auto failover, 4 video references. Card I/O not included: add it to the device as extra ports. '
        'Check: rear layout, PSU inlet count and Ethernet count.',
        'GV Sirius 800 datasheet (DS-PUB-3-0711C)', S8, verified=False)

# Densite frames and cards are in catalogue/gv-densite.json (card frames thread).

# ---------------- Multiviewers ----------------
KMX = 'https://media.iewc.com/SpecificationSheets/KALEIDO-MX-8X1.pdf'
for i, h, ru in [(8, 1, 1), (8, 2, 1), (16, 1, 1), (16, 2, 1), (16, 4, 1), (24, 1, 1), (24, 2, 1),
                 (32, 2, 3), (32, 4, 3), (48, 2, 3), (48, 4, 3), (64, 2, 3), (64, 4, 3)]:
    aud = 0 if (i, h) == (16, 4) else (min(h, 2) if ru == 1 else h)
    ports = [R('in', '3G-SDI', 'BNC', i, 'SDI In'), R('out', 'HDMI', 'HDMI', h, 'HDMI Out'), R('out', 'HD-SDI', 'BNC', h, 'SDI Out'),
             R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'Other', 'DB25', 1, 'GPI')]
    if aud: ports.append(R('out', 'Analog audio', 'Other', aud, 'Audio Monitor'))
    ports.append(R('in', 'Power', 'IEC', 2, 'PSU'))
    add(f'kaleido-mx-{i}x{h}', f'KALEIDO-MX-{i}X{h}', f'Kaleido-MX {i}x{h} multiviewer', 'Kaleido', 'monitor', ru, ports,
        f'{ru}RU multiviewer, {i} inputs, {"single" if h == 1 else "dual" if h == 2 else "quad"} head ({h} HDMI + {h} HD-SDI outputs). '
        'External multiformat reference, 10/100 Ethernet, ' + ('20 opto GPI in + 8 bidirectional' if ru == 1 else '20 (40 optional) opto GPI in + 8 (16) bidirectional') +
        f', hot-swap redundant PSUs ({"150" if ru == 1 else "350"} W max). Optional discrete audio via ABT modules. '
        'Check: GPI and audio monitor connector types.', 'Kaleido-MX datasheet', KMX)
add('kip-x240', 'KIP-X240', 'Kaleido-IP X240 IP multiviewer', 'Kaleido', 'monitor', 1,
    [R('io', 'Ethernet', 'RJ45', 2, 'Mgmt 1GbE'), R('in', 'SFP', 'SFP', 2, '10GbE Media'), R('in', 'SFP', 'QSFP', 4, '100GbE Media (opt)'),
     R('out', 'HDMI', 'HDMI', 4, 'Head Out'), R('in', 'Power', 'IEC', 2, 'PSU')],
    '1RU IP multiviewer: 2 x 10GbE compressed inputs, optional up to 4 x 100GbE uncompressed, 4 independent HDMI or DisplayPort outputs, '
    '2 x 1GbE management, 750 W 1+1 hot-swap PSUs. SDI via GV ST 2110 gateways, GPI via GPI-1501. Check: optional 100GbE fit.',
    'GV Kaleido-IP datasheet (DS-PUB-3-0133C)', 'https://www.grassvalley.com/products/multiviewers-hardware/kaleido-ip/')

# ---------------- Servers ----------------
K2 = 'https://wwwapps.grassvalley.com/manuals/k2_summit_v10.1.3/core/sub/topic/k2/c_k2_summit_3gplus_production_client_specifications.html'
for ch in (2, 4):
    add(f'k2-summit-3gplus-{ch}ch', f'K2 Summit 3G+ {ch} channel', f'K2 Summit 3G+ {ch}-channel server', 'K2', 'recorder', 2,
        [R('io', '3G-SDI', 'BNC', ch, 'SDI Ch'), R('out', 'HD-SDI', 'BNC', 1, 'SDI Monitor'),
         R('in', 'Reference', 'HD-BNC', 1, 'Ref'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'),
         R('io', 'Timecode', 'Mini-XLR', ch, 'LTC'), R('io', 'RS-422', 'DB9', 4, 'RS-422'), R('io', 'Other', 'DB25', 1, 'GPI (12 in/12 out)'),
         R('io', 'Ethernet', 'RJ45', 1, 'Ethernet 1G'), R('io', 'Ethernet', 'SFP', 2, '10GbE'), R('io', 'AES/EBU', 'DB25', ch, 'AES (opt)'),
         R('out', 'DisplayPort', 'DisplayPort', 1, 'DP'), R('in', 'Power', 'IEC', 2, 'PSU')],
        f'2RU, 61.6 cm deep. {ch} bidirectional HD/SD-SDI record/play channels (each channel configured as in or out), SDI monitor out with '
        'timecode burn-in, 2 HD-BNC reference loop, LTC on mini-XLR per channel, 4 RS-422, GPI 12 in/12 out on DB25, 1G plus 10GbE, '
        '4 AES pairs per channel (optional DB25), DisplayPort GUI out, dual redundant hot-swap 600 W PSUs. '
        'Check: SDI connector type and whether each channel has separate in and out BNCs.',
        'K2 Summit 3G+ production client specifications', K2, verified=False)

# ---------------- Camera base station ----------------
XCU = 'https://www.grassvalley.com/products/cameras/xcu-xpress-uxf/'
add('xcu-xpress-uxf', 'XCU Xpress UXF + cradle', 'XCU Xpress UXF camera base station', 'LDX cameras', 'converter', 2,
    [R('out', '3G-SDI', 'BNC', 6, 'SDI Out'), R('out', 'HD-SDI', 'BNC', 2, 'Live/Effect'), R('out', 'HD-SDI', 'BNC', 1, 'HD Monitor'),
     R('out', 'HD-SDI', 'BNC', 3, 'SD Out/Mon'), R('out', 'Other', 'BNC', 1, 'CVBS Monitor'), R('io', 'SFP', 'SFP', 4, 'SFP (12G/10GbE)'),
     R('in', '3G-SDI', 'BNC', 3, 'Ext In'), R('in', 'Reference', 'BNC', 2, 'Ref Loop'), R('in', 'Other', 'BNC', 2, 'Prompter Loop'),
     R('io', 'Other', 'DB15', 1, 'Intercom'), R('io', 'Other', 'DB15', 1, 'Tally'), R('io', 'Other', 'DB9', 1, 'Data RS-232'),
     R('out', 'Analog audio', 'XLR', 2, 'Audio Out'), R('out', 'AES/EBU', 'BNC', 2, 'AES Out'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'),
     R('io', 'Fibre', 'LEMO SMPTE', 1, 'Camera Fibre'), R('in', 'Power', 'IEC', 1, 'AC In')],
    '2RU base station that slides into a rack cradle (cradle stores settings), 12.5 kg with cradle. Outputs depend on mode: 4K 2 x 4K + 2 x 3G; '
    '1X 6 x 3G + 2 x 1.5G; 3X/6X 6 x 3G. 3 return inputs (input 1 loops), ref and prompter loop-through, intercom DB15, tally DB15, '
    'RS-232 DB9, 2 XLR + 2 AES audio out, C2IP and IP trunk Ethernet, 4 SFP+ (12G or 10GbE), LEMO hybrid fibre. '
    'Check: exact BNC count on the rear.', 'GV XCU datasheet (DS-PUB-3-1041B)', XCU, verified=False)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(OUT, 'w'), indent=1)
print(len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
