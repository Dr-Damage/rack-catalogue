#!/usr/bin/env python3
"""Generates the modular fibre patch catalogue (added 2026-11-14):
  catalogue/corning.json   Corning Closet Connector Housings (CCH-01U..04U) as frames; CCH LC adapter panels and CCH pigtailed
                           splice cassettes as cards.
  catalogue/panduit.json   Panduit Opticom FCE1U/2U/4U enclosures as frames; FAP adapter panels and QuickNet MTP cassettes as cards.
  catalogue/neutrik.json   Neutrik opticalCON angled rack panels (NZP1RU-8/-12) and Z-panel frames (NZPF1RU/NZPF3RU) as frames
                           with D-size positions; opticalCON DUO and QUAD chassis connectors as cards.
Fixed Canare fibre splice panels are in canare.json (tools/canare.py); the Canare keystone fibre splice panels are added here
to canare-fibre.json.

How it is drawn: the enclosure is a frame, each adapter panel / cassette / connector is a card. The card's front ports
(card.portGroups, face front) are the patch side; its one rear module carries the trunk side (LC, MPO/MTP or splices) and is
included with the card. Schema: catalogue/FRAMES.md. Notes start any doubt with "Check:"."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
BOX = {'x0': 0.04, 'x1': 0.96, 'y0': 0.08, 'y1': 0.92}

def frame(file, id, mfr, pn, name, fam, ru, fr, notes, src, url, verified=True, ports=None, **kw):
    fr = dict(dict(slotOrder='ltr', rearAlign=1, door=False, front=BOX, rear=BOX), **fr)
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category='frame', ru=ru, widthCols=12,
             fullDepth=False, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports or [], frame=fr)
    m.update(kw); FILES.setdefault(file, []).append(m)

def card(file, id, mfr, pn, name, fam, fits, front, rear, notes, src, url, verified=True, rearName='Rear (trunk side)', color=None, **kw):
    c = dict(fits=fits, slotWidth=1)
    if color: c['color'] = color
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category='card', ru=0, widthCols=0, fullDepth=False,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=front, card=c,
             rearModules=[dict(partNumber=pn, name=rearName, width=1, cardsPerModule=1, cardOffset=0, default=True,
                               included=True, portGroups=rear)])
    m.update(kw); FILES.setdefault(file, []).append(m)

FIB = 'Fibre'

# ======================= Corning CCH =======================
CCH_URL = 'https://ecatalog.corning.com/optical-communications/US/en/p/closet-connector-housing-cch'
CCH_SRC = 'Corning CCH housing specifications and LAN-3414 brochure'
for ru, n, layout in [(1, 2, dict(orient='h', cols=2)), (2, 4, dict(orient='h', cols=2)), (3, 6, dict(orient='h', cols=2)),
                      (4, 12, dict(orient='v'))]:
    pn = f'CCH-0{ru}U'
    frame('corning.json', f'corning-cch-0{ru}u', 'Corning', pn, f'{pn} Closet Connector Housing, {n} CCH panels', 'CCH housings', ru,
          dict(system='Corning CCH', slots=n, **layout,
               controller='None (passive). Slots take CCH connector panels, CCH pigtailed splice cassettes or CCH Plug & Play modules.'),
          f'{ru}U 19-inch fibre housing for {n} CCH connector panels, cassettes or modules (up to {n * 24} fibres with 24-fibre panels). '
          + ('483 x 430 x 44 mm, 3.9 kg. ' if ru == 1 else '483 x 433 x 178 mm, 7.5 kg shipping. ' if ru == 4 else '')
          + ('Slide-out tray with removable translucent top cover. Panels lie flat, two side by side. ' if ru < 4 else
             'Front and rear sliding lockable doors. Panels stand side by side. ')
          + 'Accepts 19 or 23-inch racks. Splice trays go in through the CCH-CS pigtailed splice cassettes (or a CCH-CS-PST pass-through '
          'splice cassette, which has no adapters). The panel drawing shows the patch side only. '
          + ('Check: panel order (left to right, then up). ' if ru in (2, 3) else ''),
          CCH_SRC, CCH_URL if ru != 4 else 'https://ecatalog.corning.com/optical-communications/EMEA/en/Fiber-Optic-Hardware/Housings/Closet-Connector-Housing-(CCH)/p/CCH-04U',
          verified=ru in (1, 4))
CODES = {'A9': ('OS2 single-mode, UPC', 'blue'), 'B3': ('OS2 single-mode, APC', 'green'), 'AE': ('OS2 single-mode, UPC, shuttered', 'blue'),
         'E4': ('OM3/OM4 50 um multimode', 'aqua'), 'AD': ('OM3/OM4 50 um multimode, shuttered', 'aqua'),
         'D3': ('OM2 50 um multimode', 'black'), 'A8': ('OM1 62.5 um multimode', 'beige')}
CCH_PANELS = [(f, c) for c in ('A9', 'B3', 'E4', 'D3', 'A8') for f in (6, 8, 12, 16, 24)] + [(12, 'AE'), (24, 'AE'), (36, 'AE'), (12, 'AD')]
for fibres, code in CCH_PANELS:
    pn = f'CCH-CP{fibres:02d}-{code}'
    kind, colour = CODES[code]
    a = fibres // 2
    card('corning.json', 'corning-' + pn.lower(), 'Corning', pn, f'{pn} CCH panel, {a} x LC duplex ({fibres}F, {kind.split(",")[0]})',
         'CCH connector panels', ['Corning CCH'], [F('io', FIB, 'LC duplex', a, 'LC')], [R('io', FIB, 'LC duplex', a, 'LC')],
         f'CCH connector panel with {a} LC duplex adapters ({fibres} fibres), {kind}, {colour} adapters. Patch cords plug in the front; '
         'the rear takes pigtails, a trunk fan-out or field connectors.', 'Corning CCH panel, LC adapters (e-catalogue)',
         'https://ecatalog.corning.com/optical-communications/US/en/p/closet-connector-housing-cch-panel-lc-adapters',
         color={'blue': '#2f6fd1', 'green': '#2e9b4f', 'aqua': '#21b5c4', 'black': '#333333', 'beige': '#c9b38a'}[colour])
for pn, fibres, code, kind, splice in [('CCH-CS12-A9-P00RE', 12, 'A9', 'OS2 single-mode, UPC', 'single-fibre'),
                                       ('CCH-CS24-A9-P00RE', 24, 'A9', 'OS2 single-mode, UPC', 'single-fibre'),
                                       ('CCH-CS12-E4-P00QE', 12, 'E4', 'OM4 multimode', 'single-fibre'),
                                       ('CCH-CS24-AE-P00RJ', 24, 'AE', 'OS2 single-mode, UPC, shuttered', '12-fibre ribbon')]:
    a = fibres // 2
    card('corning.json', 'corning-' + pn.lower(), 'Corning', pn, f'{pn} CCH pigtailed splice cassette, {a} x LC duplex ({fibres}F)',
         'CCH splice cassettes', ['Corning CCH'], [F('io', FIB, 'LC duplex', a, 'LC')], [R('in', FIB, 'Splice', fibres, 'Splice')],
         f'Splice cassette preloaded with {fibres} pigtails and an LC duplex panel ({kind}), for {splice} fusion splicing of the incoming '
         'cable inside the housing. Part number: CCH-CS<fibres>-<adapter>-P00<fibre type><splice type>.', CCH_SRC,
         'https://www.corning.com/catalog/coc/documents/brochures/LAN-3414-AEN.pdf', rearName='Splice tray (inside)',
         color='#21b5c4' if code == 'E4' else '#2f6fd1')

# ======================= Panduit Opticom FCE =======================
PAN_SRC = 'Panduit Opticom QuickNet enclosure and FAP spec sheet'
PAN_URL = 'https://media.onlinecomponents.com/productfiles/mf-pn/109881.pdf'
for ru, n, layout in [(1, 4, dict(orient='h', cols=4)), (2, 8, dict(orient='h', cols=4)), (4, 12, dict(orient='v'))]:
    pn = f'FCE{ru}U'
    frame('panduit.json', f'panduit-fce{ru}u', 'Panduit', pn, f'{pn} Opticom fibre enclosure, {n} FAP/FMP panels or cassettes',
          'Opticom FCE enclosures', ru, dict(system='Panduit FAP', slots=n, **layout,
                                             controller='None (passive). Slots take FAP/FMP adapter panels or QuickNet cassettes.'),
          f'{ru}U enclosure, 447 mm wide, about 426 mm deep. Holds {n} FAP or FMP adapter panels or QuickNet cassettes: up to {n * 24} fibres with '
          '12-duplex LC panels. Front and rear doors. ' + ('FCE1UA is the open-access version. ' if ru == 1 else '')
          + ('Panels lie flat, four side by side. ' if ru < 4 else 'Panels stand side by side. ')
          + ('Check: panel order (left to right, then up). ' if ru == 2 else ''),
          PAN_SRC, f'https://www.panduit.com/en/products/fiber-optic-systems/fiber-optic-panels-cassettes-enclosures/fiber-optic-enclosures/fce{ru}u.html')
for pn, n, conn, kind, colour, note in [
        ('FAP12WBUDLCZ', 12, 'LC duplex', 'OS1/OS2 single-mode', 'blue', ''),
        ('FAP6WBUDLCZ', 6, 'LC duplex', 'OS1/OS2 single-mode', 'blue', ''),
        ('FAP12WAQDLC', 12, 'LC duplex', 'OM3/OM4 10Gig multimode', 'aqua', 'Check: current part number may end in Z (zirconia sleeves). '),
        ('FAP6WAQDLC', 6, 'LC duplex', 'OM3/OM4 10Gig multimode', 'aqua', 'Check: current part number may end in Z (zirconia sleeves). '),
        ('FAP6WAQDSC', 6, 'SC', 'OM3/OM4 10Gig multimode', 'aqua', 'Check: current part number may end in Z. '),
        ('FAP3WAQDSC', 3, 'SC', 'OM3/OM4 10Gig multimode', 'aqua', 'Check: current part number may end in Z. '),
        ('FAP6WST', 6, 'ST', 'multimode or single-mode', 'grey', '')]:
    simplex = conn in ('SC', 'ST') and pn != 'FAP6WST'
    count = n * 2 if simplex else n
    what = f'{n} duplex SC' if simplex else (f'{n} simplex ST' if conn == 'ST' else f'{n} duplex LC')
    card('panduit.json', 'panduit-' + pn.lower(), 'Panduit', pn, f'{pn} FAP adapter panel, {what} ({kind})', 'Opticom FAP adapter panels',
         ['Panduit FAP'], [F('io', FIB, conn, count, conn)], [R('io', FIB, conn, count, conn)],
         f'Fibre adapter panel with {what} adapters, {kind}, {colour}. ' + note,
         PAN_SRC if 'BU' not in pn else 'Panduit FAP product listings', PAN_URL if 'BU' not in pn else
         'https://crescentelectric.com/product/59762/opticom-fap-os2-12-lc-duplex-blue',
         color={'blue': '#2f6fd1', 'aqua': '#21b5c4', 'grey': '#888888'}[colour])
for pn, kind, colour in [('FCXO-24-10Y', 'OM3/OM4 10Gig', 'aqua'), ('FCXO-12-10Y', 'OM3/OM4 10Gig', 'aqua'), ('FCXO-12-3Y', 'OM3/OM4 10Gig', 'aqua'),
                         ('FC5-24-10Y', 'OM2 50/125', 'black'), ('FC9-24-10Y', 'OS1 single-mode', 'blue'), ('FC9-12-10Y', 'OS1 single-mode', 'blue'),
                         ('FC9-12-3Y', 'OS1 single-mode', 'blue')]:
    fibres = int(pn.split('-')[1]); sc = pn.endswith('-3Y')
    front = F('io', FIB, 'SC', fibres, 'SC') if sc else F('io', FIB, 'LC duplex', fibres // 2, 'LC')
    card('panduit.json', 'panduit-' + pn.lower(), 'Panduit', pn,
         f'{pn} QuickNet MTP cassette, {fibres // 2} x {"SC" if sc else "LC"} duplex to {fibres // 12} x MTP ({kind})',
         'QuickNet MTP cassettes', ['Panduit FAP'], [front], [R('io', FIB, 'MPO/MTP', fibres // 12, 'MTP')],
         f'Pre-terminated cassette: {fibres // 2} duplex {"SC" if sc else "LC"} adapters on the front, {fibres // 12} x 12-fibre MTP on the rear '
         f'for a QuickNet trunk, {kind}. Fits FCE enclosures and FAP/FMP-style patch panels.', PAN_SRC, PAN_URL,
         color={'blue': '#2f6fd1', 'aqua': '#21b5c4', 'black': '#333333'}[colour])

# ======================= Neutrik opticalCON =======================
NEU = 'https://www.neutrik.com/product/'
NEU_SRC = 'Neutrik product pages and Canford opticalCON panel listing'
for pn, n, layout, note in [
        ('NZP1RU-8', 8, dict(orient='v'), 'Angled 1U rack panel with 8 D-size cutouts for opticalCON ADVANCED chassis connectors. Made to order. '),
        ('NZP1RU-12', 12, dict(orient='v'), 'Angled 1U rack panel with 12 D-size cutouts for opticalCON ADVANCED chassis connectors. Made to order. '),
        ('NZPF1RU', 2, dict(orient='h', cols=2), '1U Z-panel frame with a 45-degree angled outlet, for up to 2 plates (NZPFD single-D plates or '
         'NZPFBP blanks; not the dual NZPFD-2). Each position here is one NZPFD plate. Made for tight OB truck I/O panels. '),
        ('NZPF3RU', 9, dict(orient='v'), '3U Z-panel frame for up to 9 plates angled up or down. Each position here is one NZPFD single-D plate; '
         'with NZPFD-2 dual plates the frame takes 18 connectors (add the second connector of a plate as another device). ')]:
    frame('neutrik.json', 'neutrik-' + pn.lower(), 'Neutrik', pn, f'{pn} opticalCON panel, {n} D-size positions', 'opticalCON rack panels',
          int(pn[4]) if pn.startswith('NZPF') else 1, dict(system='D-size hole', slots=n, **layout,
                                                         controller='None (passive). Each position takes one D-size chassis connector.'),
          note + 'Chassis connectors (cards here) and plates are bought separately.', NEU_SRC, NEU + pn.lower(),
          verified=True)
for pn, name, front, rear, note in [
        ('NO2-4FDW-A', 'opticalCON DUO ADVANCED chassis connector', [F('io', FIB, 'opticalCON DUO', 1, 'opticalCON DUO')],
         [R('io', FIB, 'LC duplex', 1, 'LC')], '2-channel rugged fibre feed-through: opticalCON DUO on the front, standard LC duplex on the rear. '),
        ('NO4FDW-A', 'opticalCON QUAD ADVANCED chassis connector', [F('io', FIB, 'opticalCON QUAD', 1, 'opticalCON QUAD')],
         [R('io', FIB, 'LC simplex', 4, 'LC')], '4-channel rugged fibre feed-through: opticalCON QUAD on the front, four LC connectors on the rear. ')]:
    card('neutrik.json', 'neutrik-' + pn.lower(), 'Neutrik', pn, f'{pn} {name}', 'opticalCON chassis', ['D-size hole'], front, rear,
         note + 'D-size mounting, metal shutter, IP65 when mated with an SCDP gasket. Gasket colours: black multimode, blue single-mode PC, '
         'green single-mode APC.', 'Neutrik product page', NEU + pn.lower())

# ======================= Canare keystone fibre splice panels =======================
for pn, fib in [('K24FCE-S24-1U-BLK', 24), ('K24FCE-S48-1U-BLK', 48)]:
    m = dict(id='canare-' + pn.lower(), manufacturer='Canare', partNumber=pn, name=f'{pn} 24-hole keystone fibre splice panel ({fib}F)',
             family='Fibre Splice Unit', category='patch', ru=1, widthCols=12, fullDepth=False, verified=True,
             source='Canare product page (Fiber-Optic Splice Unit)', productUrl='https://www.canare.co.jp/en/products/fiber_optic_systems/index.php?tid=1_059',
             notes=f'1RU splice panel with 24 keystone positions and splice trays for {fib} fibres. Keystone couplers are sold separately: FKDLJ-JS '
                   '(LC duplex SM), FKSJ-JS (SC SM), FKDLJ-JM (LC duplex MM), FKSJ-JM (SC MM), FKMPJ-JM (MPO MM). Unloaded as listed; '
                   'rename the front ports once couplers are fitted.',
             portGroups=[F('io', FIB, 'Keystone', 24, 'Keystone'), R('in', FIB, 'Splice', fib, 'Splice')])
    FILES.setdefault('canare-fibre.json', []).append(m)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
