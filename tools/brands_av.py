#!/usr/bin/env python3
"""AV and broadcast brands batch 1 (added 2026-11-15): rack-mount ranges, plus desktop units that live on rack kits/shelves.
  osprey-talon.json   Osprey Video Talon encoders / decoders and the 1U three-unit rack kit.
  lumantek.json       Lumantek ez-Rack, ez-Converter range, ez-Distributor.
  avpro-edge.json     AVPro Edge HDMI / HDBaseT matrices, DAs and MXnet rack kits.
  kanexpro.json       KanexPro HDMI / HDBaseT matrices.
  avmatrix.json       AVMatrix 1RU SDI matrices, multiviewer and DA.
  decimator-more.json Decimator Design desktop converters and multiviewers (decimator.json has the DMON-16S).
  theatrixx.json      Theatrixx xVision reversible module frames (XVVRF2 / XVVRF8) and modules (as cards, system 'xVision').
  muxlab.json         MuxLab matrices and extender rack chassis.
  orei.json           OREI HDMI matrices (rack-mountable models).
  gefen.json          Gefen matrices, seamless / multiview switchers, wall controllers, half-rack extenders and EXT-RACK-1U-GRY.
  kramer-more.json    Kramer matrices, scalers, DAs, multiviewers, amplifiers, DSP and rack adapters (kramer.json has the VS-88H2).
Desktop units that go on a rack kit carry `formFactor` and `boxMm`; kits carry `carrier {bays, fits}`.
Specs from maker or dealer pages (each entry's source). 'Check:' marks anything unconfirmed; verified=false unless the
ports came from a spec sheet."""
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
DC = lambda v='12V DC', c='DC locking': R('in', 'Power', c, 1, v)
LAN = lambda n=1, p='LAN': R('io', 'Ethernet', 'RJ45', n, p)
RS232 = lambda c='DB9': R('io', 'RS-232', c, 1, 'RS-232')
IR = R('in', 'Other', '3.5mm', 1, 'IR In')
def hdmi_mx(i, o, extra=(), hdbt=0, hdmi_out=None):
    ports = [R('in', 'HDMI', 'HDMI', i, 'HDMI In')]
    ho = o - hdbt if hdmi_out is None else hdmi_out
    if ho: ports.append(R('out', 'HDMI', 'HDMI', ho, 'HDMI Out'))
    if hdbt: ports.append(R('out', 'Ethernet', 'RJ45', hdbt, 'HDBaseT Out'))
    return ports + list(extra)

# ======================= Osprey Video Talon =======================
OF, OS = 'osprey-talon.json', 'Osprey Video'
TU = 'https://www.markertek.com/brand/osprey-video'
TALON_BOX = {'w': 140, 'h': 38}
def talon(id, pn, name, ports, notes, verified=False, src='Osprey Talon dealer listings', url=TU):
    add(OF, 'osprey-' + id, OS, pn, name, 'Talon', 'converter', 1, ports, notes, src, url, verified=verified, w=4,
        formFactor='Osprey Talon', boxMm=TALON_BOX)
talon('talon-4k-sc', 'Talon 4K-SC', 'Talon 4K-SC 4K60 12G-SDI / HDMI H.265 / H.264 encoder',
      [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Loop'), R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'),
       LAN(1, 'GigE'), R('io', 'USB', 'USB-A', 1, 'USB 2.0 (record)'), DC('12V DC (24 W)')],
      'Desktop streaming encoder, 140 x 140 x 38 mm, 12 V 24 W, 16 ch audio from SDI. Up to three in the 1U Talon rack kit.',
      verified=True, src='Osprey Talon 4K-SC data sheet (2022)', url='https://cdw.jbanda.com/wp-content/uploads/Talon_4K_SC_070222.pdf')
talon('talon-uhd-sc', 'Talon UHD-SC', 'Talon UHD-SC 4K 12G-SDI 10-bit 4:2:2 encoder',
      [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Loop'), LAN(1, 'GigE'), R('io', 'USB', 'USB-A', 1, 'USB'), DC()],
      '10-bit 4:2:2 HEVC contribution encoder, 16 audio channels. Check: rear connectors.')
talon('talon-g1', 'Talon G1', 'Talon G1 HD H.264 encoder',
      [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), LAN(1, 'GigE'), DC()], 'HD encoder. Check: rear connectors.')
talon('talon-4k-scd', 'Talon 4K-SCD', 'Talon 4K-SCD 4K decoder with genlock',
      [LAN(1, 'GigE'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'), DC()],
      'Decoder partner for Talon encoders (NG version has HD-BNC). Check: rear connectors.')
talon('talon-uhd-scd', 'Talon UHD-SCD', 'Talon UHD-SCD 12G-SDI decoder',
      [LAN(1, 'GigE'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'), DC()], 'Check: rear connectors.')
add(OF, 'osprey-talon-rack-kit', OS, 'Talon Rackmount Kit', 'Talon 1U rackmount kit for three Talon units', 'Talon', 'shelf', 1,
    [AC(2, 'AC In A/B')], '1U kit with active cooling and redundant power for up to three Talon encoders / decoders (some listings say two).',
    'Osprey Talon 4K-SC data sheet (2022)', TU, carrier={'bays': 3, 'fits': ['Osprey Talon']})

# ======================= Lumantek =======================
LF, LM = 'lumantek.json', 'Lumantek'
LU = 'https://muzeekworld.com/collections/lumantek'
EZ_BOX = {'w': 75, 'h': 25}
def ez(id, pn, name, ports, notes):
    add(LF, 'lumantek-' + id, LM, pn, name, 'ez-Converter', 'converter', 1, ports + [DC('12V DC')], notes + ' Check: connectors.',
        'Lumantek dealer listings', LU, w=2, formFactor='Lumantek ez-Converter', boxMm=EZ_BOX)
ez('ez-sh', 'ez-Converter SH', 'ez-Converter SH 3G-SDI to HDMI converter', [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')], 'Mini converter.')
ez('ez-hs', 'ez-Converter HS', 'ez-Converter HS HDMI to dual 3G-SDI converter', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')], 'Mini converter with two SDI outputs.')
ez('ez-hs-plus', 'ez-Converter HS+', 'ez-Converter HS+ HDMI / VGA to 3G-SDI scaler', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('in', 'VGA', 'HD15', 1, 'VGA In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')], 'Scaling converter.')
ez('ez-shv-plus', 'ez-SHV+', 'ez-SHV+ SDI to HDMI converter with display and scaler', [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')], 'Converter with small screen.')
ez('ez-hsv-plus', 'ez-HSV+', 'ez-HSV+ HDMI to SDI converter with display and scaler', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Loop'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')], 'Converter with small screen.')
ez('ez-md-plus', 'ez-MD+', 'ez-MD+ HDMI / SDI cross converter with audio mux / demux', [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'Analog audio', '3.5mm', 2, 'Audio In/Out')], 'Cross converter with analogue audio embed / de-embed.')
add(LF, 'lumantek-ez-rack', LM, 'LUM-RACK', 'ez-Rack 1RU rack mount for up to ten ez-Converters', 'ez-Converter', 'shelf', 1, [],
    'Rack frame for up to ten Mini / ez-Converter units. Check: rack height.', 'Lumantek dealer listings', 'https://muzeekworld.com/products/lumantek-lum-rack-converter-rack-mount',
    carrier={'bays': 10, 'fits': ['Lumantek ez-Converter']})
add(LF, 'lumantek-ez-distributor', LM, 'ez-Distributor', 'ez-Distributor 3G-SDI distribution amplifier with LCD', 'ez-Pro', 'converter', 1,
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), DC()],
    'Half-rack DA with status LCD. Check: output count and width.', 'B&H listing', 'https://www.bhphotovideo.com/c/product/1430634-REG/lumantek_lum_ez_distributor_distribution_amplifier_with_lcd.html', w=6)
add(LF, 'lumantek-ez-pro-vs10', LM, 'ez-Pro VS10', 'ez-Pro VS10 10x1 3G-SDI / HDMI switcher (desktop console)', 'ez-Pro', 'switcher', 3,
    [R('in', '3G-SDI', 'BNC', 6, 'SDI In'), R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'PGM Out'), R('out', 'HDMI', 'HDMI', 2, 'PGM / MV Out'), LAN(1), DC()],
    'Console-style switcher; sits on a shelf. Check: input split and outputs.', 'Lumantek dealer listings', LU)

# ======================= AVPro Edge =======================
AF, AV = 'avpro-edge.json', 'AVPro Edge'
AU = lambda s: 'https://www.avproedge.com/' + s
AS = 'AVPro Edge matrix switcher list (2025)'
CTL = [LAN(1, 'LAN control'), RS232('Terminal block 3-pin'), IR]
def avm(pn, name, i, o, ru, hdbt=0, extra=(), notes='', w=12, ver=False):
    add(AF, 'avpro-' + pn.lower(), AV, pn, name, 'Matrix', 'router', ru,
        hdmi_mx(i, o, [R('out', 'Analog audio', 'Terminal block', o, 'Audio De-embed Out')] + list(extra) + CTL + [AC()], hdbt=hdbt),
        (notes + ' ' if notes else '') + 'Check: rack height and audio / control connectors.', AS, AU(pn.lower()), verified=ver, w=w)
avm('AC-MX-88X', 'AC-MX-88X 8x8 40 Gbps 8K HDMI matrix', 8, 8, 1)
avm('AC-MX-44X', 'AC-MX-44X 4x4 48 Gbps 8K HDMI matrix', 4, 4, 1)
avm('AC-MX-42X', 'AC-MX-42X 4x2 40 Gbps 8K HDMI matrix', 4, 2, 1, w=6)
avm('AC-MX-88', 'AC-MX-88 8x8 18 Gbps HDMI matrix with audio de-embed and scalers', 8, 8, 1)
avm('AC-MX-44', 'AC-MX-44 4x4 18 Gbps HDMI matrix', 4, 4, 1)
avm('AC-MX-1616', 'AC-MX-1616 16x16 18 Gbps HDMI matrix', 16, 16, 2)
avm('AC-MX-82RM', 'AC-MX-82RM 8x2 18 Gbps HDMI matrix', 8, 2, 1)
avm('AC-MX-44HDBT', 'AC-MX-44HDBT 4x4 HDMI / HDBaseT matrix', 4, 8, 1, hdbt=4, notes='Mirrored HDMI and HDBaseT outputs.')
avm('AC-MX-88HDBT', 'AC-MX-88HDBT 8x8 HDMI / HDBaseT matrix', 8, 16, 2, hdbt=8, notes='Mirrored HDMI and HDBaseT outputs.')
avm('AC-CX-84', 'AC-CX-84 8x4 HDMI / HDBaseT matrix', 8, 8, 1, hdbt=4, notes='Mirrored HDMI and HDBaseT outputs.')
for pn, n in (('AC-DA18-AUHD-GEN2', 8), ('AC-DA-18X2', 8)):
    add(AF, 'avpro-' + pn.lower(), AV, pn, f'{pn} 1x{n} HDMI distribution amplifier', 'DA', 'converter', 1,
        [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', n, 'HDMI Out'), LAN(1), RS232('Terminal block 3-pin'), DC()],
        'Check: rack height and control ports.', AS, AU(pn.lower()))
add(AF, 'avpro-ac-mxnet-1g-r15', AV, 'AC-MXNET-1G-R15', 'MXnet 1G 15-slot rack mount kit', 'MXnet', 'shelf', 2, [AC(2)],
    'Rack chassis for up to 15 MXnet 1G encoders / decoders, powered centrally. Check: rack height and power.', AS, AU('ac-mxnet-1g-r15'),
    carrier={'bays': 15, 'fits': ['AVPro MXnet card']})
add(AF, 'avpro-ac-ezrack-15', AV, 'AC-EZRACK-15-TAA', 'EZ Rack 15-slot extender rack mount', 'Extenders', 'shelf', 2, [AC(1)],
    'Rack chassis for up to 15 AVPro extenders. Check: rack height.', AS, AU('ac-ezrack-15-taa'), carrier={'bays': 15, 'fits': ['AVPro extender']})

# ======================= KanexPro =======================
KF, KP = 'kanexpro.json', 'KanexPro'
add(KF, 'kanexpro-mx-hdbt8x818g', KP, 'MX-HDBT8X818G', 'MX-HDBT8X818G 4K60 8x8 HDBaseT matrix with audio matrix', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out (local)'), R('out', 'Ethernet', 'RJ45', 6, 'HDBaseT Out'),
     R('in', 'Analog audio', '3.5mm', 2, 'Analog Audio In'), R('in', 'Other', 'Toslink', 2, 'S/PDIF Optical In'), R('in', 'Other', 'RCA', 2, 'S/PDIF Coax In'),
     R('out', 'Analog audio', '3.5mm', 6, 'Analog Audio Out'), R('out', 'Other', 'Toslink', 6, 'S/PDIF Optical Out'),
     R('in', 'Other', '3.5mm', 8, 'IR In'), R('out', 'Other', '3.5mm', 7, 'IR Out'), R('io', 'RS-232', 'Terminal block 3-pin', 4, 'RS-232'),
     LAN(1, 'TCP/IP'), R('io', 'USB', 'Micro-USB', 1, 'Firmware'), R('in', 'Power', 'DC locking', 1, 'DC In (60 W)')],
    '1U steel 19-inch enclosure; external 100-240 V supply.', 'KanexPro MX-HDBT8X818G data sheet', 'https://files.hdtvsupply.com/brand/kanexpro/kanexpro-mx-hdbt8x818g-ds.pdf', verified=True)
add(KF, 'kanexpro-hdmx88-18g', KP, 'HDMX88-18G', 'HDMX88-18G 4K 8x8 HDMI matrix', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), R('out', 'Other', 'RCA', 8, 'S/PDIF Out'), R('io', 'RS-232', 'DB9', 1, 'RS-232'),
     LAN(1, 'Ethernet'), R('io', 'USB', 'Micro-USB', 1, 'Firmware'), R('in', 'Power', 'DC locking', 1, '24V DC')],
    '1U 19-inch, 44 mm high.', 'KanexPro HDMX88-4K specifications', 'https://www.markertek.com/Attachments/Specifications/Kanexpro/HDMX88-18G-Specifications.pdf', verified=True)
for pn, n, reach in (('MMX-4X4CAT-150M', 4, '150 m'), ('MMX-8X8CAT-70M', 8, '70 m')):
    add(KF, 'kanexpro-' + pn.lower(), KP, pn, f'{pn} {n}x{n} 4K60 HDBaseT matrix ({reach} CAT extension)', 'Matrix', 'router', 1,
        [R('in', 'HDMI', 'HDMI', n, 'HDMI In'), R('out', 'Ethernet', 'RJ45', n, 'HDBaseT Out'), R('out', 'HDMI', 'HDMI', n, 'HDMI Out (mirror)'),
         R('out', 'Analog audio', 'Terminal block', n, 'Audio Out'), RS232(), LAN(1), IR, AC()],
        'Matrix sold with HDBaseT receivers. Check: rack height, mirrored HDMI outputs and power.', 'KanexPro dealer listings',
        'https://www.markertek.com/product/kan-mmx4x4cat150/kanexpro-mmx-4x4cat-150m-4x4-4k60-hdbaset-matrix-switcher-with-cat-extension-up-to-492-feet')
add(KF, 'kanexpro-hdbase8x8', KP, 'HDBASE8X8', 'HDBASE8X8 4K HDBaseT 8x8 matrix with PoE', 'Matrix', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'Ethernet', 'RJ45', 8, 'HDBaseT Out (PoE)'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), RS232(), LAN(1), IR, AC()],
    'Check: rack height and outputs.', 'KanexPro dealer listings', 'https://www.adorama.com/kanexpro-4k-hdbaset-8-x-8-matrix-switcher-poe/p/kphdbase8x8')

# ======================= AVMatrix =======================
XF, XM = 'avmatrix.json', 'AVMatrix'
add(XF, 'avmatrix-mmv1630', XM, 'MMV1630', 'MMV1630 16-channel 3G-SDI multiviewer and switcher, 1RU', 'Multiviewer', 'monitor', 1,
    [R('in', '3G-SDI', 'BNC', 16, 'SDI In'), R('out', '3G-SDI', 'BNC', 16, 'SDI Loop'), R('out', '3G-SDI', 'BNC', 2, 'MV / PGM Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
     LAN(1), R('io', 'RS-422', 'Other', 1, 'RS-422 (reserved)'), R('in', 'Power', 'DC locking', 2, 'PS-1 / PS-2 12-20V DC')],
    '16 inputs as multiviewer or 16x2 switcher; 2.2-inch front LCD; 483 x 44 x 149 mm, 2 kg, 36 W. Check: RS-422 connector.',
    'Omega Broadcast MMV1630 listing', 'https://omegabroadcast.com/av-matrix-mmv1630-16-channel-3g-sdi-multiviewer-and-routing-switcher-1-ru', verified=True, powerW=36, weightKg=2)
add(XF, 'avmatrix-mss1611', XM, 'MSS1611', 'MSS1611 16x16 seamless 3G-SDI matrix, 1RU', 'Matrix', 'router', 1,
    [R('in', '3G-SDI', 'BNC', 16, 'SDI In'), R('out', '3G-SDI', 'BNC', 16, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), LAN(1), R('io', 'RS-422', 'Other', 1, 'RS-422'),
     R('in', 'Power', 'DC locking', 2, 'DC In A/B')], 'Seamless frame-synced 16x16. Check: reference and power connectors.',
    'AVMatrix dealer listings', 'https://www.rubbermonkey.co.nz/AV-Matrix-1RU-16x16-Seamless-3G-SDI-Matrix-Switcher')
add(XF, 'avmatrix-mss0811', XM, 'MSS0811', 'MSS0811 8x8 3G-SDI matrix', 'Matrix', 'router', 1,
    [R('in', '3G-SDI', 'BNC', 8, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out'), LAN(1), R('in', 'Power', 'DC locking', 1, 'DC In')],
    'Check: rack height (may be half rack) and connectors.', 'AVMatrix dealer listings', 'https://focuscamera.com/products/lilliput-mss0811-video-accessories-signal-video-management', w=6)
add(XF, 'avmatrix-sd1191', XM, 'SD1191', 'SD1191 1x9 3G-SDI distribution amplifier', 'DA', 'converter', 1,
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 9, 'SDI Out'), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Small metal DA; sits on a shelf. Check: size.', 'Adorama AVMatrix listing', 'https://www.adorama.com/brands/AVMatrix', w=4, boxMm={'w': 160, 'h': 30})
add(XF, 'avmatrix-mv0430', XM, 'MV0430', 'MV0430 3G-SDI quad-split multiviewer', 'Multiviewer', 'monitor', 1,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Loop'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
     R('in', 'Power', 'DC locking', 1, '12V DC')], 'Desktop quad split; sits on a shelf. Check: connectors.', 'Adorama AVMatrix listing', 'https://www.adorama.com/brands/AVMatrix',
    w=4, boxMm={'w': 160, 'h': 30})
add(XF, 'avmatrix-se1117', XM, 'SE1117', 'SE1117 SDI H.265 / H.264 streaming encoder', 'Streaming', 'converter', 1,
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), LAN(1), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Small encoder box; sits on a shelf.', 'Adorama AVMatrix listing', 'https://www.adorama.com/brands/AVMatrix', w=2, boxMm={'w': 100, 'h': 25})

# ======================= Decimator Design =======================
DF, DD = 'decimator-more.json', 'Decimator Design'
DU = 'https://www.adorama.com/brands/Decimator'
def dec(id, pn, name, fam, cat, ports, notes, box, w=3):
    add(DF, 'dec-' + id, DD, pn, name, fam, cat, 1, ports + [R('in', 'Power', 'DC locking', 1, '5-32V DC')], notes + ' Check: connectors.',
        'Decimator Design dealer listings', DU, w=w, boxMm=box, formFactor='Decimator ' + ('DMON' if fam == 'DMON' else 'MD'))
MD_BOX = {'w': 104, 'h': 25}
dec('md-hx', 'MD-HX', 'MD-HX HDMI / SDI cross converter with scaler', 'MD', 'converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
    'Miniature cross converter with up/down/cross scaling and frame-rate conversion.', MD_BOX)
dec('md-lx', 'MD-LX', 'MD-LX HDMI / SDI bi-directional converter', 'MD', 'converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
    'Non-scaling cross converter.', MD_BOX)
dec('md-cross-v2', 'MD-CROSS V2', 'MD-CROSS V2 HDMI / SDI cross converter with scaler', 'MD', 'converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
    'Cross converter with scaling.', MD_BOX)
dec('md-ducc', 'MD-DUCC', 'MD-DUCC 3G/HD/SD-SDI up/down/cross converter', 'MD', 'converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')], 'SDI-only up/down/cross converter.', MD_BOX)
dec('12g-cross', '12G-CROSS', '12G-CROSS 12G-SDI / HDMI 2.0 cross converter with scaler', 'MD', 'converter',
    [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB-C', 1, 'USB')],
    '12G cross converter with scaling.', {'w': 136, 'h': 29})
DM_BOX = {'w': 220, 'h': 29.5}
dec('dmon-quad', 'DMON-QUAD', 'DMON-QUAD 4-channel multiviewer', 'DMON', 'monitor',
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Loop'), R('out', '3G-SDI', 'BNC', 1, 'MV SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'MV HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
    'Quad split multiviewer with SDI loop-throughs.', {'w': 104, 'h': 25})
dec('dmon-4s', 'DMON-4S', 'DMON-4S 4-channel multiviewer', 'DMON', 'monitor',
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'MV SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'MV HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
    '4-input multiviewer.', {'w': 104, 'h': 25})
for n in (6, 12):
    dec(f'dmon-{n}s', f'DMON-{n}S', f'DMON-{n}S {n}-channel multiviewer', 'DMON', 'monitor',
        [R('in', '3G-SDI', 'BNC', n, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'MV SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'MV HDMI Out'), R('io', 'USB', 'USB mini-B', 1, 'USB')],
        f'{n}-input multiviewer; same case as the DMON-16S (two per rack shelf).', DM_BOX, w=6)

# ======================= Theatrixx xVision =======================
TF, TX = 'theatrixx.json', 'Theatrixx'
TS = 'Theatrixx xVision dealer listings (Markertek, Leisuretec)'
TUR = 'https://www.markertek.com/product/ttx-xvvrf8/theatrixx-xvvrf8-8-bay-reversible-converter-empty-frame-with-dual-psus-3ru'
add(TF, 'theatrixx-xvvrf8', TX, 'XVVRF8', 'xVision RF8 8-bay reversible converter frame, dual PSU, 3RU', 'xVision', 'frame', 3,
    [R('in', 'Power', 'powerCON TRUE1', 2, 'Mains In A/B')],
    '8 bays for xVision reversible modules (each can face front or rear), two hot-backup PSUs with front status LEDs. 483 x 132 x 178 mm, '
    '5 kg empty, 200 W max per input.', 'Theatrixx XVVRF8 (Markertek listing)', TUR, verified=True,
    frame={'system': 'xVision', 'slots': 8, 'slotOrder': 'ltr', 'rearAlign': 1, 'door': False, 'controller': 'none (passive frame)',
           'front': {'x0': 0.06, 'x1': 0.94, 'y0': 0.05, 'y1': 0.95}, 'rear': {'x0': 0.06, 'x1': 0.94, 'y0': 0.05, 'y1': 0.95}})
add(TF, 'theatrixx-xvvrf2', TX, 'XVVRF2', 'xVision RF2 2-bay reversible converter frame, 1RU', 'xVision', 'frame', 1,
    [R('in', 'Power', 'powerCON TRUE1', 2, 'Mains In A/B')],
    'Two modules side by side, lying flat. Sold with one or two PSUs. Check: power connectors on the single-PSU version.', TS,
    'https://www.leisuretec.co.uk/product/xvision-reversible-2bay-video-converter-frame-with-dual-psus-1u-webthe00098',
    frame={'system': 'xVision', 'slots': 2, 'slotOrder': 'ltr', 'rearAlign': 1, 'door': False, 'orient': 'h', 'cols': 2, 'controller': 'none (passive frame)',
           'front': {'x0': 0.06, 'x1': 0.94, 'y0': 0.08, 'y1': 0.92}, 'rear': {'x0': 0.06, 'x1': 0.94, 'y0': 0.08, 'y1': 0.92}})
def xm(pn, name, ports, notes=''):
    add(TF, 'theatrixx-' + pn.lower().replace('ttx-', ''), TX, pn, name, 'xVision module', 'card', 0, [],
        'Reversible module: mounts facing the front or rear of the frame; ports shown at the rear. ' + notes + 'Check: connectors.', TS, TUR, w=0,
        card={'fits': ['xVision'], 'slotWidth': 1},
        rearModules=[{'partNumber': pn, 'name': 'Module panel (rear facing)', 'width': 1, 'cardsPerModule': 1, 'cardOffset': 0, 'default': True,
                      'included': True, 'portGroups': ports}])
S12 = lambda d, n, p: R(d, '12G-SDI', 'BNC', n, p)
S3 = lambda d, n, p: R(d, '3G-SDI', 'BNC', n, p)
H = lambda d, n, p: R(d, 'HDMI', 'HDMI', n, p)
OC = lambda d, n, p, m: R(d, 'Fibre', 'opticalCON DUO', n, p + f' ({m})')
xm('XVVRMSDI2HDMI12G', 'xVision 12G-SDI to HDMI 2.0 module', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Loop'), H('out', 1, 'HDMI Out')])
xm('XVVRMHDMI2SDI12G', 'xVision HDMI 2.0 to 12G-SDI module', [H('in', 1, 'HDMI In'), S12('out', 2, 'SDI Out')])
xm('XVVRMSDXHDMI', 'xVision bidirectional HDMI / 3G-SDI module', [S3('in', 1, 'SDI In'), H('out', 1, 'HDMI Out'), H('in', 1, 'HDMI In'), S3('out', 1, 'SDI Out')])
xm('XVVRMSDIHDMI', 'xVision 3G-SDI to HDMI module', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), H('out', 1, 'HDMI Out')])
xm('XVVRMHDMISDI', 'xVision HDMI to 3G-SDI module', [H('in', 1, 'HDMI In'), S3('out', 2, 'SDI Out')])
xm('XVVRMSDI2SDI', 'xVision 3G-SDI scaler / converter module', [S3('in', 1, 'SDI In'), S3('out', 2, 'SDI Out')])
xm('XVVRMSDI2AUD', 'xVision audio de-embedder, 3G-SDI to HDMI + audio', [S3('in', 1, 'SDI In'), H('out', 1, 'HDMI Out'), R('out', 'Analog audio', 'Terminal block', 4, 'Audio Out')])
xm('XVVRMAUDIO2S', 'xVision audio embedder, HDMI / 3G-SDI + audio to 3G-SDI', [S3('in', 1, 'SDI In'), H('in', 1, 'HDMI In'), R('in', 'Analog audio', 'Terminal block', 4, 'Audio In'), S3('out', 1, 'SDI Out')])
xm('XVVRMSDA812G', 'xVision 1:8 12G-SDI distribution amplifier module', [S12('in', 1, 'SDI In'), S12('out', 8, 'SDI Out')])
xm('XVVRMHDMIDA', 'xVision 1:4 HDMI 2.0 distribution amplifier module', [H('in', 1, 'HDMI In'), H('out', 4, 'HDMI Out')])
xm('XVVRMDP2QSDI', 'xVision DisplayPort to quad 3G-SDI module', [R('in', 'DisplayPort', 'DisplayPort', 1, 'DP In'), S3('out', 4, 'SDI Out')])
xm('XVVRMAD2SDI', 'xVision analogue to 3G-SDI module', [R('in', 'Analog video', 'BNC', 3, 'Analog Video In'), S3('out', 2, 'SDI Out')])
for mode in ('MM', 'SM'):
    m = 'multimode' if mode == 'MM' else 'singlemode'
    xm(f'XVVRMS2F12G-{mode}', f'xVision 12G-SDI to fibre module ({m})', [S12('in', 1, 'SDI In'), S12('out', 1, 'SDI Loop'), OC('out', 1, 'Fibre Out', m)])
    xm(f'XVVRMF2S12G-{mode}', f'xVision fibre to 12G-SDI module ({m})', [OC('in', 1, 'Fibre In', m), S12('out', 2, 'SDI Out')])
    xm(f'XVVRMH2F-{mode}', f'xVision HDMI 2.0 to fibre module ({m})', [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Loop'), OC('out', 1, 'Fibre Out', m)])
    xm(f'XVVRMF2H-{mode}', f'xVision fibre to HDMI 2.0 module ({m})', [OC('in', 1, 'Fibre In', m), H('out', 1, 'HDMI Out')])
    xm(f'XVVRMOBO44-{mode}', f'xVision 4K 1:4 optical breakout module ({m})', [OC('in', 1, 'Fibre In', m), OC('out', 4, 'Fibre Out', m)])
    xm(f'XVVRMOBO1212-{mode}', f'xVision 4K 1:12 optical breakout module ({m})', [OC('in', 1, 'Fibre In', m), OC('out', 12, 'Fibre Out', m)])
xm('XVVRMHDBTHDM', 'xVision HDBaseT to HDMI module', [R('in', 'Ethernet', 'etherCON', 1, 'HDBaseT In'), H('out', 1, 'HDMI Out')])
xm('XVVRMHDMIHDB', 'xVision HDMI to HDBaseT module', [H('in', 1, 'HDMI In'), H('out', 1, 'HDMI Loop'), R('out', 'Ethernet', 'etherCON', 1, 'HDBaseT Out')])
xm('XVVRMNETSW1G', 'xVision 4-port gigabit switch module with fibre uplink', [R('io', 'Ethernet', 'etherCON', 4, 'GbE'), OC('io', 1, 'Fibre uplink', 'multimode')])
xm('XVVRMOPTO3', 'xVision 1:3 DMX splitter / isolator with thru + RDM (XLR3)', [R('in', 'DMX', 'XLR3M', 1, 'DMX In'), R('out', 'DMX', 'XLR3F', 1, 'DMX Thru'), R('out', 'DMX', 'XLR3F', 3, 'DMX Out')])
xm('XVVRMOPTO5', 'xVision 1:3 DMX splitter / isolator with thru + RDM (XLR5)', [R('in', 'DMX', 'XLR5M', 1, 'DMX In'), R('out', 'DMX', 'XLR5F', 1, 'DMX Thru'), R('out', 'DMX', 'XLR5F', 3, 'DMX Out')])
xm('XVVRMSDIDLY', 'xVision 3G-SDI delay module', [S3('in', 1, 'SDI In'), S3('out', 2, 'SDI Out')])
add(TF, 'theatrixx-xvvrm-blank', TX, 'XVVRM-BLANK', 'xVision blank module', 'xVision module', 'card', 0, [], 'Blank filler for an empty bay.', TS, TUR, w=0,
    card={'fits': ['xVision'], 'slotWidth': 1},
    rearModules=[{'partNumber': 'XVVRM-BLANK', 'name': 'Blank', 'width': 1, 'cardsPerModule': 1, 'cardOffset': 0, 'default': True, 'included': True, 'portGroups': []}])

# ======================= MuxLab =======================
MF, MX = 'muxlab.json', 'MuxLab'
MS = 'Canford MuxLab listings'
add(MF, 'muxlab-500444', MX, '500444', '500444 4x4 HDMI matrix, 1U', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', 'HDMI', 'HDMI', 4, 'HDMI Out'), R('out', 'Other', 'RCA', 4, 'Coax Digital Audio Out'), LAN(1), R('in', 'Other', '3.5mm', 1, 'IR Sensor'), RS232(), DC()],
    'Rack brackets included.', MS, 'https://www.canford.co.uk/MUXLAB-VIDEO-SWITCHERS-HDMI', verified=True)
add(MF, 'muxlab-500443', MX, '500443', '500443 8x8 HDMI matrix, 1U', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), R('out', 'Other', 'RCA', 8, 'Coax Digital Audio Out'), LAN(1), R('in', 'Other', '3.5mm', 1, 'IR Sensor'), RS232(), DC()],
    '8x8 version of the 500444. Check: connectors.', MS, 'https://www.canford.co.uk/MUXLAB-VIDEO-SWITCHERS-HDMI')
add(MF, 'muxlab-500413', MX, '500413', '500413 8x8 HDMI / HDBaseT matrix', 'Matrix', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'Ethernet', 'RJ45', 8, 'HDBaseT Out (PoH)'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out (mirror 1-2)'),
     R('out', 'Other', 'RCA', 8, 'Coax Digital Audio Out'), R('io', 'RS-232', 'Terminal block 3-pin', 1, 'RS-232'), R('in', 'Other', '3.5mm', 8, 'IR Sensor'),
     R('out', 'Other', '3.5mm', 8, 'IR Emitter'), R('in', 'Power', 'Terminal block 3-pin', 1, '48V DC')],
    '444.5 x 94 x 229 mm; powers receivers over HDBaseT.', MS, 'https://www.canford.co.uk/MUXLAB-VIDEO-SWITCHERS-HDMI', verified=True)
add(MF, 'muxlab-500412-v2', MX, '500412-V2', '500412-V2 4x4 HDMI / HDBaseT matrix kit, 1U', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', 'HDMI', 'HDMI', 4, 'HDMI Out'), R('out', 'Ethernet', 'RJ45', 4, 'HDBaseT Out'), R('out', 'Other', 'RCA', 4, 'Coax Audio Out'),
     R('out', 'Analog audio', 'Terminal block 5-pin', 4, 'Balanced Audio Out'), R('in', 'Other', '3.5mm', 5, 'IR In'), R('out', 'Other', '3.5mm', 5, 'IR Out'), LAN(1), RS232(), DC()],
    '440 x 44.5 x 200 mm, with four HDBaseT receivers.', MS, 'https://www.canford.co.uk/MUXLAB-VIDEO-SWITCHERS-HDMI', verified=True)
add(MF, 'muxlab-500905', MX, '500905', '500905 3-slot rack-mount extender chassis, 1U', 'Rack chassis', 'shelf', 1, [],
    'Holds three MuxLab extenders lying flat (500112, 500114, 500451, 500453, 500454, 500456, 500753-500756).', MS,
    'https://www.canford.co.uk/Products/2027414/28-7097', verified=True, carrier={'bays': 3, 'fits': ['MuxLab extender']})
add(MF, 'muxlab-500920', MX, '500920', '500920 16-slot rack-mount extender chassis, 3U', 'Rack chassis', 'shelf', 3, [],
    'Holds sixteen MuxLab extenders standing up, facing front or rear (also 500757-500759). 500921 filler plates.', MS,
    'https://canford.co.uk/MUXLAB-HARDWARE-AND-ACCESSORIES', verified=True, carrier={'bays': 16, 'fits': ['MuxLab extender']})

# ======================= OREI =======================
RF, OR = 'orei.json', 'OREI'
ORU = 'https://orei.com/collections/matrix'
for pn, i, o, ru, txt in (('HDS-808', 8, 8, 1, '4K30 8x8'), ('HDS-816', 8, 16, 1, '4K30 8x16'), ('HDS-1616', 16, 16, 2, '4K30 16x16'),
                          ('UHD-808', 8, 8, 1, '4K60 8x8 with audio extract'), ('UHD-1616', 16, 16, 2, '4K60 16x16 with audio extract'),
                          ('UHDS-808VW', 8, 8, 1, '4K60 8x8 seamless with video wall')):
    add(RF, 'orei-' + pn.lower(), OR, pn, f'{pn} {txt} HDMI matrix', 'Matrix', 'router', ru,
        hdmi_mx(i, o, [R('out', 'Analog audio', '3.5mm', o, 'Audio Out')] if 'UHD' in pn else []) + [LAN(1), RS232(), IR, AC()],
        'Check: rack height, audio outputs and power.', 'OREI matrix collection', ORU)
add(RF, 'orei-uhd88-exb400r-k', OR, 'UHD88-EXB400R-K', 'UHD88-EXB400R-K 8x8 HDMI / HDBaseT matrix kit', 'Matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'Ethernet', 'RJ45', 8, 'HDBaseT Out'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out (mirror)'), LAN(1), RS232(), IR, AC()],
    'Matrix with eight HDBaseT receivers. Check: connectors.', 'OREI support article', 'https://support.orei.com/hc/en-us/articles/41705385377559-UHD88-EXB400R-K-Overview-and-Use-Cases')

# ======================= Gefen =======================
GF, GE = 'gefen.json', 'Gefen'
GS = 'Gefen product catalogue (June 2019)'
GU = 'https://www.ambertech.com.au/documents/brochures/Gefen%20June%202019.pdf'
add(GF, 'gefen-ext-uhd-88', GE, 'EXT-UHD-88', 'EXT-UHD-88 4K Ultra HD 8x8 HDMI matrix, 2U', 'Matrix', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In (locking)'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out (locking)'), RS232(), LAN(1, 'IP control'), R('in', 'Other', '3.5mm', 1, 'IR In/Ext'),
     R('in', 'Power', 'DIN 4-pin locking', 1, '24V DC')], '440 x 89 x 400 mm without ears.', 'Gefen EXT-UHD-88 data sheet', 'https://www.ivojo.co.uk/pdf/gefen/gefen-ext-uhd-88.pdf', verified=True)
add(GF, 'gefen-ext-uhd600a-88', GE, 'EXT-UHD600A-88', 'EXT-UHD600A-88 4K 600 MHz 8x8 matrix with HDR and audio de-embed', 'Matrix', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), R('out', 'Other', 'Toslink', 8, 'Optical Audio Out'), R('out', 'Analog audio', '3.5mm', 8, 'Analog Audio Out'),
     RS232(), LAN(1), R('in', 'Other', '3.5mm', 1, 'IR In'), R('in', 'Power', 'DIN 4-pin locking', 1, '24V DC')], 'Check: audio connectors and height.', GS, GU)
add(GF, 'gefen-gef-uhd-89-hbt2', GE, 'GEF-UHD-89-HBT2', 'GEF-UHD-89-HBT2 4K 8x9 HDMI / HDBaseT 2.0 matrix', 'Matrix', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'Ethernet', 'RJ45', 8, 'HDBaseT Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out (local)'), RS232(), LAN(1), AC()],
    'Check: height and connectors.', GS, GU)
add(GF, 'gefen-ext-cu-lan', GE, 'EXT-CU-LAN', 'EXT-CU-LAN AV-over-IP matrix controller, 2U', 'Control', 'control', 2,
    [LAN(2, 'LAN'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC()], 'Controller for Gefen LANS AV-over-IP systems; rack ears included. Check: ports.', GS, GU)
for pn, name, ins, outs in (('EXT-HD-VWC-144', 'HD video wall controller, 1x4 (2x2 wall)', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In')], [R('out', 'HDMI', 'HDMI', 4, 'HDMI Out')]),
                            ('EXT-UHD600A-VWC-14', '4K 600 MHz video wall controller, 1x4', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In')], [R('out', 'HDMI', 'HDMI', 4, 'HDMI Out')]),
                            ('EXT-UHD600A-MVSL-41', '4K 600 MHz 4x1 multiview seamless switcher', [R('in', 'HDMI', 'HDMI', 4, 'HDMI In')], [R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')]),
                            ('EXT-HD-MVSL-441', 'HD 4x1 multiview seamless switcher', [R('in', 'HDMI', 'HDMI', 4, 'HDMI In')], [R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')]),
                            ('EXT-HD-SL-444', 'HD 4x4 seamless HDMI matrix', [R('in', 'HDMI', 'HDMI', 4, 'HDMI In')], [R('out', 'HDMI', 'HDMI', 4, 'HDMI Out')])):
    add(GF, 'gefen-' + pn.lower(), GE, pn, f'{pn} {name}, 1U', 'Video wall / seamless', 'switcher', 1,
        ins + outs + [RS232(), LAN(1), R('in', 'Power', 'DIN 4-pin locking', 1, '24V DC')], '1U with rack ears. Check: audio and power connectors.', GS, GU)
add(GF, 'gefen-ext-rack-1u-gry', GE, 'EXT-RACK-1U-GRY', 'EXT-RACK-1U-GRY 1U rack tray for two half-rack Gefen units', 'Rack kits', 'shelf', 1, [],
    'Holds two half-rack-width Gefen boxes (ELR, HBT2 and LANS extenders, EXT-MFP).', GS, GU, carrier={'bays': 2, 'fits': ['Gefen half-rack']})
HALF = {'w': 210, 'h': 40}
def gh(pn, name, ports, fam='Extenders', cat='converter'):
    add(GF, 'gefen-' + pn.lower(), GE, pn, name, fam, cat, 1, ports + [R('in', 'Power', 'DC locking', 1, '5V DC')],
        'Half-rack-width box; two fit the EXT-RACK-1U-GRY. Check: connectors.', GS, GU, w=6, formFactor='Gefen half-rack', boxMm=HALF)
gh('EXT-DVIKA-HBT2-TX', 'EXT-DVIKA-HBT2 DVI KVM over HDBaseT 2.0 sender', [R('in', 'DVI', 'DVI-I', 1, 'DVI In'), R('io', 'USB', 'USB-B', 1, 'USB Host'), R('in', 'Analog audio', '3.5mm', 1, 'Audio In'), R('out', 'Ethernet', 'RJ45', 1, 'HDBaseT Link'), RS232()])
gh('EXT-DVIKA-HBT2-RX', 'EXT-DVIKA-HBT2 DVI KVM over HDBaseT 2.0 receiver', [R('in', 'Ethernet', 'RJ45', 1, 'HDBaseT Link'), R('out', 'DVI', 'DVI-I', 1, 'DVI Out'), R('io', 'USB', 'USB-A', 4, 'USB Device'), R('out', 'Analog audio', '3.5mm', 1, 'Audio Out'), RS232()])
gh('EXT-HDKVM-ELR-TX', 'EXT-HDKVM-ELR HDMI KVM ELR sender (one CAT-5)', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('io', 'USB', 'USB-B', 1, 'USB Host'), R('out', 'Ethernet', 'RJ45', 1, 'Link'), RS232()])
gh('EXT-HDKVM-ELR-RX', 'EXT-HDKVM-ELR HDMI KVM ELR receiver', [R('in', 'Ethernet', 'RJ45', 1, 'Link'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB-A', 2, 'USB Device'), RS232()])
gh('EXT-UHD-LANS-TX', 'EXT-UHD-LANS 4K HDMI over IP sender', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Loop'), LAN(1, 'AV LAN'), RS232()], fam='AV over IP')
gh('EXT-UHD-LANS-RX', 'EXT-UHD-LANS 4K HDMI over IP receiver', [LAN(1, 'AV LAN'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), RS232()], fam='AV over IP')
gh('EXT-UHDKA-LANS-TX', 'EXT-UHDKA-LANS 4K HDMI KVM over IP sender', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('io', 'USB', 'USB-B', 1, 'USB Host'), R('in', 'Analog audio', '3.5mm', 1, 'Audio In'), LAN(1, 'AV LAN'), RS232()], fam='AV over IP')
gh('EXT-UHDKA-LANS-RX', 'EXT-UHDKA-LANS 4K HDMI KVM over IP receiver', [LAN(1, 'AV LAN'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'USB', 'USB-A', 4, 'USB Device'), R('out', 'Analog audio', '3.5mm', 1, 'Audio Out'), RS232()], fam='AV over IP')
gh('EXT-MFP', 'EXT-MFP multi-format presentation switcher', [R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('in', 'DisplayPort', 'DisplayPort', 1, 'DP In'), R('in', 'DVI', 'DVI-I', 1, 'DVI In'), R('in', 'VGA', 'HD15', 1, 'VGA In'),
                            R('in', 'Analog video', 'RCA', 1, 'Composite In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'Ethernet', 'RJ45', 1, 'HDBaseT Out'), LAN(1)], fam='Presentation', cat='switcher')

# ======================= Kramer =======================
KRF, KR = 'kramer-more.json', 'Kramer'
KU = lambda s: 'https://www.kramerav.com/product/' + s
KS = 'Kramer product listings'
def kr(pn, name, fam, cat, ru, ports, notes, w=12, ver=False, src=KS, url=None, **kw):
    if w == 6: kw.setdefault('formFactor', 'Kramer half-rack'); kw.setdefault('boxMm', {'w': 216, 'h': 43})
    add(KRF, 'kramer-' + pn.lower().replace('/', '-'), KR, pn, name, fam, cat, ru, ports, notes, src, url or KU(pn), verified=ver, w=w, **kw)
CTL_K = [LAN(1, 'Ethernet'), RS232('Terminal block 3-pin'), F('io', 'USB', 'Mini USB-B', 1, 'USB')]
kr('VS-1616DN-EM', 'VS-1616DN-EM 2x2 to 16x16 modular 4K60 multi-format matrix, 4U', 'Modular matrix', 'router', 4,
   [R('io', 'Other', 'Card slot', 1, 'Input / output card rears (HDMI, HDBaseT, DGKat, DVI, fibre, VGA)'), LAN(1, 'Ethernet'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC()],
   'Populated in steps of two inputs / outputs with I/O cards; add card ports per device. 19 x 14.17 in deep. Front mini USB and audio test jacks.',
   ver=True, src='Kramer VS-1616DN-EM data sheet', url='https://www.fullcompass.com/common/files/36175-VS1616DNEMDatasheet.pdf')
kr('VS-3232DN-EM', 'VS-3232DN-EM 4x4 to 32x32 modular multi-format matrix', 'Modular matrix', 'router', 8,
   [R('io', 'Other', 'Card slot', 1, 'Input / output card rears'), LAN(1, 'Ethernet'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC(2)],
   'Larger sibling of the VS-1616DN-EM. Check: rack height and PSUs.')
for pn, i, o, ru, txt in (('VS-44H2', 4, 4, 1, '4x4 4K HDR HDMI matrix'), ('VS-84H2', 8, 4, 1, '8x4 4K HDR HDMI matrix'), ('VS-1616D', 16, 16, 2, '16x16 DVI matrix (legacy)')):
    t = 'DVI' if 'DVI' in txt else 'HDMI'
    kr(pn, f'{pn} {txt}', 'VS matrix', 'router', ru, [R('in', t, t if t == 'HDMI' else 'DVI-I', i, f'{t} In'), R('out', t, t if t == 'HDMI' else 'DVI-I', o, f'{t} Out')] + CTL_K + [AC()],
       'Check: connectors.', w=12)
kr('VS-88UT', 'VS-88UT 8x8 4K HDMI / HDBaseT matrix with PoE', 'VS matrix', 'router', 2,
   [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('in', 'Ethernet', 'RJ45', 4, 'HDBaseT In'), R('out', 'HDMI', 'HDMI', 4, 'HDMI Out'), R('out', 'Ethernet', 'RJ45', 4, 'HDBaseT Out (PoE)'),
    R('io', 'Analog audio', 'Terminal block 5-pin', 8, 'Audio I/O')] + CTL_K + [AC()], 'Mixed HDMI / HDBaseT ports. Check: split.')
kr('VP-440X', 'VP-440X 18G 4K presentation scaler / switcher, 1U', 'Scaler', 'switcher', 1,
   [R('in', 'HDMI', 'HDMI', 3, 'HDMI In'), R('in', 'Ethernet', 'RJ45', 1, 'HDBaseT In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'Ethernet', 'RJ45', 1, 'HDBaseT Out'),
    R('io', 'Analog audio', 'Terminal block 5-pin', 2, 'Audio In/Out')] + CTL_K + [AC()], 'Check: inputs.', w=6)
kr('VP-558', 'VP-558 7-input dual-zone ProScale presentation switcher / scaler, 1U', 'Scaler', 'switcher', 1,
   [R('in', 'HDMI', 'HDMI', 3, 'HDMI In'), R('in', 'VGA', 'HD15', 2, 'VGA In'), R('in', 'Analog video', 'BNC', 2, 'CV / YC In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
    R('out', 'Ethernet', 'RJ45', 1, 'HDBaseT Out'), R('io', 'Analog audio', 'Terminal block 5-pin', 4, 'Audio I/O'), R('in', 'Analog audio', 'XLR3F', 2, 'Mic In')] + CTL_K + [AC()],
   'Check: all counts.')
kr('VP-734', 'VP-734 9-input ProScale presentation switcher / scaler, 1U', 'Scaler', 'switcher', 1,
   [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('in', 'VGA', 'HD15', 2, 'VGA In'), R('in', 'Analog video', 'BNC', 3, 'CV / YC / YPbPr In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
    R('out', 'VGA', 'HD15', 1, 'VGA Out'), R('io', 'Analog audio', 'Terminal block 5-pin', 6, 'Audio I/O')] + CTL_K + [AC()], 'Check: all counts.')
kr('MV-6', 'MV-6 6-window 3G-SDI / HDMI multiviewer, 1U', 'Multiviewer', 'monitor', 1,
   [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Loop'), R('out', 'HDMI', 'HDMI', 1, 'MV HDMI Out'),
    R('out', '3G-SDI', 'BNC', 1, 'MV SDI Out')] + CTL_K + [AC()], 'Check: input split.')
kr('MV-4X', 'MV-4X 4K60 4x1 quad-view multiviewer / seamless switcher', 'Multiviewer', 'monitor', 1,
   [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')] + CTL_K + [DC()], 'Half-rack. Check: connectors.', w=6)
kr('VM-4H2', 'VM-4H2 1:4 4K HDR HDMI distribution amplifier', 'DA', 'converter', 1,
   [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 4, 'HDMI Out'), RS232('Terminal block 3-pin'), DC()], 'Small box; RK-T2B or shelf to rack. Check: size.', w=4)
kr('VM-8H2', 'VM-8H2 1:8 4K HDR HDMI distribution amplifier, 1U', 'DA', 'converter', 1,
   [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), RS232('Terminal block 3-pin'), LAN(1), AC()], 'Check: model name and connectors.')
kr('VM-3UT', 'VM-3UT 1:3 4K HDMI / HDBaseT distribution amplifier', 'DA', 'converter', 1,
   [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'Ethernet', 'RJ45', 3, 'HDBaseT Out'), RS232('Terminal block 3-pin'), DC()], 'Check: connectors.', w=6)
kr('PA-120Z', 'PA-120Z 2 x 60 W power amplifier, half rack', 'Audio amplifier', 'audio', 1,
   [R('in', 'Analog audio', 'Terminal block 3-pin', 2, 'Line In'), R('out', 'Analog audio', 'Terminal block', 2, 'Speaker Out'), DC('24V DC')], '70 V / 100 V or low-impedance outputs. Check: connectors.', w=6)
kr('PA-240Z', 'PA-240Z 2 x 120 W power amplifier, half rack', 'Audio amplifier', 'audio', 1,
   [R('in', 'Analog audio', 'Terminal block 3-pin', 2, 'Line In'), R('out', 'Analog audio', 'Terminal block', 2, 'Speaker Out'), AC()], 'Check: connectors.', w=6)
kr('AFM-20DSP', 'AFM-20DSP audio matrix with DSP, 1U', 'Audio DSP', 'audio', 1,
   [R('in', 'Analog audio', 'Terminal block 3-pin', 12, 'Mic / Line In'), R('out', 'Analog audio', 'Terminal block 3-pin', 8, 'Line Out'), R('io', 'Dante/AES67', 'RJ45', 1, 'Dante (option)'), LAN(1), RS232('Terminal block 3-pin'), AC()],
   'Check: model variants (AFM-20DSP-AEC) and channel counts.')
kr('DSP-62-AEC', 'DSP-62-AEC 6x2 audio DSP with echo cancelling, half rack', 'Audio DSP', 'audio', 1,
   [R('in', 'Analog audio', 'Terminal block 3-pin', 6, 'Mic / Line In'), R('out', 'Analog audio', 'Terminal block 3-pin', 2, 'Line Out'), R('io', 'USB', 'USB-B', 1, 'USB audio'), LAN(1), DC()], 'Check: connectors.', w=6)
kr('RK-T2B', 'RK-T2B 19-inch rack adapter for two half-rack Kramer units', 'Rack adapters', 'shelf', 1, [], 'Check: which units it takes.', carrier={'bays': 2, 'fits': ['Kramer half-rack']})
kr('RK-3T', 'RK-3T 19-inch rack adapter for three TOOLS units', 'Rack adapters', 'shelf', 1, [], 'Takes three Kramer TOOLS mini units. Check: fit.', carrier={'bays': 3, 'fits': ['Kramer TOOLS']})

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
idx = json.load(open(ip))  # re-read just before appending
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
