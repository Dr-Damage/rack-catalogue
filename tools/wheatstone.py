#!/usr/bin/env python3
"""Wheatstone (added 2026-11-15) -> catalogue/wheatstone.json.
  WheatNet-IP I/O blades (analog, AES, mic, console, mix engine, MADI, logic, HD-SDI, EDGE, Aura8-IP processing, M4IP-USB), the Blade 4 TVE mix
  engine for the Arcus / Strata / Tekton TV consoles, the Gibraltar Network cage (4U, card-based, card list not published) and the FM-55 processor.
Blades are 1RU unless stated. Stereo analog and AES run on RJ45 (one stereo pair per jack, StudioHub pinout) with D-sub alternatives; the 12
logic (GPIO) ports are on two RJ45s. Blade 4 (fourth generation) units add a second network port, front and rear USB-A, a rear HDMI on most
types and an optional second PSU: shown with two network ports and one AC inlet. Sources: wheatstone.com/blades, the TV mix engine page, the
Gibraltar cage page and the FM-55 technical manual. Most entries are verified=False with "Check:" because per-connector counts are not tabulated."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
AA, AES = 'Analog audio', 'AES/EBU'; OUT = []
BL = ('Wheatstone WheatNet-IP blades page', 'https://www.wheatstone.com/blades')
LOGIC = lambda: R('io', 'GPIO', 'RJ45', 2, 'Logic (12 ports)')
NET = lambda: R('io', 'Ethernet', 'RJ45', 2, 'WheatNet-IP (Gb)')
def ws(id, pn, name, fam, cat, ru, ports, notes, src=BL, verified=False, power=True, **kw):
    m = dict(id='wheatstone-' + id, manufacturer='Wheatstone', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=12,
             fullDepth=False, verified=verified, source=src[0], productUrl=src[1], notes=notes,
             portGroups=ports + ([R('in', 'Power', 'IEC', 1, 'AC In')] if power else []))
    m.update(kw); OUT.append(m)
B4 = ' Blade 4 version: dual network ports, front/rear USB-A with clip players, rear HDMI, optional dual PSU.'
for pn, desc, ins, outs, w in (('IP-88A', 'analog I/O blade, 8 stereo in / 8 stereo out', [R('in', AA, 'RJ45', 8, 'Analog In (stereo)'), R('in', AA, 'DB25', 2, 'Analog In (D-sub)')],
                                [R('out', AA, 'RJ45', 8, 'Analog Out (stereo)'), R('out', AA, 'DB25', 2, 'Analog Out (D-sub)')], 30),
                               ('IP-88D', 'AES I/O blade, 8 AES in / 8 AES out', [R('in', AES, 'RJ45', 8, 'AES In'), R('in', AES, 'DB25', 2, 'AES In (D-sub)')],
                                [R('out', AES, 'RJ45', 8, 'AES Out'), R('out', AES, 'DB25', 2, 'AES Out (D-sub)')], 12),
                               ('IP-88AD', 'analog and AES I/O blade, 4 + 4 in / 4 + 4 out', [R('in', AA, 'RJ45', 4, 'Analog In (stereo)'), R('in', AES, 'RJ45', 4, 'AES In'),
                                R('in', 'Other', 'DB25', 2, 'In (D-sub)')], [R('out', AA, 'RJ45', 4, 'Analog Out (stereo)'), R('out', AES, 'RJ45', 4, 'AES Out'),
                                R('out', 'Other', 'DB25', 2, 'Out (D-sub)')], 19)):
    ws(pn.lower(), pn, f'{pn} {desc}', 'WheatNet-IP Blades', 'audio', 1, ins + outs + [LOGIC(), NET()],
       f'1RU WheatNet-IP blade: 8 stereo (16 mono) inputs and outputs on RJ45, the same I/O also on four D-subs (2 in, 2 out), 12 logic ports, '
       f'{w} W. Blade 3 part numbers add -3 (IP-88-3A etc.).{B4} Check: D-sub type and whether RJ45 and D-sub are parallel.', powerW=w)
ws('ip-88-3m', 'IP88-3M', 'IP88-3M mic blade, 8 mic preamps', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', AA, 'XLR3F', 8, 'Mic In'), R('out', AA, 'RJ45', 4, 'Line Out (2 mono each)'), R('out', AA, 'DB25 (8 ch)', 1, 'Line Out (D-sub)'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '1RU, 8 mic preamps on female XLR (-50 dBu nominal), 8 mono line outputs on four RJ45s and one DB25, 12 logic ports on two RJ45s, Gigabit Ethernet, 19 W.',
   verified=True, powerW=19)
ws('ip-88cb', 'IP88CB', 'IP88CB console audio blade with mix engine', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', AA, 'XLR3F', 2, 'Mic In'), R('in', AA, 'RJ45', 4, 'Analog In (stereo)'), R('out', AA, 'RJ45', 4, 'Analog Out (stereo)'),
    R('in', AES, 'RJ45', 4, 'AES In'), R('out', AES, 'RJ45', 4, 'AES Out'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '1RU console blade with the mix engine for IP-12, IP-16, L-8 and L-12 surfaces: 2 mic XLR, 4 stereo analog in and out, 4 AES in and out '
   '(all RJ45), 12 logic, Gigabit Ethernet, 19 W. CBL and CBE variants exist.', verified=True, powerW=19)
ws('cb32', 'CB32', 'CB32 double console audio blade, 2RU', 'WheatNet-IP Blades', 'audio', 2,
   [R('in', AA, 'XLR3F', 4, 'Mic In'), R('in', AA, 'RJ45', 8, 'Analog In (stereo)'), R('out', AA, 'RJ45', 8, 'Analog Out (stereo)'),
    R('in', AES, 'RJ45', 8, 'AES In'), R('out', AES, 'RJ45', 8, 'AES Out'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '2RU console blade with twice the IP88CB I/O: 4 mic XLR, 8 stereo analog in and out, 8 AES in and out on RJ45. Check: logic port count.')
ws('ip-88e', 'IP88E', 'IP88E mix engine blade (no audio I/O)', 'WheatNet-IP Blades', 'audio', 1, [LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   'DSP mix engine for one radio control surface, no audio I/O; 12 logic ports, Gigabit Ethernet, 10 W. Check: rack height (1RU shown).', powerW=10)
ws('blade4-tve', 'Blade 4 TVE', 'Blade 4 TVE mix engine for Arcus, Strata and Tekton TV consoles', 'TV mix engines', 'audio', 1, [LOGIC(), NET()],
   '1RU mix engine for the Arcus, Strata and Tekton 32 TV audio consoles, AES67 compatible; 12 logic ports; optional synchronised backup engine '
   'for automatic failover. Audio I/O comes from blades on the network.', src=('Wheatstone TV console mix engine page', 'https://wheatstone.com/product/tv-console-mix-engine-blades/'))
ws('madi-blade', 'MADI Blade', 'MADI blade, 64 channels each way', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', 'MADI', 'BNC', 1, 'MADI In'), R('out', 'MADI', 'BNC', 1, 'MADI Out'), R('io', 'MADI', 'SFP', 1, 'MADI fibre'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '1RU, 64-channel bidirectional MADI on BNC in/out plus an SFP for fibre, two 8x2 mixers, 12 logic, Gigabit Ethernet.', verified=True)
ws('lio-48', 'LIO-48', 'LIO-48 logic blade, 48 GPIO ports', 'WheatNet-IP Blades', 'control', 1,
   [R('io', 'GPIO', 'RJ45', 8, 'Logic (6 ports each)'), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '48 individually configurable universal logic ports with front LEDs, Gigabit Ethernet. Check: logic connector count and rack height.')
ws('hd-sdi-blade', 'HD-SDI Blade', 'HD-SDI de-embedder blade, 4 SDI inputs', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', 'HD-SDI', 'BNC', 4, 'SDI In'), R('out', 'HD-SDI', 'BNC', 4, 'SDI Loop'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   '1RU, de-embeds up to 8 audio channels from each of 4 HD-SDI streams onto WheatNet-IP; 4 looping BNC outputs, 12 logic, Gigabit Ethernet.', verified=True)
ws('network-edge', 'Network EDGE', 'Network EDGE WheatNet-IP to IP STL translator', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', AES, 'RJ45', 2, 'AES In'), R('in', AA, 'RJ45', 2, 'Analog In (stereo)'), LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'Network')],
   '1RU fanless unit that translates between WheatNet-IP and IP wireless STL radios; 2 AES and 2 stereo analog inputs. Check: audio connector types and logic count.')
ws('aura8-ip', 'Aura8-IP', 'Aura8-IP processing blade, 8 stereo processors', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', AES, 'RJ45', 8, 'AES In'), R('out', AES, 'RJ45', 8, 'AES Out'), R('in', AES, 'DB25', 1, 'AES In (D-sub)'), R('out', AES, 'DB25', 1, 'AES Out (D-sub)'),
    LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   'Eight stereo audio processors on the network: 8 AES in and out on both D-sub and RJ45, 12 logic ports. Check: rack height and D-sub count.')
ws('m4ip-usb', 'M4IP-USB', 'M4IP-USB 4-channel mic processor blade', 'WheatNet-IP Blades', 'audio', 1,
   [R('in', AA, 'XLR3F', 4, 'Mic In'), R('out', AA, 'XLR3M', 4, 'Analog Out'), R('out', AES, 'XLR3M', 2, 'AES Out'), F('io', 'USB', 'USB-A', 1, 'USB'),
    LOGIC(), R('io', 'Ethernet', 'RJ45', 1, 'WheatNet-IP (Gb)')],
   'Four-channel mic and voice processor on the WheatNet-IP network with analog and digital outputs and USB. Check: output connectors and counts.',
   src=('Wheatstone M4IP-4USB listing (SCMS)', 'https://www.scmsinc.com/wheatstone-m4ip-4usb-4-channel-mic-processing-blade-4-inputs-with-analog-and-digital-outputs.html'))
ws('gibraltar-cage', 'Gibraltar Network Cage', 'Gibraltar network cage, 4U, 20 card slots', 'Gibraltar', 'audio', 4,
   [R('in', 'Reference', 'BNC', 1, 'Sync In (CPU card)'), R('io', 'Ethernet', 'RJ45', 1, 'Network (CPU card)'), R('in', 'Power', 'Other', 2, 'PSU (external)')],
   '4U, 406 mm deep (457 mm with connectors), 13.6 kg. 20 universal hot-swap slots: 2 redundant CPUs, 3 DSP, 15 I/O (analog, AES with SRC, MADI, '
   'SDI de-embed, mix engine, audio-over-Ethernet, 16-channel AoIP). Cards load from the front; rear interface modules give RJ, D-sub, BNC or '
   'screw terminals. 512 channels on the backplane, 44.1/48 kHz. Engine for Wheatstone TV consoles (D-8EX, Dimension Three). Add the rear '
   'module connectors as extra ports. Check: slot count (16 or 20) and PSU arrangement.',
   src=('Wheatstone Gibraltar Network Cage page', 'https://mail.wheatstone.com/television-products1/gibraltar-network/2016-11-28-10-23-75'),
   power=False, fullDepth=True, depthMm=457, weightKg=13.6)
ws('fm-55', 'FM-55', 'FM-55 FM audio processor, 1RU', 'Processors', 'audio', 1,
   [R('in', AA, 'XLR3F', 2, 'Analog In L/R'), R('out', AA, 'XLR3M', 2, 'Analog Out L/R'), R('in', AES, 'XLR3F', 1, 'AES In'), R('out', AES, 'XLR3M', 1, 'AES Out'),
    R('in', 'Other', 'BNC', 2, 'SCA In'), R('out', 'Other', 'BNC', 2, 'Composite (MPX) Out'), R('io', 'GPIO', 'RJ45', 1, 'GPI'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet / WheatNet-IP')],
   '1RU FM broadcast processor, 229 mm deep behind the rails. Analog and AES in and out on XLR (AES out switchable to baseband192), 2 SCA inputs '
   'and 2 composite outputs on BNC, GPI and Ethernet on RJ45, IEC mains 90-240 V, no power switch.',
   src=('Wheatstone FM-55 technical manual', 'https://manualmachine.com/wheatstone/fm55/19899416-technical-manual'), verified=True, depthMm=229)

ids = [m['id'] for m in OUT]; assert len(ids) == len(set(ids))
json.dump(OUT, open(os.path.join(CAT, 'wheatstone.json'), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'wheatstone.json' not in idx: idx.append('wheatstone.json')
json.dump(idx, open(ip, 'w')); print('wheatstone.json', len(OUT), 'entries,', sum(m['verified'] for m in OUT), 'verified;', len(idx), 'files')
