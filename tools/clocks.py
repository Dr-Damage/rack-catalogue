#!/usr/bin/env python3
"""World clock pathways (added 2026-11-22) -> catalogue/clocks.json.

Master clocks, clock line distribution and the clocks they drive, so a facility's time path can be drawn and cabled:
GPS / NTP / PTP master clock -> time code DA, impulse or RS-485 line driver, or a PoE switch (NTP) -> wall clocks, studio
clocks and world clock (time zone) displays. Category 'clock' (tag CLK). Wall and studio clocks are off-rack end points:
add them in Signal paths as a Clock end point and pick the model, then type the time zone(s) each one shows.

Port types: 'Timecode' for SMPTE / EBU LTC, IRIG-B, ESE TC89 / TC90 and RS-485 time telegrams; 'Clock impulse' for polarised
minute / second impulse lines and MOBALine; NTP and PTP ride on 'Ethernet'. A model's 'zones' is how many time zones it shows.

Sources: TimeMachines time zone display page, MOBATIME TZI manual BE-801220.00 and DTS 4801/4802/4806 leaflet LE-800719.08,
Masterclock modular time zone clock page, Markertek ESE ES-192U listing. Generic templates are typical, not a product."""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue', 'clocks.json')
items = []
OFF = 'Off-rack end point: leave it out of the racks; add it in Signal paths as a Clock end point and type its time zone(s).'


def g(d, t, c, n, p, face='rear'):
    return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)


def add(id, mfr, pn, name, fam, ports, notes, src='Generic', url='', verified=False, ru=1, w=12, full=False, zones=None, cat='clock', **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=[p for p in ports if p])
    if zones: m['zones'] = zones
    m.update({k: v for k, v in kw.items() if v is not None})
    items.append(m)


AC = lambda n=1: g('in', 'Power', 'IEC C14', n, 'PSU' if n > 1 else 'AC In')
POE = g('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE in, NTP)')
CHK = 'Check: a typical layout, not a product; set the connectors to the real clock.'

# ---------------- generic: sources and distribution (racked) ----------------
add('generic-clock-master-gps', 'Generic', 'Master clock (GPS / NTP / PTP)', 'GPS master clock and NTP / PTP time server, 1U', 'Generic master clock',
    [g('in', 'RF', 'TNC', 1, 'GNSS Antenna'), g('io', 'Ethernet', 'RJ45', 2, 'NTP / PTP LAN'), g('out', 'Timecode', 'BNC', 4, 'LTC Out'),
     g('out', 'Timecode', 'BNC', 1, 'IRIG-B Out'), g('out', 'Clock impulse', 'Terminal block', 2, 'Impulse Line Out'),
     g('out', 'Timecode', 'Terminal block', 1, 'RS-485 Time Data Out'), g('out', 'Reference', 'BNC', 1, '1PPS Out'), g('out', 'Reference', 'BNC', 1, '10 MHz Out'),
     g('out', 'Other', 'Terminal block', 1, 'Alarm Relay'), AC(2)],
    'The top of a world clock pathway: GNSS locks the time, then NTP / PTP on the LAN, LTC and IRIG-B on BNC, impulse and RS-485 clock lines on terminals. ' + CHK)
add('generic-clock-tc-da', 'Generic', 'Time code DA 1x8', 'Time code (LTC / IRIG-B) distribution amplifier, 1 in 8 out, 1U', 'Generic clock distribution',
    [g('in', 'Timecode', 'BNC', 1, 'TC In'), g('out', 'Timecode', 'BNC', 1, 'TC Loop'), g('out', 'Timecode', 'BNC', 8, 'TC Out'), AC()],
    'Splits one time code feed from the master to clocks and units around the plant. ' + CHK, w=6)
add('generic-clock-line-driver', 'Generic', 'Clock line driver / sub-master', 'Slave clock line driver / sub-master, NTP in, 4 impulse and 2 RS-485 lines, 1U', 'Generic clock distribution',
    [g('io', 'Ethernet', 'RJ45', 1, 'NTP In'), g('in', 'Timecode', 'BNC', 1, 'TC In'), g('out', 'Clock impulse', 'Terminal block', 4, 'Impulse Line Out'),
     g('out', 'Timecode', 'Terminal block', 2, 'RS-485 Time Data Out'), g('out', 'Other', 'Terminal block', 1, 'Alarm Relay'), AC()],
    'Takes time from the master (NTP or time code) and drives lines of impulse or RS-485 slave clocks, each line to a floor or area. ' + CHK)
add('generic-clock-world-graphics', 'Generic', 'World clock generator (on screens)', 'World clock graphics generator, clocks and time zones on SDI / HDMI screens, 1U', 'Generic world clock',
    [g('io', 'Ethernet', 'RJ45', 1, 'NTP In'), g('in', 'Timecode', 'BNC', 1, 'LTC In'), g('in', 'Reference', 'BNC', 1, 'Ref In'),
     g('out', '3G-SDI', 'BNC', 2, 'SDI Out'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), AC()],
    'For world clocks shown on monitors or a multiviewer input: type every zone it shows in Time zone(s). ' + CHK, zones=12)
add('generic-gnss-antenna', 'Generic', 'GNSS antenna', 'GPS / GNSS timing antenna (roof)', 'Generic GNSS antenna',
    [g('out', 'RF', 'N-type', 1, 'RF Out')],
    'Roof antenna for the master clock. Off-rack: add it as an Other end point. ' + CHK, cat='other')

# ---------------- generic: clocks (off-rack) ----------------
add('generic-clock-ntp-poe-digital', 'Generic', 'NTP PoE digital clock', 'Digital wall clock, NTP over PoE, 4 or 6 digits', 'Generic wall clock',
    [POE], 'Time from the master over the network (NTP), power from the PoE switch port. ' + OFF + ' ' + CHK, zones=1)
add('generic-clock-ntp-poe-analogue', 'Generic', 'NTP PoE analogue clock', 'Analogue wall clock, NTP over PoE', 'Generic wall clock',
    [POE], 'Time and power on one network cable. ' + OFF + ' ' + CHK, zones=1)
add('generic-clock-impulse-analogue', 'Generic', 'Impulse slave clock', 'Analogue slave clock on a polarised minute impulse line (24 V)', 'Generic wall clock',
    [g('in', 'Clock impulse', 'Terminal block', 1, 'Impulse Line In')],
    'Driven and powered by the master clock or line driver impulse line; clocks on one line are wired in parallel. ' + OFF + ' ' + CHK, zones=1)
add('generic-clock-rs485-digital', 'Generic', 'RS-485 slave digital clock', 'Digital slave clock on an RS-485 time data line', 'Generic wall clock',
    [g('in', 'Timecode', 'Terminal block', 1, 'RS-485 Time Data In'), g('out', 'Timecode', 'Terminal block', 1, 'RS-485 Time Data Thru'), AC()],
    'Up to about 31 clocks daisy-chained on one RS-485 line from the master or line driver. ' + OFF + ' ' + CHK, zones=1)
add('generic-clock-ltc-display', 'Generic', 'Time code display', 'SMPTE / EBU LTC time code display', 'Generic studio clock',
    [g('in', 'Timecode', 'XLR3F', 1, 'LTC In'), g('out', 'Timecode', 'XLR3M', 1, 'LTC Thru'), g('in', 'Power', 'DC jack', 1, 'DC In')],
    'Shows the house time code from the master clock or a time code DA. ' + OFF + ' ' + CHK, zones=1)
add('generic-clock-irig-display', 'Generic', 'IRIG-B time display', 'IRIG-B time display', 'Generic studio clock',
    [g('in', 'Timecode', 'BNC', 1, 'IRIG-B In'), AC()], OFF + ' ' + CHK, zones=1)
add('generic-clock-studio-onair', 'Generic', 'Studio clock with on-air light', 'Studio LED ring clock with on-air tally, NTP or LTC', 'Generic studio clock',
    [g('io', 'Ethernet', 'RJ45', 1, 'LAN (NTP)'), g('in', 'Timecode', 'XLR3F', 1, 'LTC In'), g('in', 'Other', 'Terminal block', 2, 'Tally / GPI In'), g('in', 'Power', 'DC jack', 1, 'DC In')],
    OFF + ' ' + CHK, zones=1)
add('generic-world-clock-4-ntp', 'Generic', 'World clock, 4 zones (NTP PoE)', 'World clock panel, 4 time zones with city names, NTP over PoE', 'Generic world clock',
    [POE], 'One network cable for time and power; type the four zones (e.g. Perth, Sydney, London, New York). ' + OFF + ' ' + CHK, zones=4)
add('generic-world-clock-8-line', 'Generic', 'World clock, 8 zones (clock line)', 'World clock panel, 8 time zones, fed from a clock line (impulse, MOBALine, IRIG-B) or NTP', 'Generic world clock',
    [g('in', 'Clock impulse', 'Terminal block', 1, 'Clock Line In'), g('io', 'Ethernet', 'RJ45', 1, 'LAN (NTP)'), AC()],
    'Cable the clock line or the LAN, whichever the master uses. ' + OFF + ' ' + CHK, zones=8)

# ---------------- TimeMachines: two-line PoE time zone displays (verified from the maker page) ----------------
TM_URL = 'https://timemachinescorp.com/timezone-clock-timer-displays/'
for pn, dig, sz, box in [('760-2482-000', '4-digit', '2.5"', [400, 200, 60]), ('760-2682-000', '6-digit', '2.5"', [400, 200, 60]), ('760-4482-000', '4-digit', '4"', [445, 251, 64])]:
    add('timemachines-' + pn.lower(), 'Time Machines', pn, f'Time zone clock, {sz} {dig}, 2-line dot matrix, PoE (SNTP)', 'Time zone displays', [POE],
        f'Line 1 is the time ({sz} 7-segment), line 2 a dot-matrix text line naming the zone; switches between up to 5 time zones on set intervals; '
        'also timer and bar-graph modes. Powered by PoE 802.3af only (WiFi versions end in W). Wall or shelf / desk. ' + OFF,
        'TimeMachines time zone clock / timer displays page', TM_URL, verified=True, zones=5, boxMm=dict(w=box[0], h=box[1]))

# ---------------- MOBATIME ----------------
MB_DTS = 'https://www.mobatime.com/wp-content/uploads/2022/01/LE-800719.08-DTS-4801-4802-4806-masterclock.pdf'
for pn, lines, depth in [('DTS 4801', 1, 125), ('DTS 4802', 2, 125), ('DTS 4806', 6, 224)]:
    add('mobatime-' + pn.lower().replace(' ', '-'), 'MOBATIME', pn, f'{pn} network master clock and NTP server, {lines} MOBALine / impulse line{"s" if lines > 1 else ""}, 1U', 'DTS 48xx',
        [g('io', 'Ethernet', 'RJ45', 1, 'LAN (NTP server / client)', face='front'), g('io', 'RS-232', 'DB9', 1, 'Terminal', face='front'), g('io', 'USB', 'USB-A', 1, 'USB', face='front'),
         g('in', 'Timecode', 'Terminal block', 1, 'DCF / GPS 4500 In'), g('out', 'Power', 'Terminal block', 1, 'DC Out (GPS 4500)'),
         g('out', 'Clock impulse', 'Terminal block', lines, 'MOBALine / Impulse Line'), g('out', 'Timecode', 'Terminal block', 1, 'RS-485 Clock Line'),
         g('out', 'Timecode', 'Terminal block', 1, 'DCF / Pulse Out'), g('io', 'RS-232', 'Terminal block', 1, 'Serial'), g('in', 'Other', 'Terminal block', 4, 'Alarm / Control In'),
         g('out', 'Other', 'Terminal block', 1, 'Alarm Relay'), g('in', 'Power', 'Terminal block', 1, 'DC In 24-28V'), AC()],
        'Master clock for impulse, MOBALine or IRIG-B / AFNOR (option on 4801) slave clocks, NTP server and NTP time zone server; RS-485 clock line for up to 31 clocks. '
        'Time from a DCF 4500 / GPS 4500 receiver and / or NTP. 80 predefined and 20 programmable time zones. 90-240 VAC (max 30 VA) or 24-28 VDC. '
        f'483 x 44 x {depth} mm. Check: terminal layout and line counts (the leaflet output table is hard to read).',
        'MOBATIME leaflet LE-800719.08', MB_DTS, verified=False, powerW=30)
MB_TZI = 'https://www.mobatime.com/wp-content/uploads/2020/02/BE-801220.00-TZI-Time-zone-display_170316.pdf'
for pn, dig in [('TZI.57', '57 mm'), ('TZI.100', '100 mm')]:
    add('mobatime-' + pn.lower().replace('.', '-'), 'MOBATIME', pn, f'{pn} time zone display, {dig} digits with city name line, up to 8 zones', 'TZI',
        [g('in', 'Clock impulse', 'Terminal block', 1, 'Lines In (MOBALine / impulse / IRIG-B / DCF)'), g('in', 'Timecode', 'Terminal block', 1, 'RS-485 In (option)'),
         g('io', 'RS-232', 'Terminal block', 1, 'RS-232 (option)'), g('io', 'Ethernet', 'RJ45', 1, 'LAN NTP (option)'), g('in', 'Power', 'Terminal block', 1, 'AC In 100-240V')],
        'Indoor world time display: one row per zone, time in 7-segment digits and the location in dot matrix; up to 8 zones. Wall, ceiling or custom mount. '
        'Set by MOBALine, impulse, IRIG-B / AFNOR, DCF, MOBATIME serial code or NTP. ' + OFF + ' Check: variant names and how many rows your order has.',
        'MOBATIME TZI manual BE-801220.00', MB_TZI, verified=False, zones=8)

# ---------------- Masterclock and ESE ----------------
add('masterclock-ntds-tz', 'Masterclock', 'NTDS time zone module', 'Modular time zone clock, PoE NTP, 4 or 6 digits with 8-character zone line (e.g. NTDS24-8AL)', 'Modular time zone clocks',
    [POE, g('in', 'Timecode', 'Other', 1, 'Time Code In (option)'), g('in', 'Power', 'DC jack', 1, 'DC In (option)')],
    'One module per zone on a quick-release DIN rail; add a Clock end point per module, or one for the row and type every zone. ' + OFF + ' Check: part number per digit size and colour.',
    'Masterclock modular time zone clocks page', 'https://www.masterclock.com/modular-time-zone-clocks.html', verified=False, zones=1)
add('ese-es-192u', 'ESE', 'ES-192U', 'ES-192U low-cost master clock, 6-digit, TC90 output to slave displays, 1U', 'ES-192',
    [g('out', 'Timecode', 'BNC', 1, 'TC90 Out'), AC()],
    'Line-frequency (or optional quartz) timebase, drives ESE slave displays over TC90 time code; auto daylight saving. Check: connectors and rack size.',
    'Markertek ES-192U listing', 'https://m.markertek.com/product/es-192u/es-192u-master-clock-6-digit-12-hour', verified=False)

json.dump(items, open(OUT, 'w'), indent=1, ensure_ascii=False)
open(OUT, 'a').write('\n')
print(len(items), 'models ->', OUT)
