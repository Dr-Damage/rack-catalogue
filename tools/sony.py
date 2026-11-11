#!/usr/bin/env python3
"""Generates catalogue/sony.json (Sony Professional rack-mount broadcast products) from pro.sony spec pages."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'sony.json')
M = []
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=True, **kw):
    m = dict(id='sony-' + id, manufacturer='Sony', partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

add('xvs-g1', 'XVS-G1', 'XVS-G1 switcher processor', 'XVS', 'switcher', 4,
    [R('in', '12G-SDI', 'BNC', 44, 'SDI In'), R('out', '12G-SDI', 'BNC', 24, 'SDI Out'),
     R('in', 'Reference', 'BNC', 2, 'Ref In'), R('out', 'Reference', 'BNC', 2, 'Ref Loop'), R('out', 'Reference', 'BNC', 1, 'Ref Out'),
     R('io', 'Other', 'DB25', 1, 'GPI'), R('io', 'Other', 'DB25', 2, 'Tally/GPI (opt)'), R('io', 'RS-422', 'RJ45', 4, 'RS-422 x2 (opt)'),
     R('io', 'Ethernet', 'RJ45', 2, 'LAN'), R('io', 'USB', 'USB-A', 4, 'USB (maint)'), R('in', 'Power', 'IEC', 2, 'AC In')],
    '4RU, 440 x 176 x 583 mm, 22 kg fully optioned. 44 primary inputs and 24 outputs with all XKS-G1110 boards (1.5G/3G/12G), '
    'two HD multiviewers standard. Ref in x2 with loop, ref out. GPI DB25 (16 out, 6 in); optional Tally/GPI DB25 x2 (32 out, 12 in); '
    'optional RS-422 x8 on 4 RJ45 via breakout. LAN 1/2 gigabit, built-in redundant PSU. Check: AC inlet count.',
    'Sony XVS-G1 specifications (pro.sony)', 'https://pro.sony/en_DK/products/video-switchers/xvs-g1')
XVS = 'Sony Production Switcher System catalogue 2022 (sony.jp)'
for code, ru, ins, outs, fc, me4, mehd, ins4, outs4 in [('XVS-9000', 15, 160, 80, 0, 5, 5, 80, 40), ('XVS-8000', 10, 160, 48, 16, 5, 5, 40, 12),
                                                        ('XVS-7000', 8, 112, 48, 16, 3, 3, 28, 12), ('XVS-6000', 6, 64, 24, 16, 2, 2, 16, 6)]:
    ports = [R('in', '3G-SDI', 'BNC', ins, 'SDI In'), R('out', '3G-SDI', 'BNC', outs, 'SDI Out')]
    if fc: ports.append(R('out', '3G-SDI', 'BNC', fc, 'FC Out'))
    ports += [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
              R('io', 'Ethernet', 'RJ45', 1, 'MVS LAN'), R('io', 'Ethernet', 'RJ45', 1, 'UTL LAN')]
    if code == 'XVS-9000': ports.append(R('out', 'Other', 'DB25', 1, 'GPI Out (8)'))
    ports.append(R('in', 'Power', 'IEC', 1, 'AC In'))
    add(code.lower(), code, f'{code} switcher processor', 'XVS', 'switcher', ru, ports,
        f'{ru}RU processor. Shown fully loaded in HD: {ins} in, {outs} out' + (f' plus {fc} format-converter outputs' if fc else '') +
        f' (4K: {ins4} in, {outs4} out). {mehd} M/E (split M/E doubles it). I/O comes from 12G-SDI and 100G IP option boards '
        '(XKS-S9112, XKS-C9111), so remove ports you do not fit. Ref in with loop, MVS LAN and UTL LAN. '
        + ('GPI out DB25 (4 relay, 4 open collector). ' if code == 'XVS-9000' else '') +
        'Tally, GPI and RS-422 are on the separate MKS-X7700/X2700 interface units. Check: AC inlet count and SDI board standard (12G boards available).',
        XVS, f'https://pro.sony/ue_US/products/video-switchers/{code.lower()}')

CCU = lambda fibres: [
    R('io', 'Fibre', 'SMPTE 304 fibre', fibres, 'Camera'), R('out', '12G-SDI', 'BNC', 2, 'UHD SDI A/B'), R('io', '12G-SDI', 'BNC', 2, 'UHD SDI C/D'),
    R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('io', '3G-SDI', 'BNC', 4, 'SDI I/O'), R('in', '3G-SDI', 'BNC', 4, 'SDI Ret'),
    R('in', 'Other', 'BNC', 2, 'Prompter'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
    R('io', 'Other', 'DB50', 1, 'Intercom/Tally/IO'), R('io', 'Other', '8-pin multi', 1, 'RCP/CNU'), R('io', 'Other', '12-pin', 1, 'Trunk'),
    R('io', 'Ethernet', 'RJ45', 1, 'LAN-COM'), R('io', 'Ethernet', 'RJ45', 1, 'Network Trunk'),
    R('out', 'Analog audio', 'XLR3M', 2, 'Audio Out'), R('out', 'AES/EBU', 'BNC', 1, 'Character/AES'), R('in', 'Power', 'IEC', 1, 'AC In')]
add('hdcu-3500', 'HDCU-3500', 'HDCU-3500 camera control unit', 'HDCU', 'converter', 3, CCU(1),
    '3RU half-rack width CCU, 6.3 kg. UHD SDI A/B out and C/D I/O on 12G BNC (12G/6G need HZCU-UHD35), 4 SDI out, 4 SDI I/O and 4 return '
    'on 3G BNC, 2 prompter, ref loop, intercom/tally/IO D-sub 50, RCP/CNU 8-pin, trunk 12-pin, LAN-COM, network trunk, 2 XLR audio out, '
    'character/AES BNC. Check: whether LAN-COM and network trunk are RJ45.', 'Sony HDCU-3500 specifications', 'https://pro.sony/en_CZ/products/camera-control-unit/hdcu-3500', w=6)
add('hdcu-5500', 'HDCU-5500', 'HDCU-5500 camera control unit', 'HDCU', 'converter', 3, CCU(1),
    '3RU half-rack width CCU with the same rear I/O as HDCU-3500 plus options: HKCU-SFP50 ST 2110 IP interface, HKCU-SM50 single-mode fibre, '
    'HKCU-REC55 recording. Check: LAN connector types.', 'Sony HDCU-5500 specifications', 'https://pro.sony/es_PT/pdf/hdcu-5500', w=6)
add('hdcu-5000', 'HDCU-5000', 'HDCU-5000 camera control unit', 'HDCU', 'converter', 4, CCU(2),
    'Full 19 in rack-width CCU, 19.5 kg, 2 camera fibre connectors. Same SDI, prompter, ref, intercom and audio I/O as HDCU-3500. '
    'Check: rack height (not stated by Sony) and LAN connector types.', 'Sony HDCU-5000 specifications', 'https://pro.sony/ue_US/pdf/hdcu-5000', verified=False)
add('pws-4500', 'PWS-4500', 'PWS-4500 multi-port server', 'PWS', 'recorder', 4,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out'), R('out', 'HD-SDI', 'BNC', 2, 'Monitor'),
     R('out', 'HD-SDI', 'BNC', 4, 'Input Monitor 5-8'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
     R('in', 'Timecode', 'BNC', 1, 'TC In'), R('out', 'Timecode', 'BNC', 1, 'TC Out'), R('io', 'RS-422', 'RJ45', 4, 'Remote 1/2-7/8'),
     R('io', 'Other', 'DB25', 1, 'GPIO'), R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('io', 'Ethernet', 'SFP', 1, '10G Network (opt)'),
     R('io', 'Ethernet', 'RJ45', 2, 'Share Play 10G'), R('io', 'Ethernet', 'RJ45', 2, 'NMI Monitor'), R('io', 'USB', 'USB-A', 1, 'Maintenance'),
     R('in', 'Power', 'IEC', 2, 'AC In')],
    '4K/HD multi-port AV storage server, 22 kg, 480 W max, redundant power. 4 SDI encoder inputs and 8 decoder outputs (3G), '
    '2 HD monitor outs, 4 input monitor outs, ref loop, TC in/out BNC, 8 remote ports on 4 RJ45, GPIO DB25, 2 x 1G network, '
    'optional SFP+ 10G, 2 x 10G share play. 12G needs PWSK-4508. Check: rack height (assumed 4RU) and AC inlet count.',
    'Sony PWS-4500 specifications', 'https://pro.sony/en_AU/pdf/pws-4500', verified=False)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
# ---- Decks and VTRs (added 2026-11-11) ----
def F(*a): return g('front', *a)
AA = 'Analog audio'
def xdcam_compact(id, pn, name, verified, notes, src, url):
    add(id, pn, name, 'XDCAM', 'recorder', 3,
        [R('in', 'HD-SDI', 'BNC', 1, 'HD/SD-SDI In'), R('out', 'HD-SDI', 'BNC', 2, 'HD-SDI Out'), R('out', 'SD-SDI', 'BNC', 2, 'SD-SDI Out'),
         R('out', 'Other', 'BNC', 2, 'Composite Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
         R('in', 'Timecode', 'BNC', 1, 'TC In'), R('out', 'Timecode', 'BNC', 1, 'TC Out'),
         R('in', AA, 'XLR3F', 2, 'Audio In'), R('out', AA, 'XLR3M', 2, 'Audio Out'), R('out', AA, 'XLR3M', 2, 'Monitor Out'),
         R('in', 'AES/EBU', 'BNC', 2, 'AES In'), R('out', 'AES/EBU', 'BNC', 2, 'AES Out'),
         R('io', 'RS-422', 'DB9F', 1, 'Remote (9-pin)'), R('io', 'Other', 'DB9F', 1, 'Video Control (RS-423)'),
         R('io', 'Other', 'IEEE 1394 6-pin', 1, 'i.LINK'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB', 2, 'USB (maint)'),
         F('out', AA, '6.3mm TRS', 1, 'Headphones'), R('in', 'Power', 'IEC', 1, 'AC In'), R('in', 'Power', 'XLR4M', 1, 'DC In 12V'),
         R('out', 'Power', '4-pin', 1, 'DC Out 12V')],
        'Half-rack desktop deck, 210 x 132 x 396 mm (3RU high, half width), about 6.5 kg, AC 100-240 V or DC 12 V, 80 W. '
        'Rack mount needs a Sony half-rack mount kit (two decks side by side in 3RU). ' + notes, src, url, verified=verified, w=6, full=False)
xdcam_compact('pdw-f1600', 'PDW-F1600', 'PDW-F1600 XDCAM HD professional disc recorder', True,
              'Full-feature XDCAM HD deck (MPEG HD 4:2:0 up to 35 Mb/s, DVCAM, IMX), jog/shuttle. Check: USB and i.LINK panel face.',
              'Sony PDW-F1600 specifications (pro.sony)', 'https://pro.sony/ue_US/pdf/pdw-f1600')
xdcam_compact('pdw-hd1500', 'PDW-HD1500', 'PDW-HD1500 XDCAM HD422 compact recording deck', True,
              'XDCAM HD422 50 Mb/s, up to 8 audio channels. Also has a REMOTE 4-pin (DC 12 V) port. Check: USB and i.LINK panel face.',
              'Sony PDW-HD1500 specifications (pro.sony) and XDCAM HD422 catalogue', 'https://pro.sony/en_DO/pdf/pdw-hd1500')
xdcam_compact('pdw-f1500', 'PDW-F1500', 'PDW-F1500 XDCAM HD compact deck', False,
              'First-generation XDCAM HD half-rack deck (MPEG HD 4:2:0, 35/25/18 Mb/s), predecessor of the PDW-HD1500 and PDW-F1600. '
              'Check: connectors assumed the same as the PDW-F1600 (same chassis); Sony no longer publishes the F1500 sheet.',
              'Sony PDW-F1600 / PDW-HD1500 specifications (shared chassis)', 'https://pro.sony/ue_US/pdf/pdw-f1600')
add('xds-pd2000', 'XDS-PD2000', 'XDS-PD2000 XDCAM professional media station (disc + SxS + SSD)', 'XDCAM', 'recorder', 3,
    [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('in', 'HD-SDI', 'BNC', 1, 'HD/SD-SDI In'),
     R('out', 'HD-SDI', 'BNC', 2, 'HD-SDI Out'), R('out', 'SD-SDI', 'BNC', 2, 'SD-SDI Out'), R('out', 'HD-SDI', 'BNC', 2, 'SDI Monitor (HD/SD)'),
     R('out', 'Other', 'BNC', 1, 'Composite Out'), R('out', 'Other', 'BNC', 1, 'Composite Monitor'),
     R('in', 'Timecode', 'BNC', 1, 'TC In'), R('in', 'Timecode', 'BNC', 1, 'System TC In'), R('out', 'Timecode', 'BNC', 1, 'TC Out'),
     R('in', AA, 'XLR3F', 2, 'Audio In'), R('out', AA, 'XLR3M', 2, 'Audio Out'), R('out', AA, 'XLR3M', 2, 'Monitor Out'),
     R('in', 'AES/EBU', 'BNC', 4, 'AES In (8 ch)'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out (8 ch)'),
     R('out', 'HDMI', 'HDMI', 1, 'HDMI Monitor'), R('out', 'Other', 'DE-15', 1, 'VGA Monitor'),
     R('io', 'RS-422', 'DB9F', 2, 'Remote (RS-422A)'), R('io', 'Other', 'DB9F', 1, 'Video Control (RS-423)'), R('io', 'Other', 'DB15F', 1, 'GPIO'),
     R('io', 'Ethernet', 'RJ45', 1, 'Ethernet (1G)'), R('io', 'USB', 'USB', 5, 'USB'), F('out', AA, '6.3mm TRS', 1, 'Headphones'),
     R('in', 'Power', 'IEC', 1, 'AC In')],
    '424 x 132 x 460 mm (3RU, full width), 16 kg, AC 100-240 V, 210 W. Professional Disc drive, 2 SxS slots, internal SSD; '
    'XAVC, MPEG HD422, IMX, DVCAM. Check: which USB ports are on the front.', 'Sony XDS-PD2000 specifications (pro.sony)',
    'https://pro.sony/ue_US/pdf/xds-pd2000-a', full=False)
add('hdw-m2000', 'HDW-M2000P', 'HDW-M2000P HDCAM studio VTR (multi-format playback)', 'HDCAM', 'recorder', 4,
    [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('in', 'HD-SDI', 'BNC', 1, 'HD-SDI In'),
     R('out', 'HD-SDI', 'BNC', 3, 'HD-SDI Out'), R('out', 'SD-SDI', 'BNC', 3, 'SDI Out'), R('out', 'Other', 'BNC', 3, 'Composite Out'),
     R('out', 'Other', 'BNC', 3, 'Component Out (Y/R-Y/B-Y)'), R('in', AA, 'XLR3F', 5, 'Audio In (CH1-4, Cue)'),
     R('out', AA, 'XLR3M', 5, 'Audio Out (CH1-4, Cue)'), R('out', AA, 'XLR3M', 2, 'Monitor Out'),
     R('in', 'AES/EBU', 'BNC', 2, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out'),
     R('in', 'Timecode', 'XLR3F', 1, 'TC In'), R('out', 'Timecode', 'XLR3M', 1, 'TC Out'),
     R('io', 'RS-422', 'DB9F', 1, 'Remote In (RS-422A)'), R('io', 'RS-422', 'DB9F', 1, 'Remote Out (RS-422A)'), R('io', 'Other', 'DB9', 1, 'RS-232C'),
     R('io', 'Other', 'DB15', 1, 'Video Control'), R('io', 'Other', 'DB50F', 1, 'Parallel Remote'), F('out', AA, '6.3mm TRS', 1, 'Headphones'),
     R('in', 'Power', 'IEC', 1, 'AC In')],
    '427 x 174 x 544 mm (194 mm with feet), 23 kg, AC 100-240 V, 220 W. Records HDCAM, plays Digital Betacam, Betacam SX, Betacam SP. '
    'Optional HKDW-102 adds SDTI in/out. Rack mount on slides. Check: rack height (4RU without feet) and the D-sub 9 video control port.',
    'Expandore HDW-M2000P specification page and HDW-M2000 operation manual', 'https://expandore.com/PRODUCT/Sony/Proav/model/HD/HDCAM_VTR_M2000P.htm',
    verified=False)
add('srw-5800', 'SRW-5800', 'SRW-5800 HDCAM SR studio VTR', 'HDCAM SR', 'recorder', 5,
    [R('in', 'HD-SDI', 'BNC', 2, 'HD-SDI In A (1 loop)'), R('in', 'HD-SDI', 'BNC', 2, 'HD-SDI In B (opt, 1 loop)'),
     R('in', 'Reference', 'BNC', 2, 'Ref In 1 (1 loop)'), R('in', 'Reference', 'BNC', 2, 'Ref In 2 (HKSR-5001)'),
     R('in', 'AES/EBU', 'BNC', 6, 'AES In (CH1-12)'), R('in', 'Timecode', 'XLR3F', 1, 'TC In'),
     R('out', 'HD-SDI', 'BNC', 3, 'HD-SDI Out A'), R('out', 'HD-SDI', 'BNC', 3, 'HD-SDI Out B (opt)'),
     R('out', 'HD-SDI', 'BNC', 4, 'Format Conv Out A/B (HKSR-5001)'), R('out', 'SD-SDI', 'BNC', 3, 'SD-SDI Out'),
     R('out', 'Other', 'BNC', 1, 'Composite Out'), R('out', 'Reference', 'BNC', 1, 'SD Sync Out'), R('out', 'Reference', 'BNC', 2, 'HD Ref Out'),
     R('out', 'AES/EBU', 'BNC', 6, 'AES Out (CH1-12)'), R('out', AA, 'XLR3M', 1, 'Cue Out'), R('out', AA, 'XLR3M', 2, 'Monitor L/R'),
     R('out', 'Timecode', 'XLR3M', 1, 'TC Out'), R('io', 'RS-422', 'DB9F', 1, 'Remote 1 In'), R('io', 'RS-422', 'DB9F', 1, 'Remote 1 I/O'),
     R('io', 'Other', 'DB9F', 1, 'Video Control'), R('io', 'Other', 'DB50F', 1, 'Parallel I/O'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
     F('out', AA, '6.3mm TRS', 1, 'Headphones'), R('in', 'Power', 'IEC', 1, 'AC In')],
    'About 427 x 218 x 544 mm (5RU), 30 kg, 380 W with all options. HDCAM SR 4:4:4 / 4:2:2 dual-link capable with input/output B option boards; '
    'HKSR-5001 adds format conversion and a second reference. Check: rack height with feet removed, AC voltage range outside Japan '
    '(source is the Japanese catalogue, AC 100 V).', 'Sony SRW-5800 catalogue (sony.jp)', 'https://www-origin.sony.jp/products/catalog/SPC_SRW-5800.pdf')
add('dvw-a500', 'DVW-A500P', 'DVW-A500P Digital Betacam studio VTR', 'Digital Betacam', 'recorder', 6,
    [R('in', 'SD-SDI', 'BNC', 2, 'SDI In (active loop)'), R('in', 'Other', 'BNC', 3, 'Component In (Y/R-Y/B-Y)'),
     R('in', 'Other', 'BNC', 2, 'Composite In (opt BKDW-506, loop)'), R('in', 'Reference', 'BNC', 2, 'Ref In (loop)'),
     R('out', 'SD-SDI', 'BNC', 4, 'SDI Out'), R('out', 'Other', 'BNC', 3, 'Component Out'), R('out', 'Other', 'BNC', 3, 'Composite Out'),
     R('in', AA, 'XLR3F', 5, 'Audio In (CH1-4, Cue)'), R('out', AA, 'XLR3M', 5, 'Audio Out (CH1-4, Cue)'),
     R('in', 'AES/EBU', 'XLR3F', 2, 'AES In'), R('out', 'AES/EBU', 'XLR3M', 2, 'AES Out'), R('out', AA, 'XLR3M', 2, 'Monitor L/R'),
     R('in', 'Timecode', 'XLR3F', 1, 'TC In'), R('out', 'Timecode', 'XLR3M', 1, 'TC Out'),
     R('io', 'RS-422', 'DB9F', 2, 'Remote 1 In/Out'), R('io', 'Other', 'DB25', 1, 'RS-232C'), R('io', 'Other', 'DB50', 1, 'Parallel (opt BKDW-509)'),
     R('io', 'Other', 'DB15', 1, 'Video Control'), F('out', AA, '6.3mm TRS', 1, 'Headphones'), R('in', 'Power', 'IEC', 1, 'AC In')],
    '427 x 237 x 520 mm, 35 kg, AC 90-265 V, 175 W. Digital Betacam record, plays analogue Betacam/SP (A500). DVW-500P is the same without '
    'analogue playback (33 kg). Same frame size as BVW studio VTRs. Check: rack height (237 mm includes feet; 6RU assumed, may fit 5RU on slides).',
    'Sony Digital Betacam family brochure', 'https://archive.decromancer.ca/vtda.org/docs/AV/Sony/DVW-A500/SonyDigitalBetacamFamily.pdf',
    verified=False)
# Professional monitors
add('pvm-1741', 'PVM-1741', 'PVM-1741 17-inch OLED professional monitor', 'PVM OLED', 'monitor', 7,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
     R('in', 'Other', 'BNC', 1, 'Composite In'), R('out', 'Other', 'BNC', 1, 'Composite Loop'),
     R('in', AA, '3.5mm TRS', 1, 'Audio In'), R('out', AA, '3.5mm TRS', 1, 'Audio Monitor Out'), R('out', AA, '3.5mm TRS', 1, 'Headphones'),
     R('io', 'Other', '8-pin modular', 1, 'Parallel Remote'), R('io', 'Ethernet', 'RJ45', 1, 'LAN Remote'),
     R('in', 'Power', 'IEC', 1, 'AC In'), R('in', 'Power', 'XLR4M', 1, '12V DC In')],
    '17-inch Full HD OLED (1920 x 1080, 10-bit RGB). 436 x 289.6 x 120 mm without stand, 7.2 kg. EIA 19-inch rack mount with the '
    'supplied brackets. AC 100-240 V or 12 V DC (XLR 4-pin), about 70 W typical, 90 W max. 2 x 3G/HD/SD-SDI in, 1 SDI out, HDMI in, '
    'composite in with loop-through, stereo mini-jack audio in, audio monitor out and headphones, parallel remote (8-pin modular), '
    'Ethernet remote (up to 32 monitors). Replaced by the PVM-1741A. Check: rack height (7RU from the 290 mm panel height), the AC inlet '
    'type and which jacks are on the front.',
    'Sony PVM-1741 specifications (pro.sony)', 'https://pro.sony/en_AU/products/broadcastpromonitors/pvm-1741', full=False,
    screens={'count': 1, 'sizeIn': 17, 'aspect': '16:9'})
json.dump(M, open(OUT, 'w'), indent=1)
print(len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
