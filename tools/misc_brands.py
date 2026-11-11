#!/usr/bin/env python3
"""Generates catalogue files for brands first met on site drawings (added 2026-11-11 for the CAR rack import):
evertz.json (standalone Evertz units; frames and cards stay in evertz-frames.json), omnitronics.json, drawmer.json, hpe.json and bmd-legacy.json (discontinued Blackmagic units; ids use `bmdl-` because `bmd-` is reserved
for the app's built-in Blackmagic catalogue). Avid, Synology, Tieline and Dejero moved to media_brands.py (full ranges). verified=False and a 'Check:' note mark anything not confirmed from a maker's document."""
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

# ---------------- HPE ----------------
HP = lambda *a, **k: add('hpe.json', 'hpe-', 'HPE', *a, **k)
HP('dl360p-gen8', 'ProLiant DL360p Gen8', 'ProLiant DL360p Gen8 1U server (legacy)', 'ProLiant', 'computer', 1,
   [R('out', 'Other', 'VGA', 1, 'VGA'), R('io', 'Other', 'DB9', 1, 'Serial'), R('io', 'USB', 'USB-A', 4, 'USB 2.0'),
    R('io', 'Ethernet', 'RJ45', 4, '1GbE FlexibleLOM'), R('io', 'Ethernet', 'RJ45', 1, 'iLO 4'), R('io', 'Other', 'Card slot', 2, 'PCIe slot'),
    R('in', 'Power', 'IEC C14', 2, 'PSU')],
   '1U two-socket Xeon E5-2600 / v2 server (2012-2015), 4-port 1GbE FlexibleLOM (or 2 x 10GbE), dedicated iLO 4, 2 PCIe slots, '
   'redundant Flex Slot PSUs. Check: FlexibleLOM fitted and PCIe cards.',
   'HPE QuickSpecs DL360p Gen8', 'https://www.hpe.com/psnow/doc/c04123079', verified=False, full=True)

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

# ---------------- Omnitronics ----------------
OM = lambda *a, **k: add('omnitronics.json', 'omnitronics-', 'Omnitronics', *a, **k)
OM('ipr100', 'IPR100', 'IPR100 radio-over-IP gateway (1 channel, desktop)', 'RoIP gateway', 'audio', 1,
   [R('io', 'Analog audio', 'DB15', 1, 'Radio (4-wire E&M)'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-232', 'DB9', 1, 'Serial'),
    R('in', 'Power', '12V DC', 1, 'DC In'), F('io', 'Analog audio', 'RJ11', 1, 'Handset')],
   'Desktop gateway that links one analog two-way radio (or a 4-wire E&M line) to IP: RTP unicast/multicast and SIP, '
   '12 VoIP channels, DTMF / CTCSS / Selcall signalling, serial data pass-through and serial channel change, web set-up, '
   '12 V DC plug-pack. Front: status LEDs and a handset jack (Omnitronics 960 handsets). Sits on a rack shelf; superseded by the IPR110+. '
   'Check: rear connector types (radio port, serial) and the width (estimated at about 270 mm from the maker photo); the maker\'s '
   'manual is behind a customer login.',
   'Omnitronics RoIP/VoIP connectivity pages', 'https://www.omnitronicsworld.com/voip-connectivity/', verified=False, w=7)

# ---------------- Drawmer ----------------
DM = lambda *a, **k: add('drawmer.json', 'drawmer-', 'Drawmer', *a, **k)
DM('dl241', 'DL241', 'DL241 dual auto compressor / expander / limiter', 'Pro Series', 'audio', 1,
   [R('out', 'Analog audio', 'XLR3M', 1, 'Ch 2 Output'), R('in', 'Analog audio', 'XLR3F', 1, 'Ch 2 Input'),
    R('out', 'Analog audio', 'XLR3M', 1, 'Ch 1 Output'), R('in', 'Analog audio', 'XLR3F', 1, 'Ch 1 Input'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU, 482 x 44 x 200 mm deep, 3.2 kg, 9 VA (115/230 V selector, fused IEC inlet). Two channels of auto compressor, expander/gate and '
   'peak limiter with gain reduction and output meters, stereo link, hard-wire bypass per channel, rear +4 dBu / -10 dBV switch per '
   'channel. Balanced I/O. Also built with 6.3 mm jack I/O instead of XLR: check which version you have.',
   'Drawmer DL241 product page and operator manual', 'https://www.drawmer.com/products/pro-series/dl241.php', w=12)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
