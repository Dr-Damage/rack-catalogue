#!/usr/bin/env python3
"""Generates catalogue/aja.json, decimator.json, lawo.json, datavideo.json (standalone rack gear only;
card frames and frame cards belong to the card frames thread's files)."""
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

# ---------------- AJA ----------------
A = lambda *a, **k: add('aja.json', 'aja-', 'AJA Video Systems', *a, **k)
for n, ru, w in [(16, 1, 16), (32, 2, 20), (64, 4, 50)]:
    A(f'kumo-{n}{n}-12g', f'KUMO {n}{n}-12G', f'KUMO {n}{n}-12G router', 'KUMO', 'router', ru,
      [R('in', '12G-SDI', 'BNC', n, 'SDI In'), R('out', '12G-SDI', 'BNC', n, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref'),
       R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'DB9', 1, 'RS-422'),
       R('io', 'USB', 'Mini-USB', 1, 'USB'), R('in', 'Power', '4-pin Molex', 2, '12V DC')],
      f'{ru}RU {n}x{n} 12G-SDI router, 39 mm deep. Looping non-terminating reference (black burst or tri-level), gigabit Ethernet, '
      f'RS-422 DB9, Mini-USB for eMini-Setup. Dual redundant 10-14V DC inputs (4-pin Molex), {w} W typical; one AC adapter included, '
      'second sold separately. Same hardware as the Grass Valley Sirius compact routers.',
      f'AJA KUMO {n}{n}-12G spec sheet', f'https://www.aja.com/products/kumo-{n}{n}-12g')
for code, url in [('FS4', 'https://www.aja.com/products/fs4'), ('FS-HDR', 'https://www.aja.com/products/fs-hdr')]:
    ports = [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'),
             R('in', '12G-SDI', 'SFP', 4, '12G In (SFP)'), R('out', '12G-SDI', 'SFP', 4, '12G Out (SFP)'), R('out', '3G-SDI', 'BNC', 1, 'Monitor Out')]
    if code == 'FS4': ports.append(R('out', 'HDMI', 'HDMI', 1, 'HDMI Monitor'))
    ports += [R('in', 'Reference', 'BNC', 1, 'Ref'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('in', 'AES/EBU', 'DB25', 1, 'AES In (8)'),
              R('out', 'AES/EBU', 'DB25', 1, 'AES Out (8)'), R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('in', 'MADI audio', 'ST fibre', 1, 'MADI In Fibre'),
              R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), R('out', 'MADI audio', 'ST fibre', 1, 'MADI Out Fibre'), R('io', 'Other', 'DB25', 1, 'GPI (4/4)'),
              R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Power', 'IEC', 2, 'PSU')]
    A(code.lower(), code, f'{code} frame sync / converter', 'FS', 'converter', 1, ports,
      f'1RU, 444.5 x 406.4 mm deep. 4 x 3G-SDI BNC in/out plus 4 x 12G-SDI in/out on optional SFP modules (fibre or HD-BNC), 3G monitor out'
      + (', HDMI monitor out' if code == 'FS4' else '') + ', 2 looping ref BNC, 8 AES in and out on DB25s, 2 MADI in/out (BNC + ST fibre), '
      'GPI DB25 (4 in, 4 out), gigabit Ethernet, dual redundant AC supplies.' + (' HDR/WCG conversion with Colorfront engine.' if code == 'FS-HDR' else ''),
      f'AJA {code} spec sheet', url, full=True)
A('ki-pro-ultra-12g', 'Ki Pro Ultra 12G', 'Ki Pro Ultra 12G recorder', 'Ki Pro', 'recorder', 2,
  [R('in', '12G-SDI', 'BNC', 1, '12G In'), R('in', '3G-SDI', 'BNC', 3, '3G In'), R('out', '12G-SDI', 'BNC', 1, '12G Out'), R('out', '3G-SDI', 'BNC', 3, '3G Out'),
   R('in', 'SFP', 'SFP', 4, 'Fibre In (opt)'), R('out', 'SFP', 'SFP', 4, 'Fibre Out (opt)'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
   R('io', 'AES/EBU', 'DB25', 1, 'AES (8 ch)'), R('in', AA := 'Analog audio', 'DB25', 1, 'Analog In'), R('out', AA, 'DB25', 1, 'Analog Out'),
   R('out', AA, 'RCA', 2, 'Monitor Out'), F('out', AA, '3.5mm jack', 1, 'Headphones'), R('in', 'Timecode', 'BNC', 1, 'LTC In'), R('out', 'Timecode', 'BNC', 1, 'LTC Out'),
   R('in', 'Reference', 'BNC', 1, 'Ref'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('io', 'RS-422', 'DB9', 1, 'RS-422'),
   R('in', 'Power', 'XLR4', 2, '12-18V DC')],
  'Half rack wide, 2RU, 219 x 269 x 84 mm, 2.6 kg. 4K/UHD/HD recorder with 2 AJA Pak media slots. SDI in/out: 1 x 12G + 3 x 3G BNC, plus optional '
  'fibre/HD-BNC SFPs; HDMI in/out; AES and analog audio on TASCAM DB25s; LTC in/out, looping ref, LAN, RS-422 (Sony 9-pin), dual 4-pin XLR DC '
  '(external AC adapter). Check: which face each connector is on.', 'AJA Ki Pro Ultra 12G spec sheet', 'https://www.aja.com/products/ki-pro-ultra-12g', w=6)

# ---------------- Decimator ----------------
add('decimator.json', 'dec-', 'Decimator Design', 'dmon-16s', 'DMON-16S', 'DMON-16S 16-channel multiviewer', 'DMON', 'monitor', 1,
    [R('in', '3G-SDI', 'BNC', 16, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
     R('io', 'USB', 'USB', 1, 'USB'), R('in', 'Power', 'DC locking', 1, '5-32V DC')],
    'Desktop 16-input 3G/HD/SD multiviewer, 220 x 103.7 x 29.5 mm; sits on a rack shelf (Decimator rack kits hold two). '
    '1 SDI + 1 HDMI out, USB control, locking 5-32V DC inlet.', 'Decimator DMON-16S brochure',
    'https://www.fullcompass.com/common/files/24640-DecimatorDesignDMON16SBrochure.pdf', w=6, boxMm={'w': 220, 'h': 29.5})

# Riedel moved to tools/comms.py (riedel.json, clearcom.json, rts.json)

# ---------------- Lawo ----------------
add('lawo.json', 'lawo-', 'Lawo', 'a-uhd-core', 'A__UHD Core', 'A__UHD Core audio engine', 'A__line', 'audio', 1,
    [R('io', 'Ethernet', 'RJ45', 2, 'Mgmt'), R('io', 'Dante/AES67', 'SFP', 8, 'Media (4 redundant pairs)'), R('io', 'USB', 'USB-A', 1, 'Firmware USB'),
     R('io', 'RS-422', 'Other', 1, 'Serial'), R('in', 'Other', 'BNC', 1, 'WCLK In'), R('out', 'Other', 'BNC', 1, 'WCLK Out'), R('out', 'Other', 'BNC', 1, 'WCLK Thru'),
     R('in', 'Power', 'IEC', 2, 'PSU'), F('io', 'USB', 'USB-A', 1, 'Licence dongle')],
    '1RU, 483 x 379 mm deep, 7.4 kg. IP audio engine (ST 2110-30 / AES67, RAVENNA): 2 redundant 1GbE management ports, 8 x 1GbE SFP streaming '
    'ports in redundant pairs, serial, word clock in/out/thru, service panel (USB-A, DisplayPort, USB-B), 2 hot-swap 220 W PSUs. '
    'Check: front/rear split (inferred from callouts).', 'Lawo A__UHD Core datasheet', 'https://lawo.com/a__uhd-core/', full=True)

# ---------------- Datavideo ----------------
add('datavideo.json', 'dv-', 'Datavideo', 'se-1200mu', 'SE-1200MU', 'SE-1200MU 6-input switcher', 'SE', 'switcher', 1,
    [R('in', 'HD-SDI', 'BNC', 4, 'SDI In'), R('out', 'HD-SDI', 'BNC', 2, 'SDI Out'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
     R('in', 'Analog audio', 'XLR', 2, 'Audio In'), R('out', 'Other', 'DB15', 1, 'Tally'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
     R('io', 'RS-422', 'Other', 1, 'RS-422/232'), R('in', 'Power', 'DC barrel', 1, '12V DC')],
    '1RU mainframe, 440 x 215 x 49 mm, 1.5 kg, rack ears included; controlled by RMC panels or PC over Ethernet. 4 HD-SDI + 2 HDMI in, '
    '2 SDI + 2 HDMI out (assignable), internal genlock, 2 balanced XLR audio in, dual-colour tally DB15, 12V 19 W adapter. '
    'Check: RS-422/232 connector type.', 'Datavideo SE-1200MU product page', 'https://datavideo.com/us/product/SE-1200MU')

# AJA FS2 (added 2026-11-11, legacy dual-channel frame sync)
A('fs2', 'FS2', 'FS2 dual-channel frame sync / converter (legacy)', 'FS', 'converter', 1,
  [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
   R('in', 'Analog video', 'BNC', 2, 'Analog In'), R('out', 'Analog video', 'BNC', 2, 'Analog Out'),
   R('in', 'Reference', 'BNC', 1, 'Ref'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
   R('io', 'AES/EBU', 'DB25', 2, 'AES I/O'), R('io', 'Analog audio', 'DB25', 2, 'Analog Audio I/O'), R('io', 'Other', 'DB25', 1, 'GPI'),
   R('io', 'RS-422', 'DB9', 2, 'RS-422'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Power', 'IEC', 2, 'PSU')],
  '1RU dual-channel universal frame synchroniser and up/down/cross converter (two independent channels, 3G-SDI, optional fibre SFPs), '
  'dual redundant AC supplies, web control. Discontinued; replaced by FS4. Check: connector counts are from memory of the rear panel, not '
  'from the AJA spec sheet; correct them from your unit.', 'AJA FS2 product page (archived)', 'https://www.aja.com/products/fs2',
  verified=False, full=True)
# AJA BRIDGE LIVE (added 2026-11-11)
for code, n, t, c in [('12G-4', 4, '12G-SDI', 'BNC'), ('3G-8', 8, '3G-SDI', 'DIN 1.0/2.3')]:
    A(f'bridge-live-{code.lower()}', f'BRIDGE LIVE {code}', f'BRIDGE LIVE {code} streaming / transcoding appliance', 'BRIDGE LIVE', 'converter', 1,
      [R('io', t, c, n, 'SDI I/O'), R('io', 'Ethernet', 'RJ45', 2, '10GigE'), R('out', 'DisplayPort', 'DisplayPort', 1, 'Local display'),
       R('io', 'USB', 'USB-A', 2, 'USB'), R('in', 'Power', 'IEC', 2, 'AC In')],
      f'1RU, 436.9 x 429.3 x 43.2 mm, 8.2 kg. {n} SDI ports, each input or output, 2 x 10GigE RJ45, dual redundant 100-240 V PSUs. '
      'Local UI via DisplayPort and USB. Encodes/decodes H.264/HEVC/MPEG-2, SRT, RTMP, HLS, NDI. Check: USB and DisplayPort counts.',
      'AJA BRIDGE LIVE spec sheet', 'https://www.aja.com/products/bridge-live', full=True)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(idx)
