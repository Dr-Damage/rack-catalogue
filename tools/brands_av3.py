#!/usr/bin/env python3
"""AV and broadcast brands batch 3, a gap hunt through a long brand list (added 2026-11-15):
  lynx-yellobrik.json   Lynx Technik yellobrik modules (converters, DAs, fibre, frame sync, embedders) and the RFR 1200 frame.
  lynx-greenmachine.json greenMachine titan and callisto half-rack units (fit the RFR 6000 frame in lynx.json).
  kiloview-n.json       Kiloview N-series NDI converters (fit the RU01 / RU03 frames).
  bzbgear-ipgear.json   BZBGear IPGEAR Ultra and PRO units (fit the IPGEAR rack brackets in bzbgear.json).
  avpro-mxnet.json      AVPro Edge MXnet 1G encoder and decoder (fit the AC-MXNET-1G-R15 rack).
  muxlab-more.json      MuxLab 500451 HDBaseT extenders (fit the 500905 / 500920 chassis).
  kramer-megatools.json Kramer VM-2H2 (fits the RK-T2B adapter).
  tascam-more.json      TASCAM CD / media players, master recorder, Dante interfaces.
  vitec-more.json       VITEC MGW Ace encoder / decoder and their rack shelf.
  magewell.json         Magewell Ultra Encode AIO.
  matrox-more.json      Matrox Monarch EDGE D4 decoder.
  panasonic-more.json   Panasonic KAIROS Core 200L1, AK-UCU600 CCU.
  sony-bpu.json         Sony BPU-4800 baseband processor.
  vizrt-more.json       Vizrt 3Play 3P2.
  epiphan-more.json     Epiphan Pearl Nexus.
  rgblink.json          RGBlink FLEX 8 modular switcher.
  vaddio.json           Vaddio AV Bridge Mini.
Brands on the list with nothing added this round: Blackmagic Design and AJA (already well covered), AWS Elemental, AVMATRIX,
OREI, Roland, Mackie, Teradek, DVEO, Lumens (already in other files); Broadcast Pix (no published rack size), and the mostly
desktop or consumer brands (A-Neuvideo, VigilLink, DVDO, Cerevo, CNDLive, INOGENI, MAXHUB, MiNE Media, Miri, MR-NET, Raywowo,
RODE, SalrayWorks, SCIENCE IMAGE, Sprolink, Videon, YoloLiv).
Specs from maker data sheets and dealer listings; 'Check:' marks anything unconfirmed."""
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
AC = lambda n=1, p=None: R('in', 'Power', 'IEC C14', n, p or ('PSU' if n > 1 else 'AC In'))
DC = lambda v='12V DC', c='DC locking', n=1: R('in', 'Power', c, n, v)
LAN = lambda n=1, p='LAN': R('io', 'Ethernet', 'RJ45', n, p)
S3 = lambda d, n, p: R(d, '3G-SDI', 'BNC', n, p)
S12 = lambda d, n, p: R(d, '12G-SDI', 'BNC', n, p)
H = lambda d, n, p: R(d, 'HDMI', 'HDMI', n, p)
LCD = lambda d, n, p='Fibre': R(d, 'Fibre', 'LC duplex', n, p)
LCS = lambda n, p='Fibre (simplex)': R('io', 'Fibre', 'LC', n, p)
SFPF = lambda d, n, p='Fibre SFP (option)': R(d, 'Fibre', 'LC (SFP)', n, p)
REF = lambda n=1, p='Ref In': R('in', 'Reference', 'BNC', n, p)

# ======================= Lynx Technik yellobrik =======================
YF, LX = 'lynx-yellobrik.json', 'Lynx Technik'
YSRC, YURL = 'Lynx Technik yellobrik catalog Rev55 (2026)', 'https://lynx-usa.com/wp-content/uploads/2026/05/Yellobrik_Catalog_Rev55.pdf'
YB1, YB2 = {'w': 30, 'h': 41}, {'w': 60, 'h': 41}
def yb(pn, name, cat, ports, notes='', double=False, power=True, verified=True):
    note = (notes + ' ' if notes else '') + ('Double-width module (takes two frame slots). ' if double else '') + \
        'Fits the RFR 1000 / RFR 1200 frames or stands alone. Check: module size.'
    add(YF, 'lynx-' + pn.lower().replace(' ', '-'), LX, pn, f'yellobrik {pn} {name}', 'yellobrik', cat, 1,
        ports + ([R('in', 'Power', 'DC barrel', 1, '12V DC (or frame)')] if power else []), note.strip(), YSRC, YURL,
        verified=verified, w=2 if double else 1, formFactor='yellobrik', boxMm=YB2 if double else YB1)

add(YF, 'lynx-rfr-1200', LX, 'RFR 1200', 'yellobrik RFR 1200 1RU rack frame (14 modules, powered slot bus)', 'yellobrik', 'shelf', 1,
    [F('io', 'Other', 'Card slot', 14, 'yellobrik slot'), DC('12V DC primary', 'DC locking'), DC('12V DC secondary', 'DC locking'),
     R('out', 'GPIO', 'Other', 1, 'Power-fail alarm GPO')],
    'Up to 14 yellobriks; modules take power from the slot bus (200 W per frame), primary and secondary 12 V DC inputs. '
    'The RCT 1012 controller adds USB control of up to 12 modules. Add each yellobrik as its own device. Check: rear connectors.',
    YSRC, YURL, verified=True, carrier={'bays': 14, 'fits': ['yellobrik']})

yb('CDE 1922', '3G-SDI / ST 2110 bridge', 'converter',
   [S3('in', 2, 'SDI In'), S3('out', 2, 'SDI Out'), R('io', 'SFP', 'SFP+', 2, '10GbE ST 2110'), LAN(2, 'Mgmt')], double=True)
yb('PEC 1464', 'H.264 / H.265 streamer and recorder', 'converter',
   [H('in', 1, 'HDMI In'), S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), R('in', 'Analog audio', 'Other', 1, 'Analog audio In'),
    R('io', 'USB', 'USB-A', 1, 'USB 3.0 record'), R('io', 'USB', 'USB-B', 1, 'USB control'), R('io', 'SFP', 'SFP', 1, 'Network')],
   'Check: audio connector.', double=True)
yb('IDC 1411', 'AI voice cleaner (SDI audio)', 'audio',
   [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out'), SFPF('io', 1), R('in', 'AES/EBU', 'BNC', 1, 'AES In'), R('out', 'AES/EBU', 'BNC', 1, 'AES Out')],
   double=True)
yb('CHD 1402', 'HDMI to 12G-SDI converter', 'converter', [H('in', 1, 'HDMI In'), S12('out', 2, 'SDI Out'), SFPF('out', 1)])
yb('CHD 1412', 'HDMI to 12G-SDI converter with frame sync', 'converter',
   [H('in', 1, 'HDMI In'), S12('out', 2, 'SDI Out'), SFPF('out', 1), R('in', 'Analog audio', 'Other', 1, 'Analog stereo In'),
    R('in', 'AES/EBU', 'BNC', 1, 'AES In'), REF()], 'Check: analog audio connector.')
yb('CHD 1802-1', 'HDMI to 3G-SDI converter', 'converter', [H('in', 1, 'HDMI In'), S3('out', 2, 'SDI Out'), SFPF('out', 1)])
yb('CHD 1812-1', 'HDMI to 3G-SDI converter with frame sync', 'converter',
   [H('in', 1, 'HDMI In'), S3('out', 2, 'SDI Out'), SFPF('out', 1), R('in', 'Analog audio', 'Other', 2, 'Analog In'), REF()],
   'Check: analog audio connector.')
yb('CDH 1411', '12G-SDI to HDMI monitoring converter', 'converter',
   [S12('in', 2, 'SDI In'), SFPF('in', 1), S12('out', 1, 'SDI Loop'), H('out', 1, 'HDMI Out'), R('out', 'Analog audio', 'Other', 1, 'Analog audio Out'),
    R('out', 'AES/EBU', 'BNC', 1, 'AES Out'), R('io', 'USB', 'USB-B', 1, 'USB control')], 'Check: analog audio connector.')
yb('CDH 1813', '3G-SDI to HDMI monitoring converter', 'converter',
   [S3('in', 1, 'SDI In'), SFPF('io', 1), H('out', 1, 'HDMI Out'), R('out', 'Analog audio', 'Other', 1, 'Analog audio Out'),
    R('out', 'AES/EBU', 'BNC', 1, 'AES Out')], 'Check: SDI input count and audio connector.')
yb('SPG 1708', 'sync pulse generator', 'other',
   [REF(1, 'Genlock In'), R('out', 'Reference', 'BNC', 2, 'Bi / Tri-level Out'), R('out', 'Word clock', 'BNC', 1, 'WCLK / DARS Out')],
   'Check: output counts.')
yb('OTX 1712-2', 'analog sync / video to fibre transmitter', 'converter',
   [R('in', 'Analog video', 'BNC', 1, 'Sync / video In'), R('out', 'Analog video', 'BNC', 1, 'Loop'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')],
   'Fibre LC, ST, SC or MM versions.')
yb('ORX 1702-1', 'fibre to analog sync / video receiver', 'converter',
   [R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', 'Analog video', 'BNC', 1, 'Sync / video Out')], 'Fibre LC, ST, SC or MM versions. Check: output count.')
yb('PMV 1841', 'quad-split multiviewer', 'monitor', [S3('in', 4, 'SDI In'), H('out', 1, 'HDMI Out')])
yb('CQS 1462', '12G quad-link / single-link converter (2SI / SQD)', 'converter',
   [S12('in', 4, 'SDI In'), SFPF('in', 1, 'Fibre In (SFP)'), S12('out', 5, 'SDI Out'), SFPF('out', 1, 'Fibre Out (SFP)'), R('io', 'USB', 'USB-B', 1, 'USB control')])
yb('PVD 1400', '12G-SDI frame synchroniser', 'converter',
   [S12('in', 1, 'SDI In'), REF(), S12('out', 2, 'SDI Out'), S12('out', 1, 'SDI Loop'), SFPF('io', 1), R('io', 'USB', 'USB-B', 1, 'USB control')])
yb('PVD 1800', '3G-SDI frame synchroniser with up / down / cross conversion', 'converter',
   [S3('in', 2, 'SDI In'), S3('out', 2, 'SDI Out'), REF(), R('in', 'GPI', 'Other', 1, 'GPI (input switch)')], 'Check: connector counts.', verified=False)
yb('PDM 1484 D', '12G-SDI analog / AES audio embedder', 'audio',
   [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out'), R('io', 'Analog audio', 'Other', 4, 'Analog / AES audio'), R('io', 'USB', 'USB-B', 1, 'USB control')],
   'Check: audio connector.')
yb('PDM 1484 B', '12G-SDI AES audio embedder', 'audio', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 4, 'AES')],
   'Check: AES connector.')
yb('PDM 1383', '3G-SDI analog audio embedder', 'audio',
   [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Out'), R('io', 'Analog audio', 'DB25', 1, 'Analog audio (4 ch)'), SFPF('io', 1)])
for pn, nm, sig, i, o in (('DVD 1417', '12G-SDI 1x7 distribution amplifier', '12G-SDI', 1, 7),
                          ('DVD 1423', 'dual 12G-SDI 1x3 distribution amplifier', '12G-SDI', 2, 6),
                          ('DVD 1817', '3G-SDI 1x7 distribution amplifier', '3G-SDI', 1, 7),
                          ('DVD 1823', 'dual 3G-SDI 1x3 distribution amplifier', '3G-SDI', 2, 6)):
    yb(pn, nm, 'converter', [R('in', sig, 'BNC', i, 'SDI In'), R('out', sig, 'BNC', o, 'SDI Out')])
yb('DVA 1714', 'wideband analog video 1x4 distribution amplifier', 'converter',
   [R('in', 'Analog video', 'BNC', 1, 'Video In'), R('out', 'Analog video', 'BNC', 4, 'Video Out')], 'Check: connector type.')
# fibre: (pn, name, ports, double)
for pn, nm, ports, dbl in (
        ('OTR 1410', '12G-SDI fibre transceiver', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out'), LCD('io', 1)], False),
        ('OTR 1414', '4-channel 12G-SDI fibre transceiver', [S12('in', 4, 'SDI In'), S12('out', 4, 'SDI Out'), LCD('io', 2)], True),
        ('OBD 1410', '12G-SDI bidirectional fibre (simplex)', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out'), LCS(1)], False),
        ('OBD 1414', '4-channel 12G-SDI bidirectional fibre (simplex)', [S12('in', 4, 'SDI In'), S12('out', 4, 'SDI Out'), LCS(2)], True),
        ('OTT 1414', '4-channel 12G-SDI fibre transmitter', [S12('in', 4, 'SDI In'), LCD('out', 2)], False),
        ('ORR 1404', '4-channel fibre to 12G-SDI receiver', [LCD('in', 2), S12('out', 4, 'SDI Out')], False),
        ('OTT 1412', '2-channel 12G-SDI fibre transmitter', [S12('in', 2, 'SDI In'), LCD('out', 1)], False),
        ('ORR 1402', '2-channel fibre to 12G-SDI receiver', [LCD('in', 1), S12('out', 2, 'SDI Out')], False),
        ('OTX 1410', '12G-SDI fibre transmitter', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Loop'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')], False),
        ('ORX 1400', 'fibre to 12G-SDI receiver', [R('in', 'Fibre', 'LC', 2, 'Fibre In'), S12('out', 6, 'SDI Out')], False),
        ('OTR 1810-1', '3G-SDI fibre transceiver', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Out'), LCD('io', 1)], False),
        ('OTR 1814', '4-channel 3G-SDI fibre transceiver', [S3('in', 4, 'SDI In'), S3('out', 4, 'SDI Out'), LCD('io', 2)], True),
        ('OBD 1810-2', '3G-SDI bidirectional fibre (simplex)', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Out'), LCS(1)], False),
        ('OBD 1814', '4-channel 3G-SDI bidirectional fibre (simplex)', [S3('in', 4, 'SDI In'), S3('out', 4, 'SDI Out'), LCS(2)], True),
        ('OTT 1814', '4-channel 3G-SDI fibre transmitter', [S3('in', 4, 'SDI In'), LCD('out', 2)], False),
        ('ORR 1804', '4-channel fibre to 3G-SDI receiver', [LCD('in', 2), S3('out', 4, 'SDI Out')], False),
        ('OTT 1812-1', '2-channel 3G-SDI fibre transmitter', [S3('in', 2, 'SDI In'), LCD('out', 1)], False),
        ('ORR 1802-2', '2-channel fibre to 3G-SDI receiver', [LCD('in', 1), S3('out', 2, 'SDI Out')], False),
        ('OTX 1812', '3G-SDI fibre transmitter', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')], False),
        ('ORX 1802-2', 'fibre to 3G-SDI receiver', [R('in', 'Fibre', 'LC', 1, 'Fibre In'), S3('out', 2, 'SDI Out')], False),
        ('OTR 1210', 'MADI coax to fibre transceiver', [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), LCD('io', 1)], False),
        ('OBD 1210', 'MADI bidirectional fibre (simplex)', [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), LCS(1)], False),
        ('OET 1514', '1GbE fibre extender with 3-port switch', [LAN(2), LCD('io', 1)], False),
        ('OBD 1514 E', '1GbE bidirectional fibre extender with 3-port switch (simplex)', [LAN(2), LCS(1)], False),
        ('OET 1910', '1 / 10GbE copper to fibre converter', [LAN(1), LCD('io', 1)], False),
        ('OBD 1910', '1 / 10GbE bidirectional fibre converter (simplex)', [LAN(1), LCS(1)], False),
        ('ODT 1510', 'serial and GPI fibre transmitter', [R('io', 'RS-232', 'RJ45', 1, 'Serial'), R('io', 'GPIO', 'RJ45', 1, 'GPI (2)'), LCD('io', 1)], False),
        ('OBD 1510 D', 'serial and GPI bidirectional fibre (simplex)', [R('io', 'RS-232', 'RJ45', 1, 'Serial / GPI'), LCS(1)], False)):
    yb(pn, nm, 'converter', ports, 'Fibre versions for single-mode, multimode or CWDM.' if pn.startswith(('OTR 14', 'OTR 18', 'OTX', 'ORX', 'OET')) else '',
       double=dbl, verified=not dbl)
for pn, nm, o in (('OSP 1812', '50/50 optical splitter (passive)', 2), ('OSP 1812M', '90/10 monitoring optical splitter (passive)', 2),
                  ('OSP 1814', 'four-way optical splitter (passive)', 4)):
    yb(pn, nm, 'patch', [R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', 'Fibre', 'LC', o, 'Fibre Out')], 'Single-mode LC, no power needed.', power=False)
yb('OSW 1022', '2x2 optical switch (CWDM / DWDM)', 'patch',
   [LCD('io', 2, 'Fibre pair'), R('in', 'GPI', 'Other', 2, 'GPI'), R('out', 'GPI', 'Other', 2, 'GPO')], 'Check: GPI connector.')

# ======================= Lynx Technik greenMachine =======================
GMF = 'lynx-greenmachine.json'
GM = {'w': 218, 'h': 44}
add(GMF, 'lynx-gm-6840-titan', LX, 'GM 6840', 'greenMachine titan 4-channel 12G / 3G-SDI processing platform', 'greenMachine', 'converter', 1,
    [S12('in', 1, 'SDI In (12G)'), S3('in', 3, 'SDI In'), S12('out', 1, 'SDI Out (12G)'), S3('out', 3, 'SDI Out'), H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Out'),
     REF(), R('out', 'Reference', 'BNC', 1, 'Ref Out'), R('io', 'Analog audio', 'DB25', 1, 'Analog / AES audio (4 in, 4 out)'),
     R('io', 'SFP', 'SFP', 3, 'Fibre SFP (option)'), LAN(1), R('io', 'GPIO', 'RJ45', 1, 'GPI 4 in / 4 out'), R('io', 'RS-422', 'RJ45', 1, 'Serial'),
     DC('12V DC A', 'DC locking'), DC('12V DC B (redundant)', 'DC locking')],
    'Half-rack 1RU, 218 x 44 x 225 mm, 1.4 kg, 45 W, 7-24 V DC. Function set by greenMachine APPs. Fits the RFR 6000 frame (2 per 1RU). '
    'Check: DC connector type.', 'Lynx Technik GM 6840 titan data sheet Rev3.0', 'https://lynx-usa.com/wp-content/uploads/2023/10/GM6840_Titan_Rev3.0.pdf',
    verified=True, w=6, formFactor='greenMachine', boxMm=GM, powerW=45, weightKg=1.4)
add(GMF, 'lynx-gm-6820-callisto', LX, 'GM 6820', 'greenMachine callisto 2-channel 3G-SDI processing platform', 'greenMachine', 'converter', 1,
    [S3('in', 2, 'SDI In'), S3('out', 2, 'SDI Out'), H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Out'), REF(), R('out', 'Reference', 'BNC', 1, 'Ref / CVBS Out'),
     R('io', 'Analog audio', 'DB25', 1, 'Analog / AES audio (4 in, 4 out)'), R('io', 'SFP', 'SFP', 2, 'Fibre SFP (option)'), LAN(1),
     R('io', 'GPIO', 'RJ45', 1, 'GPI 2 in / 2 out'), DC('12V DC A', 'DC locking'), DC('12V DC B (redundant)', 'DC locking')],
    'Half-rack 1RU, 218 x 44 x 225 mm, 1.1 kg, 25 W, 7-24 V DC. Fits the RFR 6000 frame (2 per 1RU). Check: SFP count and DC connector type.',
    'Lynx Technik GM 6820 callisto data sheet', 'https://www.lynx-technik.com/products/greenmachine/greenmachine-hardware/greenmachine-callisto-3ghdsd-dual-channel-sdi-video-and-audio-processing-platform/',
    verified=True, w=6, formFactor='greenMachine', boxMm=GM, powerW=25, weightKg=1.1)

# ======================= Kiloview N series =======================
KF, KV = 'kiloview-n.json', 'Kiloview'
KB = {'w': 105, 'h': 35}
add(KF, 'kiloview-n60', KV, 'N60', 'N60 4K HDMI / USB to NDI bi-directional converter', 'N series', 'converter', 1,
    [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Out / Loop'), R('io', 'USB', 'USB-A', 1, 'USB 3.0'), R('io', 'USB', 'USB-C', 1, 'USB-C'),
     R('io', 'Ethernet', 'RJ45', 1, 'LAN 1 (PoE)'), LAN(1, 'LAN 2'), R('in', 'Analog audio', '3.5mm', 1, 'Line In'), R('out', 'Analog audio', '3.5mm', 1, 'Line Out'),
     DC('12V DC (or PoE)', 'DC barrel')],
    '135 x 105 x 35 mm, 480 g, 16 W max. Fits the RU01 (4 per 1RU) and RU03 frames.', 'Videoguys N60 listing',
    'https://videoguys.com/collections/kiloview/products/kiloview-n60-4k-hdmi-usb-to-ndi-bi-directional-converter',
    verified=True, w=3, formFactor='Kiloview encoder', boxMm=KB, powerW=16, weightKg=0.48)
add(KF, 'kiloview-n50', KV, 'N50', 'N50 12G-SDI / USB to NDI bi-directional converter', 'N series', 'converter', 1,
    [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Out / Loop'), R('io', 'USB', 'USB-A', 1, 'USB 3.0'), R('io', 'Ethernet', 'RJ45', 1, 'LAN 1 (PoE)'), LAN(1, 'LAN 2'),
     R('in', 'Analog audio', '3.5mm', 1, 'Line In'), R('out', 'Analog audio', '3.5mm', 1, 'Line Out'), DC('12V DC (or PoE)', 'DC barrel')],
    'SDI sister of the N60. Fits the RU01 and RU03 frames. Check: ports and size (taken from the N60).', 'Kiloview N50 dealer listing',
    'https://avlgear.com/collections/video-production/products/kiloview-n50-12g-sdi-usb-to-ndi-bi-directional-converter',
    w=3, formFactor='Kiloview encoder', boxMm=KB)
add(KF, 'kiloview-n40', KV, 'N40', 'N40 4K HDMI to NDI bi-directional converter', 'N series', 'converter', 1,
    [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Out / Loop'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('in', 'Analog audio', '3.5mm', 1, 'Line In'),
     R('out', 'Analog audio', '3.5mm', 1, 'Line Out'), R('io', 'USB', 'USB-A', 1, 'USB'), DC('12V DC (or PoE)', 'DC barrel')],
    'Fits the RU01 (4 per 1RU), RN01 and RU03 frames. Check: ports and size.', 'Kiloview N40 dealer listing',
    'https://kiloview.com/en/ndi/4k-hdmi', w=3, formFactor='Kiloview encoder', boxMm=KB)

# ======================= BZBGear IPGEAR units =======================
BF, BZ = 'bzbgear-ipgear.json', 'BZBGear'
add(BF, 'bzbgear-bg-ipgear-ultra', BZ, 'BG-IPGEAR-ULTRA', 'BG-IPGEAR-ULTRA 4K AV-over-IP transceiver (encoder / decoder)', 'IPGEAR', 'converter', 1,
    [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Out'), R('in', 'Analog audio', 'Terminal block', 2, 'Balanced audio In'),
     R('out', 'Analog audio', 'Terminal block', 2, 'Balanced audio Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('io', 'SFP', 'SFP', 1, 'Fibre SFP'),
     R('io', 'USB', 'USB-C', 1, 'USB-C host'), R('io', 'USB', 'USB-A', 2, 'USB KVM'), R('io', 'USB', 'USB-A', 2, 'USB 2.0'),
     R('io', 'RS-232', 'Terminal block', 1, 'RS-232'), DC('12V DC (or PoE)', 'DC barrel')],
    'One box works as encoder or decoder. 204 x 30 x 132 mm, 5.4 W. Fits the RM2 (2 per 1RU) and RM10 (10 in 6RU) brackets. Check: USB split.',
    'BZBGear BG-IPGEAR-ULTRA product brief', 'https://bzbgear.com/wp-content/uploads/BG-IPGEAR-ULTRA-pb.pdf',
    verified=True, w=6, formFactor='BZBGear IPGEAR', boxMm={'w': 204, 'h': 30}, powerW=5.4)
for pn, nm, ports, wt, pw in (
        ('BG-IPGEAR-PRO-T', 'IPGEAR PRO 4K60 AV-over-IP transmitter',
         [H('in', 1, 'HDMI In'), R('in', 'Analog audio', '3.5mm', 2, 'Audio / IR In'), R('out', 'Analog audio', '3.5mm', 2, 'Audio / IR Out'),
          R('out', 'Other', 'TOSLINK', 1, 'S/PDIF Out'), R('io', 'USB', 'USB-A', 2, 'USB'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), DC('5V DC (or PoE)', 'DC barrel')], 0.66, 6),
        ('BG-IPGEAR-PRO-R', 'IPGEAR PRO 4K60 AV-over-IP receiver',
         [H('out', 1, 'HDMI Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('out', 'Other', 'TOSLINK', 1, 'S/PDIF'), R('out', 'Analog audio', '3.5mm', 2, 'Audio / IR Out'),
          R('io', 'USB', 'USB-A', 5, 'USB'), DC('5V DC (or PoE)', 'DC barrel')], 0.64, 7)):
    add(BF, 'bzbgear-' + pn.lower(), BZ, pn, pn + ' ' + nm, 'IPGEAR PRO', 'converter', 1, ports,
        f'194 x 133 x 28 mm, {pw} W max, 5 V DC or 48 V PoE. Fits the IPGEAR PRO 4RU rack. Check: S/PDIF connector, RS-232 port.',
        'BZBGear BG-IPGEAR-PRO product brief', 'https://bzbgear.com/wp-content/uploads/catalogs/AVOIP_MiniCatalog.pdf',
        w=6, formFactor='BZBGear IPGEAR', boxMm={'w': 194, 'h': 28}, powerW=pw, weightKg=wt)

# ======================= AVPro Edge MXnet 1G =======================
XF, AV = 'avpro-mxnet.json', 'AVPro Edge'
XB = {'w': 200, 'h': 20}
add(XF, 'avpro-ac-mxnet-1g-e', AV, 'AC-MXNET-1G-E', 'AC-MXNET-1G-E MXnet 1G AV-over-IP encoder', 'MXnet 1G', 'converter', 1,
    [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Loop'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('io', 'SFP', 'SFP', 1, 'Fibre SFP'),
     R('out', 'Analog audio', 'Terminal block', 1, 'Audio Out (5-pin)'), R('in', 'Analog audio', '3.5mm', 1, 'Audio In'), R('io', 'Other', '3.5mm', 3, 'IR'),
     R('io', 'RS-232', 'Terminal block', 1, 'RS-232 (5-pin)'), R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'USB', 'Micro-USB', 1, 'Service'),
     DC('12V DC (or PoE)', 'DC barrel')],
    '200 x 104 x 20 mm, 6.5 W. Fits the AC-MXNET-1G-R15 rack (15 standing up).', 'AVPro Edge AC-MXNET-1G-E data sheet',
    'https://www.avproglobal.com/ac-mxnet-1g-e.html', verified=True, w=6, formFactor='AVPro MXnet card', boxMm=XB, powerW=6.5)
add(XF, 'avpro-ac-mxnet-1g-d', AV, 'AC-MXNET-1G-D', 'AC-MXNET-1G-D MXnet 1G AV-over-IP decoder', 'MXnet 1G', 'converter', 1,
    [H('out', 1, 'HDMI Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('io', 'SFP', 'SFP', 1, 'Fibre SFP'),
     R('out', 'Analog audio', 'Terminal block', 1, 'Audio Out (5-pin)'), R('io', 'Other', '3.5mm', 3, 'IR'), R('io', 'RS-232', 'Terminal block', 1, 'RS-232 (5-pin)'),
     R('io', 'USB', 'USB-A', 2, 'USB'), DC('12V DC (or PoE)', 'DC barrel')],
    'Same case as the encoder. Fits the AC-MXNET-1G-R15 rack. Check: ports (taken from the encoder).', 'AVPro Edge MXnet 1G page',
    'https://www.avproglobal.com/pages/mxnet-1g', w=6, formFactor='AVPro MXnet card', boxMm=XB)

# ======================= MuxLab extenders =======================
MF, MX = 'muxlab-more.json', 'MuxLab'
for pn, nm, pw in (('500451-TX', 'HDMI over HDBaseT extender transmitter, UHD-4K', 1.6), ('500451-RX', 'HDMI over HDBaseT extender receiver, UHD-4K', 3.2)):
    tx = pn.endswith('TX')
    add(MF, 'muxlab-' + pn.lower(), MX, pn, f'{pn} {nm}', 'HDBaseT extenders', 'converter', 1,
        [H('in' if tx else 'out', 1, 'HDMI In' if tx else 'HDMI Out'), R('io', 'Ethernet', 'RJ45', 1, 'HDBaseT link'), R('io', 'Other', '3.5mm', 2, 'IR'),
         DC('5V DC', 'DC barrel')],
        f'Sold as the 500451 kit (TX + RX). 4K up to 40 m, 1080p up to 70 m, {pw} W. Fits the 500905 (3 per 1U) and 500920 (16 in 3U) chassis. '
        'Check: case size (chassis take 111 x 75 x 25 mm units).', 'MuxLab 500451 data sheet v1.4',
        'https://muxlab.com/wp-content/uploads/2019/05/DS-500451_v1.4.pdf', verified=True, w=4, formFactor='MuxLab extender',
        boxMm={'w': 111, 'h': 25}, powerW=pw)

# ======================= Kramer MegaTOOLS =======================
add('kramer-megatools.json', 'kramer-vm-2h2', 'Kramer', 'VM-2H2', 'VM-2H2 1:2 4K60 HDMI distribution amplifier', 'MegaTOOLS', 'converter', 1,
    [H('in', 1, 'HDMI In'), H('out', 2, 'HDMI Out'), R('io', 'RS-232', 'Terminal block 3-pin', 1, 'RS-232 (firmware)'), DC('5V DC', 'DC barrel')],
    '190 x 116 x 27 mm, 5 V 730 mA. Two fit side by side in the RK-T2B adapter.', 'Kramer VM-2H2 product page',
    'https://www1.kramerav.com/product/VM-2H2', verified=True, w=6, formFactor='Kramer half-rack', boxMm={'w': 190, 'h': 27})

# ======================= TASCAM =======================
TF, TC = 'tascam-more.json', 'TASCAM'
add(TF, 'tascam-cd-400u', TC, 'CD-400U', 'CD-400U CD / SD / USB player with Bluetooth and AM/FM tuner, 1RU', 'Media players', 'recorder', 1,
    [R('out', 'Analog audio', 'XLR3M', 2, 'Balanced Out'), R('out', 'Analog audio', 'RCA', 2, 'Unbal Out'), R('out', 'Analog audio', 'RCA', 2, 'Tuner Out'),
     R('io', 'RS-232', 'DB9', 1, 'RS-232C'), R('in', 'RF', 'F', 1, 'FM antenna'), R('in', 'RF', 'Other', 1, 'AM antenna'),
     F('in', 'Analog audio', '3.5mm', 1, 'Aux In'), F('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), F('io', 'USB', 'USB-A', 1, 'USB'), AC(1)],
    '482.6 x 45 x 300.5 mm, 3.3 kg, 20 W. Check: AC inlet type.', 'TASCAM CD-400U product page', 'https://tascam.com/us/product/cd-400u',
    verified=True, full=True, powerW=20, weightKg=3.3)
add(TF, 'tascam-ss-cdr250n', TC, 'SS-CDR250N', 'SS-CDR250N CD / memory recorder with network, 1RU', 'Recorders', 'recorder', 1,
    [R('in', 'Analog audio', 'XLR3F', 2, 'Balanced In'), R('out', 'Analog audio', 'XLR3M', 2, 'Balanced Out'), R('in', 'Analog audio', 'RCA', 2, 'Unbal In'),
     R('out', 'Analog audio', 'RCA', 2, 'Unbal Out'), R('in', 'Other', 'RCA', 1, 'S/PDIF coax In'), R('out', 'Other', 'RCA', 1, 'S/PDIF coax Out'),
     LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232C'), R('io', 'Other', 'DB25', 1, 'Parallel'), F('io', 'USB', 'USB-A', 1, 'USB'), AC(1)],
    'CD plus SD / USB / CF recording, FTP and Telnet control over the LAN port. Check: connectors (taken from the SS-R250N).',
    'TASCAM SS-CDR250N product page', 'https://tascam.com/us/product/ss-cdr250n', full=True)
add(TF, 'tascam-bd-mp4k', TC, 'BD-MP4K', 'BD-MP4K 4K UHD Blu-ray player, 1RU', 'Media players', 'recorder', 1,
    [H('out', 1, 'HDMI Out (main)'), H('out', 1, 'HDMI Out (sub / audio)'), R('out', 'Analog audio', 'XLR3M', 2, 'Balanced Out'),
     R('out', 'Analog audio', 'RCA', 2, 'Unbal Out'), R('out', 'Other', 'RCA', 1, 'S/PDIF coax Out'), R('out', 'Other', 'TOSLINK', 1, 'Optical Out'),
     LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232C'), F('io', 'USB', 'USB-A', 1, 'USB'), AC(1)],
    'Check: connectors.', 'TASCAM BD-MP4K product page', 'https://tascam.com/us/product/bd-mp4k', full=True)
add(TF, 'tascam-da-3000', TC, 'DA-3000', 'DA-3000 stereo master recorder / ADDA converter, 1RU', 'Recorders', 'recorder', 1,
    [R('in', 'Analog audio', 'XLR3F', 2, 'Balanced In'), R('out', 'Analog audio', 'XLR3M', 2, 'Balanced Out'), R('in', 'Analog audio', 'RCA', 2, 'Unbal In'),
     R('out', 'Analog audio', 'RCA', 2, 'Unbal Out'), R('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), R('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
     R('in', 'Other', 'RCA', 1, 'S/PDIF In'), R('out', 'Other', 'RCA', 1, 'S/PDIF Out'), R('in', 'Word clock', 'BNC', 1, 'Word clock In'),
     R('out', 'Word clock', 'BNC', 1, 'Word clock Out'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232C'), AC(1)],
    'DSD and PCM to 192 kHz on SD / CF. Check: connectors.', 'TASCAM DA-3000 product page', 'https://tascam.com/us/product/da-3000', full=True)
for pn, ch in (('ML-32D', 32), ('ML-16D', 16)):
    add(TF, 'tascam-' + pn.lower(), TC, pn, f'{pn} {ch}-channel analog / Dante interface, 1RU', 'Dante interfaces', 'audio', 1,
        [R('in', 'Analog audio', 'DB25 (8 ch)', ch // 8, 'Analog In (DB25)'), R('out', 'Analog audio', 'DB25 (8 ch)', ch // 8, 'Analog Out (DB25)'),
         R('io', 'Dante/AES67', 'RJ45', 1, 'Dante Primary'), R('io', 'Dante/AES67', 'RJ45', 1, 'Dante Secondary'), AC(1)],
        f'{ch} in / {ch} out on TASCAM-pinout DB25s. Check: word clock and AC inlet.', f'TASCAM {pn} product page',
        f'https://tascam.com/us/product/{pn.lower()}', full=True)

# ======================= VITEC =======================
VF, VT = 'vitec-more.json', 'VITEC'
ACE = {'w': 202, 'h': 43}
add(VF, 'vitec-mgw-ace-decoder', VT, 'MGW Ace Decoder', 'MGW Ace Decoder 4K HEVC / H.264 low-latency decoder', 'MGW Ace', 'converter', 1,
    [S12('out', 1, '12G-SDI Out'), S3('out', 1, 'SDI Out'), H('out', 1, 'HDMI 2.0 Out'), R('out', 'Analog video', 'BNC', 1, 'CVBS Out'),
     R('out', 'Analog audio', 'RCA', 2, 'Unbal audio Out'), R('out', 'Analog audio', 'XLR3M', 2, 'Balanced audio Out'), R('out', 'AES/EBU', 'BNC', 2, 'AES Out'),
     R('in', 'Other', 'BNC', 1, 'ASI In'), R('out', 'Other', 'BNC', 1, 'ASI Loop'), R('in', 'Analog audio', '3.5mm', 1, 'Talkback In'),
     R('out', 'Analog audio', '3.5mm', 1, 'Talkback Out'), LAN(2, 'GigE'), R('io', 'Other', 'Other', 1, 'Serial / audio / genlock'), DC('20-50V DC', 'DC locking')],
    '202 x 42.4 x 117.5 mm, 1.1 kg, 22 W typical. Optional 1RU rack kit; also made as an openGear card. Check: connector types.',
    'VITEC MGW Ace Decoder data sheet', 'https://vitec.com/dl/mgw-ace-decoder-datasheet', verified=True, w=6,
    formFactor='VITEC MGW Ace', boxMm=ACE, powerW=22, weightKg=1.1)
add(VF, 'vitec-mgw-ace-encoder', VT, 'MGW Ace Encoder', 'MGW Ace Encoder HEVC / H.264 low-latency encoder', 'MGW Ace', 'converter', 2,
    [S3('in', 1, 'SDI In'), H('in', 1, 'HDMI In'), R('in', 'DVI', 'DVI-D', 1, 'DVI-D In'), R('in', 'Analog video', 'BNC', 1, 'CVBS In'),
     R('in', 'Analog audio', 'XLR3F', 2, 'Balanced audio In'), R('in', 'Analog audio', 'RCA', 2, 'Unbal audio In'), R('out', 'Analog audio', 'RCA', 1, 'Talkback Out'),
     S3('out', 1, 'SDI Out'), R('out', 'Other', 'BNC', 1, 'ASI Out'), LAN(2, 'GigE'), R('io', 'Other', 'Other', 1, 'Serial / audio breakout'),
     DC('20-50V DC', 'DC locking')],
    '196 x 65 x 199 mm, so it takes 2RU of space on a shelf; rack shelf kit 16858. Check: connector types.',
    'VITEC MGW Ace Encoder data sheet', 'https://avlgear.com/products/vitec-mgw-ace-compact-hevc-h-265-hardware-encoder',
    verified=True, w=6, formFactor='VITEC MGW Ace', boxMm={'w': 196, 'h': 65})
add(VF, 'vitec-16858', VT, '16858', 'MGW portable appliance rack shelf kit (2 units)', 'MGW Ace', 'shelf', 2,
    [], 'Holds two MGW Ace encoders or decoders side by side. Check: rack height (listed as 1.5RU, so allow 2RU) and count.',
    'Adorama 16858 listing', 'https://www.adorama.com/vi16858.html', carrier={'bays': 2, 'fits': ['VITEC MGW Ace']})

# ======================= Magewell =======================
add('magewell.json', 'magewell-ultra-encode-aio', 'Magewell', 'Ultra Encode AIO', 'Ultra Encode AIO SDI / HDMI streaming encoder, half-rack 1RU',
    'Ultra Encode', 'converter', 1,
    [R('in', '6G-SDI', 'BNC', 1, 'SDI In'), R('out', '6G-SDI', 'BNC', 1, 'SDI Loop'), H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Loop'),
     R('in', 'Analog audio', '3.5mm', 1, 'Line In'), R('out', 'Analog audio', '3.5mm', 1, 'Line Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE+)'),
     R('io', 'USB', 'USB-C', 1, 'USB-C (config)'), R('io', 'USB', 'USB-A', 2, 'USB'), DC('9-18V DC', 'DC locking')],
    '214.9 x 128.2 x 44.6 mm, 11.5 W max. Ships with rack ears for 1RU (one unit, or two side by side). Also has an SD card slot and Wi-Fi.',
    'Magewell Ultra Encode AIO tech specs', 'https://www.magewell.com/tech-specs/ultra-encode-aio', verified=True, w=6, powerW=11.5)

# ======================= Matrox =======================
add('matrox-more.json', 'matrox-monarch-edge-d4', 'Matrox', 'Monarch EDGE D4', 'Monarch EDGE D4 4-channel decoder, half-rack 1RU', 'Monarch EDGE',
    'converter', 1,
    [R('out', 'SDI', 'BNC', 4, 'SDI Out'), REF(1, 'Genlock'), LAN(2, 'Network'), AC(1)],
    'Decode partner of the Monarch EDGE E4 (4 x HD or 1 x 4K). Check: ports (taken from the E4).', 'Matrox Monarch EDGE tech specs',
    'https://video.matrox.com/en/products/encoders-decoders/monarch-edge-series/monarch-edge-tech-specs', w=6)

# ======================= Panasonic =======================
PF, PA = 'panasonic-more.json', 'Panasonic'
add(PF, 'panasonic-at-kc200l1', PA, 'AT-KC200L1', 'KAIROS Core 200L1 live production mainframe, 4RU', 'KAIROS', 'switcher', 4,
    [R('in', '3G-SDI', 'HD-BNC', 24, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', 12, 'SDI Out'), R('in', 'Reference', 'HD-BNC', 6, 'Ref'),
     R('out', 'DisplayPort', 'DisplayPort', 4, 'Multiview'), R('io', 'Other', 'Card slot', 1, 'Option board slot'), LAN(2),
     R('io', 'USB', 'USB-A', 4, 'USB (system)'), R('out', 'VGA', 'HD15', 1, 'VGA (system)'), AC(2, 'AC In (redundant)')],
    '430 x 176 x 505 mm, about 17.8 kg. Three SDI boards fitted (24 in / 12 out 3G, or 12 in / 6 out 4K), up to 32 / 16 with the fourth board; '
    'optional ST 2110 board with 2 x 100G QSFP28. Controlled from the KAIROS panels or software.', 'Panasonic KAIROS specifications page',
    'https://pro-av.panasonic.net/en/products/it_ip_platform/spec.html', verified=True, full=True, weightKg=17.8)
add(PF, 'panasonic-ak-ucu600', PA, 'AK-UCU600', 'AK-UCU600 4K camera control unit, 2RU', 'Studio cameras', 'converter', 2,
    [R('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'Camera'), S12('out', 2, '12G-SDI Out'), S3('out', 5, 'SDI Out'), R('out', 'HD-SDI', 'BNC', 1, 'Monitor Out'),
     R('out', 'Analog video', 'BNC', 2, 'CVBS Out'), R('out', 'HD-SDI', 'BNC', 1, 'Trunk Out'), S3('out', 1, 'TICO Out'), S3('in', 4, 'Return In'),
     R('in', 'Analog video', 'BNC', 1, 'Return CVBS In'), R('in', 'HD-SDI', 'BNC', 1, 'Prompter In'), R('in', 'Analog video', 'BNC', 2, 'Prompter CVBS In'),
     REF(), R('out', 'Analog audio', 'XLR3M', 2, 'Mic Out'), R('io', 'Intercom', 'Other', 2, 'Intercom'), R('in', 'Analog audio', 'XLR3F', 2, 'PGM In'),
     R('in', 'Other', 'Other', 1, 'Tally'), R('io', 'RS-422', 'Other', 2, 'Trunk data'), R('io', 'RS-422', 'Other', 1, 'ROP'),
     R('io', 'RS-422', 'Other', 1, 'MSU'), LAN(1), AC(1)],
    '424 x 88 x 401 mm, 8.9 kg, 500 W with camera (90 W without); powers the camera head over the fibre. Check: intercom, tally and control connector types.',
    'Panasonic AK-UCU600 product page', 'https://pro-av.panasonic.net/en/products/ak-ucu600/', verified=True, full=True, powerW=500, weightKg=8.9)

# ======================= Sony =======================
add('sony-bpu.json', 'sony-bpu-4800', 'Sony', 'BPU-4800', 'BPU-4800 4K / HFR baseband processor unit (HDC-4800), 3RU', 'Camera systems', 'converter', 3,
    [R('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'Camera'), R('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'CCU'), R('io', 'Other', 'Other', 1, 'Remote (RCP / CNU)'),
     R('io', 'Other', 'RJ45', 1, 'Remote'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('io', 'SFP', 'SFP+', 2, 'Share play'),
     R('io', 'SFP', 'SFP+', 2, 'NMI-LAN'), R('io', 'GPIO', 'DB25', 1, 'GPIO'), R('in', 'HD-SDI', 'BNC', 2, 'SDI In'), REF(), R('out', 'Reference', 'BNC', 1, 'Ref Out'),
     R('in', 'Timecode', 'BNC', 1, 'TC In'), R('out', 'Timecode', 'BNC', 1, 'TC Out'), R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out'),
     S3('out', 8, 'Live Out (slot 1)'), S3('out', 8, 'Replay Out (slot 1)'), S3('out', 2, 'Replay Out (slot 2)'), R('out', 'HD-SDI', 'BNC', 2, 'Live / Replay Out (slot 3)'),
     R('io', 'USB', 'USB-A', 1, 'Maintenance'), AC(2, 'AC In')],
    '424 x 132 x 410 mm, about 16.5 kg, 4.5 A max. Records and replays the HDC-4800 high frame rate feed. Outputs depend on the fitted boards.',
    'Sony BPU-4800 specifications', 'https://pro.sony/ue_US/pdf/bpu-4800', verified=True, full=True, weightKg=16.5)

# ======================= Vizrt =======================
add('vizrt-more.json', 'vizrt-3play-3p2', 'Vizrt (NewTek)', '3Play 3P2', '3Play 3P2 replay system, 2RU', '3Play', 'recorder', 2,
    [S3('in', 4, 'SDI In'), S3('out', 4, 'SDI Out (A / B or quad-link)'), REF(1, 'Genlock'), R('io', 'Ethernet', 'RJ45', 1, '10GbE'), LAN(1, '1GbE'),
     R('in', 'Analog audio', 'XLR3F', 2, 'XLR In'), R('in', 'Analog audio', '1/4" TRS', 6, 'Line In'), R('out', 'Analog audio', 'XLR3M', 2, 'XLR Out'),
     R('out', 'Analog audio', '1/4" TRS', 2, 'Line Out'), R('out', 'DVI', 'DVI-D', 1, 'UI'), H('out', 1, 'Multiview'), R('out', 'DisplayPort', 'DisplayPort', 1, 'Multiview'),
     F('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), AC(1)],
    '483 x 89 x 497 mm, 12 kg, one 400 W PSU. 8 inputs (4 SDI + NDI), 2 outputs. Pairs with the 3P1 control surface. Discontinued. Check: headphone location.',
    'Markertek 3Play 3P2 listing', 'https://www.markertek.com/product/tri-3p22ru/vizrt-3play-3p2-10-channel-instant-sports-replay-production-system-with-ndi-3g-sdi',
    verified=True, full=True, powerW=400, weightKg=12)

# ======================= Epiphan =======================
add('epiphan-more.json', 'epiphan-pearl-nexus', 'Epiphan', 'Pearl Nexus', 'Pearl Nexus 1RU encoder / switcher / recorder', 'Pearl', 'switcher', 1,
    [H('in', 2, 'HDMI In'), R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('io', 'USB', 'USB-A', 2, 'USB video In'), R('io', 'USB', 'USB-A', 2, 'USB audio'),
     H('out', 1, 'HDMI Out'), R('in', 'Analog audio', 'XLR/TRS combo', 2, 'XLR / TRS In'), R('in', 'Analog audio', 'RCA', 2, 'RCA In'),
     R('in', 'Analog audio', '3.5mm', 1, 'Mic In'), LAN(1, 'LAN (Dante audio)'), F('io', 'USB', 'USB-A', 1, 'USB'), F('out', 'Analog audio', '3.5mm', 1, 'Phones'),
     DC('12V DC', 'DC locking')],
    '483 x 190 x 43 mm with ears, 2.4 kg, external 60 W supply (84 W option).', 'Epiphan Pearl Nexus tech specs',
    'https://www.epiphan.com/products/pearl-nexus/tech-specs/', verified=True, full=True, weightKg=2.4)

# ======================= RGBlink =======================
add('rgblink.json', 'rgblink-flex-8', 'RGBlink', 'FLEX 8', 'FLEX 8 modular 8x8 switcher / scaler, 1RU', 'FLEX', 'switcher', 1,
    [R('in', 'Other', 'Card slot', 2, 'Input module slot'), R('out', 'Other', 'Card slot', 2, 'Output module slot'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232'),
     AC(1)],
    'Up to 8 inputs and 8 outputs on plug-in modules (SDI, HDMI, DVI, DisplayPort, HDBaseT, USB). 484 x 463 x 45 mm, 2.5 kg, 200 W max. '
    'Add the fitted modules to the notes. Check: modules per slot.', 'RGBlink FLEX 8 specification V1.1',
    'https://cdn.shopify.com/s/files/1/0150/7190/3844/files/FLEX_8_Specification_EN_V1.1_20190416.pdf', verified=True, full=True, powerW=200, weightKg=2.5)

# ======================= Vaddio =======================
add('vaddio.json', 'vaddio-av-bridge-mini', 'Vaddio', '999-8240-000', 'AV Bridge Mini HDMI / audio to USB and IP encoder, half-rack', 'AV Bridge',
    'converter', 1,
    [H('in', 1, 'HDMI In'), R('io', 'USB', 'USB-B', 1, 'USB 3.0'), R('in', 'Analog audio', 'Terminal block', 2, 'Mic / line In'),
     R('out', 'Analog audio', 'Terminal block', 2, 'Line Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), R('io', 'RS-232', 'RJ45', 1, 'RS-232')],
    '213 x 44 x 152 mm, powered by PoE (802.3af, injector included). Ships with a 1RU rack kit. Check: audio connector type.',
    'Vaddio AV Bridge Mini specifications', 'https://www.markertek.com/Attachments/Specifications/Vaddio/999-8240-000-Specifications.pdf', verified=True, w=6)

# ======================= write =======================
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
allids = set()
for f in idx:
    if f in FILES: continue
    try: allids |= {m['id'] for m in json.load(open(os.path.join(CAT, f)))}
    except Exception: pass
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), (f, [i for i in ids if ids.count(i) > 1])
    dup = allids & set(ids)
    if dup: print('  skipped, already in another file:', sorted(dup)); ms[:] = [m for m in ms if m['id'] not in dup]
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    print(f, len(ms))
idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
