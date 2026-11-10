#!/usr/bin/env python3
"""Generates rack-mount encoders, recorders, switchers and frames from a streaming-equipment brand list (2026-11-11):
vitec.json, dveo.json, awselemental.json, epiphan.json, teradek.json, kiloview.json, tascam.json, panasonic.json,
roland.json, lynx.json, lumens.json. AJA BRIDGE LIVE lives in others.py (aja.json).
Brands on the list with no rack-mount product (desktop/USB/camera-top only) are listed at the bottom."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, pre, mfr, id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=pre + id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
AA = 'Analog audio'

# ---------------- VITEC ----------------
VI = lambda *a, **k: add('vitec.json', 'vitec-', 'VITEC', *a, **k)
VI('mgw-diamond', 'MGW Diamond', 'MGW Diamond 4K / multi-channel HEVC encoder', 'MGW', 'converter', 1,
   [R('in', '3G-SDI', 'HD-BNC', 4, 'SDI/Composite In'), R('in', AA, 'Breakout', 4, 'Analog audio In'), R('out', AA, 'Breakout', 1, 'Talkback Out'),
    R('io', 'Ethernet', 'RJ45', 1, 'GigE'), R('io', 'SFP', 'SFP', 1, 'SFP (GigE)'), R('io', 'USB', 'USB-A', 1, 'USB'),
    R('io', 'Other', 'Breakout', 4, 'RS-232 (KLV)'), R('out', 'Other', 'BNC', 1, 'DVB-ASI'), R('in', 'Power', '12V DC', 1, 'DC In')],
   'Compact box 109.6 x 40.1 x 107.6 mm, 12 V DC 14-17 W (external PSU). Optional 1RU 19-inch rack kit; also made as an openGear card '
   '(MGW Diamond OG). Up to 4 x 3G/HD/SD-SDI or composite inputs on HD-BNC, 1 x 4K or 4 x HD HEVC/H.264. Analog audio, talkback and serial '
   'are on breakout cable 17239. Check: how many units the rack kit holds (4 per 1RU assumed) and the DVB-ASI port.',
   'VITEC MGW Diamond datasheet', 'https://vitec.com/product/mgw-diamond', w=3)

# ---------------- DVEO ----------------
DV = lambda *a, **k: add('dveo.json', 'dveo-', 'DVEO', *a, **k)
for n in (1, 2, 4, 8):
    DV(f'premio-{n}ch', f'Premio {n}ch SDI', f'Premio {n}-channel 3G-SDI to IP broadcast encoder', 'Premio', 'converter', 1,
       [R('in', '3G-SDI', 'BNC', n, 'SDI In'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('in', 'Power', 'IEC', 1, 'AC In')],
       f'1RU Windows-based broadcast encoder, {n} x 3G-SDI in, 2 Ethernet ports, 100-240 V. Encodes H.264/HEVC to SRT, UDP, RTMP, HLS. '
       'Check: extra server ports (USB, VGA) and PSU count.', 'DVEO Premio data sheet',
       'https://dveo.com/products/premio' + ('' if n == 1 else f'-{n}ch-sdi'), full=True)

# ---------------- AWS Elemental ----------------
add('awselemental.json', 'aws-', 'AWS Elemental', 'live-l900', 'Elemental Live L900 series', 'Elemental Live L900-series encoder appliance',
    'Elemental Live', 'converter', 1,
    [R('io', 'Other', 'Card slot', 2, 'SDI card (AJA, 3G/12G)'), R('io', 'SFP', 'QSFP28', 2, 'ConnectX-6 (red/blue)'),
     R('io', 'Ethernet', 'RJ45', 2, 'Management'), R('in', 'Power', 'IEC', 2, 'AC In')],
    '1RU server chassis (L900, L901, L910, L920, L940, L980; -U models add uncompressed ST 2110). Needs 31.85 in rack depth '
    '(L900/L901: 21.04 in). SDI I/O on AJA PCIe cards, 10/25/40/100G networking on NVIDIA ConnectX-6 QSFP28. DC kits for L910 and up. '
    'Check: SDI count per SKU, management ports and PSUs (AWS publishes these per SKU on request).',
    'AWS Elemental Live L900 announcement (AWS Media blog)', 'https://aws.amazon.com/elemental-live/', verified=False, full=True)

# ---------------- Epiphan ----------------
for code, twin in [('ESP1151', 1), ('ESP1152', 2)]:
    k = twin
    add('epiphan.json', 'epiphan-', 'Epiphan', f'pearl-2-rackmount{"-twin" if twin == 2 else ""}', code,
        f'Pearl-2 Rackmount{" Twin" if twin == 2 else ""} live production / streaming / recording system', 'Pearl-2', 'switcher', 2,
        [R('in', '12G-SDI', 'BNC', 2 * k, 'SDI In'), R('in', 'HDMI', 'HDMI', 2 * k, 'HDMI In'), R('in', 'HDMI', 'HDMI', 2 * k, '4K HDMI In'),
         R('in', AA, 'XLR3F', 4 * k, 'XLR In'), R('in', AA, 'RCA', 2 * k, 'RCA In'), R('out', 'HDMI', 'HDMI', 2 * k, 'HDMI Out'),
         R('in', 'USB', 'USB-A', 2 * k, 'USB 3.0 (UVC)'), F('io', 'USB', 'USB-A', k, 'USB 3.0'), F('out', AA, '3.5mm', k, 'Audio monitor'),
         R('io', 'Ethernet', 'RJ45', k, 'Ethernet'), R('in', 'Power', 'IEC', 1, 'AC In')],
        '2RU, 485 x 89 x 276 mm incl. tabs, ' + ('5.5 kg' if twin == 1 else '6.6 kg; two independent Pearl-2 systems in one chassis') +
        '. Per system: 2 x 12G-SDI, 2 x HDMI, 2 x 4K HDMI (4K add-on), 4 XLR line, RCA pair, 2 HDMI out, front touch screen. '
        'Check: AC inlet count on the Twin.', 'Epiphan Pearl-2 tech specs', 'https://www.epiphan.com/products/pearl-2/')

# ---------------- Teradek ----------------
for ru, cards, red in [(1, 3, False), (2, 9, True)]:
    add('teradek.json', 'teradek-', 'Teradek', f'prism-rack-{ru}ru', f'Prism Rack {ru}RU', f'Prism Rack {ru}RU chassis ({cards} cards)', 'Prism', 'converter', ru,
        [F('io', 'Other', 'Card slot', cards, 'Prism card'), R('io', 'Ethernet', 'RJ45', 2, 'GigE'), R('in', 'Power', 'IEC', 2 if red else 1, 'AC In')],
        f'{ru}RU chassis for {cards} Prism cards: 853 encoder (12G-SDI in + loop, 3.5 mm audio), 873 decoder (2 x 12G-SDI out), 877 Duplex '
        '(SDI or HDMI, encode or decode), server cards. Up to 15 W per card. Dual gigabit Ethernet' + (', redundant power.' if red else '.') +
        ' Add each card\'s connectors as extra ports. Check: which face cards load from, PSU inlets.',
        'Teradek Prism Rack page and Prism 4K 1RU/2RU specs', 'https://teradek.com/pages/prism-ru', verified=False)

# ---------------- Kiloview ----------------
KV = lambda *a, **k: add('kiloview.json', 'kiloview-', 'Kiloview', *a, **k)
KV('rf02', 'RF02', 'Cradle Series RF02 2RU media platform (18 card slots)', 'Cradle', 'converter', 2,
   [R('io', 'Other', 'Card slot', 18, 'Card slot'), R('io', 'SFP', 'SFP+', 3, '10G SFP+'), R('io', 'Ethernet', 'RJ45', 1, '10G'),
    R('io', 'Ethernet', 'RJ45', 2, '5G'), R('in', 'Power', 'IEC', 2, 'AC In')],
   '2RU, 483 x 487 x 88 mm, rear plug-in cards: FN-60 HDMI 2.0 and FN-50 12G-SDI encoders, decoders, FMG-400 gateway, FMV-400/FD-400 '
   'multiview, NDI converters. Built-in 240 Gb/s switch, 18 x 1/2.5G links to the slots, dual redundant 500 W PSUs (optional). '
   'Front 3 in LCD. Add each card\'s connectors as extra ports. Check: front/rear placement of the network ports.',
   'Kiloview Cradle Series RF02 datasheet', 'https://kiloview.com/en/wp-content/uploads/2024/09/CRADLE-SERIES-RF02.pdf', full=True)
KV('ru01', 'RU01', 'RU01 1RU rack frame for 4 encoders (redundant power)', 'Rack frames', 'shelf', 1,
   [F('io', 'Other', 'Card slot', 4, 'Encoder bay'), R('in', 'Power', 'DC', 2, 'PSU')],
   '1RU, 483 x 150 x 44 mm. Holds 4 Kiloview FULL NDI encoders/decoders (all except U40) with 2 x 35 W supplies for redundancy. '
   'Add each unit as its own device with its ports. Check: power inlet type.', 'Kiloview RU01 dealer listing',
   'https://videoguys.com/products/kiloview-ru01-1ru-4ch-redundant-power-rackmount-frame', verified=False)

# ---------------- TASCAM ----------------
TA = lambda *a, **k: add('tascam.json', 'tascam-', 'TASCAM', *a, **k)
TA('ss-r250n', 'SS-R250N', 'SS-R250N networked solid-state audio recorder', 'SS-R', 'recorder', 1,
   [R('in', AA, 'XLR3F', 2, 'Balanced In'), R('out', AA, 'XLR3M', 2, 'Balanced Out'), R('in', AA, 'RCA', 2, 'Unbal In'),
    R('out', AA, 'RCA', 2, 'Unbal Out'), R('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), R('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
    R('in', 'AES/EBU', 'RCA', 1, 'S/PDIF In'), R('out', 'AES/EBU', 'RCA', 1, 'S/PDIF Out'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
    R('io', 'Other', 'DB9', 1, 'RS-232C'), R('io', 'Other', 'DB25', 1, 'Parallel'), F('out', AA, '6.3mm TRS', 1, 'Headphones'),
    F('io', 'USB', 'USB-A', 1, 'USB'), F('in', AA, 'XLR3F', 1, 'Front Mic'), F('in', 'Other', '2.5mm TRS', 1, 'Remote'),
    R('io', 'Other', 'Card slot', 1, 'Option slot (IF-DA2 Dante)'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU, 482.6 x 45 x 300.5 mm, 2.9 kg. Stereo SD/CF/USB recorder with FTP, parallel and RS-232C control, optional IF-DA2 Dante card. '
   'Check: connector counts and faces (spec sheet lists types only; one each per stereo pair assumed) and the front mic input.',
   'TASCAM SS-R250N spec sheet', 'https://tascam.com/us/product/ss-r250n', verified=False)
for pn, dp in [('DA-6400', False), ('DA-6400dp', True)]:
    TA(pn.lower(), pn, f'{pn} 64-track recorder' + (' (dual PSU)' if dp else ''), 'DA-6400', 'recorder', 1,
       [R('io', 'Other', 'Card slot', 2, 'Option slot (MADI/Dante/AES/Analog)'), R('in', 'Reference', 'BNC', 1, 'Word/Video In'),
        R('out', 'Reference', 'BNC', 1, 'Word Thru/Out'), R('in', 'Timecode', 'BNC', 1, 'TC In'), R('out', 'Timecode', 'BNC', 1, 'TC Out'),
        R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'DB9F', 1, 'RS-422'), R('io', 'Other', 'DB15F', 1, 'Parallel'),
        R('io', 'USB', 'USB-A', 1, 'USB (control)'), F('out', AA, '6.3mm TRS', 1, 'Phones'), F('io', 'Other', 'Caddy', 1, 'AK-CC25 SSD caddy'),
        R('in', 'Power', 'IEC', 2 if dp else 1, 'AC In')],
       '1RU, 482.6 x 44.9 x 300.5 mm, ' + ('4.0' if dp else '3.9') + ' kg. 64 tracks to a hot-swap SSD caddy. Two option slots: IF-DA64 Dante '
       '(2 x RJ45), IF-MA64/EX MADI (BNC in/out/thru + optical), IF-MA64/BN MADI coax, IF-AE16 AES (2 x DB25), IF-AN16/OUT analog (2 x DB25). '
       'Add the fitted cards\' connectors as extra ports.' + (' Dual redundant PSUs.' if dp else '') + ' Check: AC inlet count on the dp.',
       'TASCAM DA-6400/DA-6400dp data sheet', 'https://tascam.com/us/product/da-6400')

# ---------------- Panasonic ----------------
add('panasonic.json', 'pana-', 'Panasonic', 'av-uhs500', 'AV-UHS500', 'AV-UHS500 4K live switcher main unit', 'Live switchers', 'switcher', 4,
    [R('in', '12G-SDI', 'BNC', 8, 'SDI In'), R('out', '12G-SDI', 'BNC', 5, 'SDI Out'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'),
     R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('io', 'Reference', 'BNC', 2, 'Ref (loop)'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'),
     R('io', 'Other', 'D-sub', 1, 'Tally/GPI (8 in, 19 out)'), R('out', 'Other', 'Other', 1, 'Alarm'),
     R('io', 'Other', 'Card slot', 2, 'Option slot'), R('in', 'Power', 'IEC', 1, 'AC In')],
    '440 x 170 x 360 mm (4RU), 7 kg, AC 100-240 V. 8 x 12G-SDI in (1/2 shared with HDMI 1/2), 5 SDI out, 2 HDMI in/out. '
    'Options: AV-UHS5M1G 4 SDI in, M2G 4 SDI out, M3G 3 HDMI in, M4G 3 HDMI out, M6G NDI (2 LAN). Control panel AV-UHS500 control '
    'unit is separate. Check: option slot count, tally connector type.', 'Panasonic AV-UHS500 specifications',
    'https://pro-av.panasonic.net/en/products/av-uhs500/spec.html', verified=False)

# ---------------- Roland ----------------
for n in (2, 3, 4):
    add('roland.json', 'roland-', 'Roland', f'xs-8{n}h', f'XS-8{n}H', f'XS-8{n}H 8 x {n} multi-format AV matrix switcher', 'XS', 'router', 2,
        [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('in', 'Other', 'HD-15', 8, 'RGB/Component In'), R('in', AA, 'Terminal block', 8, 'Audio In'),
         R('out', 'HDMI', 'HDMI', n, 'HDMI Out'), R('out', 'Other', 'RJ45', n, 'HDBaseT Out'), R('out', AA, 'Terminal block', n, 'Audio Out'),
         R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('io', 'Other', 'DB9', 1, 'RS-232C'), R('io', 'USB', 'USB-A', 2, 'USB'),
         R('in', 'Power', 'IEC', 1, 'AC In')],
        f'2RU (EIA), 481 x 88 x 353 mm. 8 HDMI + 8 analog RGB/component inputs, {n} HDMI outputs mirrored on {n} HDBaseT, '
        'audio mixer with 8 balanced inputs on 5-pin terminal blocks.', 'Roland XS Series spec sheet', 'https://proav.roland.com/global/products/xs-84h/')

# ---------------- Lynx Technik ----------------
add('lynx.json', 'lynx-', 'Lynx Technik', 'rfr-1000', 'RFR 1000', 'yellobrik RFR 1000 1RU rack frame (14 modules)', 'yellobrik', 'shelf', 1,
    [F('io', 'Other', 'Card slot', 14, 'yellobrik bay'), R('in', 'Power', 'Molex Mini-Fit', 2, '12V DC (primary/redundant)'),
     R('out', 'Other', 'Other', 2, 'PSU fail GPO')],
    '1RU, 145 mm deep. Holds up to 14 yellobriks; two 12 V DC inputs (RPS 1000 12 V 8 A supplies, one or two). Add each yellobrik as its own '
    'device with its ports.', 'Lynx Technik RFR 1000 specification sheet', 'https://lynx-technik.com/p/rfr-1000/')
add('lynx.json', 'lynx-', 'Lynx Technik', 'rfr-6000', 'RFR 6000', 'greenMachine RFR 6000 1RU rack frame (2 units)', 'greenMachine', 'shelf', 1,
    [F('io', 'Other', 'Card slot', 2, 'greenMachine bay'), R('in', 'Power', '12V DC', 2, 'RPS A100 PSU'), R('out', 'Other', 'Other', 1, 'PSU fail GPI')],
    '1RU frame for 1 or 2 greenMachine units, two RPS A100 supplies (sold separately) for redundancy. Add each greenMachine as its own device.',
    'Lynx Technik RFR 6000 page', 'https://lynx-technik.com/p/rfr-6000/')

# ---------------- Lumens ----------------
add('lumens.json', 'lumens-', 'Lumens', 'lc200', 'LC200', 'LC200 CaptureVision media processor (switch/record/stream)', 'CaptureVision', 'switcher', 1,
    [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out (PGM/MV)'), R('in', AA, '3.5mm', 4, 'Line/Mic In'),
     R('out', AA, '3.5mm', 1, 'Line Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (3 IP sources)'), F('io', 'USB', 'USB-A', 1, 'USB 3.0'),
     R('io', 'USB', 'USB-A', 2, 'USB 2.0'), R('io', 'Other', 'Other', 1, 'RS-232/RS-485'), R('in', 'Power', '12V DC', 1, 'DC In')],
    '1RU, 431 x 44.3 x 122.5 mm, 12 V 2 A external supply. 4 HDMI + 3 IP (H.264) sources, program and multiview HDMI outputs, '
    'records and streams. Check: serial port connector.', 'Lumens VS-LC200 spec sheet', 'https://www.mylumens.com/en/Products/LC200')

# Brands on the list with no rack-mount product found (desktop, USB, camera-top or HDMI-only boxes):
# A-Neuvideo, AVMATRIX, Cerevo, CNDLive, DVDO, INOGENI, Magewell, Matrox (Monarch EDGE/ConvertIP), MiNE Media, Miri, MR-NET, OREI,
# Raywowo, RGBlink, RODE (RODE X), SalrayWorks, SCIENCE IMAGE, Sprolink, Vaddio, VigilLink, Videon (LiveEdge Max form factor unknown),
# Broadcast Pix (rack height unknown), Mackie. Blackmagic, Sony and Vizrt are already catalogued.

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(idx)
