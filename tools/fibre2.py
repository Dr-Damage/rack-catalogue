#!/usr/bin/env python3
"""More fibre patching (added 2026-11-14):
  catalogue/commscope.json  CommScope Propel fixed panels (PPL-1U/2U/4U-HD-FX) as frames; generic Propel 24-fibre LC adapter pack and
                            MPO-to-LC module as cards. One slot = one 24-fibre position (the user manual's 24-fibre column).
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
def card(id, pn, name, front, rear, notes, rearName='Rear (trunk side)'):
    model('commscope.json', id=id, manufacturer='CommScope', partNumber=pn, name=name, family='Propel', category='card', ru=0, widthCols=0,
          fullDepth=False, verified=False, source=PP_SRC, productUrl=PP_URL, notes=notes, portGroups=front,
          card=dict(fits=['CommScope Propel'], slotWidth=1, color='aqua'),
          rearModules=[dict(partNumber=pn, name=rearName, width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=rear)])
card('commscope-propel-ap-12lc', 'Propel LC adapter pack 24F', 'Propel LC adapter pack, 12 LC duplex (24 fibres)',
     [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('io', 'Fibre', 'LC duplex', 12, 'LC')],
     'Generic 24-fibre LC duplex adapter pack (feed-through). Pick the exact part (single-mode or multimode, colour, shutters) from '
     'CommScope. Check: part number.')
card('commscope-propel-mod-24f-mpo', 'Propel module 24F MPO-LC', 'Propel module, MPO24 to 12 LC duplex',
     [F('io', 'Fibre', 'LC duplex', 12, 'LC')], [R('io', 'Fibre', 'MPO/MTP', 1, 'MPO24')],
     'Generic 24-fibre Propel module breaking an MPO24 trunk out to 12 LC duplex. Also made with 2 x MPO12. Check: part number and trunk type.')

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
