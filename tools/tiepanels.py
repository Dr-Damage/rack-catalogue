"""Tie-line panels, D-series punched panels, wall/floor boxes and MUSA video jackfields -> catalogue/tiepanels.json.

Feed-through entries carry `thru {holes, rows, prefix, insert, fixed}`: the app gives each fitted hole a "<prefix>n front" and
"<prefix>n rear" port joined straight through, and follows tie lines through them. D-series punched panels and boxes have
fixed=false, so the insert (BNC, XLR, etherCON, HDMI, opticalCON, SMPTE LEMO...) is chosen per hole on the placed unit.
Insert keys: bnc xlr3f xlr3m xlr5f ethercon rj45 hdmi usb ocduo lc smpte db25 db9 speakon trs blank.
MUSA jackfields use the `jack` block (see jackfields.py). Everything is verified=false until checked on the maker's sheet.
"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'tiepanels.json')
items = []
CHECK = 'Check: configuration from the maker or reseller listing; confirm against the spec sheet.'

def tp(id, mfr, pn, name, family, ru, holes, rows, insert='', fixed=False, prefix='D', cat='patch', src='Generic', url='', notes=''):
    items.append({'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': cat, 'ru': ru, 'widthCols': 12,
                  'fullDepth': False, 'verified': False, 'source': src, 'productUrl': url, 'notes': (notes + ' ' if notes else '') + CHECK,
                  'thru': {'holes': holes, 'rows': rows, 'prefix': prefix, 'insert': insert, 'fixed': fixed}, 'portGroups': []})

# ---- D-series punched panels: pick the insert per hole ----
tp('penn-r1269-1uk-16', 'Penn Elcom', 'R1269/1UK-16', '1U rack panel punched for 16 D-series connectors', 'D-series panel', 1, 16, 1, src='Penn Elcom product page', url='https://www.penn-elcom.com/1u-rack-panels-punched-for-16-x-d-series-connectors-r1269-1uk-16')
tp('penn-r1269id-1uk-16', 'Penn Elcom', 'R1269ID-1UK-16', '1U rack panel with ID strip, punched for 16 D-series connectors', 'D-series panel', 1, 16, 1, src='Penn Elcom product page', url='https://penn-elcom.com/mx/1u-rack-panels-with-id-strip-punched-for-16-x-d-series-connectors-r1269id-1uk-16')
tp('lowell-n10p-id-1', 'Lowell', 'N10P-ID-1', '1U steel rack panel, 10 punches for Neutrik D / Switchcraft E connectors', 'D-series panel', 1, 10, 1, src='Full Compass listing', url='https://www.fullcompass.com/prod/183873-lowell-n10p-id-1-rack-panel-for-neutrik-d-series-connectors-1-rack-unit-black')
for ru, holes, rows in [(1, 16, 1), (2, 32, 2), (3, 48, 3)]:
    tp(f'tie-generic-d-{ru}u-{holes}', 'Generic', f'D-series panel {ru}U {holes}', f'{ru}U tie-line panel punched for {holes} D-series inserts (choose each insert)', 'D-series panel', ru, holes, rows, notes='Neutrik D / Switchcraft E size holes.')

# ---- fixed tie panels ----
F = [('xlr3f', 'XLR', 'XLR3 female front / male rear', 'Audio tie panel'), ('xlr3m', 'XLR', 'XLR3 male front / female rear', 'Audio tie panel'),
     ('db25', 'DB', 'DB25 feed-through (8 channels each)', 'Audio tie panel'), ('ethercon', 'NET', 'etherCON feed-through', 'Network tie panel'),
     ('bnc', 'BNC', 'BNC feed-through (12G)', 'Video tie panel'), ('hdmi', 'HDMI', 'HDMI feed-through', 'Video tie panel'),
     ('ocduo', 'FO', 'opticalCON DUO fibre feed-through', 'Fibre tie panel')]
for ins, pre, desc, fam in F:
    tp(f'tie-generic-{ins}-1u-16', 'Generic', f'{desc} panel 1U 16', f'1U tie panel, 16 x {desc}', fam, 1, 16, 1, ins, True, pre)
    if ins in ('xlr3f', 'bnc', 'ethercon'):
        tp(f'tie-generic-{ins}-2u-32', 'Generic', f'{desc} panel 2U 32', f'2U tie panel, 32 x {desc}', fam, 2, 32, 2, ins, True, pre)
tp('tie-generic-rj45-1u-24', 'Generic', 'RJ45 Cat6 coupler panel 1U 24', '1U feed-through panel, 24 x RJ45 Cat6 couplers', 'Network tie panel', 1, 24, 1, 'rj45', True, 'P')
tp('tie-generic-rj45-2u-48', 'Generic', 'RJ45 Cat6 coupler panel 2U 48', '2U feed-through panel, 48 x RJ45 Cat6 couplers', 'Network tie panel', 2, 48, 2, 'rj45', True, 'P')
tp('tie-generic-lc-1u-24', 'Generic', 'LC duplex coupler panel 1U 24', '1U fibre tie panel, 24 x LC duplex couplers', 'Fibre tie panel', 1, 24, 1, 'lc', True, 'FO')
tp('tie-generic-smpte-1u-8', 'Generic', 'SMPTE 311 fibre panel 1U 8', '1U camera fibre tie panel, 8 x SMPTE 311 (LEMO 3K.93C, e.g. EDW.3K.93C) feed-through', 'SMPTE fibre tie panel', 1, 8, 1, 'smpte', True, 'CAM',
   notes='For CCU tie lines. LEMO EDW.3K.93C is the square-flange panel socket; the hybrid fibre and copper pass straight through.')
tp('tie-generic-smpte-2u-16', 'Generic', 'SMPTE 311 fibre panel 2U 16', '2U camera fibre tie panel, 16 x SMPTE 311 (LEMO 3K.93C) feed-through', 'SMPTE fibre tie panel', 2, 16, 2, 'smpte', True, 'CAM')

# ---- wall and floor boxes (not racked: say where they are) ----
for holes, rows, kind in [(2, 1, 'wall'), (4, 1, 'wall'), (6, 2, 'wall'), (8, 2, 'wall'), (4, 1, 'floor'), (8, 2, 'floor'), (12, 3, 'floor')]:
    tp(f'box-generic-{kind}-{holes}d', 'Generic', f'{kind.title()} box {holes} x D', f'{kind.title()} box with {holes} D-series holes (choose each insert)', f'{kind.title()} box', 1, holes, rows,
       cat='wallbox', prefix='D', notes='Leave it out of the racks and type where it is, so tie lines show their far end.')

# ---- MUSA video jackfields (Canford) ----
def musa(pn, pts, url):
    items.append({'id': 'canford-' + pn.replace('-', ''), 'manufacturer': 'Canford', 'partNumber': pn, 'name': f'MUSA 3G HD video patch panel, 1U, 2x{pts}', 'family': 'MUSA video jackfield',
                  'category': 'patch', 'ru': 1, 'widthCols': 12, 'fullDepth': False, 'verified': False, 'source': 'Canford product page', 'productUrl': url,
                  'notes': 'MUSA jacks, 75 ohm. Check: normalling (MUSA panels are usually patched with U-links, so shown as not normalled) and the rear connector.',
                  'jack': {'points': pts, 'normal': 'none', 'type': '3G-SDI', 'front': 'MUSA jack', 'rear': 'BNC'},
                  'portGroups': [{'face': 'front', 'dir': 'io', 'type': '3G-SDI', 'connector': 'MUSA jack', 'count': pts * 2, 'prefix': 'Jack'},
                                 {'face': 'rear', 'dir': 'in', 'type': '3G-SDI', 'connector': 'BNC', 'count': pts, 'prefix': 'A'},
                                 {'face': 'rear', 'dir': 'out', 'type': '3G-SDI', 'connector': 'BNC', 'count': pts, 'prefix': 'B'}]})
musa('48-4381', 32, 'https://canford.co.uk/Products/48-4381_CANFORD-MUSA-3G-HD-PATCH-PANEL-1U-2x32-MUSA-3G-HD-grey')
musa('48-4318', 24, 'https://www.canford.de/Products/48-4318_CANFORD-MUSA-Steckfeld-1HE-2x24-3G-HD-grau')
musa('48-4314', 20, 'https://www.canford.co.uk/Products/48-4314_CANFORD-MUSA-3G-HD-PATCH-PANEL-1U-2x20-MUSA-3G-HD-grey')

json.dump(items, open(OUT, 'w'), indent=1)
print(len(items), 'entries ->', OUT)
