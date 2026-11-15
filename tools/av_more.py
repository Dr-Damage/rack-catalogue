#!/usr/bin/env python3
"""AV / venue gear batch (added 2026-11-15): common venue and broadcast AV gear that the catalogue did not have yet.

  Files: daktronics, extron, kramer, buffalo, raritan-more (KVM switches and LCD drawers; raritan.json stays with kvm.py),
  tripleplay, electrovoice, dynacord, cisco-smb (cisco.json stays with network.py), ikusi (Class A headend frame + modules),
  promax-headend (DTTV headend; promax.json stays with timing_rf.py), dataflow (1RU fibre panels), bmd-atem-tvs (ATEM
  Television Studio HD8 / HD8 ISO; prefix bmdt-, since bmd- belongs to the app's built-in list).
  Wider ranges asked for the same day: Raritan (KX IV, SX II, LX II, drawers), Extron (DXP, SW, DSC, IN1800, IPCP Pro, XTP II,
  DTP CrossPoint, XPA, DA), lilliput and marshall-more (dual 7-inch rack monitors), audinate and dante-adapters (Dante adapters with a 'dongle' block), crestron (CP4/CP4N/PRO4, DM-MD frames and DMC cards, DM NVX, DMPS3) and amx (NX controllers,
  Enova DGX frames and boards, DVX, NXA-PDU).

Daktronics publishes no rack sizes or connector lists for its control-room gear (VP-6000 / DI-6000 processors, DMP-8000
players, display-control PCs, signal converters). Those entries are drawn from photos of installed units and are all
verified=false with "Check:" notes. Everything else comes from the maker's data sheet or a dealer listing (see source).
Not added: Audinate Dante AVIO adapters (inline dongles, not rack gear), unbranded dual / quad 7-inch rack monitors
(TVLogic RKM-270A is the nearest catalogued unit)."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m); return m
AC = lambda n=1: R('in', 'Power', 'IEC C14', n, 'PSU' if n > 1 else 'AC In')
LAN = lambda n=1, p='LAN', face='rear': g(face, 'io', 'Ethernet', 'RJ45', n, p)

# ======================= Daktronics (photos only) =======================
DK = 'https://www.daktronics.com/en-us/support/components/vp-6000'
DKS = 'Photos of installed units; Daktronics publishes no rack data'
add('daktronics.json', 'daktronics-vp-6000', 'Daktronics', 'VP-6000', 'VP-6000 video processor (6000 series)', '6000 Series processors', 'converter', 3,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', 'DisplayPort', 'DisplayPort', 4, 'Display Out'), R('out', '3G-SDI', 'BNC', 1, 'Confidence SDI Out'),
     LAN(2, 'Control LAN'), R('io', 'USB', 'USB-A', 2, 'USB'), AC(2)],
    'Daktronics LED display video processor (scaler / router for video boards and ribbons), front LCD window, handles. Paired main and backup '
    'units are common (Venus Control Suite switches primary to backup). Check: height (3RU from photos) and every connector; the I/O is '
    'configured per job (KB DD3663054 shows the panels as images only).', DKS, DK, verified=False, full=True)
add('daktronics.json', 'daktronics-di-6000', 'Daktronics', 'DI-6000', 'DI-6000 display interface (6000 series)', '6000 Series processors', 'converter', 3,
    [R('in', 'DisplayPort', 'DisplayPort', 4, 'Display In'), R('out', 'Fibre', 'LC duplex', 4, 'Display Fibre Out'), LAN(2, 'Control LAN'), AC(2)],
    'Display interface that drives the LED display data lines from the processor. Same chassis as the VP-6000. Check: height and connectors.',
    DKS, 'https://www.daktronics.com/en-us/support/kb/DD3663054', verified=False, full=True)
add('daktronics.json', 'daktronics-dmp-8000', 'Daktronics', 'DMP-8000', 'DMP-8000 display media player (half-width)', 'Display Media Players', 'computer', 2,
    [R('out', 'DisplayPort', 'DisplayPort', 4, 'Display Out'), R('in', '3G-SDI', 'BNC', 1, 'Live Video In (option)'), LAN(2), R('io', 'USB', 'USB-A', 2, 'USB'),
     F('io', 'USB', 'USB-A', 2, 'USB'), AC()],
    'Show Control / Venus content player PC for scoreboards and ribbons, half-rack 2RU, often two side by side (main and backup). '
    'Check: height, width and outputs (video card fit varies).', DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False, w=6, full=True)
add('daktronics.json', 'daktronics-control-pc-half-2ru', 'Daktronics', 'Control PC (half-width 2RU)', 'Half-width 2RU control PC (Show Control, DSTI, data servers)',
    'Control-room PCs', 'computer', 2,
    [R('out', 'DisplayPort', 'DisplayPort', 2, 'Display Out'), LAN(2), R('io', 'USB', 'USB-A', 4, 'USB'), R('io', 'RS-232', 'DB9', 1, 'COM'),
     F('io', 'USB', 'USB-A', 2, 'USB'), AC()],
    'Daktronics-badged half-rack PC used for Show Control, DSTI (statistics / data interface) and similar roles; the front badge names the role. '
    'Check: connectors (generic PC build).', DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False, w=6, full=True)
add('daktronics.json', 'daktronics-control-pc-2ru', 'Daktronics', 'Control PC (2RU)', 'Full-width 2RU display control PC (ribbon / board control)',
    'Control-room PCs', 'computer', 2,
    [R('out', 'DisplayPort', 'DisplayPort', 4, 'Display Out'), LAN(2), R('io', 'USB', 'USB-A', 4, 'USB'), R('io', 'RS-232', 'DB9', 1, 'COM'),
     F('io', 'USB', 'USB-A', 2, 'USB'), AC()],
    'Daktronics-badged 2RU PC with handles and front logo window, used for ribbon or board control (main and backup pairs). '
    'Check: height and connectors.', DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False, full=True)
add('daktronics.json', 'daktronics-signal-converter', 'Daktronics', 'Signal Converter', 'Signal Converter, 3 channels (RS-232 / RS-422 / fibre data)',
    'Interface units', 'converter', 1,
    [R('in', 'RS-232', 'DB9', 3, 'Converter In'), R('out', 'Fibre', 'ST', 3, 'Converter Out (fibre)'), R('out', 'RS-422', 'Terminal block', 3, 'Converter Out (RS-422)'), AC()],
    'Front: power switch and RX/TX LEDs for converters 1-3. Carries scoreboard / statistics serial data (e.g. results feeds) to the displays. '
    'Check: rear connectors.', DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False)
add('daktronics.json', 'daktronics-switch-interface', 'Daktronics', 'Switch Interface', 'Switch Interface, 1RU', 'Interface units', 'control', 1,
    [R('io', 'RS-232', 'DB9', 2, 'Data'), R('in', 'Other', 'Terminal block', 1, 'Switch inputs'), AC()],
    'Front: logo and power switch only. Interfaces switch / GPI closures with the display control system. Check: rear connectors.',
    DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False)
add('daktronics.json', 'daktronics-db9-panel-8', 'Daktronics', 'Serial panel 8 x DB9', 'Serial interface panel, 8 x DB9, 1RU', 'Interface units', 'patch', 1,
    [F('io', 'RS-232', 'DB9', 8, 'Port'), R('io', 'RS-232', 'Terminal block', 8, 'Port')],
    'Silver 1RU panel with 8 numbered DB9 sockets on the front, wired at the rear to the console / data lines. Check: rear termination.',
    DKS, 'https://www.daktronics.com/en-us/support/manuals', verified=False)

# ======================= Extron / Kramer =======================
add('extron.json', 'extron-sw2-hd-4k-plus', 'Extron', '60-1603-01', 'SW2 HD 4K PLUS two-input 4K/60 HDMI switcher (half-rack)', 'SW HD 4K PLUS', 'switcher', 1,
    [R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), LAN(1), R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'),
     R('io', 'Other', 'Captive screw 5-pole', 1, 'Contact / Tally'), F('io', 'USB', 'Mini USB-B', 1, 'Config'), R('in', 'Power', '12V DC captive screw', 1, '12V DC In')],
    'HDCP 2.3, auto-switching. 1U half-rack (44 x 222 x 152 mm), 0.5 kg, external 12 V 1.5 A supply, 5.5 W. Rack shelf sold separately.',
    'Extron SW HD 4K PLUS Series brochure A2', 'https://media.extron.com/public/download/files/brochure/sw_hd_4k_plus_series_A2.pdf', w=6, powerW=5.5, weightKg=0.5)
add('kramer.json', 'kramer-vs-88h2', 'Kramer', 'VS-88H2', 'VS-88H2 8x8 4K HDR HDCP 2.2 HDMI matrix switcher', 'VS matrix', 'router', 1,
    [R('in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('out', 'HDMI', 'HDMI', 8, 'HDMI Out'), LAN(1), R('io', 'RS-232', 'Terminal block 3-pin', 1, 'RS-232'),
     R('out', 'USB', 'USB-A', 1, 'USB power'), F('io', 'USB', 'Mini USB-B', 1, 'Firmware / control'), AC()],
    '18 Gbps 4K60 4:4:4 HDR matrix, 1U, 436 x 183 x 44 mm, 2.4 kg, 100-240 V AC. Check: which connectors are on the front (mini USB assumed front).',
    'Kramer VS-88H2 specifications', 'https://cdn.shopify.com/s/files/1/2507/3278/files/VS-88H2_Specifications.pdf', weightKg=2.4)

# ======================= Buffalo NAS =======================
add('buffalo.json', 'buffalo-ts3420rn', 'Buffalo', 'TS3420RN', 'TeraStation 3420RN 4-bay 1U rackmount NAS', 'TeraStation', 'computer', 1,
    [R('io', 'Ethernet', 'RJ45', 2, 'LAN (1 GbE)'), R('io', 'USB', 'USB-A', 1, 'USB 3.0'), F('io', 'USB', 'USB-A', 1, 'USB'), AC()],
    '4 front hot-swap drive bays, 1U. Check: rear connectors (front LEDs show LAN1 / LAN2).', 'Buffalo TeraStation dealer listings',
    'https://www.adorama.com/buts342rn42.html', verified=False, full=True)
add('buffalo.json', 'buffalo-ts5420rn', 'Buffalo', 'TS5420RN', 'TeraStation 5420RN 4-bay 1U rackmount NAS (10 GbE)', 'TeraStation', 'computer', 1,
    [R('io', 'Ethernet', 'RJ45', 2, 'LAN (10 GbE)'), R('io', 'Ethernet', 'RJ45', 2, 'LAN (1 GbE)'), R('io', 'USB', 'USB-A', 2, 'USB 3.2'), AC()],
    '4 front hot-swap bays, Alpine AL524 quad core, 8 GB. Check: port counts.', 'Buffalo TeraStation 5420RN dealer listing',
    'https://www.bhphotovideo.com/c/product/1760843-REG/buffalo_ts5420rn1604_terastation_5420rn_1u_rm_16tb.html', verified=False, full=True)

# ======================= Raritan KVM (more) =======================
add('raritan-more.json', 'raritan-dkx3-216', 'Raritan', 'DKX3-216', 'Dominion KX III-216 KVM-over-IP switch, 16 ports, 2 remote users', 'Dominion KX III', 'control', 1,
    [R('io', 'Other', 'RJ45 (CIM)', 16, 'Server'), LAN(2, 'LAN (GbE)'), R('out', 'DVI', 'DVI-D', 1, 'Local Port DVI'), R('io', 'USB', 'USB-A', 3, 'Local USB'),
     F('io', 'USB', 'USB-A', 1, 'Local USB'), R('io', 'Other', 'RJ45', 1, 'Tiering / KVM'), R('io', 'RS-232', 'DB9', 1, 'Serial (modem)'), AC(2)],
    'Servers connect through Raritan CIMs on Cat5 to the RJ45 server ports. Dual power. 1U. Discontinued; KX IV is the successor.',
    'Raritan DKX3-216 dealer specs', 'https://www.markertek.com/product/rar-dkx3-216/raritan-dominion-kx-iii-high-performance-kvm-over-ip-switch-16-server-ports-2-remote-users-1-local-port')
add('raritan-more.json', 'raritan-mccat216', 'Raritan', 'MCCAT216', 'MasterConsole CAT 2x16 KVM switch (2 users, 16 ports)', 'MasterConsole CAT', 'control', 1,
    [R('io', 'Other', 'RJ45 (CIM)', 16, 'Server'), R('out', 'Other', 'VGA + PS/2 + USB', 2, 'User console'), R('io', 'Other', 'RJ45', 1, 'Expansion'), AC()],
    'Analogue Cat5 KVM switch, 2 local users, 16 server ports with front port LEDs. Check: model (front reads "2x16 KVM") and console connectors.',
    'Raritan MasterConsole CAT range', 'https://www.raritan.com/products/kvm-serial', verified=False)
add('raritan-more.json', 'raritan-t1700g2-led', 'Raritan', 'T1700G2-LED', 'T1700G2-LED 17.3-inch LCD console drawer, 1U', 'LCD consoles', 'control', 1,
    [R('in', 'Other', 'DVI-I', 1, 'DVI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('in', 'DisplayPort', 'DisplayPort', 1, 'DP In'),
     R('io', 'USB', 'USB', 1, 'USB (keyboard / touchpad)'), F('io', 'USB', 'USB-A', 1, 'USB 3.0 pass-through'), AC()],
    '17.3-inch 1080p screen, keyboard and touchpad on a slide-out tray. 17.6 W. Category control (not monitor) so the app does not draw a screen on the front.',
    'Raritan rackmount LCD consoles data sheet', 'https://www.raritan.com/assets/ram/resources/data_sheets/ds-rackmount-lcd-consoles.pdf', full=True, powerW=17.6)
add('raritan-more.json', 'raritan-t1900-led', 'Raritan', 'T1900-LED', 'T1900-LED 19-inch LCD console drawer, 1U', 'LCD consoles', 'control', 1,
    [R('in', 'Other', 'DVI-D', 1, 'DVI In'), R('in', 'Other', 'VGA', 1, 'VGA In'), R('io', 'USB', 'USB', 1, 'USB / PS/2 (keyboard)'),
     F('io', 'USB', 'USB-A', 1, 'USB 2.0 pass-through'), AC()],
    '19-inch 4:3 screen, keyboard and touchpad on a slide-out tray. 17.4 W.',
    'Raritan rackmount LCD consoles data sheet', 'https://www.raritan.com/assets/ram/resources/data_sheets/ds-rackmount-lcd-consoles.pdf', full=True, powerW=17.4)

# ======================= Tripleplay (Uniguest) encoders =======================
TP = 'https://uniguest.com/wp-content/uploads/2023/09/Low-Latency-4K-HD-Encoders.pdf'
for pn, nm, ch, sdi, note in [('ENCOD3R-LH2', 'ENCOD3R-LH2 low latency HD encoder, 2 channels', 2, 'HD-SDI', 'H.264 UDP multicast for IPTV.'),
                              ('ENCOD3R-LK41', 'ENCOD3R-LK41 low latency 4K encoder, 1 channel', 1, '12G-SDI', 'HEVC UDP multicast for IPTV.'),
                              ('ENCOD3R-LK42', 'ENCOD3R-LK42 low latency 4K encoder, 2 channels', 2, '12G-SDI', 'HEVC UDP multicast for IPTV.')]:
    add('tripleplay.json', 'tripleplay-' + pn.lower(), 'Tripleplay (Uniguest)', pn, nm, 'ENCOD3R', 'converter', 1,
        [R('in', 'HDMI', 'HDMI', ch, 'HDMI In'), R('in', sdi, 'BNC', ch, 'SDI In'), LAN(1, 'Stream / control LAN'), AC()],
        note + ' 1U, front LCD and keypad, channel / status LEDs. Check: LAN count, audio and power connectors (not published).',
        'Uniguest Low Latency 4K / HD Encoders sheet', TP, verified=False)

# ======================= Electro-Voice / Dynacord =======================
add('electrovoice.json', 'ev-n8000', 'Electro-Voice', 'N8000', 'NetMax N8000 digital matrix controller (300 MIPS)', 'NetMax', 'audio', 2,
    [R('io', 'Other', 'Card slot', 4, 'Audio card slot (AI-1 / AO-1 / MI-1 / DI-1 / DO-1)'), R('io', 'Other', 'Card slot', 1, 'Network slot (CM-1 CobraNet / DM-1 Dante)'),
     LAN(1, 'Control LAN'), R('io', 'Other', 'RJ45', 2, 'CAN bus'), R('io', 'RS-232', 'DB9', 2, 'RS-232'), R('io', 'Other', 'Euroblock 6-pole', 2, 'GPIO'),
     F('io', 'USB', 'USB-B', 1, 'USB'), AC()],
    'DSP matrix for PA / voice-alarm systems, 2U, 483 x 88 x 381 mm, 90 W max. I/O comes from the plug-in cards: add their ports per job. '
    'Often paired with Dynacord amplifiers.', 'Electro-Voice N8000 data sheet',
    'https://products.electrovoice.com/binary/N8000_NetMax_300_MIPS_Digital_Matrix_Controller_Datasheet_51_en_12595645195.pdf', full=True, powerW=90)
DY = 'https://products.dynacord.com/ap/de/c1800fdi'
for pn, w, note in [('C1800FDi', 700, '2 x 950 W'), ('C3600FDi', 1100, '2 x 1800 W')]:
    add('dynacord.json', 'dynacord-' + pn.lower(), 'Dynacord', pn, pn + ' DSP install power amplifier, ' + note, 'C Series', 'audio', 2,
        [R('in', 'Analog audio', 'Euroblock', 2, 'Input'), R('out', 'Other', 'Euroblock', 2, 'Speaker Out'), R('io', 'Other', 'Euroblock', 1, 'GPIO / remote power'),
         LAN(1, 'Network (SONICUE)'), AC()],
        'Two-channel FIR DSP amplifier for fixed install (low-Z or 70/100 V), 2U, 483 x 88 mm. Check: network port and speaker connector types; '
        + ('power figure ' + str(w) + ' W from the maker page.' if pn == 'C1800FDi' else 'power figure.'),
        'Dynacord C1800FDi product page', DY, verified=False, full=True, powerW=w)

# ======================= Cisco small business =======================
add('cisco-smb.json', 'cisco-rv345', 'Cisco', 'RV345-K9', 'RV345 dual-WAN gigabit VPN router', 'RV340 Series', 'network', 1,
    [F('io', 'Ethernet', 'RJ45', 16, 'LAN'), F('io', 'Ethernet', 'RJ45', 2, 'WAN'), F('io', 'USB', 'USB-A', 2, 'USB'), F('io', 'Other', 'RJ45', 1, 'Console'),
     R('in', 'Power', '12V DC barrel', 1, '12V DC In')],
    '280 x 44 x 170 mm, 1.2 kg, rack brackets included, external 12 V 2.5 A adapter.', 'Cisco RV345 product specifications',
    'https://www.cisco.com/c/en/us/support/docs/smb/routers/cisco-rv-series-small-business-routers/smb5465-product-specifications-of-the-rv345-dual-wan-vpn-router.html')
add('cisco-smb.json', 'cisco-sg250-26', 'Cisco', 'SG250-26', 'SG250-26 26-port gigabit smart switch', '250 Series', 'network', 1,
    [F('io', 'Ethernet', 'RJ45', 24, 'GE'), F('io', 'SFP', 'RJ45 / SFP combo', 2, 'Combo GE'), AC()],
    '24 x GbE plus 2 combo GbE / SFP. Check: data sheet (end of sale; successor CBS250-24T-4G).', 'Cisco 250 Series data sheet',
    'https://www.cisco.com/c/en/us/products/switches/250-series-smart-switches/index.html', verified=False)
add('cisco-smb.json', 'cisco-sg350-28', 'Cisco', 'SG350-28', 'SG350-28 28-port gigabit managed switch', '350 Series', 'network', 1,
    [F('io', 'Ethernet', 'RJ45', 24, 'GE'), F('io', 'SFP', 'RJ45 / SFP combo', 2, 'Combo GE'), F('io', 'SFP', 'SFP', 2, 'SFP'), F('io', 'Other', 'RJ45', 1, 'Console'), AC()],
    '24 x GbE, 2 combo GbE / SFP, 2 SFP. Check: data sheet (end of sale; successor CBS350-24T-4G).', 'Cisco 350 Series data sheet',
    'https://www.cisco.com/c/en/us/products/switches/350-series-managed-switches/index.html', verified=False)

# ======================= ATEM Television Studio HD8 =======================
TVS = 'https://www.blackmagicdesign.com/products/atemtelevisionstudiohd/techspecs'
for pn, nm, extra in [('SWATEMTVSTC/HD08', 'ATEM Television Studio HD8', ''), ('SWATEMTVSTC/HD08ISO', 'ATEM Television Studio HD8 ISO', ' ISO records every input to USB disks.')]:
    add('bmd-atem-tvs.json', 'bmdt-' + nm.lower().replace(' ', '-'), 'Blackmagic Design', pn, nm + ' live production switcher (8 SDI in)', 'ATEM Television Studio', 'switcher', 1,
        [R('in', '3G-SDI', 'BNC', 8, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'Program Out'), R('out', '3G-SDI', 'BNC', 2, 'Aux Out'),
         R('out', '3G-SDI', 'BNC', 1, 'Multiview Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Multiview'),
         R('in', 'Analog audio', 'XLR', 2, 'Mic / Line In'), R('in', 'Analog audio', 'RCA', 2, 'RCA In'), R('in', 'MADI audio', 'BNC', 1, 'MADI In'),
         R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), R('out', 'Analog audio', '1/4in jack', 4, 'Audio Out'), R('io', 'Other', 'XLR5', 1, 'Talkback'),
         R('io', 'Ethernet', 'RJ45', 1, 'Talkback (3rd party)'), R('in', 'Timecode', 'BNC', 1, 'Timecode In'), R('out', 'Timecode', 'BNC', 1, 'Timecode Out'),
         R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Out'), R('io', 'RS-422', 'RJ12', 1, 'Remote'),
         R('io', 'Ethernet', 'RJ45', 4, 'Ethernet switch'), R('io', 'USB', 'USB-C', 2, 'USB 3.0 (disk / PC)'), R('out', 'USB', 'USB-C', 2, 'Webcam Out'),
         F('out', 'Analog audio', '1/4in jack', 1, 'Headphones'), F('in', 'Analog audio', '1/4in jack', 1, 'Mic'), AC(), R('in', 'Power', 'XLR4', 1, '12V DC In')],
        'Rack / desktop switcher with built-in panel: 8 source buttons, ON / AFV audio keys, LCD. 100 W max.' + extra +
        ' Check: height (1RU-high front panel from photos; Blackmagic lists no RU) and SDI output split (12 SDI outs in total per maker).',
        'Blackmagic ATEM Television Studio HD8 tech specs', TVS, verified=False, full=True, powerW=100)

# ======================= Ikusi Class A headend (frame + modules, connectors on the module front) =======================
IK = 'https://www.ikusi.tv/en/products/tpc-010'
def ik_card(pn, ref, nm, ports, notes, url=IK, color='#c8ccd0', ver=False):
    add('ikusi.json', 'ikusi-' + pn.lower(), 'Ikusi', pn, nm, 'Class A modules', 'card', 0, ports, notes, 'Ikusi / dealer pages (ref ' + ref + ')', url,
        verified=ver, w=0, card=dict(fits=['Ikusi Class A'], slotWidth=1, color=color),
        rearModules=[dict(partNumber=pn, name='No rear connectors (front-wired module)', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=[])])
add('ikusi.json', 'ikusi-classa-rack-frame', 'Ikusi', 'Class A rack frame', 'Class A 19-inch rack frame for headend modules (9 positions)', 'Class A', 'frame', 6,
    [], 'Grey 19-inch frame with handles holding Class A modules side by side (processors, PSU, combiner, optical transmitters, splitters). '
    'All cabling (RF F-type, control DB9, red 12-24 V power bus) is on the module fronts. Frames join side by side and cascade the power bus. '
    'Check: height (about 6RU from photos) and number of positions (UNIBASE base plate is 9 bays).', 'Photos; Sciteq Ikusi listings',
    'https://www.sciteq.com.au/product/ikusi-tpc-010d-digital-channel-processor/', verified=False,
    frame=dict(system='Ikusi Class A', slots=9, slotOrder='ltr', rearAlign=1, door=False, front=dict(x0=0.08, x1=0.92, y0=0.06, y1=0.94),
               rear=dict(x0=0.08, x1=0.92, y0=0.06, y1=0.94), controller='None: each module is set up from its own DB9 control port (PCH programmer).'))
ik_card('CFP-700', '—', 'CFP-700 power supply module for Class A', [g('front', 'in', 'Power', 'IEC', 1, 'AC In'), g('front', 'out', 'Power', 'Banana', 5, 'DC Out (+24/+18/+12/+15/+5 V)')],
        'Feeds the module power bus; one or more per headend. Older model, CFP-900 is current. Check: outputs.', color='#9aa3ab')
ik_card('CFP-900', '—', 'CFP-900 power supply module for Class A', [g('front', 'in', 'Power', 'IEC', 1, 'AC In'), g('front', 'out', 'Power', 'Banana', 5, 'DC Out')],
        'Current PSU for the Class A family. Check: outputs.', color='#9aa3ab')
ik_card('TPC-010', '3842', 'TPC-010 agile DVB-T / DVB-C channel processor / converter',
        [g('front', 'in', 'RF', 'F', 1, 'RF In'), g('front', 'out', 'RF', 'F', 1, 'RF Out'), g('front', 'out', 'RF', 'F', 1, 'RF Loop'), g('front', 'io', 'RS-232', 'DB9', 1, 'Control'),
         g('front', 'in', 'Power', 'Banana', 1, 'DC bus')],
        'Double conversion, 45-862 MHz, 7/8 MHz channels, output 65-80 dBuV. One per channel. Check: loop connector.', ver=False)
ik_card('AMX-400', '—', 'AMX-400 4-input combiner (multiplexer)', [g('front', 'in', 'RF', 'F', 4, 'RF In'), g('front', 'out', 'RF', 'F', 1, 'RF Out'), g('front', 'out', 'RF', 'F', 1, 'Test'),
        g('front', 'in', 'Power', 'Banana', 1, '12V DC')],
        'Combines module outputs to the launch amplifier (HPA) in large Class A headends. 12 V 470 mA. Discontinued.',
        url='https://www.orbitadigital.com/en/discontinued/8402-ikusi-amx-400-multiplexer-4-inputs-and-up-to-24-outputs.html')
ik_card('FTD-420', '—', 'FTD-420 optical transmitter, 47-2150 MHz, 4 mW DFB', [g('front', 'in', 'RF', 'F', 1, 'RF In'), g('front', 'out', 'Fibre', 'SC/APC', 1, 'Optical Out'),
        g('front', 'in', 'Power', 'Banana', 1, 'DC bus')],
        'Sends terrestrial TV plus satellite IF over single-mode fibre (1310 nm). Check: optical connector (green SC/APC in photos).',
        url='https://www.orbitadigital.com/en/satellite-terrestrial/distribution/optical/2231-ikusi-ftd-420-optical-transmitter-module.html', color='#4caf50')
ik_card('FSP-306', '4918', 'FSP-306 optical splitter, 6 ways', [g('front', 'in', 'Fibre', 'SC/APC', 1, 'Optical In'), g('front', 'out', 'Fibre', 'SC/APC', 6, 'Optical Out')],
        'Passive 1:6 single-mode splitter, about 9 dB loss, return loss over 55 dB. Check: input connector position.',
        url='https://www.manualslib.com/manual/1555802/Ikusi-Fsp-Series.html', color='#4caf50')

# ======================= Promax DTTV headend =======================
PX = 'https://www.promaxelectronics.com/ing/products/digital-tv-headends-dttv'
add('promax-headend.json', 'promax-dttv-chassis', 'Promax', 'DTTV chassis', 'Digital To TV (DTTV) headend 19-inch chassis', 'DTTV', 'frame', 6, [AC()],
    'Plug-in transmodulator headend (DVB-S/S2 or DVB-T in, DVB-T out) with a DT-800 front control module (LCD, keypad, LAN). Modules cable on the rear. '
    'Check: height (about 6RU from photos) and slot count.', 'Photos; Promax DTTV news page', PX, verified=False, full=True,
    frame=dict(system='Promax DTTV', slots=10, slotOrder='ltr', rearAlign=1, door=False, front=dict(x0=0.06, x1=0.94, y0=0.05, y1=0.95),
               rear=dict(x0=0.06, x1=0.94, y0=0.05, y1=0.95), controller='DT-800 control module, normally slot 1', controllerSlot=1))
for pn, nm, ports, note in [
        ('DT-800', 'DT-800 DTTV control module', [g('front', 'io', 'Ethernet', 'RJ45', 1, 'LAN')], 'Front LCD and keypad; sets IP address for PC control software.'),
        ('DT-802', 'DT-802 DVB-S2 to DVB-T transmodulator module', [g('rear', 'in', 'RF', 'F', 1, 'Sat IF In'), g('rear', 'out', 'RF', 'F', 1, 'IF Loop'),
                                                                    g('rear', 'out', 'RF', 'F', 1, 'RF Out')], 'With CAM slot for scrambled services. Check: connectors.')]:
    add('promax-headend.json', 'promax-' + pn.lower(), 'Promax', pn, nm, 'DTTV modules', 'card', 0, [p for p in ports if p['face'] == 'front'], note,
        'Promax DT-802 manual (manualmachine)', 'https://manualmachine.com/promax/dt802/20616168-user-manual', verified=False, w=0,
        card=dict(fits=['Promax DTTV'], slotWidth=1, onlySlots=[1] if pn == 'DT-800' else None) if pn == 'DT-800' else dict(fits=['Promax DTTV'], slotWidth=1),
        rearModules=[dict(partNumber=pn, name='Rear', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=[p for p in ports if p['face'] == 'rear'])])

# ======================= DataFlow 1RU fibre panels (frame + adapter plates) =======================
DF = 'https://www.dataflow.com.au'
add('dataflow.json', 'dataflow-1ru-2plate', 'DataFlow', '1RU fibre panel (2 plates)', '1RU fibre patch panel, 2 adapter plate positions (up to 24 LC duplex)',
    'Fibre panels', 'frame', 1, [],
    'Black 1RU fibre termination panel with two removable adapter plates (left and right, each 6 or 12 LC duplex) and a centre logo badge. '
    'Laser warning on each plate. Check: maker part numbers (Australian brand, no online catalogue found).', 'Photos', DF, verified=False,
    frame=dict(system='DataFlow plate', slots=2, slotOrder='ltr', rearAlign=1, door=False, front=dict(x0=0.08, x1=0.92, y0=0.1, y1=0.9),
               rear=dict(x0=0.08, x1=0.92, y0=0.1, y1=0.9)))
for n, desc, col in [(6, 'OS2 single-mode, blue', '#2f6fd1'), (12, 'OS2 single-mode, blue', '#2f6fd1'), (6, 'OM3/OM4 multimode, aqua', '#2bb3b1'), (12, 'OM3/OM4 multimode, aqua', '#2bb3b1')]:
    sm = 'OS2' in desc
    pid = 'dataflow-plate-%dlc-%s' % (n, 'os2' if sm else 'om')
    add('dataflow.json', pid, 'DataFlow', 'Plate %d x LC duplex %s' % (n, 'OS2' if sm else 'OM'), 'Adapter plate, %d x LC duplex (%d fibres, %s)' % (n, n * 2, desc),
        'Fibre plates', 'card', 0, [F('io', 'Fibre', 'LC duplex', n, 'LC')],
        'Front is the patch side; the rear takes the spliced pigtails. %s' % ('One row of 6.' if n == 6 else 'Two rows of 6.'), 'Photos', DF, verified=False, w=0,
        card=dict(fits=['DataFlow plate'], slotWidth=1, color=col),
        rearModules=[dict(partNumber='Rear (splice side)', name='Rear (splice side)', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True,
                          portGroups=[R('io', 'Fibre', 'Splice', n * 2, 'F')])])
add('dataflow.json', 'dataflow-plate-blank', 'DataFlow', 'Blank plate', 'Blank adapter plate', 'Fibre plates', 'card', 0, [], 'Fills an unused plate position.',
    'Photos', DF, verified=False, w=0, card=dict(fits=['DataFlow plate'], slotWidth=1, color='#333a40'),
    rearModules=[dict(partNumber='Blank', name='Blank', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=[])])


# ======================= Wider ranges (requested 2026-11-15): Raritan, Extron, Crestron, AMX =======================
# Most of these come from range knowledge and dealer listings rather than a data sheet per model, so they are verified=False
# with "Check:" notes unless the source says otherwise.

# ---- Raritan KVM-over-IP, serial console, LX II ----
RKX = 'https://www.raritan.com/products/kvm-serial/kvm-over-ip-switches'
for pn, ports, users, ru in [('DKX4-108', 8, 1, 1), ('DKX4-116', 16, 1, 1), ('DKX4-216', 16, 2, 1), ('DKX4-232', 32, 2, 1), ('DKX4-416', 16, 4, 1),
                             ('DKX4-432', 32, 4, 1), ('DKX4-464', 64, 4, 2), ('DKX4-832', 32, 8, 1), ('DKX4-864', 64, 8, 2)]:
    add('raritan-more.json', 'raritan-' + pn.lower(), 'Raritan', pn, 'Dominion KX IV-%s KVM-over-IP switch, %d servers, %d remote users' % (pn[5:], ports, users),
        'Dominion KX IV', 'control', ru,
        [R('io', 'Other', 'RJ45 (CIM)', ports, 'Server'), LAN(2, 'LAN (GbE)'), R('out', 'DisplayPort', 'DisplayPort', 1, 'Local Port DP'),
         R('out', 'HDMI', 'HDMI', 1, 'Local Port HDMI'), R('io', 'USB', 'USB-A', 2, 'Local USB'), R('io', 'RS-232', 'RJ45', 1, 'Serial / modem'),
         R('io', 'Other', 'RJ45', 1, 'Tiering'), AC(2)],
        'Servers connect through Raritan D4CIM / DCIM computer interface modules on Cat5/6. Dual power. Check: local port connectors and RU for this size.',
        'Raritan Dominion KX IV range', RKX, verified=False)
for pn, n, dual in [('DSX2-4', 4, False), ('DSX2-8', 8, False), ('DSX2-16', 16, True), ('DSX2-32', 32, True), ('DSX2-48', 48, True)]:
    add('raritan-more.json', 'raritan-' + pn.lower(), 'Raritan', pn, 'Dominion SX II %d-port serial console server' % n, 'Dominion SX II', 'network', 1,
        [R('io', 'RS-232', 'RJ45', n, 'Serial'), LAN(2, 'LAN (GbE)'), R('io', 'RS-232', 'DB9', 1, 'Console'), R('io', 'USB', 'USB-A', 2, 'USB'),
         R('io', 'Other', 'RJ45', 1, 'Modem')] + ([AC(2)] if dual else [AC()]),
        'Secure out-of-band serial access to switches, routers and PDUs (Cisco-style RJ45 pinout). Check: power inlet count.', 'Raritan Dominion SX II range',
        'https://www.raritan.com/products/kvm-serial/serial-console-server', verified=False)
for pn, ports, users in [('DLX2-108', 8, 1), ('DLX2-116', 16, 1), ('DLX2-216', 16, 2), ('DLX2-416', 16, 4)]:
    add('raritan-more.json', 'raritan-' + pn.lower(), 'Raritan', pn, 'Dominion LX II-%s KVM-over-IP switch, %d servers' % (pn[5:], ports), 'Dominion LX II', 'control', 1,
        [R('io', 'Other', 'RJ45 (CIM)', ports, 'Server'), LAN(1, 'LAN'), R('out', 'Other', 'VGA', 1, 'Local Port VGA'), R('io', 'USB', 'USB-A', 2, 'Local USB'), AC()],
        'Entry KVM-over-IP for small server rooms. Check: connectors.', 'Raritan Dominion LX II data sheet',
        'https://www.legrand.com/datacenter/sites/g/files/ocwmcr716/files/2023-03/DOMINION%20LXII.pdf', verified=False)
for pn, sz, ins in [('T1700-LED', 17, 'VGA'), ('T1700-LED-KX4-116', 17, 'built-in KX IV 16-port'), ('T1900-KX4-132', 19, 'built-in KX IV 32-port')]:
    if pn == 'T1700-LED':
        add('raritan-more.json', 'raritan-t1700-led', 'Raritan', pn, 'T1700-LED 17-inch LCD console drawer, 1U (first generation)', 'LCD consoles', 'control', 1,
            [R('in', 'Other', 'VGA', 1, 'VGA In'), R('io', 'USB', 'USB', 1, 'USB (keyboard / touchpad)'), AC()],
            'Earlier 17-inch drawer (replaced by T1700G2-LED). Check: inputs.', 'Raritan LCD consoles', 'https://www.raritan.com/products/kvm-serial', verified=False, full=True)

# ---- Extron ----
EX = 'https://www.extron.com'
DXP = 'https://muzmart.com/files/store/127660/dxp_hd_4k_plus_series_d3_032818.pdf'
for n_in, n_out, wt in [(4, 4, 20.4), (8, 4, None), (8, 8, 30.8)]:
    pn = 'DXP %d%d HD 4K PLUS' % (n_in, n_out)
    add('extron.json', 'extron-dxp-%d%d-hd-4k-plus' % (n_in, n_out), 'Extron', pn, pn + ' %dx%d 4K/60 HDMI matrix switcher' % (n_in, n_out), 'DXP HD 4K PLUS', 'router', 1,
        [R('in', 'HDMI', 'HDMI', n_in, 'HDMI In'), R('out', 'HDMI', 'HDMI', n_out, 'HDMI Out'), R('out', 'Analog audio', 'Captive screw 5-pole', 2, 'Analog Audio Out'),
         R('out', 'AES/EBU', 'RCA (S/PDIF)', 2, 'S/PDIF Out'), R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'), LAN(1),
         F('io', 'USB', 'Mini USB-B', 1, 'Config'), AC()],
        '1U, internal 100-240 V supply, de-embedded audio on two outputs.' + (' %s W full load.' % wt if wt else ''),
        'Extron DXP HD 4K PLUS Series brochure D3', DXP, powerW=wt)
for n, w in [(4, 6), (8, 12)]:
    add('extron.json', 'extron-sw%d-hd-4k-plus' % n, 'Extron', 'SW%d HD 4K PLUS' % n, 'SW%d HD 4K PLUS %d-input 4K/60 HDMI switcher' % (n, n), 'SW HD 4K PLUS', 'switcher', 1,
        [R('in', 'HDMI', 'HDMI', n, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), LAN(1), R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'),
         R('io', 'Other', 'Captive screw', 1, 'Contact / Tally'), F('io', 'USB', 'Mini USB-B', 1, 'Config'), R('in', 'Power', '12V DC captive screw', 1, '12V DC In')],
        'Same family as the SW2. Check: width (%s) and power.' % ('half-rack' if w == 6 else 'full-rack'), 'Extron SW HD 4K PLUS Series brochure A2',
        'https://media.extron.com/public/download/files/brochure/sw_hd_4k_plus_series_A2.pdf', verified=False, w=w)
add('extron.json', 'extron-dsc-hd-hd-4k-plus-a', 'Extron', 'DSC HD-HD 4K PLUS A', 'DSC HD-HD 4K PLUS A HDMI to HDMI 4K scaler with audio', 'DSC', 'converter', 1,
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'Analog audio', 'Captive screw 5-pole', 1, 'Audio Out'),
     R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'), F('io', 'USB', 'Mini USB-B', 1, 'Config'), R('in', 'Power', '12V DC captive screw', 1, '12V DC In')],
    'Quarter-rack 1U scaler (rack shelf). Check: connectors.', 'Extron DSC range', EX, verified=False, w=3)
for n in (4, 6, 8):
    add('extron.json', 'extron-in180%d' % n, 'Extron', 'IN180%d' % n, 'IN180%d %d-input HDCP 2.2 scaling presentation switcher' % (n, n), 'IN1800', 'switcher', 1,
        [R('in', 'HDMI', 'HDMI', n - 2 if n > 4 else n, 'HDMI In'), R('in', 'Other', 'RJ45 (DTP2)', 2 if n > 4 else 0, 'DTP2 In'),
         R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('out', 'Other', 'RJ45 (DTP2)', 1, 'DTP2 Out'), R('out', 'Analog audio', 'Captive screw 5-pole', 1, 'Audio Out'),
         R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'), LAN(1), AC()],
        '1U presentation switcher with scaler, DTP2 extension and audio de-embedding. Check: input split by model.', 'Extron IN1800 range', EX, verified=False)
for pn, ru, w, com, ir, rel, io in [('IPCP Pro 250', 1, 6, 2, 1, 2, 0), ('IPCP Pro 350', 1, 12, 3, 2, 4, 4), ('IPCP Pro 550', 1, 12, 8, 8, 8, 8),
                                     ('IPCP Pro 555', 1, 12, 8, 8, 8, 8)]:
    add('extron.json', 'extron-' + pn.lower().replace(' ', '-'), 'Extron', pn, pn + ' IP Link Pro control processor', 'IP Link Pro', 'control', ru,
        [R('io', 'RS-232', 'Captive screw', com, 'COM'), R('out', 'Other', 'Captive screw', ir, 'IR / Serial'), R('out', 'Other', 'Captive screw', rel, 'Relay')] +
        ([R('io', 'Other', 'Captive screw', io, 'Digital I/O')] if io else []) +
        [LAN(1, 'LAN'), LAN(1, 'AV LAN'), R('io', 'Other', 'Captive screw', 1, 'eBUS'), F('io', 'USB', 'Mini USB-B', 1, 'Config'),
         R('in', 'Power', '12V DC captive screw', 1, '12V DC In')],
        'Room / system control processor. Check: port counts per model.', 'Extron IPCP Pro range', EX, verified=False, w=w)
for pn, ru, ins, outs in [('XTP II CrossPoint 1600', 4, 16, 16), ('XTP II CrossPoint 3200', 7, 32, 32), ('XTP II CrossPoint 6400', 14, 64, 64)]:
    add('extron.json', 'extron-' + pn.lower().replace(' ', '-'), 'Extron', pn, pn + ' modular 4K matrix switcher frame (%dx%d)' % (ins, outs), 'XTP II CrossPoint', 'router', ru,
        [R('io', 'Other', 'Board slot (4 ports)', ins // 4, 'Input board slot'), R('io', 'Other', 'Board slot (4 ports)', outs // 4, 'Output board slot'),
         LAN(1), R('io', 'RS-232', 'Captive screw', 1, 'RS-232'), AC(2)],
        'Input and output boards (XTP, HDMI, DTP, fibre, 3G-SDI) go in 4-port slots; add the board ports per job. Redundant PSU. Check: height.',
        'Extron XTP II CrossPoint range', EX, verified=False, full=True)
add('extron.json', 'extron-dtp-crosspoint-84-4k-ipcp-sa', 'Extron', 'DTP CrossPoint 84 4K IPCP SA', 'DTP CrossPoint 84 4K IPCP SA scaling matrix with control and amp',
    'DTP CrossPoint', 'router', 2,
    [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('in', 'Other', 'RJ45 (DTP)', 2, 'DTP In'), R('in', 'Other', 'VGA', 2, 'VGA In'),
     R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('out', 'Other', 'RJ45 (DTP)', 2, 'DTP Out'), R('in', 'Analog audio', 'Captive screw', 4, 'Mic / Line In'),
     R('out', 'Analog audio', 'Captive screw', 2, 'Speaker Out (amp)'), R('io', 'RS-232', 'Captive screw', 8, 'COM / IR / Relay / IO'), LAN(2), AC()],
    '8x4 scaling presentation matrix with built-in IPCP Pro control processor and stereo amplifier. Check: connector counts.', 'Extron DTP CrossPoint range', EX,
    verified=False, full=True)
for pn, ch in [('XPA 2001-70V', 1), ('XPA 2002', 2), ('XPA 2004', 4)]:
    add('extron.json', 'extron-' + pn.lower().replace(' ', '-'), 'Extron', pn, pn + ' power amplifier, %d channel%s' % (ch, 's' if ch > 1 else ''), 'XPA 2000', 'audio', 1,
        [R('in', 'Analog audio', 'Captive screw', ch, 'Input'), R('out', 'Other', 'Captive screw', ch, 'Speaker Out'), R('io', 'Other', 'Captive screw', 1, 'Remote / standby'), AC()],
        '1U convection-cooled amplifier. Check: model power and outputs.', 'Extron XPA 2000 range', EX, verified=False)
for n in (2, 4, 6):
    add('extron.json', 'extron-da%d-hd-4k-plus' % n, 'Extron', 'DA%d HD 4K PLUS' % n, 'DA%d HD 4K PLUS 1:%d 4K/60 HDMI distribution amplifier' % (n, n), 'DA HD 4K PLUS', 'converter', 1,
        [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', n, 'HDMI Out'), R('io', 'RS-232', 'Captive screw 3-pole', 1, 'RS-232'),
         F('io', 'USB', 'Mini USB-B', 1, 'Config'), R('in', 'Power', '12V DC captive screw', 1, '12V DC In')],
        'Check: width (half-rack assumed).', 'Extron DA HD 4K PLUS range', EX, verified=False, w=6)

# ---- Crestron ----
CR = 'https://www.crestron.com'
add('crestron.json', 'crestron-cp4n', 'Crestron', 'CP4N', 'CP4N 4-Series control system (with control subnet)', '4-Series control', 'control', 1,
    [R('io', 'RS-232', 'Terminal block', 2, 'COM (RS-232/422/485)'), R('out', 'Other', 'Terminal block', 8, 'IR / Serial'), R('out', 'Other', 'Terminal block', 8, 'Relay'),
     R('io', 'Other', 'Terminal block', 8, 'Versiport I/O'), R('io', 'Other', 'Terminal block 4-pin', 1, 'Cresnet'), LAN(1, 'LAN'),
     R('io', 'Ethernet', 'RJ45', 8, 'Control Subnet (PoE)'), R('io', 'USB', 'USB-A', 1, 'USB'), F('io', 'USB', 'USB-C', 1, 'Computer'), AC()],
    '1U 4-Series processor; CP4 is the same without the control-subnet switch. Check: subnet port count.', 'Crestron CP4N range', CR, verified=False)
add('crestron.json', 'crestron-cp4', 'Crestron', 'CP4', 'CP4 4-Series control system', '4-Series control', 'control', 1,
    [R('io', 'RS-232', 'Terminal block', 2, 'COM (RS-232/422/485)'), R('out', 'Other', 'Terminal block', 8, 'IR / Serial'), R('out', 'Other', 'Terminal block', 8, 'Relay'),
     R('io', 'Other', 'Terminal block', 8, 'Versiport I/O'), R('io', 'Other', 'Terminal block 4-pin', 1, 'Cresnet'), LAN(1, 'LAN'), R('io', 'USB', 'USB-A', 1, 'USB'), AC()],
    '1U 4-Series processor. Check: connectors.', 'Crestron CP4 range', CR, verified=False)
add('crestron.json', 'crestron-pro4', 'Crestron', 'PRO4', 'PRO4 4-Series control system', '4-Series control', 'control', 2,
    [R('io', 'RS-232', 'DB9', 6, 'COM'), R('out', 'Other', 'Terminal block', 8, 'IR / Serial'), R('out', 'Other', 'Terminal block', 8, 'Relay'),
     R('io', 'Other', 'Terminal block', 8, 'Versiport I/O'), R('io', 'Other', 'Terminal block 4-pin', 2, 'Cresnet'), LAN(1, 'LAN'),
     R('io', 'Ethernet', 'RJ45', 1, 'Control Subnet'), R('io', 'USB', 'USB-A', 1, 'USB'), AC()],
    'High-port-count 4-Series processor. Check: height and COM connectors.', 'Crestron PRO4 range', CR, verified=False)
DMMD = 'https://de.crestron.com/getmedia/c145abc1-c7cc-4457-85bb-c96cd6c819bd/ss_dm-md8x8_cpu3'
for n, ru in [(8, 4), (16, 8), (32, 15)]:
    add('crestron.json', 'crestron-dm-md%dx%d-cpu3' % (n, n), 'Crestron', 'DM-MD%dX%d-CPU3' % (n, n), 'DM-MD%dX%d-CPU3 DigitalMedia modular switcher frame' % (n, n),
        'DigitalMedia switchers', 'frame', ru,
        [LAN(1, 'LAN'), LAN(1, 'CONTENT (streaming)'), R('io', 'USB', 'USB-A', 1, 'USB (EDID / firmware)'), AC()],
        '%d single-input card slots and %d two-output card slots (one output card = 2 outputs). ' % (n, n // 2) +
        ('Verified for 8x8: 4RU, 177 x 485 x 399 mm, 9.1 kg, 220 W typical.' if n == 8 else 'Check: height (scaled from the 8x8).'),
        'Crestron DM-MD8X8-CPU3 spec sheet', DMMD, verified=(n == 8), full=True, powerW=220 if n == 8 else None,
        frame=dict(system='Crestron DM-MD', slots=n + n // 2, slotOrder='ltr', rearAlign=1, door=False, front=dict(x0=0.05, x1=0.95, y0=0.05, y1=0.95),
                   rear=dict(x0=0.05, x1=0.95, y0=0.05, y1=0.95),
                   controller='Slots 1-%d are input cards, slots %d-%d are output cards (2 outputs each).' % (n, n + 1, n + n // 2)))
def cr_card(pn, nm, ports, note):
    add('crestron.json', 'crestron-' + pn.lower(), 'Crestron', pn, nm, 'DigitalMedia cards', 'card', 0, [], note, 'Crestron DMC card range', CR, verified=False, w=0,
        card=dict(fits=['Crestron DM-MD'], slotWidth=1),
        rearModules=[dict(partNumber=pn, name='Card I/O', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=ports)])
cr_card('DMC-4KZ-HD', 'DMC-4KZ-HD HDMI input card', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In')], 'Input card slot. Check: audio breakout.')
cr_card('DMC-4KZ-C', 'DMC-4KZ-C DM 8G+ input card', [R('in', 'Other', 'RJ45 (DM 8G+)', 1, 'DM 8G+ In')], 'Input card slot (HDBaseT twisted pair).')
cr_card('DMC-12G-SDI', 'DMC-12G-SDI input card', [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Loop')], 'Input card slot. Check: model name.')
cr_card('DMC-4KZ-CO-HD', 'DMC-4KZ-CO-HD output card (2 x DM 8G+ and 2 x HDMI)', [R('out', 'Other', 'RJ45 (DM 8G+)', 2, 'DM 8G+ Out'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out')],
        'Output card slot, 2 outputs (each mirrored on DM and HDMI).')
cr_card('DMC-4KZ-HDO', 'DMC-4KZ-HDO output card (2 x HDMI)', [R('out', 'HDMI', 'HDMI', 2, 'HDMI Out')], 'Output card slot, 2 HDMI outputs.')
add('crestron.json', 'crestron-dm-nvx-dir-80', 'Crestron', 'DM-NVX-DIR-80', 'DM-NVX-DIR-80 DM NVX Director virtual switching appliance (80 endpoints)', 'DM NVX', 'network', 1,
    [LAN(2, 'LAN'), R('io', 'USB', 'USB-A', 2, 'USB'), AC()], 'Manages DM NVX AV-over-IP encoders and decoders. DIR-160 / DIR-ENT are larger. Check: ports.',
    'Crestron DM NVX Director range', CR, verified=False)
add('crestron.json', 'crestron-dm-nvx-360', 'Crestron', 'DM-NVX-360', 'DM-NVX-360 4K60 AV-over-IP encoder / decoder (half-width with rack kit)', 'DM NVX', 'converter', 1,
    [R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE+)'), R('io', 'SFP', 'SFP', 1, 'SFP'),
     R('in', 'Analog audio', 'Terminal block', 1, 'Audio In'), R('out', 'Analog audio', 'Terminal block', 1, 'Audio Out'), R('io', 'RS-232', 'Terminal block', 1, 'COM'),
     R('out', 'Other', 'Terminal block', 1, 'IR'), R('in', 'Power', '24V DC', 1, '24V DC In')],
    'Desktop box; two fit side by side on a 1U rack kit. Check: connectors.', 'Crestron DM NVX range', CR, verified=False, w=6)
for pn, ru in [('DMPS3-4K-250-C', 2), ('DMPS3-4K-350-C', 3)]:
    add('crestron.json', 'crestron-' + pn.lower(), 'Crestron', pn, pn + ' 4K DigitalMedia presentation system', 'DMPS3-4K', 'switcher', ru,
        [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('in', 'Other', 'RJ45 (DM 8G+)', 2 if ru == 2 else 3, 'DM In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
         R('out', 'Other', 'RJ45 (DM 8G+)', 1, 'DM Out'), R('in', 'Analog audio', 'Terminal block', 4, 'Mic / Line In'), R('out', 'Analog audio', 'Terminal block', 2, 'Audio Out'),
         R('out', 'Other', 'Terminal block', 2, 'Speaker Out (amp)'), R('io', 'RS-232', 'Terminal block', 2, 'COM'), R('out', 'Other', 'Terminal block', 4, 'IR / Relay / IO'),
         LAN(1, 'LAN'), R('io', 'Ethernet', 'RJ45', 1, 'Control Subnet'), AC()],
        'Presentation switcher with built-in 3-Series control, DSP and amplifier. Check: input counts.', 'Crestron DMPS3-4K range', CR, verified=False, full=True)

# ---- AMX ----
AMXU = 'https://www.amx.com'
for pn, com, ir, rel, io, w in [('NX-1200', 2, 2, 2, 4, 6), ('NX-2200', 4, 4, 4, 4, 12), ('NX-3200', 8, 8, 8, 8, 12), ('NX-4200', 16, 8, 8, 8, 12)]:
    add('amx.json', 'amx-' + pn.lower(), 'AMX', pn, pn + ' NetLinx NX integrated controller', 'NetLinx NX', 'control', 1,
        [R('io', 'RS-232', 'DB9 / terminal block', com, 'COM (RS-232/422/485)'), R('out', 'Other', 'Terminal block', ir, 'IR / Serial'), R('out', 'Other', 'Terminal block', rel, 'Relay'),
         R('io', 'Other', 'Terminal block', io, 'I/O'), R('io', 'Other', 'Terminal block', 1, 'AxLink'), LAN(1, 'LAN'), R('io', 'Ethernet', 'RJ45', 1, 'ICSLan'),
         R('io', 'USB', 'USB-A', 1, 'USB'), F('io', 'USB', 'Mini USB-B', 1, 'Program'), R('in', 'Power', '12V DC terminal', 1, '12V DC In')],
        'NetLinx control processor. Check: port counts per model; the NX-1200 is half-width.', 'AMX NetLinx NX range', AMXU, verified=False, w=w)
for n, ru in [(8, 4), (16, 7), (32, 11), (64, 24)]:
    add('amx.json', 'amx-enova-dgx-%d' % (n * 100), 'AMX', 'DGX%d-ENC' % (n * 100), 'Enova DGX %d enclosure (%dx%d modular matrix)' % (n * 100, n, n), 'Enova DGX', 'frame', ru,
        [LAN(1, 'LAN'), R('io', 'RS-232', 'DB9', 1, 'Program'), R('io', 'USB', 'USB-B', 1, 'Program'), AC(2 if n > 8 else 1)],
        '%d input boards and %d output boards of 4 ports each (HDMI, DXLink twisted pair, DXLink fibre, DVI, audio). All four sizes share the boards. '
        'Check: height and PSU count.' % (n // 4, n // 4), 'AMX Enova DGX family guide', 'https://pdf.archiexpo.com/pdf/amx/enova-dgx-family/51274-177325.html',
        verified=False, full=True,
        frame=dict(system='AMX Enova DGX', slots=n // 2, slotOrder='ltr', rearAlign=1, door=False, front=dict(x0=0.05, x1=0.95, y0=0.05, y1=0.95),
                   rear=dict(x0=0.05, x1=0.95, y0=0.05, y1=0.95),
                   controller='Slots 1-%d are input boards, %d-%d output boards.' % (n // 4, n // 4 + 1, n // 2)))
def amx_board(pn, nm, ports, note):
    add('amx.json', 'amx-' + pn.lower(), 'AMX', pn, nm, 'Enova DGX boards', 'card', 0, [], note, 'AMX Enova DGX family guide',
        'https://pdf.archiexpo.com/pdf/amx/enova-dgx-family/51274-177325.html', verified=False, w=0, card=dict(fits=['AMX Enova DGX'], slotWidth=1),
        rearModules=[dict(partNumber=pn, name='Board I/O', width=1, cardsPerModule=1, cardOffset=0, default=True, included=True, portGroups=ports)])
amx_board('DGX-I-HDMI-4K60', 'DGX-I-HDMI-4K60 input board, 4 x HDMI', [R('in', 'HDMI', 'HDMI', 4, 'HDMI In')], 'Input board slot.')
amx_board('DGX-O-HDMI-4K60', 'DGX-O-HDMI-4K60 output board, 4 x HDMI', [R('out', 'HDMI', 'HDMI', 4, 'HDMI Out')], 'Output board slot.')
amx_board('DGX-I-DXL-4K60', 'DGX-I-DXL-4K60 input board, 4 x DXLink', [R('in', 'Other', 'RJ45 (DXLink)', 4, 'DXLink In')], 'Input board slot (HDBaseT).')
amx_board('DGX-O-DXL-4K60', 'DGX-O-DXL-4K60 output board, 4 x DXLink', [R('out', 'Other', 'RJ45 (DXLink)', 4, 'DXLink Out')], 'Output board slot (HDBaseT).')
amx_board('DGX-I-DXF-MMS', 'DGX-I-DXF-MMS input board, 4 x DXLink fibre (multimode)', [R('in', 'Fibre', 'LC duplex', 4, 'DXF In')], 'Input board slot.')
amx_board('DGX-O-DXF-MMS', 'DGX-O-DXF-MMS output board, 4 x DXLink fibre (multimode)', [R('out', 'Fibre', 'LC duplex', 4, 'DXF Out')], 'Output board slot.')
for pn, ru in [('DVX-3266-4K', 3), ('DVX-2265-4K', 2)]:
    add('amx.json', 'amx-' + pn.lower(), 'AMX', pn, pn + ' Enova DVX all-in-one presentation switcher', 'Enova DVX', 'switcher', ru,
        [R('in', 'HDMI', 'HDMI', 6 if ru == 3 else 4, 'HDMI In'), R('in', 'Other', 'RJ45 (DXLink)', 4 if ru == 3 else 2, 'DXLink In'),
         R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('out', 'Other', 'RJ45 (DXLink)', 2, 'DXLink Out'), R('in', 'Analog audio', 'Terminal block', 4, 'Mic / Line In'),
         R('out', 'Analog audio', 'Terminal block', 2, 'Line Out'), R('out', 'Other', 'Terminal block', 2, 'Speaker Out (amp)'),
         R('io', 'RS-232', 'Terminal block', 4, 'COM'), R('out', 'Other', 'Terminal block', 4, 'IR / Relay / IO'), LAN(1), R('io', 'Ethernet', 'RJ45', 1, 'ICSLan'), AC()],
        'Matrix switcher with NetLinx controller, DSP and amplifier in one. Check: input counts.', 'AMX Enova DVX range', AMXU, verified=False, full=True)
add('amx.json', 'amx-nxa-pdu-1508-8', 'AMX', 'NXA-PDU-1508-8', 'NXA-PDU-1508-8 power distribution unit, 8 outlets, network controlled', 'Power', 'pdu', 1,
    [LAN(1), R('io', 'Other', 'Terminal block', 1, 'AxLink')],
    'Per-outlet switching and current sensing from NetLinx. Check: outlet type for AU (IEC C13 assumed).', 'AMX power range', AMXU, verified=False,
    pdu=dict(mount='h', phase=1, volts=230, amps=15, plug='c14', metering='switched-outlet', main=dict(type='none'),
             circuits=[dict(id='A', type='resettable', amps=15)], outlets=[dict(type='c13', count=8, circuit='A', switched=True)]))
# ---- Dual 7-inch rack monitors (Lilliput, Marshall) ----
add('lilliput.json', 'lilliput-rm-7028s', 'Lilliput', 'RM-7028S', 'RM-7028S dual 7-inch 3RU rack monitor (3G-SDI / HDMI)', 'Rack monitors', 'monitor', 3,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Loop'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Loop'),
     R('in', 'Other', 'BNC', 6, 'YPbPr In'), R('in', 'Other', 'BNC', 2, 'Composite In'), LAN(1, 'LAN (remote)'), R('in', 'Other', 'Tally', 1, 'Tally'),
     R('in', 'Power', 'DC 7-24V', 1, 'DC In')],
    'Two 7-inch 1280 x 800 IPS screens, one input set per screen. 482.5 x 133.5 x 25.3 mm, 2.9 kg, 18 W. Check: YPbPr / composite loop counts and DC connector.',
    'Lilliput RM-7028S product page', 'https://lilliput.com/rm-7028s-product', powerW=18, weightKg=2.9, screens=dict(count=2, sizeIn=7, aspect='16:10'))
add('marshall-more.json', 'marshall-ml-702-v2', 'Marshall Electronics', 'ML-702-V2', 'ML-702-V2 dual 7-inch 3RU rack monitor (3G-SDI / HDMI / composite)', 'ML', 'monitor', 3,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Loop'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Loop'),
     R('in', 'Other', 'RCA', 2, 'CVBS In'), R('out', 'Other', 'RCA', 2, 'CVBS Loop'), R('in', 'Analog audio', 'RCA', 4, 'Audio In (L/R)'),
     R('in', 'Other', 'DB9', 1, 'GPI Tally'), F('out', 'Analog audio', '3.5mm jack', 2, 'Headphones'), R('in', 'Power', 'XLR4', 1, '12V DC In')],
    'Two 7-inch 1920 x 1200 screens, one input set per screen. 481.9 x 133.5 x 53.4 mm, 2.3 kg, 12 V 1.6 A (also a 5.5 x 2.1 mm jack). Check: tally connector.',
    'Markertek ML-702-V2 listing', 'https://www.markertek.com/product/mar-ml-702-v2/marshall-ml-702-v2-dual-7-inch-rackmountable-1920-x-1200-lcd-video-monitor-with-hdmi-3g-sdi-and-composite-inputs',
    powerW=19, weightKg=2.3, screens=dict(count=2, sizeIn=7, aspect='16:10'))
add('marshall-more.json', 'marshall-v-702w-12g', 'Marshall Electronics', 'V-702W-12G', 'V-702W-12G dual 7-inch 3RU 12G rack monitor with waveform', 'V-702W', 'monitor', 3,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
     R('in', 'Power', 'XLR4', 1, '12V DC In')],
    'Two 7-inch screens with waveform / vectorscope tools. 482.6 x 134.6 x 30.5 mm, 2.3 kg. Check: tally and power figure.',
    'Full Compass V-702W-12G listing', 'https://fullcompass.com/prod/623680-marshall-electronics-v-702w-12g-dual-7-inch-3ru-rackmount-12g-monitor-with-waveform-hdmi-and-12g-sdi-inputs',
    verified=False, weightKg=2.3, screens=dict(count=2, sizeIn=7, aspect='16:10'))

# ---- Dante adapters (requested 2026-11-15): not rack gear. The 'dongle' block says what they plug into, so the app can
# attach them to a host device's port (a USB adapter to a PC's USB port, an XLR adapter to a desk or amp XLR) and list them
# with that device. dongle = {plugs: connector on the adapter that mates with the host, hostType: port type it fits, power}.
AUD = 'https://www.markertek.com/brand/audinate'
DAN = lambda d='io': R(d, 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)')
def dongle(file, id, mfr, pn, nm, fam, ports, plugs, hostType, notes, src, url, verified=True, mm=(60, 25), **kw):
    add(file, id, mfr, pn, nm, fam, 'audio', 1, ports, notes, src, url, verified=verified, w=1,
        dongle=dict(plugs=plugs, hostType=hostType, power=kw.pop('power', 'PoE')), boxMm=dict(w=mm[0], h=mm[1]), **kw)
dongle('audinate.json', 'audinate-adp-usb-au-2x2', 'Audinate', 'ADP-USB-AU-2X2', 'Dante AVIO USB-A adapter, 2 x 2', 'AVIO',
       [DAN(), R('io', 'USB', 'USB-A (plug)', 1, 'USB to computer')], 'USB-A', 'USB',
       'Class-compliant USB audio: the computer sees a 2-in / 2-out sound card, no driver. Powered by USB or PoE.', 'Markertek Audinate listing', AUD, power='USB or PoE')
dongle('audinate.json', 'audinate-adp-usbc-au-2x2', 'Audinate', 'ADP-USBC-AU-2X2', 'Dante AVIO USB-C adapter, 2 x 2', 'AVIO',
       [DAN(), R('io', 'USB', 'USB-C (plug)', 1, 'USB-C to computer')], 'USB-C', 'USB',
       'Class-compliant USB-C audio, no driver. Powered by USB or PoE.', 'Audinate ADP-USBC-AU-2X2 data sheet',
       'https://cdn.shopify.com/s/files/1/0558/9630/9837/files/ADP-USBC-AU-2X2_datasheet_95ce78fb-8bab-41ff-a05c-653d7e984981.pdf', power='USB or PoE')
for pn, nm, ports, plugs, ht in [
        ('ADP-DAI-AU-1X0', 'Dante AVIO analogue input adapter, 1 channel', [DAN('out'), R('in', 'Analog audio', 'XLR3F', 1, 'Line In')], 'XLR3F', 'Analog audio'),
        ('ADP-DAI-AU-2X0', 'Dante AVIO analogue input adapter, 2 channels', [DAN('out'), R('in', 'Analog audio', 'XLR3F', 2, 'Line In')], 'XLR3F', 'Analog audio'),
        ('ADP-DAO-AU-0X1', 'Dante AVIO analogue output adapter, 1 channel', [DAN('in'), R('out', 'Analog audio', 'XLR3M', 1, 'Line Out')], 'XLR3M', 'Analog audio'),
        ('ADP-DAO-AU-0X2', 'Dante AVIO analogue output adapter, 2 channels', [DAN('in'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out')], 'XLR3M', 'Analog audio'),
        ('ADP-AES3-AU-2X2', 'Dante AVIO AES3 adapter, 2 x 2', [DAN(), R('in', 'AES/EBU', 'XLR3F', 1, 'AES3 In'), R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out')], 'XLR3', 'AES/EBU')]:
    dongle('audinate.json', 'audinate-' + pn.lower(), 'Audinate', pn, nm, 'AVIO', ports, plugs, ht,
           'In-line adapter on a short cable: the XLR end plugs straight into the other device, so attach it to that port. Line level, PoE powered.',
           'Markertek Audinate listing', AUD)
dongle('audinate.json', 'audinate-adp-bt-au-2x1', 'Audinate', 'ADP-BT-AU-2X1', 'Dante AVIO Bluetooth adapter, 2 in / 1 out', 'AVIO',
       [DAN(), R('in', 'Other', 'Bluetooth', 1, 'Bluetooth (wireless)')], 'none', '',
       'Pairs a phone or laptop over Bluetooth into Dante. PoE powered; sits loose on the network.', 'Markertek Audinate listing', AUD)
for pn, ins, outs in [('AVIO-A-2IN-EB', 2, 0), ('AVIO-A-2OUT-EB', 0, 2), ('AVIO-A-2IN2OUT-EB', 2, 2), ('AVIO-A-4IN-EB', 4, 0), ('AVIO-A-4OUT-EB', 0, 4)]:
    ports = [DAN()] + ([R('in', 'Analog audio', 'Euroblock 6-pin', ins // 2 if ins > 2 else 1, 'Line In (2 ch per block)')] if ins else []) + \
            ([R('out', 'Analog audio', 'Euroblock 6-pin', outs // 2 if outs > 2 else 1, 'Line Out (2 ch per block)')] if outs else [])
    dongle('audinate.json', 'audinate-' + pn.lower(), 'Audinate', pn, 'Dante AVIO Install analogue %s' % ('%d in / %d out' % (ins, outs)), 'AVIO Install', ports, 'none', '',
           'Small box with Euroblock terminals for fixed installs (behind displays, in lecterns, on a rack shelf). PoE powered. Check: Euroblock count.',
           'Markertek Audinate listing', AUD, verified=False, mm=(100, 30))
dongle('dante-adapters.json', 'neutrik-na2-io-dline', 'Neutrik', 'NA2-IO-DLINE', 'NA2-IO-DLINE Dante 2 x 2 line breakout box', 'Dante adapters',
       [R('io', 'Dante/AES67', 'etherCON', 1, 'Dante (PoE)'), R('in', 'Analog audio', 'XLR3F', 2, 'Line In'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out')], 'none', '',
       'Rugged end-of-network box, PoE powered. Check: connectors.', 'Canford Dante interfaces list', 'https://www.canford.co.uk/Index/Dante-interfaces', verified=False, mm=(120, 45))
dongle('dante-adapters.json', 'shure-ani22-xlr', 'Shure', 'ANI22-XLR', 'ANI22-XLR Dante 2 x 2 audio network interface', 'ANI',
       [R('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)'), R('in', 'Analog audio', 'XLR3F', 2, 'Mic / Line In'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out')], 'none', '',
       'Small box for table or wall (block-connector version ANI22-BLOCK). PoE powered. Check: connectors.', 'Shure ANI range', 'https://www.shure.com', verified=False, mm=(130, 45))
for pn, d in [('ANI4IN-XLR', 'in'), ('ANI4OUT-XLR', 'out')]:
    add('dante-adapters.json', 'shure-' + pn.lower(), 'Shure', pn, pn + ' 4-channel Dante audio network interface (%s)' % ('inputs' if d == 'in' else 'outputs'), 'ANI', 'audio', 1,
        [R('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)'), R(d, 'Analog audio', 'XLR3F' if d == 'in' else 'XLR3M', 4, 'Mic / Line In' if d == 'in' else 'Line Out')],
        'Half-rack box (rack tray holds two), PoE powered. Check: width.', 'Shure ANI range', 'https://www.shure.com', verified=False, w=6)
dongle('dante-adapters.json', 'focusrite-rednet-am2', 'Focusrite', 'RedNet AM2', 'RedNet AM2 Dante stereo headphone / line output', 'RedNet',
       [R('in', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)'), F('out', 'Analog audio', '1/4in and 3.5mm jack', 1, 'Headphones'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out')], 'none', '',
       'Desktop monitoring box, PoE powered. Check: connectors.', 'Focusrite RedNet range', 'https://focusrite.com/rednet', verified=False, mm=(130, 45))
dongle('dante-adapters.json', 'focusrite-rednet-x2p', 'Focusrite', 'RedNet X2P', 'RedNet X2P Dante 2 x 2 with mic preamps', 'RedNet',
       [R('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)'), F('in', 'Analog audio', 'XLR / jack combo', 2, 'Mic / Line In'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out'),
        F('out', 'Analog audio', '1/4in jack', 1, 'Headphones')], 'none', '',
       'Desktop 2 x 2 interface, PoE powered. Check: connectors.', 'Focusrite RedNet range', 'https://focusrite.com/rednet', verified=False, mm=(170, 50))
for pn, nm, ports in [('unDX2IO+', 'unDX2IO+ Dante 2 x 2 XLR wall plate', [R('in', 'Analog audio', 'XLR3F', 2, 'Mic / Line In'), R('out', 'Analog audio', 'XLR3M', 2, 'Line Out')]),
                      ('unD6IO', 'unD6IO Dante 4 x 2 wall plate (XLR, RCA, 3.5 mm)', [R('in', 'Analog audio', 'XLR3F', 2, 'Mic / Line In'), R('in', 'Analog audio', 'RCA', 2, 'RCA In'),
                                                                                        R('out', 'Analog audio', 'Euroblock', 2, 'Line Out')])]:
    add('dante-adapters.json', 'attero-' + pn.lower().replace('+', 'plus'), 'Attero Tech (QSC)', pn, nm, 'unD', 'wallbox', 1, [R('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)')] + ports,
        'Decora wall plate, PoE powered. Check: connectors.', 'Attero Tech unD range', 'https://www.atterotech.com', verified=False, w=1)

for models in FILES.values():
    for m in models:
        m['portGroups'] = [p for p in m['portGroups'] if p['count'] > 0]
        if m.get('powerW') is None: m.pop('powerW', None)
for f, models in FILES.items():
    for m in models:
        if m.get('card') and m['card'].get('onlySlots') is None: m['card'].pop('onlySlots', None)
    json.dump(models, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w'), indent=1)
print(sum(len(v) for v in FILES.values()), 'models in', len(FILES), 'files')
