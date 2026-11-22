#!/usr/bin/env python3
"""Time and RF batch (added 2026-11-15): master clocks and NTP/PTP time servers, rack time displays, satellite IRDs and
modems, L-band distribution, UHF/VHF two-way radio base stations and repeaters, and RF / DVB-T in-house TV distribution.

  Timing:  masterclock, ese, wharton, timemachines, safran, microchip-timing, rosendahl, meinberg-more
  Satellite / contribution:  mediakind, synamedia (Cisco D98xx), sencore-more, ateme-more, harmonic-more, comtech
  L-band switching:  dev (splitters and LTC / reference DAs are done by tools of the catalogue thread)
  Two-way radio:  tait, motorola-radio, hytera, kenwood-radio, icom, simoco
  UHF / RF TV distribution:  wisi, promax, thor, blondertongue, kingray

Not added (no rack-mount product with published sizes or ports found): Plura and Alpermann+Velte (catalogue lists no models
or sizes online), Tekron (DIN-rail clocks), Global Invacom (FibreIRS GTUs are wall boxes), Novra (desktop receivers),
Triax TDH 800 (no rack height published), Teleste, Kathrein, Johansson (small wall-mount headend boxes), Vecsat (reseller),
Kordia (service provider). Studio wall clocks are not rack gear, so they are left out.

Brand files that already belong to other generators (meinberg, sencore, ateme, harmonic, evertz) are extended through
separate '-more' files so re-running either script never clobbers the other.
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
AC = lambda n=1: R('in', 'Power', 'IEC C14', n, 'PSU' if n > 1 else 'AC In')
LAN = lambda n=1, p='LAN': R('io', 'Ethernet', 'RJ45', n, p)

# ======================= Masterclock =======================
add('masterclock.json', 'masterclock-gmr1000', 'Masterclock', 'GMR1000', 'GMR1000 NTP / PTP master clock (quarter-rack)', 'GMR', 'clock', 1,
    [R('in', 'RF', 'SMA', 1, 'GNSS Antenna (option)'), LAN(1, 'NTP / PTP'), R('out', 'Timecode', 'DB9', 1, 'Time Code Gen (option)'),
     R('in', 'Timecode', 'DB9', 1, 'Time Code Reader (option)'), R('out', 'Reference', 'SMA', 1, '1PPS Out (option)'),
     R('out', 'Reference', 'SMA', 1, 'Prog Pulse Out (option)'), R('in', 'Reference', 'SMA', 1, 'Sync In (option)'),
     R('io', 'RS-232', 'Terminal block', 1, 'Serial / NMEA'), R('out', 'Other', 'Terminal block', 1, 'Alarm Relay'),
     R('in', 'Power', 'Locking DC jack', 1, '9-28V DC')],
    'Compact box (164 x 106 x 39 mm, 0.45 kg, under 7.5 W) with a 6-digit front display. NTP server/client as standard; options add '
    'PTP (IEEE 1588v2) grandmaster, GNSS, IRIG / SMPTE 12M time code generator and reader, 1PPS and 10 MHz. Mounts four across a 1U '
    'shelf with the RM4 bracket, so drawn as a quarter-width unit. External 24 V DC supply. Check: which options are fitted.',
    'Masterclock GMR1000 data sheet rev B', 'https://www.masterclock.com/masterclock-gmr-1000.html', w=3, powerW=7.5, weightKg=0.45)
add('masterclock.json', 'masterclock-gmr5000', 'Masterclock', 'GMR5000', 'GMR5000 multi-function master clock, 1U', 'GMR', 'clock', 1,
    [R('in', 'RF', 'SMA', 1, 'GNSS Antenna'), LAN(2, 'NTP / PTP'), R('out', 'Timecode', 'BNC', 2, 'SMPTE / IRIG Out'),
     R('out', 'Reference', 'BNC', 2, '1PPS / 10 MHz Out'), R('io', 'RS-232', 'DB9', 2, 'Serial'), R('out', 'Other', 'Terminal block', 1, 'Relays'), AC(2)],
    'Full-width 1U version of the GMR platform with a large front display and room for more output modules. '
    'Check: every port (the maker page gives no rear panel detail; counts are typical for a fitted unit).',
    'Masterclock product range page', 'https://masterclock.com/products/master-clocks', verified=False)

# ======================= ESE =======================
add('ese.json', 'ese-es-185u', 'ESE', 'ES-185U', 'ES-185U GPS master clock / time code generator, 1U', 'ES-185', 'clock', 1,
    [R('in', 'RF', 'TNC', 1, 'GPS Antenna'), R('out', 'Timecode', 'BNC', 1, 'SMPTE/EBU TC Out'), R('out', 'Timecode', 'BNC', 2, 'ESE TC89 / TC90 Out'),
     R('out', 'Reference', 'BNC', 1, '1PPS Out'), R('out', 'RS-232', 'DB9', 1, 'ASCII Out'), LAN(1, 'NTP (option /NTP)'),
     R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '1U rack master clock with a 9-digit LED UTC display (day of year, hours, minutes, seconds), 12-channel GPS receiver, '
    'SMPTE/EBU and ESE serial time code outputs that drive ESE slave clocks, 1PPS (+/-10 ns). /NTP option adds an NTP server port. '
    'Check: output counts and the antenna connector.', 'B&H and Markertek listings; ESE ES-185U manual (manualslib)',
    'https://www.markertek.com/product/es-185untp/ese-es-185u-ntp-gps-master-clock-time-code-generator', verified=False)
add('ese.json', 'ese-es-188f', 'ESE', 'ES-188F', 'ES-188F NTP-referenced master clock / time code generator, 1U', 'ES-188', 'clock', 1,
    [LAN(1, 'NTP Client'), R('out', 'Timecode', 'BNC', 1, 'SMPTE/EBU TC Out'), R('out', 'Timecode', 'BNC', 2, 'ESE TC89 / TC90 Out'),
     R('out', 'RS-232', 'DB9', 1, 'ASCII Out'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '1U rack master clock that takes time from an NTP server on the LAN and generates SMPTE/EBU and ESE time code for slave clocks '
    'and displays. ES-188E is the same with a smaller display. Check: output counts.', 'AVL Gear / Markertek listings',
    'https://avlgear.com/collections/ese/products/ese-es-188f-1ru-rackmount-ntp-referenced-master-clock-and-time-code-generator', verified=False)

# ======================= Wharton =======================
add('wharton.json', 'wharton-5400', 'Wharton', '5400', '5400 NTP time server / master clock (dual PSU)', '5000 Series', 'clock', 1,
    [LAN(1, 'NTP Server'), R('in', 'Timecode', 'Other', 1, 'Time Ref In (488HS4-GPS option)'), R('out', 'Timecode', 'Other', 2, 'zCode / Slave Clock Drive'),
     R('out', 'Timecode', 'Other', 2, 'AFOUT IRIG-B / EBU LTC'), R('io', 'RS-232', 'DB9', 2, 'SER23 RS-232/485 (option)'), AC(2)],
    'Rack-mount NTP / SNTP time server that also drives Wharton slave clocks (w482 mode up to fifty 4000E/NE clocks, impulse, '
    'DCF77/MSF) and outputs IRIG-B / EBU time code. GPS time comes from the 488HS4-GPS receiver. 5400 and 5600 have factory-fit dual '
    'redundant AC; others take a single AC or 24/48 V DC. Check: rack height and connector types.',
    'Canford Wharton 5000 Series page', 'https://canford.co.uk/WHARTON-CLOCKS-NTP-Time-Servers-Ethernet-5000-Series', verified=False)

# ======================= Time Machines =======================
add('timemachines.json', 'timemachines-tm160', 'Time Machines', 'TM160', 'TM160 PoE NTP clock display, 0.5-inch digits (rack plate)', 'Rack clocks', 'clock', 1,
    [R('in', 'Ethernet', 'RJ45', 1, 'PoE / NTP'), R('out', 'Other', 'Terminal block', 1, 'Relay')],
    'Small red-LED NTP clock powered from PoE (127 x 107 x 33 mm). Fits a 1U face plate: 760-022-000 single, or 760-023-000 dual to '
    'share the space with a TM1000/TM2000/TM2500 time server, so drawn half width.', 'Time Machines product page',
    'https://timemachinescorp.com/product/rack-mount-0-5-inch-poe-ntp-clock/', w=6)
add('timemachines.json', 'timemachines-tm2000', 'Time Machines', 'TM2000A', 'TM2000A GPS / GNSS NTP and PTP time server (rack plate)', 'Time servers', 'clock', 1,
    [R('in', 'RF', 'SMA', 1, 'GNSS Antenna'), R('in', 'Ethernet', 'RJ45', 1, 'PoE / NTP / PTP'), R('in', 'Power', 'DC barrel', 1, '12V DC (optional)')],
    'Compact GNSS NTP / PTP server on the same 1U plates as the TM160. Check: model suffix and power input.', 'Time Machines product range',
    'https://timemachinescorp.com/', verified=False, w=6)

# ======================= Safran (Orolia / Spectracom) =======================
add('safran.json', 'safran-securesync-2400', 'Safran', 'SecureSync 2400', 'SecureSync 2400 time and frequency server, 1U', 'SecureSync', 'clock', 1,
    [R('in', 'RF', 'SMA', 1, 'GNSS Antenna'), LAN(4, 'NTP / PTP / Mgmt'), R('out', 'Reference', 'BNC', 1, '1PPS Out'), R('out', 'Reference', 'BNC', 1, '10 MHz Out'),
     R('io', 'Other', 'Option slot', 6, 'Option Card Slot'), R('io', 'RS-232', 'DB9', 1, 'Serial'), R('out', 'Other', 'Terminal block', 1, 'Alarm'), AC(2)],
    'Ex-Spectracom (Orolia, now Safran) GNSS time server: NTP, PTP grandmaster, 1PPS and 10 MHz, with 6 option bays for time code '
    '(IRIG, SMPTE/EBU LTC), video sync (black burst / tri-level), more Ethernet and PTP ports. Dual AC or DC option. '
    'Check: base port counts and fitted cards.', 'Safran SecureSync data sheet', 'https://safran-navigation-timing.com/', verified=False)

# ======================= Microchip =======================
add('microchip-timing.json', 'microchip-syncserver-s650', 'Microchip', 'SyncServer S650', 'SyncServer S650 GNSS time server, 1U', 'SyncServer', 'clock', 1,
    [R('in', 'RF', 'BNC', 1, 'GNSS Antenna'), LAN(4, 'NTP / PTP'), R('out', 'Reference', 'BNC', 1, '1PPS Out'), R('out', 'Reference', 'BNC', 1, '10 MHz Out'),
     R('out', 'Timecode', 'BNC', 1, 'IRIG-B Out'), R('io', 'Other', 'Option slot', 1, 'Timing I/O module'), R('io', 'RS-232', 'DB9', 1, 'Console'), AC(2)],
    'GNSS NTP server and PTP grandmaster (ex-Symmetricom), with an option bay for extra time code, frequency and sync outputs. '
    'S600 is the version without the timing I/O bay. Check: port counts.', 'Microchip SyncServer S600/S650 data sheet',
    'https://www.microchip.com/', verified=False)

# ======================= Rosendahl =======================
add('rosendahl.json', 'rosendahl-nanosyncs-hd', 'Rosendahl', 'nanosyncs HD', 'nanosyncs HD sync generator (video, word clock, LTC), 1U', 'nanosyncs', 'other', 1,
    [R('in', 'Reference', 'BNC', 1, 'Video Ref In'), R('out', 'Reference', 'BNC', 6, 'Video Sync Out (BB / Tri)'), R('in', 'Reference', 'BNC', 1, 'Word Clock In'),
     R('out', 'Word clock', 'BNC', 8, 'Word Clock Out'), R('out', 'AES/EBU', 'XLR3M', 2, 'AES / DARS Out'), R('in', 'Timecode', 'XLR3F', 1, 'LTC In'),
     R('out', 'Timecode', 'XLR3M', 1, 'LTC Out'), R('io', 'Other', 'DIN', 1, 'MIDI'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Master sync generator for SD/HD video, word clock and AES with time code; locks to video, word clock or internal. '
    'Check: output counts.', 'Rosendahl nanosyncs HD manual', 'https://www.rosendahl-studiotechnik.com/', verified=False)

# ======================= Meinberg (more) =======================
add('meinberg-more.json', 'meinberg-lantime-m300', 'Meinberg', 'LANTIME M300', 'LANTIME M300 GPS NTP time server, 1U', 'LANTIME', 'clock', 1,
    [R('in', 'RF', 'BNC', 1, 'GPS Antenna'), LAN(1, 'NTP'), R('out', 'Reference', 'BNC', 1, '1PPS Out'), R('out', 'Reference', 'BNC', 1, '10 MHz Out'),
     R('out', 'Timecode', 'BNC', 1, 'IRIG-B Out'), R('io', 'RS-232', 'DB9', 2, 'COM'), R('out', 'Other', 'DB9', 1, 'Error Relay'), AC()],
    'Classic 1U NTP server with a built-in GPS receiver and front display. Extra Ethernet ports with the LAN option. '
    'Check: rear connectors (from the M300 data sheet summary).', 'Meinberg LANTIME M300 data sheet',
    'https://NOC.ac.uk/files/documents/facilities/james_cook/Meinberg_LANtime_M300_Datasheet.pdf', verified=False)

# ======================= MediaKind (ex-Ericsson) =======================
add('mediakind.json', 'mediakind-rx8200', 'MediaKind', 'RX8200', 'RX8200 advanced modular receiver (IRD), 1U', 'RX8000', 'converter', 1,
    [R('in', 'RF', 'F', 4, 'L-band In'), R('in', 'SDI', 'BNC', 1, 'ASI In'), R('in', 'Reference', 'BNC', 1, 'Frame Sync In'),
     R('out', '3G-SDI', 'BNC', 3, 'SDI / ASI Out'), R('out', 'Analog video', 'BNC', 1, 'Composite Out'), R('out', 'Analog video', 'DB15', 1, 'YPbPr / RGB Out'),
     R('out', 'AES/EBU', 'DB9', 2, 'Balanced Audio (2 analog + 2 AES pairs each)'), R('io', 'Ethernet', 'RJ45', 2, 'TS over IP'),
     R('io', 'RS-232', 'DB9', 1, 'Remote Control'), R('io', 'RS-232', 'DB9', 1, 'Data'), R('out', 'Other', 'DB9', 1, 'Alarm Relays'),
     R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), F('io', 'Other', 'CI slot', 2, 'CAM'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Ericsson / MediaKind satellite IRD: 4 L-band inputs (DVB-S / S2 / S2X), ASI and IP TS input, MPEG-2 / H.264 / HEVC decode, '
    'BISS and Common Interface CA. 442.5 x 545 x 44 mm, 100 W max. Audio comes on two D9 connectors with XLR or screw-terminal '
    'breakout cables. Check: management port and CAM slot count.', 'MediaKind RX8200 data sheet',
    'https://www.mediakind.com/wp-content/uploads/2020/10/RX8200-Datasheet.pdf', full=True, powerW=100)

# ======================= Synamedia / Cisco =======================
add('synamedia.json', 'cisco-d9800', 'Cisco (Synamedia)', 'D9800', 'D9800 network transport receiver, 1U', 'D98xx', 'converter', 1,
    [R('in', 'RF', 'F', 4, 'L-band In (LNB power on 1)'), R('in', 'SDI', 'BNC', 1, 'ASI In'), R('out', 'SDI', 'BNC', 1, 'ASI Out'),
     R('io', 'Ethernet', 'RJ45', 2, 'TS over IP'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out (option)'), R('out', 'AES/EBU', 'BNC', 2, 'AES-3id Out'),
     R('out', 'Analog audio', 'Terminal block', 2, 'Balanced Audio Pair'), R('out', 'HDMI', 'HDMI', 1, 'Monitor Out'),
     R('out', 'Analog video', 'BNC', 1, 'Composite Out'), R('out', 'Other', 'Terminal block', 1, 'Alarm Relay'),
     R('out', 'Analog audio', 'Terminal block', 1, 'Cue Tone'), R('out', 'GPIO', 'DB15', 1, 'Cue Triggers (8)'),
     R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), F('io', 'Other', 'CI slot', 2, 'CAM (option)'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'PowerVu / DVB satellite receiver-decoder (successor to the D9854/D9858). Four tuners (one active by default), +13/18 V LNB power '
    'on input 1, HDMI monitoring, 2 SDI out. 441 x 514 x 44 mm, 6.8-10 kg, 70-82 W. Check: ASI and Ethernet port counts.',
    'Synamedia D9800 data sheet', 'https://www.synamedia.com/wp-content/uploads/2019/04/Synamedia-D9800-Network-Transport-Receiver-Data-Sheet.pdf',
    verified=False, full=True, powerW=82)
add('synamedia.json', 'cisco-d9854', 'Cisco', 'D9854', 'D9854 advanced program receiver (legacy IRD), 1U', 'D98xx', 'converter', 1,
    [R('in', 'RF', 'F', 4, 'L-band In'), R('in', 'SDI', 'BNC', 1, 'ASI In'), R('out', 'SDI', 'BNC', 1, 'ASI Out'), R('out', 'HD-SDI', 'BNC', 2, 'SDI Out'),
     R('out', 'Analog video', 'BNC', 1, 'Composite Out'), R('out', 'AES/EBU', 'BNC', 2, 'AES Out'), R('out', 'Analog audio', 'Terminal block', 2, 'Audio Pair'),
     R('io', 'Ethernet', 'RJ45', 1, 'Data / Mgmt'), R('out', 'Other', 'Terminal block', 1, 'Alarm Relay'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Older PowerVu IRD still common in MCRs taking network feeds; replaced by the D9800. Check: all counts (from the D9854 manual summary).',
    'Cisco D9854 installation manual (manualslib)', 'https://www.manualslib.com/manual/1261104/Cisco-D9854.html', verified=False, full=True)

# ======================= Sencore (more) =======================
add('sencore-more.json', 'sencore-mrd-3187b', 'Sencore', 'MRD 3187B', 'MRD 3187B modular receiver decoder, 1U', 'MRD', 'converter', 1,
    [R('in', 'RF', 'F', 2, 'Satellite In (option)'), R('in', 'SDI', 'BNC', 2, 'ASI In'), R('out', 'SDI', 'BNC', 1, 'ASI Out'),
     R('io', 'Ethernet', 'RJ45', 1, 'TS over IP'), R('out', 'HD-SDI', 'BNC', 2, 'SDI Out'), R('out', 'Analog video', 'BNC', 1, 'Composite Out'),
     R('out', 'Analog audio', 'DB25', 1, 'Audio Out'), R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'),
     R('out', 'Other', 'Terminal block', 1, 'Alarm Relay'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'MPEG-2 / H.264 IRD with satellite, ASI and IP inputs and BISS descrambling. Check: all counts.', 'Sencore MRD 3187B data sheet',
    'https://www.sencore.com/', verified=False)

# ======================= Ateme (more) =======================
add('ateme-more.json', 'ateme-kyrion-dr5000', 'Ateme', 'Kyrion DR5000', 'Kyrion DR5000 integrated receiver decoder, 1U', 'Kyrion', 'converter', 1,
    [R('in', 'RF', 'F', 2, 'DVB-S/S2 In'), R('in', 'SDI', 'BNC', 2, 'ASI In'), R('io', 'Ethernet', 'RJ45', 2, 'TS over IP'),
     R('out', 'HD-SDI', 'BNC', 2, 'SDI Out'), R('out', 'AES/EBU', 'DB15', 1, 'AES Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
     R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Compact contribution / distribution IRD (H.264 / HEVC / MPEG-2, 4:2:2 10-bit) with BISS. Check: all counts.',
    'Ateme Kyrion DR5000 data sheet', 'https://www.ateme.com/', verified=False)

# ======================= Harmonic (more) =======================
add('harmonic-more.json', 'harmonic-proview-7100', 'Harmonic', 'ProView 7100', 'ProView 7100 integrated receiver decoder, 1U', 'ProView', 'converter', 1,
    [R('in', 'RF', 'F', 2, 'Satellite In'), R('in', 'SDI', 'BNC', 2, 'ASI In'), R('out', 'SDI', 'BNC', 2, 'ASI Out'), R('io', 'Ethernet', 'RJ45', 2, 'TS over IP'),
     R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'AES/EBU', 'DB25', 1, 'AES / Analog Audio'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
     R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('out', 'Other', 'DB9', 1, 'Alarm'), F('io', 'Other', 'CI slot', 2, 'CAM'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'Multi-format IRD for satellite, ASI and IP with transcoding options. Check: all counts.', 'Harmonic ProView 7100 data sheet',
    'https://www.harmonicinc.com/', verified=False)

# ======================= Comtech EF Data =======================
add('comtech.json', 'comtech-cdm-625a', 'Comtech EF Data', 'CDM-625A', 'CDM-625A advanced satellite modem, 1U', 'CDM', 'network', 1,
    [R('out', 'RF', 'N', 1, 'L-band Tx'), R('in', 'RF', 'N', 1, 'L-band Rx'), R('out', 'RF', 'BNC', 1, '70/140 MHz IF Tx'), R('in', 'RF', 'BNC', 1, '70/140 MHz IF Rx'),
     R('io', 'Ethernet', 'RJ45', 4, 'Traffic GbE'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), R('io', 'Other', 'HSSI / EIA-530', 1, 'Data (option)'),
     R('in', 'Reference', 'BNC', 1, '10 MHz In'), R('out', 'Other', 'DB15', 1, 'Alarms'), R('io', 'RS-232', 'DB9', 1, 'Remote'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    'SCPC satellite modem with DoubleTalk Carrier-in-Carrier, IF and L-band (BUC/LNB power options). Check: port counts.',
    'Comtech CDM-625A data sheet', 'https://www.comtechefdata.com/', verified=False)

# ======================= L-band switching =======================
add('dev.json', 'dev-1951', 'DEV Systemtechnik', 'DEV 1951', 'DEV 1951 universal switch chassis (L-band / ASI redundancy), 1U', 'Switching', 'router', 1,
    [R('in', 'RF', 'F', 4, 'Ch A/B In (per card)'), R('out', 'RF', 'F', 2, 'Out'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'),
     R('io', 'RS-232', 'DB9', 1, 'Serial'), R('io', 'GPIO', 'DB9', 1, 'Digital I/O'), AC(2)],
    'Two slots for DPST, transfer, ASI or optical switch cards (plus passive splitters) for L-band, ASI/SDI or broadband redundancy '
    'switching, SNMP and web control, redundant PSUs. Connectors depend on the card (F, BNC, SMA, N, E2000, SC/APC, FC/APC); drawn '
    'with two 2:1 L-band switch cards on F. Check: fitted cards.', 'DEV Systemtechnik DEV 1951 product page',
    'https://dev-systemtechnik.com/product/universal-switch-chassis-1-ru-dev-1951/', verified=False)
# ======================= Two-way radio =======================
RADIO = lambda rx='BNC': [R('out', 'RF', 'N', 1, 'Tx Antenna'), R('in', 'RF', rx, 1, 'Rx Antenna')]
add('tait.json', 'tait-tb9300', 'Tait', 'TB9300', 'TB9300 DMR base station subrack, 4U', 'TB9300', 'other', 4,
    RADIO() + [R('in', 'Reference', 'BNC', 1, 'Ext Freq Ref'), R('in', 'Reference', 'BNC', 1, '1PPS In'), LAN(1, 'Network (IP / Mgmt)'),
               R('io', 'Analog audio', 'DB25', 1, 'System Interface (600R line, E&M, TxKey / RxGate)'),
               R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In (12/24/48 V)')],
    'DMR Tier 2 / Tier 3 and analogue base station in a 4U subrack (177 x 483 x 400 mm): single-channel 50 W or 100 W, or dual 50 W. '
    'Bands: VHF 174-193 / 216-225 MHz, UHF 400-470 MHz, 900 MHz. Smart PSU switches from AC to DC battery backup. Ports shown for one '
    'reciter; a dual-channel build has two sets. Check: connectors (taken from the TB7300 sheet, the same reciter family).',
    'Tait TB9300 specification sheet', 'https://www.taitcommunications.com/products/dmr-radio/tb9300', verified=False)
add('tait.json', 'tait-tb9400', 'Tait', 'TB9400', 'TB9400 P25 base station subrack, 4U', 'TB9400', 'other', 4,
    RADIO() + [R('in', 'Reference', 'BNC', 1, 'Ext Freq Ref'), R('in', 'Reference', 'BNC', 1, '1PPS In'), LAN(1, 'Network (IP / Mgmt)'),
               R('io', 'Analog audio', 'DB25', 1, 'System Interface'), R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In')],
    'P25 Phase 1/2 and analogue sibling of the TB9300 in the same 4U subrack. Check: ports.', 'Tait TB9400 specification sheet',
    'https://www.taitcommunications.com/', verified=False)
add('tait.json', 'tait-tb7300', 'Tait', 'TB7300', 'TB7300 DMR / analogue slimline base station, 1U', 'TB7300', 'other', 1,
    RADIO() + [R('in', 'Reference', 'BNC', 1, 'Ext Freq Ref'), R('in', 'Reference', 'BNC', 1, '1PPS In'), LAN(1, 'Network'),
               R('io', 'RS-232', 'RJ11', 1, 'Serial'), R('io', 'Analog audio', 'DB25', 1, 'System Interface (analog line / I/O)'),
               R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In / 13.5V Aux Out')],
    '1U (44 x 483 x 400 mm) DMR Tier 2 and analogue base station / repeater. VHF 136-174 MHz 50 W, UHF 400-470 and 470-520 MHz 40 W, '
    '762-870 MHz 35 W. AC 120-230 V or DC 13.8 V / 55.2 V.', 'Tait TB7300 specification sheet',
    'https://www.taitcommunications.com/products/dmr-radio/tb7300')
add('tait.json', 'tait-tb8100', 'Tait', 'TB8100', 'TB8100 analogue base station subrack (legacy), 4U', 'TB8100', 'other', 4,
    RADIO() + [LAN(1, 'Network'), R('io', 'Analog audio', 'DB25', 1, 'System Interface'), R('in', 'Power', 'IEC C14', 1, 'AC In'),
               R('in', 'Power', 'Terminal block', 1, 'DC In')],
    'Older analogue / MPT base station in the 4U subrack that the TB9300 replaced; many still in service. Check: ports.',
    'Tait TB8100 installation manual', 'https://www.taitcommunications.com/', verified=False)
add('motorola-radio.json', 'motorola-slr5700', 'Motorola Solutions', 'SLR 5700', 'MOTOTRBO SLR 5700 repeater, 1U', 'MOTOTRBO', 'other', 1,
    RADIO() + [LAN(2, 'Ethernet'), R('io', 'USB', 'USB-A', 1, 'USB'), R('io', 'Other', 'DB25', 1, 'Accessory / Option board'),
               R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In (11-14.4 V)'), F('io', 'USB', 'USB-B', 1, 'Programming')],
    'MOTOTRBO digital / analogue repeater, 1-50 W, VHF 136-174 or UHF 400-470 MHz. 44 x 483 x 370 mm, 8.6 kg. '
    'Check: accessory connector.', 'Motorola SLR 5700 data sheet', 'https://bearcom.com/motorola-slr-5700-analog-or-digital-repeater-two-way-radio-infrastructure',
    weightKg=8.6)
add('motorola-radio.json', 'motorola-slr8000', 'Motorola Solutions', 'SLR 8000', 'MOTOTRBO SLR 8000 base station / repeater, 2U', 'MOTOTRBO', 'other', 2,
    RADIO('N') + [LAN(2, 'Ethernet'), R('io', 'Other', 'DB25', 1, 'Aux / System'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'),
                  R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In'), F('io', 'USB', 'USB-B', 1, 'Programming')],
    'High-power (100 W) MOTOTRBO repeater, 2U, with optional built-in preselector. Check: ports.', 'Motorola SLR 8000 data sheet',
    'https://www.motorolasolutions.com/', verified=False)
add('motorola-radio.json', 'motorola-mtr3000', 'Motorola Solutions', 'MTR3000', 'MTR3000 MOTOTRBO base station / repeater, 3U', 'MOTOTRBO', 'other', 3,
    RADIO('N') + [LAN(1, 'Ethernet'), R('io', 'Other', 'DB25', 1, 'System Connector'), R('in', 'Power', 'IEC C14', 1, 'AC In'), R('in', 'Power', 'Terminal block', 1, 'DC In (28.6 V)')],
    'Continuous-duty 100 W repeater, VHF 136-174 / UHF 403-470 MHz. 133 x 483 x 419 mm, 19 kg; AC 85-264 V or 28.6 V DC. '
    'Tx and Rx are both N female. Discontinued. Check: system and Ethernet connectors.', 'Motorola DR3000 / MTR3000 specifications',
    'https://aem-cloud-prod-cdn.motorolasolutions.com/content/dam/msi/docs/products/two-way-radios/mototrbo/dr3000-mtr3000-specifications.pdf',
    verified=False, weightKg=19)
add('hytera.json', 'hytera-rd985', 'Hytera', 'RD985', 'RD985 DMR repeater, 2U', 'RD98x', 'other', 2,
    RADIO() + [LAN(1, 'Ethernet (IP connect)'), R('io', 'Other', 'DB26', 1, 'Accessory'), R('in', 'Power', 'Terminal block', 1, '13.6V DC In'),
               F('io', 'USB', 'Other', 1, 'Programming')],
    'DMR / analogue repeater, VHF 136-174 or UHF 400-470 / 450-520 MHz, up to 50 W. 88 x 463 x 366 mm, 8.5 kg; 13.6 V DC (PS22002 '
    'external supply). RD985S is the newer version (adds 350-400 MHz and a 100 W model). Check: rear connectors.',
    'Hytera RD985 data sheet', 'https://hytera-europe.com/products/rd985', verified=False, weightKg=8.5)
add('kenwood-radio.json', 'kenwood-nxr-5800', 'Kenwood', 'NXR-5800', 'NXR-5800 UHF NXDN / DMR repeater, 2U', 'NXR-5000', 'other', 2,
    RADIO('N') + [LAN(1, 'Ethernet'), R('io', 'Other', 'DB25', 1, 'Accessory'), R('in', 'Power', 'IEC C14', 1, 'AC In'),
                  R('in', 'Power', 'Terminal block', 1, 'DC In')],
    'UHF 380-470 MHz digital / analogue repeater, up to 50 W. NXR-5700 is the VHF 136-174 MHz version. Check: height and ports.',
    'Kenwood NXR-5700/5800 brochure', 'https://www.kenwood.com/ca/com/systems/nxr-5700_5800/spec.html', verified=False)
add('icom.json', 'icom-ic-fr6300', 'Icom', 'IC-FR6300', 'IC-FR6300 UHF digital repeater, 2U', 'IC-FR5300', 'other', 2,
    RADIO('N') + [R('io', 'Other', 'DB25', 1, 'Accessory'), LAN(1, 'Ethernet (UC-FR5300 option)'), R('in', 'Power', 'Terminal block', 1, '13.6V DC In')],
    'NXDN / analogue repeater, 483 x 88 x 260 mm. UHF 400-470 / 450-520 MHz up to 50 W; IC-FR5300 is VHF 136-174 MHz. Optional '
    'UR-PA6000 100 W amplifier. Check: antenna connectors.', 'Icom America IC-FR5300/FR6300 page',
    'https://icomamerica.com/lineup/products/IC-FR5300_NXDN/', verified=False)
add('simoco.json', 'simoco-sdb680', 'Simoco', 'SDB680', 'SDB680 DMR base station / repeater, 2U', 'SDB600', 'other', 2,
    RADIO('N') + [LAN(1, 'IP'), R('io', 'Other', 'DB25', 1, 'Facilities'), R('in', 'Power', 'Terminal block', 1, '14.1V DC In')],
    'DMR Tier 2 / Tier 3 base station, 50 W, VHF 136-174, UHF 400-480 / 440-520 MHz. 408 x 450 x 88.9 mm. SDB670 is the 25 W version '
    '(AC or DC). Check: connectors.', 'Simoco DMR base station data sheet', 'https://simoco.com/wp-content/uploads/2025/05/Simoco-DMR-base-station.pdf', verified=False)

# ======================= UHF / RF TV distribution =======================
add('wisi.json', 'wisi-chameleon-gn20r', 'WISI', 'GN20R', 'Chameleon GN20R chassis (2 modules, dual PSU), 1U', 'Chameleon', 'converter', 1,
    [R('in', 'RF', 'F', 4, 'RF In'), R('io', 'SDI', 'BNC', 4, 'ASI In/Out'), R('out', 'RF', 'F', 2, 'RF Out'), R('io', 'Ethernet', 'RJ45', 2, 'Mgmt'),
     R('io', 'Ethernet', 'RJ45', 2, 'Streaming'), AC(2)],
    'Headend chassis, 482.6 x 44.45 x 235 mm, for two Chameleon software-defined modules (each: 2 RF in, 2 ASI BNC, RF out, management '
    'and GbE streaming). Modules receive DVB-S2/T2/C, transcode and modulate to DVB-T/C or IP. Encoder modules take 4 HDMI '
    '(GNHWENC2H) or 4 HD-SDI (GNHWENC2S). GN20B is the single-PSU version; GN50 is the 3U 10-module chassis. Under 60 W. '
    'Check: connector types.', 'WISI Chameleon data sheet rev G', 'https://amt.com/wp-content/uploads/2023/07/WISI_Chameleon_DS_RevG-1.pdf',
    verified=False, powerW=60)
add('promax.json', 'promax-mo-480', 'Promax', 'MO-480', 'MO-480 broadcast DVB-T / T2 modulator (SFN/MFN), 1U', 'MO', 'converter', 1,
    [R('in', 'SDI', 'BNC', 2, 'ASI / T2-MI In'), R('io', 'Ethernet', 'RJ45', 1, 'TS over IP In'), R('out', 'RF', 'N', 1, 'RF Out'),
     R('in', 'Reference', 'BNC', 1, '10 MHz In'), R('in', 'Reference', 'BNC', 1, '1PPS In'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), AC()],
    'Broadcast-grade DVB-T / T2 modulator for SFN and MFN, 30-900 MHz output. Check: connector types and PSU.', 'Promax MO-480 page',
    'https://www.promaxelectronics.com/ing/products/modulators/MO-480-481/broadcast-grade-dvb-t2-modulator/', verified=False)
add('thor.json', 'thor-h-thunder-8', 'Thor Broadcast', 'H-THUNDER-8', 'H-THUNDER-8 8-channel HDMI to RF modulator (QAM / ATSC / DVB-T), 1U', 'Thunder', 'converter', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'RF', 'F', 1, 'RF Out'), R('io', 'Ethernet', 'RJ45', 1, 'NMS'), AC()],
    'Encodes 8 HDMI sources to H.264 and modulates them onto coax (QAM, ATSC, DVB-T, ISDB-T), 50-950 MHz, about 20 W. RF only, no IPTV. '
    'H-THUNDER-1 and -4 are the 1 and 4 channel versions. Check: RF connector and SDI-input version.', 'Markertek Thor H-THUNDER-8 listing',
    'https://www.markertek.com/product/thr-h-thunder-8/thor-h-thunder-8-eight-hdmi-digital-rf-encoder-modulator-full-hd-up-to-1080p-1ru',
    verified=False, powerW=20)
add('blondertongue.json', 'blondertongue-rmda-1000-42p', 'Blonder Tongue', 'RMDA-1000-42P', 'RMDA-1000-42P rack mount distribution amplifier, 1U', 'RMDA', 'other', 1,
    [R('in', 'RF', 'F', 1, 'RF In'), R('out', 'RF', 'F', 1, 'RF Out'), F('out', 'RF', 'F', 2, 'Test Point -30 dB'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '42 dB, 54-1000 MHz forward-path broadband RF amplifier with gain and slope controls and in/out test points. '
    'Check: connector positions.', 'Blonder Tongue RMDA-1000-42P page', 'https://www.blondertongue.com/product/rmda-1000-42p', verified=False)
add('kingray.json', 'kingray-kr110', 'Kingray', 'KR110', 'KR110 headend frame (10 x KCC110 combiners + KLA110 launch amp)', 'Headend', 'other', 3,
    [F('in', 'RF', 'F', 10, 'KCC110 Ch In'), F('out', 'RF', 'F', 1, 'KLA110 RF Out'), F('out', 'RF', 'F', 1, 'Test Point'), R('in', 'Power', 'Other', 1, 'Mains In')],
    'Australian 19-inch rack or wall frame (reversible brackets) for up to ten KCC110 channel combiner modules and one KLA110 launch '
    'amplifier / power supply, for combining modulators and off-air channels onto one UHF/VHF feed. Check: rack height (estimated '
    '3U) and connector faces.', 'Bitek listing (Kingray KR110)', 'https://bitek.com.au/kingray-19-rack-or-wall-mountable-frame', verified=False)

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
allids = set()
for f in idx:
    if f in FILES: continue
    try: allids |= {m['id'] for m in json.load(open(os.path.join(CAT, f)))}
    except Exception: pass
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    clash = allids & set(ids); assert not clash, clash
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index', sum(len(v) for v in FILES.values()), 'models')
