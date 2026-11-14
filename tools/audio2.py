#!/usr/bin/env python3
"""Broadcast audio cores, I/O and monitoring (added 2026-11-14):
  calrec.json, ssl.json, digico.json, stagetec.json, wohler.json, rtw.json, dhd.json, merging.json, focusrite.json.
Console surfaces are not rack gear and are left out; their cores, engines, I/O racks and monitors are in.
Specs from each maker's data sheet or dealer listing (each entry's source). Modular frames (Calrec modular I/O, DiGiCo SD-Rack,
Stagetec NEXUS) are plain units whose notes give the slot count; add their I/O as wired. 'Check:' marks anything unconfirmed."""
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
def PSU(n=2, conn='IEC C14'): return R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')
DANTE = lambda conn='RJ45': R('io', 'Dante/AES67', conn, 2, 'Dante Pri/Sec')
WC = [R('in', 'Reference', 'BNC', 1, 'Word Clock In'), R('out', 'Reference', 'BNC', 1, 'Word Clock Out')]

# ======================= Calrec =======================
CA = ('Calrec Hydra2 and ImPulse pages', 'https://calrec.com/hydra2/')
def calrec(id, pn, name, fam, ru, ports, notes, verified=False):
    add('calrec.json', 'calrec-' + id, 'Calrec', pn, name, fam, 'audio', ru, ports, notes, CA[0], CA[1], verified, full=True)
H2 = lambda n: R('io', 'SFP', 'SFP', n, 'Hydra2 SFP')
calrec('impulse1', 'ImPulse1', 'ImPulse1 IP audio processing core, 1U', 'ImPulse', 1,
       [R('io', 'SFP', 'SFP', 4, 'ST 2110 / AES67 SFP'), R('io', 'Ethernet', 'RJ45', 2, 'Control'), PSU()],
       'Compact ST 2110-30 / AES67 core with two cores inside for redundancy and dual AC PSUs, up to 432 processing paths. '
       'Drives Argo surfaces. Check: SFP and control port counts.')
calrec('impulse-5u', 'ImPulse', 'ImPulse IP audio processing core, 5U', 'ImPulse', 5,
       [R('io', 'SFP', 'SFP', 8, 'ST 2110 / AES67 SFP'), R('io', 'Ethernet', 'RJ45', 2, 'Control'), PSU()],
       'Modular ST 2110 / AES67 processing core for Argo and Apollo/Artemis surfaces, redundant DSP, router and PSU modules. '
       'Can bridge to Hydra2 I/O. Check: rear port counts.')
for ru, ex in ((4, ''), (8, ' Takes two router expander modules for more Hydra2 ports.')):
    calrec(f'hydra2-core-{ru}u', f'Hydra2 {ru}U core', f'Hydra2 {ru}U processing and routing core', 'Hydra2', ru,
           [H2(16 if ru == 4 else 32), R('io', 'SFP', 'SFP', 4, 'Surface SFP'), R('io', 'Ethernet', 'RJ45', 2, 'Router control (SW-P-08/Ember)'), PSU()],
           'Primary and secondary router cards (SFP ports, copper or fibre, for Hydra2 I/O boxes and other cores), primary and '
           'secondary control processors (2 SFP each for the surface), two PSUs.' + ex + ' Check: SFP counts per router card.')
calrec('modular-io-apex-m6', 'Apex M6', 'Hydra2 modular I/O frame, 1U, 6 card slots', 'Hydra2 I/O', 1,
       [H2(2), PSU()], '1U modular I/O box with 6 I/O card slots (mic/line, AES, MADI, SDI, Dante, GPIO cards). Two Hydra2 SFP ports '
       '(primary and secondary). Add the I/O of the cards fitted as you wire it. Check: PSU count.')
calrec('modular-io-3u', 'Hydra2 modular I/O 3U', 'Hydra2 modular I/O frame, 3U, 20 card slots', 'Hydra2 I/O', 3,
       [H2(2), PSU()], '3U modular I/O box with 20 I/O card slots. Two Hydra2 SFP ports, redundant PSUs. Add the I/O of the cards fitted as you wire it.')
calrec('h2-ip-gateway', 'H2-IP', 'Hydra2 H2-IP gateway, ST 2110 / AES67', 'Hydra2 I/O', 1,
       [H2(2), R('io', 'SFP', 'SFP', 2, 'ST 2110 / AES67'), PSU()], 'Interface between a Hydra2 network and an ST 2110 / AES67 network. Check: RU and ports.')

# ======================= SSL =======================
SS = ('SSL Network I/O stageboxes page', 'https://www.solidstatelogic.com/products/stageboxes-broadcast')
def ssl(id, pn, name, ru, ports, notes, verified=True, **k):
    add('ssl.json', 'ssl-' + id, 'Solid State Logic', pn, name, 'Network I/O', 'audio', ru, ports, notes, SS[0], SS[1], verified, **k)
ssl('sb-32-24', 'SB 32.24', 'SB 32.24 Dante stagebox, 32 mic in / 16 line out + 8 AES', 5,
    [R('in', 'Analog audio', 'XLR3F', 32, 'Mic/Line In'), R('out', 'Analog audio', 'XLR3M', 16, 'Line Out'),
     R('io', 'AES/EBU', 'XLR3F', 4, 'AES I/O pair'), DANTE('etherCON'), R('io', 'SFP', 'SFP', 1, 'Network SFP'), R('io', 'GPIO', 'DB25', 1, 'GPIO'), PSU()],
    '5U Dante/AES67 stagebox with remote-controlled mic pres, 16 analogue outs and 4 AES3 pairs, redundant Dante, one '
    'user SFP (RJ45 or fibre), dual PSUs. Check: connector placement (front or rear) and AES/GPIO connectors.', verified=False)
ssl('sb-16-12', 'SB 16.12', 'SB 16.12 Dante stagebox, 16 mic in / 8 line out + 4 AES', 3,
    [R('in', 'Analog audio', 'XLR3F', 16, 'Mic/Line In'), R('out', 'Analog audio', 'XLR3M', 8, 'Line Out'),
     R('io', 'AES/EBU', 'XLR3F', 2, 'AES I/O pair'), DANTE('etherCON'), R('io', 'SFP', 'SFP', 1, 'Network SFP'), PSU()],
    '3U Dante/AES67 stagebox, redundant Dante, one user SFP, dual PSUs. Check: connector placement and AES connectors.', verified=False)
ssl('sb-8-8', 'SB 8.8', 'SB 8.8 Dante stagebox, 8 mic in / 8 line out', 2,
    [F('in', 'Analog audio', 'XLR3F', 8, 'Mic/Line In'), F('out', 'Analog audio', 'XLR3M', 8, 'Line Out'), DANTE('etherCON'),
     R('io', 'GPIO', 'DB25', 1, 'GPIO'), PSU()],
    '2U Dante/AES67 stagebox with redundant Dante and PSUs, GPIO. SB i16 is the 16-input version. Check: GPIO connector.', verified=False)
ssl('sb-i16', 'SB i16', 'SB i16 Dante stagebox, 16 mic in', 2,
    [F('in', 'Analog audio', 'XLR3F', 16, 'Mic/Line In'), DANTE('etherCON'), R('io', 'GPIO', 'DB25', 1, 'GPIO'), PSU()],
    '2U Dante/AES67 16-input stagebox, redundant Dante and PSUs, GPIO. Check: GPIO connector.', verified=False)

# ======================= DiGiCo =======================
DG = ('DiGiCo racks brochure (2013) and 4REA4 data sheet', 'https://digico.biz/')
def digico(id, pn, name, ru, ports, notes, verified=False, **k):
    add('digico.json', 'digico-' + id, 'DiGiCo', pn, name, 'Racks', 'audio', ru, ports, notes, DG[0], DG[1], verified, full=True, **k)
MADI2 = [R('in', 'MADI audio', 'BNC', 2, 'MADI In'), R('out', 'MADI audio', 'BNC', 2, 'MADI Out')]
digico('sd-rack', 'SD-Rack', 'SD-Rack stage rack, 14 I/O card slots', 10,
       MADI2 + [R('io', 'Fibre', 'Other', 2, 'Optocore (option)'), PSU()],
       '10U stage rack with 14 eight-channel card slots (mic, line out, AES), up to 56 in and 56 out, dual MADI, optional '
       'optics, two hot-swap PSUs. 466 mm deep. Add the card I/O as you wire it.')
digico('sd-mini-rack', 'SD-MiNi Rack', 'SD-MiNi Rack compact stage rack', 4,
       MADI2 + [R('io', 'Fibre', 'Other', 2, 'Optocore (option)'), PSU()],
       '4U rack, up to 32 in and 32 out in banks of 8 (analogue or digital cards: AES, Dante, AES42, ADAT, HD-SDI). Dual PSUs. 408 mm deep.')
digico('sd-nano-rack', 'SD-NaNo Rack', 'SD-NaNo Rack, optical', 2,
       [R('io', 'Fibre', 'Other', 2, 'Optocore'), PSU()], '2U optical rack with half the MiNi capacity (for example 8 mic in, 8 line out, 16 AES). Dual PSUs.')
digico('d2-rack', 'D2-Rack', 'D2-Rack stage rack, 48 in / 8 out', 4,
       [R('in', 'Analog audio', 'XLR3F', 48, 'Mic In'), R('out', 'Analog audio', 'XLR3M', 8, 'Line Out'), R('io', 'Ethernet', 'etherCON', 2, 'Cat5 (MADI)'),
        R('io', 'MADI audio', 'BNC', 2, 'MADI'), PSU()],
       'Expandable stage box, 48 mic in and 8 outs, more outputs with modules. Cat5, BNC MADI or optical versions. Check: RU and connectors.')
digico('4rea4', '4REA4', '4REA4 centralised DSP engine, 6U', 6,
       [R('io', 'Ethernet', 'etherCON', 4, 'A3232 I/O'), R('io', 'Ethernet', 'etherCON', 2, 'ASTAR Pri/Sec'), R('io', 'Ethernet', 'RJ45', 1, 'Control'),
        R('io', 'Other', 'Card slot', 4, 'DMI slot'), R('io', 'Other', 'Card slot', 3, 'SD-Rack card slot')] + WC +
       [R('io', 'GPIO', 'Euroblock', 2, 'GPI/GPO'), F('io', 'USB', 'USB-A', 1, 'USB'), F('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), PSU()],
       '6U engine: 128 inputs into a 128 x 56 matrix, 4 DMI slots (MADI, Dante, Optocore, Waves, AES, mic, AVIOM), 3 SD-Rack '
       'card slots, 4 A3232 remote I/O ports, dual ASTAR. 380 mm deep, 20.2 kg, dual IEC PSUs (90 W each).', verified=True,
       powerW=180, weightKg=20.2)

# ======================= Stagetec =======================
add('stagetec.json', 'stagetec-nexus-base-3u', 'Stage Tec', 'NEXUS Base Device 3U', 'NEXUS Base Device, 3U mainframe', 'NEXUS', 'audio', 3,
    [R('io', 'Fibre', 'Other', 2, 'NEXUS fibre link'), PSU()],
    'NEXUS audio network / router mainframe on a 4 HP grid with 3U slide-in boards (analogue, AES, MADI, Dante, SDI, DSP and fibre '
    'boards). Also made in 1U, 6U, 9U, 12U and 15U. Add the board I/O as you wire it. Check: link and PSU connectors.',
    'Audinate NEXUS Base Devices listing', 'https://audinate.com/products/dante-enabled/stage-tec/stage-tec-nexus-base-devices', verified=False, full=True)
add('stagetec.json', 'stagetec-nexus-base-6u', 'Stage Tec', 'NEXUS Base Device 6U', 'NEXUS Base Device, 6U mainframe', 'NEXUS', 'audio', 6,
    [R('io', 'Fibre', 'Other', 4, 'NEXUS fibre link'), PSU()],
    'Larger NEXUS mainframe, two rows of 3U boards. Add the board I/O as you wire it. Check: link and PSU connectors.',
    'Audinate NEXUS Base Devices listing', 'https://audinate.com/products/dante-enabled/stage-tec/stage-tec-nexus-base-devices', verified=False, full=True)

# ======================= Wohler =======================
add('wohler.json', 'wohler-iam-12g-sdi', 'Wohler', 'iAM-12G-SDI', 'iAM-12G-SDI audio monitor, 2RU', 'iAM', 'audio', 2,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('io', 'AES/EBU', 'HD15', 1, 'AES 4 pairs'), R('io', 'Analog audio', 'DB25', 2, 'Analogue 16 ch'),
     R('io', 'SFP', 'SFP', 4, 'SFP (option)'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones'),
     F('io', 'USB', 'USB-A', 1, 'USB'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '2RU touchscreen audio monitor for 12G-SDI, AES, analogue, with 4 SFP cages for fibre, SDI, HDMI, ST 2110 or 2022-6 modules. '
    'Options add MADI (BNC), more analogue, TOSLINK, Dante or RAVENNA. 40 W, 242 mm deep, 5 kg. Check: power inlet.',
    'Wohler iAM-12G-SDI data sheet', 'https://www.wohler.com/wp-content/uploads/2023/07/iAM-12G-SDI_d.pdf', verified=False, powerW=40, weightKg=5.0)
add('wohler.json', 'wohler-iam1-12g', 'Wohler', 'iAM1-12G', 'iAM1-12G triple-screen audio monitor, 1RU', 'iAM', 'audio', 1,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('io', 'Analog audio', 'DB25', 1, 'Analogue'), R('io', 'SFP', 'SFP', 2, 'SFP (option)'),
     R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '1RU audio monitor with three touchscreens, 6-channel metering, 12G-SDI and analogue. Check: all connector counts (from the product title).',
    'Wohler iAM1-12G listing', 'https://www.wohler.com/wp-content/uploads/2023/06/iAM1-12G_d.pdf', verified=False)

# ======================= RTW =======================
add('rtw.json', 'rtw-tm7-rack', 'RTW', 'TM7-Rack', 'TouchMonitor TM7-Rack 7-inch loudness meter, 3U half rack', 'TouchMonitor', 'audio', 3,
    [R('in', 'AES/EBU', 'DB25', 1, 'AES 8 ch'), R('in', '3G-SDI', 'BNC', 1, 'SDI (option)'), R('out', 'VGA', 'VGA', 1, 'VGA Out'),
     R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-A', 2, 'USB'), R('io', 'GPIO', 'DB9', 1, 'GPIO'),
     R('in', 'Power', 'DC locking', 1, '12-24V DC')],
    'Half-19-inch 3U (42 HP) panel with a 7-inch touchscreen loudness and level meter. 8-channel AES on D-sub 25, optional 3G-SDI, '
    'analogue options. External 12-24 V PSU (Binder 710). TM9 has a separate 4U rack kit (TM9-MA4U). Check: GPIO connector.',
    'RTW TM7-Rack listing (Vintage King)', 'https://vintageking.com/products/rtw-7-rack-touchmonitor-for-tv-broadcast-and-post-production',
    verified=False, w=6)

# ======================= DHD =======================
DH = ('DHD XC3 / XD3 flyer', 'https://dhd.audio/systems/xc3/')
add('dhd.json', 'dhd-xc3', 'DHD.audio', '52-7520', 'XC3 IP audio core', 'XC3', 'audio', 2,
    [R('io', 'Dante/AES67', 'RJ45', 2, 'AES67 / Dante (IPx)'), R('io', 'SFP', 'SFP', 4, 'GA / MADI SFP'), R('io', 'Other', 'Card slot', 12, 'APC slot'),
     R('io', 'Ethernet', 'RJ45', 1, 'Control')] + WC + [R('in', 'Reference', 'BNC', 1, 'Video Sync'), R('in', 'Power', 'Other', 2, '48V DC A/B')],
    'Mixing core for radio and TV desks up to 48 faders, 72 stereo busses. 12 APC slots for I/O and control modules, 4 GA/MADI SFP '
    'slots, one IPx slot (Dante 64/512 ch or AES67 64/128 ch), redundant 48 V inputs, word clock / AES11 / video sync. '
    'Check: rack height and connector counts.', DH[0], DH[1], verified=False)
add('dhd.json', 'dhd-xd3', 'DHD.audio', '52-7550', 'XD3 high-capacity IP audio core', 'XD3', 'audio', 2,
    [R('io', 'Dante/AES67', 'RJ45', 4, 'AES67 / Dante (IPx)'), R('io', 'SFP', 'SFP', 4, 'GA / MADI SFP'), R('io', 'Other', 'Card slot', 4, 'APC slot'),
     R('io', 'Ethernet', 'RJ45', 1, 'Control')] + WC + [R('in', 'Reference', 'BNC', 1, 'Video Sync'), R('in', 'Power', 'Other', 2, '48V DC A/B')],
    'High-capacity core: up to 96 stereo faders, 126 busses, up to 24 Gigabit audio ports with the 52-7540 IP router, two IPx slots, '
    'up to 5 DSPs. 52-7554 is the quad-core version. Check: rack height and connector counts.', DH[0], 'https://dhd.audio/systems/xd3/', verified=False)

# ======================= Merging =======================
MG = ('Merging Technologies Horus / Hapi MkII product information', 'https://merging.com/products/interfaces/horus')
add('merging.json', 'merging-horus', 'Merging Technologies', 'Horus', 'Horus RAVENNA/AES67 networked converter, 2U', 'Horus', 'audio', 2,
    [R('io', 'Other', 'Card slot', 6, 'I/O card slot'), R('io', 'SFP', 'SFP', 3, 'MADI SFP'), R('io', 'Dante/AES67', 'RJ45', 2, 'AES67 / RAVENNA')]
    + WC + [R('in', 'Timecode', 'XLR3F', 1, 'LTC'), F('out', 'Analog audio', '1/4" TRS', 2, 'Headphones'), PSU()],
    '2U AES67 / RAVENNA / ST 2110-30 converter with modular analogue, mic and AES cards, MADI on SFP, redundant PSUs. '
    'Check: all connector counts (from memory of the data sheet).', MG[0], MG[1], verified=False)
add('merging.json', 'merging-hapi-mkii', 'Merging Technologies', 'Hapi MkII', 'Hapi MkII RAVENNA/AES67 networked converter, 1U', 'Hapi', 'audio', 1,
    [R('io', 'Other', 'Card slot', 2, 'I/O card slot'), R('io', 'Other', 'Card slot', 1, 'Option slot (MADI/Dante)'),
     R('io', 'Dante/AES67', 'RJ45', 2, 'AES67 / RAVENNA')] + WC + [F('out', 'Analog audio', '1/4" TRS', 2, 'Headphones'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '1U converter with two 8-channel I/O card slots and one option slot (MADI SFP or Dante), OLED display. '
    'Check: all connector counts (from memory of the data sheet).', MG[0], MG[1], verified=False)

# ======================= Focusrite RedNet =======================
FR = ('Canford Focusrite RedNet listings', 'https://www.canford.co.uk/FOCUSRITE-AUDIO-INTERFACES-AoIP')
def rn(id, pn, name, ru, ports, notes, url, verified=True):
    add('focusrite.json', 'focusrite-' + id, 'Focusrite', pn, name, 'RedNet', 'audio', ru, ports + [DANTE(), PSU()], notes, FR[0], url, verified)
DARS = R('in', 'AES/EBU', 'XLR3F', 1, 'DARS In')
rn('rednet-a16r-mkii', 'RedNet A16R MkII', 'RedNet A16R MkII 16 x 16 analogue Dante interface', 1,
   [R('in', 'Analog audio', 'DB25', 2, 'Analogue In 1-16'), R('out', 'Analog audio', 'DB25', 2, 'Analogue Out 1-16')] + WC + [DARS],
   '16 x 16 line-level analogue on AES59 D-sub, plus an AES3 pair on channels 17-18, redundant Dante and dual PSUs. '
   'Check: where the AES pair connects.', 'https://focusrite.com/products/rednet-a16r-mkii')
rn('rednet-d16r-mkii', 'RedNet D16R MkII', 'RedNet D16R MkII 16 x 16 AES3 Dante interface', 1,
   [R('io', 'AES/EBU', 'DB25', 2, 'AES 1-16'), R('in', 'AES/EBU', 'XLR3F', 1, 'AES In 1-2'), R('out', 'AES/EBU', 'XLR3M', 1, 'AES Out 1-2'),
    R('in', 'Other', 'RCA', 1, 'S/PDIF In'), R('out', 'Other', 'RCA', 1, 'S/PDIF Out')] + WC + [DARS],
   '16 x 16 AES3 (8 pairs) on two D-subs, plus XLR and S/PDIF, redundant Dante and dual PSUs.', 'https://focusrite.com/products/rednet-d16r-mkii')
rn('rednet-d64r', 'RedNet D64R', 'RedNet D64R 64 x 64 MADI Dante bridge', 1,
   [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), R('io', 'Fibre', 'SC', 2, 'MADI optical')] + WC,
   '64 x 64 MADI to Dante on coax and duplex SC optical, redundant Dante and dual PSUs.', 'https://focusrite.com/')
rn('rednet-hd32r', 'RedNet HD32R', 'RedNet HD32R 32 x 32 Pro Tools HD Dante bridge', 2,
   [R('io', 'Other', 'Other', 2, 'DigiLink'), R('io', 'Other', 'Other', 1, 'Expansion')] + WC,
   '32 x 32 Pro Tools | HD / HDX to Dante (16 x 16 in expansion mode), Mini-DigiLink ports, redundant Dante and dual PSUs.',
   'https://vintageking.com/cdn/shop/files/focusrite_rednet_hd32r1_DATA_SHEET.pdf')
rn('rednet-mp8r', 'RedNet MP8R', 'RedNet MP8R 8-channel remote mic pre with Dante', 1,
   [R('in', 'Analog audio', 'XLR3F', 8, 'Mic/Line In'), R('out', 'Analog audio', 'DB25', 1, 'Split Out 1-8')] + WC,
   '8 remote-controlled mic pres with an analogue split output per channel, redundant Dante and dual PSUs. '
   'Check: split output connector.', 'https://focusrite.com/', verified=False)

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
