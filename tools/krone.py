#!/usr/bin/env python3
"""Krone gear (added 2026-11-15). Krone is now part of CommScope; parts keep their Krone numbers (6450 2 009-00 = 64502009-00).
  catalogue/krone.json
    LSA-PLUS 19-inch back-mount-frame subracks (1U 3-way, 2U 9-way, 3U 15-way flush and recessed, the older 3U frame 8A) as frames,
    and the 10-pair disconnection and connection modules and the 6-pair screened ABS module as cards (system 'Krone LSA-PLUS').
    LSA PROFIL 19-inch subracks (3U data rack, 4U with jumper elements) as frames with PROFIL 10-pair modules (system 'Krone LSA PROFIL').
    HighBand 25 recessed frame kits (2U 100-pair, 3U 200-pair, 4U 300-pair; sold loaded with modules) as patch panels.
    Krone Cat5e and Cat6 24-port RJ45 patch panels.
Modelling: a module's jumper side is its front ports; its cable side is the one included rear module (the pairs punched down
from the incoming cable). One port = one pair (ABS: one screened pair). Connector 'Krone LSA' is the LSA-PLUS IDC.
Not added: Krone made no audio or video jackfields (its sister brand ADC did); wall boxes, 5A frames and profile rod frames are not 19-inch.
Specs from CommScope data sheets and product pages, Canford, MMEM and RS listings (each entry's source)."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
F_ = 'krone.json'; MFR = 'Krone'; LSA = 'Krone LSA'
BOX = {'x0': 0.05, 'x1': 0.95, 'y0': 0.08, 'y1': 0.92}
CS = 'https://www.commscope.com/product-type/frames-panels-cassettes-modules/copper-panels-modules-cassettes/copper-back-mount-frames/'
RP = ('CommScope data sheet: Copper racks and panels for subscriber access and transmission networks (LSA-PLUS subracks)',
      'https://www.commscope.com/globalassets/digizuite/728608-racks-and-panels-family-pa-115201-en.pdf')
S2 = ('CommScope data sheet: LSA-PLUS Series 2 family', 'https://www.commscope.com/globalassets/digizuite/2859-lsa-plus-series2-family-pa-113026-en.pdf')
def model(**m):
    m = dict(dict(manufacturer=MFR, widthCols=12, fullDepth=False, verified=True, portGroups=[]), **m)
    FILES.setdefault(F_, []).append(m)
def pn_id(pn):
    s = pn.lower(); num = s.replace(' ', '').replace('-', '').isdigit()
    return 'krone-' + (s.replace(' ', '') if num else s.replace(' ', '-')).replace('/', '-')

# ======================= LSA-PLUS back-mount-frame subracks (frames) =======================
def subrack(pn, ru, ways, mount, src, notes, system='Krone LSA-PLUS', verified=True, family='LSA-PLUS subracks'):
    fr = dict(system=system, slots=ways, slotOrder='ltr', rearAlign=1, door=False, front=BOX, rear=BOX,
              controller='None (passive). Takes 10-pair modules, one per way.')
    if ru == 1: fr.update(orient='h', cols=ways)   # 1U: the modules lie flat, end to end
    else: fr['orient'] = 'v'
    model(id=pn_id(pn), partNumber=pn, name=f'{pn} LSA-PLUS 19-inch subrack, {ru}U, {ways} modules, {mount}', family=family,
          category='frame', ru=ru, verified=verified, source=src[0], productUrl=src[1], frame=fr,
          notes=f'{ru}U 19-inch back mount frame for {ways} LSA-PLUS 10-pair modules ({ways * 10} pairs), {mount}. Modules are sold separately. ' + notes)
subrack('6450 1 202-00', 1, 3, 'flush', RP, 'Modules lie flat, end to end.')
subrack('6450 2 009-00', 2, 9, 'recessed', (RP[0] + '; CommScope 64502009-00 page', CS + 'item64502009-00/'),
        'Silver, thermoplastic and steel. CommScope also lists it as the HighBand backmount frame, 9-way (Australia/New Zealand).')
subrack('6450 1 008-00', 3, 15, 'flush', (RP[0] + '; MMEM listing (Krone TruNet backmount frame 15 way 3RU)', 'https://mm.mmem.com.au/kro6450-1-008-00'), '')
subrack('6450 2 006-00', 3, 15, 'recessed', (RP[0] + '; MMEM listing', 'https://mm.mmem.com.au/kro6450-2-006-00'), '')
subrack('6427 1 017-01', 3, 15, 'recessed with jumper rings (mounting frame 8A)',
        ('Canford 46-123 KRONE mounting frame 8A', 'https://canford.co.uk/Products/46-123_KRONE-MOUNTING-FRAME-8A-15-module-recessed-3U'),
        'The older Krone mounting frame 8A, common in broadcast audio bays: up to 150 pairs or 90 ABS circuits, horizontal blocks. Discontinued.',
        family='LSA-PLUS frames')

# ======================= LSA-PLUS modules (cards) =======================
def module(pn, name, pairs, notes, src, fits='Krone LSA-PLUS', label='Pr', typ='Analog audio', verified=True):
    model(id=pn_id(pn), partNumber=pn, name=name, family='LSA-PLUS modules', category='card', ru=0, widthCols=0, verified=verified,
          source=src[0], productUrl=src[1], notes=notes, portGroups=[F('io', typ, LSA, pairs, label)],
          card=dict(fits=[fits], slotWidth=1),
          rearModules=[dict(partNumber=pn, name='Cable side', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True,
                            portGroups=[R('io', typ, LSA, pairs, 'Cable ' + label)])])
CAN = ('Canford COMMSCOPE (KRONE) LSA-PLUS modules page', 'https://www.canford.co.uk/Products/46-101_COMMSCOPE-KRONE-LSA-PLUS-ABS-Module')
module('6089 1 102-02', 'LSA-PLUS 2/10 disconnection module (237A), 10 pairs', 10,
       'The standard Krone block for audio, control and comms: 10 pairs, each with a disconnect point between cable and jumper side '
       '(test or break with a plug). Printed 0-9; -01 and -06 are other printings. BT type 237A. Front ports are the jumper side.', S2)
module('6089 1 002-02', 'LSA-PLUS 2/10 connection module (237B), 10 pairs', 10,
       'As the disconnection module but cable and jumper side are permanently joined. BT type 237B.', S2)
module('LSA-PLUS ABS', 'LSA-PLUS ABS screened disconnection module, 6 pairs + screen', 6,
       'Audio broadcast module: 6 screened pairs, each screen carried through separately to the jumper side so screens are not commoned '
       '(avoids earth loops on low-level audio). 15 per 3U frame = 90 circuits. Discontinued.', CAN, label='Ch')

# ======================= LSA PROFIL 19-inch subracks and modules =======================
def profil(pn, ru, notes):
    model(id=pn_id(pn), partNumber=pn, name=f'{pn} LSA PROFIL 19-inch subrack, {ru}U, 18 modules', family='LSA PROFIL subracks',
          category='frame', ru=ru, source=RP[0], productUrl=RP[1],
          frame=dict(system='Krone LSA PROFIL', slots=18, slotOrder='ltr', orient='v', rearAlign=1, door=False, front=BOX, rear=BOX,
                     controller='None (passive). PROFIL modules clip onto 2 profile rods.'),
          notes=f'{ru}U 19-inch subrack with profile rods for 18 LSA-PLUS Series 2 PROFIL modules (180 pairs; 23 HD180 PROFIL modules also fit). ' + notes)
profil('6690 1 300-00', 3, 'DATA rack version. 6690 1 125-00 is the same size with rods only.')
profil('6690 1 371-00', 4, 'With jumper elements and a cable-fixation bracket (4U / 7SU).')
module('6089 1 121-02', 'LSA-PLUS Series 2 PROFIL disconnection module, 10 pairs', 10,
       'PROFIL (rod-mounted) version of the 10-pair disconnection module.', (S2[0], 'https://www.commscope.com/network-type/copper-broadband-access/copper-connectivity/telecom-copper-modules/item60891121-02'),
       fits='Krone LSA PROFIL')
module('6089 1 120-02', 'LSA-PLUS Series 2 PROFIL connection module, 10 pairs', 10,
       'PROFIL (rod-mounted) version of the 10-pair connection module.', S2, fits='Krone LSA PROFIL')

# ======================= HighBand 25 recessed frame kits (patch) =======================
HB = ('CommScope HighBand panels page (Australia/New Zealand)', 'https://www.commscope.com/network-type/enterprise-networks-structured-cabling/netconnect/copper-structured-cabling/highband-panels')
for pn, ru, ways in (('6450 2 176-00', 2, 4), ('6450 2 177-00', 3, 8), ('6450 2 178-00', 4, 12)):
    pairs = ways * 25
    model(id=pn_id(pn), partNumber=pn, name=f'{pn} HighBand 25 recessed frame kit, {ru}U, {ways}-way, {pairs} pairs', family='HighBand',
          category='patch', ru=ru, source=HB[0], productUrl=HB[1],
          notes=f'{ru}U 19-inch recessed frame sold loaded with {ways} colour-coded HighBand 25 modules ({pairs} pairs) for patch-by-exception '
                f'Cat 6 data or voice. Drawn as 4-pair data channels (6 per 25-pair module, {ways * 6} in all); for voice or audio each module is 25 pairs. '
                f'Silver, thermoplastic and steel.',
          portGroups=[F('io', 'Ethernet', LSA, ways * 6, 'Ch'), R('in', 'Ethernet', LSA, ways * 6, 'Cable ch')])

# ======================= RJ45 patch panels =======================
for pn, cat, shield, d, src in (('7022 1 056-24', 'Cat6', 'UTP', 150, ('RS 512-3057 listing', 'https://uk.rs-online.com/web/p/rj-patch-panels/5123057')),
                                ('7022 1 015-24', 'Cat5e', 'STP', 175, ('RS 342-8029 listing', 'https://uk.rs-online.com/p/rj-patch-panels/3428029'))):
    model(id=pn_id(pn), partNumber=pn, name=f'{pn} {cat} {shield} 24-port RJ45 patch panel, 1U', family='Krone patch panels', category='patch', ru=1,
          verified=False, source=src[0], productUrl=src[1],
          notes=f'1U 24-port {cat} {shield} panel{" on a PCB" if cat == "Cat5e" else ""}, 483 x 44 mm, {d} mm deep. Discontinued; CommScope now sells '
                f'NETCONNECT panels (e.g. CPP-6-UDDM-SL-1U-24 in Australia). Check: rear termination (shown as LSA-PLUS IDC).',
          portGroups=[F('io', 'Ethernet', 'RJ45', 24, 'Port'), R('in', 'Ethernet', LSA, 24, 'IDC')])

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
