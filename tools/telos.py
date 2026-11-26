#!/usr/bin/env python3
"""Generates catalogue/telos.json: Telos Alliance (Axia) xNode and xNode2 Livewire+/AES67 audio I/O nodes, the Linear Acoustic SDI xNode
and SDI AoIP Node. Added 2026-11-26.

The original xNode family (legacy, replaced by xNode2): Analog, AES/EBU, Microphone, Mixed Signal and GPIO. Each is a fanless
half-rack 1RU box; two sit side by side in 1RU with the xNode rack-mount kit (p/n 2011-00076), modelled as a shelf with 2 bays.
Sources: telosalliance.com legacy product pages (rear labels read from Telos' product photos), the Axia xNode Installation & User's
Guide rev 2.0 (Jan 2016, p/n 1490-00081-002) for pinouts, dimensions, power and the mounting kits. Telos publishes no per-model
part numbers and no net weight (shipping weight 3.2 kg)."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
M = []
FF = 'Telos xNode'
URL = 'https://telosalliance.com/legacy/'
COMMON_PORTS = [
    R('io', 'Ethernet', 'RJ45', 1, 'NET 1 Livewire+/AES67 10/100 (PoE in)'),
    R('io', 'Ethernet', 'RJ45', 1, 'NET 2 Livewire+/AES67 10/100'),
    R('in', 'Power', 'IEC C14', 1, 'AC Input'),
]
COMMON = ('Fanless half-rack 1RU Livewire+/AES67 audio node (legacy; replaced by xNode2). Front: OLED status/setup display, two soft '
          'buttons and a power LED (green AC, red PoE, orange both). Network: two 100BT RJ45 ports, NET 1 (top) takes IEEE 802.3af PoE, '
          'used as redundant mirrored ports or as Livewire plus a separate management port. Power: auto-ranging 90-240 VAC 50/60 Hz IEC '
          'inlet and/or PoE, 14 W. 216 x 44 x 298 mm (8.5 x 1.72 x 11.75 in); net weight not published (3.2 kg shipping). Two fit side by '
          'side in 1RU with the xNode rack-mount kit 2011-00076; surface-mount kit 2011-00077. ')
SRC = 'Telos Alliance legacy xNode pages (rear labels from Telos product photos) and Axia xNode Installation & User\'s Guide rev 2.0'

def add(id, pn, name, ports, notes, slug):
    M.append(dict(id='telos-xnode-' + id, manufacturer='Telos Alliance', partNumber=pn, name=name, family='Axia xNode', category='audio',
                  ru=1, widthCols=6, fullDepth=False, verified=True, source=SRC, productUrl=URL + slug, notes=COMMON + notes,
                  portGroups=ports + COMMON_PORTS, formFactor=FF, boxMm=dict(w=216, h=44), depthMm=298, powerW=14))

add('analog', 'Analog xNode', 'Analog xNode 4x4 stereo line I/O (Livewire+/AES67)', [
    R('in', 'Analog audio', 'DB25', 1, 'Analog Line Inputs 1-4'),
    R('out', 'Analog audio', 'DB25', 1, 'Analog Line Outputs 1-4'),
    R('in', 'Analog audio', 'RJ45', 4, 'Analog Line In (stereo)'),
    R('out', 'Analog audio', 'RJ45', 4, 'Analog Line Out (stereo)'),
], '4 stereo (8 mono) balanced line inputs and 4 stereo line outputs, also usable as 5.1 plus a stereo mix. Inputs switch between '
   '-10 dBV and +4 dBu; outputs reach +24 dBu. The same 4 stereo inputs and 4 stereo outputs appear in parallel on the RJ45 jacks '
   '(one stereo pair per jack: pins 1/2 left +/-, 3/6 right +/-, 4 ground) and on the two DB25s (8 balanced channels each, '
   'Tascam/AES59 pinout), so wire one or the other. Rear, left to right: DB25 inputs over DB25 outputs, RJ45 inputs 1-4 over outputs 1-4, '
   'NET 1 over NET 2, IEC.', 'telos-alliance-analog-xnode')

add('aes', 'AES/EBU xNode', 'AES/EBU xNode 4x4 AES3 I/O (Livewire+/AES67)', [
    R('in', 'AES/EBU', 'DB25', 1, 'AES/EBU Inputs 1-4'),
    R('out', 'AES/EBU', 'DB25', 1, 'AES/EBU Outputs 1-4'),
    R('in', 'AES/EBU', 'RJ45', 4, 'AES/EBU In'),
    R('out', 'AES/EBU', 'RJ45', 4, 'AES/EBU Out'),
], '4 stereo AES3 inputs and 4 AES3 outputs. The same signals appear in parallel on the RJ45 '
   'jacks (one AES pair per jack on pins 1/2) and on the two DB25s, so wire one or the other. Rear, left to right: DB25 inputs over DB25 '
   'outputs, RJ45 inputs 1-4 over outputs 1-4, NET 1 over NET 2, IEC.', 'telos-alliance-aesebu-xnode')

add('mic', 'Microphone xNode', 'Microphone xNode 4 mic in / 4 stereo line out (Livewire+/AES67)', [
    R('in', 'Analog audio', 'DB25', 1, 'Microphone Inputs 1-4'),
    R('out', 'Analog audio', 'DB25', 1, 'Analog Line Outputs 1-4'),
    R('in', 'Analog audio', 'RJ45', 4, 'Mic In'),
    R('out', 'Analog audio', 'RJ45', 4, 'Analog Line Out (stereo)'),
], '4 mono mic preamps (selectable phantom power, software gain, -75 to -20 dBu nominal) and 4 stereo line outputs. Mic inputs are on '
   'RJ45 (pins 1/2 mic +/-, 4 ground) or the DB25, not XLR; the same channels appear in parallel on both, so wire one or the other. '
   'Rear, left to right: DB25 mic inputs over DB25 line outputs, RJ45 mic inputs 1-4 over line outputs 1-4, NET 1 over NET 2, IEC.',
    'xnodes')

add('mixed-signal', 'Mixed Signal xNode', 'Mixed Signal xNode mic/line, analog, AES3 and GPIO (Livewire+/AES67)', [
    R('in', 'Analog audio', 'XLR3F', 1, 'Mic (1)'),
    R('in', 'Analog audio', 'RJ45', 3, 'Analog Line In (stereo)'),
    R('in', 'AES/EBU', 'RJ45', 1, 'AES/EBU Input'),
    R('out', 'Analog audio', 'RJ45', 3, 'Analog Line Out (stereo)'),
    R('out', 'AES/EBU', 'RJ45', 1, 'AES/EBU Output'),
    R('io', 'GPIO', 'DB15', 2, 'GPIO'),
], 'Mixed signal I/O audio / logic node: 1 selectable mic/line input on an XLR-F, analog line inputs and outputs on RJ45 (stereo per jack), '
   '1 AES3 input and 1 AES3 output on RJ45, and 2 GPIO ports on DA-15 (each 5 opto inputs and 5 relay outputs, Axia GPIO pinout). '
   'Telos lists 2 dedicated line inputs plus the mic/line input; the rear is labelled Analog Line Inputs 1-3 and Outputs 1-3. '
   'Rear, left to right: XLR mic, RJ45 line inputs 1-3 and AES in over line outputs 1-3 and AES out, GPIO 1 over GPIO 2, NET 1 over NET 2, IEC.',
    'xnodes')

add('gpio', 'GPIO xNode', 'GPIO xNode 6 logic ports (Livewire+)', [
    R('io', 'GPIO', 'DB15', 6, 'GPIO'),
], '6 GPIO ports on DA-15 female, each with 5 opto-isolated inputs and 5 solid state relay outputs, plus +5 V and ground '
   '(100 mA combined per port; external logic supply up to 48 VDC, GPO up to 24 V). Pin-for-pin compatible with Axia GPIO accessory '
   'modules. Rear: GPIO 1/2, 3/4, 5/6 in three columns, NET 1 over NET 2, IEC.', 'telos-alliance-gpio-xnode')

# xNode2 (current range, 2022+): same half-rack chassis and rack kit; colour LCD, gigabit, PoE+.
COMMON2_PORTS = [
    R('io', 'Ethernet', 'RJ45', 1, 'NET 1 Livewire+/AES67 10/100/1000 (PoE+ in)'),
    R('io', 'Ethernet', 'RJ45', 1, 'NET 2 10/100/1000 (management or 2022-7)'),
    R('in', 'Power', 'IEC C14', 1, 'AC Input'),
]
COMMON2 = ('Fanless half-rack 1RU Livewire+/AES67 audio node (current xNode2 range). Front: colour LCD, two navigation buttons, PoE and AC '
           'LEDs. Network: two gigabit RJ45 ports; NET 1 (top) is the default AoIP port and takes IEEE 802.3at PoE+, NET 2 is management or '
           'SMPTE 2022-7 redundancy. Power: 100-240 VAC 50/60 Hz IEC inlet with automatic switchover to PoE+, 16 W. 216 x 44 x 298 mm '
           '(8.5 x 1.72 x 11.75 in); weight not published. Rack-mount kit included (two side by side in 1RU); optional surface-mount kit. ')
SRC2 = 'Telos Alliance xNode2 pages and docs.telosalliance.com xNode2 manual (rear labels from Telos product photos)'

def add2(id, pn, name, ports, notes, slug):
    M.append(dict(id='telos-xnode2-' + id, manufacturer='Telos Alliance', partNumber=pn, name=name, family='Axia xNode2', category='audio',
                  ru=1, widthCols=6, fullDepth=False, verified=True, source=SRC2,
                  productUrl=slug,
                  notes=COMMON2 + notes, portGroups=ports + COMMON2_PORTS, formFactor=FF, boxMm=dict(w=216, h=44), depthMm=298, powerW=16))

add2('analog', 'Analog xNode2', 'Analog xNode2 4x4 stereo line I/O (Livewire+/AES67)', [
    R('in', 'Analog audio', 'DB25', 1, 'Analog Line Inputs 1-4'),
    R('out', 'Analog audio', 'DB25', 1, 'Analog Line Outputs 1-4'),
    R('in', 'Analog audio', 'RJ45', 4, 'Analog Line In (stereo)'),
    R('out', 'Analog audio', 'RJ45', 4, 'Analog Line Out (stereo)'),
], '4 stereo (8 mono) balanced line inputs and outputs, +4 dBu nominal, +24 dBu max. The same channels appear in parallel on the RJ45 '
   'jacks (stereo per jack) and the two DB25s (AES59/Tascam pinout), so wire one or the other. Rear: DB25 inputs over outputs, RJ45 inputs '
   '1-4 over outputs 1-4, NET 1 over NET 2, IEC.', 'https://docs.telosalliance.com/docs/analog-xnode2')

add2('aes', 'AES/EBU xNode2', 'AES/EBU xNode2 4x4 AES3 I/O (Livewire+/AES67)', [
    R('in', 'AES/EBU', 'DB25', 1, 'AES/EBU Inputs 1-4'),
    R('out', 'AES/EBU', 'DB25', 1, 'AES/EBU Outputs 1-4'),
    R('in', 'AES/EBU', 'RJ45', 4, 'AES/EBU In'),
    R('out', 'AES/EBU', 'RJ45', 4, 'AES/EBU Out'),
], '4 AES3 inputs (32-192 kHz) and 4 AES3 outputs, 24 bit. The same signals appear in parallel on the RJ45 jacks and '
   'the two DB25s, so wire one or the other. Rear: DB25 inputs over outputs, RJ45 inputs 1-4 over outputs 1-4, NET 1 over NET 2, IEC.',
    'https://docs.telosalliance.com/docs/digital-aes3-xnode2')

add2('mic', 'Microphone xNode2', 'Microphone xNode2 4 mic in / 4 stereo line out (Livewire+/AES67)', [
    R('in', 'Analog audio', 'DB25', 1, 'Microphone Inputs 1-4'),
    R('out', 'Analog audio', 'DB25', 1, 'Analog Line Outputs 1-4'),
    R('in', 'Analog audio', 'RJ45', 4, 'Mic In'),
    R('out', 'Analog audio', 'RJ45', 4, 'Line Out (stereo)'),
], '4 mono mic/line inputs (14-68 dB gain, switchable +48 V phantom) and 4 stereo line outputs, on RJ45 or DB25 (parallel, wire one or the '
   'other); no XLR. The RJ45 block differs from the other xNode2s: Mic In 1/2 top left, Mic In 3/4 bottom left, Line Out 1/2 top right, '
   'Line Out 3/4 bottom right. Rear: DB25 mic inputs over DB25 line outputs, the RJ45 block, NET 1 over NET 2, IEC.', 'https://docs.telosalliance.com/docs/microphone-xnode2')

add2('mixed-signal', 'Mixed Signal xNode2', 'Mixed Signal xNode2 mic, analog, AES3 and GPIO (Livewire+/AES67)', [
    R('in', 'Analog audio', 'XLR3F', 1, 'Mic (1)'),
    R('in', 'Analog audio', 'RJ45', 3, 'Analog Line In (stereo)'),
    R('in', 'AES/EBU', 'RJ45', 1, 'AES/EBU Input'),
    R('out', 'Analog audio', 'RJ45', 3, 'Analog Line Out (stereo)'),
    R('out', 'AES/EBU', 'RJ45', 1, 'AES/EBU Output'),
    R('io', 'GPIO', 'DB15', 2, 'GPIO'),
], '1 mic/mono line input on an XLR-F, 3 stereo line inputs and 1 AES3 input on RJ45 (top row), 3 stereo line outputs and 1 AES3 output on '
   'RJ45 (bottom row), and 2 GPIO ports on DA-15 female (5 opto inputs, 5 relay outputs, +5 V each). Rear: XLR, RJ45 block, GPIO 1 over '
   'GPIO 2, NET 1 over NET 2, IEC.', 'https://docs.telosalliance.com/docs/mixed-signal-xnode2')

add2('gpio', 'GPIO xNode2', 'GPIO xNode2 6 logic ports (Livewire+)', [
    R('io', 'GPIO', 'DB15', 6, 'GPIO'),
], '6 GPIO ports on DA-15 female, each with 5 opto-isolated inputs and 5 outputs plus +5 V. Rear: GPIO 1/2, 3/4, 5/6 in three columns, '
   'NET 1 over NET 2, IEC.', 'https://telosalliance.com/distributed-decentralized-routing/audio-interfaces/telos-alliance-xnode2s/gpio-xnode2')

# Linear Acoustic SDI xNode (legacy, same half-rack chassis) and its full-width successor, the SDI AoIP Node.
M.append(dict(id='telos-sdi-xnode', manufacturer='Telos Alliance', partNumber='SDI xNode', name='SDI xNode 2-channel SDI audio embedder/de-embedder (Livewire+/AES67)',
    family='Linear Acoustic xNode', category='converter', ru=1, widthCols=6, fullDepth=False, verified=True,
    source='Telos Alliance legacy SDI xNode page and Linear Acoustic SDI xNode manual (rear labels from Telos product photo)',
    productUrl='https://telosalliance.com/legacy/sdi-xnode', formFactor=FF, boxMm=dict(w=216, h=44), depthMm=298, powerW=18,
    notes='Legacy Linear Acoustic SDI xNode (replaced by the SDI AoIP Node). Two 3G/HD/SD-SDI inputs de-embed up to 8 pairs each to '
          'Livewire+/AES67, and two SDI outputs re-embed up to 8 pairs from the network. Fanless half-rack 1RU, same chassis and rack kit as '
          'the other xNodes. Front: OLED meters/display, two buttons, status LED. Network: two 10/100 RJ45 (NET 1, NET 2; redundant or '
          'Livewire plus management). Power: 90-240 VAC IEC (0.2 A) plus a locking +12 VDC backup input; 15-18 W max. 216 x 44 x 298 mm. '
          'Rear, left to right: SDI 1 In/Out, SDI 2 In/Out, +12VDC Backup In, NET 1 over NET 2, IEC.',
    portGroups=[R('in', '3G-SDI', 'BNC', 1, 'SDI 1 In'), R('out', '3G-SDI', 'BNC', 1, 'SDI 1 Out'),
                R('in', '3G-SDI', 'BNC', 1, 'SDI 2 In'), R('out', '3G-SDI', 'BNC', 1, 'SDI 2 Out'),
                R('in', 'Power', 'DC locking', 1, '+12VDC Backup In'),
                R('io', 'Ethernet', 'RJ45', 1, 'NET 1 Livewire+/AES67 10/100'), R('io', 'Ethernet', 'RJ45', 1, 'NET 2 10/100'),
                R('in', 'Power', 'IEC C14', 1, 'AC Input')]))

M.append(dict(id='telos-sdi-aoip-node', manufacturer='Telos Alliance', partNumber='SDI AoIP Node', name='SDI AoIP Node 2-channel 3G-SDI embedder/de-embedder (AES67)',
    family='Linear Acoustic xNode', category='converter', ru=1, widthCols=12, fullDepth=False, verified=True,
    source='Telos Alliance SDI AoIP Node page, brochure and docs.telosalliance.com front/rear panel overview (rear from Telos product photo)',
    productUrl='https://telosalliance.com/Linear/SDI-Node', depthMm=229, powerW=30, weightKg=2.72,
    notes='Successor to the SDI xNode. Full-width 1RU. Two 3G/HD/SD-SDI inputs de-embed up to 8 pairs each to AES67, two SDI outputs re-embed '
          'up to 8 pairs. Reference: PTP (AES67), SDI or internal 48 kHz. Front: four status LEDs (PWR 1, PWR 2, status, sync), colour LCD, '
          'five-button navigation cluster. Rear, left to right: GPI/O DB15 female (5 in / 5 out, not supported in firmware 1.2.006), AES '
          'in/out holes (blanked in Telos photo, not listed in the docs, so not added as ports), SDI 1 Out/In, SDI 2 Out/In, AES67 and '
          'CONTROL gigabit RJ45, PWR 1 and PWR 2 IEC (dual internal redundant 95-240 VAC supplies, 30 W max). 483 x 229 x 45 mm '
          '(19 x 9 x 1.75 in), 2.72 kg.',
    portGroups=[R('io', 'GPIO', 'DB15', 1, 'GPI/O'),
                R('out', '3G-SDI', 'BNC', 1, 'SDI 1 Out'), R('in', '3G-SDI', 'BNC', 1, 'SDI 1 In'),
                R('out', '3G-SDI', 'BNC', 1, 'SDI 2 Out'), R('in', '3G-SDI', 'BNC', 1, 'SDI 2 In'),
                R('io', 'Ethernet', 'RJ45', 1, 'AES67'), R('io', 'Ethernet', 'RJ45', 1, 'Control'),
                R('in', 'Power', 'IEC C14', 1, 'PWR 1'), R('in', 'Power', 'IEC C14', 1, 'PWR 2')]))

M.append(dict(id='telos-xnode-rack-kit', manufacturer='Telos Alliance', partNumber='2011-00076', name='xNode rack-mount kit (2 xNodes, xNode2s or SDI xNodes in 1RU)',
              family='Axia xNode', category='shelf', ru=1, widthCols=12, fullDepth=False, verified=True, source=SRC, productUrl=URL + 'xnodes',
              notes='Rack ears (one short, one long) and a spacer that join two half-rack xNodes side by side in 1RU, or mount one xNode with '
                    'the long ear filling the other half. Add each xNode as its own device.', portGroups=[],
              carrier=dict(bays=2, fits=[FF])))

json.dump(M, open(os.path.join(CAT, 'telos.json'), 'w'), indent=1)
idx = os.path.join(CAT, 'index.json'); L = json.load(open(idx))
if 'telos.json' not in L: L.append('telos.json'); json.dump(L, open(idx, 'w'))
print(len(M), [m['id'] for m in M])
