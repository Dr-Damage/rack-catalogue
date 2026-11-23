"""Room end points: where cables terminate outside the racks -> catalogue/room-endpoints.json.

Two kinds:
- Room patch points (category 'wallbox', endpoint 'patch'): SDI, XLR, data, HDMI, fibre, speakON and DMX wall plates, desk
  plates and floor pockets. They use the feed-through engine (`thru` with per-hole `inserts`), so each hole has a
  "<prefix>n rear" (the tie line from the rack) and a "<prefix>n front" (the room side you plug into). Inserts can be changed
  on the placed plate.
- Room gear (category 'endpoint', tag EP): generic TVs, commercial displays, SDI monitors, projectors, PCs, laptops, KVM desk
  receivers, mics, speakers, access points, intercom beltpacks and wall stations, tally lights. Each carries `endpoint` (the
  Signal paths end point kind it belongs to) so the Model picker on New endpoint lists it.
- Mains power outlets (GPOs, 2026-11-23; category 'endpoint', endpoint 'power'): AU / NZ 10A, 15A, 20A, 32A and 3 phase outlets, plus IEC
  C13 / C19, IEC 60309, Schuko, UK and NEMA. Each carries a hardwired `pdu` block, so it has outlets to cable power into.

All generic, so connectors are typical rather than one product's: verified=False with a 'Check:' note.
"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'room-endpoints.json')
items = []
CHECK = 'Generic room end point: typical connectors, check against the actual product before ordering.'
OFF = 'Off-rack end point: leave it out of the racks and type where it is (or add it as an end point in Signal paths and pick the model there).'


def g(dir, type, conn, count, prefix, face='rear'):
    return {'face': face, 'dir': dir, 'type': type, 'connector': conn, 'count': count, 'prefix': prefix}


# ---------------- room patch points (feed-through plates) ----------------
def plate(id, pn, name, fam, inserts, rows=1, prefix='P', kind='patch', notes=''):
    items.append({'id': 'room-' + id, 'manufacturer': 'Generic', 'partNumber': pn, 'name': name, 'family': fam, 'category': 'wallbox',
                  'endpoint': kind, 'ru': 1, 'widthCols': 12, 'fullDepth': False, 'verified': False, 'source': 'Generic',
                  'notes': (notes + ' ' if notes else '') + 'Rear = the tie line from the rack, front = the room side you plug into. ' + OFF + ' ' + CHECK,
                  'thru': {'holes': len(inserts), 'rows': rows, 'prefix': prefix, 'insert': '', 'fixed': False, 'inserts': inserts}, 'portGroups': []})


SDI = 'SDI patch point'
for n in (1, 2, 4, 6, 8):
    plate(f'sdi-{n}', f'SDI patch point {n} x BNC', f'SDI patch point, {n} x BNC (12G) wall plate', SDI, ['bnc'] * n, 1 if n <= 4 else 2, 'SDI')
XLR = 'XLR patch point'
for n in (1, 2, 4, 6, 8):
    plate(f'xlr-{n}f', f'XLR patch point {n} x XLR3F', f'XLR patch point, {n} x XLR3 female (mic / line into the rack)', XLR, ['xlr3f'] * n, 1 if n <= 4 else 2, 'XLR')
for n in (1, 2, 4):
    plate(f'xlr-{n}m', f'XLR patch point {n} x XLR3M', f'XLR patch point, {n} x XLR3 male (line out to the room)', XLR, ['xlr3m'] * n, 1, 'XLR')
plate('xlr-2f2m', 'XLR patch point 2F + 2M', 'XLR patch point, 2 x XLR3 female in + 2 x XLR3 male out', XLR, ['xlr3f', 'xlr3f', 'xlr3m', 'xlr3m'], 1, 'XLR')
plate('xlr-4f4m', 'XLR patch point 4F + 4M', 'XLR patch point, 4 x XLR3 female in + 4 x XLR3 male out', XLR, ['xlr3f'] * 4 + ['xlr3m'] * 4, 2, 'XLR')
plate('xlr-db25-8', 'XLR stage plate 8 x XLR3F', 'Stage / audio plate, 8 x XLR3 female (8-channel multicore or DB25 tie)', XLR, ['xlr3f'] * 8, 2, 'XLR')
NET = 'Data outlet'
plate('rj45-1', 'Data outlet 1 x RJ45', 'Data outlet, 1 x RJ45 Cat6 (wall plate)', NET, ['rj45'], 1, 'DATA')
plate('rj45-2', 'Data outlet 2 x RJ45', 'Data outlet, 2 x RJ45 Cat6 (wall plate)', NET, ['rj45'] * 2, 1, 'DATA')
plate('rj45-4', 'Data outlet 4 x RJ45', 'Data outlet, 4 x RJ45 Cat6 (wall plate)', NET, ['rj45'] * 4, 1, 'DATA')
plate('ethercon-2', 'etherCON patch point 2', 'etherCON patch point, 2 x etherCON (touring / stage)', NET, ['ethercon'] * 2, 1, 'NET')
AV = 'AV wall plate'
plate('hdmi-1', 'HDMI wall plate 1', 'HDMI wall plate, 1 x HDMI', AV, ['hdmi'], 1, 'HDMI')
plate('hdmi-usb', 'HDMI + USB wall plate', 'Presenter wall plate, HDMI + USB', AV, ['hdmi', 'usb'], 1, 'AV')
plate('hdmi-rj45', 'HDMI + RJ45 wall plate', 'Display wall plate, HDMI + RJ45 data (behind a TV)', AV, ['hdmi', 'rj45'], 1, 'AV')
plate('tv-plate', 'TV wall plate: SDI, HDMI, 2 x RJ45', 'TV / display wall plate: BNC, HDMI, 2 x RJ45', AV, ['bnc', 'hdmi', 'rj45', 'rj45'], 1, 'AV',
      notes='Typical plate behind a wall-mounted TV or monitor.')
plate('combo-av', 'AV patch point: 2 BNC, 2 XLR, etherCON', 'AV patch point: 2 x BNC, 2 x XLR3F, 1 x etherCON', AV, ['bnc', 'bnc', 'xlr3f', 'xlr3f', 'ethercon'], 1, 'AV')
plate('combo-av-big', 'AV patch point: 4 BNC, 4 XLR, 2 etherCON, HDMI', 'AV patch point: 4 x BNC, 4 x XLR3F, 2 x etherCON, HDMI', AV,
      ['bnc'] * 4 + ['xlr3f'] * 4 + ['ethercon', 'ethercon', 'hdmi'], 2, 'AV')
FO = 'Fibre outlet'
plate('lc-1', 'Fibre outlet 1 x LC duplex', 'Fibre outlet, 1 x LC duplex', FO, ['lc'], 1, 'FO')
plate('lc-2', 'Fibre outlet 2 x LC duplex', 'Fibre outlet, 2 x LC duplex', FO, ['lc'] * 2, 1, 'FO')
plate('ocduo-1', 'opticalCON DUO patch point', 'Fibre patch point, 1 x opticalCON DUO', FO, ['ocduo'], 1, 'FO')
SP = 'Speaker / DMX outlet'
plate('speakon-1', 'Speaker outlet 1 x speakON', 'Speaker outlet, 1 x speakON NL4', SP, ['speakon'], 1, 'SPK')
plate('speakon-2', 'Speaker outlet 2 x speakON', 'Speaker outlet, 2 x speakON NL4', SP, ['speakon'] * 2, 1, 'SPK')
plate('dmx-2', 'DMX outlet 2 x XLR5', 'DMX outlet, 2 x XLR5 female (lighting)', SP, ['xlr5f'] * 2, 1, 'DMX')
DESK = 'Desk / floor termination'
plate('desk-op', 'Desk plate: 2 BNC, 2 XLR, 4 RJ45, HDMI', 'Operator desk termination plate: 2 x BNC, 2 x XLR3F, 4 x RJ45, HDMI', DESK,
      ['bnc', 'bnc', 'xlr3f', 'xlr3f', 'rj45', 'rj45', 'rj45', 'rj45', 'hdmi'], 2, 'D', kind='desk')
plate('desk-ic', 'Desk plate: intercom XLR, 2 RJ45', 'Desk termination plate: intercom XLR3F, 2 x RJ45', DESK, ['xlr3f', 'rj45', 'rj45'], 1, 'D', kind='desk')
plate('floor-pocket', 'Floor pocket: 2 BNC, 4 XLR, 2 RJ45', 'Floor pocket: 2 x BNC, 4 x XLR3F, 2 x RJ45', DESK, ['bnc', 'bnc'] + ['xlr3f'] * 4 + ['rj45', 'rj45'], 2, 'FP')

# ---------------- room gear (generic) ----------------
def ep(id, kind, pn, name, family, ports, notes='', mfr='Generic'):
    items.append({'id': 'room-' + id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': 'endpoint', 'endpoint': kind,
                  'ru': 1, 'widthCols': 12, 'fullDepth': False, 'verified': False, 'source': 'Generic',
                  'notes': (notes + ' ' if notes else '') + OFF + ' ' + CHECK, 'portGroups': [p for p in ports if p]})


IEC = lambda conn='IEC C14': g('in', 'Power', conn, 1, 'Power In')
# TVs and displays
ep('tv', 'monitor', 'Generic TV', 'TV (consumer), 3 x HDMI, LAN, RF', 'TV / display',
   [g('in', 'HDMI', 'HDMI', 3, 'HDMI In'), g('in', 'Other', 'F connector', 1, 'RF In (antenna)'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'),
    g('out', 'Analog audio', 'Toslink', 1, 'Optical Audio Out'), g('io', 'USB', 'USB-A', 1, 'USB'), IEC('IEC C7')])
ep('tv-hotel', 'monitor', 'Generic TV with RS-232', 'TV (commercial / hospitality), 3 x HDMI, RS-232, LAN, RF', 'TV / display',
   [g('in', 'HDMI', 'HDMI', 3, 'HDMI In'), g('in', 'Other', 'F connector', 1, 'RF In (antenna)'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'),
    g('io', 'Other', '3.5mm jack', 1, 'RS-232 Control'), IEC('IEC C7')])
ep('display-commercial', 'monitor', 'Generic commercial display', 'Commercial display, 2 x HDMI, DisplayPort, HDBaseT, RS-232, LAN', 'TV / display',
   [g('in', 'HDMI', 'HDMI', 2, 'HDMI In'), g('in', 'DisplayPort', 'DisplayPort', 1, 'DP In'), g('in', 'Ethernet', 'RJ45', 1, 'HDBaseT In'),
    g('io', 'Other', 'DB9', 1, 'RS-232'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'), g('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'), IEC()])
ep('display-sdi', 'monitor', 'Generic commercial display with SDI', 'Commercial display with 3G-SDI in and loop, HDMI, LAN', 'TV / display',
   [g('in', '3G-SDI', 'BNC', 1, 'SDI In'), g('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'), g('in', 'HDMI', 'HDMI', 2, 'HDMI In'),
    g('io', 'Other', 'DB9', 1, 'RS-232'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'), IEC()])
ep('mon-sdi-3g', 'monitor', 'Generic 3G-SDI monitor', 'Broadcast / field monitor, 2 x 3G-SDI in with loop, HDMI', 'SDI monitor',
   [g('in', '3G-SDI', 'BNC', 2, 'SDI In'), g('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'), g('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
    g('in', 'GPI', 'RJ45', 1, 'Tally / GPI'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')])
ep('mon-sdi-12g', 'monitor', 'Generic 12G-SDI monitor', 'Broadcast reference monitor, 12G-SDI in and out, quad 3G, HDMI, ref', 'SDI monitor',
   [g('in', '12G-SDI', 'BNC', 2, 'SDI In'), g('out', '12G-SDI', 'BNC', 2, 'SDI Out'), g('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
    g('in', 'Reference', 'BNC', 1, 'Ref In'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'), g('in', 'GPI', 'DB9', 1, 'GPI / Tally'), IEC()])
# projectors
ep('proj', 'projector', 'Generic projector', 'Projector, 2 x HDMI, HDBaseT, RS-232, LAN', 'Projector',
   [g('in', 'HDMI', 'HDMI', 2, 'HDMI In'), g('in', 'Ethernet', 'RJ45', 1, 'HDBaseT In'), g('io', 'Other', 'DB9', 1, 'RS-232'),
    g('io', 'Ethernet', 'RJ45', 1, 'LAN'), IEC()])
ep('proj-sdi', 'projector', 'Generic large-venue projector', 'Large-venue laser projector, 3G-SDI, 2 x HDMI, HDBaseT, DisplayPort, RS-232, LAN', 'Projector',
   [g('in', '3G-SDI', 'BNC', 1, 'SDI In'), g('in', 'HDMI', 'HDMI', 2, 'HDMI In'), g('in', 'DisplayPort', 'DisplayPort', 1, 'DP In'),
    g('in', 'Ethernet', 'RJ45', 1, 'HDBaseT In'), g('io', 'Other', 'DB9', 1, 'RS-232'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'), IEC('IEC C20')])
# PCs
ep('pc', 'workstation', 'Generic desktop PC', 'Desktop PC, 2 x DisplayPort, HDMI, LAN, USB, audio', 'PC',
   [g('out', 'DisplayPort', 'DisplayPort', 2, 'DP Out'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'),
    g('io', 'USB', 'USB-A', 2, 'USB'), g('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'), g('in', 'Analog audio', '3.5mm jack', 1, 'Mic In'), IEC()])
ep('pc-capture', 'workstation', 'Generic PC with SDI capture card', 'Workstation PC with a 4-channel SDI I/O card (e.g. DeckLink), ref in', 'PC',
   [g('io', '3G-SDI', 'BNC', 4, 'SDI'), g('in', 'Reference', 'BNC', 1, 'Ref In'), g('out', 'DisplayPort', 'DisplayPort', 2, 'DP Out'),
    g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('io', 'Ethernet', 'RJ45', 2, 'LAN'), g('io', 'USB', 'USB-A', 2, 'USB'), IEC()],
   notes='SDI ports are bidirectional, as on DeckLink Quad cards; set each to In or Out in the unit panel if needed.')
ep('laptop', 'workstation', 'Generic laptop', 'Laptop, HDMI out, USB-C, LAN', 'PC',
   [g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('io', 'USB', 'USB-C', 2, 'USB-C'), g('io', 'Ethernet', 'RJ45', 1, 'LAN'),
    g('out', 'Analog audio', '3.5mm jack', 1, 'Headset'), g('in', 'Power', 'Other', 1, 'Power In')])
ep('kvm-rx', 'workstation', 'Generic KVM desk receiver', 'KVM extender receiver at a desk: link in, 2 x DisplayPort, USB, audio', 'PC',
   [g('in', 'Ethernet', 'RJ45', 1, 'Link In'), g('out', 'DisplayPort', 'DisplayPort', 2, 'DP Out'), g('io', 'USB', 'USB-A', 4, 'USB'),
    g('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'), g('in', 'Power', 'Other', 1, 'DC In')],
   notes='For a fibre KVM link, change Link In to Fibre / LC duplex.')
# mics and speakers
ep('mic-dyn', 'mic', 'Generic dynamic mic', 'Dynamic microphone (XLR3M out)', 'Microphone', [g('out', 'Analog audio', 'XLR3M', 1, 'Mic Out')])
ep('mic-cond', 'mic', 'Generic condenser mic', 'Condenser microphone (XLR3M out, needs 48V phantom)', 'Microphone', [g('out', 'Analog audio', 'XLR3M', 1, 'Mic Out')])
ep('mic-gooseneck', 'mic', 'Generic gooseneck mic', 'Gooseneck desk microphone (XLR3M out)', 'Microphone', [g('out', 'Analog audio', 'XLR3M', 1, 'Mic Out')])
ep('mic-ceiling-dante', 'mic', 'Generic Dante ceiling mic', 'Ceiling array microphone, Dante over PoE', 'Microphone', [g('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)')])
ep('spk-passive', 'speaker', 'Generic passive speaker', 'Passive loudspeaker, speakON NL4 in and link', 'Speaker',
   [g('in', 'Analog audio', 'speakON', 1, 'Speaker In'), g('out', 'Analog audio', 'speakON', 1, 'Speaker Link')])
ep('spk-active', 'speaker', 'Generic active speaker', 'Active loudspeaker / monitor, XLR in and thru, IEC power', 'Speaker',
   [g('in', 'Analog audio', 'XLR3F', 1, 'Line In'), g('out', 'Analog audio', 'XLR3M', 1, 'Line Thru'), IEC()])
ep('spk-100v', 'speaker', 'Generic 100V ceiling speaker', '100V line ceiling speaker (Phoenix / terminal)', 'Speaker',
   [g('in', 'Analog audio', 'Phoenix', 1, '100V In'), g('out', 'Analog audio', 'Phoenix', 1, '100V Link')])
ep('spk-dante', 'speaker', 'Generic Dante PoE speaker', 'Dante PoE speaker', 'Speaker', [g('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)')])
# network
ep('ap', 'ap', 'Generic PoE access point', 'Wireless access point, PoE powered', 'Access point', [g('in', 'Ethernet', 'RJ45', 1, 'LAN (PoE)')])
ep('ap-dual', 'ap', 'Generic Wi-Fi 6E/7 access point', 'Wireless access point with 2 uplinks (one PoE)', 'Access point',
   [g('in', 'Ethernet', 'RJ45', 1, 'LAN 1 (PoE)'), g('io', 'Ethernet', 'RJ45', 1, 'LAN 2')])
# other room gear
ep('ic-beltpack', 'other', 'Generic wired beltpack', 'Partyline intercom beltpack (XLR3 in and loop, headset XLR4)', 'Intercom station',
   [g('io', 'Intercom', 'XLR3M', 1, 'Line In'), g('io', 'Intercom', 'XLR3F', 1, 'Line Loop'), g('io', 'Other', 'XLR4M', 1, 'Headset')])
ep('ic-wall', 'other', 'Generic intercom wall station', 'Intercom wall / speaker station (4-wire XLR or IP)', 'Intercom station',
   [g('io', 'Intercom', 'RJ45', 1, '4-wire / IP'), g('io', 'Other', 'XLR5F', 1, 'Headset')])
ep('tally-light', 'other', 'Generic tally light', 'Studio tally / on-air light (GPI)', 'Tally', [g('in', 'GPI', 'Other', 1, 'Tally In'), g('in', 'Power', 'Other', 1, 'Power In')])
ep('onair-sign', 'other', 'Generic on-air sign', 'On-air / recording sign (GPI, mains)', 'Tally', [g('in', 'GPI', 'Other', 1, 'GPI In'), IEC('IEC C8')])


# ---------------- mains power outlets (GPOs) ----------------
# A GPO is modelled like a hardwired power strip: a `pdu` block (plug 'hard', the outlets and the circuit that feeds them), so
# its ports are "Mains In" + "Outlet n", a room unit's Power In cables to an outlet (cable P-nnnn) and the outlet shows its
# load like a rack PDU does. Category 'endpoint', endpoint 'power' (Signal paths: Mains power outlet (GPO)).
GPO_NOTE = ('Mains outlet in the room. Cable a unit\'s Power In to one of its outlets to show what it feeds and the load on the '
            'circuit. The circuit (breaker / RCD at the board) is typical: set it to match the electrical drawings. Mains wiring is '
            'for a licensed electrician.')


def gpo(id, pn, name, fam, outlets, volts=230, amps=10, phase=1, circuit=None, notes=''):
    circuit = circuit or {'id': 'A', 'type': 'rcbo', 'amps': 16 if amps <= 10 else 20 if amps <= 16 else 32 if amps <= 32 else amps, 'mA': 30}
    items.append({'id': 'room-' + id, 'manufacturer': 'Generic', 'partNumber': pn, 'name': name, 'family': fam, 'category': 'endpoint',
                  'endpoint': 'power', 'ru': 1, 'widthCols': 12, 'fullDepth': False, 'verified': False, 'source': 'Generic',
                  'notes': (notes + ' ' if notes else '') + GPO_NOTE + ' ' + OFF + ' ' + CHECK,
                  'pdu': {'mount': 'h', 'phase': phase, 'volts': volts, 'amps': amps, 'plug': 'hard', 'main': {'type': 'none'},
                          'circuits': [circuit], 'outlets': [{'type': t, 'count': n, 'circuit': 'A', 'switched': sw} for t, n, sw in outlets],
                          'metering': 'none'},
                  'portGroups': []})


AU = 'AU / NZ power outlet (GPO)'
gpo('gpo-au-1-10', 'GPO single 10A', 'Power point (GPO), single 10A switched, AS/NZS 3112', AU, [('au10', 1, True)])
gpo('gpo-au-2-10', 'GPO double 10A', 'Power point (GPO), double 10A switched, AS/NZS 3112', AU, [('au10', 2, True)])
gpo('gpo-au-4-10', 'GPO quad 10A', 'Power point (GPO), quad 10A switched (desk / AV wall)', AU, [('au10', 4, True)])
gpo('gpo-au-2-10-ip', 'GPO double 10A IP56', 'Weatherproof power point, double 10A switched, IP56', AU, [('au10', 2, True)],
    notes='For outdoor camera positions, roofs and wash-down areas.')
gpo('gpo-au-1-15', 'GPO single 15A', 'Power point (GPO), single 15A switched (wide earth pin)', AU, [('au15', 1, True)], amps=15)
gpo('gpo-au-2-15', 'GPO double 15A', 'Power point (GPO), double 15A switched (wide earth pin)', AU, [('au15', 2, True)], amps=15)
gpo('gpo-au-1-20', 'Outlet single 20A', 'Power outlet, single 20A switched, AS/NZS 3112', AU, [('au20', 1, True)], amps=20)
gpo('gpo-au-32-1p', 'Outlet 32A single phase', 'Industrial outlet, 32A single phase 3 pin round (AS/NZS 3123), switched', AU, [('au32', 1, True)], amps=32,
    notes='For a large PDU, UPS or OB truck feed.')
gpo('gpo-au-20-3p', 'Outlet 20A 3 phase 5 pin', 'Industrial outlet, 20A 3 phase 5 pin (AS/NZS 3123), switched', AU, [('au3p20', 1, True)], volts=400, amps=20, phase=3,
    circuit={'id': 'A', 'type': 'rcbo', 'amps': 20, 'mA': 30})
gpo('gpo-au-32-3p', 'Outlet 32A 3 phase 5 pin', 'Industrial outlet, 32A 3 phase 5 pin (AS/NZS 3123), switched', AU, [('au3p32', 1, True)], volts=400, amps=32, phase=3,
    circuit={'id': 'A', 'type': 'rcbo', 'amps': 32, 'mA': 30}, notes='For a 3 phase rack PDU, dimmer rack or OB truck feed.')
IEC = 'IEC and other region outlets'
gpo('gpo-c13-2', 'Outlet plate 2 x IEC C13', 'Outlet plate, 2 x IEC C13 (UPS or clean power circuit)', IEC, [('c13', 2, False)])
gpo('gpo-c19-1', 'Outlet plate 1 x IEC C19', 'Outlet plate, 1 x IEC C19 16A', IEC, [('c19', 1, False)], amps=16)
gpo('gpo-cee16-1', 'Outlet IEC 60309 16A blue', 'Industrial outlet, IEC 60309 16A single phase (blue)', IEC, [('cee16', 1, True)], amps=16)
gpo('gpo-cee32-1', 'Outlet IEC 60309 32A blue', 'Industrial outlet, IEC 60309 32A single phase (blue)', IEC, [('cee32', 1, True)], amps=32)
gpo('gpo-cee3p16-1', 'Outlet IEC 60309 16A red 3 phase', 'Industrial outlet, IEC 60309 16A 3 phase (red)', IEC, [('cee3p16', 1, True)], volts=400, amps=16, phase=3,
    circuit={'id': 'A', 'type': 'rcbo', 'amps': 16, 'mA': 30})
gpo('gpo-cee3p32-1', 'Outlet IEC 60309 32A red 3 phase', 'Industrial outlet, IEC 60309 32A 3 phase (red)', IEC, [('cee3p32', 1, True)], volts=400, amps=32, phase=3,
    circuit={'id': 'A', 'type': 'rcbo', 'amps': 32, 'mA': 30})
gpo('gpo-schuko-2', 'Outlet double Schuko', 'Power outlet, double Schuko (Europe, CEE 7/3)', IEC, [('schuko', 2, False)], amps=16)
gpo('gpo-uk-2', 'Outlet twin UK 13A', 'Power outlet, twin switched 13A (UK, BS 1363)', IEC, [('uk', 2, True)], amps=13,
    circuit={'id': 'A', 'type': 'rcbo', 'amps': 32, 'mA': 30}, notes='UK sockets are usually on a 32A ring final circuit.')
gpo('gpo-nema-515-2', 'Duplex receptacle NEMA 5-15R', 'Duplex receptacle, 2 x NEMA 5-15R 15A 120V (North America)', IEC, [('n515', 2, False)], volts=120, amps=15,
    circuit={'id': 'A', 'type': 'mcb', 'amps': 15})
gpo('gpo-nema-520-2', 'Duplex receptacle NEMA 5-20R', 'Duplex receptacle, 2 x NEMA 5-20R 20A 120V (North America)', IEC, [('n520', 2, False)], volts=120, amps=20,
    circuit={'id': 'A', 'type': 'mcb', 'amps': 20})

json.dump(items, open(OUT, 'w'), indent=1)
print(len(items), 'entries ->', OUT)
