#!/usr/bin/env python3
"""Dante rack gear (added 2026-11-14):
  shure.json        Shure ULX-D and Axient Digital receivers, P300 IntelliMix processor.
  sennheiser.json   Sennheiser EW-DX EM 4 Dante and Digital 6000 EM 6000 Dante receivers.
  ferrofish.json    Ferrofish A32pro Dante converter.
Already in: Yamaha Rio/Tio (yamaha.json), DirectOut EXBOX.MD / PRODIGY (directout.json), Focusrite RedNet (focusrite.json).
Not added: Audinate makes AVIO adapters and software only; Attero Tech (now QSC) makes wall plates and small boxes;
Glensound's Dante range is desktop and portable commentary gear.
Specs from Shure / Sennheiser / dealer pages (each entry's source)."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m)
ANT = lambda n_in=2, n_out=2: [R('in', 'RF', 'BNC', n_in, 'Antenna In'), R('out', 'RF', 'BNC', n_out, 'Antenna Cascade')]
DANTE = R('io', 'Dante/AES67', 'RJ45', 2, 'Dante/Network')

# ======================= Shure =======================
SH = 'Shure'
add('shure.json', 'shure-ulxd4q', SH, 'ULXD4Q', 'ULXD4Q quad-channel digital wireless receiver', 'ULX-D', 'audio', 1,
    ANT(2, 2) + [R('out', 'Analog audio', 'XLR3M', 4, 'Audio Out'), DANTE, R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Four-channel ULX-D receiver, 1RU: one XLR output per channel (mic/line switch), Dante on a dual-port Ethernet switch (redundant or daisy-chain), '
    'antenna A and B inputs each with a cascade output to one more receiver. 274 mm deep, 3.45 kg. Rear panel checked against the Shure photo.',
    'BSW ULXD4Q listing (Shure specifications); rear from a Shure product photo', 'https://bswusa.com/shure-ulxd4q/', weightKg=3.45)
add('shure.json', 'shure-ulxd4d', SH, 'ULXD4D', 'ULXD4D dual-channel digital wireless receiver, half rack', 'ULX-D', 'audio', 1,
    ANT(2, 2) + [R('out', 'Analog audio', 'XLR3M', 2, 'Audio Out'), R('out', 'Analog audio', '1/4" TRS', 2, 'Audio Out (jack)'), DANTE,
                 R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Two-channel ULX-D receiver, half-rack 1RU, Dante on a dual-port switch. Two side by side with the supplied link bar. '
    'Check: all counts (from memory of the Shure spec sheet).', 'Shure ULX-D product information', 'https://www.shure.com/', verified=False, w=6)
add('shure.json', 'shure-ad4q', SH, 'AD4Q', 'Axient Digital AD4Q quad-channel wireless receiver', 'Axient Digital', 'audio', 1,
    ANT(2, 2) + [R('out', 'Analog audio', 'XLR3M', 4, 'Audio Out'), R('out', 'Analog audio', '1/4" TRS', 4, 'Audio Out (jack)'),
                 R('io', 'Dante/AES67', 'RJ45', 2, 'Dante'), R('io', 'Ethernet', 'RJ45', 2, 'Control'),
                 R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Thru'),
                 R('in', 'Power', 'IEC C14', 1, 'AC In'), R('out', 'Power', 'IEC C13', 1, 'AC Out'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones')],
    'Four-channel Axient Digital receiver, 1RU: XLR and -10 dB jack output per channel; with AES3 switched on, XLR outputs 1&2 and 3&4 carry AES3. '
    'Two Dante and two control ports (PoE), word clock in and thru, AC in and out. Antennas A and B with C and D for quadversity, 12 V DC on the antenna inputs. '
    '4.8 kg. AD4Q-DC takes DC power. AD4D is the two-channel version. Check: which antenna BNCs are cascade outputs.', 'Shure AD4Q spec sheet (Rentex); panels from a Shure product photo',
    'https://www.rentex.com/wp-content/uploads/2019/08/Shure-AD4Q-Axient-Wireless-Receiver-Spec-Sheet-from-Rentex.pdf', verified=False, weightKg=4.8)
add('shure.json', 'shure-p300', SH, 'P300', 'P300 IntelliMix audio conferencing processor', 'IntelliMix', 'audio', 1,
    [R('io', 'Dante/AES67', 'RJ45', 1, 'Dante/Network'), R('in', 'Analog audio', 'Euroblock', 2, 'Analog In'), R('out', 'Analog audio', 'Euroblock', 2, 'Analog Out'),
     R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'GPIO', 'Euroblock', 1, 'Logic'), R('in', 'Power', 'DC locking', 1, 'DC In')],
    'Conferencing DSP with 8 Dante inputs, AEC, auto-mix, USB and mobile audio. PoE+ powered. Half rack 1RU with a mounting kit. '
    'Check: all counts (from memory of the Shure spec sheet).', 'Shure P300 product information', 'https://www.shure.com/', verified=False, w=6)

# ======================= Sennheiser =======================
SE = 'Sennheiser'
add('sennheiser.json', 'sennheiser-ew-dx-em-4-dante', SE, 'EW-DX EM 4 DANTE', 'EW-DX EM 4 Dante four-channel digital rack receiver', 'EW-DX', 'audio', 1,
    ANT(2, 2) + [R('out', 'Analog audio', 'XLR3M', 4, 'Audio Out'), R('out', 'Analog audio', '1/4" TRS', 4, 'Audio Out (unbal jack)'),
                 R('io', 'Dante/AES67', 'RJ45', 2, 'Ethernet / Dante'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Four-channel EW-DX receiver with Dante (48 or 96 kHz), two antenna cascade outputs for up to four receivers, 37 W max, '
    '373 mm deep, 4.56 kg. Balanced XLR and unbalanced jack output per channel; the two RJ45 ports carry Dante and control. '
    'EW-DX EM 2 Dante is the two-channel version. Rear panel checked against a Sennheiser photo.',
    'Sennheiser EW-DX EM 4 Dante specifications; rear from a Sennheiser product photo', 'https://docs.cloud.sennheiser.com/en-us/ew-d/ew-d/specifications-ew-dx-em4-dante.html',
    verified=False, powerW=37, weightKg=4.56)
add('sennheiser.json', 'sennheiser-em-6000-dante', SE, 'EM 6000 DANTE', 'Digital 6000 EM 6000 Dante two-channel receiver', 'Digital 6000', 'audio', 1,
    ANT(2, 2) + [R('out', 'Analog audio', 'XLR3M', 2, 'Audio Out'), R('out', 'Analog audio', '1/4" TRS', 2, 'Audio Out (jack)'),
                 R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'),
                 R('io', 'Dante/AES67', 'etherCON', 1, 'Dante'), R('io', 'Ethernet', 'RJ45', 1, 'Control'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones'),
                 R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Two-channel Digital 6000 receiver with XLR and jack outputs per channel, AES3 on XLR, word clock in and out, one Dante port (etherCON) and an RJ45 control port. '
    'EM 6000 is the version without Dante. Rear panel checked against a Sennheiser photo.',
    'Sennheiser EM 6000 product overview; rear from a Sennheiser product photo', 'https://docs.cloud.sennheiser.com/en-us/digital-6000/digital-6000/manual-em6000-overview.html', verified=False)

# ======================= Ferrofish =======================
add('ferrofish.json', 'ferrofish-a32pro-dante', 'Ferrofish', 'A32pro Dante', 'A32pro Dante 32-channel AD/DA converter, Dante / MADI / ADAT', 'A32', 'audio', 1,
    [R('in', 'Analog audio', 'DB25', 4, 'Analog In'), R('out', 'Analog audio', 'DB25', 4, 'Analog Out'), R('out', 'Analog audio', '1/4" TRS', 2, 'Main Out'),
     R('io', 'SFP', 'SFP', 2, 'MADI SFP'), R('in', 'Other', 'TOSLINK', 4, 'ADAT In'), R('out', 'Other', 'TOSLINK', 4, 'ADAT Out'),
     R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'),
     R('io', 'Other', '3.5mm TRS', 2, 'MIDI'), R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'GPIO', 'DB15', 1, 'GPIO'),
     F('out', 'Analog audio', '1/4" TRS', 2, 'Headphones'), R('in', 'Power', 'DC locking', 2, '12V DC A/B')],
    '32 x 32 AD/DA on Tascam D-subs with Dante, MADI (SFP, optical module included) and ADAT, redundant 12 V supplies. '
    'A32pro is the version without Dante. Panels checked against the Ferrofish launch photo.', 'Trew Audio A32pro Dante listing; panels from the Ferrofish launch photo',
    'https://www.trewaudio.com/product/ferrofish-a32pro-dante/')

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
