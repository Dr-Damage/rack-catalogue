#!/usr/bin/env python3
"""Generates catalogue files for brands first met on site drawings (added 2026-11-11 for the CAR rack import):
evertz.json (standalone Evertz units; frames and cards stay in evertz-frames.json), avid.json, synology.json, hpe.json,
tieline.json, dejero.json and bmd-legacy.json (discontinued Blackmagic units; ids use `bmdl-` because `bmd-` is reserved
for the app's built-in Blackmagic catalogue). verified=False and a 'Check:' note mark anything not confirmed from a maker's document."""
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

# ---------------- Evertz (standalone) ----------------
EV = lambda *a, **k: add('evertz.json', 'evertz-', 'Evertz', *a, **k)
EV('5601msc', '5601MSC', '5601MSC master clock / SPG', 'Master clock', 'other', 1,
   [R('out', 'Reference', 'HD-BNC', 6, 'Sync Out'), R('out', 'Timecode', 'Mini-XLR', 2, 'LTC/IRIG Out'), R('out', 'AES/EBU', 'HD-BNC', 2, 'DARS Out'),
    R('out', 'Reference', 'BNC', 2, 'Word Clock Out'), R('io', 'Ethernet', 'SFP28', 2, 'PTP SFP28'), R('io', 'Ethernet', 'QSFP28', 2, 'PTP QSFP28'),
    R('io', 'Ethernet', 'RJ45', 2, 'Control'), R('in', 'Other', 'GNSS antenna', 2, 'GNSS In'), F('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU, 483 x 45 x 292 mm. GNSS-locked master clock and SPG: 6 configurable black burst / tri-level / 10 MHz / 1PPS outputs (HD-BNC), '
   '2 LTC/IRIG outputs, 2 DARS outputs, 2 word clock outputs, PTP grandmaster on 2 SFP28 + 2 QSFP28, 2 control Ethernet, 2 GNSS inputs. '
   'Front-mounted hot-swap PSU, second one optional (+2PS), 200 W max. Pairs with the 5601ACO2 changeover. '
   'Check: rear connector layout and the word clock connector type.',
   'Evertz 5601MSC product page', 'https://evertz.com/products/5601MSC', verified=False, full=True)
EV('5601aco2', '5601ACO2', '5601ACO2 automatic changeover', 'Master clock', 'other', 2,
   [R('in', 'Reference', 'BNC', 16, 'A In'), R('in', 'Reference', 'BNC', 16, 'B In'), R('out', 'Reference', 'BNC', 16, 'Out'),
    R('in', 'Timecode', 'DB15', 2, 'LTC/IRIG In'), R('out', 'Timecode', 'XLR-3M', 2, 'LTC/IRIG Out'),
    R('io', 'Other', 'Terminal block', 1, 'ACO GPI/GPO'), R('io', 'Other', 'Terminal block', 1, 'MSC GPI/GPO'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '2RU, 90 mm high. Automatic changeover between two 5601MSC master clocks: 16 coax groups, each with an A input, a B input and one output '
   '(3G/HD/SD video, bi/tri-level sync, ATG, 10 MHz, word clock, AES/DARS); LTC/IRIG in (DB15, one per 5601MSC) and out (XLR); GPI/GPO on '
   'removable terminal blocks; two redundant 40 W supplies, each with its own cord. Check: separate AES and analog audio changeover connectors.',
   'Evertz 5601ACO2 user manual', 'https://evertz.com/products/5600ACO', full=False)

# ---------------- Avid ----------------
AV = lambda *a, **k: add('avid.json', 'avid-', 'Avid', *a, **k)
AV('nexis-e4', 'NEXIS | E4', 'NEXIS E4 storage engine', 'NEXIS', 'computer', 4,
   [R('io', 'Ethernet', 'QSFP', 2, '40GbE'), R('io', 'Ethernet', 'SFP+', 4, '10GbE'), R('io', 'Ethernet', 'RJ45', 2, 'Management'),
    R('in', 'Power', 'IEC', 2, 'PSU')],
   '4U shared-storage engine for Avid NEXIS with 60 drive slots (top-loading drawers), two controllers with redundant PSUs. '
   'Check: controller network ports for your build (10/40/100GbE) and whether a System Director / NEXIS | E2 sits alongside.',
   'Avid NEXIS product information', 'https://www.avid.com/products/avid-nexis', verified=False, full=True)

# ---------------- Synology ----------------
SY = lambda *a, **k: add('synology.json', 'synology-', 'Synology', *a, **k)
SY('sa3400', 'SA3400', 'SA3400 12-bay rackmount NAS', 'SA series', 'computer', 2,
   [R('io', 'Ethernet', 'RJ45', 4, '1GbE'), R('io', 'Ethernet', 'SFP+', 2, '10GbE'), R('io', 'Other', 'Card slot', 2, 'PCIe slot'),
    R('io', 'Other', 'Mini-SAS HD', 2, 'Expansion'), R('io', 'USB', 'USB-A', 2, 'USB 3.2'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '2U, 12 x 3.5/2.5 in hot-swap bays, Intel Xeon D-1541, 4 x 1GbE RJ45 and 2 x 10GbE SFP+ onboard, 2 PCIe 3.0 x8 slots, '
   '2 expansion ports for RX1217sas units, redundant PSUs. Rails needed (a support shelf is often fitted under it).',
   'Synology SA3400 datasheet', 'https://www.synology.com/en-global/products/SA3400', full=True)

# ---------------- HPE ----------------
HP = lambda *a, **k: add('hpe.json', 'hpe-', 'HPE', *a, **k)
HP('dl360p-gen8', 'ProLiant DL360p Gen8', 'ProLiant DL360p Gen8 1U server (legacy)', 'ProLiant', 'computer', 1,
   [R('out', 'Other', 'VGA', 1, 'VGA'), R('io', 'Other', 'DB9', 1, 'Serial'), R('io', 'USB', 'USB-A', 4, 'USB 2.0'),
    R('io', 'Ethernet', 'RJ45', 4, '1GbE FlexibleLOM'), R('io', 'Ethernet', 'RJ45', 1, 'iLO 4'), R('io', 'Other', 'Card slot', 2, 'PCIe slot'),
    R('in', 'Power', 'IEC C14', 2, 'PSU')],
   '1U two-socket Xeon E5-2600 / v2 server (2012-2015), 4-port 1GbE FlexibleLOM (or 2 x 10GbE), dedicated iLO 4, 2 PCIe slots, '
   'redundant Flex Slot PSUs. Check: FlexibleLOM fitted and PCIe cards.',
   'HPE QuickSpecs DL360p Gen8', 'https://www.hpe.com/psnow/doc/c04123079', verified=False, full=True)

# ---------------- Tieline ----------------
TL = lambda *a, **k: add('tieline.json', 'tieline-', 'Tieline', *a, **k)
for code, ch, notes in [('Gateway', 16, 'Up to 16 IP audio codec channels (8 stereo) '), ('Gateway 4', 4, 'Up to 4 IP audio codec channels ')]:
    TL(code.lower().replace(' ', ''), code, f'{code} IP audio codec', 'Gateway', 'audio', 1,
       [R('io', 'Analog audio', 'XLR', 2, 'Analog In/Out'), R('io', 'AES/EBU', 'XLR', 1, 'AES3'), R('io', 'Dante/AES67', 'RJ45', 2, 'AoIP'),
        R('io', 'Ethernet', 'RJ45', 2, 'WAN'), R('io', 'Other', 'DB15', 1, 'GPIO'), R('io', 'USB', 'USB-A', 1, 'USB'),
        R('in', 'Power', 'IEC', 2, 'PSU')],
       f'1RU multichannel IP audio codec for radio and STL links. {notes}over Dante/AES67/ST 2110-30 (and WheatNet-IP, Livewire), '
       'dual Ethernet WAN with SmartStream Plus redundancy, dual redundant PSUs. '
       'Check: analog and AES I/O counts on the rear (the Gateway is mainly an AoIP device).',
       'Tieline Gateway product page', 'https://www.tieline.com/gateway/', verified=False)

# ---------------- Dejero ----------------
DJ = lambda *a, **k: add('dejero.json', 'dejero-', 'Dejero', *a, **k)
DJ('waypoint', 'WayPoint', 'WayPoint receiver', 'WayPoint', 'converter', 1,
   [R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
    R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('io', 'USB', 'USB-A', 2, 'USB'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU receiver that decodes and reassembles Dejero transmitter (EnGo, PathWay) streams and outputs SDI/HDMI or IP (NDI, SRT, RTMP). '
   'Models 101, 102 and 104 differ in decode channels. Check: model and SDI output count on your unit.',
   'Dejero WayPoint product page', 'https://www.dejero.com/products/waypoint-receiver/', verified=False, full=True)

# ---------------- Blackmagic Design (discontinued) ----------------
BL = lambda *a, **k: add('bmd-legacy.json', 'bmdl-', 'Blackmagic Design', *a, **k)
BL('ultrastudio-4k', 'UltraStudio 4K', 'UltraStudio 4K Thunderbolt 2 capture / playback (legacy)', 'UltraStudio', 'converter', 1,
   [R('in', '6G-SDI', 'BNC', 1, 'SDI In'), R('out', '6G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
    R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', 'Analog video', 'BNC', 3, 'Component/Composite In'),
    R('out', 'Analog video', 'BNC', 3, 'Component/Composite Out'), R('in', 'Analog audio', 'XLR', 2, 'Analog Audio In'),
    R('out', 'Analog audio', 'XLR', 2, 'Analog Audio Out'), R('io', 'AES/EBU', 'BNC', 2, 'AES I/O'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
    R('io', 'RS-422', 'DB9', 1, 'Deck Control'), R('io', 'Other', 'Thunderbolt 2', 2, 'Thunderbolt'), R('in', 'Power', 'IEC', 1, 'Power')],
   '1RU Thunderbolt 2 capture and playback unit (2013): 6G-SDI, HDMI 4K, analog component/composite, balanced XLR and AES audio, '
   'genlock, RS-422 deck control, front LCD and audio meters. Discontinued; nearest current unit is UltraStudio 4K Extreme 3. '
   'Check: counts are from memory of the rear panel, not from a Blackmagic spec sheet.',
   'Blackmagic support archive', 'https://www.blackmagicdesign.com/support', verified=False, full=True)
BL('smart-videohub-12x12', 'Smart Videohub 12x12', 'Smart Videohub 12x12 6G router (legacy)', 'Videohub', 'router', 1,
   [R('in', '6G-SDI', 'BNC', 12, 'SDI In'), R('out', '6G-SDI', 'BNC', 12, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
    R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-B', 1, 'USB'), R('in', 'Power', 'IEC', 1, 'Power')],
   '1RU 12x12 6G-SDI router with front LCD and spin-knob control, Ethernet and USB set-up, reference input. Replaced by the '
   'Smart Videohub 12G and CleanSwitch 12x12. Check: 6G or 12G version and whether a second (redundant) AC inlet is fitted.',
   'Blackmagic support archive', 'https://www.blackmagicdesign.com/support', verified=False, full=True)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
