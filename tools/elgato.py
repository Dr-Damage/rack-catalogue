#!/usr/bin/env python3
"""Elgato (added 2026-11-16) -> catalogue/elgato.json.
  Stream Deck Studio: Elgato's only rack-mount product, a 1RU 19-inch control surface with 32 LCD keys, 2 push encoders with LED rings and an
  NFC reader, run over Ethernet (PoE+) or USB-C, made with Bitfocus (Companion). Its front USB expansion port takes a bus-powered Stream Deck.
  The companions that go with it on a desk or shelf: the Network Dock (puts a USB Stream Deck on the network, PoE powered) and the desktop
  Stream Decks (MK.2, XL, + and + XL). Desktop units are drawn at their real width with boxMm so they sit on a rack shelf.
Sources: Elgato help-centre technical specification pages and the Stream Deck Studio quick start guide."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
OUT = []
HELP = 'https://help.elgato.com/hc/en-us/articles/'
def el(id, pn, name, fam, cat, ru, cols, ports, notes, src, verified=True, **kw):
    m = dict(id='elgato-' + id, manufacturer='Elgato', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=cols,
             fullDepth=False, verified=verified, source=src[0], productUrl=src[1], notes=notes, portGroups=ports)
    m.update(kw); OUT.append(m)

el('stream-deck-studio', '10GBO9901', 'Stream Deck Studio 1RU control surface, 32 LCD keys, 2 dials', 'Stream Deck', 'control', 1, 12,
   [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet (PoE+)'), R('io', 'USB', 'USB-C', 1, 'USB-C Data'), R('in', 'Power', 'USB-C', 1, 'USB-C PD In'),
    F('io', 'USB', 'USB-C', 1, 'USB Expansion')],
   '1RU 19-inch control surface with removable rack ears (two mounting depths): 32 LCD keys in two rows of 16, 2 360-degree push encoders '
   'with LED rings and an NFC reader. Rear: RJ45 Ethernet 100 Mb/s with PoE+ (802.3at Class 4), USB-C data to a computer, and USB-C PD 3.0 '
   'power in (9 V 3 A, supply not included). Ethernet power wins when both are connected. Front: USB expansion port for a bus-powered '
   'Stream Deck. Up to 15 W. 447 x 80 x 44 mm without ears, 0.9 kg. Runs Stream Deck software over USB or Bitfocus Companion over the '
   'network. Check: connector type of the front expansion port (shown as USB-C).',
   ('Elgato Stream Deck Studio technical specifications and quick start guide', HELP + '29982976486669-Elgato-Stream-Deck-Studio-Technical-Specifications'),
   powerW=15, weightKg=0.9, depthMm=80)
el('network-dock', '10GBW9901', 'Network Dock for Stream Deck (Ethernet, PoE)', 'Stream Deck', 'converter', 1, 2,
   [R('in', 'Ethernet', 'RJ45', 1, 'Ethernet (PoE)'), R('in', 'Power', 'USB-C', 1, 'USB-C PD In'), R('out', 'USB', 'USB-C', 1, 'Stream Deck')],
   'Puts a USB Stream Deck on the network so it can be run from Bitfocus Companion or the Stream Deck app without a local computer. RJ45 '
   'with 802.3af PoE, or USB-C PD power (5 V 0.9 A) on networks without PoE; USB-C (USB 2.0) to the Stream Deck, which gets up to 3.5 W. '
   'Works with Stream Deck Studio, Stream Deck Pedal and second-generation Stream Decks. 79 x 59 x 27 mm.',
   ('Elgato Network Dock for Stream Deck technical specifications', HELP + '39072725488145-Elgato-Network-Dock-for-Stream-Deck-Technical-Specifications'),
   powerW=4.5, boxMm={'w': 79, 'h': 27})
el('stream-deck-mk2', '10GBA9901', 'Stream Deck MK.2, 15 LCD keys', 'Stream Deck', 'control', 1, 3,
   [R('io', 'USB', 'USB-C', 1, 'USB-C')],
   'Desktop control panel with 15 LCD keys (3 x 5) and a removable stand, USB 2.0 on USB-C to the computer, Network Dock or Stream Deck Studio '
   'expansion port; bus powered. 118 x 84 x 25 mm and 145 g without stand.',
   ('Elgato Stream Deck MK.2 technical specifications', HELP + '18208816152333-Elgato-Stream-Deck-MK-2-Technical-Specifications'),
   weightKg=0.145, boxMm={'w': 118, 'h': 25})
el('stream-deck-xl', '10GAT9901', 'Stream Deck XL, 32 LCD keys', 'Stream Deck', 'control', 1, 5,
   [R('io', 'USB', 'USB-C', 1, 'USB-C')],
   'Desktop control panel with 32 LCD keys (4 x 8) and a magnetic stand, USB 3.0 on USB-C to the computer, Network Dock or Stream Deck Studio '
   'expansion port; bus powered. 182 x 112 x 34 mm and 410 g without stand.',
   ('Elgato Stream Deck XL technical specifications', HELP + '18170516758157-Elgato-Stream-Deck-XL-Technical-Specifications'),
   weightKg=0.41, boxMm={'w': 182, 'h': 34})
el('stream-deck-plus', '10GBD9901', 'Stream Deck +, 8 LCD keys, 4 dials, touch strip', 'Stream Deck', 'control', 3, 4,
   [R('io', 'USB', 'USB-C', 1, 'USB-C')],
   'Desktop control panel with 8 LCD keys, 4 push dials and an LCD touch strip, USB 2.0 on USB-C; bus powered. 140 x 138 x 110 mm, 465 g. '
   'Drawn 3RU tall because of its angled body; it sits on a shelf rather than in the rails.',
   ('Elgato Stream Deck + technical specifications', HELP + '10567379685901-Elgato-Stream-Deck-Technical-Specifications'),
   weightKg=0.465, boxMm={'w': 140, 'h': 110})
el('stream-deck-plus-xl', 'Stream Deck + XL', 'Stream Deck + XL, 36 LCD keys, 6 dials, touch strip', 'Stream Deck', 'control', 4, 6,
   [R('io', 'USB', 'USB-C', 1, 'USB-C')],
   'Desktop control panel with 36 LCD keys, 6 push dials (multifunction dials) and a 1200 x 100 LCD touch strip, USB 3.0 on USB-C, bus powered '
   '(5 V 0.9 A, 4 W), 1.09 kg. Elgato lists 205 x 147 x 175 mm, drawn as 205 wide by 175 high (4RU on a shelf) like the Stream Deck +. Check: which dimension is the height.',
   ('Elgato Stream Deck + XL technical specifications', HELP + '44835542537617-Elgato-Stream-Deck-XL-Technical-Specifications'),
   verified=False, powerW=4, weightKg=1.085, boxMm={'w': 205, 'h': 175})

ids = [m['id'] for m in OUT]; assert len(ids) == len(set(ids))
json.dump(OUT, open(os.path.join(CAT, 'elgato.json'), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'elgato.json' not in idx: idx.append('elgato.json')
json.dump(idx, open(ip, 'w')); print('elgato.json', len(OUT), 'entries,', sum(m['verified'] for m in OUT), 'verified;', len(idx), 'files')
