#!/usr/bin/env python3
"""More RTS intercom (added 2026-11-15) -> catalogue/rts-more.json. rts.json stays with tools/comms.py, which now draws ADAM, ADAM-M and
Cronus as card frames (systems 'RTS ADAM', 'RTS ADAM-M', 'RTS Cronus').
  Cards: AIO-16A / AIO-16 with SCSI, MDR or RJ-45 back cards, MADI-16 Plus, OMI (OMNEO), RVON-16, MCII-e controller, TBX Tribus expander;
         Cronus AIO (RJ-12 or MDR back card) and RVON-C.
  XCP breakout panels for the AIO back cards and the controller, so matrix ports can be wired through to keypanels.
  Rack units: KP-3016/3016A and expansion panels, RP-1000/RP-1932, KP-12 CLD, KP-12, EKP-20, MKP-12, PAM-16, PAP-5032, level control panels,
         RVON-I/O, GPIO-16, UIO-256, IFB-828, 4010, TM-10K trunk master with ICP-2000 and SWP-2000, TIF-4000, SIP-ISDN, SAP-1626,
         RM-325, BOP-220.
A matrix port (keypanel or 4-wire) is drawn as type 'Analog audio'; multipins name the port count, e.g. 'SCSI 50-pin (8 ports)'.
Sources: RTS matrix brochure (avbroadcast.fr copy), KP-Series brochure, AIO-16 and RVON-I/O manuals (manualslib), Markertek AIO-16A listing,
the RTS DWF front drawings for rack heights. Most rear connector types are not published, so those entries are verified=False with "Check:"."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
AA = 'Analog audio'; OUT = []
BRO = ('RTS digital matrix brochure', 'https://www.avbroadcast.fr/media/productfile/r/t/rts-matrices-intercom-digitales.pdf')
KPB = ('RTS KP-Series brochure', 'https://www.avbroadcast.fr/media/productfile/r/t/rts-serie-kp-brochure.pdf')
DWF = ('RTS CAD drawing (DWF front view) and RTS matrix brochure', 'https://products.rtsintercoms.com/na/en/downloads')
def unit(id, pn, name, fam, cat, ru, ports, notes, src, verified=False, w=12, full=False, **kw):
    m = dict(id='rts-' + id, manufacturer='RTS', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src[0], productUrl=src[1], notes=notes, portGroups=ports)
    m.update(kw); OUT.append(m)
def bc(pn, name, ports, default=False): return dict(partNumber=pn, name=name, width=1, cardsPerModule=1, cardOffset=0, default=default, included=False, portGroups=ports)
def card(id, pn, name, fits, notes, src, backs, watts=None, color=None, verified=False, front=()):
    c = dict(fits=fits, slotWidth=1)
    if watts: c['watts'] = watts
    if color: c['color'] = color
    unit(id, pn, name, 'ADAM cards' if 'RTS ADAM' in fits or 'RTS ADAM-M' in fits else 'Cronus cards', 'card', 0, list(front), notes, src,
         verified=verified, w=0, card=c, rearModules=backs)

# ======================= ADAM / ADAM-M cards =======================
SCSI = lambda: bc('AIO-16 SCSI back card', 'SCSI back card (2 x 50-pin SCSI)', [R('io', AA, 'SCSI 50-pin (8 ports)', 2, 'Ports')], True)
MDR = lambda: bc('AIO-16 MDR back card', 'MDR back card (2 x 50-pin MDR)', [R('io', AA, 'MDR 50-pin (8 ports)', 2, 'Ports')])
RJ = lambda: bc('AIO-16 RJ-45 back card', 'RJ-45 back card (ADAM-M only)', [R('io', AA, 'RJ45', 16, 'Port')])
AIO_NOTE = ('Ports {} on each frame are fixed by slot. Back card (ordered separately): 50-pin SCSI (to XCP-40-DB9, XCP-40-RJ12, XCP-24, '
            'XCP-24-USOC, XCP-955), 50-pin MDR (separate data driver per keypanel; to XCP-32-DB9, XCP-16-DB9-T, XCP-48-RJ45) or RJ-45 (ADAM-M only). '
            'Each 50-pin connector carries 8 ports.')
card('aio-16a', 'AIO-16A', 'AIO-16A 16-port analog I/O card (ADAM, ADAM-M)', ['RTS ADAM', 'RTS ADAM-M'],
     '16 analog 4-wire intercom ports per card, up to 17 per ADAM. Hot-swap, detects the back card, drop-in replacement for the AIO-16. '
     + AIO_NOTE.format('1-16'), ('RTS AIO-16A listing (Markertek)', 'https://markertek.com/product/rts-aio-16a/rts-aio-16a-16-channel-standard-omi-input-output-frontcard-for-adam-or-adam-m-matrix-intercom-frames-no-led'),
     [SCSI(), MDR(), RJ()], verified=True)
card('aio-16', 'AIO-16', 'AIO-16 16-port analog I/O card (legacy)', ['RTS ADAM', 'RTS ADAM-M'],
     'Earlier 16-port AIO card (9000-7726-001 with LED front). Same back cards as the AIO-16A. ' + AIO_NOTE.format('1-16'),
     ('RTS AIO-16 user manual (manualslib)', 'https://www.manualslib.com/manual/327125/Rts-Aio-16.html'), [SCSI(), MDR(), RJ()])
card('madi-16-plus', 'MADI-16 Plus', 'MADI-16 Plus MADI interface card, 16-64 ports', ['RTS ADAM', 'RTS ADAM-M'],
     'AES10 MADI card, 16 to 64 ports at 44.1/48 kHz, coax or fibre back card. In an ADAM-M it goes in slot 8. Check: back card connectors.',
     BRO, [bc('MADI-16 coax back card', 'Coax back card', [R('in', 'MADI', 'BNC', 1, 'MADI In'), R('out', 'MADI', 'BNC', 1, 'MADI Out')], True),
           bc('MADI-16 fibre back card', 'Fibre back card', [R('io', 'MADI', 'SC duplex', 1, 'MADI fibre')])])
card('omi', 'OMI', 'OMI OMNEO matrix interface card, 16-64 ports', ['RTS ADAM', 'RTS ADAM-M'],
     'OMNEO (Dante / AES67) IP audio card for ADAM and ADAM-M, 16 to 64 ports. Back card: 2 RJ45 plus 1 LC SFP. 14.9 W front and back.',
     BRO, [bc('OMI back card', 'OMI back card', [R('io', 'Dante/AES67', 'RJ45', 2, 'OMNEO'), R('io', 'Dante/AES67', 'SFP', 1, 'OMNEO fibre')], True)],
     watts=14.9, verified=True)
card('rvon-16', 'RVON-16', 'RVON-16 16-port VoIP card (ADAM)', ['RTS ADAM', 'RTS ADAM-M'],
     'RTS Voice Over Network card: 16 VoIP ports to RVON keypanels and RVON-I/O. Check: back card connectors (one RJ45 shown).',
     BRO, [bc('RVON-16 back card', 'RVON back card', [R('io', 'Ethernet', 'RJ45', 1, 'Network')], True)])
card('mcii-e', 'MCII-e', 'MCII-e master controller card (ADAM, ADAM-M)', ['RTS ADAM', 'RTS ADAM-M'],
     'Ethernet master controller. Fit two (main and backup) with matching DIP switches. Back card J1 Ethernet to AZedit, J2 to J12 on the '
     'XCP-ADAM-MC breakout panel (RS-232, trunking and peripheral RS-485, GPI). Check: J2 connector type.',
     ('RTS MCII-e user manual and ADAM-M installation manual (manualslib)', 'https://www.manualslib.com/manual/327257/Rts-Mcii-E.html'),
     [bc('MCII-e back card', 'Controller back card', [R('io', 'Ethernet', 'RJ45', 1, 'J1 Ethernet (AZedit)'), R('io', 'Other', 'Multipin', 1, 'J2 to XCP-ADAM-MC')], True)])
card('tbx-tribus', 'TBX-Tribus', 'TBX Tribus bus expander card', ['RTS ADAM', 'RTS ADAM-M'],
     'Triple-bus expander linking up to 4 ADAM frames over dual fibre ring or mesh. In an ADAM-M the TBX cards go in slots 4-6 (then only one '
     'MADI card fits). Check: fibre connector type.', BRO,
     [bc('TBX back card', 'TBX fibre back card', [R('io', 'Fibre', 'Other', 2, 'Bus link')], True)])

# ======================= Cronus cards =======================
card('cronus-aio', 'Cronus AIO', 'Cronus AIO 8-port analog I/O card', ['RTS Cronus'],
     '8 analog 4-wire intercom ports. RJ-12 back card (8 jacks) or MDR back card (one 50-pin MDR, to XCP-48-RJ45, XCP-32-DB9, XCP-48-Telco).', BRO,
     [bc('Cronus RJ-12 back card', 'RJ-12 back card', [R('io', AA, 'RJ12', 8, 'Port')], True),
      bc('Cronus MDR back card', 'MDR back card', [R('io', AA, 'MDR 50-pin (8 ports)', 1, 'Ports')])])
card('rvon-c', 'RVON-C', 'RVON-C 8-port VoIP card (Cronus)', ['RTS Cronus'],
     'RTS Voice Over Network card for Cronus: 8 VoIP ports. Check: back card connectors (one RJ45 shown).', BRO,
     [bc('RVON-C back card', 'RVON back card', [R('io', 'Ethernet', 'RJ45', 1, 'Network')], True)])

# ======================= XCP breakout panels =======================
AIOM = ('RTS AIO-16 user manual and matrix brochure', 'https://www.manualslib.com/manual/327125/Rts-Aio-16.html')
for pn, ru, src_conn, n_in, out_conn, n_out, extra in (
        ('XCP-40-DB9', 2, 'SCSI 50-pin (8 ports)', 5, 'DB9', 40, 'For AIO SCSI back cards.'),
        ('XCP-40-RJ12', 1, 'SCSI 50-pin (8 ports)', 5, 'RJ12', 40, 'For AIO SCSI back cards (also written XCP-40-RJ11).'),
        ('XCP-32-DB9', 2, 'MDR 50-pin (8 ports)', 4, 'DB9', 32, 'For AIO and Cronus MDR back cards; also works with AIO-8.'),
        ('XCP-16-DB9-T', 1, 'MDR 50-pin (8 ports)', 2, 'DB9', 16, 'For MDR back cards, with audio isolation transformers.'),
        ('XCP-48-RJ45', 1, 'MDR 50-pin (8 ports)', 6, 'RJ45', 48, 'For AIO and Cronus MDR back cards (MDR back card required).')):
    unit(pn.lower(), pn, f'{pn} breakout panel, {n_out} x {out_conn} from {n_in} x {src_conn.split(" (")[0]}', 'XCP breakout panels', 'patch', ru,
         [R('io', AA, src_conn, n_in, 'Card link'), R('io', AA, out_conn, n_out, 'Port')],
         f'Breaks the matrix back card multipins out to one {out_conn} per intercom port (keypanel or 4-wire). {extra} '
         'Check: rack height and which face the connectors are on (all shown on the rear).', AIOM)
unit('xcp-adam-mc', 'XCP-ADAM-MC', 'XCP-ADAM-MC master controller breakout panel', 'XCP breakout panels', 'patch', 1,
     [R('io', 'Other', 'Multipin', 1, 'J12 to MCII-e'), R('io', 'RS-232', 'DB9', 1, 'J1 PC (RS-232)'), R('io', 'RS-422', 'DB9', 1, 'J2 Trunk (RS-485)'),
      R('io', 'RS-422', 'DB9', 1, 'J3 PAP / UIO-256 / GPIO-16 (RS-485)'), R('io', 'Other', 'DB9', 7, 'Aux'), R('io', 'GPIO', 'DB25', 1, 'GPIO')],
     'Breaks the MCII-e controller back card out to the AZedit PC (RS-232), trunk master (RS-485), PAP/UIO-256/GPIO-16 peripherals and GPI. '
     'The brochure lists 10 DB9 and 1 DB25. Check: rack height and the use of J4-J10.', ('RTS MC-ADAM and ADAM-M installation manuals', 'https://www.manualslib.com/manual/327249/Rts-Mc-Adam.html'))

# ======================= Keypanels =======================
def kp(id, pn, name, ru, keys, notes, src, omneo=True, depth=None, w=None, verified=False):
    ports = [F('io', AA, 'XLR5F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Panel mic')]
    if omneo: ports.append(R('io', 'Dante/AES67', 'RJ45', 2, 'OMNEO'))
    ports += [R('io', AA, 'RJ45', 1, 'Analog matrix'), R('io', 'Other', 'Other', 1, 'Expansion'), R('in', 'Power', 'DC locking', 1, 'DC In')]
    unit(id, pn, name, 'KP-Series', 'control', ru, ports, notes, src, verified=verified, **({'depthMm': depth} if depth else {}), **({'powerW': w} if w else {}))
for pn, omneo, w in (('KP-3016', True, 11), ('KP-3016A', False, 8)):
    kp(pn.lower(), pn, f'{pn} 16-key keypanel, 1RU' + ('' if omneo else ' (analog only)'), 1, 16,
       f'Entry-level 1RU keypanel, 16 lever keys with full-colour HD displays, 98 mm deep (110 mm with keys), 1.5 kg. '
       + ('OMNEO (IP) and 4-wire analog matrix connection. ' if omneo else 'Analog 4-wire matrix connection only. ')
       + f'External 100-240 V supply, {w} W. User-replaceable headset XLR, 4 or 5-pin (KP-3016-A4F = 4-pin). Takes EKP-3016 expansion. '
       'Check: rear connector counts.', ('RTS KP-3016 data sheet (LA-BS copy)', 'https://www.la-bs.com/ObjetsMultimedia/57360/FR/KP-3016_RTS-INTERCOM_dt.pdf'),
       omneo=omneo, depth=98, w=w)
for pn, ru, keys, host in (('EKP-3016', 1, 16, 'KP-3016 / KP-3016A'), ('EKP-4016', 1, 16, 'KP-4016 / KP-5032 (up to 7 / 6 per panel)')):
    unit(pn.lower(), pn, f'{pn} 16-key expansion panel, 1RU', 'KP-Series', 'control', ru, [R('io', 'Other', 'Other', 1, 'Expansion link'), R('in', 'Power', 'DC locking', 1, 'DC In')],
         f'1RU expansion panel, 16 lever keys with HD colour displays, for the {host}. -PB versions have pushbuttons. Check: link and power connectors.', KPB)
unit('pap-5032', 'PAP-5032', 'PAP-5032 16-position IFB router panel, 2RU', 'KP-Series', 'control', 2,
     [R('io', 'Dante/AES67', 'RJ45', 2, 'OMNEO'), R('in', 'Power', 'DC locking', 1, 'DC In')],
     '2RU program assign panel: routes program sources to 16 IFB destinations, KP-5032 style keys and displays. Check: rear connectors.', KPB)
unit('rp-1000', 'RP-1000', 'RP-1000 32-key colour keypanel, 2RU', 'KP-Series (legacy)', 'control', 2,
     [F('io', AA, 'XLR5F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Panel mic'), R('io', AA, 'RJ45', 1, 'Matrix'), R('io', 'Other', 'Other', 1, 'RC connector kit'),
      R('io', 'Other', 'Other', 1, 'OKI / RVON-2 slot'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '2RU, 32 keys with colour TFT displays, 83 mm deep, 2.9 kg. Rear connector kit: 6 aux, 3 relays, 4 opto inputs, 2 OC outputs. '
     'Optional OKI card (2 RJ45 + LC SFP, OMNEO) or RVON-2. RP-1932 is its 2RU colour expansion panel. Check: matrix and power connectors.', BRO, depthMm=83)
unit('rp-1932', 'RP-1932', 'RP-1932 colour expansion panel for RP-1000, 2RU', 'KP-Series (legacy)', 'control', 2,
     [R('io', 'Other', 'Other', 1, 'Expansion link')], '2RU colour expansion panel for the RP-1000, 2.9 kg. Check: link connector and key count.', BRO)
unit('kp-12-cld', 'KP 12 CLD', 'KP 12 CLD 12-key colour keypanel, 1RU', 'KP-Series (legacy)', 'control', 1,
     [F('io', AA, 'XLR5F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Panel mic'), R('io', AA, 'RJ45', 1, 'Matrix'), R('io', 'Other', 'Other', 1, 'RC connector kit'),
      R('io', 'Other', 'Other', 1, 'OKI / RVON-2 slot'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 12 keys with colour displays, 109 mm deep, 1.7 kg. Rear connector kit (KP 12 CLD RC): 3 aux, 3 relays, 4 opto inputs, 2 OC outputs. '
     'Optional OKI (OMNEO) or RVON-2 card. Check: matrix and power connectors.', BRO, depthMm=109)
unit('kp-12', 'KP-12', 'KP-12 12-key keypanel, 1RU (legacy)', 'KP-Series (legacy)', 'control', 1,
     [F('io', AA, 'XLR5F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Mic'), R('io', AA, 'DB9', 1, 'Matrix'), R('io', 'Other', 'Other', 2, 'KPM option modules'),
      R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 12 lever keys with displays, 140 mm deep, 2.3 kg (KP-12LK lever keys, KP-12PB pushbuttons). Option modules: KPM-CK (mic in/out, line in, '
     'headset, speaker) and KPM-I/O (4 opto, 2 OC, 2 relays). EKP-20 adds 20 keys. Check: rear connectors.', DWF, depthMm=140)
unit('ekp-20', 'EKP-20', 'EKP-20 20-key expansion panel, 1RU (legacy)', 'KP-Series (legacy)', 'control', 1,
     [R('io', 'Other', 'Other', 1, 'Expansion link')], '1RU, 20 keys with displays (EKP-20LK lever, EKP-20PB pushbutton), 181 mm deep, 2.1 kg. Check: link connector.', DWF, depthMm=181)
unit('mkp-12', 'MKP-12', 'MKP-12 12-key value keypanel, 1RU', 'KP-Series (legacy)', 'control', 1,
     [F('io', AA, 'XLR4F', 1, 'Headset'), F('in', AA, 'Other', 1, 'Mic'), R('io', AA, 'DB9', 1, 'Matrix'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU value-series keypanel, 12 keys, 203 mm deep, 2.3 kg. Check: rear connectors.', DWF, depthMm=203)
unit('pam-16', 'PAM-16', 'PAM-16 16-key program audio monitor, 1RU', 'KP-Series (legacy)', 'control', 1,
     [F('io', AA, 'XLR4F', 1, 'Headset'), R('io', AA, 'DB9', 1, 'Matrix'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU program audio monitor panel with 16 monitor keys, 2 kg. PAM-32 is the 2RU version. Check: rear connectors.', DWF)
for pn, ru, keys, desc in (('LCP-12', 1, 12, '12 level controls'), ('LCP-20', 1, 20, '20 level controls'), ('LCP-32/16', 1, 16, '16 level controls, 44 mm deep')):
    unit(pn.lower().replace('/', '-'), pn, f'{pn} level control panel, 1RU', 'Level control', 'control', ru,
         [R('io', 'Other', 'Other', 1, 'Matrix data'), R('in', 'Power', 'Other', 1, 'Power')],
         f'1RU level control panel: {desc} for matrix crosspoints or ports, set in AZedit. Check: data and power connectors.', DWF,
         **({'depthMm': 44} if '32' in pn else {}))
unit('lcp-102', 'LCP-102', 'LCP-102 analog trim panel, 2RU', 'Level control', 'control', 2,
     [R('io', 'RS-422', 'DB9', 1, 'Peripheral (RS-485)'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '2RU, 16 channels each with a name display, output level knob and second level knob, address key, 181 mm deep, 3.8 kg. Connects to the '
     'matrix peripheral port (Zeus III, XCP-ADAM-MC). Check: rear connectors.', DWF, depthMm=181)

# ======================= Interfaces and peripherals =======================
unit('rvon-i-o', 'RVON-I/O', 'RVON-I/O 8-port VoIP interface, 1RU', 'RVON', 'audio', 1,
     [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', AA, 'DB9M', 1, 'I/O (8 ports audio + data)'), R('io', 'GPIO', 'DB25F', 1, 'GPI/O'),
      R('out', 'GPIO', 'DB9F', 1, 'Relays'), R('io', 'RS-232', 'DB9', 1, 'Serial'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 203 mm deep, 1.7 kg, 90-240 V AC. Carries 8 analog intercom ports (audio and keypanel data) over IP to an RVON-16 / RVON-C card '
     'or another RVON-I/O.', ('RTS RVON-I/O user manual (manualslib)', 'https://www.manualslib.com/manual/327307/Rts-Rvon-I-O.html'), verified=True, depthMm=203)
unit('gpio-16', 'GPIO-16', 'GPIO-16 general purpose I/O frame, 16 in / 16 relays', 'Peripherals', 'control', 1,
     [R('in', 'GPIO', 'DB25', 1, 'Opto inputs 1-16'), R('out', 'GPIO', 'DB25', 1, 'Relays 1-16'), R('io', 'RS-422', 'DB9', 1, 'Matrix data (RS-485)'),
      R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 16 opto-isolated inputs and 16 relay outputs, 178 mm deep, 2.5 kg. Front input status LEDs. Connects to the matrix peripheral bus '
     '(XCP-ADAM-MC J3, ODIN, Zeus). Check: GPIO connector types.', BRO, depthMm=178)
unit('uio-256', 'UIO-256', 'UIO-256 universal I/O frame, 16 GPI in / 16 out', 'Peripherals', 'control', 1,
     [R('in', 'GPIO', 'DB25', 1, 'GPI inputs 1-16'), R('out', 'GPIO', 'DB25', 1, 'GPI outputs 1-16'), R('io', 'RS-422', 'DB9', 1, 'Matrix data (RS-485)'),
      R('in', 'Power', 'Other', 1, 'Power')],
     'GPI interface: 16 inputs (remote keys for ports, party lines or outputs) and 16 outputs for lights, transmitters and paging. Legacy, '
     'replaced by the GPIO-16. Check: rack height and connectors.', ('RTS UIO-256 specifications (manualslib)', 'https://www.manualslib.com/manual/142792/Rts-Uio-256.html'))
unit('ifb-828', 'IFB-828', 'IFB-828 IFB interface, 8 outputs, 1RU', 'IFB', 'audio', 1,
     [R('in', AA, 'XLR3F', 2, 'Program In'), R('in', AA, 'Other', 1, 'Matrix (4-wire)'), R('out', AA, 'XLR3M', 8, 'IFB Out'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 178 mm deep, 4 kg. Feeds up to 8 IFB beltpacks (4030 / IFB-325) with program and interrupt; 8 front level controls. Check: rear connectors.',
     BRO, depthMm=178)
unit('4010', '4010', '4010 central IFB electronics, 1RU', 'IFB', 'audio', 1,
     [R('in', AA, 'Other', 4, 'Program In'), R('out', AA, 'Other', 4, 'IFB Out'), R('io', 'Other', 'Other', 1, 'Control station'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 381 mm deep, 4.9 kg. Central IFB electronics for the 4001 (4-channel) and 4003 (12-channel) control stations. Check: channel count and connectors.',
     BRO, depthMm=381)
unit('tm-10k', 'TM-10K', 'TM-10K trunk master, 2RU', 'Trunking', 'control', 2,
     [R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('io', 'RS-422', 'DB9', 8, 'Trunk port (RS-485)'), R('in', 'Power', 'IEC', 2, 'PSU')],
     '2RU, 305 mm deep, 12 kg. Links up to 256 matrix systems and 10,000+ users; dual PSUs, dual network interfaces, optional redundant trunk master. '
     'Check: trunk port count and connectors.', BRO, depthMm=305)
unit('icp-2000', 'ICP-2000', 'ICP-2000 trunk interface, 1RU', 'Trunking', 'control', 1, [R('io', 'RS-422', 'DB9', 2, 'Trunk'), R('in', 'Power', 'Other', 1, 'Power')],
     '1RU companion to the TM-10K / TM-2000 trunk master. Check: function and connectors.', DWF)
unit('swp-2000', 'SWP-2000', 'SWP-2000 trunk switch panel, 1RU', 'Trunking', 'control', 1, [R('io', 'RS-422', 'DB9', 2, 'Trunk'), R('in', 'Power', 'Other', 1, 'Power')],
     '1RU, 146 mm deep. Companion to the TM-10K trunk master (switches to the redundant trunk master). Check: function and connectors.', DWF, depthMm=146)
unit('tif-4000', 'TIF-4000', 'TIF-4000 12-line telephone interface, 4RU', 'Interfaces', 'audio', 4,
     [R('io', AA, 'RJ11', 12, 'Telephone line'), R('io', AA, 'Other', 12, 'Matrix (4-wire)'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '4RU, 330 mm deep, 12.9 kg. Up to 12 analog telephone lines into the matrix (hybrids with auto-answer). Check: connector types.', BRO, depthMm=330)
unit('sip-isdn', 'SIP-ISDN', 'SIP-ISDN telephone interface, 1RU', 'Interfaces', 'audio', 1,
     [R('io', 'Other', 'RJ45', 1, 'ISDN S0'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (SIP)'), R('io', AA, 'Other', 2, 'Matrix (4-wire)'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '1RU, 216 mm deep, 1.4 kg. One ISDN S0 (2 lines) plus LAN for SIP calls into the matrix. Check: matrix connectors.', BRO, depthMm=216)
unit('sap-1626', 'SAP-1626', 'SAP-1626 source assignment panel, 2RU', 'Interfaces', 'control', 2,
     [R('in', AA, 'Telco 50-pin', 1, 'Channel I/O A'), R('out', AA, 'Telco 50-pin', 1, 'Channel I/O B'), R('in', 'Power', 'IEC', 1, 'AC In')],
     '2RU, 249 mm deep, 4.5 kg. Assigns 12 intercom and 3 program channels to 26 user stations; two 50-pin I/O connectors. Check: connector type.',
     BRO, depthMm=249)
unit('rm-325', 'RM-325', 'RM-325 two-channel binaural user station, 1RU', 'TW', 'audio', 1,
     [F('io', AA, 'XLR4F', 1, 'Headset'), R('io', AA, 'XLR3', 2, 'TW line'), R('in', 'Power', 'Other', 1, 'Power')],
     '1RU, 203 mm deep, 1.2 kg. Two-channel binaural TW user station. Check: rear connectors and rack width.', BRO, depthMm=203)
unit('bop-220', 'BOP-220', 'BOP-220 breakout panel, 20 XLR', 'TW', 'patch', 2,
     [R('io', AA, 'XLR3', 20, 'Line'), R('io', AA, 'Multipin', 2, 'Multipin')],
     'Breakout panel with 20 XLRs (J101-J120, two rows of 10) and two multipin connectors, from the RTS drawing. Check: rack height, function '
     'and connector genders.', DWF)

ids = [m['id'] for m in OUT]; assert len(ids) == len(set(ids))
json.dump(OUT, open(os.path.join(CAT, 'rts-more.json'), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'rts-more.json' not in idx: idx.append('rts-more.json')
json.dump(idx, open(ip, 'w')); print('rts-more.json', len(OUT), 'entries,', sum(m['verified'] for m in OUT), 'verified;', len(idx), 'files in index')
