#!/usr/bin/env python3
"""Generates catalogue/novastar.json: NovaStar LED display controllers and processors. Added 2026-11-14.

All-in-one controllers (VX Pro), sending boxes (MCTRL), the COEX MX40 Pro broadcast controller and the H series
modular splicing processors. Their RJ45 'Ethernet' outputs drive LED receiving cards over gigabit Ethernet cabling
(NovaStar protocol, not a LAN), and OPT ports are 10G fibre to NovaStar fibre converters. Sources are NovaStar
specification sheets hosted by dealers (each entry's productUrl); heights come from the printed dimensions
(about 50 mm = 1U with feet, about 95 mm = 2U)."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
MODELS = []
def add(id, pn, name, fam, ru, ports, notes, src, url, verified=True, **kw):
    m = dict(id='novastar-' + id, manufacturer='NovaStar', partNumber=pn, name=name, family=fam, category='converter', ru=ru,
             widthCols=12, fullDepth=kw.pop('full', True), verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); MODELS.append(m); return m
def led(n, conn='RJ45'): return R('out', 'Ethernet', conn, n, 'LED output (to receiving cards)')
def opt(n, label='OPT (10G fibre)', d='io'): return R(d, 'Fibre', 'LC (SFP)', n, label)
AC = R('in', 'Power', 'IEC C14', 1, 'AC In')
CTRL = lambda n=2: R('io', 'Ethernet', 'RJ45', n, 'Control Ethernet (PC / cascade)')
GEN = [R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop')]
VX_COMMON = [R('in', 'USB', 'USB-A', 1, 'USB 3.0 (media playback)'), R('out', 'HDMI', 'HDMI', 1, 'Monitor HDMI Out (1080p60)'),
             R('out', 'Other', 'Other', 1, '3D emitter'), R('in', 'Analog audio', '3.5mm jack', 1, 'Audio In'),
             R('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'), *GEN, R('io', 'USB', 'USB-B', 1, 'USB 2.0 (firmware, EDID, cascade)'),
             R('io', 'RS-232', 'Terminal block', 1, 'RS-232 (3-pin)'), R('in', 'Other', 'Other', 1, 'Light sensor'), F('io', 'USB', 'USB-B', 1, 'USB (NovaLCT PC)')]

VX6_DS = 'https://shop.captech.se/sv-SE/Product/167159/Link/94689/VX600%20Pro%20All-in-One%20Controller%20Specifications-V1.3.0.pdf'
add('vx400-pro', 'VX400 Pro', 'VX400 Pro all-in-one LED controller (2.6 Mpx, 4 outputs)', 'NovaStar VX Pro', 1,
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Loop'), R('in', 'HDMI', 'HDMI', 2, 'HDMI 1.3 In'),
     R('in', '3G-SDI', 'BNC', 1, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 1, '3G-SDI Loop'), opt(1, 'OPT 1 (10G fibre, in or out)'),
     led(4), CTRL(2)] + VX_COMMON + [AC],
    'Video processor and LED sending card in one: up to 2.6 million pixels over 4 gigabit outputs plus one 10G fibre port, 1U. '
    'Check: connectors (taken from the VX600 Pro).', 'NovaStar VX600 Pro specifications (sibling)', VX6_DS, verified=False, powerW=40, full=False)
add('vx600-pro', 'VX600 Pro', 'VX600 Pro all-in-one LED controller (3.9 Mpx, 6 outputs)', 'NovaStar VX Pro', 1,
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Loop'), R('in', 'HDMI', 'HDMI', 2, 'HDMI 1.3 In'),
     R('in', '3G-SDI', 'BNC', 1, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 1, '3G-SDI Loop'), opt(1, 'OPT 1 (10G fibre, in or out)'),
     opt(1, 'OPT 2 (10G fibre out)', 'out'), led(6), CTRL(2)] + VX_COMMON + [AC],
    'Video processor and LED sending card in one: up to 3.9 million pixels over 6 gigabit outputs plus 10G fibre. 482.6 x 302.2 x 50.1 mm '
    '(1U with feet), 3.9 kg, 43 W.', 'NovaStar VX600 Pro specifications V1.3.0', VX6_DS, powerW=43, weightKg=3.9, full=False)
add('vx1000-pro', 'VX1000 Pro', 'VX1000 Pro all-in-one LED controller (6.5 Mpx, 10 outputs)', 'NovaStar VX Pro', 1,
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Loop'), R('in', 'HDMI', 'HDMI', 2, 'HDMI 1.3 In'),
     R('in', '3G-SDI', 'BNC', 1, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 1, '3G-SDI Loop'), opt(1, 'OPT 1 (10G fibre, in or out)'),
     opt(1, 'OPT 2 (10G fibre out)', 'out'), led(10), CTRL(2)] + VX_COMMON + [AC],
    'Video processor and LED sending card in one: up to 6.5 million pixels over 10 gigabit outputs plus two 10G fibre ports. '
    '482.6 x 302.2 x 50.1 mm (1U with feet), 3.9 kg, 44 W.', 'NovaStar VX1000 Pro specifications',
    'https://manuals.plus/m/8e0a22850348a3d5645d848b96bead5e19b7e19d975076747ed498ce29c3d31b', powerW=44, weightKg=3.9, full=False)
add('vx2000-pro', 'VX2000 Pro', 'VX2000 Pro all-in-one LED controller (13 Mpx, 20 outputs)', 'NovaStar VX Pro', 2,
    [R('in', 'DisplayPort', 'DisplayPort', 1, 'DP 1.2 In'), R('in', 'HDMI', 'HDMI', 2, 'HDMI 2.0 In'), R('in', 'HDMI', 'HDMI', 4, 'HDMI 1.3 In'),
     R('in', '12G-SDI', 'BNC', 1, '12G-SDI In'), R('out', '12G-SDI', 'BNC', 1, '12G-SDI Loop'), opt(2, 'OPT 1-2 (10G fibre, in or out)'),
     opt(2, 'OPT 3-4 (10G fibre out)', 'out'), led(20), CTRL(2)] + VX_COMMON + [AC],
    'Video processor and LED sending card in one: up to 13 million pixels over 20 gigabit outputs plus four 10G fibre ports. '
    '482.6 x 493.0 x 94.6 mm (2U with feet), 7 kg, 83 W.', 'NovaStar VX2000 Pro specifications V1.0.3',
    'https://ret.de/wp-content/uploads/2025/08/VX2000-Pro-All-in-One-Controller-Specifications-V1.0.3.pdf', powerW=83, weightKg=7)
add('mx40-pro', 'MX40 Pro', 'COEX MX40 Pro LED display controller (9 Mpx, 20 outputs)', 'NovaStar COEX MX', 2,
    [R('in', 'HDMI', 'HDMI', 3, 'HDMI 2.0 In'), R('out', 'HDMI', 'HDMI', 3, 'HDMI 2.0 Loop'), R('in', 'DisplayPort', 'DisplayPort', 1, 'DP 1.2 In'),
     R('in', '12G-SDI', 'BNC', 1, '12G-SDI In'), R('out', '12G-SDI', 'BNC', 1, '12G-SDI Loop'), opt(4, 'OPT 1-4 (10G fibre out)', 'out'),
     led(20, 'etherCON'), *GEN, CTRL(2), R('out', 'Other', 'TOSLINK', 1, 'S/PDIF Out'), R('io', 'RS-232', 'RJ45', 1, 'AUX'),
     F('io', 'USB', 'USB-A', 1, 'USB 2.0'), AC],
    'Broadcast-grade LED controller for VMP software: up to 9 million pixels over 20 gigabit outputs plus four 10G fibre outputs, 12G-SDI, '
    'genlock. 482.6 x 467.0 x 94.2 mm (2U with feet), 7.5 kg, 95 W. The 20 LED outputs are etherCON, AUX is RJ45 and S/PDIF out is optical (rear photo).',
    'NovaStar MX40 Pro specifications V1.5.1', 'https://ret.de/wp-content/uploads/2026/07/MX40-Pro-LED-Display-Controller-Specifications-V1.5.1.pdf',
    powerW=95, weightKg=7.5)
add('mctrl4k', 'MCTRL4K', 'MCTRL4K LED sending box (8.8 Mpx, 16 outputs)', 'NovaStar MCTRL', 2,
    [R('in', 'DisplayPort', 'DisplayPort', 1, 'DP 1.2 In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'), R('in', 'DVI', 'DVI-D', 2, 'Dual-link DVI In'),
     led(16, 'etherCON'), opt(4, 'OPT 1-4 (fibre out, 3-4 backup)', 'out'), CTRL(1), R('in', 'USB', 'USB-B', 1, 'USB In (PC / cascade)'),
     R('out', 'USB', 'USB-A', 1, 'USB Out (cascade)'), *GEN, F('in', 'USB', 'USB-A', 1, 'USB (drive)'), AC],
    'LED sending box for 4K screens: up to 8.8 million pixels on 16 gigabit outputs (Neutrik etherCON) or 4 fibre outputs. '
    '482.6 x 372.0 x 96.0 mm (2U with feet), 4.6 kg, 30 W.', 'NovaStar MCTRL4K specifications',
    'https://www.fullcompass.com/common/files/62199-MCTRL4KSpecSheet.pdf', powerW=30, weightKg=4.6)
add('mctrl660-pro', 'MCTRL660 PRO', 'MCTRL660 PRO LED sending box (3.9 Mpx, 6 outputs)', 'NovaStar MCTRL', 1,
    [R('in', 'DVI', 'DVI-D', 1, 'DVI In'), R('out', 'DVI', 'DVI-D', 1, 'DVI Loop'), R('in', 'HDMI', 'HDMI', 1, 'HDMI 1.4 In'),
     R('out', 'HDMI', 'HDMI', 1, 'HDMI Loop'), R('in', '3G-SDI', 'BNC', 1, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 1, '3G-SDI Loop'),
     led(6), opt(2, 'OPT 1-2 (10G fibre)', 'out'), R('out', 'HDMI', 'HDMI', 1, 'Monitor HDMI Out'), *GEN, CTRL(1),
     R('in', 'USB', 'USB-B', 1, 'USB In'), R('out', 'USB', 'USB-A', 1, 'USB Out (cascade)'), F('io', 'USB', 'USB-B', 1, 'USB (firmware)'), AC],
    'Rental LED sending box: up to 3.9 million pixels on 6 gigabit outputs and two 10G fibre outputs, with DVI, HDMI and 3G-SDI loops. '
    '482.6 x 356.0 x 50.1 mm (1U with feet), 4.6 kg, 20 W.', 'NovaStar MCTRL660 PRO specifications',
    'https://spectra-displays.co.uk/wp-content/uploads/2022/07/MCTRL660-PRO.pdf', powerW=20, weightKg=4.6)
H = 'https://dynamo-led-displays.co.uk/novastar-led-processor-guide/'
for pn, ru, mpx, inp, snd, extra in (('H2', 2, 52, 4, 2, ''), ('H5', 5, 78, 10, 3, ''), ('H9', 9, 130, 15, 5, ' The H9 Enhanced takes 10 sending cards (260 Mpx).'),
                                      ('H15', 15, 260, 30, 10, ' The H15 Enhanced takes 16 sending cards (416 Mpx).'), ('H20', 20, 520, 40, 20, '')):
    add(pn.lower(), pn, f'{pn} modular video wall splicing processor ({ru}U, {inp} input cards, {snd} sending cards)', 'NovaStar H series', ru, [AC],
        f'Modular LED and LCD video wall processor: up to {inp} input cards (HDMI, DVI, DP, 12G-SDI, IP) and {snd} sending cards (20 gigabit '
        f'LED outputs each, about 13 Mpx), up to {mpx} million pixels.{extra} The cards are not modelled yet, so add their connectors with Edit model. '
        'Check: power inlets (larger frames have redundant supplies).', 'NovaStar H series overview (dealer guide)', H, verified=False)

ids = [m['id'] for m in MODELS]; assert len(ids) == len(set(ids))
json.dump(MODELS, open(os.path.join(CAT, 'novastar.json'), 'w'), indent=1)
print('novastar.json', len(MODELS), 'entries,', sum(m['verified'] for m in MODELS), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'novastar.json' not in idx: idx.append('novastar.json')
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
