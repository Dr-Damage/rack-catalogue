#!/usr/bin/env python3
"""Multiviewers, processing, probes and tally (added 2026-11-14):
  catalogue/imagine.json      Imagine Communications Selenio Network Processor (SNP) and Platinum IP3 router frames.
  catalogue/cobalt.json       Cobalt Digital openGear cards (multiviewers, converters, DAs, routers, encoders) and WAVE routers.
                              The 9904-UDX-4K and 9902-2UDX stay in frames-opengear.json.
  catalogue/apantac.json      Apantac multiviewers.
  catalogue/tsl.json          TSL Products PAM audio monitors and TallyMan tally controllers.
  catalogue/bridgetech.json   Bridge Technologies VB330 and VB440 probes.
Riedel MediorNet MicroN / HorizoN / MetroN are already in riedel.json; Embrionix (now Riedel) makes SFP modules only.
Specs from the makers' data sheets and the openGear.tv card pages (each entry's source). 'Check:' marks anything unconfirmed."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m)
def PSU(n=2, conn='IEC C14'): return R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')

# ======================= Imagine Communications =======================
IM = 'Imagine Communications'
add('imagine.json', 'imagine-snp', IM, 'SNP-PLATFORM-4A', 'Selenio Network Processor (SNP), 4 processors', 'Selenio SNP', 'converter', 1,
    [R('io', '12G-SDI', 'HD-BNC', 8, 'SDI 12G'), R('io', '3G-SDI', 'HD-BNC', 24, 'SDI'), R('io', 'SFP', 'QSFP28', 2, '100GbE'),
     R('io', 'SFP', 'SFP+', 4, 'Expansion SFP'), R('io', 'Ethernet', 'RJ45', 2, 'Mgmt'), PSU()],
    '1RU software-defined processor: 4 personalities (ST 2110 / 2022-6 gateway, up/down/cross, frame sync, multiviewer, JPEG XS) '
    'on 4 application processors (SNP-PLATFORM-2AU has 2, upgradable). 32 bidirectional HD-BNC SDI ports (8 are 12G), 2 x QSFP28 '
    '(100GbE), quad SFP+ cage for MADI, 3G coax or optical. Under 350 W, 594 mm deep, 7.5 kg. Check: which panel carries the '
    'management ports.', 'Imagine SNP data sheet', 'https://imaginecommunications.com/product/selenio-network-processor-snp/',
    full=True, powerW=350, weightKg=7.5)
for ru, size, slots, psu in ((15, '288 x 512', 32, 2), (28, '576 x 1024', 64, 4)):
    add('imagine.json', f'imagine-platinum-ip3-{ru}ru', IM, f'Platinum IP3 {ru}RU', f'Platinum IP3 {ru}RU router frame, up to {size}',
        'Platinum IP3', 'router', ru,
        [R('in', 'Reference', 'BNC', 2, 'Ref In'), R('io', 'Ethernet', 'RJ45', 2, 'Control (PX-RES)'), PSU(psu, 'IEC C20')],
        f'{ru}RU hybrid SDI/IP router frame with {slots} input and {slots} output card slots, up to {size} in one frame. '
        f'Takes Platinum SX Pro multiviewer cards (1 to 4 slots) and IP gateway cards. Magellan control via the PX-RES resource module. '
        f'{psu} x 1500 W PX-PS supplies standard. I/O sits on the cards, so add the signals as you wire it. '
        'Check: rear reference, control and power connectors.', 'Imagine Platinum IP3 data sheet',
        'https://imaginecommunications.com/insights-and-resources/platinum-ip3-router', verified=False, full=True)

# ======================= Cobalt Digital (openGear cards) =======================
CB = 'Cobalt Digital'
def rm(pn, name, width, ports, default=False, notes=None, offset=0):
    d = dict(partNumber=pn, name=name, width=width, cardsPerModule=1, cardOffset=offset, default=default, portGroups=ports, included=False)
    if notes: d['notes'] = notes
    return d
def card(id, pn, name, rms, notes, url, verified=True, watts=None, src=None):
    m = dict(id='cobalt-' + id, manufacturer=CB, partNumber=pn, name=name, family='Cobalt openGear', category='card', ru=0, widthCols=0,
             fullDepth=False, verified=verified, source=src or f'openGear.tv / Cobalt {pn} page', productUrl=url, notes=notes,
             portGroups=[], card=dict(fits=['openGear'], slotWidth=1), rearModules=rms)
    if watts: m['powerW'] = watts
    FILES.setdefault('cobalt.json', []).append(m)
SDI = lambda d, t, n, p: R(d, t, 'HD-BNC', n, p)
GPIO = R('io', 'GPIO', 'RJ45', 1, 'GPIO/COMM'); ETH = R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')
card('9905-mpx', '9905-MPx', '9905-MPx 3G/HD/SD quad-path up/down/cross converter, frame sync',
     [rm('RM20-9905-D-HDBNC', 'Standard width', 2, [SDI('in', '3G-SDI', 5, 'SDI In'), SDI('out', '3G-SDI', 6, 'SDI Out'),
         R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), R('in', 'MADI audio', 'HD-BNC', 1, 'MADI In'), GPIO, ETH], True,
         'Occupies the adjacent odd slot; not in slots 19/20.'),
      rm('RM20-9905-G-HDBNC', 'Standard width with SFP', 2, [SDI('in', '3G-SDI', 4, 'SDI In'), SDI('out', '3G-SDI', 4, 'SDI Out'),
         R('io', 'AES/EBU', 'HD-BNC', 3, 'AES I/O'), R('io', 'SFP', 'SFP', 2, 'SFP'), GPIO], offset=0),
      rm('RM20-9905-B-HDBNC', 'Double width', 4, [SDI('in', '3G-SDI', 5, 'SDI In'), SDI('out', '3G-SDI', 8, 'SDI Out'),
         R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), R('in', 'MADI audio', 'HD-BNC', 1, 'MADI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), GPIO, ETH],
         offset=1),
      rm('RM20-9905-F-HDBNC', 'Double width, full I/O', 4, [SDI('in', '3G-SDI', 5, 'SDI In'), SDI('out', '3G-SDI', 8, 'SDI Out'),
         R('io', 'AES/EBU', 'HD-BNC', 8, 'AES I/O'), R('in', 'MADI audio', 'HD-BNC', 1, 'MADI In'), R('out', 'MADI audio', 'HD-BNC', 1, 'MADI Out'),
         R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'SFP', 'SFP', 2, 'SFP'), GPIO, ETH], offset=1)],
     'Four independent up/down/cross, frame sync and audio embed/de-embed paths with AES and MADI routing. INDIGO 2110-DC-01 '
     'daughtercard adds dual 25G ST 2110. Rear modules C, H and J also exist.', 'https://opengear.tv/card/9905-mpx/')
card('9970-qs', '9970-QS', '9970-QS quint-split multiviewer (5 x 3G/HD/SD/CVBS in)',
     [rm('RM20-9970-B', 'Standard width', 2, [R('in', '3G-SDI', 'BNC', 5, 'SDI/CVBS In'), R('out', '3G-SDI', 'BNC', 2, 'MV Out'),
         R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', 'GPI', 'RJ45', 1, 'GPI/Tally'), ETH], True)],
     'Five auto-detecting SDI or composite inputs, 2 SDI and 1 HDMI multiviewer outputs, 16-channel embedded audio meters, '
     'tally by GPI, Ethernet or serial. Under 18 W. 9970-QS-MC is the multicast version. Check: rear module connectors and width.',
     'https://www.markertek.com/product/cb-9970-qs/cobalt-digital-9970-qs-3g-hd-sd-sdi-cvbs-quint-split-multi-image-display-processor-opengear-card',
     verified=False, watts=18, src='Markertek 9970-QS listing')
BR = ('Cobalt Digital 2024 product brief', 'https://www.cobaltdigital.com/')
def bcard(id, pn, name, ports, notes, wide=False):
    card(id, pn, name, [rm('RM20-' + pn.split('-')[0] + ('-B' if wide else '-A'), 'Double width' if wide else 'Standard width', 4 if wide else 2,
                           ports, True, offset=1 if wide else 0)],
         notes + ' Check: rear module part number and connector counts (from the product brief).', BR[1], verified=False, src=BR[0])
bcard('9971-mv18-4k', '9971-MV18-4K', '9971-MV18-4K 18-input 4K multiviewer',
      [SDI('in', '3G-SDI', 18, 'SDI In'), SDI('out', '12G-SDI', 4, 'MV Out'), GPIO, ETH], '18 SDI inputs, 4 SDI outputs (UHD or quad HD).', wide=True)
bcard('9971-mv6-4k', '9971-MV6-4K', '9971-MV6-4K 6-input 4K multiviewer',
      [SDI('in', '3G-SDI', 6, 'SDI In'), SDI('out', '12G-SDI', 4, 'MV Out'), GPIO, ETH], '6 SDI inputs, 4 SDI outputs. -4H version adds HDMI 2.0 out.')
bcard('9915da-4x16-xpt-12g', '9915DA-4X16-XPT-12G', '9915DA-4x16-XPT-12G quad 12G reclocking DA with crosspoint',
      [SDI('in', '12G-SDI', 4, 'SDI In'), SDI('out', '12G-SDI', 16, 'SDI Out'), ETH], 'Four inputs to 16 outputs through a x4 output crosspoint. Optional fibre I/O. '
      '2x16 and 1x16 versions also made.')
bcard('9942-rtr-12x12-12g', '9942-RTR-12X12-12G', '9942-RTR-12X12-12G WAVE 12 x 12 12G router card',
      [SDI('in', '12G-SDI', 12, 'Router In'), SDI('out', '12G-SDI', 12, 'Router Out'), ETH], 'Passes 12G/3G/HD/SD-SDI, ASI and MADI. 24 x 24 version also made.', wide=True)
bcard('og-2110-bidi4-gateway', 'OG-2110-BIDI4-GATEWAY', 'INDIGO OG-2110-BIDI4-GATEWAY 4-channel ST 2110 / SDI gateway',
      [SDI('io', '3G-SDI', 4, 'SDI I/O'), R('io', 'SFP', 'SFP28', 2, '25GbE'), ETH], 'Bidirectional, four channels, dual 25G (ST 2022-7).')
bcard('og-aud4-dante', 'OG-AUD4-DANTE', 'ARIA OG-AUD4-DANTE 4-channel audio embedder/de-embedder with Dante',
      [SDI('in', '12G-SDI', 4, 'SDI In'), SDI('out', '12G-SDI', 4, 'SDI Out'), R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec'),
       R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), R('io', 'MADI audio', 'HD-BNC', 1, 'MADI')], 'Four SDI paths with frame sync, Dante, AES and MADI. OG-AUD2-DANTE has two.', wide=True)
bcard('9926-4htos', '9926-4HtoS', 'SAPPHIRE 9926-4HtoS quad HDMI to 3G-SDI converter',
      [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), SDI('out', '3G-SDI', 4, 'SDI Out'), ETH], 'Four channels with frame sync. 9926-2HtoS is the dual 12G version.', wide=True)
bcard('9992-enc', '9992-ENC', 'PACIFIC 9992-ENC HEVC/AVC broadcast encoder',
      [SDI('in', '12G-SDI', 4, 'SDI In'), R('out', 'Other', 'BNC', 2, 'ASI Out'), R('io', 'Ethernet', 'RJ45', 2, 'TS over IP'), ETH],
      'Up to 4Kp60 or four HD channels, HEVC/AVC/MPEG-2, IP and ASI outputs. 9992-DEC is the matching decoder.')
for ru, n in ((4, 32), (4, 64)):
    add('cobalt.json', f'cobalt-wave-rtr-{n}x{n}', CB, f'WAVE RTR-{n}x{n}', f'WAVE RTR-{n}x{n} 12G-SDI router', 'WAVE', 'router', ru,
        [R('in', '12G-SDI', 'BNC', n, 'In'), R('out', '12G-SDI', 'BNC', n, 'Out'), R('in', 'Reference', 'BNC', 1, 'Ref'),
         R('io', 'Ethernet', 'RJ45', 1, 'Control'), PSU()],
        f'{n} x {n} 12G/3G/HD/SD-SDI router, 4U. WAVE CP-84L / CP-42L / CP-78 / CP-44 control panels over Ethernet (PoE++). '
        'Check: connector type (BNC or HD-BNC), reference and power supplies.', BR[0], BR[1], verified=False)

# ======================= Apantac =======================
AP = 'Apantac'
add('apantac.json', 'apantac-mi-16-uhd', AP, 'Mi-16-UHD', 'Mi-16-UHD 16-input UHD multiviewer', 'Mi series', 'converter', 1,
    [R('in', '3G-SDI', 'BNC', 16, 'SDI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('out', '12G-SDI', 'BNC', 1, '12G-SDI Out'),
     R('out', '3G-SDI', 'BNC', 1, '3G-SDI Out'), R('in', 'Timecode', 'BNC', 1, 'LTC In'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
     R('io', 'RS-232', 'RJ45', 1, 'RS-232'), R('in', 'GPI', 'Other', 4, 'GPI (RJ50)'), R('in', 'Power', 'IEC C14', 1, 'AC In'),
     R('in', 'Power', 'DC locking', 1, '12V DC')],
    '1RU, 16 auto-detect 3G/HD/SD-SDI inputs, UHD HDMI 2.0 and 12G-SDI multiviewer outputs, 16 embedded audio channels per input, '
    'audio breakout, TSL / AXP tally, GPI through 4 RJ50-to-DB9 cables. 55 W, 452 mm deep. Optional redundant PSU. '
    'Check: HDMI output count (data sheet says 2 in the table and 1 + 1 in the features) and GPI count.',
    'Apantac Mi-16-UHD data sheet', 'https://www.apantac.com/', verified=False, powerW=55)
add('apantac.json', 'apantac-tahoma-le-4', AP, 'TAHOMA-LE-4', 'TAHOMA-LE-4 4-input multiviewer, half rack', 'Tahoma LE', 'converter', 1,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI/CVBS In'), R('out', 'DVI', 'DVI-I', 1, 'DVI/HDMI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out (option)'),
     R('in', 'Timecode', 'BNC', 1, 'LTC In'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-232', 'RJ45', 1, 'RS-232'),
     R('in', 'GPI', 'DB9', 1, 'GPI'), R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Half-width 1RU quad-split: 4 auto-detect HD/SD-SDI or composite inputs, 1 DVI/HDMI output, optional SDI output, 16 embedded '
    'and optional discrete audio per input, 16 GPI. 25 W, 215 x 370 mm. Check: GPI connector count and DC inlet.',
    'Apantac TAHOMA-LE-4 data sheet (Thameside)', 'https://www.thameside.tv/documents/Tahoma-LE4-Datasheet.pdf', verified=False, w=6, powerW=25)

# ======================= TSL Products =======================
TS = 'TSL Products'
PAMNOTE = ('Check: AES and analogue connector types (shown as D-sub), GPI and USB connectors. ')
def pam(id, pn, name, ru, ports, notes, src, url, d, check=PAMNOTE):
    add('tsl.json', 'tsl-' + id, TS, pn, name, 'PAM', 'audio', ru, ports, notes + f' {d} mm deep. ' + check, src, url, verified=False)
def add_ip(power=None): return [R('io', 'SFP', 'SFP+', 2, 'ST 2110 SFP'), R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec'),
                  R('io', 'Ethernet', 'RJ45', 1, 'Control'), power or R('in', 'Power', 'DC locking', 2, 'PSU A/B')]
# 2RU rear (from the PAM2-IP-3G rear photo): AES I/O and analogue out on D-sub, 2 stereo analogue ins on XLR, 2 analogue outs on XLR, GPIO D9, DC on 4-pin XLR
PAM2_AUDIO = lambda aes: [R('io', 'AES/EBU', 'DB25', 1, f'AES I/O {aes}'), R('out', 'Analog audio', 'DB25', 1, 'Analogue Out 1-8'),
                          R('in', 'Analog audio', 'XLR3F', 4, 'Analogue In (2 stereo)'), R('out', 'Analog audio', 'XLR3M', 2, 'Analogue Out A1/A2'),
                          R('io', 'GPIO', 'DB9', 1, 'GPIO')]
PAM2_PSU = R('in', 'Power', 'XLR4M', 2, 'PSU A/B (DC)')
pam('pam2-12g', 'PAM2-12G', 'PAM2-12G precision audio monitor, 12G-SDI, 2RU', 2,
    [R('in', '12G-SDI', 'BNC', 1, '12G-SDI In'), R('in', '3G-SDI', 'BNC', 3, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, '12G Loop'),
     R('out', '3G-SDI', 'BNC', 2, 'SDI Out')] + PAM2_AUDIO('1-4') + add_ip(PAM2_PSU),
    'Audio monitor with screen and speakers for 12G/3G SDI, AES, analogue, Dante and ST 2110 / 2022-6 (2 x 10G SFP, Embrionix). '
    '4 AES in/out, 2 stereo analogue in, 8 analogue out. External PSU, optional redundant. 4.9 kg. Audio connectors as on the PAM2-IP-3G rear.',
    'TSL PAM2-12G data sheet', 'https://tslproducts.com/product/pam2-12g/', 335, 'Check: SDI BNC count. ')
pam('pam2-ip-3g', 'PAM2-IP-3G', 'PAM2-IP-3G precision audio monitor, IP and 3G-SDI, 2RU', 2,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')] + PAM2_AUDIO('1-8') + add_ip(PAM2_PSU),
    'Audio monitor for ST 2110 / 2022-6 (2 x 10G SFP), Dante/AES67, 3G-SDI, AES and analogue. Options: Dolby decode, Dante. '
    'External PSU, optional redundant (PSU-PAMIP-11A). Rear checked against a photo of the unit.', 'TSL PAM IP range data sheet; rear from a Canford photo',
    'https://tslproducts.com/products/audio-monitoring/pam-range', 250, '')
pam('pam1-ip-3g', 'PAM1-IP-3G', 'PAM1-IP-3G precision audio monitor, IP and 3G-SDI, 1RU', 1,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'AES/EBU', 'DB25', 1, 'AES In 1-8'),
     R('out', 'AES/EBU', 'DB25', 1, 'AES Out 1-8'), R('in', 'Analog audio', 'DB25', 1, 'Analogue In'),
     R('out', 'Analog audio', 'DB25', 1, 'Analogue Out 1-8')] + add_ip(),
    'Audio monitor for ST 2110 / 2022-6 (2 x 10G SFP), Dante/AES67, 3G-SDI, AES and analogue. Options: Dolby decode, Dante. '
    'External PSU, optional redundant (PSU-PAMIP-11A).', 'TSL PAM IP range data sheet', 'https://tslproducts.com/products/audio-monitoring/pam-range', 250)
add('tsl.json', 'tsl-tm1-tally', TS, 'TM1-TALLY', 'TallyMan TM1-TALLY tally controller, 64 GPIO', 'TallyMan', 'control', 1,
    [R('io', 'GPIO', 'DB37', 2, 'GPIO 1-64'), R('io', 'RS-422', 'DB9', 4, 'RS-422'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'),
     R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'TallyMan system controller for tally: 64 configurable GPIO, 4 RS-422, dual Gigabit Ethernet, single PSU, 60 W max. '
    '483 x 233 mm, 2.15 kg. TM1-Mk3+ is the full controller (unlimited devices, dual hot-swap PSU). '
    'Check: GPIO connector type and count (shown as 2 x DB37).', 'TSL TM1-Tally data sheet',
    'https://www.tslproducts.com/products/tsl-control/tallyman-control-system/system-controllers/tm1-tally', verified=False, powerW=60, weightKg=2.15)

# ======================= Bridge Technologies =======================
BT = 'Bridge Technologies'
add('bridgetech.json', 'bridgetech-vb330', BT, 'VB330', 'VB330 10G IP probe, 1RU', 'VB300', 'network', 1,
    [R('in', 'SFP', 'SFP+', 2, '10G Probe A/B'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('io', 'USB', 'USB-A', 1, 'USB'), PSU()],
    'Core/edge network probe for OTT and IPTV monitoring: 2 x 10G SFP+ inputs, Gigabit management, USB for setup. 483 x 400 mm, '
    '150 W max chassis. Also as an embedded blade (EC chassis) and appliance. Check: PSU count and which face has the ports.',
    'Bridge Technologies VB330 data sheet', 'https://bridgetech.tv/', verified=False, powerW=150, weightKg=8.2)
add('bridgetech.json', 'bridgetech-vb440', BT, 'VB440', 'VB440 ST 2110 / 2022 studio probe, 1RU appliance', 'VB400', 'network', 1,
    [R('in', 'SFP', 'QSFP28', 2, '100G A/B'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('io', 'USB', 'USB-A', 1, 'USB'), PSU()],
    'Real-time ST 2110 / 2022-6 / JPEG XS analytics with waveform, vectorscope and multiviewer in a browser. Dual 10/25/40/50/100G '
    'NIC, dual PSU, about 500 mm deep, 15 kg. Check: NIC cage type and count.', 'Bridge Technologies VB440 / VB330 appliance specs',
    'https://bridgetech.tv/', verified=False, full=True, weightKg=15)

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
