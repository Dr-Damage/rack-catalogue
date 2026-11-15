#!/usr/bin/env python3
"""AV and broadcast brands batch 2 (added 2026-11-15):
  apantac-more.json   Apantac Crescent Mi / MX / LE multiviewers, TAHOMA T# modular frames, UE, SDI DA (apantac.json: Mi-16-UHD, TAHOMA-LE-4).
  datavideo-more.json Datavideo switcher mainframes, MTX matrices, rack monitors, recorders, DAC converters and RMK rack kits
                      (datavideo.json: SE-1200MU).
  bzbgear.json        BZBGear matrices, multiviewers, HDMI DAs and IPGEAR rack brackets.
  gravue.json         Gra-Vue MRS / VIO multiviewers, XIO frame, MIO mini converters.
Not added: LinkBridge (maker not identified yet). Specs from dealer listings; 'Check:' marks anything unconfirmed."""
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
S3 = lambda d, n, p: R(d, '3G-SDI', 'BNC', n, p)
S12 = lambda d, n, p: R(d, '12G-SDI', 'BNC', n, p)
H = lambda d, n, p: R(d, 'HDMI', 'HDMI', n, p)

# ======================= Apantac =======================
AF, AP = 'apantac-more.json', 'Apantac'
MK = 'https://www.markertek.com/brand/apantac'
add(AF, 'apantac-mi-8-12g-uhd', AP, 'Mi-8-12G-UHD', 'Crescent Mi-8-12G-UHD 8-input 12G multiviewer, 1RU', 'Crescent Mi', 'monitor', 1,
    [S12('in', 8, 'SDI In'), H('out', 1, 'HDMI 2.0 Out (UHD)'), H('out', 1, 'HDMI 1.4 Out'), S12('out', 1, '12G-SDI Out'), S3('out', 1, '3G-SDI Out'),
     LAN(1), R('io', 'GPI', 'RJ45', 4, 'GPI (32, RJ50)'), R('io', 'RS-232', 'RJ45', 1, 'RS-232 (TSL / AXP)'), AC(2, 'AC In (2nd optional)')],
    '446 x 452 x 44 mm, 55 W typical (100 W rated), optional redundant PSU. Check: audio monitor outputs.', 'Markertek Mi-8-12G-UHD listing',
    'https://www.markertek.com/product/apa-mi-8-12g-uhd/apantac-crescent-mi-8-12g-uhd-1ru-8x1-12g-3g-hd-sdi-input-multiviewer-with-hdmi-2-0-uhd-output', verified=True, full=True)
add(AF, 'apantac-mi-16-12g-uhd', AP, 'Mi-16-12G-UHD', 'Crescent Mi-16-12G-UHD 16-input 12G multiviewer, 2RU', 'Crescent Mi', 'monitor', 2,
    [S12('in', 16, 'SDI In'), H('out', 1, 'HDMI 2.0 Out (UHD)'), H('out', 1, 'HDMI 1.4 Out'), S12('out', 1, '12G-SDI Out'), S3('out', 1, '3G-SDI Out'),
     LAN(1), R('io', 'GPI', 'RJ45', 8, 'GPI (64, RJ50)'), R('io', 'RS-232', 'RJ45', 1, 'RS-232'), AC(2)],
    'Check: outputs and GPI count (by analogy with the Mi-8-12G-UHD).', 'Markertek Mi-16-12G-UHD listing',
    'https://www.markertek.com/product/apa-mi-16-12guhd/apantac-crescent-mi-16-12g-uhd-2ru-16x1-12g-3g-hd-sdi-input-multiviewer-with-hdmi-2-0-uhd-output', full=True)
add(AF, 'apantac-mx-32x2-uhd', AP, 'MX-32x2-UHD', 'Crescent MX-32x2-UHD 32-input dual-head multiviewer, 2RU', 'Crescent MX', 'monitor', 2,
    [S3('in', 32, 'SDI In'), H('out', 2, 'HDMI 2.0 Out (UHD)'), S12('out', 2, 'SDI Out (12G / 3G)'), LAN(1), R('io', 'GPI', 'RJ45', 8, 'GPI (64, RJ50)'),
     R('io', 'RS-232', 'RJ45', 1, 'RS-232'), AC(2)],
    '100 W, redundant PSU. Check: power connectors.', 'Markertek MX-32X2-UHD listing',
    'https://www.markertek.com/product/apa-mx-32x2-uhd/apantac-mx-32x2-uhd-crescent-mx-2ru-32x2-3g-hd-sd-sdi-multiviewer-with-2-uhd-outputs', verified=True, full=True)
add(AF, 'apantac-mi-9', AP, 'Mi-9', 'Crescent Mi-9 9-input multiviewer, 1RU', 'Crescent Mi', 'monitor', 1,
    [S3('in', 9, 'SDI In'), S3('out', 9, 'SDI Loop'), H('out', 1, 'HDMI Out'), S3('out', 1, 'SDI Out'), LAN(1), R('io', 'GPI', 'RJ45', 2, 'GPI'), R('io', 'RS-232', 'RJ45', 1, 'RS-232'), AC(1)],
    'Check: all counts.', 'Apantac catalogue excerpts', 'https://pdf.directindustry.com/pdf/apantac-llc/apantac-multiviewer-catalog/239833-971198.html', full=True)
add(AF, 'apantac-le-16cv-ii', AP, 'LE-16CV-II', 'Crescent LE-16CV-II 16-input composite multiviewer, 1RU', 'Crescent LE', 'monitor', 1,
    [R('in', 'Analog video', 'BNC', 16, 'CVBS In'), H('out', 1, 'HDMI Out'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC(1)],
    '500 mm deep. Check: counts.', 'Apantac catalogue excerpts', 'https://pdf.directindustry.com/pdf/apantac-llc/apantac-multiviewer-catalog/239833-971198.html', full=True)
for n in (4, 8):
    add(AF, f'apantac-ue-{n}-k-ii', AP, f'UE-{n}-K-II', f'UE-{n}-K-II {n}-input 4K HDMI multiviewer, 2RU', 'UE', 'monitor', 2,
        [H('in', n, 'HDMI In'), H('out', 1, 'HDMI Out'), S12('out', 1, '12G-SDI Out'), S3('out', 1, '3G-SDI Out'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC(1)],
        '450 mm deep. Check: counts.', 'Apantac catalogue excerpts', 'https://pdf.directindustry.com/pdf/apantac-llc/ue-multiviewers/239833-968569.html')
add(AF, 'apantac-tahoma-t-4ru', AP, 'TAHOMA T# 4RU', 'TAHOMA T# modular multiviewer frame, 4RU (up to 64x16)', 'TAHOMA T#', 'monitor', 4,
    [R('io', 'Other', 'Card slot', 8, 'Input card slots (SDI, SFP ST 2110 / 2022-6, HDMI)'), R('io', 'Other', 'Card slot', 4, 'Output card slots'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), LAN(2), AC(2)],
    'Modular frame: 8 input slots, 4 output slots; card I/O varies, so add card ports per device. Check: fixed connectors.',
    'Apantac TAHOMA T# brochure', 'https://pdf.directindustry.com/pdf/apantac-llc/tahoma-t/239833-968568.html', full=True)
add(AF, 'apantac-tahoma-t-2ru', AP, 'TAHOMA T# 2RU', 'TAHOMA T# modular multiviewer frame, 2RU (up to 32x4)', 'TAHOMA T#', 'monitor', 2,
    [R('io', 'Other', 'Card slot', 4, 'Input card slots'), R('io', 'Other', 'Card slot', 1, 'Output card slot'), R('in', 'Reference', 'BNC', 1, 'Ref In'), LAN(2), AC(2)],
    'Modular frame: 4 input slots, 1 output slot. Check: fixed connectors.', 'Apantac TAHOMA T# brochure', 'https://pdf.directindustry.com/pdf/apantac-llc/tahoma-t/239833-968568.html', full=True)
add(AF, 'apantac-sdi-da-16x1x2', AP, 'SDI-DA-1x2x16', '16 x 1:2 SDI / ASI distribution amplifier, 1RU', 'DA', 'converter', 1,
    [S3('in', 16, 'SDI In'), S3('out', 32, 'SDI Out'), AC(1)], 'Sixteen 1:2 DAs in 1RU. Check: part number and power.', 'Apantac product portfolio',
    'https://pdf.directindustry.com/pdf/apantac-llc/product-portfolio/239833-971199.html')

# ======================= Datavideo =======================
DF, DV = 'datavideo-more.json', 'Datavideo'
DG = 'Datavideo product guide (2017)'
DU = 'https://www.rentex.com/wp-content/uploads/2017/03/Datavideo_Product_Guide_2017.pdf'
add(DF, 'dv-se-2850', DV, 'SE-2850', 'SE-2850 8/12-input HD/SD switcher mainframe, 2RU', 'SE switchers', 'switcher', 2,
    [S3('in', 8, 'SDI In (12 max)'), H('in', 2, 'HDMI In'), R('in', 'Analog video', 'BNC', 1, 'CV In'), S3('out', 4, 'SDI Out'), H('out', 2, 'HDMI Out'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Other', 'DB25', 1, 'Tally'), LAN(1, 'Control panel LAN'), AC(1)],
    'Mainframe with separate control panel. Check: input split and connectors.', DG, DU, full=True)
add(DF, 'dv-se-2200', DV, 'SE-2200', 'SE-2200 6-input HD switcher mainframe, 2RU', 'SE switchers', 'switcher', 2,
    [S3('in', 6, 'SDI In'), H('in', 2, 'HDMI In'), S3('out', 6, 'SDI Out'), H('out', 2, 'HDMI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
     R('io', 'Other', 'DB25', 1, 'Tally'), LAN(1, 'Control panel LAN'), AC(1)], 'Check: input split and connectors.', DG, DU, full=True)
add(DF, 'dv-se-2800', DV, 'SE-2800', 'SE-2800 8/12-input HD switcher processor', 'SE switchers', 'switcher', 2,
    [S3('in', 8, 'SDI In (12 max)'), S3('out', 3, 'SDI Out'), H('out', 2, 'HDMI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Other', 'DB25', 1, 'Tally'), LAN(1), AC(1)],
    'Processor and separate control panel. Check: rack height.', DG, DU, full=True)
add(DF, 'dv-mtx-100', DV, 'MTX-100', 'MTX-100 12x8 video commander matrix, 2RU', 'MTX', 'router', 2,
    [S3('in', 12, 'In'), S3('out', 8, 'Out'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC(1)], 'Check: connector types.', DG, DU)
add(DF, 'dv-mtx-200', DV, 'MTX-200', 'MTX-200 20x16 video commander matrix, 3RU', 'MTX', 'router', 3,
    [S3('in', 20, 'In'), S3('out', 16, 'Out'), LAN(1), R('io', 'RS-232', 'DB9', 1, 'RS-232'), AC(1)], 'Check: connector types.', DG, DU)
def tlm(pn, name, ru, scr, ports, notes):
    add(DF, 'dv-' + pn.lower(), DV, pn, name, 'TLM rack monitors', 'monitor', ru, ports + [DC()], notes, DG, DU, screens=scr)
tlm('TLM-170PR', 'TLM-170PR 17.3-inch rack monitor, 7RU', 7, {'count': 1, 'sizeIn': 17.3, 'aspect': '16:9'},
    [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), H('in', 2, 'HDMI In'), R('in', 'Analog video', 'BNC', 3, 'YUV In'), R('in', 'Analog video', 'BNC', 2, 'CV In'), R('out', 'Analog video', 'BNC', 1, 'CV Loop')],
    'Check: power connector.')
tlm('TLM-702HD', 'TLM-702HD dual 7-inch rack monitor, 3RU', 3, {'count': 2, 'sizeIn': 7, 'aspect': '16:9'},
    [S3('in', 2, 'SDI In'), H('in', 2, 'HDMI In'), R('in', 'Analog video', 'BNC', 6, 'YUV In'), R('in', 'Analog video', 'BNC', 2, 'CV In')], 'No loop-throughs.')
tlm('TLM-434H', 'TLM-434H quad 4.3-inch rack monitor, 2RU', 2, {'count': 4, 'sizeIn': 4.3, 'aspect': '16:9'},
    [S3('in', 4, 'SDI In'), S3('out', 4, 'SDI Loop'), H('in', 4, 'HDMI In'), R('in', 'Analog video', 'BNC', 2, 'CV In')], 'Check: power connector.')
add(DF, 'dv-hdr-70', DV, 'HDR-70', 'HDR-70 HD/SD recorder, 1RU', 'HDR recorders', 'recorder', 1,
    [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), S3('out', 1, 'SDI Out'), H('out', 1, 'HDMI Out'), R('in', 'Analog audio', 'XLR3F', 2, 'Audio In'), DC()],
    '8-channel embedded audio recording.', DG, DU, verified=True)
RMK2 = 'Datavideo DAC'
add(DF, 'dv-rmk-2', DV, 'RMK-2', 'RMK-2 2RU rack kit for eight DAC converters', 'Rack kits', 'shelf', 2, [], 'Holds up to eight DAC-series converters (or an HDR-10).', DG, DU,
    verified=True, carrier={'bays': 8, 'fits': [RMK2]})
add(DF, 'dv-rmk-1', DV, 'RMK-1', 'RMK-1 1RU rack kit', 'Rack kits', 'shelf', 1, [], 'Check: which units it holds.', 'Datavideo racks and rack panels page',
    'https://www.datavideo.com/category/racks-and-rack-panels', carrier={'bays': 4, 'fits': [RMK2]})
def dac(pn, name, ports, notes=''):
    add(DF, 'dv-' + pn.lower(), DV, pn, name, 'DAC converters', 'converter', 2, ports + [DC('5V DC')], (notes + ' ' if notes else '') + 'Fits the RMK-2 rack kit.',
        DG, DU, verified=True, w=1, formFactor=RMK2, boxMm={'w': 50, 'h': 80})
dac('DAC-70', 'DAC-70 up/down/cross converter', [R('in', 'VGA', 'HD15', 1, 'VGA In'), H('in', 1, 'HDMI In'), S3('in', 1, 'SDI In'), S3('out', 2, 'SDI Out')])
dac('DAC-60', 'DAC-60 3G-SDI to VGA converter', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), R('out', 'VGA', 'HD15', 1, 'VGA Out')])
dac('DAC-50S', 'DAC-50S 3G-SDI to analogue down-converter', [S3('in', 1, 'SDI In'), R('out', 'Analog video', 'BNC', 2, 'CV / Y-C Out')], 'Check: analogue output count.')
dac('DAC-9P', 'DAC-9P HDMI to SDI converter', [H('in', 1, 'HDMI In'), S3('out', 2, 'SDI Out')])
dac('DAC-8P', 'DAC-8P SDI to HDMI converter', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), H('out', 1, 'HDMI Out')])
dac('DAC-7', 'DAC-7 analogue to SD-SDI converter', [R('in', 'Analog video', 'BNC', 3, 'CV / YUV / Y-C In'), R('out', 'SDI', 'BNC', 2, 'SD-SDI Out')])
add(DF, 'dv-itc-100', DV, 'ITC-100', 'ITC-100 8-user wired intercom base station, 1RU', 'Intercom', 'audio', 1,
    [R('io', 'Analog audio', 'RJ45', 8, 'Beltpack'), R('io', 'Analog audio', 'XLR4M', 1, 'Headset'), R('io', 'Other', 'DB25', 1, 'Tally In'), R('in', 'Analog audio', 'XLR3F', 1, 'Program In'), DC()],
    'Rack-mount base for up to 8 beltpacks over CAT-5, with tally. Check: connectors.', 'Datavideo ITC-100 page', 'https://datavideo.com/product/ITC-100')

# ======================= BZBGear =======================
BF, BZ = 'bzbgear.json', 'BZBGear'
BU = 'https://avlgear.com/collections/bzbgear'
BS = 'AVLGear BZBGear listings'
def bz(pn, name, fam, cat, ru, ports, notes, w=12):
    add(BF, 'bzbgear-' + pn.lower(), BZ, pn, name, fam, cat, ru, ports + [LAN(1), R('io', 'RS-232', 'Terminal block 3-pin', 1, 'RS-232'), R('in', 'Other', '3.5mm', 1, 'IR In'), DC()],
        notes + ' Check: rack height and connectors.', BS, BU, w=w)
bz('BG-4K-44MA', 'BG-4K-44MA 4x4 HDMI 2.0 matrix with audio de-embed', 'Matrix', 'router', 1, [H('in', 4, 'HDMI In'), H('out', 4, 'HDMI Out'), R('out', 'Analog audio', '3.5mm', 4, 'Audio Out')], '')
bz('BZ-MVS4X4-4K', 'BZ-MVS4X4-4K 4x4 18 Gbps seamless matrix / video wall processor', 'Matrix', 'router', 1, [H('in', 4, 'HDMI In'), H('out', 4, 'HDMI Out')], '')
bz('BG-MVS4X4-CV', 'BG-MVS4X4-CV 4x4 4K seamless matrix / video wall processor', 'Matrix', 'router', 1, [H('in', 4, 'HDMI In'), H('out', 4, 'HDMI Out')], '')
bz('BG-MV41A-G2', 'BG-MV41A-G2 4x1 4K seamless multiviewer', 'Multiviewer', 'monitor', 1, [H('in', 4, 'HDMI In'), H('out', 1, 'HDMI Out')], 'Half-rack desktop box.', w=6)
bz('BG-8K-DA18', 'BG-8K-DA18 1x8 HDMI 2.1 8K splitter with downscaling', 'DA', 'converter', 1, [H('in', 1, 'HDMI In'), H('out', 8, 'HDMI Out'), R('out', 'Analog audio', '3.5mm', 1, 'Audio Out')], '')
add(BF, 'bzbgear-bg-ipgear-ultra-acc-rm2', BZ, 'BG-IPGEAR-ULTRA-ACC-RM2', 'BG-IPGEAR-ULTRA-ACC-RM2 1RU rack bracket for two IPGEAR units', 'IPGEAR', 'shelf', 1, [],
    'Holds two IPGEAR Ultra encoders / decoders. Check: count.', BS, BU, carrier={'bays': 2, 'fits': ['BZBGear IPGEAR']})
add(BF, 'bzbgear-bg-ipgear-ultra-acc-rm10', BZ, 'BG-IPGEAR-ULTRA-ACC-RM10', 'BG-IPGEAR-ULTRA-ACC-RM10 6RU rack bracket for ten IPGEAR units', 'IPGEAR', 'shelf', 6, [],
    'Holds ten IPGEAR units standing up.', BS, BU, carrier={'bays': 10, 'fits': ['BZBGear IPGEAR']})
add(BF, 'bzbgear-ipgear-pro-rack-4ru', BZ, 'BG-IPGEAR-PRO rack (4RU)', '4RU rack for ten BG-IPGEAR-PRO transmitters / receivers', 'IPGEAR', 'shelf', 4, [],
    'Check: part number.', BS, BU, carrier={'bays': 10, 'fits': ['BZBGear IPGEAR']})

# ======================= Gra-Vue =======================
GF, GV = 'gravue.json', 'Gra-Vue'
add(GF, 'gravue-mrs-1608mvs', GV, 'MRS-1608MVS', 'MRS-1608MVS 16-input 8-output multiview display system, 1RU', 'MRS', 'monitor', 1,
    [R('in', 'HD-SDI', 'BNC', 16, 'SDI In'), R('out', 'HD-SDI', 'BNC', 8, 'MV Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
     LAN(1, 'Control'), LAN(4, 'Upgrade'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'GPI', 'DB26', 1, 'GPI'), R('in', 'Timecode', 'BNC', 1, 'LTC'), R('in', 'Power', 'Other', 2, '48V DC')],
    'Check: LTC connector; power is two 48 V supplies.', 'B&H MRS-1608MVS listing', 'https://www.bhphotovideo.com/c/product/1033959-REG/gra_vue_mrs_1608mvs_1ru_8_output_multi_viewer.html', verified=True)
add(GF, 'gravue-mrs-1204mvs', GV, 'MRS-1204MVS', 'MRS-1204MVS 12-input 4-output multiview display system, 1RU', 'MRS', 'monitor', 1,
    [R('in', 'HD-SDI', 'BNC', 12, 'SDI In'), R('out', 'HD-SDI', 'BNC', 4, 'MV Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
     LAN(1, 'Control'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'GPI', 'DB26', 1, 'GPI'), R('in', 'Power', 'Other', 2, '48V DC')],
    'Check: counts (by analogy with MRS-1608MVS).', 'B&H MRS-1204MVS listing', 'https://www.bhphotovideo.com/c/product/1110712-REG/gra_vue_mrs_1204mvs_4_output_multi_viewer_display.html')
add(GF, 'gravue-vio-mvs-8hd', GV, 'VIO MVS-8HD', 'VIO MVS-8HD 8-input multiviewer, 1RU', 'VIO', 'monitor', 1,
    [R('in', 'HD-SDI', 'BNC', 8, 'SDI In'), R('out', 'HD-SDI', 'BNC', 8, 'SDI Loop'), R('out', 'HDMI', 'HDMI', 1, 'HDMI / DVI Out'), R('out', 'HD-SDI', 'BNC', 1, 'MV SDI Out'), LAN(1), AC(1)],
    'Check: counts.', 'B&H VIO MVS-8HD listing', 'https://www.bhphotovideo.com/c/product/936619-REG/gra_vue_vio_mvs_8hd_1u_multiviewer.html')
add(GF, 'gravue-xio-3u', GV, 'XIO 3U', 'XIO 3U modular platform', 'XIO', 'frame', 3,
    [R('io', 'Other', 'Card slot', 1, 'Module rears'), R('in', 'Reference', 'BNC', 1, 'Ref In'), LAN(1), AC(2)],
    'Modular frame for Gra-Vue converter / DA / multiviewer modules; card I/O added per device. Check: slot count.', 'Tanotis XIO listing',
    'https://www.tanotis.com/products/gra-vue-xio-3u-modular-platform')
add(GF, 'gravue-vio-mfc-x', GV, 'VIO MFC-X', 'VIO MFC-X universal video cross converter', 'VIO', 'converter', 1,
    [S3('in', 1, 'SDI In'), H('in', 1, 'HDMI In'), R('in', 'VGA', 'HD15', 1, 'VGA In'), S3('out', 2, 'SDI Out'), H('out', 1, 'HDMI Out'), DC()],
    'Half-rack box. Check: connectors.', 'Proflix Gra-Vue VIO listing', 'https://proflixsales.com/products/gravue-products/vio-series/gravue-vio-mfc-x-universal-video-cross-convertor', w=6)
MIO = {'w': 100, 'h': 25}
for pn, name, ports in (('MIO SDI-AVIEWER', 'MIO SDI-AVIEWER 3G-SDI to HDMI / DVI scaling converter', [S3('in', 1, 'SDI In'), S3('out', 1, 'SDI Loop'), H('out', 1, 'HDMI / DVI Out')]),
                        ('MIO MVS-4HD', 'MIO MVS-4HD quad HD/SD-SDI multiviewer', [R('in', 'HD-SDI', 'BNC', 4, 'SDI In'), H('out', 1, 'HDMI / DVI Out')]),
                        ('MIO MVS-4HDMI', 'MIO MVS-4HDMI quad HDMI multiviewer', [H('in', 4, 'HDMI In'), H('out', 1, 'HDMI Out')]),
                        ('MIO AV-AVIEWER', 'MIO AV-AVIEWER composite to HDMI / DVI converter', [R('in', 'Analog video', 'BNC', 1, 'CV In'), H('out', 1, 'HDMI / DVI Out')])):
    add(GF, 'gravue-' + pn.lower().replace(' ', '-'), GV, pn, name, 'MIO', 'converter', 1, ports + [DC('5V DC')], 'Mini box; sits on a shelf. Check: connectors.',
        'Gra-Vue MIO dealer listings', 'https://proflixsales.com/products/gravue-products/mio-series/gravue-mio-sdi-aviewer-hd-sd-sdi-to-hdmi-dvi-video-scaling', w=2, boxMm=MIO)

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
