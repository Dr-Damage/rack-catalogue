#!/usr/bin/env python3
"""Generates catalogue/ross.json (Ross Video rack-mount products).
Port data from Ross spec pages and quick start guides (documentation.rossvideo.com).
verified=False and a 'Check:' note mark anything not confirmed from a Ross document."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'ross.json')
M = []
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=True, **kw):
    m = dict(id='ross-' + id, manufacturer='Ross Video', partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

ULX = 'https://www.rossvideo.com/infrastructure/routing-systems/ultrix/specifications/'
ULXQS = 'Ross Ultrix specifications page, Ultrix FR1/FR2 Quick Start Guide (2101DR-002) and Ultrix Installation Guide (2101DR-003)'
DCIN = lambda: [R('in', 'Power', 'DC locking', 1, 'PWR 1 (main)'), R('in', 'Power', 'DC locking', 1, 'PWR 2 (redundant)')]

# ---------------- Ultrix ----------------
for fr, ru, slots, mx, wt in [('FR1', 1, 1, '36x36', '4.06 kg'), ('FR2', 2, 3, '72x72', '5.44 kg')]:
    add(f'ultrix-{fr.lower()}', f'ULTRIX-NS-{fr}', f'Ultrix {fr} ({ru}RU)', 'Ultrix', 'router', ru,
        [R('in', '12G-SDI', 'HD-BNC', 16, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 16, 'SDI Out'),
         R('io', 'SFP', 'SFP', 2, 'AUX'), R('in', 'Reference', 'HD-BNC', 1, 'Ref A'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'),
         R('io', 'Ethernet', 'RJ45', 2, 'ENET'), R('io', 'USB', 'USB-A', 1, 'USB (serial)'), R('in', 'Power', '4-pin DC', 4, 'PSU 15V')],
        f'{ru}RU hyperconverged router frame. Built-in 16 x 16 HD-BNC (bottom row: OUT 1-16 then IN 1-16) plus 2 AUX SFP ports '
        f'(SDI, HDMI or 64 ch MADI), {slots} I/O/processing card slot{"s" if slots > 1 else ""} above it, max matrix {mx}. '
        'ENET 1 primary, ENET 2 backup 1GbE. USB-A for a USB-serial adapter. Four 15V DC PSU inputs numbered 1-4 from the left, '
        f'fed by external supplies (brick or Ultripower); ships with {"one supply" if fr == "FR1" else "two supplies"}. Frame weight {wt}. '
        'Card I/O (HDX-IO, MODX-IO, IP cards) is not included: add it to the device as extra ports. '
        + ('Also the host frame for Ultrix Carbonite (up to 2 SDPE switcher blades). ' if fr == 'FR2' else '') +
        'Check: any GPI ports on your hardware revision.',
        ULXQS, ULX)
for fr, ru, slots, mx, ups, wt in [('FR5', 5, 9, '160x160', 2, '6.35 kg'), ('FR12', 12, 16, '288x288', 3, '34.47 kg')]:
    add(f'ultrix-{fr.lower()}', f'ULTRIX-{fr}', f'Ultrix {fr} ({ru}RU)', 'Ultrix', 'router', ru,
        [R('in', 'Reference', 'HD-BNC', 2, 'Ref In'), R('out', 'Reference', 'HD-BNC', 2, 'Ref Loop'),
         R('io', 'Ethernet', 'RJ45', 2, 'ENET'), R('io', 'RS-422', 'RJ45', 1, 'Serial'),
         R('in', 'Power', 'DC locking', ups, 'Ultripower In')],
        f'{ru}RU Ultrix frame with {slots} I/O/processing slots' + (' (one is a FLEX slot)' if fr == 'FR5' else '') +
        f', max matrix {mx}, no built-in SDI. Powered from up to {ups} external 1RU Ultripower frames (plus redundant). '
        f'Frame weight {wt} without cards. Host frame for Ultrix Carbonite and Ultrix Acuity (SDPE blades: '
        + ('up to 4' if fr == 'FR5' else 'up to 8') + '; each blade adds GPI DB25, Tally DB25, Editor, 2 AES, LTC). '
        'Card I/O is not included: add it to the device as extra ports. '
        'Check: exact rear layout and connector types for the reference, serial and Ethernet ports.',
        'Ross Ultrix specifications page; Ultrix Carbonite and Acuity frame guides', ULX, verified=False)
add('ultrix-fr30', 'Ultrix 30RU frame', 'Ultrix 30RU frame', 'Ultrix', 'router', 30,
    [R('in', 'Reference', 'HD-BNC', 2, 'Ref In'), R('out', 'Reference', 'HD-BNC', 2, 'Ref Loop'),
     R('io', 'Ethernet', 'RJ45', 2, 'ENET'), R('in', 'Power', 'IEC', 8, 'PSU module')],
    '30RU Ultrix frame, 32 I/O/processing slots, max matrix 576x576, up to 8 integrated plug-in power modules (2N redundancy), '
    '16.9 in deep, 123 kg without cards. Card I/O not included. Check: part number, rear connectors and power inlet type.',
    'Ross Ultrix specifications page', ULX, verified=False)
add('ultripower', 'ULTRIPOWER', 'Ultripower 1RU power frame', 'Ultrix', 'power', 1,
    [R('in', 'Power', 'IEC', 1, 'Mains In'), F('out', 'Power', 'DC locking', 4, 'DC Out'), F('io', 'Ethernet', 'RJ45', 1, 'Ethernet')],
    '1RU external power frame for Ultrix FR5/FR12, Ultrix Carbonite and Acuity blades, optional on FR1/FR2 and Carbonite Ultra. '
    'Front labelled ports 1-4, OUT, RESTART, ETHERNET, RESET. Several units are grouped and managed with Ultripower Manager. '
    'Check: which face the DC outputs are on, mains inlet count, and output count on your unit.',
    'Ultrix Acuity FR12 frame guide (4842DR-201)', ULX, verified=False)

# ---------------- NRG ----------------
NRG = 'https://www.rossvideo.com/infrastructure/routing-systems/nrg/'
for lcp in ('', '-LCP'):
    add('nrg-fr1' + lcp.lower(), 'NRG-FR1' + lcp, 'NRG 16x16 router (1RU)' + (' with local panel' if lcp else ''), 'NRG', 'router', 1,
        [R('in', '12G-SDI', 'HD-BNC', 16, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 16, 'SDI Out'),
         R('in', 'Reference', 'HD-BNC', 1, 'Ref'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'),
         R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-A', 1, 'USB'), R('out', 'DisplayPort', 'DisplayPort', 1, 'DP (MV)')] + DCIN(),
        '1RU 16x16 12G router, 270 Mb/s to 12G, ASI, MADI. Output 16 doubles as the quad-split multiviewer SDI output; '
        'DisplayPort 1.2a multiviewer head. 15V DC on PWR 1, optional redundant supply on PWR 2, no power switch. '
        f'{"Front local control panel. 35.2" if lcp else "31.7"} W max. 8.8 cm deep. Control: GVG Native, SW-P-08. '
        'Check: USB connector type.',
        'NRG-FR1 and NRG-FR1-LCP Quick Start Guide (2200DR-401)', NRG, full=False)
    add('nrg-fr2' + lcp.lower(), 'NRG-FR2' + lcp, 'NRG 32x34 router (2RU)' + (' with local panel' if lcp else ''), 'NRG', 'router', 2,
        [R('in', '12G-SDI', 'HD-BNC', 32, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 32, 'SDI Out'),
         R('out', '12G-SDI', 'HD-BNC', 2, 'MV'),
         R('in', 'Reference', 'HD-BNC', 1, 'Ref'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'),
         R('io', 'Ethernet', 'RJ45', 2, 'ETH'), R('io', 'USB', 'USB-A', 1, 'USB'), R('out', 'DisplayPort', 'DisplayPort', 1, 'DP (MV)')] + DCIN(),
        '2RU 32x34 12G router (32 BNC in and out plus MV1/MV2 outputs). One quad-split multiviewer head standard, second licensable; '
        'DisplayPort 1.2a head output. ETH 1 primary, ETH 2 backup. 15V DC, redundant PWR 2. '
        f'{"Front local control panel. 64.0" if lcp else "56.6"} W max. Check: MV1/MV2 connector type (assumed HD-BNC SDI).',
        'NRG-FR2 and NRG-FR2-LCP Quick Start Guide (2200DR-402)', NRG, full=False)
add('nrg-fr3', 'NRG-FR3', 'NRG 64x68 router (3RU)', 'NRG', 'router', 3,
    [R('in', '12G-SDI', 'HD-BNC', 64, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 64, 'SDI Out'), R('out', '12G-SDI', 'HD-BNC', 4, 'MV'),
     R('in', 'Reference', 'HD-BNC', 1, 'Ref'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'),
     R('io', 'Ethernet', 'RJ45', 2, 'ETH'), R('out', 'DisplayPort', 'DisplayPort', 1, 'DP (MV)')] + DCIN(),
    '3RU 64x68 12G router, no local panel option, 2.90 kg. Check: part number, how the 68 outputs split between router and MV outputs, '
    'and the rear ports (inferred from the FR2).', 'NRG product page and solution brief', NRG, verified=False, full=False)

# ---------------- NK ----------------
NKU = 'https://www.rossvideo.com/products/routing-systems/nk-3g-series/'
def nk(code, ru, i, o, w, url=NKU, vid='3G-SDI', conn='BNC', fam='NK', note=''):
    add(code.lower(), code, f'{code} {i}x{o} router', fam, 'router', ru,
        [R('in', vid, conn, i, 'In'), R('out', vid, conn, o, 'Out'), R('io', 'Other', 'RJ45', 2, 'T-Bus'),
         R('in', 'Power', 'DC locking', 1, '+15V DC'), R('in', 'Power', 'DC locking', 1, 'Redundant DC')],
        f'{ru}RU {i}x{o} {vid} utility router, 75 ohm BNC, cable-equalised inputs, reclocking outputs. +15V DC from the included universal '
        f'supply, {w} W; optional redundant NK-RP1/P (1RU) or a second NK-P1. Set up by web browser or DashBoard via NK-IPS. {note}'
        'Check: T-Bus and reference connectors on the rear (not listed on the Ross page).',
        'Ross NK series product pages', url, verified=False, full=False)
nk('NK-3G164', 1, 16, 4, 16)
nk('NK-3G16', 1, 16, 16, 16)
nk('NK-3G34', 2, 34, 34, 30)
nk('NK-3G64', 3, 64, 64, 60, 'https://www.rossvideo.com/products/routing-systems/nk-3g64/', note='Expandable in groups of 8 in and 8 out. Check: rack height. ')
nk('NK-3G72', 3, 72, 72, 60, 'https://www.rossvideo.com/products/routing-systems/nk-3g72/', note='Expandable in groups of 8 in and 8 out, 12 cm deep. ')
add('nk-rp1', 'NK-RP1/P', 'NK-RP1 redundant power supply', 'NK', 'power', 1,
    [R('in', 'Power', 'IEC', 1, 'Mains In'), R('out', 'Power', 'DC locking', 2, '+15V DC Out')],
    '1RU 100 W +15V redundant supply for NK routers, connects with NK-S12/P or NK-D12/PN cables. Check: number of DC outputs.',
    'Ross NK product pages', 'https://www.rossvideo.com/products/routing-systems/nk-rp1/', verified=False, full=False)
add('nk-3g144', 'NK-3G144', 'NK-3G144 144x144 router', 'NK', 'router', 10,
    [R('in', '3G-SDI', 'BNC', 144, 'In'), R('out', '3G-SDI', 'BNC', 144, 'Out'), R('out', '3G-SDI', 'BNC', 32, 'Out Dup (113-144)'),
     R('in', 'Reference', 'BNC', 2, 'Vid Ref (loop)'), R('io', 'Other', 'RJ45', 2, 'T-Bus'), R('out', 'Other', 'Terminal', 1, 'Alarm GPI'),
     R('in', 'Power', 'IEC', 2, 'PSU')],
    '10RU, 320 mm deep, 144x144 3G/HD/SD-SDI router built from 8-port input (NK-I3G) and output (NK-O3G) cards, 18 input and 22 output slots. '
    'Slots 15D-18D give duplicate outputs 113D-144D for monitoring. Looping reference, T-Bus on RJ45 (straight CAT5), alarm relay, '
    'one PSU included with a second IEC for a redundant load-sharing PSU, under 500 W. No Ethernet on the frame; control via NK-IPS. '
    'Check: number of T-Bus RJ45 connectors.',
    'Ross NK-3G144 User Guide (9807DR-5600)', 'https://documentation.rossvideo.com/files/Manuals/Routers/NK/NK-3G144%20User%20Guide%20(9807DR-5600).pdf')
add('nk-ips', 'NK-IPS', 'NK-IPS network bridge', 'NK', 'control', 1,
    [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'Other', 'RJ45', 8, 'T-Bus'), R('in', 'Power', 'DC locking', 1, '+15V DC'),
     R('in', 'Power', 'DC locking', 1, 'Redundant DC')],
    '1RU, 2.4 cm deep. Gateway from Ethernet (10 Mbps, static or DHCP) to the NK T-Bus, with a buffered 8-port T-Bus hub; web and DashBoard '
    'set-up, firmware and alarms. Universal supply included, optional NK-RP1/P or NK-P1 redundant power. Check: T-Bus connector type.',
    'Ross NK-IPS product page', 'https://www.rossvideo.com/products/routing-systems/nk-ips/', verified=False, full=False)
add('nk-vrc', 'NK-VRC', 'NK-VRC virtual routing core', 'NK', 'control', 1,
    [R('io', 'Other', 'RJ45', 2, 'T-Bus'), R('in', 'Power', 'DC locking', 1, '+15V DC'), R('in', 'Power', 'DC locking', 1, 'Redundant DC')],
    'Maps physical sources and destinations of an NK system to virtual ones and ties router levels (for example analog and digital) through '
    'external resources. Universal supply included, optional NK-RP1/P (NK-D12/P cable) or NK-P1. Needs DashBoard. '
    'Check: rack height (1RU assumed from a site drawing) and rear connectors, not listed on the Ross page.',
    'Ross NK-VRC product page', 'https://www.rossvideo.com/products/routing-systems/nk-vrc/', verified=False, full=False)
for n, ru, w in [(16, 1, 9), (32, 2, 15)]:
    add(f'nk-m{n}', f'NK-M{n}', f'NK-M{n} machine control / data router', 'NK', 'router', ru,
        [R('io', 'RS-422', 'DB9', n, 'Port'), R('io', 'Other', 'RJ45', 2, 'T-Bus'), R('in', 'Power', 'DC locking', 1, '+15V DC'),
         R('in', 'Power', 'DC locking', 1, 'Redundant DC')],
        f'{ru}RU {n}-port RS-422 machine control (data) router, DB9 female ports, 6.4 cm deep, {w} W. Universal supply included, '
        'optional NK-RP1/P or NK-P1 redundant power. Check: T-Bus connectors.',
        'Ross NK-M series product page', 'https://www.rossvideo.com/products/routing-systems/nk-m-series/', full=False)

# ---------------- Switchers ----------------
CU = 'https://www.rossvideo.com/live-production/production-switchers/carbonite-ultra/specifications/'
add('carbonite-ultra', 'Carbonite Ultra', 'Carbonite Ultra 1RU switcher frame', 'Carbonite', 'switcher', 1,
    [R('in', '12G-SDI', 'HD-BNC', 24, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 10, 'SDI Out'), R('out', '12G-SDI', 'HD-BNC', 2, 'MV Out'),
     R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Out'), R('in', 'Timecode', 'Other', 1, 'LTC In'),
     R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'RJ45', 1, 'Editor'), R('io', 'Other', 'DB25', 1, 'GPI/O (24)'),
     R('out', 'Other', 'DB25', 1, 'Tally (24)'), R('out', 'AES/EBU', 'Other', 2, 'AES Out'), R('in', 'Power', 'DC locking', 1, 'DC In')],
    '1RU, 254 mm deep, 5.9 kg. 24 HD-BNC inputs (18 at UHD), 12 outputs: 10 assignable plus 2 dedicated MultiViewer (11 at UHD). '
    'Up to 3 MEs and 4 MiniMEs, up to 4 MultiViewers. 24 GPI/O and 24 tallies, RS-422 editor port, LTC input, 2 AES outputs. '
    '114 W from the standard external supply or optional Ultripower. Also the frame for Carbonite Mosaic. '
    'Optional 1RU Audio Breakout Module (8 analog in, 5 out, AES in/out). Check: GPI/tally, LTC and AES connector types.',
    'Ross Carbonite Ultra specifications page', CU)
add('carbonite-ultra-solo', 'Carbonite Ultra Solo', 'Carbonite Ultra Solo switcher', 'Carbonite', 'switcher', 1,
    [R('in', '12G-SDI', 'HD-BNC', 12, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 6, 'SDI Out'),
     R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Power', 'DC locking', 1, 'DC In')],
    '12 in, 6 out, 1 ME, 2 MiniMEs, 1 MultiViewer, UHD capable. Sold as an all-in-one unit or 1RU. '
    'Check: rear connectors (only counts are published) and whether outputs include the MultiViewer.',
    'Ross Carbonite Ultra series page', 'https://www.rossvideo.com/products/production-switchers/carbonite-ultra-solo/', verified=False)
add('carbonite-ultra-60', 'Carbonite Ultra 60', 'Carbonite Ultra 60 3RU switcher frame', 'Carbonite', 'switcher', 3,
    [R('in', '12G-SDI', 'HD-BNC', 60, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 20, 'SDI Out'), R('out', '12G-SDI', 'HD-BNC', 5, 'MV Out'),
     R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'), R('out', 'Reference', 'HD-BNC', 1, 'Ref Out'),
     R('in', 'Timecode', 'Other', 1, 'LTC In'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'RJ45', 1, 'Serial'),
     R('io', 'Other', 'DB25', 1, 'GPI/O (24)'), R('out', 'Other', 'DB25', 1, 'Tally (24)'), R('in', 'Power', 'IEC', 1, 'AC In')],
    '3RU modular frame, 444.5 mm rear width, 9.07 kg. Shown fully loaded (3 I/O boards: 60 in x 25 out). Base engine is 12 x 4; '
    '2 boards give 36 x 12. Up to 3 MEs, 4 MiniMEs, up to 7 MultiViewers. 24 GPI/O, 24 tallies, 1 serial, LTC in, ref in and loop plus '
    'independent ref out. 800 W 12V DC supply, AC 100-240 V. Check: split of the 25 outputs between program and MV, connector types.',
    'Ross Ultra 60 / Ultrix Carbonite / Acuity product matrix (2024)', 'https://www.rossvideo.com/live-production/production-switchers/carbonite-ultra-60/')
add('carbonite-black-x36', 'Carbonite Black (x36 / x36+ / x36+12G)', 'Carbonite Black frame (x36 family)', 'Carbonite', 'switcher', 2,
    [R('in', '3G-SDI', 'BNC', 36, 'SDI In'), R('out', '3G-SDI', 'BNC', 17, 'SDI Out'), R('out', '3G-SDI', 'BNC', 5, 'MV Out'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('out', 'Reference', 'BNC', 1, 'Ref Out'),
     R('in', 'Timecode', 'Other', 1, 'LTC In'), R('io', 'Ethernet', 'RJ45', 2, 'LAN'), R('io', 'RS-422', 'RJ45', 1, 'Serial'),
     R('io', 'Other', 'DB37', 1, 'GPI/O (34)'), R('out', 'Other', 'DB37', 1, 'Tally (34)'), R('out', 'AES/EBU', 'Other', 1, 'AES Out'),
     R('in', 'Power', 'IEC', 2, 'PS')],
    'Carbonite Black / Black+ / Black+ 12G frame (x36, x36+, x36+12G). 36 BNC inputs, outputs up to 22 (11-22 have format converters on '
    'x36+), MultiViewers on outputs 1-2 plus MV3-MV5 on x36+ frames. GPI/O DB37 (34 lines), Tally DB37 (34), RS-422 on RJ45, LAN1/LAN2, '
    'AES stereo out, LTC in, PS1/PS2 supplies. 120 W (x36), 180 W (x36+), 206 W (x36+12G); x36+12G inputs are 12G. '
    'Check: rack height and exact output count for your frame.',
    'Carbonite Black hardware quick start (4804DR-200-11)', 'https://www.rossvideo.com/products/production-switchers/carbonite-ultra/', verified=False)
add('graphite', 'Graphite', 'Graphite all-in-one production system', 'Graphite', 'switcher', 4,
    [R('in', 'Power', 'IEC', 2, 'Power')],
    '4RU all-in-one system: Carbonite switcher, audio mixer, XPression graphics and clip player. '
    'Check: rear I/O is not published on the product page, add the ports from your unit.',
    'Ross Graphite product page', 'https://www.rossvideo.com/products/production-switchers/all-in-one-production-systems/', verified=False)

# ---------------- Servers ----------------
TRIA = 'https://www.rossvideo.com/live-production/video-servers-replay/production-servers/tria-plus/specifications/'
for ch in (4, 8, 12):
    q = ch // 4
    add(f'tria-plus-{ch}ch', f'Tria+ {ch} channel', f'Tria+ {ch}-channel production server', 'Tria', 'recorder', 3,
        [R('in', '3G-SDI', 'HD-BNC', ch, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', ch, 'SDI Out'), R('out', '3G-SDI', 'BNC', q, 'Quad Viewer'),
         R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('in', 'Timecode', 'XLR', 1, 'LTC In'), R('io', 'RS-422', 'RJ45', 8, 'RS-422'),
         R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-A', 9, 'USB'), R('out', 'DisplayPort', 'DisplayPort', 2, 'DP'),
         R('out', 'HDMI', 'HDMI', 1, 'HDMI'), R('io', 'AES/EBU', 'DB25', 2, 'AES'), R('out', 'Analog audio', '3.5mm jack', q, 'Monitor Out'),
         R('in', 'Power', 'IEC', 2, 'PSU')],
        f'3RU, 65.1 cm deep, slide rails included. {ch} bi-directional channels (each 1 SDI in, 1 SDI out on HD-BNC, quad-link 2160p supported), '
        f'{q} quad viewer BNC out. Ref in, LTC XLR, 8 RS-422 on RJ45 (octal breakout to D9), gigabit Ethernet, 2 DP + 1 HDMI GUI outputs, '
        'AES on 2 x D25, dual hot-swap PSUs. Check: 10G Ethernet option.',
        'Ross Tria+ specifications page', TRIA)

# ---------------- openGear ----------------
OGX = 'https://www.rossvideo.com/products/signal-processing/opengear/frames-accessories/ogx-frame/'
# slot geometry agreed with the card frames thread (see catalogue/FRAMES.md)
FRAME = {"system": "openGear", "slots": 20, "slotOrder": "ltr", "rearAlign": 2, "door": True,
         "controller": "GFC-8322 in a dedicated slot right of PS1; network card MFC-OG3-N",
         "front": {"x0": 0.10, "x1": 0.98, "y0": 0.05, "y1": 0.95}, "rear": {"x0": 0.02, "x1": 0.82, "y0": 0.05, "y1": 0.95}}
for sfx, card, net in [('-CNS', 'MFC-OG3-N', '1000BASE-T, SNMP'), ('-CN', 'MFC-OG3-N', '1000BASE-T'), ('-C', 'MFC-8322-S', '100BASE-TX')]:
    add('ogx-fr' + sfx.lower(), 'OGX-FR' + sfx, f'openGear OGX-FR{sfx} 20-slot frame', 'openGear', 'converter', 2,
        [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Reference', 'BNC', 2, 'Ref'), R('out', 'Reference', 'BNC', 2, 'Ref Loop'),
         R('in', 'Power', 'IEC', 2, 'PS')],
        f'2RU openGear oGx frame, 20 front-loading card slots with rear module slots. {card} network/controller card ({net}). '
        'REF 1 and REF 2 with loops, PS1 main and PS2 redundant power (100-240 V, IEC C13 cords). Allow 2 in side and 5 in rear clearance. '
        'Place cards in the frame\'s slots.',
        'OGX-FR Quick Start Guide (8322DR-202)', OGX, frame=dict(FRAME, rearGen=4))
add('og3-fr', 'OG3-FR', 'openGear OG3-FR 20-slot frame (legacy)', 'openGear', 'converter', 2,
    [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Reference', 'BNC', 2, 'Ref'), R('out', 'Reference', 'BNC', 2, 'Ref Loop'),
     R('in', 'Power', 'IEC', 2, 'PS')],
    'Previous-generation 2RU, 20-slot openGear frame. Place cards in the frame\'s slots. Check: rear layout (assumed same as OGX-FR).',
    'Ross openGear page', OGX, verified=False, frame=dict(FRAME, rearGen=3))
add('dfr-8321', 'DFR-8321', 'openGear DFR-8321 20-slot frame (legacy)', 'openGear', 'converter', 2,
    [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Reference', 'BNC', 2, 'Ref'), R('out', 'Reference', 'BNC', 2, 'Ref Loop'),
     R('in', 'Power', 'IEC', 2, 'PS')],
    'First-generation 2RU, 20-slot openGear frame (DFR-8321-BN with network card, -C with cooling door); takes DFR-8321 generation rear '
    'modules. Superseded by OG3-FR and OGX-FR. Place cards in the frame\'s slots. Check: rear layout (assumed same as OGX-FR) and the Ethernet '
    'option fitted.', 'Ross openGear page', OGX, verified=False, frame=dict(FRAME, rearGen=2))

# ---------------- Control ----------------
UT = 'https://www.rossvideo.com/control-systems/routing-control/ultritouch/specifications/'
for ru in (2, 4):
    add(f'ultritouch-{ru}ru', f'Ultritouch {ru}RU', f'Ultritouch {ru}RU touchscreen panel', 'Ultrix', 'control', ru,
        [R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('out', 'HDMI', 'HDMI', 1, 'HDMI'), R('io', 'USB', 'USB-A', 1, 'USB'),
         R('in', 'Power', 'DC locking', 2, 'DC In')],
        f'{ru}RU touchscreen control panel (DashBoard/Ultrix control), 2.5 in deep, Gorilla Glass. Redundant Ethernet, HDMI, USB, '
        'external power supply with optional redundant supply.' + (' VESA mount.' if ru == 4 else '') +
        ' Check: connector counts (page lists features, not counts).',
        'Ross Ultritouch specifications page', UT, verified=False, full=False)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(OUT, 'w'), indent=1)
print(len(M), 'entries ->', os.path.abspath(OUT))
