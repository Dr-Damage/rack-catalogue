#!/usr/bin/env python3
"""Venue wireless audio (added 2026-11-15): rack wireless mic receivers, in-ear monitor (IEM) transmitters, antenna
distribution (splitters) and IEM antenna combiners, plus assistive-listening transmitters.

  shure-more.json        AD4D, SLXD4D, QLXD4, PSM1000 P10T, PSM900 P9T, UA845UWB, UA844+SWB, PA821B, AD600 / AXT600
  sennheiser-more.json   SR 2050 IEM, SR IEM G4, EM 3732-II, EW-DX EM 2, EW-D EM, AC 3200-II, AC 3, ASA 214, ASA 3000,
                         Spectera base station
  lectrosonics.json      Venue 2 (VRM2 host, six VRT2 modules), DSQD, M2T
  wisycom.json           MRK980, MTK982
  sony-wireless.json     DWR-R03D
  audiotechnica.json     ATW-R5220, ATW-R3210, ATW-DA49
  rfvenue.json           DISTRO9 HDR, COMBINE8
  beyerdynamic.json      TG 1000 receiver
  akg.json               DMS800 SR, WMS470 SR
  mipro.json             ACT-848
  line6.json             XD-V75 RX
  pws.json               Professional Wireless Systems GX8 combiner
  listen.json            Listen Technologies LT-800 assistive-listening transmitter
shure.json / sennheiser.json (tools/dante.py) already hold ULXD4Q, ULXD4D, AD4Q, P300, EW-DX EM 4 Dante and EM 6000 Dante.
Antenna ports are type 'RF' on BNC. IEM inputs use the 'XLR/TRS combo' connector. Chargers, bodypacks, handhelds and
antennas are not rack gear and are left out. Specs from maker or dealer pages (each entry's source); 'Check:' marks
anything unconfirmed."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=False, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m)
AC = lambda: R('in', 'Power', 'IEC C14', 1, 'AC In')
DCIN = lambda v='12V DC': R('in', 'Power', 'Locking DC jack', 1, v)
LAN = lambda n=1, p='Network': R('io', 'Ethernet', 'RJ45', n, p)
DANTE = lambda: R('io', 'Dante/AES67', 'RJ45', 2, 'Dante / Network')
def RX(n, ant_out=True, xlr=True):          # receiver: antenna A/B in (+ cascade), one XLR per channel
    p = [R('in', 'RF', 'BNC', 2, 'Antenna In A/B')]
    if ant_out: p.append(R('out', 'RF', 'BNC', 2, 'Antenna Cascade A/B'))
    if xlr: p.append(R('out', 'Analog audio', 'XLR3M', n, 'Audio Out'))
    return p
def IEM(n):                                   # IEM transmitter: L/R input per channel, loop through, one antenna out per channel
    return [R('in', 'Analog audio', 'XLR/TRS combo', 2 * n, 'Audio In L/R'), R('out', 'Analog audio', '1/4" TRS', 2 * n, 'Loop Out L/R'),
            R('out', 'RF', 'BNC', n, 'Antenna Out'), F('out', 'Analog audio', '3.5mm TRS', 1, 'Headphone')]
def SPLIT(rx, ps=0, pslabel='DC Out to receivers'):   # antenna distribution: A/B in, rx outputs per side, cascade
    p = [R('in', 'RF', 'BNC', 2, 'Antenna In A/B'), R('out', 'RF', 'BNC', 2 * rx, 'RF Out to receivers (A/B)'),
         R('out', 'RF', 'BNC', 2, 'Cascade Out A/B')]
    if ps: p.append(R('out', 'Power', 'DC jack', ps, pslabel))
    return p
def COMB(n):                                  # IEM combiner: n transmitter inputs, one antenna output
    return [R('in', 'RF', 'BNC', n, 'Tx In'), R('out', 'RF', 'BNC', 1, 'Antenna Out')]

# ======================= Shure =======================
SH, SHU = 'Shure', 'https://www.shure.com/'
add('shure-more.json', 'shure-ad4d', SH, 'AD4D', 'AD4D Axient Digital dual-channel receiver', 'Axient Digital', 'audio', 1,
    RX(2) + [R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), DANTE(), AC()],
    'Two-channel Axient Digital receiver, full width 1U, ShowLink and Dante; same rear layout as the AD4Q with two channels. '
    'Check: AES output count.', 'Shure AD4D product page', SHU)
add('shure-more.json', 'shure-slxd4d', SH, 'SLXD4D', 'SLXD4D SLX-D dual-channel digital receiver', 'SLX-D', 'audio', 1,
    RX(2) + [R('out', 'Analog audio', '1/4" TRS', 2, 'Audio Out (jack)'), LAN(1), AC()],
    'Dual SLX-D receiver, full width 1U, with antenna cascade. SLXD4 is the half-rack single-channel version. Check: ports.', 'Shure SLX-D user guide', SHU)
add('shure-more.json', 'shure-qlxd4', SH, 'QLXD4', 'QLXD4 QLX-D single-channel digital receiver, half rack', 'QLX-D', 'audio', 1,
    RX(1) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Audio Out (jack)'), LAN(1), DCIN('15V DC')],
    'Half-rack QLX-D receiver on an external 15 V supply; two side by side on the URT2 tray. Check: ports.', 'Shure QLX-D user guide', SHU, w=6)
add('shure-more.json', 'shure-p10t', SH, 'P10T', 'PSM1000 P10T dual-channel IEM transmitter', 'PSM1000', 'audio', 1,
    IEM(2) + [LAN(2), AC()],
    'Two-channel PSM1000 in-ear monitor transmitter, full width 1U (483 x 343 x 44 mm, 4.7 kg), XLR/TRS combo inputs with loop outs, '
    'antennas front or rear, dual Ethernet. Feed several into a PA821B combiner. Check: antenna outputs (one per channel).',
    'AVL Gear P10T listing (Shure specifications)', 'https://avlgear.com/product/shure-p10t-g10-psm1000-dual-rack-unit-wireless-transmitter', weightKg=4.7)
add('shure-more.json', 'shure-p9t', SH, 'P9T', 'PSM900 P9T IEM transmitter, half rack', 'PSM900', 'audio', 1,
    IEM(1) + [DCIN('15V DC')],
    'Single-channel PSM900 in-ear transmitter, half rack 1U, stereo XLR/TRS inputs with loop outs. P3T (PSM300) is the smaller sibling. '
    'Check: ports.', 'Shure PSM900 user guide', SHU, w=6)
add('shure-more.json', 'shure-ua845uwb', SH, 'UA845UWB', 'UA845UWB antenna and power distribution (5-way), 1U', 'Antenna distribution', 'audio', 1,
    SPLIT(4, 4, 'DC Out 15V to receivers') + [AC()],
    'Wideband 174-1805 MHz active splitter: antenna A and B in, four receiver outputs per side plus cascade (fifth receiver or a second '
    'UA845UWB), four 15 V DC outputs to power receivers. 482.6 x 295.3 x 44.5 mm.', 'Shure UA845UWB user guide',
    'https://media.musson.com/mti/docs/u/a/ua845uwb_guide_en-us.pdf', verified=True)
add('shure-more.json', 'shure-ua844swb', SH, 'UA844+SWB', 'UA844+SWB antenna and power distribution, half rack', 'Antenna distribution', 'audio', 1,
    SPLIT(4, 5, 'DC Out to receivers') + [DCIN('15V DC')],
    'Half-rack passive-style splitter for four receivers (A/B), cascade out and DC power to up to five receivers. Check: ports.', 'Shure UA844+ user guide', SHU, w=6)
add('shure-more.json', 'shure-pa821b', SH, 'PA821B', 'PA821B 8-channel IEM antenna combiner, 1U', 'Combiner', 'audio', 1,
    COMB(8) + [R('out', 'Power', 'DC jack', 8, 'DC Out to transmitters'), AC()],
    'Combines up to eight PSM transmitters onto one antenna and can power them. PA421B is the four-way half-rack version. '
    'Check: DC output count.', 'Shure PA821B user guide', SHU)
add('shure-more.json', 'shure-ad600', SH, 'AD600', 'AD600 Axient Digital spectrum manager, 1U', 'Axient Digital', 'audio', 1,
    [R('in', 'RF', 'BNC', 2, 'Antenna In A/B'), R('out', 'RF', 'BNC', 2, 'Cascade A/B'), LAN(2), AC()],
    'Scans RF, calculates and deploys compatible frequencies to Axient Digital / ULX-D receivers. Replaces the AXT600. Check: ports.',
    'Shure AD600 user guide', SHU)

# ======================= Sennheiser =======================
SE, SEU = 'Sennheiser', 'https://www.sennheiser.com/'
add('sennheiser-more.json', 'sennheiser-sr-2050-iem', SE, 'SR 2050 IEM', 'SR 2050 IEM twin stereo transmitter', '2000 IEM', 'audio', 1,
    IEM(2) + [LAN(1), AC()], 'Two-channel stereo IEM transmitter, full width 1U; pairs with the AC 3200-II combiner. Check: ports.',
    'Sennheiser SR 2050 IEM spec sheet', SEU)
add('sennheiser-more.json', 'sennheiser-sr-iem-g4', SE, 'SR IEM G4', 'SR IEM G4 stereo transmitter, half rack', 'evolution wireless G4', 'audio', 1,
    IEM(1) + [DCIN()], 'Half-rack ew IEM G4 transmitter (GA 3 rack kit holds two). Check: ports.', 'Sennheiser ew IEM G4 manual', SEU, w=6)
add('sennheiser-more.json', 'sennheiser-em-3732-ii', SE, 'EM 3732-II', 'EM 3732-II twin true-diversity receiver', '3000 / 5000', 'audio', 1,
    RX(2) + [R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'), LAN(1), AC()],
    'Two-channel analogue receiver for the 3000 / 5000 series. Check: rack height and ports.', 'Sennheiser EM 3732-II spec sheet', SEU)
add('sennheiser-more.json', 'sennheiser-ew-dx-em-2', SE, 'EW-DX EM 2', 'EW-DX EM 2 two-channel digital receiver', 'EW-DX', 'audio', 1,
    RX(2) + [R('out', 'Analog audio', '1/4" TRS', 2, 'Audio Out (jack)'), LAN(1), DCIN()],
    'Two-channel EW-DX receiver, half rack 1U. EW-DX EM 4 Dante (full width) is in sennheiser.json. Check: ports.', 'Sennheiser EW-DX EM 2 page', SEU, w=6)
add('sennheiser-more.json', 'sennheiser-ew-d-em', SE, 'EW-D EM', 'EW-D EM digital receiver, half rack', 'Evolution Wireless Digital', 'audio', 1,
    RX(1, ant_out=False) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Audio Out (jack)'), LAN(1), DCIN()],
    'Single-channel EW-D receiver, half rack. Check: ports.', 'Sennheiser EW-D manual', SEU, w=6)
add('sennheiser-more.json', 'sennheiser-ac-3200-ii', SE, 'AC 3200-II', 'AC 3200-II active 8:1 antenna combiner', 'Combiner', 'audio', 1,
    COMB(8) + [AC()], 'Combines up to eight IEM transmitters (100 mW in each) onto one antenna. Check: connectors.',
    'Sennheiser AC 3200-II spec sheet', 'https://docs.cloud.sennheiser.com/en-us/2000-iem/2000-iem/product-variants-ac3200.html')
add('sennheiser-more.json', 'sennheiser-ac-3', SE, 'AC 3', 'AC 3 4:1 antenna combiner, half rack', 'Combiner', 'audio', 1,
    COMB(4) + [R('out', 'Power', 'DC jack', 4, 'DC Out to transmitters'), DCIN()], 'Four-way IEM combiner for ew IEM transmitters. Check: ports.',
    'Sennheiser AC 3 manual', SEU, w=6)
add('sennheiser-more.json', 'sennheiser-asa-214', SE, 'ASA 214', 'ASA 214 active antenna splitter (4 receivers), 1U', 'Antenna distribution', 'audio', 1,
    SPLIT(4, 4) + [AC()], 'Splits two diversity antennas to four twin receivers (or eight with cascade). Check: ports.', 'Sennheiser ASA 214 manual', SEU)
add('sennheiser-more.json', 'sennheiser-asa-3000', SE, 'ASA 3000', 'ASA 3000 antenna splitter (8 outputs), 1U', 'Antenna distribution', 'audio', 1,
    SPLIT(8) + [AC()], 'Antenna splitter for Digital 6000 / 3000-5000 receivers: A/B in, eight outputs per side, cascade. Check: ports.',
    'Sennheiser ASA 3000 spec sheet', SEU)
add('sennheiser-more.json', 'sennheiser-spectera-base', SE, 'Spectera Base Station', 'Spectera wideband bidirectional base station, 1U', 'Spectera', 'audio', 1,
    [R('io', 'RF', 'BNC', 2, 'DAD antenna (RF over coax)'), DANTE(), R('io', 'MADI audio', 'BNC', 2, 'MADI'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'),
     LAN(1, 'Control'), AC()],
    'Wideband digital base station (mics and IEM in one system) with Dante / AES67 and MADI; DAD antennas on coax. Check: ports.',
    'Sennheiser Spectera product page', SEU)

# ======================= Lectrosonics =======================
LE, LEU = 'Lectrosonics', 'https://www.lectrosonics.com/'
add('lectrosonics.json', 'lectrosonics-venue-2', LE, 'VRM2 Venue 2', 'Venue 2 six-channel modular receiver (VRM2 + VRT2)', 'Venue 2', 'audio', 1,
    [R('in', 'RF', 'BNC', 2, 'Antenna In A/B'), R('out', 'RF', 'BNC', 2, 'Antenna Loop A/B'), R('out', 'Analog audio', 'XLR3M', 6, 'Audio Out'),
     F('io', 'USB', 'USB', 1, 'USB'), R('in', 'Power', 'Locking DC jack', 1, '10-18V DC')],
    '1U host (483 x 197 mm deep) with built-in multicoupler (dual 1 in, 7 out) for up to six VRT2 receiver modules, one balanced XLR '
    'out per channel. Antenna inputs can be moved to the front. Check: USB position.', 'Lectrosonics VRM2WBL specifications',
    'https://www.markertek.com/Attachments/Specifications/Lectrosonics/VRM2WBL-Specifications.pdf', verified=True)
add('lectrosonics.json', 'lectrosonics-dsqd', LE, 'DSQD', 'DSQD four-channel digital receiver, half rack', 'D Squared', 'audio', 1,
    RX(4) + [R('out', 'AES/EBU', 'DB25', 1, 'AES3 Out'), DCIN()], 'Half-rack 4-channel digital receiver (analogue XLR or AES3 out). '
    'Check: connectors.', 'Lectrosonics DSQD manual', LEU, w=6)
add('lectrosonics.json', 'lectrosonics-m2t', LE, 'M2T', 'M2T Duet digital IEM transmitter, half rack', 'Duet', 'audio', 1,
    IEM(2) + [R('in', 'Dante/AES67', 'RJ45', 1, 'Dante (option)'), DCIN()], 'Two-channel (or one stereo) digital IEM transmitter for '
    'Duet M2R receivers. Check: rack width and ports.', 'Lectrosonics M2T manual', LEU, w=6)

# ======================= Wisycom =======================
WI, WIU = 'Wisycom', 'https://www.wisycom.com/'
add('wisycom.json', 'wisycom-mrk980', WI, 'MRK980', 'MRK980 dual true-diversity receiver with Dante, 1U', 'MRK', 'audio', 1,
    RX(2) + [R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), DANTE(), F('io', 'USB', 'USB', 1, 'USB'), R('io', 'GPIO', 'Other', 1, 'GPIO / PTT (EXP1 option)'), AC()],
    'Ultra-wideband (VHF and UHF) two-channel receiver: analogue, AES and redundant Dante outputs, optional PTT outputs and EXP1 '
    'expansion board. Check: connector counts.', 'Prolyd / Full Compass MRK980 listings', 'https://www.gothamsound.com/node/21792')
add('wisycom.json', 'wisycom-mtk982', WI, 'MTK982', 'MTK982 dual IEM / IFB transmitter, 1U', 'MTK', 'audio', 1,
    IEM(2) + [LAN(1), AC()], 'Wideband two-channel IEM and IFB transmitter. Check: ports.', 'Wisycom MTK982 page', WIU)

# ======================= Sony =======================
add('sony-wireless.json', 'sony-dwr-r03d', 'Sony', 'DWR-R03D', 'DWR-R03D digital wireless receiver (2 channels)', 'DWX', 'audio', 1,
    RX(2) + [R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'), LAN(1), AC()],
    'Two-channel DWX digital receiver with Dante option. Check: rack width and ports.', 'Sony DWR-R03D page', 'https://pro.sony/')

# ======================= Audio-Technica =======================
AT, ATU = 'Audio-Technica', 'https://www.audio-technica.com/'
add('audiotechnica.json', 'audiotechnica-atw-r5220', AT, 'ATW-R5220', 'ATW-R5220 5000 series dual receiver, 1U', '5000 Series', 'audio', 1,
    RX(2) + [DANTE(), AC()], 'Two-channel 5000 series (4th gen) receiver with Dante. Check: ports.', 'Audio-Technica ATW-R5220 page', ATU)
add('audiotechnica.json', 'audiotechnica-atw-r3210', AT, 'ATW-R3210', 'ATW-R3210 3000 series receiver, half rack', '3000 Series', 'audio', 1,
    RX(1, ant_out=False) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Audio Out (jack)'), DCIN()], 'Half-rack single receiver. Check: ports.',
    'Audio-Technica ATW-R3210 page', ATU, w=6)
add('audiotechnica.json', 'audiotechnica-atw-da49', AT, 'ATW-DA49', 'ATW-DA49 antenna distribution (4 receivers), 1U', 'Antenna distribution', 'audio', 1,
    SPLIT(4, 4) + [AC()], 'Active splitter for four receivers, with cascade and DC power outputs. Check: ports.', 'Audio-Technica ATW-DA49 page', ATU)

# ======================= RF Venue =======================
RV = 'RF Venue'
add('rfvenue.json', 'rfvenue-distro9-hdr', RV, 'DISTRO9 HDR', 'DISTRO9 HDR multi-zone antenna distribution (9 receivers)', 'DISTRO', 'audio', 1,
    [R('in', 'RF', 'BNC', 4, 'Antenna In (2 zones x A/B)'), R('out', 'RF', 'BNC', 18, 'RF Out to receivers (A/B)'),
     R('out', 'Power', 'Anderson Powerpole', 9, '12V DC Out to receivers'), AC()],
    'Wideband 50-1000 MHz splitter for nine diversity receivers with two antenna zones; any unity-gain output can cascade to another '
    'DISTRO9. 480 x 250 x 45 mm. Check: height (the sheet says both 2RU and 45 mm) and output counts.', 'RF Venue DISTRO9 spec sheet',
    'https://www.rfvenue.com/hubfs/Spec%20Sheets/DISTRO9_spec_REV1.pdf')
add('rfvenue.json', 'rfvenue-combine8', RV, 'COMBINE8', 'COMBINE8 8-channel IEM transmitter combiner, 1U', 'COMBINE', 'audio', 1,
    COMB(8) + [AC()], 'Combines eight IEM / IFB transmitters onto one antenna. COMBINE4 is the 4-channel version. Check: ports.',
    'RF Venue COMBINE8 page', 'https://www.rfvenue.com/')

# ======================= Others =======================
add('beyerdynamic.json', 'beyerdynamic-tg-1000-receiver', 'beyerdynamic', 'TG 1000 receiver', 'TG 1000 two-channel digital receiver, 1U', 'TG 1000', 'audio', 1,
    RX(2) + [R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), DANTE(), AC()], 'Wideband 470-789 MHz two-channel receiver with Dante option. '
    'Check: ports.', 'beyerdynamic TG 1000 page', 'https://www.beyerdynamic.com/')
add('akg.json', 'akg-dms800-sr', 'AKG', 'DMS800 SR', 'DMS800 digital wireless receiver (4 channels), 1U', 'DMS800', 'audio', 1,
    RX(4) + [R('out', 'AES/EBU', 'XLR3M', 2, 'AES3 Out'), DANTE(), AC()], 'Four-channel digital receiver (discontinued, still in venues). '
    'Check: channel count and ports.', 'AKG DMS800 manual', 'https://www.akg.com/')
add('akg.json', 'akg-wms470-sr', 'AKG', 'SR470', 'WMS470 SR470 receiver, half rack', 'WMS470', 'audio', 1,
    RX(1, ant_out=False) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Audio Out (jack)'), DCIN()], 'Half-rack analogue receiver. Check: ports.',
    'AKG WMS470 manual', 'https://www.akg.com/', w=6)
add('mipro.json', 'mipro-act-848', 'MIPRO', 'ACT-848', 'ACT-848 quad-channel receiver, 1U', 'ACT', 'audio', 1,
    RX(4) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Mix Out'), LAN(1), AC()], 'Four-channel UHF receiver. Check: ports.', 'MIPRO ACT-848 page',
    'https://www.mipro.com.tw/')
add('line6.json', 'line6-xd-v75-rx', 'Line 6', 'XD-V75 RX', 'XD-V75 digital wireless receiver, half rack', 'XD-V', 'audio', 1,
    RX(1, ant_out=False) + [R('out', 'Analog audio', '1/4" TRS', 1, 'Audio Out (jack)'), DCIN('9V DC')], '2.4 GHz digital receiver. Check: ports.',
    'Line 6 XD-V75 manual', 'https://line6.com/', w=6)
add('pws.json', 'pws-gx8', 'Professional Wireless Systems', 'GX8', 'GX8 8-channel IEM transmitter combiner, 1U', 'Combiner', 'audio', 1,
    COMB(8) + [AC()], 'Touring-grade active combiner for eight IEM transmitters. Check: ports.', 'PWS GX8 page', 'https://www.professionalwireless.com/')
add('listen.json', 'listen-lt-800', 'Listen Technologies', 'LT-800', 'LT-800 stationary RF assistive-listening transmitter, 1U', 'ListenRF', 'audio', 1,
    [R('in', 'Analog audio', 'XLR/TRS combo', 2, 'Audio In'), R('out', 'Analog audio', '1/4" TRS', 1, 'Loop Out'), R('out', 'RF', 'BNC', 1, 'Antenna Out'),
     LAN(1), R('in', 'Power', 'DC jack', 1, '12V DC')],
    '72 MHz (or 216 MHz) FM assistive-listening transmitter for venue hearing access. Check: rack width and ports.', 'Listen LT-800 page',
    'https://www.listentech.com/')

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
allids = set()
for f in idx:
    if f in FILES: continue
    try: allids |= {m['id'] for m in json.load(open(os.path.join(CAT, f)))}
    except Exception: pass
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    clash = allids & set(ids); assert not clash, clash
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index', sum(len(v) for v in FILES.values()), 'models')
