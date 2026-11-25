#!/usr/bin/env python3
"""Generates catalogue/videon.json: Videon LiveEdge edge encoders. Added 2026-11-25.

LiveEdge Node and LiveEdge Max 2 are small fanless desktop encoders; three of each sit in 1RU on Videon's horizontal rack mount
trays (shelves here, with carrier bays, one formFactor per body). EdgeCaster / LiveEdge Rack is a 1RU unit built from three Node
engines. Specs from videonlabs.com tech spec pages and PDFs (each entry's source). Videon publishes I/O lists but no labelled rear
drawing, so which end each connector is on is a best reading of the product photos (front: SD slot and buttons). No weights published."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
M = []
NODE = 'Videon LiveEdge Node'
MAX2 = 'Videon LiveEdge Max 2'
def add(id, pn, name, cat, ru, w, ports, notes, url, source, verified=True, **kw):
    m = dict(id='videon-' + id, manufacturer='Videon', partNumber=pn, name=name, family='LiveEdge', category=cat, ru=ru, widthCols=w,
             fullDepth=False, verified=verified, source=source, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

add('liveedge-node', 'LiveEdge Node', 'LiveEdge Node single channel 4Kp30 edge encoder', 'converter', 1, 4, [
    R('in', 'Power', 'DC barrel', 1, '12V DC In'),
    R('io', 'Ethernet', 'RJ45', 1, 'Ethernet (PoE in)'),
    R('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
    R('in', '3G-SDI', 'BNC', 1, 'SDI In'),
    R('in', 'Analog audio', '3.5mm jack', 1, 'Line In'),
    R('io', 'USB', 'USB-A', 1, 'USB 3.0'),
    F('io', 'Other', 'SD card', 1, 'SD Card'),
], 'Fanless single channel edge encoder (Qualcomm Snapdragon) with Docker container support. Video in: HDMI 1.4a or 3G-SDI '
   '(one channel; up to 8 embedded audio channels on SDI), plus a 3.5 mm line level analog audio in. Encodes H.264/AVC or H.265/HEVC '
   'up to 3840x2160p30; RTMP, SRT, HLS, UDP/RTP, recording to USB 3.0 or SD card (MPEG-TS or MP4, FAT32), FTP upload. '
   'KLV metadata (SMPTE 336M) and SMPTE 2038 ANC from SDI. Network: 1 x 10/100/1000 RJ45. '
   'Power: +12V DC in or IEEE 802.3af PoE, 8 W total. Front: SD card slot and an Action button (start/stop RTMP streaming). '
   '127 x 38 x 107.5 mm (5.0 x 1.5 x 4.234 in, W x H x D read from Videon\'s figures), weight not published. No SDI or HDMI out. '
   'Three fit in 1RU on the Videon Horizontal Rack Mount Tray. Check: which end each connector is on and the DC jack type.',
    'https://www.videonlabs.com/liveedge-node', 'Videon LiveEdge Node tech specs (videonlabs.com/node-tech-specs and Tech Specs PDF)',
    formFactor=NODE, boxMm=dict(w=127, h=38), depthMm=108, powerW=8)

add('liveedge-max-2', 'LiveEdge Max 2', 'LiveEdge Max 2 dual 12G-SDI 4Kp60 edge encoder', 'converter', 1, 4, [
    R('in', 'Power', 'DC barrel', 2, '12V DC In'),
    R('io', 'Ethernet', 'RJ45', 2, 'Ethernet 2.5G'),
    R('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'),
    R('in', '12G-SDI', 'BNC', 2, 'SDI In'),
    R('in', 'Analog audio', '3.5mm jack', 1, 'Line In'),
    R('io', 'USB', 'USB-A', 1, 'USB 3.0'),
    F('io', 'Other', 'SD card', 1, 'SD Card'),
], 'Edge encoder with an 8 core CPU (2.5x the compute of LiveEdge Node, 20x for AI/ML). Video in: 2 x 12G-SDI (4Kp60 each, used as '
   'two channels, a backup feed or a loop-through depending on licence) and 1 x HDMI 2.0, up to 16 embedded audio channels, plus a '
   '3.5 mm line level analog audio in. Recording to USB 3.0 or SD card. Network: dual 1000/2500 Mb/s RJ45. Dual power: +12V DC '
   '(10-15V, 25 W max) and IEEE 802.3af/PoE+. Front: 2.35 inch LCD and 3 buttons. 145 x 43 x 170 mm (5.7 x 1.7 x 6.7 in, W x H x D '
   'read from Videon\'s figures), weight not published. Videon says output types and counts depend on licensing; no SDI out is listed. '
   'Three fit in 1RU on the Videon Horizontal Short Rack Mount Tray. Check: whether the two power inputs are two DC jacks, and connector ends.',
    'https://www.videonlabs.com/liveedge-max', 'Videon LiveEdge Max 2 Tech Specs PDF and product page',
    formFactor=MAX2, boxMm=dict(w=145, h=43), depthMm=170, powerW=25)

add('node-rack-tray', 'LiveEdge Node rack tray', 'Horizontal Rack Mount Tray (19 in, 1RU) for 3 LiveEdge Node', 'shelf', 1, 12, [],
    '1RU 19 inch horizontal tray that holds up to three LiveEdge Node units side by side. Add each Node as its own device. '
    'Videon publishes no part number for it.', 'https://www.videonlabs.com/liveedge-node', 'Videon LiveEdge Node product page',
    carrier=dict(bays=3, fits=[NODE]))
add('max-2-rack-tray', 'LiveEdge Max 2 short rack tray', 'Horizontal Short Rack Mount Tray (19 in, 1RU) for 3 LiveEdge Max 2', 'shelf', 1, 12, [],
    '1RU 19 inch short horizontal tray that holds up to three LiveEdge Max 2 units side by side. Add each Max 2 as its own device. '
    'Videon publishes no part number for it.', 'https://www.videonlabs.com/liveedge-max', 'Videon LiveEdge Max 2 product page',
    carrier=dict(bays=3, fits=[MAX2]))

RACK_NOTES = ('1RU, 3 channel edge encoder built from three LiveEdge Node engines (sold as EdgeCaster Rack / LiveEdge Rack). '
    '3 x 3G-SDI in, 3 channels of 1080p60, 3 x Ethernet uplinks, 3 x 110/220 VAC inputs (one per engine), about 30 W max for the whole '
    'unit. 19 x 5.95 in (480 x 151 mm deep); weight not published. Bundles: VCS-ECRACK-3I (base, ready for custom options), '
    'VCS-ECRACK-3IS (+ LiveEdge Stream), VCS-ECRACK-3AI (fully loaded: Stream, Advanced and Run). Check: the overview PDF text is garbled, '
    'so confirm the power inlet type and count and any HDMI or USB ports.')
for pn, lic in [('VCS-ECRACK-3I', 'base'), ('VCS-ECRACK-3IS', 'with LiveEdge Stream'), ('VCS-ECRACK-3AI', 'fully loaded')]:
    add('edgecaster-rack-' + pn[-3:].lower().lstrip('-'), pn, f'EdgeCaster Rack 3 channel 1RU encoder ({lic})', 'converter', 1, 12, [
        R('in', 'Power', 'IEC C14', 3, 'AC In'),
        R('io', 'Ethernet', 'RJ45', 3, 'Ethernet'),
        R('in', '3G-SDI', 'BNC', 3, 'SDI In'),
    ], RACK_NOTES, 'https://www.videonlabs.com/liveedge-rack', 'Videon EdgeCaster Rack Product Overview PDF and LiveEdge Rack page',
        verified=False, depthMm=151, powerW=30)

json.dump(M, open(os.path.join(CAT, 'videon.json'), 'w'), indent=1)
idx = os.path.join(CAT, 'index.json'); L = json.load(open(idx))
if 'videon.json' not in L: L.append('videon.json'); json.dump(L, open(idx, 'w'))
print(len(M), [m['id'] for m in M])
