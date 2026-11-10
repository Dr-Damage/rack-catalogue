#!/usr/bin/env python3
"""Generates catalogue/behringer.json, yamaha.json, allenheath.json and klarkteknik.json (rack-mount audio mixers and stageboxes)."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, pre, mfr, id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=pre + id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
AA, AO = 'Analog audio', 'AES/EBU'

# ---------------- Behringer ----------------
B = lambda *a, **k: add('behringer.json', 'beh-', 'Behringer', *a, **k)
B('x32-rack', 'X32 RACK', 'X32 RACK digital mixer', 'X32', 'audio', 3,
  [R('in', AA, 'XLR', 16, 'Mic In'), R('in', AA, 'XLR', 1, 'Talkback Mic'), R('out', AA, 'XLR', 8, 'Out'),
   R('out', AA, '1/4" TRS', 2, 'Monitor Out'), R('in', AA, '1/4" TRS', 6, 'Aux In'), R('in', AA, 'RCA', 2, 'RCA In'),
   R('out', AA, '1/4" TRS', 6, 'Aux Out'), R('out', AA, 'RCA', 2, 'RCA Out'), R('out', AO, 'XLR', 1, 'AES/EBU Out'),
   R('io', 'AES50', 'etherCON', 2, 'AES50'), R('out', 'Other', 'RJ45', 1, 'Ultranet'), R('in', 'Other', 'MIDI DIN', 1, 'MIDI In'),
   R('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), R('io', 'Ethernet', 'RJ45', 1, 'Remote'), R('in', 'Power', 'IEC', 1, 'Power'),
   F('out', AA, '1/4" TRS', 1, 'Phones'), F('io', 'USB', 'USB-A', 1, 'USB')],
  '3U 40-input, 25-bus digital mixer: 16 Midas mic preamps, 8 XLR outs, 6 aux in/out, 2 AES50 (A/B), Ultranet for P-16, MIDI, '
  'Ethernet remote, 1 option card slot (32 ch, e.g. X-USB, X-Dante, X-MADI), 5" display on the front. Check: USB position (top or front).',
  'X32 RACK quick start / spec sheet', 'https://www.behringer.com/product.html?modelCode=0603-ACV')
B('wing-rack', 'WING RACK', 'WING RACK digital mixer', 'WING', 'audio', 4,
  [R('in', AA, 'XLR', 24, 'Mic In'), R('out', AA, 'XLR', 8, 'Out'), R('io', 'AES50', 'etherCON', 3, 'AES50'),
   R('io', AA, 'XLR', 1, 'StageConnect'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('io', 'USB', 'USB-B', 1, 'USB Audio'),
   R('in', 'Power', 'IEC', 1, 'Power'), F('out', AA, '1/4" TRS', 4, 'Phones')],
  '4U 48-channel, 28-bus mixing engine. 24 Midas PRO mic preamps, 8 outputs, 3 AES50 ports (144 I/O), StageConnect (32 ch over XLR), '
  'expansion slot (64 ch Dante, MADI or SoundGrid), dual Ethernet, USB audio/MIDI 48 ch, dual SD recorder, 4 phones outs. '
  'Check: aux jacks, AES/EBU, MIDI DIN and talkback connectors, and front/rear split.',
  'Reseller product page (Andertons)', 'https://www.behringer.com/product.html?modelCode=0604-AAE', verified=False)
B('s32', 'S32', 'S32 digital snake 32x16', 'X32', 'audio', 3,
  [F('in', AA, 'XLR', 32, 'Mic In'), F('out', AA, 'XLR', 16, 'Out'), R('out', AO, 'XLR', 2, 'AES/EBU Out'),
   R('io', 'AES50', 'etherCON', 2, 'AES50'), R('out', 'Other', 'RJ45', 1, 'Ultranet'), R('out', 'Other', 'Toslink', 2, 'ADAT Out'),
   R('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), R('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), R('io', 'USB', 'USB-B', 1, 'USB'),
   R('in', 'Power', 'IEC', 1, 'Power')],
  '3U stagebox, 19 x 5.4 x 9.5 in. 32 Midas mic preamps, 16 XLR line outs, 2 AES/EBU outs, 2 AES50 (48 ch each), Ultranet for P-16, '
  '2 ADAT outs, MIDI, USB-B for updates. Check: which connectors are on the front vs rear.',
  'Full Compass product page', 'https://www.fullcompass.com/prod/278127-behringer-s32-digital-snake-stagebox-with-32-inputs-16-outputs')
B('s16', 'S16', 'S16 digital snake 16x8', 'X32', 'audio', 2,
  [F('in', AA, 'XLR', 16, 'Mic In'), F('out', AA, 'XLR', 8, 'Out'), R('io', 'AES50', 'etherCON', 2, 'AES50'),
   R('out', 'Other', 'RJ45', 1, 'Ultranet'), R('out', 'Other', 'Toslink', 2, 'ADAT Out'), R('in', 'Other', 'MIDI DIN', 1, 'MIDI In'),
   R('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), R('io', 'USB', 'USB-B', 1, 'USB'), F('out', AA, '1/4" TRS', 1, 'Phones'),
   R('in', 'Power', 'IEC', 1, 'Power')],
  '16 Midas preamps, 8 XLR outs, AES50, Ultranet and direct P-16 port, 2 ADAT, MIDI, USB, phones. 483 x 89 x 210 mm (2U), 4.9 kg. Check: AES50 port count (1 or 2) and front/rear split.', 'Thomann product page', 'https://www.thomann.ae/behringer_s16.htm', verified=False)

# ---------------- Yamaha ----------------
Y = lambda *a, **k: add('yamaha.json', 'yam-', 'Yamaha', *a, **k)
for code, ru, i, o, aes in [('Rio3224-D2', 4, 32, 16, 4), ('Rio1608-D2', 3, 16, 8, 0)]:
    ports = [F('in', AA, 'XLR', i, 'In'), F('out', AA, 'XLR', o, 'Out')]
    if aes: ports.append(F('out', AO, 'XLR', aes, 'AES/EBU Out'))
    ports += [R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Primary'), R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Secondary'),
              R('in', 'Power', 'IEC (V-lock)', 1, 'AC In')]
    Y(code.lower(), code, f'{code} Dante I/O rack', 'Rio', 'audio', ru, ports,
      f'Dante stagebox, {i} mic/line XLR inputs and {o} XLR outputs on the front' + (', 8 AES/EBU outputs on 4 XLR (1/2 to 7/8)' if aes else '') +
      '. Dante primary and secondary etherCON on the rear, dual internal power supplies on one V-lock AC inlet. '
      'Check: rack height (not stated in the manual).', 'Yamaha Rio3224-D2/Rio1608-D2 owner\'s manual',
      'https://usa.yamaha.com/products/proaudio/interfaces/r_series_adda_2/index.html', verified=False)
Y('tio1608-d2', 'Tio1608-D2', 'Tio1608-D2 Dante I/O rack', 'Tio', 'audio', 2,
  [F('in', AA, 'XLR/TRS combo', 16, 'In'), F('out', AA, 'XLR', 8, 'Out'), R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Primary'),
   R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Secondary'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '2U, 480 x 88 x 364 mm. 16 combo inputs (XLR or TRS), 8 XLR outputs, Dante primary/secondary on etherCON, for TF and DM3 consoles. '
  'Check: which face carries the Dante and power connectors.', 'Yamaha Tio1608-D2 datasheet', 'https://europe.yamaha.com/en/audio/portable-pa/products/accessories/tio1608-d2/')

# ---------------- Allen & Heath ----------------
A = lambda *a, **k: add('allenheath.json', 'ah-', 'Allen & Heath', *a, **k)
for code, ru, i, o in [('DM32', 7, 32, 16), ('DM48', 8, 48, 24), ('DM64', 10, 64, 32)]:
    A(f'dlive-{code.lower()}', f'dLive {code}', f'dLive {code} MixRack', 'dLive', 'audio', ru,
      [R('in', AA, 'XLR', i, 'Mic In'), R('out', AA, 'XLR', o, 'Line Out'), R('io', 'Other', 'Card slot', 3, 'I/O Port'),
       R('io', 'Other', 'etherCON', 2, 'gigaACE'), R('io', 'Other', 'etherCON', 4, 'DX'), R('out', 'Other', 'etherCON', 1, 'ME'),
       R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('in', 'Other', 'BNC', 1, 'Word Clock In'), R('out', 'Other', 'BNC', 1, 'Word Clock Out'),
       R('out', AA, '1/4" TRS', 1, 'Phones'), R('in', 'Power', 'IEC', 2, 'PSU')],
      f'{ru}U dLive S Class MixRack, {i} mic in, {o} line out (+4 dBu XLR), 3 I/O ports (128 x 128 each, e.g. Dante, MADI, Waves), '
      '2 gigaACE (redundant surface link), 4 DX ports for 2 redundant DX expanders, ME port, 2 gigabit network, word clock, hot-swap PSU '
      '(ships with one, second optional). Check: word clock BNC count.', 'dLive DM32/DM48/DM64 MixRack guide',
      'https://www.allen-heath.com/hardware/dlive/')
for code, ru, i, o in [('CDM32', 3, 32, 16), ('CDM48', 4, 48, 24), ('CDM64', 5, 64, 32)]:
    A(f'dlive-{code.lower()}', f'dLive {code}', f'dLive {code} MixRack (C Class)', 'dLive', 'audio', ru,
      [R('in', AA, 'XLR', i, 'Mic In'), R('out', AA, 'XLR', o, 'Line Out'), R('io', 'Other', 'Card slot', 1, 'I/O Port'),
       R('io', 'Other', 'etherCON', 1, 'gigaACE'), R('io', 'Other', 'etherCON', 2, 'DX'), R('io', 'Ethernet', 'RJ45', 1, 'Network'),
       R('in', 'Power', 'IEC', 1, 'Power')],
      f'dLive C Class MixRack, {i} mic in, {o} line out, XCVI 160x64 core, 1 I/O port. '
      'Check: rack height, DX/ME port count and network ports (from model naming, not a datasheet).',
      'Reseller listings', 'https://www.allen-heath.com/hardware/dlive/', verified=False)
A('dx168', 'DX168', 'DX168 96kHz expander 16x8', 'DX', 'audio', 4,
  [F('in', AA, 'XLR', 16, 'Mic In'), F('out', AA, 'XLR', 8, 'Line Out'), R('io', 'Other', 'etherCON', 1, 'DX A'),
   R('io', 'Other', 'etherCON', 1, 'DX B'), R('in', 'Power', 'IEC', 1, 'AC In')],
  'Portable 96 kHz expander for dLive, Avantis, SQ and AHM-64: 16 mic preamps, 8 XLR line outs, DX A and DX B (daisy chain or redundancy). '
  'Rack kit optional. Check: rack height (4U per dealer) and front/rear split.', 'DX168 datasheet', 'https://www.fullcompass.com/common/files/37069-DX168Datasheet.pdf', verified=False)
A('ab168', 'AB168', 'AB168 AudioRack 16x8', 'AudioRack', 'audio', 4,
  [F('in', AA, 'XLR', 16, 'Mic In'), F('out', AA, 'XLR', 8, 'Line Out'), R('io', 'Other', 'etherCON', 1, 'dSNAKE'),
   R('io', 'Other', 'etherCON', 1, 'Expander'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '48 kHz dSNAKE stagebox for SQ, Qu, Avantis and AHM-64: 16 mic in, 8 XLR line out, dSNAKE and expander/ME etherCON, 45 W internal supply. '
  'Rack kit optional. Check: rack height (4U per dealer).', 'AB168 datasheet', 'https://www.allen-heath.com/hardware/audiorack/', verified=False)
A('dx32', 'DX32', 'DX32 modular expander', 'DX', 'audio', 4,
  [R('io', 'Other', 'Card slot', 4, 'Module Slot'), R('io', 'Other', 'etherCON', 2, 'DX'), R('in', 'Power', 'IEC', 2, 'PSU')],
  'Modular 96 kHz expander with 4 slots for 8-channel modules (8 mic XLR in, 8 line XLR out, 4 stereo AES3 in or 4 stereo AES3 out), '
  'redundant DX etherCON pair, dual hot-swap PSU option. Add the module connectors as extra ports. Check: rack height.',
  'DX32 technical datasheet', 'https://www.allen-heath.com/hardware/dlive/', verified=False)

# ---------------- Klark Teknik (added 2026-11-11) ----------------
K = lambda *a, **k: add('klarkteknik.json', 'kt-', 'Klark Teknik', *a, **k)
KT = 'https://www.klarkteknik.com/en/products/'
K('dn9680', 'DN9680', 'DN9680 8-port AES50 extender and multiplexer', 'DN96xx networking', 'audio', 1,
  [R('io', 'AES50', 'etherCON', 8, 'AES50'), R('io', 'Ethernet', 'etherCON', 1, 'Control'), R('io', 'AES50', 'etherCON', 1, 'Snake (copper)'),
   R('io', 'Fibre', 'opticalCON DUO', 1, 'Snake (fibre)'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU steel. Multiplexes 8 AES50 streams onto one copper or fibre snake; single-mode opticalCON DUO up to 1000 m '
  '(DN9680-MM is the multi-mode version, 500 m). Universal auto-sensing PSU. Check: front/rear placement of the AES50 ports.',
  'Klark Teknik DN9680 product page and KT brochure', KT + '0606-ABL')
K('dn9680-mm', 'DN9680-MM', 'DN9680-MM 8-port AES50 extender (multi-mode fibre)', 'DN96xx networking', 'audio', 1,
  [R('io', 'AES50', 'etherCON', 8, 'AES50'), R('io', 'Ethernet', 'etherCON', 1, 'Control'), R('io', 'AES50', 'etherCON', 1, 'Snake (copper)'),
   R('io', 'Fibre', 'opticalCON DUO', 1, 'Snake (fibre MM)'), R('in', 'Power', 'IEC', 1, 'AC In')],
  'Multi-mode version of the DN9680, fibre snake up to 500 m.', 'Klark Teknik KT brochure', KT + '0606-ACS')
K('dn9620', 'DN9620', 'DN9620 dual-port AES50 extender', 'DN96xx networking', 'audio', 1,
  [R('io', 'AES50', 'etherCON', 2, 'AES50'), R('io', 'USB', 'USB-B', 1, 'USB (config)'), R('io', 'AES50', 'etherCON', 1, 'Snake (copper)'),
   R('io', 'Fibre', 'opticalCON DUO', 1, 'Snake (fibre MM)'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU half-rack, rack bracket included. 2 AES50 ports over one multi-mode fibre (up to 500 m) or copper snake.',
  'Klark Teknik KT brochure', KT + '0606-ABM', w=6)
K('dn9650', 'DN9650', 'DN9650 network bridge (AES50 to Dante/MADI etc.)', 'DN96xx networking', 'audio', 1,
  [R('io', 'AES50', 'etherCON', 3, 'AES50'), R('io', 'Other', 'Card slot', 1, 'Network module (KT-DANTE64/KT-MADI)'),
   R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out'), R('in', 'Reference', 'BNC', 1, 'Black Burst In'),
   R('io', 'Ethernet', 'RJ45', 1, 'Control'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU, 483 x 44 x 411 mm, 5.1 kg. Up to 64 bidirectional channels between AES50 and a third-party network via a module '
  '(KT-DANTE64 Dante, KT-MADI, KT-USB, KT-AES50), ASRC between domains. Add the fitted module\'s connectors as extra ports. '
  'Check: AES50 port count (page says "all three") and control port connector.', 'Klark Teknik DN9650 product page', KT + '0606-AAZ',
  verified=False)
K('dn9652', 'DN9652', 'DN9652 dual network bridge', 'DN96xx networking', 'audio', 1,
  [R('io', 'Other', 'Card slot', 2, 'Network module A/B'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'),
   R('out', 'Reference', 'BNC', 1, 'Word Clock Out'), R('in', 'Reference', 'BNC', 1, 'Black Burst In'),
   R('io', 'Ethernet', 'etherCON', 1, 'Control'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU, 483 x 44 x 411 mm, 5.0 kg, <50 W. Bridges two third-party networks (64 channels each way) using two modules: KT-DANTE64, '
  'KT-MADI, KT-USB or KT-AES50. Add the modules\' connectors as extra ports.', 'Klark Teknik DN9652 product page and KT brochure', KT + '0606-ABA')
K('dm8000', 'DM8000', 'DM8000 installation DSP (10 in / 6 out, AEC)', 'DM processors', 'audio', 1,
  [R('in', AA, 'Euroblock', 10, 'Mic/Line In'), R('out', AA, 'Euroblock', 6, 'Out'), R('io', 'Other', 'RJ45', 2, 'ULTRANET'),
   R('io', 'USB', 'USB-B', 1, 'USB Audio'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'Other', 'DB9F', 1, 'RS232'),
   R('io', 'Other', 'Euroblock', 6, 'GPIO'), R('io', 'Other', 'Card slot', 1, 'Expansion module'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU, 483 x 49 x 300 mm, 48 W. 10 balanced inputs (8 with acoustic echo cancellation, +48 V phantom), 6 outputs, ULTRANET 16x16, '
  'USB audio 2x2. Optional expansion (e.g. DM80 Ultranet). Check: GPIO connector type.', 'Klark Teknik DM8000 data sheet',
  'https://www.fullcompass.com/common/files/38553-DM8000DataSheet.pdf')
K('dm8500', 'DM8500', 'DM8500 installation DSP with Dante (10 in / 6 out)', 'DM processors', 'audio', 1,
  [R('in', AA, 'Euroblock', 10, 'Mic/Line In'), R('out', AA, 'Euroblock', 6, 'Out'), R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec (64x64)'),
   R('out', 'Other', 'RJ45', 1, 'ULTRANET Out (16)'), R('io', 'USB', 'USB-B', 1, 'USB Audio'), R('io', 'Other', 'Euroblock', 6, 'GPIO'),
   R('io', 'Other', 'DB9F', 1, 'RS232'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '1RU, 483 x 44 x 293 mm, <48 W. Like the DM8000 with Dante 64x64 on two RJ45. Check: input connector type and Ethernet control port.',
  'Klark Teknik KT brochure', KT + '0829-ABH', verified=False)
K('76-kt', '76-KT', '76-KT FET compressor (1176-style)', 'KT classics', 'audio', 2,
  [R('in', AA, 'XLR3F', 1, 'In'), R('out', AA, 'XLR3M', 1, 'Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '2RU steel, discrete FET compressor with MIDAS transformers and VU meter, universal PSU. Check: connector counts (page gives types only).',
  'Klark Teknik 76-KT product page', KT + '0817-ABA', verified=False)
K('2a-kt', '2A-KT', '2A-KT tube optical leveling amplifier (LA-2A-style)', 'KT classics', 'audio', 2,
  [R('in', AA, 'XLR3F', 1, 'In'), R('in', AA, '6.3mm TRS', 1, 'In (TRS)'), R('out', AA, 'XLR3M', 1, 'Out'), R('out', AA, '6.3mm TRS', 1, 'Out (TRS)'),
   R('io', 'Other', '6.3mm TRS', 1, 'Stereo Link'), R('in', 'Power', 'IEC', 1, 'AC In')],
  'Tube leveling amplifier with optical attenuator and MIDAS transformers; XLR and TRS balanced I/O, stereo-link TRS. '
  'Check: rack height and power inlet (not on the product page).', 'Klark Teknik 2A-KT product page', KT + '0817-ABI', verified=False)
K('sq1d', 'Square ONE Dynamics', 'Square ONE Dynamics 8-channel compressor/gate', 'Square ONE', 'audio', 3,
  [R('in', AA, 'XLR3F', 8, 'In'), R('out', AA, 'XLR3M', 8, 'Out'), R('in', AA, '6.3mm TRS', 8, 'Sidechain'),
   R('in', AA, 'XLR3F', 1, 'Solo Bus In'), R('out', AA, 'XLR3M', 1, 'Solo Bus Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
  '3RU, 483 x 133 x 227 mm, 4.7 kg, 100-240 V. 8 dual-mode compressor/gate channels, balanced Neutrik XLR I/O, TRS key input per channel. '
  'Discontinued but common in racks.', 'Pro Acoustics listing (manufacturer data)', 'https://www.proacousticsusa.com/klark-teknik-square-one-dynamics-8-channel-dual-mode-compressor-gate.html')
K('dn360', 'DN360', 'DN360 dual 31-band graphic equaliser', 'DN analogue', 'audio', 3,
  [R('in', AA, 'XLR3F', 2, 'In'), R('out', AA, 'XLR3M', 2, 'Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
  'Classic 2-channel 1/3-octave graphic EQ. Check: rack height (3RU assumed) and any extra connectors such as the remote/bypass port.',
  'Klark Teknik DN360 dealer listings', 'https://www.adorama.com/ktdn360b.html', verified=False)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
# append our files to index.json without disturbing other threads' entries
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(idx)
