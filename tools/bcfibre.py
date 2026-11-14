#!/usr/bin/env python3
"""Generates broadcast fibre transport and camera-fibre panels (added 2026-11-14):
  catalogue/multidyne.json  MultiDyne VF-9000 VersaFrame (1RU, 9 I/O cards, 18 SFP cages), HoneyBadger local/remote, Crescendo.
  catalogue/telecast.json   Telecast Fiber Systems Python II 1RU SDI fibre TX/RX/transceivers.
  catalogue/lightware.json  Lightware MX2 HDMI 2.0 matrix switchers.
  catalogue/smpte-fibre.json  SMPTE 311M camera fibre panels: Camplex HYMOD 1RU modular frame and modules, Camplex HF-1RU-10X
                            universal LEMO feed-through panel, Canford LEMO 3K.93C EDW/FXW panel connectors with breakout tails.
Opticomm (Emcore Optiva) was looked at: its rack gear is composite-video insert cards in a 16-slot cage with no published
rack height or panel layout, so nothing was added.
Specs come from the makers' data sheets and manuals (each entry's source). 'Check:' marks anything not confirmed."""
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
def frame(file, id, mfr, pn, name, fam, ru, fr, notes, src, url, verified=True, ports=None, **kw):
    fr = dict(dict(slotOrder='ltr', rearAlign=1, door=False, front=BOX, rear=BOX), **fr)
    add(file, id, mfr, pn, name, fam, 'frame', ru, ports or [], notes, src, url, verified, frame=fr, **kw)
def card(file, id, mfr, pn, name, fam, fits, front, rear, notes, src, url, verified=True, rearName='Rear', color=None, **kw):
    c = dict(fits=fits, slotWidth=1)
    if color: c['color'] = color
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category='card', ru=0, widthCols=0, fullDepth=False,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=front, card=c,
             rearModules=[dict(partNumber=pn, name=rearName, width=1, cardsPerModule=1, cardOffset=0, default=True,
                               included=True, portGroups=rear)])
    m.update(kw); FILES.setdefault(file, []).append(m)
SDI = 'SDI'

# ======================= MultiDyne =======================
MD = 'MultiDyne'
VF_SRC, VF_URL = 'MultiDyne VF-9000 data sheet (preliminary, 2026-03)', 'https://www.multidyne.com/product/vf-9000.html'
VF_NOTE = ('1RU frame with 9 rear I/O card slots and dual internal hot-swap PSUs (C13 cords, 25 W max). Each video card has 2 BNCs '
           '(or 4 HD-BNCs) on the rear and one or two SFP cages on the front; BNC direction follows the SFP fitted (dual TX SFP makes '
           'inputs, dual RX makes outputs). Muxed (-2M) versions carry 36 signals on 2 single-mode fibres through the internal CWDM '
           'mux (LC on the front); -FP versions use one fibre per channel from the SFPs. Other cards: audio, MADI, serial/GPIO, Ethernet, '
           'HDMI, genlock. 483 x 191 mm deep. ')
for pn, name, tx, rx in (('VF9K-NNNNGGGGK-2M-A', '18 x 18 SDI transceiver, muxed (A end)', 18, 18),
                         ('VF9K-NNNNNNNNN-2M-A', '36 x SDI transmitter, muxed', 36, 0),
                         ('VF9K-GGGGGGGGG-2M-B', '36 x SDI receiver, muxed', 0, 36)):
    ports = []
    if tx: ports.append(R('in', SDI, 'BNC', tx, 'SDI In'))
    if rx: ports.append(R('out', SDI, 'BNC', rx, 'SDI Out'))
    ports += [F('io', 'Fibre', 'SFP', 18, 'SFP'), F('io', 'Fibre', 'LC duplex', 1, 'CWDM mux'), F('io', 'Ethernet', 'RJ45', 1, 'Web UI / SNMP'),
              R('in', 'Power', 'IEC C14', 2, 'PSU')]
    add('multidyne.json', 'multidyne-' + pn.lower(), MD, pn, f'VF-9000 VersaFrame {name}', 'VF-9000', 'converter', 1, ports,
        VF_NOTE + 'Ports shown with 2 BNCs per channel position (4 channels per card on muxed units, 2 BNCs each in and out). '
        'Check: exact BNC count of this configuration and where the management port is (on the front here).', VF_SRC, VF_URL, verified=False,
        powerW=25)
HB_SRC, HB_URL = 'MultiDyne HoneyBadger data sheet (2024-11)', 'https://www.multidyne.com/product/honeybadger.html'
for pn, ru, name, au, ic, pw, kg, d in (('HB-DC-DBR-12G', 5, 'HoneyBadger remote (field) unit, 8 x 8 12G-SDI', 'mic/line', '4 x 2-wire', 200, 10, 318),
                                       ('HB-DC-DBL-12G', 4, 'HoneyBadger local (truck / studio) unit, 8 x 8 12G-SDI', 'line', '4 x 4-wire', 40, 7, 262)):
    ports = [F('in', SDI, 'BNC', 8, 'SDI In'), F('out', SDI, 'BNC', 8, 'SDI Out'), F('in', 'Audio', 'XLR3 female', 8, f'Audio In ({au})'),
             F('out', 'Audio', 'XLR3 male', 8, 'Audio Out'),
             F('io', 'Intercom', 'XLR3 male' if 'remote' in name else 'RJ45', 4, 'Intercom ' + ic.split(' x ')[1]),
             F('io', 'Ethernet', 'RJ45', 2, 'GbE'), F('io', 'Other', 'Phoenix', 2, 'RS-232/422/485'), F('io', 'GPIO', 'Phoenix', 2, 'GPI/Tally'),
             F('io', 'Fibre', 'opticalCON DUO', 1, 'Fibre (N2 option)'), F('in', 'Power', 'IEC C14', 1, 'AC In')]
    add('multidyne.json', 'multidyne-' + pn.lower(), MD, pn, name, 'HoneyBadger', 'converter', ru, ports,
        f'Fibre-linked pair (one remote, one local) carrying 8 SDI each way, audio, intercom, data and 2 x GbE. Order -N2 for an opticalCON '
        f'DUO fibre port or -ST2 for dual ST (LEMO 304M also offered); -AB / -V adds an Anton Bauer or V-mount battery plate. '
        f'{pw} W max, {d} mm deep without handles, {kg} kg. 3G versions replace 12G in the part number. '
        'Check: which connectors are on the front and which on the rear (shown all on the front).',
        HB_SRC, HB_URL, verified=False, powerW=pw, weightKg=kg)

# ======================= Telecast Python II =======================
TC_SRC, TC_URL = 'Telecast Python II manual (Grass Valley)', 'https://www.grassvalley.com/docs/Manuals/purple/Python_II/Python_II_Manual.pdf'
for pn, name, tx, rx, fib in (('P2-TX16-SL-ST', '16-channel SDI fibre transmitter', 16, 0, 16), ('P2-RX16-L-ST', '16-channel SDI fibre receiver', 0, 16, 16),
                              ('P2-TX8-SL-ST', '8-channel SDI fibre transmitter', 8, 0, 8), ('P2-RX8-L-ST', '8-channel SDI fibre receiver', 0, 8, 8),
                              ('P2-TR-8X8-SL-ST', '8 x 8 SDI fibre transceiver', 8, 8, 16),
                              ('P2-TX16-13CW-ST', '16-channel SDI fibre transmitter, CWDM', 16, 0, 2),
                              ('P2-RX16-13CW-ST', '16-channel SDI fibre receiver, CWDM', 0, 16, 2)):
    ports = ([F('in', SDI, 'BNC', tx, 'SDI In')] if tx else []) + ([F('out', SDI, 'BNC', rx, 'SDI Out')] if rx else [])
    ports += [R('io', 'Fibre', 'ST', fib, 'Fibre'), R('in', 'Power', 'XLR4', 2, 'DC In 12-24 V')]
    add('telecast.json', 'telecast-' + pn.lower(), 'Telecast Fiber Systems', pn, f'Python II {name}', 'Python II', 'converter', 1, ports,
        'Python II 1RU SDI over fibre (SD/HD/3G). BNCs on the front, ST fibres on the rear (one per channel, or '
        + ('2 fibres with the CWDM option). ' if 'CW' in pn else 'use the -13CW version for 1 or 2 fibres). ') +
        'Two 4-pin XLR DC inputs (12-24 V, 1.5 A, external adapters) for redundancy. 424 x 267 mm deep. Telecast is now part of Grass Valley; '
        'Python II is a legacy product.', TC_SRC, TC_URL)

# ======================= Lightware MX2 =======================
LW = 'Lightware'
LW_URL = 'https://lightware.com/mx2-hdmi20-matrix-switchers'
def lw(pn, n, ru, ports, notes, src, **k):
    add('lightware.json', 'lightware-' + pn.lower(), LW, pn, f'{pn} {n}x{n} HDMI 2.0 matrix switcher', 'MX2', 'router', ru,
        [R('in', 'HDMI', 'HDMI', n, 'HDMI In'), R('out', 'HDMI', 'HDMI', n, 'HDMI Out')] + ports + [F('io', 'USB', 'USB mini-B', 1, 'USB control')],
        'HDMI 2.0 (18 Gbps, 4K60 4:4:4) matrix with embedded audio. Front LCD and jog dial, USB mini-B control on the front; video, audio, '
        'power, RS-232 and LAN on the rear. ' + notes, f'Lightware {pn} A&E specification', LW_URL, **k)
lw('MX2-8x8-HDMI20-L', 8, 1, [R('io', 'RS-232', 'Phoenix', 1, 'RS-232'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
   '1RU, no power switch. 442 x 277 mm deep.', 'MX2-8x8-HDMI20-L')
lw('MX2-16x16-HDMI20-R', 16, 3, [R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Ethernet', 'etherCON', 1, 'LAN'), R('in', 'Power', 'powerCON', 2, 'AC In')],
   'Redundant PSUs on two powerCON inputs. 47 W idle / 83 W max, 3RU, 280 mm deep.', 'MX2-16x16-HDMI20-R', powerW=83)
lw('MX2-24x24-HDMI20', 24, 4, [R('io', 'RS-232', 'Phoenix', 1, 'RS-232'), R('io', 'Ethernet', 'etherCON', 1, 'LAN'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
   '4RU, 280 mm deep. The -R version adds redundant PSUs (powerCON).', 'MX2-24x24-HDMI20')
lw('MX2-32x32-HDMI20-A-R', 32, 8, [R('in', 'Audio', 'Phoenix', 32, 'Analog In'), R('out', 'Audio', 'Phoenix', 32, 'Analog Out'),
                                   R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Ethernet', 'etherCON', 1, 'LAN'), R('in', 'Power', 'powerCON', 2, 'AC In')],
   'Analog audio in and out (5-pole Phoenix) beside each video port, redundant PSUs. 8RU, 280 mm deep. Check: analog audio port count.',
   'MX2-32x32-HDMI20-A-R', verified=False)
lw('MX2-48x48-HDMI20-A-R', 48, 8, [R('in', 'Audio', 'Phoenix', 16, 'Analog In'), R('out', 'Audio', 'Phoenix', 16, 'Analog Out'),
                                   R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Ethernet', 'etherCON', 1, 'LAN'), R('in', 'Power', 'powerCON', 2, 'AC In')],
   '16 analog audio in and out (5-pole Phoenix), redundant PSUs. 108 W idle / 203 W max, 8RU, 280 mm deep.', 'MX2-48x48-HDMI20-A-R', powerW=203)

# ======================= SMPTE camera fibre panels =======================
SF = 'smpte-fibre.json'
CX = 'Camplex'
LEMO = 'LEMO 3K.93C (SMPTE 304)'
HY_SRC, HY_URL = 'Camplex HYMOD-FR1 listing (Markertek)', 'https://www.markertek.com/product/hymod-fr1/camplex-hymod-fr1-hymod-smpte-modular-1ru-frame-kit-for-6-hymod-modules'
frame(SF, 'camplex-hymod-fr1', CX, 'HYMOD-FR1', 'HYMOD-FR1 SMPTE modular 1RU frame, 6 modules', 'HYMOD', 1,
      dict(system='Camplex HYMOD 1RU', slots=6, orient='v', controller='None (passive). Takes HYMOD 1RU modules.'),
      '1RU frame for 6 interchangeable HYMOD modules (SMPTE hybrid camera connectors, fibre or BNC feed-throughs). Mounts flush or recessed. '
      'The 2RU HYMOD-2Rxx modules do not fit.', HY_SRC, HY_URL)
AMP5 = ('Power', 'Other', '5-pin AMP')
for pn, name, front, rear in (
        ('HYMOD-1R01', 'SMPTE FXW plug to 2 ST + 5-pin AMP', [F('io', 'Fibre', LEMO, 1, 'SMPTE FXW plug')], [R('io', 'Fibre', 'ST', 2, 'Fibre'), R('io', 'Power', 'Other', 1, '5-pin AMP')]),
        ('HYMOD-1R02', 'SMPTE EDW jack to 2 ST + 5-pin AMP', [F('io', 'Fibre', LEMO, 1, 'SMPTE EDW jack')], [R('io', 'Fibre', 'ST', 2, 'Fibre'), R('io', 'Power', 'Other', 1, '5-pin AMP')]),
        ('HYMOD-1R05', 'SMPTE FXW plug to 2 ST + 6-pin AMP', [F('io', 'Fibre', LEMO, 1, 'SMPTE FXW plug')], [R('io', 'Fibre', 'ST', 2, 'Fibre'), R('io', 'Power', 'Other', 1, '6-pin AMP')]),
        ('HYMOD-1R06', 'SMPTE EDW jack to 2 ST + 6-pin AMP', [F('io', 'Fibre', LEMO, 1, 'SMPTE EDW jack')], [R('io', 'Fibre', 'ST', 2, 'Fibre'), R('io', 'Power', 'Other', 1, '6-pin AMP')]),
        ('HYMOD-1R25', '45-degree SMPTE EDW jack to 2 LC + 6-pin AMP', [F('io', 'Fibre', LEMO, 1, 'SMPTE EDW jack')], [R('io', 'Fibre', 'LC simplex', 2, 'Fibre'), R('io', 'Power', 'Other', 1, '6-pin AMP')]),
        ('HYMOD-1R07', '4 x ST fibre feed-through', [F('io', 'Fibre', 'ST', 4, 'ST')], [R('io', 'Fibre', 'ST', 4, 'ST')]),
        ('HYMOD-1R08', 'opticalCON DUO LC feed-through', [F('io', 'Fibre', 'opticalCON DUO', 1, 'opticalCON DUO')], [R('io', 'Fibre', 'LC duplex', 1, 'LC')]),
        ('HYMOD-1R09', '3 x BNC feed-through', [F('io', SDI, 'BNC', 3, 'BNC')], [R('io', SDI, 'BNC', 3, 'BNC')]),
        ('HYMOD-1R10', 'blank module', [], [])):
    card(SF, 'camplex-' + pn.lower(), CX, pn, f'{pn} {name}', 'HYMOD', ['Camplex HYMOD 1RU'], front, rear,
         'HYMOD 1RU module. ' + ('The SMPTE 311M hybrid connector (LEMO 3K.93C) is on the front; fibres and the camera power contacts break '
                                 'out on the rear. ' if front and front[0]['connector'] == LEMO else 'Passive feed-through. ' if front else 'Blanks an unused position. ')
         + ('Check: which side is front (the listing gives the pairing only). ' if front else ''), HY_SRC, HY_URL, verified=not front)
frame(SF, 'camplex-hf-1ru-10x', CX, 'HF-1RU-10X', 'HF-1RU-10X universal SMPTE feed-through panel, 10 positions', 'SMPTE panels', 1,
      dict(system='SMPTE LEMO panel hole', slots=10, orient='v', controller='None (passive). Takes LEMO 3K.93C panel connectors (FMW, FXW, EDW, PBW).'),
      '1RU flanged aluminium panel with 10 universal cut-outs for any LEMO SMPTE panel connector (plug or socket); 8 blanks included. '
      'Add the connectors as cards, for example the Canford breakout assemblies.', 'Camplex HF-1RU-10X listing (Markertek)',
      'https://markertek.com/product/hf-1ru-10x/camplex-1ru-10-position-universal-smpte-feedthru-panel')
CF_SRC, CF_URL = 'Canford SMPTE311M Lemo panel breakout assemblies page', 'https://www.canford.co.uk/CANFORD-SMPTE311M-HYBRID-FIBRE-CAMERA-CABLE-BREAKOUT-ASSEMBLIES-With-Lemo-panel-type-connectors'
for pn, kind, fib in (('50-1117', 'EDW', 'LC simplex'), ('50-1118', 'EDW', 'ST'), ('50-1127', 'FXW', 'LC simplex'), ('50-1128', 'FXW', 'ST')):
    side = 'panel socket (camera cable plugs in)' if kind == 'EDW' else 'panel plug'
    card(SF, 'canford-' + pn, 'Canford', pn, f'{pn} LEMO 3K.93C {kind} {side}, {fib.split()[0]} + 6-way tails',
         'SMPTE panel connectors', ['SMPTE LEMO panel hole'],
         [F('io', 'Fibre', LEMO, 1, f'SMPTE {kind}')],
         [R('io', 'Fibre', fib, 2, 'Fibre tail'), R('io', 'Power', 'Other', 1, '6-way MATE-N-LOK tail')],
         f'SMPTE 311M hybrid {kind} {side} with 250 mm breakout tails: two {fib.split()[0]} fibres and a 6-way MATE-N-LOK plug for the camera '
         'power and control contacts. Other tail lengths and SC or unterminated versions are listed on the same page.', CF_SRC, CF_URL,
         rearName='Breakout tails')

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
