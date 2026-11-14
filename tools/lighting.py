#!/usr/bin/env python3
"""Lighting control and DMX distribution (added 2026-11-14):
  etc.json, malighting.json, chamsys.json, avolites.json, pathway.json, luminex.json, swisson.json, obsidian.json, pharos.json.
Category 'lighting' (tag LX). DMX512 ports use type 'DMX' with connector 'XLR5F' (output, female) or 'XLR5M' (input, male);
bidirectional node ports are dir 'io' on XLR5F. Art-Net / sACN / network ports stay type 'Ethernet' (etherCON or RJ45).
Lighting desks themselves are not rack gear; their rack processors (RPU, processing units, TNP) are in.
Not added: DMXking and Doug Fleenor Design make DIN-rail and small desktop nodes and splitters, not 19-inch units.
Specs from the makers' data sheets and manuals (each entry's source). 'Check:' marks anything unconfirmed."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, ru, ports, notes, src, url, verified=True, w=12, full=False, cat='lighting', **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m)
DMX = lambda face, n, label='DMX', d='out': g(face, d, 'DMX', 'XLR5F' if d != 'in' else 'XLR5M', n, label)
NET = lambda face, n, conn='etherCON', label='Network': g(face, 'io', 'Ethernet', conn, n, label)
TRUE1 = lambda face='rear': [g(face, 'in', 'Power', 'powerCON TRUE1', 1, 'Mains In'), g(face, 'out', 'Power', 'powerCON TRUE1', 1, 'Mains Thru')]

# ======================= ETC =======================
add('etc.json', 'etc-ion-rpu', 'ETC', '4310L1007', 'Ion Remote Processor Unit (RPU), 2U', 'Eos family', 2,
    [DMX('rear', 2, 'DMX/RDM'), NET('rear', 2, 'RJ45'), R('out', 'DVI', 'DVI-D', 2, 'Display'), R('out', 'DisplayPort', 'DisplayPort', 1, 'Display'),
     R('io', 'USB', 'USB-A', 7, 'USB'), R('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), R('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'),
     R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Rack-mount Eos-family processor (primary, backup or tracking for Eos, Gio and Ion consoles). Two DMX/RDM universes on the unit, '
    'the rest over sACN/Net3 gateways. 403 mm deep, 10.27 kg. Ion Xe RPU and Eos RPU3 are the current versions in the same idea. '
    'Check: USB count and which face has them.', 'ETC Ion RPU data sheet (rev H)',
    'https://media.musson.com/mti/docs/4/3/4310l1007_ion_rpu_datasheet_revh.pdf', weightKg=10.27)
add('etc.json', 'etc-rsn-dmx8-xlr', 'ETC', 'Response Mk2 8-Port', 'Response Mk2 8-port DMX/RDM gateway, XLR, 1U', 'Response Mk2', 1,
    [DMX('front', 8, 'DMX/RDM', 'io'), NET('rear', 1, 'etherCON', 'Network (PoE)'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Full-width sACN / Art-Net to DMX gateway with 8 XLR ports, each input or output. A half-width version with 8 terminal ports '
    'fits two per 1U with the rack kit. Check: connector placement, PoE and mains inlet.', 'ETC news: Response Mk2 8-port gateways',
    'https://www.etcconnect.com/about/news/etc-adds-response-mk2-8-port-dmx-gateways.aspx', verified=False)
add('etc.json', 'etc-rsn-dmx4-o', 'ETC', 'RSN-DMX4-O', 'Response Mk2 4-port DMX/RDM output gateway, half rack', 'Response Mk2', 1,
    [DMX('front', 4, 'DMX/RDM Out'), NET('rear', 1, 'etherCON', 'Network (PoE)')],
    'Half-width 1U sACN to DMX gateway with 4 output ports, PoE powered. RSN-DMX4-I is the input version; two fit in 1U with the rack kit. '
    'Check: connector placement.', 'ETC Response Mk2 data sheet', 'https://www.etcconnect.com/products/networking/response-mk2/features.aspx',
    verified=False, w=6)

# ======================= MA Lighting =======================
MA = 'MA Lighting'
for size, par in (('M', '4,096'), ('L', '8,192'), ('XL', '16,384')):
    add('malighting.json', f'ma-grandma3-pu-{size.lower()}', MA, f'grandMA3 processing unit {size}', f'grandMA3 processing unit {size}', 'grandMA3', 2,
        [DMX('rear', 8, 'DMX Out'), NET('rear', 2), R('io', 'USB', 'USB-A', 1, 'USB'), F('io', 'USB', 'USB-A', 2, 'USB'), R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In')],
        f'Network processing unit adding {par} parameters to a grandMA3 session. 8 DMX outputs, 2 etherCON, 200 VA max. '
        '482 x 372 x 87 mm, 5 kg. M, L and XL share the same panels. Rear matches the MA drawing (8 DMX A-H, 2 etherCON, 1 USB, power switch). Check: front USB count.', 'grandMA3 user manual: processing unit technical data',
        'https://help.malighting.com/grandMA3/2.3/HTML/key_pu_technical_data.html', powerW=200, weightKg=5.0)
add('malighting.json', 'ma-grandma3-8port-node', MA, 'grandMA3 8Port Node', 'grandMA3 8Port Node, 1U', 'grandMA3 nodes', 1,
    [DMX('front', 8, 'DMX', 'io'), NET('rear', 1, 'etherCON', 'Network (PoE)'), R('io', 'USB', 'USB-A', 1, 'USB'), R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In')],
    '19-inch node with 8 DMX ports, each output or input, 3.9-inch colour display, PoE or mains, 15 VA. 482 x 189 x 43 mm, 2 kg. '
    'The onPC 8Port Node adds 4,096 parameters for grandMA3 onPC. Check: DMX ports front or rear.',
    'grandMA3 user manual: xPort nodes technical data', 'https://help.malighting.com/grandMA3/2.2/HTML/key_xport_nodes_technical_data.html',
    verified=False, weightKg=2.0)

# ======================= ChamSys =======================
add('chamsys.json', 'chamsys-genetix-gn10', 'ChamSys', 'GeNetix GN10', 'GeNetix GN10 10-port Ethernet-DMX node, 1U', 'GeNetix', 1,
    [DMX('front', 10, 'DMX/RDM', 'io'), NET('rear', 2, 'etherCON'), R('in', 'Timecode', 'XLR3F', 1, 'LTC In'), R('out', 'Timecode', 'XLR3M', 1, 'LTC Out'),
     R('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), R('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), F('io', 'USB', 'USB-C', 1, 'USB-C'),
     R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In')],
    'Art-Net / sACN / ChamNet node with 10 RDM DMX ports (input or output), 2 network ports (PoE on port 1), LTC and MIDI, 10 stored scenes. '
    '480 x 218 x 44 mm, 2.75 kg. Check: which face carries the DMX, LTC and MIDI connectors.',
    'ChamSys GeNetix Node 10 cutsheet', 'https://soundpro.com/content/product-documents/GeNetixNode10Cutsheet.pdf', verified=False, weightKg=2.75)

# ======================= Avolites =======================
add('avolites.json', 'avolites-tnp', 'Avolites', '30-01-1600', 'Titan Net Processor (TNP), 3U', 'Titan', 3,
    [DMX('rear', 8, 'DMX Out'), NET('rear', 2), R('out', 'DVI', 'DVI-I', 1, 'Display'), R('io', 'USB', 'USB-A', 2, 'USB'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Rack processor that adds universes to a Titan session (up to 64 universes) or runs a show on its own. 8 isolated DMX outputs, '
    '2 Gigabit etherCON, 50 W. 481 x 426 x 132 mm, 14.5 kg. Check: which face carries the DMX and USB.',
    'Avolites Titan Net Processor spec sheet', 'https://www.avolites.com/app/uploads/2021/06/Titan_Net_Processor_Spec_Sheet.pdf',
    verified=False, full=True, powerW=50, weightKg=14.5)

# ======================= Pathway Connectivity =======================
PW = ('Pathway Pathport OCTO data sheet', 'https://pathwayconnect.com/index.php/products/pathport-dmx-ethernet-nodes/59-octo-6421-6422-6423-6426-6427')
add('pathway.json', 'pathway-pathport-octo-xlr-rear', 'Pathway Connectivity', '6421', 'Pathport OCTO 8-port DMX/RDM gateway, rear XLR, 1U', 'Pathport', 1,
    [DMX('rear', 8, 'DMX/RDM', 'io'), NET('rear', 1, 'RJ45'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Rack-mount sACN / Art-Net / Pathport gateway with 8 DMX ports (each in or out), front LCD and encoder, wide-range mains. '
    'Versions: front XLR, rear terminals, RJ45 (etherCON) DMX, and PoE. Check: network connector and part number of the rack version.',
    PW[0], PW[1], verified=False)

# ======================= Luminex =======================
LX = 'Luminex'
add('luminex.json', 'luminex-luminode-12', LX, 'LU0100072', 'LumiNode 12 Ethernet-DMX processor, 12 ports, 1U', 'LumiNode', 1,
    [DMX('front', 12, 'DMX/RDM', 'io'), NET('rear', 2), R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In'), R('out', 'Power', 'powerCON TRUE1', 1, 'Mains Thru')],
    'Art-Net / sACN / RTTrPL node and processor with 16 processing engines and 12 isolated 5-pin DMX ports (each in or out), '
    '2 Gigabit etherCON, mains or PoE (802.3af) with power redundancy. 13 W, 482 x 150 x 44 mm, 1.96 kg. LumiNode 12 RJ45 is a '
    'half-rack version with RJ45 DMX. Check: which face has the DMX ports.', 'Luminex LumiNode 12 product page',
    'https://www.luminex.be/products/luminode/luminode-12/', verified=False, powerW=13, weightKg=1.96)
add('luminex.json', 'luminex-gigacore-16t', LX, 'GigaCore 16t', 'GigaCore 16t AV network switch, 1U', 'GigaCore', 1,
    [F('io', 'Ethernet', 'etherCON', 4, 'etherCON'), R('io', 'Ethernet', 'etherCON', 4, 'etherCON'), R('io', 'Ethernet', 'RJ45', 8, 'RJ45')]
    + TRUE1(),
    'Gigabit switch preconfigured for lighting, audio and video networks (Art-Net, sACN, Dante, AES67), 8 etherCON (4 front, 4 rear) '
    'and 8 rear RJ45, PoE++ on all ports in the PoE model, RPSU 5580 redundant supply option. 30 W (510 W PoE model), 482 x 204 mm, 4 kg.',
    'Luminex GigaCore 16t product page', 'https://www.luminex.be/products/gigacore/gigacore-16t/', cat='network', powerW=30, weightKg=4.0)

# ======================= Swisson =======================
add('swisson.json', 'swisson-xnd-8r5', 'Swisson', 'XND-8R5', 'XND-8R5 8-port Ethernet-DMX node, 19-inch, 5-pin', 'XND', 1,
    [DMX('front', 8, 'DMX', 'io'), NET('rear', 1)] + TRUE1(),
    'Art-Net / sACN node with up to 8 isolated DMX ports (each in or out), powerCON in and thru, 11 W. 483 x 136 x 44.5 mm, 1.8 kg. '
    'XND-8R3 (3-pin) and XND-8R8 (RJ45) versions. Check: connector placement and network connector.',
    'Swisson XND-8R5 listing (Procom)', 'https://www.procom-me.com/products/swisson-xnd-8r5-8-port-ethernet-dmx-node-19-5pin-xlr',
    verified=False, powerW=11, weightKg=1.8)

# ======================= Obsidian / Elation =======================
add('obsidian.json', 'obsidian-netron-en12', 'Obsidian Control Systems', 'NETRON EN12', 'NETRON EN12 12-port Ethernet-DMX gateway, 1U', 'NETRON', 1,
    [DMX('front', 12, 'DMX/RDM', 'io'), NET('rear', 2, 'RJ45', 'Network (PoE on 1)'), R('in', 'GPI', 'Terminal block', 1, 'Contact closures (10)'),
     R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In'), R('out', 'Power', 'powerCON TRUE1', 1, 'Mains Thru')],
    'Art-Net / sACN gateway with 12 isolated bidirectional DMX/RDM ports on the front, 2 locking RJ45 (PoE 802.3af on one), '
    '10 contact closures. 482.5 x 146 x 44 mm, 1.82 kg. EN12i is the install version with terminals. Check: power connector type.',
    'Obsidian NETRON EN12 data sheet', 'https://cdn.shopify.com/s/files/1/0290/4132/8221/files/obsidian-netron-en12.pdf', verified=False, weightKg=1.82)
add('obsidian.json', 'elation-dmx10-5', 'Elation Professional', 'DMX10-5', 'DMX10-5 10-port DMX splitter, 1U', 'DMX splitters', 1,
    [DMX('front', 2, 'DMX In A/B', 'in'), DMX('front', 10, 'DMX Out'), R('in', 'Power', 'powerCON TRUE1', 1, 'Mains In')],
    'Opto-isolated splitter: 2 inputs, 10 outputs each switched to input A or B. Not RDM. 482 x 155 x 44 mm, 1.5 kg. '
    'Obsidian RDM10 is the RDM version. Check: power connector type.', 'Adorama Elation DMX10-5 listing',
    'https://www.adorama.com/elation-dmx10-5-rackmount-10-port-5-pin-xlr-dmx-splitter/p/eldmx105', verified=False, weightKg=1.5)

# ======================= Pharos =======================
add('pharos.json', 'pharos-lpc-x', 'Pharos Architectural Controls', 'LPC X', 'LPC X lighting playback controller, 1U', 'LPC', 1,
    [NET('rear', 2, 'etherCON', 'Network / eDMX'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'USB', 'USB-A', 2, 'USB'),
     R('out', 'DVI', 'DVI-I', 1, 'DVI Out'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Architectural / show playback controller outputting sACN, Art-Net, KiNET and Pathport to eDMX nodes (no DMX ports on the unit). '
    'Sold by channel count (LPC 10 to LPC 100). Contact closures, MIDI and RS-485 through RIO accessories. 40 W typical, 13.5 in deep, '
    '3.1 kg. Optional DVI-D input.', 'Pharos LPC X data sheet (Acclaim)', 'https://www.acclaimlighting.com/cdn/shop/files/Pharos_20LPC_20X.pdf',
    powerW=50, weightKg=3.1)

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
