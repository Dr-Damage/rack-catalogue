#!/usr/bin/env python3
"""More fibre patching (added 2026-11-14):
  catalogue/commscope.json  CommScope Propel fixed panels (PPL-1U/2U/4U-HD-FX) as frames; generic Propel 24-fibre LC adapter pack and
                            MPO-to-LC module as cards. One slot = one 24-fibre position (the user manual's 24-fibre column).
                            Propel 24-fibre splice and field-term cassettes (2026-11-15, verified from CommScope item pages where noted).
  catalogue/dynamix.json    Dynamix FPP3PD 1U sliding fibre drawer (24 LC duplex, unloaded).
Molex was looked at: only a 1U enclosure for 4 ModLink cassettes is listed, with no cassette layouts, so nothing was added.
Same modelling as tools/fibre.py: the frame is the enclosure, each module is a card, card front ports are the patch side and its
rear module is the trunk side."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
BOX = {'x0': 0.04, 'x1': 0.96, 'y0': 0.08, 'y1': 0.92}
def model(file, **m): FILES.setdefault(file, []).append(m)

PP_SRC = 'CommScope Propel fixed panel user manual (TC-96342-IP) and PPL-4U product page'
PP_URL = 'https://www.commscope.com/product-type/frames-panels-cassettes-modules/fiber-panels-modules-cassettes/fiber-panels/propel-panels'
for ru, n in ((1, 4), (2, 8), (4, 16)):
    pn = f'PPL-{ru}U-HD-FX'
    model('commscope.json', id='commscope-' + pn.lower(), manufacturer='CommScope', partNumber=pn,
          name=f'{pn} Propel fixed fibre panel, {n} x 24-fibre positions', family='Propel', category='frame', ru=ru, widthCols=12,
          fullDepth=False, verified=False, source=PP_SRC, productUrl=PP_URL,
          notes=f'{ru}RU fixed Propel panel, {ru * 2} blades of 12 lanes each. Modules and adapter packs come in 8, 12, 16 and 24-fibre sizes '
                f'(2, 3, 4 or 6 lanes); here each position is one 24-fibre (6-lane) module, {n} per panel ({n * 12} LC duplex). '
                + ('PPL-{0}U-HD-FX-OPEN is the reduced-depth version. '.format(ru) if ru < 4 else 'The PPL-4U sliding version (760252004) takes up to 288 duplex LC with high-density packs. ')
                + 'Check: blade layout (shown as two columns per RU).',
          portGroups=[], frame=dict(system='CommScope Propel', slots=n, orient='h', cols=2, slotOrder='ltr', rearAlign=1, door=False,
                                    front=BOX, rear=BOX, controller='None (passive). Takes Propel modules, adapter packs and splice cassettes.'))
def card(id, pn, name, front, rear, notes, rearName='Rear (trunk side)', src=PP_SRC, url=PP_URL, verified=False, color='aqua'):
    model('commscope.json', id=id, manufacturer='CommScope', partNumber=pn, name=name, family='Propel', category='card', ru=0, widthCols=0,
          fullDepth=False, verified=verified, source=src, productUrl=url, notes=notes, portGroups=front,
          card=dict(fits=['CommScope Propel'], slotWidth=1, color=color),
          rearModules=[dict(partNumber=pn, name=rearName, width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=rear)])
card('commscope-propel-ap-12lc', 'Propel LC adapter pack 24F', 'Propel LC adapter pack, 12 LC duplex (24 fibres)',
     [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('io', 'Fibre', 'LC duplex', 12, 'LC')],
     'Generic 24-fibre LC duplex adapter pack (feed-through). Pick the exact part (single-mode or multimode, colour, shutters) from '
     'CommScope. Check: part number.')
card('commscope-propel-mod-24f-mpo', 'Propel module 24F MPO-LC', 'Propel module, MPO24 to 12 LC duplex',
     [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('io', 'Fibre', 'MPO/MTP', 1, 'MPO24')],
     'Generic 24-fibre Propel module breaking an MPO24 trunk out to 12 LC duplex. Also made with 2 x MPO12. Check: part number and trunk type.')

# Propel splice and field-term cassettes (added 2026-11-15). 24-fibre versions take 6 lanes = one position here. The 12-fibre
# versions (3 lanes, e.g. PPL-SP-12LC-SM-PT-AS 760255076) are half a position and are not modelled.
PROPEL_ITEM = 'https://www.commscope.com/network-type/data-centers/fiber-panels-and-modules/propel/item'
for code, pn, fibre, kind, ok in (('760255084', 'PPL-SP-24LC-SM-RPT-AS', 'SM', 'ribbon', True), ('760255053', 'PPL-SP-24LC-SM-PT-BEU', 'SM', 'single', False),
                                  ('760255054', 'PPL-SP-24LC-OM4-PT-BEU', 'OM4', 'single', False)):
    sm = fibre == 'SM'
    card('commscope-' + pn.lower(), pn, f'{pn} Propel {"single-mode" if sm else fibre} splice cassette, 12 LC duplex (24F), {kind}-fibre pigtails',
         [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('in', 'Fibre', 'Splice', 24, 'Splice')],
         f'CommScope {code}. Propel {"single-mode (G.657.A2, OS2)" if sm else fibre} splice cassette: 24 LC/UPC with internal shutters, '
         f'{"a ribbon pigtail for mass fusion splicing" if kind == "ribbon" else "250 um single-fibre pigtails"}, pairs straight polarity, '
         'splice protectors included. Takes 6 of the 12 lanes on a blade (one position here).' + ('' if ok else ' Check: details (taken from the matching -AS cassette).'),
         rearName='Splice tray (inside)', src=f'CommScope {code} product page', url=PROPEL_ITEM + code, verified=ok, color='#2f6fd1' if sm else '#21b5c4')
for code, pn, fibre, ok in (('760255064', 'PPL-FT-24LC-SM-00-000', 'SM', True), ('760255065', 'PPL-FT-24LC-OM4-00-000', 'OM4', False)):
    sm = fibre == 'SM'
    card('commscope-' + pn.lower(), pn, f'{pn} Propel {"single-mode" if sm else fibre} field-term cassette, 12 LC duplex (24F)',
         [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('in', 'Fibre', 'LC duplex', 12, 'Field LC')],
         f'CommScope {code}. Propel {"single-mode" if sm else fibre} field-termination cassette: 24 LC with internal shutters and no fibre; '
         'field-fitted connectors plug into the back of the adapters. Takes 6 lanes (one position here).' + ('' if ok else ' Check: details (taken from the single-mode version).'),
         rearName='Rear (field connectors)', src=f'CommScope {code} product page', url=PROPEL_ITEM + code, verified=ok, color='#2f6fd1' if sm else '#21b5c4')

DX_URL = 'https://cdlnz.com/19-1u-fibre-patch-panel-unloaded-24-port-lc-duplex-ball-bearing-sliding-drawer'
model('dynamix.json', id='dynamix-fpp3pd', manufacturer='Dynamix', partNumber='FPP3PD',
      name='FPP3PD 1U fibre patch panel, 24 LC duplex, sliding drawer (unloaded)', family='Fibre patch panels', category='patch', ru=1,
      widthCols=12, fullDepth=False, verified=True, source='Dynamix FPP3PD listing (CDL)', productUrl=DX_URL,
      notes='1U ball-bearing sliding drawer for up to 24 LC duplex (48 fibres) or 24 SC simplex adapters, sold unloaded. Front waterfall '
            'patch guide, four rear cable entries, front cover with labels. Splice trays or pigtails go inside (shown as rear splices).',
      portGroups=[F('io', 'Fibre', 'LC duplex', 24, 'LC'), R('in', 'Fibre', 'Splice', 48, 'Splice')])

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
