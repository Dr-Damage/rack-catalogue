#!/usr/bin/env python3
"""Generates catalogue/riedel.json, clearcom.json and rts.json (intercom and signal transport)."""
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
AA = 'Analog audio'

# ======================= Riedel =======================
RI = lambda *a, **k: add('riedel.json', 'riedel-', 'Riedel', *a, **k)
ART = 'https://www.riedel.net/intercom/artist/'
RI('artist-1024', 'Artist-1024', 'Artist-1024 intercom node', 'Artist', 'audio', 2,
   [F('io', 'Other', 'Card slot', 8, 'SIC bay (UIC-128-II)'), F('io', 'Other', 'Card slot', 2, 'NIC bay'),
    F('io', 'SFP', 'SFP', 4, 'NIC SFP'), F('io', 'Ethernet', 'RJ45', 2, 'NIC Mgmt'), F('io', 'USB', 'USB-C', 2, 'NIC USB'),
    R('in', 'Power', 'IEC', 2, 'PSU-1024')],
   '2RU, 483 x 88 x 404 mm. Front: 8 SIC bays and 2 NIC bays (both take UIC-128-II cards), e-paper display, rotary encoder, air filters. '
   'Each NIC card: 2 SFP slots, 1 RJ45 100/1000BASE-T, 1 USB-C. Each UIC-128-II subscriber card: SFP media slots (AES67, MADI or Dante), '
   'Artist-Fiber, RJ45 management; 8 to 128 ports per card. Rear: 2 hot-swap load-sharing PSU-1024 (225 W each), bays A-D for future use. '
   'Add subscriber card SFPs as extra ports for the cards you fit.', 'Riedel Artist-1024 datasheet', ART)
for code, ru, slots in [('32', 2, 4), ('64', 3, 8), ('128', 6, 16)]:
    RI(f'artist-{code}', f'Artist-{code}', f'Artist-{code} intercom mainframe (discontinued)', 'Artist', 'audio', ru,
       [F('io', 'Other', 'Card slot', slots, 'Client card slot'), R('io', 'Fibre', 'Other', 2, 'Fibre link'), R('in', 'Power', 'IEC', 2, 'PSU')],
       f'{ru}RU legacy Artist mainframe, up to {code} ports on 8-port client cards (AES, analog, MADI, fibre). Discontinued but common in trucks. '
       'Add the client card connectors as extra ports. Check: rack height, slot count, fibre/controller card positions and PSU inlets '
       '(from model naming and dealer listings).', 'Riedel Artist page and dealer listings', 'https://www.riedel.net/intercom/artist/artist-128-64-32/',
       verified=(code == '64'), full=True)
SP = 'https://www.riedel.net/intercom/smartpanels/'
def rsp12(code, ru, keys, depth, kg):
    return [F('io', AA, 'XLR4M', 1, 'Headset'), F('in', AA, '6.3mm jack', 1, 'Mic'), F('io', 'USB', 'USB-A', 1, 'USB'),
            R('io', 'Dante/AES67', 'RJ45', 2, 'ETH 1/2'), R('io', 'Dante/AES67', 'SFP', 2, 'ETH 3/4'), R('io', AA, 'RJ45', 2, '4-wire'),
            R('out', 'Other', 'DB9M', 1, 'GPO (3)'), R('in', 'Other', 'DB9F', 1, 'GPI (3)'), R('io', 'AES/EBU', 'RJ45', 1, 'Artist Matrix'),
            R('io', 'AES/EBU', 'BNC', 1, 'Artist Matrix BNC'), R('io', AA, 'RJ45', 2, 'Headset A/B'), R('io', 'Other', 'RJ45', 1, 'Expansion'),
            R('io', 'Ethernet', 'RJ45', 1, 'Mgmt (future)'), R('out', 'DisplayPort', 'DisplayPort', 1, 'DP (future)'), R('io', 'USB', 'USB-C', 1, 'USB-C'),
            R('in', 'Power', 'IEC', 1, 'AC In')]
RI('rsp-1232hl', 'RSP-1232HL', 'RSP-1232HL SmartPanel 32-key', 'SmartPanel', 'control', 2, rsp12('RSP-1232HL', 2, 32, 138, 3.4),
   '2RU, 483 x 88 x 138 mm, 3.4 kg. 32 lever keys, touch displays, 2 speakers. AES67/ST 2110-30 on 2 RJ45 + 2 SFP (2022-7), 2 analog 4-wire, '
   '3 GPO + 3 GPI on Sub-D9, AES3 Artist matrix port (RJ and BNC), 2 rear headset ports, expansion port for ESP-1216HL. '
   'Check: 4-wire and headset rear connector types (assumed RJ45).', 'Riedel RSP-1232HL datasheet', SP)
RI('rsp-1216hl', 'RSP-1216HL', 'RSP-1216HL SmartPanel 16-key', 'SmartPanel', 'control', 1, rsp12('RSP-1216HL', 1, 16, 138, 2.3),
   '1RU, 483 x 44 x 138 mm, 2.3 kg. 16 lever keys. Same rear I/O as RSP-1232HL. Check: 4-wire and headset rear connector types (assumed RJ45).',
   'Riedel RSP-1216HL datasheet', SP)
RI('esp-1216hl', 'ESP-1216HL', 'ESP-1216HL expansion panel', 'SmartPanel', 'control', 1,
   [R('io', 'Other', 'RJ45', 2, 'Expansion I/O'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU, 138 mm deep, 16 lever keys, 2 displays, up to 6 cascaded on an RSP-1232HL/1216HL. 15 W max.', 'Riedel ESP-1216HL datasheet', SP)
RI('rsp-2318', 'RSP-2318', 'RSP-2318 SmartPanel 18-key', 'SmartPanel', 'control', 1,
   [F('io', AA, 'XLR4M', 1, 'Headset'), F('in', AA, '6.3mm jack', 1, 'Mic'), F('io', 'USB', 'USB-A', 1, 'USB'),
    R('io', 'Dante/AES67', 'RJ45', 2, 'Ethernet AES67/AVB'), R('io', AA, 'RJ45', 2, '4-wire'), R('io', AA, 'RJ45', 2, 'Headset'),
    R('io', 'Other', 'Other', 1, 'GPIO (3 in/3 out)'), R('io', 'Other', 'Other', 1, 'Expansion'), R('io', 'USB', 'USB-A', 1, 'USB'),
    R('out', 'HDMI', 'HDMI', 1, 'HDMI (disabled)'), R('io', 'Other', 'Card slot', 1, 'Option slot (SPX-AES)'),
    R('in', 'Power', 'Other', 1, 'Power In'), R('out', 'Power', 'Other', 1, 'Power Loop Out')],
   '1RU, 446 x 44 x 79 mm installed, 1.7 kg, 3 touch displays, 18 keys, built-in PSU (30 W). AES67/AVB on 2 RJ45, AES3 via SPX-AES option card. '
   'Power loop-through out (6 A) feeds ESP-2324 expansion panels. Check: GPIO and power connector types.', 'Riedel RSP-2318 datasheet', SP)
RI('esp-2324', 'ESP-2324', 'ESP-2324 expansion panel', 'SmartPanel', 'control', 1,
   [R('in', 'Power', 'Other', 1, 'Power In'), R('out', 'Power', 'Other', 1, 'Power Loop Out'), R('in', 'Other', 'Other', 1, 'Expansion In'),
    R('out', 'Other', 'Other', 1, 'Expansion Out')],
   '1RU, 79 mm deep, 24 keys, 4 displays, 5 W, daisy-chained from an RSP-2318. Check: connector types.', 'Riedel ESP-2324 datasheet', SP)
MN = 'https://www.riedel.net/mediornet/'
RI('micron', 'MicroN', 'MediorNet MicroN', 'MediorNet', 'router', 1,
   [R('in', '3G-SDI', 'BNC', 12, 'SDI In'), R('out', '3G-SDI', 'BNC', 12, 'SDI Out'), R('io', 'MADI audio', 'SFP', 2, 'MADI (optical)'),
    R('io', 'Fibre', 'SFP+', 8, '10G Link'), R('io', 'Ethernet', 'RJ45', 1, 'GbE'), R('io', 'Ethernet', 'RJ45', 1, 'Config'),
    R('io', 'Reference', 'BNC', 1, 'Sync In/Out'), R('out', 'Reference', 'BNC', 1, 'Sync Out'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU, 483 x 44 x 241 mm. 12 x 3G-SDI in and out, 2 optical MADI, 8 x 10G SFP+ MediorNet links, GbE, switchable sync in/out plus sync out, '
   'redundant wide-range AC supply. Check: SDI connector type (BNC vs HD-BNC) and which face carries the config port.',
   'Riedel MediorNet MicroN datasheet', MN + 'mediornet-micron/', verified=False, full=True)
RI('micron-uhd', 'MicroN UHD', 'MediorNet MicroN UHD', 'MediorNet', 'router', 1,
   [R('in', '12G-SDI', 'HD-BNC', 8, '12G In'), R('out', '12G-SDI', 'HD-BNC', 8, '12G Out'), R('in', '3G-SDI', 'HD-BNC', 8, '3G In'),
    R('out', '3G-SDI', 'HD-BNC', 8, '3G Out'), R('io', '3G-SDI', 'HD-BNC', 16, '3G In/Out'), R('io', 'Fibre', 'QSFP28', 4, '100G Link'),
    R('io', 'MADI audio', 'SFP', 2, 'MADI'), R('io', 'Ethernet', 'RJ45', 3, 'GbE Tunnel'), R('io', 'Reference', 'HD-BNC', 1, 'Sync In/Out'),
    R('out', 'Reference', 'HD-BNC', 1, 'Sync Out'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU, 48 SDI ports: 8 in + 8 out at 12G, 8 in + 8 out at 3G, 16 switchable 3G. 4 x 100G links (400G), 2 MADI (128 ch), 3 x 1G Ethernet tunnels, '
   'sync reference (black burst, tri-level, word clock). Check: connector types (HD-BNC assumed), link port form factor and PSU count.',
   'Riedel MicroN UHD page and MediorNet brochure', MN + 'mediornet-micron-uhd/', verified=False, full=True)
RI('horizon', 'HorizoN', 'MediorNet HorizoN', 'MediorNet', 'router', 1,
   [R('in', '12G-SDI', 'HD-BNC', 8, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 8, 'SDI Out'), R('io', 'Fibre', 'QSFP28', 4, '100G Link'),
    R('io', 'Fibre', 'QSFP28', 4, '100G IP (2022-7)'), R('io', 'Reference', 'HD-BNC', 1, 'Sync In/Out'), R('out', 'Reference', 'HD-BNC', 1, 'Sync Out'),
    R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU, 478 x 44 x 500 mm, 10 kg, 350 W. 8 x 12G-SDI in and out, 4 x 100G MediorNet links, 4 x 100G ST 2110 IP interfaces (up to 16 x 25GE), '
   'sync (black burst, tri-level, word clock), 2 wide-range AC PSUs. Check: SDI connector type (HD-BNC assumed).', 'Riedel HorizoN page and MediorNet brochure',
   MN + 'mediornet-horizon/', full=True)
RI('metron', 'MetroN', 'MediorNet MetroN core router', 'MediorNet', 'router', 2,
   [R('io', 'Fibre', 'SFP+', 32, '10G Port'), R('io', 'Fibre', 'SFP', 32, '4.25G Port'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'),
    R('io', 'Ethernet', 'RJ45', 1, 'Config'), R('in', 'Reference', 'BNC', 1, 'Sync In'), R('out', 'Reference', 'BNC', 2, 'Sync Out'),
    R('in', 'Power', 'IEC', 2, 'PSU')],
   '2RU MediorNet core: 64 auto-sensing ports (1-32 up to 10G, 33-64 up to 4.25G), 2 Ethernet + config port, 1 sync in / 2 out, '
   'redundant PSUs and fans. Front- or rear-connector versions. Check: sync and power connector types.', 'Riedel MetroN page', MN + 'mediornet-metron/', full=True)
RI('virtu-32', 'VirtU 32', 'MediorNet VirtU 32 processing frame', 'MediorNet', 'converter', 1,
   [R('io', 'SFP', 'SFP', 32, 'MuoN SFP slot'), R('io', 'Fibre', 'QSFP28', 2, '100G Uplink'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU passive frame with 32 processing SFP slots in 8 clusters of 4 (MuoN B SFPs: BNC, fibre or HDMI I/O, gateways, multiviewer), '
   'dual 100/40GE uplinks per cluster, redundant PSU option. Check: uplink count (dual per cluster vs per frame).',
   'Riedel VirtU page and MediorNet brochure', MN + 'mediornet-virtu/', verified=False, full=True)
RI('fusion-bracket', 'FusioN 2RU bracket', 'MediorNet FusioN 2RU bracket', 'MediorNet', 'shelf', 2, [],
   '2RU bracket holding up to 9 FusioN 6B or 18 FusioN 3B miniature SFP frames (3 or 6 SFP slots each, 2 x 25/10GE uplinks). '
   'Add the frames\' SFP and uplink ports as extra ports.', 'Riedel FusioN page', MN + 'mediornet-fusion/', verified=False)
RI('rmk-1002', 'RMK-1002', 'Bolero charger rack kit', 'Bolero', 'shelf', 4, [],
   '19 in 4RU rack kit holding two Bolero 5-bay chargers with a lockable drawer. Add the chargers\' power inlets as extra ports.',
   'Riedel Bolero accessories', 'https://www.riedel.net/produkt/intercom/bolero/accessories/charger-rack-mount-kit-rmk-1002/')

# ======================= Clear-Com =======================
CC = lambda *a, **k: add('clearcom.json', 'cc-', 'Clear-Com', *a, **k)
HX = 'https://clearcom.com/Products/Products-By-Name/Eclipse-HX'
for code, ru, ports, slots, note in [('HX-Delta Lite', 3, '16 or 32', 2, ''), ('HX-Delta', 3, 'up to 416', 4, ''),
                                     ('HX-Median', 6, 'up to 496', 0, ''), ('HX-Omega', 6, 'up to 496', 0, '')]:
    pg = [R('io', AA, 'RJ45', 16 if code == 'HX-Delta Lite' else 32, 'Port (4-wire)')] if code == 'HX-Delta Lite' else []
    if slots: pg.append(R('io', 'Other', 'Card slot', slots, 'Interface card rear'))
    else: pg.append(R('io', 'Other', 'Card slot', 1, 'Interface card rears (see note)'))
    pg += [R('io', 'Ethernet', 'RJ45', 2, 'CPU LAN'), R('io', 'Other', 'Other', 1, 'CPU rear (alarm, matrix links)'),
           R('io', 'Ethernet', 'RJ45', 1, 'LAN/PNL feed-through'), R('in', 'Power', 'DC locking', 2, '12V DC In')]
    CC(code.lower().replace(' ', '-'), f'Eclipse {code}', f'Eclipse {code} matrix frame', 'Eclipse HX', 'audio', ru, pg,
       f'{ru}RU Eclipse HX matrix, {ports} ports. Redundant CPU cards, backplanes and power supplies. '
       + ('Delta: 4 interface card rear slots (2 on Delta Lite), 3 built-in interface module slots, LAN/PNL feed-through, external 12V supplies. '
          if 'Delta' in code else 'Median/Omega take MVX-A16 (16-port analog RJ45), E-IPA, E-MADI64, E-FIB and E-QUE cards. ') +
       'Add interface card rear panels (MVX-A16, E-IPA, E-MADI64, E-FIB) as extra ports. Check: CPU rear connector list and power inlet type'
       + (' (Delta Lite port connector type assumed RJ45).' if code == 'HX-Delta Lite' else '.'),
       'Clear-Com Eclipse HX pages and HX-Delta manual', HX, verified=False, full=True)
CC('arcadia', 'ARCADIA-X4/X5', 'Arcadia central station', 'Arcadia', 'audio', 1,
   [F('io', AA, 'XLR4M', 1, 'Headset'), R('io', AA, 'XLR3F', 4, '2-wire PL'), R('io', AA, 'RJ45', 8, '4-wire'),
    R('io', 'Dante/AES67', 'RJ45', 2, 'LAN 1/2'), R('io', 'Dante/AES67', 'SFP', 2, 'LAN 3/4 (SFP)'), R('io', 'Other', 'RJ45', 2, 'E1 Copper'),
    R('io', 'Fibre', 'SFP', 2, 'E1 Fibre'), R('io', 'Other', 'RJ45', 2, 'DECT Sync In/Out'), R('io', 'Other', 'DB9F', 2, 'GPIO'),
    R('in', AA, 'RJ45', 1, 'Program In / SA Out'), R('in', 'Power', 'IEC', 1, 'AC In'), R('in', 'Power', 'DC locking', 1, '12V DC In')],
   '1RU, 482.6 x 43.6 x 353.8 mm, 3.29 kg. IP central station for HelixNet, FreeSpeak II/Edge, partyline and Dante: 4 x 2-wire XLR, 8 x 4-wire RJ45 '
   '(port 8 = program/SA with split cable), 2 RJ45 + 2 SFP LAN (management, Dante primary/secondary, AES67 for IP transceivers), '
   'E1 transceiver ports (2 RJ45 + 2 fibre, 2 active, up to 10 transceivers), DECT sync in/out, 2 GPIO DB9, internal 160 W PSU on IEC C14 plus '
   '12V DC input from the supplied PSU-EXT-001 for redundancy. X4 = 4-pin XLR-M headset, X5 = 5-pin XLR-F. Licensed 32 to 96 ports.',
   'Clear-Com Arcadia datasheet and online manual', 'https://clearcom.com/Product/arcadia-central-station')
CC('hms-4x', 'HMS-4X', 'HelixNet HMS-4X main station (discontinued)', 'HelixNet', 'audio', 1,
   [F('io', AA, 'XLR4M', 1, 'Headset'), F('io', 'USB', 'USB-A', 1, 'USB'), R('io', AA, 'XLR3', 4, 'Line 1/2 (M+F)'),
    R('in', AA, 'XLR3F', 1, 'Program In'), R('out', AA, 'XLR3M', 1, 'Stage Announce'), R('out', AA, '1/4" TRS', 1, 'Hot Mic'),
    R('io', 'Other', 'DB25F', 1, 'GPIO (4 relay/4 opto)'), R('io', 'Other', 'Card slot', 3, 'Option module'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU, 483 x 320 mm deep, 2.65 kg, 4-channel digital partyline main station. 2 intercom lines each on XLR-3 M and F, program in, '
   'SA out, hot mic out, GPIO DB25, 3 option slots (HLI-ET2 Ethernet, HLI-4W2 4-wire, HLI-2W2 2-wire). Superseded by Arcadia.',
   'Clear-Com HMS-4X datasheet', 'https://www.clearcom.com/Products/Products-By-Name/Station-IC/hms-4x')

# ======================= RTS =======================
RT = lambda *a, **k: add('rts.json', 'rts-', 'RTS', *a, **k)
RT('odin', 'ODIN', 'ODIN digital matrix intercom', 'OMNEO', 'audio', 1,
   [R('io', 'Dante/AES67', 'RJ45', 2, 'OMNEO Pri/Sec'), R('io', AA, 'RJ45', 16, 'AIO 4-wire'), R('io', AA, 'XLR3F', 2, '2-wire PL'),
    R('io', 'Fibre', 'SFP', 4, 'Inter-Frame (2 up/2 down)'), R('io', 'Other', 'RJ45', 1, 'PAP/LCP/GPIO'), R('io', 'Other', 'Other', 1, 'GPIO (4 relay/4 opto)'),
    R('io', 'Ethernet', 'RJ45', 1, 'Control'), R('io', 'Ethernet', 'RJ45', 1, 'Front Panel Mgmt'), R('in', 'Reference', 'BNC', 1, 'Sync In'),
    R('in', 'Power', 'IEC', 2, 'PSU')],
   '1RU, 482.6 x 43.7 x 363.5 mm, 5.2 kg, 47 W. 16 to 128 licensed ports per frame, up to 8 frames (1024 ports). OMNEO (Dante) primary/secondary on '
   'RJ45 or optional SFP, 16 analog 4-wire RJ45, 2 partyline XLR, 4 inter-frame SFP, GPIO, BNC sync, 2 redundant load-sharing PSUs on locking IEC C14. '
   'Check: GPIO connector type.', 'RTS ODIN technical data sheet (Rev 08, 2023)', 'https://products.rtsintercoms.com/r/odin')
for code, ru, keys, h in [('KP-5032', 2, 32, 87.96), ('KP-4016', 1, 16, 43.8)]:
    RT(code.lower(), code, f'{code} OMNEO keypanel', 'KP-Series', 'control', ru,
       [F('io', AA, 'XLR5F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Panel Mic'), R('io', 'Dante/AES67', 'RJ45', 2, 'OMNEO'),
        R('io', AA, 'RJ45', 1, 'Analog Matrix'), R('io', AA, 'Other', 1, 'Headset (rear)'), R('in', AA, 'Other', 2, 'Aux In'),
        R('out', AA, 'Other', 1, 'Speaker Out'), R('io', 'Other', 'Other', 1, 'GPIO/RC'), R('in', 'Power', 'DC locking', 1, 'DC In')],
       f'{ru}RU ({h} mm high, 98.5 mm deep), {keys} lever keys with HD colour displays. OMNEO (Dante) IP plus analog matrix connection, '
       'aux 1/2 balanced inputs, rear headset and speaker, GPIO (SPDT relays, opto inputs) and RC standard, external DC supply. '
       f'Headset 5-pin XLR (4-pin option). Up to {6 if keys == 32 else 7} expansion panels. '
       'Check: rear connector counts and types (RTS lists features, not counts).', f'RTS {code} product page and KP-Series brochure',
       f'https://products.rtsintercoms.com/na/en/{code.lower()}', verified=False)

# ---- RTS / RTS Telex matrix frames, legacy keypanels, TW (added 2026-11-11) ----
RT('adam', 'ADAM', 'ADAM digital matrix intercom frame', 'ADAM', 'audio', 7,
   [F('io', 'Other', 'Card slot', 17, 'AIO slot'), F('io', 'Other', 'Card slot', 2, 'Master controller'),
    R('io', 'Other', 'Back card', 17, 'Back card'), R('io', 'Ethernet', 'RJ45', 1, 'AZedit (MCII-e)'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '7RU, 19 x 20 in deep. 17 front AIO slots, 2 master controller slots, 1 blank; redundant universal PSUs 100-240 V AC, 700 VA. '
   'Up to 512 ports per frame with MADI/OMNEO cards (8 to 880 per system). Rear interface cards: AIO-16A, MADI-16, OMI, RVON; '
   'cabling via RJ11, RJ45, DB9 or XCP breakout panels. Add each back card\'s connectors as extra ports. '
   'Check: rear connector counts and controller Ethernet position.', 'RTS ADAM product page', 'https://products.rtsintercoms.com/r/adam-2',
   verified=False, full=True)
RT('adam-m', 'ADAM-M', 'ADAM-M mid-size modular matrix intercom', 'ADAM', 'audio', 3,
   [F('io', 'Other', 'Card slot', 8, 'Interface card'), F('io', 'Other', 'Card slot', 2, 'Master controller'),
    R('io', 'Other', 'Back card', 8, 'Back card'), R('io', 'Ethernet', 'RJ45', 1, 'AZedit'), R('in', 'Power', 'IEC', 2, 'PSU')],
   '3RU, 8 interface cards (AIO-16A etc.) plus redundant master controllers and power supplies, 90-264 V AC. 128 ports per frame, '
   '512 expanded (OMNEO). Fibre trunking single or multi-mode; external GPIO-16 for GPI. Add each back card\'s connectors as extra ports. '
   'Check: rear connector counts.', 'RTS ADAM-M product page and RTS matrix brochure', 'https://products.rtsintercoms.com/na/en/adam-m',
   verified=False, full=True)
RT('cronus', 'Cronus', 'Cronus 32-port digital matrix intercom', 'Cronus', 'audio', 2,
   [F('io', 'Other', 'Card slot', 4, 'AIO / RVON-C slot'), R('io', 'Other', 'Back card', 4, 'Backcard (RJ-12 or MDR)'),
    R('io', 'Other', 'BNC', 2, 'Frame link A/B (coax)'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB', 1, 'USB'),
    R('in', 'Power', 'IEC', 2, 'PSU')],
   '2RU, 32 ports on up to 4 AIO or RVON-C cards (8 ports each), backcards RJ-12 or MDR (break out to XCP-48-RJ45, XCP-32-DB9 or '
   'XCP-48-Telco panels). Up to 4 frames linked (128 ports) over coax links A/B or optional SC fibre. Redundant power. 4 relays. '
   'Check: connector counts (from the user manual, which does not tabulate them).', 'RTS Cronus user manual and RTS matrix brochure',
   'https://www.manualslib.com/manual/808509/Rts-Cronus.html', verified=False)
for code, n, ru_note in [('Zeus III', 32, ''), ('Zeus III LE+', 16, ' LE+ is the 16-port version.')]:
    RT(code.lower().replace(' ', '-').replace('+', 'plus'), code, f'{code} digital matrix intercom, {n} ports', 'Zeus', 'audio', 1,
       [R('io', AA, 'RJ45', n, 'Port'), R('io', AA, 'XLR3', 2, 'Party line'), R('io', 'RS-422', 'DB9', 1, 'Trunk (RS485)'),
        R('io', 'Other', 'Other', 1, 'Peripheral (RS485)'), R('io', 'Other', 'Other', 1, 'PC (RS232)'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
        R('out', 'Other', 'Other', 2, 'Relay'), F('io', 'USB', 'USB', 1, 'USB (AZedit)'), R('in', 'Power', 'IEC', 2, 'AC In')],
       f'1RU, 44 x 415.8 x 381 mm, 3.18 kg. {n} RJ45 keypanel/4-wire ports plus 2 configurable party line channels, DB9 RS485 trunk, '
       'RS485 peripheral port (UIO-256, LCP-102), RS232, 10/100 Ethernet, 2 relays, front USB for AZedit, two independent AC supplies '
       f'(90-264 V) on separate feeds.{ru_note} Check: party line, peripheral, RS232 and relay connector types.',
       'RTS Zeus III technical data sheet', 'https://www.fullcompass.com/common/files/13743-ZEUSIIITechnicalDataSheet.pdf',
       verified=(n == 32))
RT('kp-32', 'KP-32', 'KP-32 legacy 32-key keypanel', 'KP-Series (legacy)', 'control', 2,
   [F('io', AA, 'XLR4', 1, 'Headset'), R('io', AA, 'DB9', 1, 'Matrix'), R('io', 'Other', 'Other', 1, 'Expansion (EPAP)'),
    R('in', 'Power', 'IEC', 1, 'AC In')],
   'Legacy RTS Telex 32-key rackmount keypanel with per-key alphanumeric displays (KP-32, KP-632, KP-832 variants); takes EPAP-32 '
   'expansion panels (20 keys each, up to 2). Optional RVON-1 card adds RJ45 VoIP. Check: rack height (sources disagree, 1RU or 2RU), '
   'matrix connector (DB9 or RJ) and power inlet.', 'RTS EPAP-32 page and KP-32 dealer listings', 'https://www.manualslib.com/manual/327219/Rts-Kp-32.html',
   verified=False)
RT('epap-32', 'EPAP-32', 'EPAP-32 20-key expansion panel', 'KP-Series (legacy)', 'control', 2,
   [R('io', 'Other', 'Other', 1, 'Expansion link')],
   '2RU (88.9 x 482.6 mm), adds 20 keys to a KP-32 / KP-632 / KP-832 / PAP-32; up to 2 per station (52 keys in 3RU per RTS). '
   'Pushbutton or lever keys, black or grey. Check: link connector.', 'RTS EPAP-32 product page', 'https://products.rtsintercoms.com/na/en/epap-32',
   verified=False)
RT('ps-20', 'PS-20', 'PS-20 two-channel TW intercom power supply', 'TW', 'power', 1,
   [F('out', AA, 'XLR3', 1, 'Monitor'), R('io', AA, 'XLR3M', 4, 'TW line'), R('in', AA, 'XLR3F', 1, 'Program In'),
    R('in', AA, '6.3mm TRS', 1, 'Audio link In'), R('out', AA, '6.3mm TRS', 1, 'Audio link Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU half-rack (207.9 mm wide), 90-264 V AC, 28-32 V DC out, about 2 A per channel. Powers 2 wet TW channels (RTS 2-channel, '
   'RTS 4-channel or Clear-Com mode), selectable 200/400 ohm termination. Four rear XLR3M TW outputs, program XLR3F, two 6.3 mm link '
   'jacks to a second PS-20, front monitor XLR. Mount with an RMK-S / RMK-D (MCP-style) rack kit.',
   'RTS PS-20 spec sheet and Canford listing', 'https://www.fullcompass.com/common/files/10335-RTSPS20SpecSheet.pdf', w=6)
RT('ssa-324', 'SSA-324', 'SSA-324 two-wire to four-wire interface', 'TW', 'audio', 1,
   [F('io', AA, 'XLR4F', 1, 'Headset'), R('io', AA, 'XLR3', 2, 'TW (2-wire)'), R('in', AA, 'XLR3F', 2, '4-wire In'),
    R('out', AA, 'XLR3M', 2, '4-wire Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '1RU half-rack, 208 x 204 mm deep. Two TW channels to 4-wire (or one 2-wire to 2-wire), call signalling, front XLR4F headset. '
   'Mains 120 V (P option 230 V). Check: rear connector counts and types (spec sheet does not list them).',
   'RTS SSA-324 spec sheet', 'https://www.fullcompass.com/common/files/4374-SSA324SpecSheet.pdf', verified=False, w=6)

# ---- RTS legacy rack units from the RTS CAD drawing set (products.rtsintercoms.com downloads, DWF front drawings) ----
# Rack height and width come from the drawings (2RU full width, or 1RU half-rack at 8.5 in). The DWFs show fronts only,
# so rear connectors are typical for the family and marked unverified.
DWF = 'RTS CAD drawing (DWF front view)'; DWFURL = 'https://products.rtsintercoms.com/na/en/downloads'
KPREAR = lambda: [F('io', AA, 'XLR4F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Panel mic'), R('io', AA, 'DB9', 1, 'Matrix'),
                  R('io', 'Other', 'Other', 1, 'Expansion'), R('in', 'Power', 'IEC', 1, 'AC In')]
for code, name, extra in [
        ('KP-632', 'KP-632 32-key keypanel (legacy)', 'Two rows of 16 lever keys with 8-character alphanumeric displays, keypad, volume, front mic and headset.'),
        ('KP-832', 'KP-832 32-key keypanel (legacy)', 'Two rows of 16 lever keys with 8-character alphanumeric displays, keypad, volume, front mic and headset.'),
        ('KP-32/16', 'KP-32/16 16-key keypanel (legacy)', 'The 16-key version of the KP-32: one block of lever keys with displays, keypad, front mic and headset.'),
        ('KP-32 CLD', 'KP-32 CLD 32-key colour display keypanel', '32 keys with colour LCD labels, front mic and headset, USB and menu keys.'),
        ('PAM-32', 'PAM-32 32-key panel with headset (legacy)', '32 lever keys with alphanumeric displays, keypad and a front headset jack.'),
        ('EKP-32', 'EKP-32 32-key expansion panel (legacy)', 'Adds 32 lever keys with displays to a KP-32 family keypanel.')]:
    ports = KPREAR() if code != 'EKP-32' else [R('io', 'Other', 'Other', 1, 'Expansion link')]
    RT(code.lower().replace('/', '-').replace(' ', '-'), code, name, 'KP-Series (legacy)', 'control', 2, ports,
       f'2RU full width (from the RTS drawing). {extra} Check: rear connectors (the drawing shows the front only).', DWF, DWFURL, verified=False)
RT('arp-32', 'ARP-32', 'ARP-32 32-key router control panel (legacy)', 'KP-Series (legacy)', 'control', 2,
   [R('io', 'Other', 'DB9', 1, 'Matrix data'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '2RU full width (from the RTS drawing). Inputs and outputs rows of lever keys with displays and IN/OUT keypad for routing on the matrix. '
   'Check: function name and rear connectors.', DWF, DWFURL, verified=False)
RT('pap-32', 'PAP-32', 'PAP-32 program assign panel (legacy)', 'KP-Series (legacy)', 'control', 2,
   [R('io', 'Other', 'DB9', 1, 'Matrix data'), R('io', 'Other', 'Other', 1, 'Expansion'), R('in', 'Power', 'IEC', 1, 'AC In')],
   '2RU full width (from the RTS drawing). Program source and IFB destination key rows with displays and SRC/DEST keypad. '
   'PAP-32LK has lever keys, PAP-32PB pushbuttons; takes EPAP-32 expansion. Check: rear connectors.', DWF, DWFURL, verified=False)
HALF = '1RU half-rack (8.5 in, from the RTS drawing)'
RT('mkp-4', 'MKP-4', 'MKP-4 4-key keypanel', 'KP-Series (legacy)', 'control', 1,
   [F('io', AA, 'XLR4F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Mic'), R('io', AA, 'DB9', 1, 'Matrix'), R('in', 'Power', 'IEC', 1, 'AC In')],
   f'{HALF}. 4 listen/talk keys with a display, call waiting, copy/clear, front mic and headset XLR, volume. Check: rear connectors.',
   DWF, DWFURL, verified=False, w=6)
RT('tif-2000a', 'TIF-2000A', 'TIF-2000A digital telephone interface', 'Interfaces', 'audio', 1,
   [R('io', AA, 'Other', 1, 'Telephone line'), R('io', AA, 'Other', 1, 'Matrix (4-wire)'), R('in', 'Power', 'IEC', 1, 'AC In')],
   f'{HALF}. Telephone hybrid with level meters to matrix and to telephone, drop/seize/auto-answer. Check: rear connectors.',
   DWF, DWFURL, verified=False, w=6)
RT('dsi-2008', 'DSI-2008', 'DSI-2008 dual 2-wire / 4-wire interface', 'Interfaces', 'audio', 1,
   [R('io', AA, 'XLR3', 2, '2-wire (System A/B)'), R('io', AA, 'Other', 2, '4-wire (System A/B)'), R('in', 'Power', 'IEC', 1, 'AC In')],
   f'{HALF}. Two systems (A and B) with to-4W and to-2W level meters, 2W channel select and 4W level reference. '
   'Check: function name and rear connectors.', DWF, DWFURL, verified=False, w=6)
RT('csi-200', 'CSI-200', 'CSI-200 two-channel interface', 'Interfaces', 'audio', 1,
   [R('io', 'Other', 'Other', 2, 'Channel A/B'), R('in', 'Power', 'IEC', 1, 'AC In')],
   f'{HALF}. Channels A and B with TX/RX indicators, frame or keypanel mode, reset. Check: function and rear connectors.',
   DWF, DWFURL, verified=False, w=6)
for code, name, extra in [('MCE-325', 'MCE-325 TW user station', 'Two channels (talk/listen, call, panel mic, speaker), channel volumes, '
                                                                    'program volume, dynamic-mic headset XLR and carbon-mic headset jack.'),
                          ('MRT-327', 'MRT-327 TW user station', 'Channel 1-2 select, call, panel mic, speaker and mic on keys, volume, sidetone, '
                                                                    'dynamic-mic headset XLR.')]:
    RT(code.lower(), code, name, 'TW', 'audio', 1,
       [F('io', AA, 'XLR4F', 1, 'Headset'), R('io', AA, 'XLR3', 2, 'TW line'), R('in', 'Power', 'IEC', 1, 'AC In')],
       f'{HALF}. {extra} Check: rear connectors.', DWF, DWFURL, verified=False, w=6)
RT('ps-15', 'PS-15', 'PS-15 TW intercom power supply', 'TW', 'power', 1,
   [R('io', AA, 'XLR3M', 2, 'TW line'), R('in', 'Power', 'IEC', 1, 'AC In')],
   f'{HALF}. Powers RTS TW party-line channels. Check: channel count and rear connectors.', DWF, DWFURL, verified=False, w=6)
for code, name in [('LMS-325', 'LMS-325 loudspeaker'), ('MCS-325', 'MCS-325 speaker')]:
    RT(code.lower(), code, name, 'TW', 'audio', 1, [R('in', AA, 'Other', 1, 'Audio In'), R('in', 'Power', 'IEC', 1, 'AC In')],
       f'{HALF}. Rack monitor loudspeaker{" with front volume" if code == "LMS-325" else ""}. Check: input and power connectors.',
       DWF, DWFURL, verified=False, w=6)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids))
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(idx)
