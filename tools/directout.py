#!/usr/bin/env python3
"""Generates catalogue/directout.json: DirectOut Technologies MADI / audio-over-IP gear. Added 2026-11-14.

EXBOX.MD (Dante), EXBOX.RAV (RAVENNA/AES67) and EXBOX.SG (SoundGrid) are one-third rack width boxes; three sit in 1RU on the
BOXMOUNT.XL kit (a shelf here, with carrier bays). MONTONE.42 and ANDIAMO are 1RU, PRODIGY.MC/MP/MX are 2RU modular frames whose
I/O comes from plug-in modules (A, B and C slots, shown as card-slot ports; add module I/O to the device to match the build).
Specs from directout.eu product pages (each entry's productUrl); EXBOX.MD's rear connectors are checked against DirectOut's rear photo."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
M = []
U = 'https://www.directout.eu/product/'
EXBOX = 'DirectOut EXBOX (1/3 width)'
def add(id, pn, name, fam, cat, ru, w, ports, notes, url, verified=True, **kw):
    m = dict(id='directout-' + id, manufacturer='DirectOut', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w,
             fullDepth=False, verified=verified, source='DirectOut product page', productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

MADI3 = [R('out', 'MADI audio', 'BNC', 1, 'MADI BNC Out'), R('in', 'MADI audio', 'BNC', 1, 'MADI BNC In'),
         R('io', 'MADI audio', 'SC duplex (multi-mode)', 1, 'MADI SC Out/In'), R('io', 'MADI audio', 'SFP', 1, 'MADI SFP I/O')]
HIROSE = R('in', 'Power', 'Hirose 4-pin (9-24V DC)', 2, 'PSU')
EXN = (' One-third 19 inch width: 140 x 42 x 140 mm (W x H x D), about 1 kg. Three fit side by side in 1RU on the BOXMOUNT.XL kit. '
       'Power: 2 x Hirose 4-pin DC inlets (9-24V, PSU 1 and 2; one external supply included, a second is optional) or PoE (802.3af) on '
       'network port 01. MADI: coaxial BNC out and in, optical SC duplex (multi-mode; single-mode version available) and an SFP cage '
       '(transceiver sold separately). Front: LEDs for clock source, sample rate, state and power only. FastSRC sample rate converters on the '
       'network side. 44.1-192 kHz, MADI 56/64 ch, 48k/96k frame, S/MUX.')
for slug, pn, net, desc, extra in [
        ('exbox-md', 'EXBOX.MD', 'Dante', 'Dante / MADI converter: 64 channels both ways between Dante (or AES67) and MADI. '
         'Network: 4 x RJ45 1 Gb/s on an internal switch, 01 (PoE) and 02 primary, 03 and 04 secondary (Dante redundancy).', []),
        ('exbox-rav', 'EXBOX.RAV', 'RAVENNA/AES67', 'RAVENNA / MADI converter: 64 channels both ways between RAVENNA, AES67 or SMPTE ST 2110-30/-31 '
         'and MADI. Network: 4 x RJ45 1 Gb/s on an internal switch (one with PoE).', []),
        ('exbox-sg', 'EXBOX.SG', 'SoundGrid', 'SoundGrid / MADI converter: links a Waves SoundGrid network with MADI. Network: 4 x RJ45 1 Gb/s on an '
         'internal switch (one with PoE). Word clock in on BNC.', [R('in', 'Reference', 'BNC', 1, 'Word Clock In')])]:
    t = 'Dante/AES67' if net != 'SoundGrid' else 'Ethernet'
    lab = (' Primary', ' Primary', ' Secondary', ' Secondary') if net == 'Dante' else ('',) * 4
    ports = [HIROSE] + [R('io', t, 'RJ45', 1, f'{net} 0{i + 1}{" (PoE)" if i == 0 else ""}{lab[i]}') for i in range(4)] + MADI3 + extra
    add(slug, pn, f'{pn} {net} / MADI converter', 'EXBOX', 'audio', 1, 4, ports, desc + EXN, U + slug + '/',
        weightKg=1.0, formFactor=EXBOX)
add('boxmount-xl', 'BOXMOUNT.XL', 'BOXMOUNT.XL 1RU rack kit for 3 EXBOX', 'EXBOX', 'shelf', 1, 12, [],
    '1RU 19 inch mounting kit that holds up to three one-third width EXBOX units (EXBOX.MD, EXBOX.RAV, EXBOX.SG) side by side. '
    'Add each EXBOX as its own device. Check: part number and whether it also takes other one-third width units.',
    U + 'exbox-md/', verified=False, carrier={'bays': 3, 'fits': [EXBOX]})

add('montone-42', 'MONTONE.42', 'MONTONE.42 MADI / RAVENNA (AES67, ST 2110-30) bridge', 'MONTONE', 'audio', 1, 12,
    [F('out', 'Analog audio', '6.3mm TRS', 1, 'Headphones'), F('io', 'USB', 'USB-B', 1, 'USB Service'),
     R('io', 'MADI audio', 'SC / BNC / SFP (as ordered)', 4, 'MADI'), R('io', 'Dante/AES67', 'RJ45', 2, 'RAVENNA/AES67 Network'),
     R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'), R('in', 'Reference', 'BNC', 1, 'Video Ref In'),
     R('in', 'Power', 'IEC', 2, 'AC In')],
    '1RU bridge between 4 MADI ports and RAVENNA / AES67 / SMPTE ST 2110-30/-31 (with ST 2022-7 redundancy on the 2 network ports). '
    'Each MADI port is ordered as SC (single- or multi-mode), coaxial BNC or SFP cage. Word clock in (AES11/DARS) and out, black burst video '
    'reference in. Front: 3 small displays, controls, headphone jack and a USB service port. 2 phase-redundant supplies on separate IEC inlets '
    'with power switches, 15 W. 483 x 44.5 x 254 mm, about 4 kg. Check: USB service connector type.',
    U + 'montone-42/', powerW=15, weightKg=4.0)

add('andiamo', 'ANDIAMO', 'ANDIAMO 32-channel AD/DA converter (MADI, network)', 'ANDIAMO', 'audio', 1, 12,
    [R('in', 'Analog audio', 'DB25', 4, 'Analog In (8 ch)'), R('out', 'Analog audio', 'DB25', 4, 'Analog Out (8 ch)'),
     R('io', 'MADI audio', 'SFP', 2, 'MADI SFP'), R('io', 'Dante/AES67', 'RJ45', 2, 'Audio Network (option card)'), R('io', 'Ethernet', 'RJ45', 1, 'Management'),
     R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'), R('in', 'Power', 'IEC', 2, 'AC In')],
    'Third generation ANDIAMO: 32 analog inputs and 32 outputs on 8 balanced DB25 (AES59) connectors, 2 MADI ports on SFP cages '
    '(transceivers sold separately), an optional audio network card (RAVENNA/AES67, Dante or SoundGrid) with 2 RJ45 ports on independent NICs, '
    'RJ45 management, word clock BNCs. 2 phase-redundant supplies on separate IEC inlets with power switches. 483 x 44.5 x 254 mm, about 4 kg. '
    'Check: whether the 8 DB25 split 4 in / 4 out, and which word clock BNC is in or out.', U + 'andiamo/', verified=False, weightKg=4.0)

PRODIGY = (' 2RU, 483 x 89 x 254 mm, about 10 kg. 2 phase-redundant supplies (84-264V AC), 20-110 W depending on modules. Front: 5 inch touch '
           'display, encoder, 2 buttons, headphone outputs on 6.3 mm and 3.5 mm jacks. Its I/O comes from plug-in modules: A slots take an '
           'audio network module (Dante, RAVENNA/AES67, SoundGrid, MILAN, dual-network), 2-port MADI (MADI2.SRC.IO on SFP, MADI2.BNC.SRC.IO) '
           'or USB.IO; B slots take 1-port MADI (BNC.IO, SC.IO, SFP.IO); C slots take 8-channel converters on DB25 (AN8.IO, MIC8.HD.IO, '
           'MIC8.LINE.IO, AES4.IO). Slots are shown as card-slot ports; add the module connectors to the device to match the build. '
           'Check: power inlet type (IEC assumed).')
HP = [F('out', 'Analog audio', '6.3mm TRS', 1, 'Headphones 1'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headphones 2')]
PW = R('in', 'Power', 'IEC', 2, 'AC In')
SLOT = lambda n, p: R('io', 'Other', 'Card slot', n, p)
add('prodigy-mc', 'PRODIGY.MC', 'PRODIGY.MC modular audio converter', 'PRODIGY', 'audio', 2, 12,
    HP + [R('in', 'Reference', 'BNC', 1, 'Word Clock I/O'), R('io', 'Ethernet', 'RJ45', 1, 'Remote Control'), R('io', 'USB', 'USB-A', 1, 'USB 2.0'),
          R('io', 'GPI', 'Other', 1, 'GPIO (2 in, 2 out)'), SLOT(1, 'A Slot (network / MADI / USB)'), SLOT(2, 'B Slot (MADI)'), SLOT(8, 'C Slot (analog / AES, DB25)'), PW],
    'Modular converter: 1 A slot (up to 128 ch), 2 B slots (64 ch each), 8 C slots (8 ch each).' + PRODIGY, U + 'prodigy-mc/',
    verified=False, powerW=110, weightKg=10.0)
add('prodigy-mp', 'PRODIGY.MP', 'PRODIGY.MP multifunction audio processor', 'PRODIGY', 'audio', 2, 12,
    HP + [R('io', 'Reference', 'BNC', 2, 'Word Clock (WCK 2 can be video sync)'), R('io', 'Ethernet', 'RJ45', 2, 'Management'), R('io', 'SFP', 'SFP', 1, 'Management SFP'),
          R('io', 'USB', 'USB-A', 1, 'USB 2.0'), F('io', 'USB', 'USB-A', 1, 'USB 2.0'), R('io', 'Other', 'MIDI DIN', 2, 'MIDI'), R('io', 'GPI', 'Other', 1, 'GPIO (2 in, 2 out)'),
          SLOT(2, 'A Slot (network / MADI / USB)'), SLOT(2, 'B Slot (MADI)'), SLOT(4, 'C Slot (analog / AES, DB25)'), PW],
    'Audio processor (DSP, matrix, tools): 2 A slots, 2 B slots, 4 C slots, up to 416 inputs and 420 outputs.' + PRODIGY, U + 'prodigy-mp/',
    verified=False, powerW=110, weightKg=10.0)
add('prodigy-mx', 'PRODIGY.MX', 'PRODIGY.MX multiformat audio matrix', 'PRODIGY', 'audio', 2, 12,
    HP + [R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'), R('io', 'Ethernet', 'RJ45', 2, 'Management'),
          R('io', 'SFP', 'SFP', 1, 'Management SFP'), SLOT(6, 'A Slot (network / MADI / USB)'), SLOT(2, 'B Slot (MADI)'), PW],
    'Audio matrix: 6 A slots (up to 256 ch each, including MADI4.IO), 2 B slots, up to 1664 inputs and 1668 outputs.' + PRODIGY,
    U + 'prodigy-mx/', verified=False, powerW=110, weightKg=10.0)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(os.path.join(CAT, 'directout.json'), 'w'), indent=1)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'directout.json' not in idx: idx.append('directout.json'); json.dump(idx, open(ip, 'w'))
print('directout.json', len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
