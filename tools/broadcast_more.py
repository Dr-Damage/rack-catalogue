#!/usr/bin/env python3
"""Test and measurement, playout servers, camera base stations, rack monitors, intercom interfaces and timing (added 2026-11-14):
  leader.json            Leader and PHABRIX waveform monitors, rasterizers and sync generators.
  telestream-video.json  Telestream (ex-Tektronix video) PRISM, WFM8300 and WVR8300. telestream.json (tools/telestream.py) has the SPG9000/ECO8000.
  harmonic.json          Harmonic Spectrum X media servers.
  ikegami.json, hitachi.json, sony-ccu.json   Camera base stations and CCUs (HDCU-3500/5000/5500 are already in sony.json).
  tvlogic.json, postium.json, marshall.json  Multi-screen rack monitors (category monitor with a screens block).
  riedel-bolero.json     Riedel Bolero NSA-002A network stream adapter (RMK-1002 charger kit is already in riedel.json).
  meinberg.json, brandywine.json             PTP / NTP grandmasters.
Not added: Flanders Scientific and Ikan make desktop monitors with optional rack kits; Simplylive and Vizrt engines run on
off-the-shelf servers; Unity Intercom is software; Cyanview RIO / CI0 are small boxes; Bolin makes PTZ cameras and joysticks.
Specs from each maker's data sheet or dealer listing (each entry's source). 'Check:' marks anything unconfirmed."""
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
REF = [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop')]
PSU = lambda n=1, conn='IEC C14': R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')
DC = lambda label='12V DC': R('in', 'Power', 'XLR4M', 1, label)

# ======================= Leader / PHABRIX =======================
LD = ('Leader digest catalogue 2025', 'https://www.leader.co.jp/uploads/2025/05/ca_digest_e.pdf')
add('leader.json', 'leader-lv5600w', 'Leader', 'LV5600W', 'LV5600W hybrid waveform monitor (12G-SDI / IP)', 'ZEN', 'other', 4,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', '12G-SDI', 'BNC', 4, 'SDI Out'), R('in', 'SFP', 'SFP28', 2, 'IP In (option)'),
     R('in', 'Reference', 'BNC', 1, 'Ext Ref'), R('out', 'HDMI', 'HDMI', 1, 'Monitor Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'),
     R('in', 'Power', 'XLR4M', 1, '12V DC')],
    'Half-rack waveform monitor with 7-inch screen: 4 SDI in, 4 SDI out, 10G / 25G ST 2110 options, HDMI monitor out. Desktop kit '
    'or LR2561 dual rack adapter (two side by side). LV7600W is the rasterizer version without a screen. '
    'Check: rack height, reference and power connectors.', LD[0], 'https://www.leader.co.jp/en/products/broadcast/waveform/lv5600/', verified=False, w=6)
add('leader.json', 'leader-lv5350', 'Leader', 'LV5350', 'LV5350 multi-SDI waveform monitor, 3U half rack', 'LV5300', 'other', 3,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'),
     R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('in', 'Power', 'XLR4M', 1, '10-18V DC')],
    'Half-rack 3U waveform monitor with screen, 2 SDI in (eye on ch 1 on the LV5300A), 2 SDI out or ch 2 monitor out, DC 10-18 V. '
    'Check: reference and power connectors.', LD[0], 'https://www.leader.co.jp/', verified=False, w=6)
add('leader.json', 'leader-lt4670', 'Leader', 'LT4670', 'LT4670 hybrid sync generator (SDI / IP / PTP), 1U', 'SPG', 'other', 1,
    [R('out', 'Reference', 'BNC', 6, 'BB / Tri-level'), R('out', '12G-SDI', 'BNC', 4, 'SDI Out (option)'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
     R('io', 'SFP', 'SFP', 2, 'PTP / IP (option)'), R('in', 'RF', 'BNC', 1, 'GNSS (option)'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), PSU(2)],
    'Sync generator: 6 analogue black burst / tri-level outputs, options for 3G or 12G SDI test signals, 25G IP test signals, PTP '
    'grandmaster and GNSS lock, hot-swap redundant AC. 482 x 44 x 400 mm. Check: LTC, word clock and alarm connectors.',
    LD[0], 'https://www.leader.co.jp/', verified=False, full=True)
add('leader.json', 'phabrix-qxl', 'PHABRIX', 'PHQXL', 'QxL 25G IP / 12G-SDI rasterizer, 1U half rack', 'Qx', 'other', 1,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Gen/Thru Out'), R('in', '12G-SDI', 'BNC', 1, 'SDI Eye In'),
     R('io', 'SFP', 'SFP28', 2, '25GE IP'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'), R('out', 'HDMI', 'HDMI', 1, 'Instrument Out'),
     R('out', '12G-SDI', 'BNC', 1, 'Instrument SDI Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('in', 'Power', 'XLR4M', 1, '10-18V DC')],
    'Half-rack 1U ST 2110 / 2022-6 rasterizer, generator and analyser with 12G-SDI options, 2 x 25G SFP28, HDMI and SDI instrument '
    'outputs. 253 x 211 mm. Qx is the 10G version; QxP is the 3U portable with a 7-inch touchscreen. Check: SDI connector counts.',
    LD[0], 'https://www.leader.co.jp/en/products/broadcast/rasterizer/qxl/', verified=False, w=6)

# ======================= Telestream (ex-Tektronix video) =======================
TP = ('Telestream PRISM product sheet (2025)', 'https://www.telestream.com/prism/')
add('telestream-video.json', 'telestream-prism-mpp-200', 'Telestream', 'MPP-200', 'PRISM MPP-200 IP/SDI waveform rasterizer, 1U', 'PRISM', 'other', 1,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', '12G-SDI', 'BNC', 4, 'SDI Loop'), R('io', 'SFP', 'SFP+', 2, '10/25GE IP'),
     R('out', 'DisplayPort', 'DisplayPort', 2, 'Display'), R('out', 'Analog audio', 'DB25', 1, 'Analog Audio Out (8 ch)'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Out'), R('out', '12G-SDI', 'BNC', 1, 'AUX Out'),
     R('out', 'Analog audio', '3.5mm TRS', 1, 'Line Out'), R('io', 'GPIO', 'DB15', 1, 'GPIO'), R('io', 'USB', 'USB-A', 2, 'USB'),
     R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), F('io', 'USB', 'USB-A', 2, 'USB'), F('io', 'USB', 'USB-C', 1, 'USB-C'), PSU()],
    'Rasterizer for post and remote work: 4 SDI in with loop-through, AUX SDI out, ref in and out, 2 SFP+ (25GE by licence), two DisplayPort outputs for an external '
    'display, 8-channel analogue audio out on D-sub, GPIO. 313 mm deep, about 3.5 kg, 160 W max. MPP-100 is SDI only; MPP-300 adds eye/jitter. '
    'Panels checked against a Telestream photo.', TP[0] + '; panels from a Telestream photo', TP[1], powerW=160, weightKg=3.5)
add('telestream-video.json', 'telestream-prism-mpd-200', 'Telestream', 'MPD-200', 'PRISM MPD-200 dual-screen waveform monitor, 3U', 'PRISM', 'other', 3,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'AUX SDI Out'), R('io', 'SFP', 'SFP+', 2, '10/25GE IP'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), PSU()],
    'Full-width 3U with two 9-inch touchscreens: 4 SDI in, 2 x 10/25G IP. MPS-200 is the half-rack single-screen version. '
    'Check: connector counts.', TP[0], TP[1], verified=False)
add('telestream-video.json', 'tektronix-wvr8300', 'Tektronix', 'WVR8300', 'WVR8300 3G/HD/SD waveform rasterizer, 1U', 'WVR8000', 'other', 1,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In A/B'), R('out', '3G-SDI', 'BNC', 2, 'SDI Loop'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
     R('out', 'DVI', 'DVI-I', 1, 'XGA/DVI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
     R('io', 'GPIO', 'DB15', 1, 'Remote/GPI'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), PSU()],
    'Legacy 1RU rasterizer (now Telestream) for 3G/HD/SD-SDI with 4K quad-link support. WFM8300 is the 3U half-rack version with '
    'its own screen. Check: all counts (from memory of the Tektronix data sheet).', 'Tektronix WVR8300 listings',
    'https://www.adorama.com/tkwvr8300.html', verified=False)

# ======================= Harmonic =======================
HM = ('Harmonic Spectrum X data sheet', 'https://www.harmonicinc.com/video-streaming/media-servers-storage/spectrum-x/')
for ru, d, typ, mx in ((1, 77.3, 550, 800), (2, 73.0, 725, 950)):
    add('harmonic.json', f'harmonic-spectrum-x-{ru}ru', 'Harmonic', f'Spectrum X {ru}RU', f'Spectrum X media server / playout, {ru}RU', 'Spectrum X', 'recorder', ru,
        [R('in', '3G-SDI', 'BNC', 8, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
         R('io', 'Other', 'DB25', 1, 'LTC / RS-422 / AES / GPIO'), R('io', 'Ethernet', 'RJ45' if ru == 2 else 'SFP+', 4, 'Control / file'),
         R('io', 'SFP', 'SFP+', 2, '10GE NDI / MediaGrid (option)')] + ([R('io', 'SFP', 'SFP28', 2, '25GE ST 2110 (option)')] if ru == 2 else []) + [PSU(2)],
        f'Integrated playout server with storage ({4 if ru == 1 else 8} drives), up to 8 HD or 2 UHD channels with simulcast outputs, '
        f'analogue black or PTP reference. {d} cm deep, {typ} W typical / {mx} W max, dual hot-swap PSUs. Spectrum X Plus (2026) doubles '
        'channel density. Check: SDI connector counts and the multi-pin connector.', HM[0], HM[1], verified=False, full=True, powerW=mx)

# ======================= Camera base stations / CCUs =======================
LEMO = R('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'Camera')
add('ikegami.json', 'ikegami-bsx-100', 'Ikegami', 'BSX-100', 'BSX-100 3G fibre base station, 3U half rack', 'BSX', 'converter', 3,
    [LEMO, R('out', '12G-SDI', 'BNC', 2, '12G-SDI Out'), R('out', 'HD-SDI', 'BNC', 8, 'HD-SDI Out'), R('in', 'HD-SDI', 'BNC', 4, 'Return In'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Out'), R('io', 'Intercom', 'Other', 1, 'Comms multi-pin'),
     R('io', 'Other', 'Other', 1, 'Remote control'), PSU()],
    'Half-rack 3U base station for HDK-99 and HDK-73 cameras over SMPTE hybrid fibre. Talkback on the front. '
    'Check: power inlet and intercom / remote connectors.', 'SVG: Ikegami develops BSX-100',
    'https://www.sportsvideo.org/2020/06/15/ikegami-develops-bsx-100-3g-fiber-base-station/', verified=False, w=6, full=True)
add('hitachi.json', 'hitachi-cu-hd1300', 'Hitachi Kokusai', 'CU-HD1300', 'CU-HD1300 4K/HD camera control unit', 'CU-HD1300', 'converter', 2,
    [LEMO, R('out', '12G-SDI', 'BNC', 2, '12G-SDI Out'), R('out', '3G-SDI', 'BNC', 6, '3G-SDI Out'), R('in', '3G-SDI', 'BNC', 3, 'Return In'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Intercom', 'Other', 1, 'Intercom'), R('io', 'Other', 'Other', 1, 'RCP'), PSU()],
    'CCU for SK-UHD and SK-HD cameras with 12G-SDI UHD outputs. CU-HD1300F-S1 is a fibre-adapter version. '
    'Check: rack size and all connector counts (from memory).', 'Hitachi Kokusai CU-HD1300 product information', 'https://www.hitachi-kokusai.co.jp/global/en/products/broadcast/', verified=False, full=True)
add('sony-ccu.json', 'sony-hdcu-3100', 'Sony', 'HDCU-3100', 'HDCU-3100 camera control unit, half rack', 'HDCU', 'converter', 2,
    [LEMO, R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('in', '3G-SDI', 'BNC', 2, 'Return In'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
     R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('io', 'Intercom', 'XLR', 1, 'Intercom'), R('io', 'Other', 'Other', 1, 'RCP'),
     R('io', 'Ethernet', 'RJ45', 1, 'LAN'), PSU()],
    'Compact CCU for HDC-3100 / HDC-3500 cameras (HD, with 4K upgrade on some versions). Check: rack size and all connector counts (from memory).',
    'Sony HDCU-3100 product information', 'https://pro.sony/', verified=False, w=6, full=True)

# ======================= Rack monitors =======================
def mon(file, id, mfr, pn, name, fam, ru, n, size, ports, notes, src, url, verified=True, aspect='16:9', **k):
    add(file, id, mfr, pn, name, fam, 'monitor', ru, ports, notes, src, url, verified, screens=dict(count=n, sizeIn=size, aspect=aspect), **k)
TV = ('TVLogic 2016 product line-up brochure', 'https://bpm-media.imgbolt.de/media/pdf/f9/a5/16/EN_TVlogic_2016_Product_LineUp_Broschure.pdf')
TVDC = R('in', 'Power', 'XLR4M', 1, '12V DC')
mon('tvlogic.json', 'tvlogic-rkm-270a', 'TVLogic', 'RKM-270A', 'RKM-270A dual 7-inch rack monitor, 3RU', 'RKM', 3, 2, 7,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In A/B'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('in', 'Analog video', 'BNC', 2, 'CVBS In'),
     R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('io', 'GPI', 'RJ45', 2, 'Remote (tally/GPI)'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet In/Out'),
     R('io', 'RS-422', 'RJ45', 2, 'RS-422 In/Out'), R('io', 'USB', 'USB-A', 1, 'Firmware'), TVDC],
    'Two 7-inch 1024 x 600 screens, each with 2 SDI in, HDMI, composite, a selected SDI out and a remote (tally/GPI) port, UMD and tally. '
    'Ethernet and RS-422 in/out for daisy-chaining, DC 12 V on XLR4. 60 W. Rear checked against the TVLogic drawing.', TV[0] + '; rear from tvlogic.tv', TV[1], aspect='16:10', powerW=60)
mon('tvlogic.json', 'tvlogic-rkm-290a', 'TVLogic', 'RKM-290A', 'RKM-290A dual 9-inch Full HD rack monitor, 4RU', 'RKM', 4, 2, 9,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In A/B'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'),
     R('io', 'GPI', 'RJ45', 1, 'Tally/GPI'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), TVDC],
    'Two 9-inch 1920 x 1080 screens, each with 2 SDI in, HDMI and a selected SDI out. DC 12/24 V, 60 W. Check: tally/LAN connectors.',
    TV[0], TV[1], verified=False, powerW=60)
mon('tvlogic.json', 'tvlogic-rkm-443a', 'TVLogic', 'RKM-443A', 'RKM-443A quad 4.3-inch rack monitor, 2RU', 'RKM', 2, 4, 4.3,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('in', 'Analog video', 'BNC', 4, 'CVBS In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'),
     R('io', 'GPI', 'RJ45', 1, 'Tally/GPI'), TVDC],
    'Four 4.3-inch 800 x 480 screens, each with SDI and composite in and SDI out. DC 12 V, 60 W.', TV[0], TV[1], verified=False, aspect='5:3', powerW=60)
mon('tvlogic.json', 'tvlogic-r-5t', 'TVLogic', 'R-5T', 'R-5T triple 5.5-inch 12G rack monitor, 2RU', 'R series', 2, 3, 5.5,
    [R('in', '12G-SDI', 'BNC', 3, '12G-SDI In'), R('in', '3G-SDI', 'BNC', 3, '3G-SDI In'), R('in', 'HDMI', 'HDMI', 3, 'HDMI In'),
     R('out', '12G-SDI', 'BNC', 3, '12G-SDI Out'), R('out', '3G-SDI', 'BNC', 3, '3G-SDI Out'), R('io', 'RS-422', 'RJ45', 2, 'RS-422'), TVDC],
    'Three 5.5-inch Full HD screens, each with 12G and 3G SDI in/out and HDMI, UMD, RS-422 and Observer network control. '
    'DC 12 V, 35 W, 480 x 87.5 x 119 mm, 2.86 kg. Replaces the RKM-535A. Check: whether the I/O counts are per screen.',
    'Adorama TVLogic R-5T listing', 'https://www.adorama.com/tv-logic-r-5t-3x-5-inch-lcd-rack-monitor-12g-sdi/p/tvr5t', verified=False, powerW=35, weightKg=2.86)
mon('postium.json', 'postium-prm-434', 'Postium', 'PRM-434', 'PRM-434 quad 4.3-inch rack monitor, 2RU', 'PRM', 2, 4, 4.3,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('in', 'Analog video', 'BNC', 4, 'CVBS In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'),
     R('in', 'GPI', 'Other', 4, 'GPI'), R('io', 'RS-422', 'RJ45', 2, 'RS-422 In/Out'), R('io', 'USB', 'USB-B', 1, 'USB'), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Four 4.3-inch 800 x 480 screens, each with 3G-SDI and composite in and SDI out, three-colour tally, GPI per screen. '
    'DC 12 V, 32 W, 480 x 86.5 x 50 mm, 1.94 kg. Check: whether the I/O is per screen.', 'Markertek Postium PRM-434 listing',
    'https://www.markertek.com/product/post-prm-434/postium-prm-434-4-3-in-multi-format-quad-lcd-rack-monitor-with-3g-sdi',
    verified=False, aspect='5:3', powerW=32, weightKg=1.94)
mon('marshall.json', 'marshall-v-r173-imd-3gte', 'Marshall Electronics', 'V-R173-IMD-3GTE', 'V-R173-IMD-3GTE 17.3-inch rack monitor, 6RU', 'V-R', 6, 1, 17.3,
    [R('in', '3G-SDI', 'BNC', 1, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 1, '3G-SDI Loop'), R('io', 'GPI', 'Other', 1, 'Tally/GPI'),
     R('io', 'RS-422', 'RJ45', 2, 'RS-485/422 In/Loop'), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Single 17.3-inch 1920 x 1080 rack monitor with 3G-SDI and loop, IMD (UMD), tally and RS-422. 12 V DC 60 W on a 2-pin twist lock. '
    '476 x 265 mm, 3.7 kg. Check: tally connector.', 'Marshall V-R173-IMD-3GTE spec sheet', 'https://www.marshall-usa.com/specsheets/V-R173-IMD-3GTE.pdf',
    verified=False, powerW=60, weightKg=3.7)
mon('marshall.json', 'marshall-v-r653-imd-3gte', 'Marshall Electronics', 'V-R653-IMD-3GTE', 'V-R653-IMD-3GTE triple 6.5-inch rack monitor, 3RU', 'V-R', 3, 3, 6.5,
    [R('in', '3G-SDI', 'BNC', 3, '3G-SDI In'), R('out', '3G-SDI', 'BNC', 3, '3G-SDI Loop'), R('io', 'RS-422', 'RJ45', 2, 'RS-422'), R('in', 'Power', 'DC locking', 1, '12V DC')],
    'Three 6.5-inch screens, each with 3G-SDI in and loop, IMD and RS-422 control. Check: tally and power connectors.',
    'Marshall LCD racks products guide', 'https://www.fullcompass.com/common/files/25931-MarshallLCDRacksProductsGuide.pdf', verified=False, aspect='4:3')

# ======================= Riedel Bolero =======================
add('riedel-bolero.json', 'riedel-nsa-002a', 'Riedel', 'NSA-002A', 'NSA-002A network stream adapter (Bolero / AES67), half rack 1U', 'Bolero', 'audio', 1,
    [R('io', 'Analog audio', 'RJ45', 6, '4-wire'), R('in', 'GPI', 'Other', 1, 'GPI 1-3'), R('out', 'GPI', 'Other', 1, 'GPO 1-3'),
     R('io', 'Dante/AES67', 'RJ45', 2, 'AES67 Network'), R('in', 'Power', 'DC locking', 1, 'DC In')],
    'Half-rack 1U AES67 throwdown box: 6 analogue 4-wire ports and 3 GPI / 3 GPO for Bolero Standalone Link and Standalone 2110. '
    'RMK-001 rack kit holds one or two. Antennas sit on the network and are not rack gear. Check: 4-wire, GPIO and power connectors.',
    'Riedel Bolero product page', 'https://www.riedel.net/en/products-solutions/intercom/bolero-wireless-intercom-1', verified=False, w=6)

# ======================= Timing =======================
add('meinberg.json', 'meinberg-lantime-m1000', 'Meinberg', 'LANTIME M1000', 'LANTIME M1000 modular time server / PTP grandmaster, 1U', 'IMS LANTIME', 'other', 1,
    [R('in', 'RF', 'BNC', 1, 'GNSS Antenna'), R('io', 'RS-232', 'DB9', 1, 'GNSS COM'), R('io', 'Ethernet', 'RJ45', 1, 'CPU LAN / NTP'), R('io', 'RS-232', 'DB9', 1, 'CPU Terminal'),
     R('io', 'USB', 'USB-A', 1, 'CPU USB'), R('io', 'SFP', 'SFP', 1, 'PTP SFP'), R('io', 'Ethernet', 'RJ45', 1, 'PTP'),
     R('io', 'Ethernet', 'RJ45', 2, 'I/O LAN'), R('out', 'Reference', 'BNC', 2, '10 MHz / PPS'), R('in', 'Power', 'Terminal block', 2, 'PSU A/B'),
     F('io', 'RS-232', 'DB9', 1, 'Terminal'), F('io', 'USB', 'USB-A', 1, 'USB')],
    'IMS modular chassis: up to 2 reference clocks (GPS/GNSS, PZF), 2 hot-swap PSUs (AC/DC mixable, 50 W each), CPU, and 4 I/O slots '
    '(PTP / NTP, pulse, frequency and time-code outputs, up to 4 PTP modules, up to 16 extra ports with LNE). 483 x 290 mm. '
    'Ports follow the fit-out in Meinberg\'s rear photo (CPU, GNSS receiver, I/O module, PTP module, two AC PSUs). Check: modules fitted.', 'Meinberg LANTIME M1000 short info; panels from Meinberg product photos',
    'https://www.meinbergglobal.com/download/docs/shortinfo/english/info_ims-lantime-m1000.pdf', verified=False, powerW=100)
add('meinberg.json', 'meinberg-lantime-m3000-broadcast', 'Meinberg', 'LANTIME M3000 (broadcast)', 'LANTIME M3000 broadcast sync platform, 3U', 'IMS LANTIME', 'other', 3,
    [R('in', 'RF', 'BNC', 1, 'GPS Antenna'), R('in', 'RF', 'SMA', 1, 'GNSS L1 Antenna'), R('out', 'Reference', 'BNC', 8, 'Video Sync (BB/Tri)'),
     R('out', 'AES/EBU', 'BNC', 1, 'DARS'), R('out', 'Reference', 'BNC', 4, 'Word Clock'), R('out', 'Reference', 'BNC', 4, '10 MHz'),
     R('io', 'Ethernet', 'RJ45', 3, 'PTP / SyncE'), R('io', 'Ethernet', 'RJ45', 4, 'LNE GbE'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'),
     R('io', 'RS-232', 'DB9', 1, 'Time string'), R('in', 'Power', 'Other', 2, 'Power A/B (5-pin DFK)')],
    '3U IMS chassis in the broadcast build: redundant GNSS receivers and PSUs, HPS-100 PTP/NTP (ST 2059-2), VSG video sync module '
    '(8 black burst / tri-level), SCG-U studio clock (word clock), LNO 10 MHz. 483 x 132 x 270 mm. Check: modules fitted.',
    'Meinberg M3000 broadcast configuration sheet', 'https://www.meinbergglobal.com/download/docs/other/M3000-Broadcast.pdf', verified=False)
add('brandywine.json', 'brandywine-ptp-800', 'Brandywine Communications', 'PTP-800', 'PTP-800 IEEE 1588 grandmaster clock, 1U', 'PTP', 'other', 1,
    [R('io', 'Ethernet', 'RJ45', 4, 'PTP/NTP (RJ45/SFP combo)'), R('in', 'RF', 'BNC', 1, 'GNSS Antenna'), R('in', 'Reference', 'BNC', 1, '10 MHz In'),
     R('out', 'Reference', 'BNC', 1, '10 MHz Out'), R('in', 'Reference', 'BNC', 1, '1PPS In'), R('out', 'Reference', 'BNC', 1, '1PPS Out'),
     R('in', 'Timecode', 'BNC', 1, 'IRIG-B In'), R('out', 'Timecode', 'BNC', 1, 'IRIG-B Out'), F('io', 'USB', 'USB micro-B', 1, 'USB'), PSU(2)],
    'Four independent PTP grandmaster ports (RJ45/SFP combo), NTP stratum 1, GNSS, 10 MHz, 1PPS and IRIG-B in and out, dual hot-swap '
    'PSUs (AC or DC). 200 mm deep, 4.5 kg, 20 W typical. No black burst or tri-level outputs.', 'Brandywine PTP-800 data sheet',
    'https://www.brandywinecomm.com/wp-content/uploads/2022/04/PTP800-BWC.pdf', powerW=20, weightKg=4.5)

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
