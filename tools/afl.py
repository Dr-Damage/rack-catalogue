#!/usr/bin/env python3
"""AFL fibre enclosures (added 2026-11-14), mostly the FRE range sold in Australia and New Zealand:
  catalogue/afl.json  FRE sliding, static sliding, limited-depth sliding, wingback fixed and basic fixed enclosures (1RU-3RU) as
                      frames; the FRE clip-in adapter panels (flat or angled, LC duplex / SC / SC duplex / ST) and blanks as cards;
                      the fixed-fascia 1RU enclosures (36SCV, 48SCV) and the DENALI high-density housings as plain patch panels.
Same modelling as tools/fibre.py: the enclosure is a frame, each adapter panel is a card. Card front ports are the patch side;
the one included rear module is the inside of the adapters (pigtails spliced to the incoming cable).
Horizontal panels fit system 'AFL FRE'; the 12-position vertical (-V) enclosures take the vertical panels, system 'AFL FRE V'.
The SC/LC panels take SC simplex or LC duplex adapters in the same holes; they are listed loaded with LC duplex.
Specs from AFL's Oceania data sheets (each entry's source)."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
BOX = {'x0': 0.04, 'x1': 0.96, 'y0': 0.08, 'y1': 0.92}
F_ = 'afl.json'; MFR = 'AFL'; FIB = 'Fibre'
AU = 'https://www.aflglobal.com/en/au/'
def model(**m):
    m = dict(dict(manufacturer=MFR, widthCols=12, fullDepth=False, verified=True, portGroups=[]), **m)
    FILES.setdefault(F_, []).append(m)

# ======================= FRE enclosures (frames) =======================
SL = ('AFL FRE Sliding Enclosures data sheet (AFL Oceania)', AU + 'Products/Fibre-Enclosure-Racks/Rackmount-Enclosures/FRE-Sliding-Enclosure1RU-2RU-3RU')
SS = ('AFL FRE Static Sliding Enclosure data sheet (AFL Oceania)', AU + 'Products/Fibre-Enclosure-Racks/Rackmount-Enclosures/FRE-Static-Sliding-Enclosure1RU-2RU-3RU')
LD = ('AFL 1RU FRE Limited Depth Sliding Enclosure page', AU + 'products/fiber-optic-connectivity/rackmount-splice--patch-solutions/sliding-enclosures/1ru-fre-limited-depth-sliding-enclosure')
WB = ('AFL FRE Wingback Enclosures data sheet (AFL Oceania, 2020)', AU + 'Products/Fibre-Enclosure-Racks/Rackmount-Enclosures/FRE-Wingback-Fixed-Enclosure1RU-2RU-3RU')
BF = ('AFL Fibre Enclosures and Racks 1RU Fixed data sheet', AU + 'Products/Fiber-Optic-Connectivity/Rackmount-Splice--Patch-Solutions/Fixed-Enclosures/FRE-Basic-Fixed-Enclosure1RU')
CAP = {1: (2, '24 SC/ST/FC or 48 LC', '36 (72 double-stacked)'), 2: (4, '48 SC/ST/FC or 96 LC', '72 (144 double-stacked)'),
       3: (8, '96 SC/ST/FC or 192 LC', '144 (288 double-stacked)')}

def enclosure(pn, ru, kind, src, depth, kg, extra='', vertical=False, verified=True, w=433):
    if vertical:
        slots, fr = 12, dict(system='AFL FRE V', orient='v')
        fib = '144 SC or 288 LC'
    else:
        slots, fib, _ = CAP[ru]
        fr = dict(system='AFL FRE', orient='h', cols=2)
    spl = CAP[ru][2]
    lay = ('12 vertical adapter panel positions' if vertical else
           f'{slots} horizontal adapter panel positions, 2 side by side' + (' in 4 rows' if ru == 3 else ' per row' if ru == 2 else ''))
    model(id='afl-' + pn.lower(), partNumber=pn, name=f'{pn} FRE {ru}RU {kind} fibre enclosure, {slots} panels' + (' (vertical)' if vertical else ''),
          family='FRE', category='frame', ru=ru, verified=verified, source=src[0], productUrl=src[1], weightKg=kg,
          notes=f'{ru}RU {kind} enclosure, {lay}. Presents up to {fib} fibres; ' + (f'splices up to {spl}. ' if 'wingback' not in kind else 'splice capacity not stated (splice trays optional). ') + f'{w} mm wide, {depth} mm deep, '
                + (f'{kg} kg, ' if kg else '') + f'charcoal powder-coated steel. Panels are sold separately (FRE adapter panels or blanks). {extra}'
                + ('Check: panel layout (shown as 2 columns of 4).' if ru == 3 and not vertical else ''),
          frame=dict(fr, slots=slots, slotOrder='ltr', rearAlign=1, door=False, front=BOX, rear=BOX,
                     controller='None (passive). Takes FRE clip-in adapter panels; splice cassettes inside.'))

for ru, d, kg in ((1, 300, 4.2), (2, 330, 5.6), (3, 365, 6.6)):
    enclosure(f'FRE-{ru}RU-MOD-S', ru, 'sliding', SL, d, kg,
              'Full-extension sliding tray. Cable entry brackets: S (standard), SB/SFL (1RU only), SRP (rodent-proof). '
              + ('Fixed fascia options: 36SCV (36-port angled), 48SCV (48-port flat). ' if ru == 1 else
                 'Fixed fascia options: 72SCV (72-port angled), 96SCV (96-port flat). ' if ru == 2 else ''))
enclosure('FRE-3RU-MOD-S-V', 3, 'sliding', SL, 365, 6.6, 'Full-extension sliding tray, MOD12 vertical faceplate. ', vertical=True)
for ru, d in ((1, 330), (2, 330), (3, 365)):
    enclosure(f'FRE-{ru}RU-MOD-SS2', ru, 'static sliding', SS, d, None,
              'Sliding tray with fixed cable entry, so incoming cables do not move when the tray slides. SS2 entry takes up to 6 cables '
              '(SS2RP rodent-proof up to 4' + ('; SS3 up to 12' if ru > 1 else '') + '). ')
for ru, d, kg in ((1, 200, 3.1), (2, 200, 5.2), (3, 200, 6.2)):
    enclosure(f'FRE-{ru}RU-MOD-S2', ru, 'limited-depth sliding', LD, d, kg,
              'For shallow racks and wall cabinets. Full-extension sliding tray; angled inward rear bracket takes glands. '
              + ('Special order only. ' if ru == 3 else ''))
for ru, kg in ((1, 2.6), (2, 3.4), (3, 4.2)):
    enclosure(f'FRE-{ru}RU-MOD-WB', ru, 'wingback fixed', WB, 250, kg, w=434, extra=
              f'Fixed, removable lid. Angled left and right rear entries, no glands needed ({4 * ru} cables each side). '
              'Made for MTP and pre-terminated trunk cables. ' + ('Up to 4 half-size blanks (FRE-BLANK-SML) space 6 panels evenly. ' if ru == 3 else ''))
enclosure('FRE-3RU-MOD-WB-V', 3, 'wingback fixed', WB, 250, 4.2, w=434, extra=
          'Fixed, removable lid. Angled left and right rear entries, no glands needed (12 cables each side). ', vertical=True)
enclosure('FRE-1RU-MOD-F', 1, 'basic fixed', BF, 250, 4.0, w=435, extra='Fixed tray, twin-aperture modular front. Up to 2 incoming cables each side. ')
for n, kind in ((36, 'angled'), (48, 'flat')):
    pn = f'FRE-1RU-{n}SCV-F'
    model(id='afl-' + pn.lower(), partNumber=pn, name=f'{pn} FRE 1RU fixed fibre enclosure, {n} x LC duplex ({kind} fascia)', family='FRE',
          category='patch', ru=1, source=BF[0], productUrl=BF[1], weightKg=4.0,
          notes=f'1RU fixed enclosure with a {n}-port {kind} fixed fascia for SC simplex or LC duplex adapters ({n} SC or {2 * n} LC fibres). '
                f'435 x 250 mm, 4 kg. Up to 2 incoming cables each side. Shown loaded with LC duplex; the inside is shown as splices. '
                f'The sliding enclosures take the same fascia (part numbers ending -S).',
          portGroups=[F('io', FIB, 'LC duplex', n, 'LC'), R('in', FIB, 'Splice', 2 * n, 'Splice')])

# ======================= FRE adapter panels (cards) =======================
PN = ('AFL FRE adapter panel listings (AFL Oceania) and FRE data sheets', AU + 'products/fibre-enclosure-racks/panels-for-rackmount-and-wall-enclosures/sclc-duplex-6-port-panel-1-6hp-flat')
def panel(pn, name, conn, n, notes, fits='AFL FRE', label=None):
    label = label or (conn or '').split(' ')[0]
    model(id='afl-' + pn.lower().replace('/', '-'), partNumber=pn, name=name, family='FRE panels', category='card', ru=0, widthCols=0,
          source=PN[0], productUrl=PN[1], notes=notes, portGroups=[F('io', FIB, conn, n, label)] if n else [],
          card=dict(fits=[fits], slotWidth=1),
          rearModules=[dict(partNumber=pn, name='Rear (pigtail side)', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True,
                            portGroups=[R('io', FIB, conn, n, label)] if n else [])])
ANG = 'Angled versions -AL (angle left) and -AR (angle right) have the same ports. '
SCLC = 'The holes take SC simplex or LC duplex adapters; shown with LC duplex. '
panel('FRE-SC12D-FL1/12', 'FRE 12-port SC/LC duplex panel, flat (ports 1-12)', 'LC duplex', 12,
      SCLC + 'FRE-SC12D-FL13/24 is the same panel labelled 13-24. ' + 'Angled: FRE-SC12H-AL1/12, FRE-SC12H-AR1/12.')
panel('FRE-SC12H-AL1/12', 'FRE 12-port SC/LC duplex panel, angled left', 'LC duplex', 12, SCLC + ANG)
panel('FRE-SC06H-FL1/6', 'FRE 6-port SC/LC duplex panel, flat', 'LC duplex', 6, SCLC + ANG)
panel('FRE-SCD06D-FL1/12-C', 'FRE 6-port SC duplex panel, flat', 'SC', 12, 'Six SC duplex adapters (12 SC fibres). Angled: FRE-SCD06H-AL1/12, -AR1/12.')
panel('FRE-SCD03H-FL1/6-C', 'FRE 3-port SC duplex panel, flat', 'SC', 6, 'Three SC duplex adapters (6 SC fibres). ' + ANG)
panel('FRE-ST12D-FL1/12-C', 'FRE 12-port ST/FC panel, flat', 'ST', 12, 'ST or FC adapters; shown as ST. FRE-ST12D-FL13/24 is labelled 13-24.')
panel('FRE-ST06H-FL1/6-C', 'FRE 6-port ST/FC panel, flat', 'ST', 6, 'ST or FC adapters; shown as ST. ' + ANG)
panel('FRE-BLANK', 'FRE blank panel', None, 0, 'Blank for an unused panel position. FRE-BLANK-SML is the half-size blank for the 3RU 8-panel enclosures.')
panel('FRE-SC12V-AU', 'FRE 12-port SC/LC duplex vertical panel, angled', 'LC duplex', 12, SCLC + 'For the 12-position vertical (-V) enclosures. '
      'FRE-SC12V-AL1/12 and -AR13/24 are labelled versions.', fits='AFL FRE V')
panel('FRE-SC06V-AU', 'FRE 6-port SC/LC duplex vertical panel, angled', 'LC duplex', 6, SCLC + 'For the 12-position vertical (-V) enclosures.', fits='AFL FRE V')
panel('FRE-SCD06V-AU', 'FRE 6-port SC duplex vertical panel, angled', 'SC', 12, 'Six SC duplex adapters (12 SC fibres). For the vertical (-V) enclosures.',
      fits='AFL FRE V')
panel('FRE-BLANK-V', 'FRE vertical blank panel', None, 0, 'Blank for an unused vertical panel position.', fits='AFL FRE V')

# ======================= DENALI high-density housings =======================
DN = ('AFL DENALI Fiber Housings page', 'https://www.aflglobal.com/en/au/products/fiber-optic-connectivity/rackmount-splice--patch-solutions/denali-high-density-platform')
for ru, trays, h in ((1, 3, 44.5), (2, 6, 88.9), (4, 12, 177.8)):
    lc, mpo = 144 * ru, 12 * ru
    model(id=f'afl-denali-{ru}ru-s', partNumber=f'DENALI-{ru}RU-S', name=f'DENALI {ru}RU high-density fibre housing, {lc // 2} x LC duplex',
          family='DENALI', category='patch', ru=ru, verified=False, source=DN[0], productUrl=DN[1],
          notes=f'{ru}RU housing with {trays} sliding trays that lock open; cassettes load from front or rear. Up to {lc} LC fibres '
                f'(or {lc * 6} fibres as MPO pass-through). Shown loaded with {4 * trays} BASE-12 MPO-LC cassettes: {lc // 2} LC duplex in front, '
                f'{mpo} MPO12 trunks at the rear. 501.6 mm deep. Check: cassette mix (BASE-8 and BASE-24 cassettes also fit).',
          portGroups=[F('io', FIB, 'LC duplex', lc // 2, 'LC'), R('in', FIB, 'MPO/MTP', mpo, 'MPO')])

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    for m in ms:
        if m.get('weightKg') is None: m.pop('weightKg', None)
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
