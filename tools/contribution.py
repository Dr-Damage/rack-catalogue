#!/usr/bin/env python3
"""Contribution, encoding and carrier edge gear (added 2026-11-14). Files:
  tvu.json            TVU Transceiver VS3500/3550/3600/3650 (the generic 'tvu-transceiver' stays built into the app).
  appear.json         Appear X10 / X20 frames and their rear modules as cards (system 'Appear X').
  nevion.json         Nevion (Sony) Virtuoso MI / RE / FA media nodes and accelerator cards (system 'Nevion Virtuoso').
  netinsight.json     Net Insight Nimbra 414 / 424.
  sencore.json        Sencore MRD 7000 receiver decoder.
  ateme.json          Ateme Kyrion CM5000 encoder and DR8400 IRD.
  vislink.json        Vislink Quantum receiver and UltraReceiver LD (Mobile Viewpoint is part of Vislink).
  kiloview-more.json  Kiloview RU03 chassis, CUBE R1 recorder, CUBE X1 NDI distribution.
  haivision-more.json Haivision Makito One F4 / F18 frames and the dual 12G blade (system 'Haivision Makito One').
  matrox.json         Matrox Monarch EDGE E4 (half width).
  telstra.json        Telstra DVN carrier edge placeholders (Telstra does not publish the models it installs).
  foxtel.json         Foxtel iQ set-top boxes for off-air monitoring, as shelf items (sizes estimated, not published).
LiveU and Dejero rack receivers were already in (liveu.json, dejero.json); Zixi sells software only; Videon and Magewell make
desktop boxes only. Specs from maker data sheets (each entry's source); 'Check:' marks what is not confirmed."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
BOX = {'x0': 0.04, 'x1': 0.96, 'y0': 0.08, 'y1': 0.92}
def frame(file, id, mfr, pn, name, fam, ru, fr, ports, notes, src, url, verified=True, **kw):
    fr = dict(dict(slotOrder='ltr', rearAlign=1, door=False, front=BOX, rear=BOX), **fr)
    add(file, id, mfr, pn, name, fam, 'frame', ru, ports, notes, src, url, verified, frame=fr, **kw)
def card(file, id, mfr, pn, name, fam, fits, rear, notes, src, url, verified=True, front=None, color=None, **kw):
    c = dict(fits=fits, slotWidth=1)
    if color: c['color'] = color
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category='card', ru=0, widthCols=0, fullDepth=False,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=front or [], card=c,
             rearModules=[dict(partNumber=pn, name='Rear I/O', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=rear)])
    m.update(kw); FILES.setdefault(file, []).append(m)
SDI = 'SDI'
AC1 = R('in', 'Power', 'IEC C14', 1, 'AC In'); AC2 = R('in', 'Power', 'IEC C14', 2, 'PSU')

# ---------------- TVU ----------------
TVU_SRC, TVU_URL = 'TVU Transceiver data sheet (June 2023)', 'https://www.tvunetworks.com/products/receivers/'
for pn, sdi, psu, ch in (('VS3500', '3G', 1, 'up to 4 HD receive channels'), ('VS3550', '3G', 2, 'up to 4 HD receive channels'),
                         ('VS3600', '12G', 1, '1 x 4K60 receive channel'), ('VS3650', '12G', 2, '1 x 4K60 receive channel')):
    add('tvu.json', 'tvu-' + pn.lower(), 'TVU Networks', pn, f'TVU Transceiver {pn} 1RU receiver ({sdi}-SDI, {"dual" if psu > 1 else "single"} PSU)',
        'Transceiver', 'converter', 1,
        [R('io', SDI, 'BNC', 4, f'{sdi}-SDI'), R('in', 'Reference', 'BNC', 1, 'Genlock'), R('out', 'HDMI', 'HDMI', 1, 'HDMI monitor'),
         R('io', 'Ethernet', 'RJ45', 1, 'GbE'), R('io', 'Ethernet', 'RJ45', 1, '2.5GbE'), R('io', 'USB', 'USB-A', 7, 'USB 3.2'),
         R('io', 'USB', 'USB-C', 1, 'USB-C'), R('in', 'Power', 'IEC C14', psu, 'PSU' if psu > 1 else 'AC In')],
        f'1RU receiver for TVU transmitters: {ch} (or receive plus Grid / RVF encode). 4 x {sdi}-SDI BNC, genlock (tri-level or black burst), '
        'HDMI monitor out, 1 GbE + 1 x 2.5 GbE, 8 x USB (external USB audio I/O). 395 mm deep. '
        'Check: SDI direction per channel and which ports are on the front.', TVU_SRC, TVU_URL, verified=False)

# ---------------- Appear X platform ----------------
AP_SRC, AP_URL = 'Appear X10/X20 technical specifications (v2.9.2)', 'https://www.appear.net/products/x-platform/'
for pn, ru, slots, cols, pw, notes in (('X10', 1, 8, 4, 750, '750 W. One fan tray with 6 fans.'),
                                       ('X20', 2, 12, 4, 1500, 'Two hot-swap redundant PSUs (800-1500 W AC, -48 V DC option). Hot-swap fan tray.')):
    frame('appear.json', 'appear-' + pn.lower(), 'Appear', pn, f'{pn} media platform chassis, {slots} module slots', 'X platform', ru,
          dict(system='Appear X', slots=slots, orient='h', cols=cols, controller='One or two front switch modules (active-active).'),
          [F('io', 'Ethernet', 'RJ45', 1, 'Control (switch module)'), AC2],
          f'{ru}RU chassis, {slots} rear module slots plus one or two front-loaded switch / control modules. 540 mm deep. {notes} '
          'Front-to-back airflow. Check: slot layout (shown as rows of 4).', AP_SRC, AP_URL, verified=False, powerW=pw)
for pn, name, rear, note in (
        ('IPx100', 'dual 10G IP interface', [R('io', 'Ethernet', 'SFP+', 2, '1/10G')], 'IP gateway, TS / SRT / Zixi. Ordered as SFP/SFP+ or 10GBASE-T.'),
        ('IPx210', 'uncompressed IP interface (ST 2110)', [R('io', 'Ethernet', 'QSFP28', 2, '40/100G')], '40G QSFP, 4 x 10G breakout, or 10G / 25G by adapter.'),
        ('SIx110', 'SDI / ASI I/O, 8 ports', [R('io', SDI, 'HD-BNC', 8, 'SDI/ASI')], '75 ohm HD-BNC, direction set per port.'),
        ('SIx120', 'ASI I/O, 16 ports (JPEG XS capable SDI version)', [R('io', SDI, 'HD-BNC', 16, 'ASI')], ''),
        ('SIx200', 'SDI I/O on video SFPs', [R('io', SDI, 'SFP', 3, 'Video SFP')], 'Non-MSA dual Rx / Tx video SFPs.'),
        ('ECx110', 'HEVC / AVC codec (encode, transcode, decode)', [], 'Processing module, no rear signal connectors.'),
        ('SR-100', 'DVB-S/S2X satellite receiver', [R('in', 'RF', 'F', 4, 'L-band In')], ''),
        ('SMx100', 'DVB-S/S2X modulator', [R('out', 'RF', 'SMA', 2, 'RF Out'), R('out', 'RF', 'SMA', 2, 'Monitor')], 'Two carriers.')):
    card('appear.json', 'appear-' + pn.lower(), 'Appear', pn, f'{pn} {name}', 'X platform modules', ['Appear X'], rear,
         f'X10 / X20 rear module. {note} Check: part suffix and exact connectors for your order.'.replace('  ', ' '), AP_SRC, AP_URL, verified=False)

# ---------------- Nevion Virtuoso ----------------
NV_SRC, NV_URL = 'Nevion Virtuoso platform data sheet (R2336)', 'https://nevion.com/products/virtuoso/'
for pn, slots, cols, d, kg, pw, ports, note in (
        ('MI', 8, 4, 582, 11.2, 500, [F('io', 'Ethernet', 'RJ45', 2, 'Controller'), F('in', 'Reference', 'BNC', 1, 'Sync In'),
                                      F('out', 'Reference', 'BNC', 1, 'Sync loop')], 'Carrier-grade modular node, redundant controllers, PSUs hot-swap from the front.'),
        ('RE', 6, 3, 425, 7.6, 370, [F('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), F('in', 'Reference', 'BNC', 1, 'Sync In')], 'Compact short-depth node.'),
        ('FA', 4, 4, 443, 6.9, 330, [R('io', 'Ethernet', 'RJ45', 2, 'Mgmt'), R('io', 'Ethernet', 'SFP+', 2, '1/10GE'), R('io', SDI, 'BNC', 4, 'ASI'),
                                     R('in', 'Reference', 'BNC', 1, 'Sync In'), R('in', 'Reference', 'BNC', 1, '1PPS'), R('io', 'Other', 'DB9', 1, 'Alarm relay')],
         'Appliance with a built-in 10GE TS-over-IP uplink and 4 ASI.')):
    frame('nevion.json', 'nevion-virtuoso-' + pn.lower(), 'Nevion (Sony)', f'Virtuoso {pn}', f'Virtuoso {pn} media node, {slots} accelerator slots', 'Virtuoso', 1,
          dict(system='Nevion Virtuoso', slots=slots, orient='h', cols=cols, controller='Built in.'), ports + [AC2],
          f'1RU, {note} Dual load-sharing AC PSUs. {pw} W max (accelerators up to 50 W each), {d} mm deep, {kg} kg. '
          'Used for IP media transport and contribution networks (JPEG XS / JPEG 2000 / H.264 / 2110). Check: slot layout.', NV_SRC, NV_URL,
          verified=False, powerW=pw, weightKg=kg)
for pn, name, rear in (('HBR-SFP4', 'HBR media accelerator, 4 x SFP+', [R('io', 'SFP', 'SFP+', 4, 'SFP+ (10GE / SDI / ASI / MADI)')]),
                       ('HBR25-SFP3', 'HBR25 media accelerator, 2 x SFP28 + 1 x SFP+', [R('io', 'Ethernet', 'SFP28', 2, '25GE'), R('io', SDI, 'SFP+', 1, 'Video SFP')]),
                       ('H264-X1', 'H.264 / AVC accelerator', [R('io', SDI, 'BNC', 3, 'SDI/ASI'), R('io', 'Reference', 'BNC', 1, 'Sync / ASI out')]),
                       ('ASI-X4', 'ASI adapter, 4 ports', [R('io', SDI, 'BNC', 4, 'ASI')]),
                       ('AES3', 'AES3 digital audio adapter, 16 ports', [R('io', 'Audio', 'DB37', 1, 'AES3 x16')]),
                       ('RPRO', 'RPRO audio adapter (analog, AES, GPIO)', [R('io', 'Audio', 'DB37', 1, 'Audio / GPIO')])):
    card('nevion.json', 'nevion-' + pn.lower(), 'Nevion (Sony)', pn, f'Virtuoso {name}', 'Virtuoso accelerators', ['Nevion Virtuoso'], rear,
         'Virtuoso accelerator card. ' + ('Breakout panels give 16 BNC or 8 in / 8 out XLR. ' if pn in ('AES3', 'RPRO') else ''), NV_SRC, NV_URL)

# ---------------- Net Insight ----------------
NI_SRC, NI_URL = 'Net Insight Nimbra 400 data sheet v2', 'https://netinsight.net/nimbra-400/'
for pn, note in (('Nimbra 414', '4 x HD and 1 x 4K MPEG-4 / HEVC 4:2:0 encode and decode.'), ('Nimbra 424', 'As the 414 with 4:2:2 profiles.')):
    add('netinsight.json', 'netinsight-' + pn.lower().replace(' ', '-'), 'Net Insight', pn, f'{pn} video contribution encoder / decoder', 'Nimbra 400', 'converter', 1,
        [R('io', SDI, 'HD-BNC', 4, 'SDI/ASI (3 x 3G, 1 x 12G)'), R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 2, '10GbE'),
         R('io', 'Ethernet', 'RJ45', 2, '2.5GbE'), AC2],
        f'{note} Single or dual hot-swap 750/800 W PSUs. 429 mm deep, 8.2 kg. Check: front / rear split.', NI_SRC, NI_URL, verified=False, weightKg=8.2)

# ---------------- Sencore ----------------
add('sencore.json', 'sencore-mrd-7000', 'Sencore', 'MRD 7000', 'MRD 7000 multichannel receiver decoder', 'MRD', 'converter', 1,
    [R('in', SDI, 'BNC', 1, 'ASI In'), R('out', SDI, 'HD-BNC', 1, '12G-SDI Out'), R('io', SDI, 'HD-BNC', 4, '3G-SDI / ASI'),
     R('io', 'Ethernet', 'RJ45', 2, 'IP (MRD 70020)'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('io', 'Ethernet', 'SFP28', 2, '25G ST 2110 (option MRD 70180)'),
     R('in', 'RF', 'F', 4, 'DVB-S/S2X (option MRD 70191)'), AC1],
    'Decodes up to 4 HD or 1 UHD (HEVC, H.264, MPEG-2) from satellite, IP (SRT, Zixi, RIST, RTMP, HLS) or ASI. Outputs 12G-SDI, 4 x 3G-SDI '
    '(genlocked), or ST 2110. Option cards and connectors depend on the order. Check: power inlets (single or dual).',
    'Sencore MRD 7000 data sheet (v10, 2024-02)', 'https://www.sencore.com/product/mrd-7000-multichannel-multiformat-receiver-decoder/', verified=False)

# ---------------- Ateme ----------------
AT_URL = 'https://www.ateme.com/'
add('ateme.json', 'ateme-kyrion-cm5000', 'Ateme', 'Kyrion CM5000', 'Kyrion CM5000 contribution encoder', 'Kyrion', 'converter', 1,
    [R('in', SDI, 'BNC', 1, 'SDI In'), R('out', SDI, 'BNC', 2, 'ASI Out'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('io', 'Ethernet', 'RJ45', 2, 'GbE stream'), AC1],
    'H.264 / HEVC 4:2:2 10-bit contribution encoder. SD / HD / 3G-SDI in with up to 16 embedded audio channels; optional AES board '
    '(16 channels) and analog board (8 channels); optional L-band / IF modulator outputs. 6.4-7.3 kg. Check: SDI input count and PSUs.',
    'Ateme Kyrion CM5000 data sheet (DirectIndustry)', AT_URL, verified=False)
add('ateme.json', 'ateme-kyrion-dr8400', 'Ateme', 'Kyrion DR8400', 'Kyrion DR8400 integrated receiver decoder', 'Kyrion', 'converter', 1,
    [R('in', 'RF', 'F', 1, 'DVB-S/S2 In'), R('in', SDI, 'BNC', 2, 'ASI In'), R('io', 'Ethernet', 'RJ45', 1, 'IP In'), R('out', SDI, 'BNC', 1, 'SDI Out'),
     R('out', 'Audio', 'XLR3 male', 4, 'AES Out'), AC1],
    'Multi-format IRD: built-in DVB-S/S2 demodulator, IP and dual ASI inputs (redundancy), TS up to 200 Mbps. SDI with embedded audio or up '
    'to 4 AES outputs. 130 W, 7.5 kg. Check: SDI output count, RF input count and management port.', 'Ateme Kyrion DR8400 data sheet (DirectIndustry)',
    AT_URL, verified=False, powerW=130, weightKg=7.5)

# ---------------- Vislink ----------------
add('vislink.json', 'vislink-quantum-receiver', 'Vislink', 'Quantum Receiver', 'Quantum receiver (wireless camera / COFDM, 1RU)', 'Quantum', 'converter', 1,
    [R('in', 'RF', 'BNC', 4, 'UHF In (per demod card)'), R('out', SDI, 'SFP+', 2, 'Main video out'), R('out', SDI, 'SFP+', 2, 'Monitor out'),
     R('io', 'Ethernet', 'RJ45', 1, 'WAN'), R('io', 'Ethernet', 'RJ45', 3, 'LAN'), R('in', SDI, 'BNC', 1, 'ASI In'), R('out', SDI, 'BNC', 1, 'ASI Out'),
     R('in', 'Reference', 'Micro BNC', 1, 'Genlock'), R('out', 'Audio', 'Other', 2, 'Audio (5-pin LEMO)'), R('io', 'Other', 'D-sub 15', 2, 'Return data'), AC1],
    'Up to 4 demodulator cards with 4 UHF inputs each (16 inputs). Video out on SFP+ (4 x 3G, 2 x 6G or 1 x 12G-SDI) with an ST 2110 option. '
    'Up to 230 W, 404 mm deep (427 with SFPs), 4.5 kg. Check: RF connector type and PSUs.', 'Vislink Quantum receiver data sheet',
    'https://www.vislink.com/product/quantum-receiver', verified=False, powerW=230, weightKg=4.5)
add('vislink.json', 'vislink-ultrareceiver-ld', 'Vislink', 'UltraReceiver LD', 'UltraReceiver LD diversity receiver (half rack, 1RU)', 'UltraReceiver', 'converter', 1,
    [R('in', 'RF', 'BNC', 4, 'UHF In'), R('out', SDI, 'Micro BNC', 4, 'SDI Out'), R('out', SDI, 'Micro BNC', 1, 'Monitor'), R('in', SDI, 'BNC', 1, 'ASI In'),
     R('out', SDI, 'Micro BNC', 1, 'ASI Out'), R('in', 'Reference', 'Micro BNC', 1, 'Genlock'), R('out', 'Audio', 'XLR3 male', 2, 'Audio Out'),
     R('io', 'Other', 'Other', 2, 'Camera control / Alarm (6-pin LEMO)'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), AC1],
    'Half-width 1RU receiver for Vislink camera links: 4 UHF inputs, 4 x 3G / HD-SDI out (UHD as quad), ASI in / out. About 100 W. '
    '210 x 44 x 350 mm, 1.2 kg.', 'Vislink UltraReceiver LD data sheet (11-24)', 'https://www.vislink.com/product/ulrx-ld/', w=6,
    boxMm={'w': 210, 'h': 44}, powerW=100, weightKg=1.2)

# ---------------- Kiloview ----------------
KV_SRC, KV_URL = 'Kiloview product catalogue 2025', 'https://www.kiloview.com/en/'
add('kiloview-more.json', 'kiloview-ru03', 'Kiloview', 'RU03', 'RU03 3RU chassis for NDI encoder / decoder modules (16 channels)', 'Rack chassis', 'shelf', 3,
    [AC2], '3RU rack chassis holding up to 16 Kiloview NDI encode / decode modules (N-series boxes), 6 fans, redundant power, 3.8 kg. '
    'Add the modules separately. Check: power inlets.', KV_SRC, KV_URL, verified=False)
add('kiloview-more.json', 'kiloview-cube-r1', 'Kiloview', 'CUBE R1', 'CUBE R1 multi-channel NDI recorder (2RU)', 'CUBE', 'computer', 2,
    [R('io', 'Ethernet', 'RJ45', 2, 'Network'), AC2],
    'Records and plays back up to 4 x 4Kp60 or 9 x 1080p60 NDI channels. Check: network ports and PSUs.', KV_SRC, KV_URL, verified=False)
add('kiloview-more.json', 'kiloview-cube-x1', 'Kiloview', 'CUBE X1', 'CUBE X1 NDI distribution system (3RU)', 'CUBE', 'computer', 3,
    [R('io', 'Ethernet', 'SFP+', 1, '10G'), R('io', 'Ethernet', 'RJ45', 2, 'Network'), AC2],
    'NDI core switcher / distributor: 16 NDI inputs to 32 outputs, 10G network port. 132 mm high. Check: other ports and PSUs.', KV_SRC, KV_URL, verified=False)

# ---------------- Haivision Makito One ----------------
HV_SRC, HV_URL = 'Haivision Makito One product page (NAB 2026)', 'https://www.haivision.com/products/makito-one-video-transport-platform/'
for pn, ru, slots, cols in (('F4', 1, 4, 4), ('F18', 4, 18, 9)):
    frame('haivision-more.json', 'haivision-makito-one-' + pn.lower(), 'Haivision', f'Makito One {pn}', f'Makito One {pn} chassis, {slots} blades', 'Makito One', ru,
          dict(system='Haivision Makito One', slots=slots, orient='v', cols=cols, controller='Built in.'), [AC2],
          f'{ru}RU Makito One video transport chassis for up to {slots} encoder / decoder blades, redundant power. Check: slot layout and management ports.',
          HV_SRC, HV_URL, verified=False)
card('haivision-more.json', 'haivision-makito-one-blade', 'Haivision', 'Makito One blade', 'Makito One encoder / decoder blade, dual 12G-SDI or ST 2110',
     'Makito One', ['Haivision Makito One'], [R('io', SDI, 'BNC', 2, '12G-SDI'), R('io', 'Ethernet', 'SFP28', 1, 'IP')],
     'Each blade has dual 12G-SDI or ST 2110 interfaces (HEVC / H.264, SRT). Check: blade part numbers and connectors.', HV_SRC, HV_URL, verified=False)

# ---------------- Matrox ----------------
add('matrox.json', 'matrox-monarch-edge-e4', 'Matrox', 'Monarch EDGE E4', 'Monarch EDGE E4 4-channel encoder / decoder (half width, 1RU)', 'Monarch EDGE', 'converter', 1,
    [R('io', SDI, 'BNC', 4, 'SDI (4:0, 3:1 or 2:2 enc:dec)'), R('in', 'Reference', 'BNC', 1, 'Genlock'), R('io', 'Ethernet', 'RJ45', 2, 'Network'), AC1],
    'Half-width 1RU appliance (two side by side per RU). 4 SDI with reconfigurable direction for remote production (H.264 / HEVC, SRT). '
    'Check: network ports, power and dimensions (spec page not reachable).', 'Matrox Monarch EDGE page', 'https://video.matrox.com/en/products/encoders-decoders/monarch-edge-series',
    verified=False, w=6)

# ---------------- Telstra DVN (carrier placeholders) ----------------
TL_URL = 'https://www.telstra.com.au/business-enterprise/industries/telstra-broadcast-services/australian-media-networks/distribution'
TL_NOTE = ('Carrier-owned and managed equipment for the Telstra Digital Video Network (DVN). Telstra does not publish the edge models it installs, '
           'and they change with network upgrades; the customer provides rack space and power. Ports here are a typical hand-off (HD / SD / ASI '
           'over BNC, dual fibre paths); edit them to match the site. ')
add('telstra.json', 'telstra-dvn-frame-2ru', 'Telstra', 'DVN card frame', 'Telstra DVN carrier card frame (2RU, model varies)', 'DVN', 'other', 2,
    [R('in', SDI, 'BNC', 4, 'SDI/ASI In'), R('out', SDI, 'BNC', 4, 'SDI/ASI Out'), R('io', 'Fibre', 'LC duplex', 2, 'Carrier fibre A/B'), AC2],
    TL_NOTE + 'Matches the 2RU "Telstra DVN cards" frames in existing site drawings.', 'Telstra DVN service description (no hardware details)', TL_URL, verified=False)
add('telstra.json', 'telstra-dvn-ntu-1ru', 'Telstra', 'DVN NTU', 'Telstra DVN network termination unit (1RU, model varies)', 'DVN', 'network', 1,
    [R('io', 'Fibre', 'LC duplex', 2, 'Carrier fibre A/B'), R('io', 'Ethernet', 'SFP+', 2, 'Customer hand-off'), AC1],
    TL_NOTE + 'Use for the carrier router / NTU that hands off IP services (10G-LR / 40G-LR / 100G-LR on Telstra\'s distributed production network).',
    'Telstra DVN service description (no hardware details)', TL_URL, verified=False)

# ---------------- Foxtel ----------------
FX_URL = 'https://www.foxtel.com.au/'
for pn, name, w, h, ports, note in (
        ('iQ5', 'Foxtel iQ5 set-top box (satellite or internet)', 210, 40,
         [R('in', 'RF', 'F', 1, 'Satellite In'), R('in', 'RF', 'Other', 1, 'Aerial In (PAL)'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
          R('out', 'Audio', 'TOSLINK', 1, 'Optical Out'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Power', 'DC barrel', 1, 'DC In')],
         'Streaming box that also takes a satellite feed; about half the size of earlier iQ boxes. 4K HDR over HDMI 2.1.'),
        ('iQ4', 'Foxtel iQ4 set-top box (satellite, 4K)', 300, 50,
         [R('in', 'RF', 'F', 2, 'Satellite In (dual LNB)'), R('in', 'RF', 'Other', 1, 'Aerial In (PAL)'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
          R('out', 'Audio', 'TOSLINK', 1, 'Optical Out'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-A', 1, 'USB'),
          R('in', 'Power', 'IEC C13', 1, 'Mains In')],
         'Satellite-only 4K PVR (8 satellite + 2 terrestrial tuners); 4K needs a dual-output satellite feed.'),
        ('iQ3', 'Foxtel iQ3 set-top box (cable or satellite)', 300, 50,
         [R('in', 'RF', 'F', 2, 'Satellite / cable In'), R('in', 'RF', 'Other', 1, 'Aerial In (PAL)'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
          R('out', 'Audio', 'TOSLINK', 1, 'Optical Out'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Power', 'IEC C13', 1, 'Mains In')],
         'HD PVR in cable and satellite versions; looks like the iQ4 from outside.')):
    cols = max(2, -(-w // 40)); ru = 1 if h <= 43 else 2
    add('foxtel.json', 'foxtel-' + pn.lower(), 'Foxtel', pn, name, 'Set-top boxes', 'converter', ru, ports,
        note + f' Sits on a rack shelf for off-air monitoring (about {w} mm wide, {h} mm high). Check: size and rear connectors '
        '(Foxtel does not publish them; estimated).', 'Foxtel and review articles (CompareTV, ChannelNews)', FX_URL, verified=False, w=cols,
        boxMm={'w': w, 'h': h})

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
