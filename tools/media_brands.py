#!/usr/bin/env python3
"""Generates the rack-mount ranges for contribution, codec, storage and post brands (2026-11-11):
tieline.json, haivision.json, dejero.json, liveu.json, avid.json and synology.json.
Tieline Gateway, Dejero WayPoint, Avid NEXIS | E4 and Synology SA3400 were first added by misc_brands.py; their ids are kept here.
AWS Elemental lives in streaming.py (awselemental.json).
verified=False and a 'Check:' note mark anything not confirmed from a maker's document."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, pre, mfr, id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=pre + id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m); return m
AA, ETH, USB, PWR = 'Analog audio', 'Ethernet', 'USB', 'Power'

# =====================================================================================
# Tieline
# =====================================================================================
TL = lambda *a, **k: add('tieline.json', 'tieline-', 'Tieline', *a, **k)
TCMP = 'Tieline G5/G6 codec comparison v10 (May 2026)'
TCMP_URL = 'https://tieline.com/wp-content/uploads/bsk-pdf-manager/2026/05/Tieline-G5-G6-Codec-Comparison-v10_-20260528-1.pdf'
GW_CHECK = ('Check: how many RJ45 sockets carry the analog and AES3 channels, and the Control Port (GPIO) connector type; '
            'the maker lists channel counts, not sockets.')
def gateway(id, pn, name, ana, aes, gpio, notes, url):
    TL(id, pn, name, 'Gateway', 'audio', 1,
       [R('io', AA, 'RJ45', 2, 'Analog I/O'), R('io', 'AES/EBU', 'RJ45', 2, 'AES3 I/O'), R('io', 'Dante/AES67', 'RJ45', 2, 'AoIP'),
        R('io', ETH, 'RJ45', 2, 'LAN (WAN)'), R('io', 'Other', 'Other', 1, f'Control Port ({gpio} GPIO)'), R('io', USB, 'USB-A', 1, 'USB'),
        R('in', PWR, 'IEC', 2, 'AC In'), F('io', 'Other', 'Card slot', 1, 'SD card')],
       f'1RU, 300 mm deep plus connectors, 4 kg. {notes} {ana} analog and {aes} AES3 channels in and out on RJ45, dual AoIP ports '
       f'(AES67, ST 2110-30, ST 2022-7, Livewire+, RAVENNA; Dante or WheatNet-IP by option card), dual Gigabit LAN with automatic '
       f'redundancy (SmartStream Plus), {gpio} GPIO on the Control Port, dual internal PSUs with two IEC inlets, front LCD, meters and '
       f'keypad. {GW_CHECK}', 'Tieline Gateway product page; ' + TCMP, url, verified=False)
gateway('gateway', 'TLR6200-16', 'Gateway 8/16 multichannel IP audio codec', 8, 16, 16,
        'Up to 16 stereo / 32 mono codec streams (Gateway 16, TLR6200-16; the Gateway 8, TLR6200-8, is the same chassis licensed for '
        '8 stereo streams).', 'https://www.tieline.com/gateway/')
gateway('gateway4', 'Gateway 4', 'Gateway 4 IP audio codec', 4, 4, 8,
        'Up to 4 stereo / 8 mono codec streams.', 'https://www.tieline.com/gateway/')
gateway('gateway-nexus', 'Gateway Nexus', 'Gateway Nexus multichannel IP audio codec', 8, 16, 16,
        'Up to 32 bidirectional mono / 16 stereo channels, built for AoIP-to-WAN bridging in large facilities.',
        'https://tieline.com/?p=14613')
for id, pn, name, dual, url in [('bridge-it-ii', 'TLB6150', 'Bridge-IT II IP audio codec', False, 'https://www.tieline.com/bridge-it-ii/'),
                                ('bridge-it-xtra-ii', 'TLB6150-XTRA', 'Bridge-IT XTRA II IP audio codec', True,
                                 'https://www.tieline.com/bridge-it-ii/')]:
    TL(id, pn, name, 'Bridge-IT', 'audio', 1,
       [R('in', AA, 'XLR3F', 2, 'Analog In'), R('out', AA, 'XLR3M', 2, 'Analog Out'), R('in', 'AES/EBU', 'XLR3F', 1, 'AES3 In'),
        R('out', 'AES/EBU', 'RJ45', 1, 'AES3 Out'), R('io', ETH, 'RJ45', 2, 'LAN (LAN2 = AoIP)'), R('io', 'Other', 'Other', 1, 'GPIO (4)'),
        R('io', USB, 'USB-A', 1, 'USB (cellular)')] + ([R('in', PWR, 'IEC', 1, 'AC In'), R('in', PWR, 'DC barrel', 1, '12V DC In')] if dual
                                                     else [R('in', PWR, 'DC barrel', 1, '12V DC In')]),
       '1RU stereo IP codec for STL and remote broadcast links: 2 analog XLR in and out, AES3 in on XLR and out on RJ45, dual Gigabit '
       'Ethernet with LAN2 switchable to AES67 / ST 2110-30 / Livewire+, 4 relay GPI and 4 opto GPO, USB cellular port. '
       + ('XTRA adds a second, redundant power input and extra algorithms. ' if dual else 'Powered by a 12 V DC plug-pack. ')
       + 'Check: GPIO connector type and which AES3 output connector your unit uses.', TCMP, url, verified=False)
TL('mpx-ii', 'MPX II', 'MPX II FM composite (MPX) IP codec', 'MPX', 'audio', 1,
   [R('in', 'Other', 'BNC', 2, 'MPX In'), R('out', 'Other', 'BNC', 2, 'MPX Out'), R('in', AA, 'XLR3F', 2, 'Analog In'),
    R('out', AA, 'XLR3M', 2, 'Analog Out'), R('io', 'AES/EBU', 'XLR', 2, 'AES3/AES192 I/O'), R('io', ETH, 'RJ45', 2, 'LAN'),
    R('io', 'Other', 'Other', 1, 'GPIO'), R('in', PWR, 'IEC', 2, 'AC In')],
   '1RU codec that carries FM composite (MPX) plus RDS over IP to transmitter sites with low bit rates. MPX I is the single-program '
   'version. Check: MPX, AES192 and analog connector counts and the PSU arrangement (from the MPX brochure, not confirmed on a rear-panel drawing).',
   'Tieline MPX brochure (Feb 2026)', 'https://tieline.com/wp-content/uploads/bsk-pdf-manager/2026/04/MPX-16th-Feb-2026-v7_4_English.pdf', verified=False)
for id, pn, name, notes in [
        ('merlin-plus', 'Merlin PLUS', 'Merlin PLUS multi-stream IP codec (legacy)',
         'Up to 6 mono / 3 stereo IP streams for talk-show and network distribution.'),
        ('genie-distribution', 'Genie Distribution', 'Genie Distribution multi-stream IP codec (legacy)',
         'Up to 6 mono / 3 stereo IP streams for program distribution.'),
        ('genie-stl', 'Genie STL', 'Genie STL studio-to-transmitter IP codec (legacy)',
         'Stereo STL codec with redundant streaming (SmartStream Plus) and dual PSUs.')]:
    TL(id, pn, name, 'Genie / Merlin', 'audio', 1,
       [R('in', AA, 'XLR3F', 2, 'Analog In'), R('out', AA, 'XLR3M', 2, 'Analog Out'), R('in', 'AES/EBU', 'XLR3F', 1, 'AES3 In'),
        R('out', 'AES/EBU', 'XLR3M', 1, 'AES3 Out'), R('io', ETH, 'RJ45', 2, 'LAN'), R('io', 'Other', 'DB15', 1, 'GPIO'),
        R('io', USB, 'USB-A', 1, 'USB'), R('in', PWR, 'IEC', 2, 'AC In')],
       f'1RU G5-generation IP audio codec, replaced by the Gateway and Bridge-IT II families. {notes} '
       'Check: rear connector counts (from the G5 range description, not a rear-panel drawing) and whether the second PSU is fitted.',
       'Tieline G5 range information', 'https://www.tieline.com/', verified=False)

# =====================================================================================
# Haivision
# =====================================================================================
HV = lambda *a, **k: add('haivision.json', 'haivision-', 'Haivision', *a, **k)
MX4_DS = 'Haivision Makito X4 series datasheets'
MX4_URL = 'https://doc.haivision.com/MakitoX4Enc/1.9/chassis-styles'
MX4_CHECK = ('Check: connector type on the SDI ports (BNC assumed), and whether the second RJ45 and the SFP+ (ST 2110 licence) are fitted.')
def mx4_ports(dirn, uhd):
    t = '12G-SDI' if uhd else '3G-SDI'
    return [R(dirn, t, 'BNC', 4, 'SDI ' + ('In' if dirn == 'in' else 'Out')), R('io', ETH, 'RJ45', 1, 'Network'),
            R('io', 'SFP', 'SFP+', 1, '10G SFP+ (ST 2110)'), R('io', 'RS-422', 'Other', 1, 'Serial (RS-232/422)')]
for kind, dirn in (('enc', 'in'), ('dec', 'out')):
    for uhd in (False, True):
        role = 'encoder' if kind == 'enc' else 'decoder'
        sku = f"MX4{'E' if kind == 'enc' else 'D'}-SDI4{'-UHD' if uhd else ''}"
        label = f"Makito X4 {'4K UHD' if uhd else 'HD'} {role}"
        HV(f'makito-x4-{kind}{"-uhd" if uhd else ""}', 'S-' + sku, f'{label} appliance', 'Makito X4', 'converter', 1,
           mx4_ports(dirn, uhd) + [R('in', PWR, '12V DC', 1, 'DC In')],
           f'Ultra-compact appliance, 24 x 152 x 192 mm (H x W x D), 12 V DC 18 W from an external supply. Four SDI '
           f'{"inputs" if dirn == "in" else "outputs"} ({"12G-SDI / quad-link UHD" if uhd else "3G/HD/SD"}), single, dual or quad channel '
           f'H.264/HEVC with SRT. Rack it with the RU-MB1-1 / RU-MB1-2 1RU brackets, or order it as blade B-{sku} for the MB6X / MB21X '
           f'chassis. {MX4_CHECK}', MX4_DS, MX4_URL, verified=False, w=4)

# MB6X and MB21X chassis take Makito X / X4 blades (single- or dual-height). Modelled as frames with flat slots in 3 columns.
def hv_frame(id, pn, name, ru, slots, ports, notes):
    m = HV(id, pn, name, 'Makito blade chassis', 'frame', ru, ports, notes, MX4_DS, MX4_URL, verified=False, full=True)
    m['frame'] = dict(system='Haivision MB', slots=slots, slotOrder='ltr', rearAlign=1, door=False, orient='h', cols=3,
                      controller='None: each blade has its own network port and web interface',
                      front={'x0': 0.06, 'x1': 0.94, 'y0': 0.06, 'y1': 0.94}, rear={'x0': 0.04, 'x1': 0.96, 'y0': 0.06, 'y1': 0.94})
hv_frame('mb6x', 'F-MB6X-RAC', 'MB6X 1RU 6-slot blade chassis', 1, 6, [R('in', PWR, 'IEC', 2, 'AC In')],
         '1RU chassis for up to 6 single-height (or 3 dual-height) Makito X / X4 encoder and decoder blades, 300 W. F-MB6X-RAC has '
         'redundant AC supplies (90-264 VAC); F-MB6X-DC takes 20-36 VDC. Blades shown as 3 columns of 2. '
         'Check: blade orientation and slot numbering, and whether the blade connectors face the rear.')
hv_frame('mb21x', 'F-MB21X-R', 'MB21X 4RU 21-slot blade chassis', 4, 21, [R('in', PWR, 'IEC', 2, 'AC In')],
         '4RU chassis for up to 21 single-height (or 10 dual-height) Makito X / X4 encoder and decoder blades, redundant dual AC '
         'supplies, 100-240 VAC, 600 W. Blades shown as 3 columns of 7. '
         'Check: blade orientation and slot numbering, and whether the blade connectors face the rear.')
for kind, dirn in (('enc', 'in'), ('dec', 'out')):
    for uhd in (False, True):
        sku = f"B-MX4{'E' if kind == 'enc' else 'D'}-SDI4{'-UHD' if uhd else ''}"
        m = HV(f'blade-mx4{kind[0]}{"-uhd" if uhd else ""}', sku,
               f"Makito X4 {'4K UHD' if uhd else 'HD'} {'encoder' if kind == 'enc' else 'decoder'} blade", 'Makito X4', 'card', 0, [],
               'Blade version of the Makito X4 appliance for the MB6X and MB21X chassis (single-height). ' + MX4_CHECK,
               MX4_DS, MX4_URL, verified=False, w=0)
        m['card'] = dict(fits=['Haivision MB'], slotWidth=1)
        m['rearModules'] = [dict(partNumber=sku, name='Blade connectors', width=1, cardsPerModule=1, cardOffset=0, default=True,
                                 portGroups=mx4_ports(dirn, uhd), layout={'cols': 6}, included=True)]
SH_URL = 'https://doc.haivision.com/StreamHub/4.4/hardware-requirements'
SRV = [R('io', ETH, 'RJ45', 2, '1GbE'), R('io', ETH, 'RJ45', 1, 'IPMI'), R('out', 'Other', 'VGA', 1, 'VGA'), R('io', USB, 'USB-A', 2, 'USB')]
for id, pn, name, io, notes in [
        ('streamhub-std-4sdi', 'StreamHub STD-4SDI', 'StreamHub receiver / decoder, Standard 4 x SDI',
         [R('io', '3G-SDI', 'BNC', 4, 'SDI In/Out (DeckLink Duo 2)')], 'Xeon E-2176G, DeckLink Duo 2 card (STD-1SDI uses a DeckLink Mini Monitor 4K).'),
        ('streamhub-ult-8hd', 'StreamHub ULT-8HD', 'StreamHub receiver / decoder, Ultra 8 x HD',
         [R('io', '3G-SDI', 'BNC', 8, 'SDI In/Out (DeckLink Quad 2)')], 'Xeon Gold 6226R, DeckLink Quad 2 card.'),
        ('streamhub-ult-4kmhd', 'StreamHub ULT-4KMHD', 'StreamHub receiver / decoder, Ultra 4K / multi-HD',
         [R('io', '12G-SDI', 'BNC', 4, 'SDI In/Out (DeckLink 8K Pro)'), R('in', 'Reference', 'BNC', 1, 'Ref In')],
         'Xeon Gold 6226R, DeckLink 8K Pro card.'),
        ('streamhub-st2110', 'StreamHub STD/ULT-ST2110', 'StreamHub receiver / decoder, ST 2110',
         [R('io', 'SFP', 'SFP', 2, '25GbE SFP28 (ConnectX-6 Lx)')], 'Mellanox ConnectX-6 Lx NIC for ST 2110 in and out.')]:
    HV(id, pn, name, 'StreamHub', 'converter', 1, io + SRV + [R('in', PWR, 'IEC', 1, 'AC In')],
       f'1RU server (Supermicro CSE-514 chassis) running StreamHub: receives SRT / SST bonded-cellular feeds from Haivision Pro and Air '
       f'transmitters and outputs SDI, NDI, SRT or ST 2110. {notes} Single PSU. Check: card I/O direction set in software, and onboard '
       f'NIC count of your build.', 'Haivision StreamHub hardware requirements', SH_URL, verified=False, full=True)
for n, notes in [(200, 'HD, H.264, 4 audio channels.'), (300, 'HD, HEVC/H.264, 4 audio channels.'),
                 (400, '4K UHD or up to 4 HD feeds, HEVC/H.264, 8 audio channels.')]:
    sdi = 4 if n == 400 else 1
    HV(f'rack{n}', f'Rack{n}', f'Rack{n} contribution encoder (half-rack)', 'Rack series', 'converter', 1,
       [R('in', '12G-SDI' if n == 400 else '3G-SDI', 'BNC', sdi, 'SDI In'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
        R('out', 'HDMI', 'HDMI', 1, 'HDMI Out (return)'), R('io', ETH, 'RJ45', 2, 'Ethernet'), R('io', USB, 'USB-A', 2, 'USB (modems)'),
        R('in', PWR, 'Other', 1, 'Power In')],
       f'Compact half-width 1RU encoder (ex AVIWEST); a kit fits one or two in 1RU. {notes} Ethernet, Wi-Fi, satellite and cellular '
       '(Quad CellLink) bonding, HDMI return-feed output, SD card recording. Check: SDI and HDMI input counts, Ethernet ports and power '
       'connector (not given on the product page).', 'Haivision Rack product page', 'https://www.haivision.com/products/rack-video-encoder/',
       verified=False, w=6)

# =====================================================================================
# Dejero
# =====================================================================================
DJ = lambda *a, **k: add('dejero.json', 'dejero-', 'Dejero', *a, **k)
DJ('waypoint', 'WayPoint', 'WayPoint receiver (101 / 102 / 104)', 'WayPoint', 'converter', 1,
   [R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
    R('io', ETH, 'RJ45', 2, 'Network'), R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 2, 'AC In')],
   '1RU receiver that decodes and reassembles Dejero transmitter (EnGo, PathWay) streams and outputs SDI/HDMI or IP (NDI, SRT, RTMP). '
   'Models 101, 102 and 104 differ in decode channels; dual PSUs. Check: model and SDI output count on your unit.',
   'Dejero WayPoint 104 product brief', 'https://www.dejero.com/products/waypoint-104', verified=False, full=True)
DJ('waypoint-3', 'WayPoint 3', 'WayPoint 3 four-output receiver', 'WayPoint', 'converter', 1,
   [R('out', '12G-SDI', 'BNC', 4, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'), R('io', ETH, 'RJ45', 2, 'Network'),
    R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 2, 'AC In')],
   'Current Dejero receiver: up to 4 HD or 2 4K UHD sources at once, SDI or MPEG-TS outputs, front-access 1 TB drives with RAID, '
   'redundant power supplies. Check: rack height (1RU assumed), SDI output type and count, and network ports.',
   'Dejero WayPoint product page', 'https://www.dejero.com/waypoint', verified=False, full=True)
DJ('pathway', 'PathWay', 'PathWay rack-mount encoder / transmitter', 'PathWay', 'converter', 1,
   [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('io', ETH, 'RJ45', 2, 'Network'),
    R('io', USB, 'USB-A', 4, 'USB (modems)'), R('in', PWR, 'IEC', 1, 'AC In')],
   '1RU fixed-location encoder that sends HEVC/H.264 to WayPoint receivers over blended Ethernet, cellular and satellite links. '
   'Check: SDI input count, loop output, USB modem ports and PSU count.',
   'Dejero PathWay / WayPoint HEVC release', 'https://tvtechnology.com/equipment/dejero-releases-pathway-waypoint-for-hevc-support',
   verified=False, full=True)

# =====================================================================================
# LiveU
# =====================================================================================
LU = lambda *a, **k: add('liveu.json', 'liveu-', 'LiveU', *a, **k)
LU2K = 'https://www.liveu.tv/wp-content/uploads/2021/02/LU2000_Feb2021.pdf'
for n, sku in ((1, 'LU10-SV-1UL01'), (2, 'LU10-SV-1UL02'), (4, 'LU10-SV-1UL04')):
    LU(f'lu2000-{n}', sku, f'LU2000 server, {n} x SDI out', 'LU2000', 'converter', 1,
       [R('out', '3G-SDI', 'BNC', n, 'SDI Out'), R('io', ETH, 'RJ45', 2, '1GbE'), R('out', 'Other', 'VGA', 1, 'VGA'),
        R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 1, 'AC In')],
       f'1RU receiver / decoder server, 43 x 437 x 503 mm, 9.5 kg, 110-240 V. Receives bonded LiveU field-unit feeds and plays them out '
       f'on {n} SD/HD/3G-SDI output{"s" if n > 1 else ""}; 2 x 10/100/1000 Ethernet. Check: VGA/USB server ports and whether a '
       'second PSU is fitted.', 'LiveU LU2000 datasheet (Feb 2021)', LU2K, verified=False, full=True)
LU('lu4000', 'LU10-SV-1UL04-4K', 'LU4000 server, single 4K / quad HD out', 'LU4000', 'converter', 1,
   [R('out', '12G-SDI', 'BNC', 4, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'), R('io', ETH, 'RJ45', 2, '1GbE'),
    R('out', 'Other', 'VGA', 1, 'VGA'), R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 2, 'AC In')],
   '1RU HEVC receiver / decoder server: one 4K UHD output (quad-link or 12G) or up to 4 HD outputs. '
   'Check: 12G vs quad-link 3G outputs, genlock input and PSU count.', 'LiveU LU4000 dealer listings',
   'https://www.adorama.com/lu10sv1ul04.html', verified=False, full=True)
LU('lu4000-st2110', 'LU10-SV-1UL04-ST2110', 'LU4000 ST 2110 server', 'LU4000', 'converter', 1,
   [R('io', 'SFP', 'SFP', 2, 'ST 2110 (25GbE)'), R('io', ETH, 'RJ45', 2, '1GbE'), R('out', 'Other', 'VGA', 1, 'VGA'),
    R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 2, 'AC In')],
   '1RU LU4000 decoder that outputs uncompressed SMPTE ST 2110 instead of SDI (a dual-output version is LU10-SV-1UD04-ST2110). '
   'Check: SFP speed and count.', 'LiveU LU4000 ST 2110 dealer listings',
   'https://www.bhphotovideo.com/c/product/1889662-REG/liveu_lu10_sv_1ul04_st2110_lu4000_st_2110_single.html', verified=False, full=True)

# =====================================================================================
# Avid
# =====================================================================================
AV = lambda *a, **k: add('avid.json', 'avid-', 'Avid', *a, **k)
NX = 'Avid NEXIS family datasheet'
NX_URL = 'https://www.avid.com/products/avid-nexis/storage-and-specs'
AV('nexis-e4', 'NEXIS | E4', 'NEXIS E4 storage engine', 'NEXIS', 'computer', 4,
   [R('io', ETH, 'QSFP', 2, '40GbE'), R('io', 'SFP', 'SFP+', 4, '10GbE'), R('io', ETH, 'RJ45', 2, 'Management'),
    R('in', PWR, 'IEC', 2, 'PSU')],
   '4U shared-storage engine for Avid NEXIS with 60 drive slots (top-loading drawers), two controllers with redundant PSUs. '
   'Check: controller network ports for your build (10/40/100GbE) and whether a System Director / NEXIS | E2 sits alongside.',
   'Avid NEXIS product information', 'https://www.avid.com/products/avid-nexis', verified=False, full=True)
for id, pn, name, ru, net, notes, v in [
        ('nexis-pro-plus', 'NEXIS | PRO+', 'NEXIS PRO+ storage engine', 2, [R('io', 'SFP', 'SFP', 2, '10/25GbE SFP28')],
         '2U entry engine, one 40 TB Media Pack, two hot-swap SSDs for configuration and metadata, embedded System Director.', True),
        ('nexis-f2', 'NEXIS | F2', 'NEXIS F2 storage engine', 2, [R('io', 'SFP', 'SFP', 2, '10/25GbE SFP28')],
         '2U engine, one Media Pack (60, 100 or 140 TB HDD), two hot-swap SSDs, embedded System Director, optional redundant controller.', True),
        ('nexis-f2x', 'NEXIS | F2X', 'NEXIS F2X expansion chassis', 2, [R('io', 'Other', 'Other', 2, 'Expansion link')],
         '2U expansion for an F2 engine, one Media Pack (60, 100 or 140 TB HDD), optional hot-spare HDDs. Check: expansion cable type.', False),
        ('nexis-f2-ssd', 'NEXIS | F2 SSD', 'NEXIS F2 SSD all-flash engine', 2, [R('io', ETH, 'QSFP28', 2, '100GbE')],
         '2U all-flash engine, 1-2 SSD Media Packs (38.4 or 153.6 TB), mirrored config SSDs, embedded System Director, optional '
         'redundant controller. Check: 100GbE connector (QSFP28 assumed).', False),
        ('nexis-f5', 'NEXIS | F5', 'NEXIS F5 storage engine', 5, [R('io', ETH, 'QSFP', 2, '50GbE QSFP+')],
         '5U engine, 4-8 Media Packs (60, 100 or 140 TB HDD), 2 hot-spare HDDs, 2 hot-swap SSDs, optional redundant controller.', True),
        ('nexis-f5-nl', 'NEXIS | F5 NL', 'NEXIS F5 NL nearline engine', 5, [R('io', 'SFP', 'SFP', 2, '10GbE SFP28')],
         '5U nearline engine, 4-8 Media Packs of 160 TB, mirrored config SSDs, optional redundant controller.', True)]:
    AV(id, pn, name, 'NEXIS', 'computer', ru, net + [R('io', ETH, 'RJ45', 1, 'Management'), R('in', PWR, 'IEC', 2, 'PSU')],
       notes + ' Redundant power and cooling. Check: management port and the number of data ports per controller.', NX, NX_URL,
       verified=False, full=True)
for id, pn, name, ru, notes in [
        ('nexis-e2', 'NEXIS | E2', 'NEXIS E2 storage engine (legacy)', 4,
         'Earlier NEXIS engine for mid-size systems, replaced by the F-series. Check: rack height, drive count and controller ports.'),
        ('nexis-e5', 'NEXIS | E5', 'NEXIS E5 storage engine (legacy)', 5,
         'Earlier high-capacity NEXIS engine (E5 NL is the nearline version), replaced by the F5. Check: rack height and controller ports.')]:
    AV(id, pn, name, 'NEXIS', 'computer', ru,
       [R('io', 'SFP', 'SFP+', 4, '10GbE'), R('io', ETH, 'QSFP', 2, '40GbE'), R('io', ETH, 'RJ45', 2, 'Management'), R('in', PWR, 'IEC', 2, 'PSU')],
       notes, 'Avid NEXIS product information', NX_URL, verified=False, full=True)
AV('nexis-sda', 'NEXIS | SDA', 'NEXIS System Director Appliance', 'NEXIS', 'computer', 1,
   [R('io', ETH, 'RJ45', 2, '1GbE'), R('io', 'SFP', 'SFP+', 2, '10GbE'), R('io', ETH, 'RJ45', 1, 'iDRAC'), R('out', 'Other', 'VGA', 1, 'VGA'),
    R('io', USB, 'USB-A', 2, 'USB'), R('in', PWR, 'IEC', 2, 'PSU')],
   '1U server that runs the NEXIS System Director for systems whose engines have no embedded director (E-series). '
   'Check: server model and ports (shown as a typical 1U Dell server).', 'Avid NEXIS product information', NX_URL, verified=False, full=True)
MTRX = 'Avid Pro Tools MTRX family comparison chart'
MTRX_URL = 'https://www.avid.com/products/pro-tools-mtrx-ii/specifications'
def mtrx(id, pn, name, dante, notes, extra):
    AV(id, pn, name, 'Pro Tools | MTRX', 'audio', 2,
       [R('io', 'Other', 'Other', 2, 'DigiLink Mini'), R('io', 'MADI audio', 'Other', 1, 'MADI (64 ch)')] + extra +
       [R('io', 'Other', 'Card slot', 8, 'Option card slot'), R('in', 'Reference', 'BNC', 1, 'Word clock / VBB In'),
        R('out', 'Reference', 'BNC', 1, 'Word clock Out'), R('io', ETH, 'RJ45', 1, 'Control'), R('in', PWR, 'IEC', 2, 'AC In')],
       f'2U Pro Tools HD interface and monitor controller: 2 x 32-channel DigiLink Mini (64 ch), 64-channel MADI built in, {dante}, '
       f'8 option card slots (analog, AES, Dante, MADI, SPQ, Thunderbolt 3 module). {notes} '
       'Check: MADI connector type, word clock BNC count and whether the second PSU is fitted.', MTRX, MTRX_URL, verified=False, full=True)
mtrx('mtrx-ii', 'MTRX II', 'Pro Tools | MTRX II audio interface', '256-channel Dante built in',
     'Current model; 8 AES3 and Dual MADI are option cards.', [R('io', 'Dante/AES67', 'RJ45', 2, 'Dante (256 ch)')])
mtrx('mtrx', 'MTRX', 'Pro Tools | MTRX audio interface (discontinued)', 'Dante by option card',
     'Built-in 8 AES pairs on two DB25.', [R('io', 'AES/EBU', 'DB25', 2, 'AES3 (8 pairs)'), R('in', 'AES/EBU', 'BNC', 1, 'AES11 In')])
AV('mtrx-studio', 'MTRX Studio', 'Pro Tools | MTRX Studio audio interface', 'Pro Tools | MTRX', 'audio', 1,
   [F('in', AA, 'XLR3F', 2, 'Mic In'), R('in', AA, 'DB25', 2, 'Line In (16)'), R('out', AA, 'DB25', 2, 'Line Out (16)'),
    R('out', AA, '1/4" TRS', 2, 'Monitor Out'), F('out', AA, '6.3mm TRS', 2, 'Headphone'), R('io', 'Other', 'Other', 2, 'DigiLink Mini'),
    R('io', 'Dante/AES67', 'RJ45', 2, 'Dante (64 ch)'), R('in', 'Reference', 'BNC', 1, 'Word clock In'),
    R('out', 'Reference', 'BNC', 1, 'Word clock Out'), R('io', 'Other', 'Card slot', 1, 'Thunderbolt 3 module'), R('in', PWR, 'IEC', 1, 'AC In')],
   '1U interface: 2 mic preamps, 16 x 16 line I/O on DB25, 2 monitor outputs, 2 headphone outputs, 64-channel Dante, 2 DigiLink '
   'Mini ports, optional Thunderbolt 3 module (64 ch), word clock and Loop Sync. Check: front/rear position of the mic inputs.',
   MTRX, 'https://www.avid.com/products/pro-tools-mtrx-studio/specifications', verified=False, full=True)
for id, pn, name, ru, ports, notes in [
        ('hd-io', 'HD I/O', 'Pro Tools | HD I/O interface (legacy)', 2,
         [R('in', AA, 'DB25', 1, 'Analog In (8)'), R('out', AA, 'DB25', 1, 'Analog Out (8)'), R('io', 'AES/EBU', 'DB25', 1, 'AES/EBU (8)'),
          R('io', 'Other', 'Other', 2, 'ADAT optical'), R('io', 'AES/EBU', 'RCA', 2, 'S/PDIF'), R('io', 'Reference', 'BNC', 2, 'Word clock In/Out'),
          R('io', 'Reference', 'BNC', 2, 'Loop Sync In/Out'), R('io', 'Other', 'Other', 2, 'DigiLink (Primary/Expansion)'),
          R('in', PWR, 'IEC', 1, 'AC In')],
         '2U Pro Tools HD interface with 8 x 8 x 8 I/O (analog / AES / ADAT) as standard; analog and digital expansion cards change the mix.'),
        ('hd-omni', 'HD OMNI', 'Pro Tools | HD OMNI interface (legacy)', 1,
         [F('in', AA, 'XLR3F', 2, 'Mic/Line In'), R('in', AA, 'DB25', 1, 'Line In'), R('out', AA, 'DB25', 1, 'Line Out'),
          R('out', AA, '1/4" TRS', 2, 'Monitor Out'), F('out', AA, '6.3mm TRS', 1, 'Headphone'), R('io', 'AES/EBU', 'XLR', 2, 'AES/EBU In/Out'),
          R('io', 'Other', 'Other', 2, 'ADAT optical'), R('io', 'Reference', 'BNC', 2, 'Word clock / Loop Sync'),
          R('io', 'Other', 'Other', 2, 'DigiLink'), R('in', PWR, 'IEC', 1, 'AC In')],
         '1U all-in-one Pro Tools HD interface with 2 mic preamps, monitoring and headphone output.'),
        ('hd-madi', 'HD MADI', 'Pro Tools | HD MADI interface (legacy)', 1,
         [R('io', 'MADI audio', 'BNC', 2, 'MADI coax In/Out'), R('io', 'MADI audio', 'Other', 2, 'MADI optical (SC)'),
          R('io', 'Reference', 'BNC', 2, 'Word clock In/Out'), R('io', 'Reference', 'BNC', 2, 'Loop Sync In/Out'),
          R('io', 'Other', 'Other', 2, 'DigiLink'), R('in', PWR, 'IEC', 1, 'AC In')],
         '1U 64-channel MADI interface for Pro Tools HD.'),
        ('sync-x', 'Sync X', 'Pro Tools | Sync X synchroniser', 1,
         [R('in', 'Reference', 'BNC', 1, 'Video Ref In'), R('out', 'Reference', 'BNC', 1, 'Video Ref Loop'), R('in', 'Timecode', 'XLR', 1, 'LTC In'),
          R('out', 'Timecode', 'XLR', 1, 'LTC Out'), R('out', 'Reference', 'BNC', 4, 'Word clock Out'), R('io', 'Reference', 'BNC', 2, 'Loop Sync'),
          R('io', 'RS-422', 'DB9', 1, '9-pin'), R('io', USB, 'USB-B', 1, 'USB'), R('in', PWR, 'IEC', 1, 'AC In')],
         '1U Pro Tools synchroniser: video reference, LTC, word clock and Loop Sync.'),
        ('artist-dnxiq', 'Artist | DNxIQ', 'Artist | DNxIQ video I/O', 1,
         [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In'),
          R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('in', AA, 'XLR3F', 2, 'Analog In'), R('out', AA, 'XLR3M', 2, 'Analog Out'),
          R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'RS-422', 'DB9', 1, 'Deck control'), R('io', 'Other', 'Other', 2, 'Thunderbolt 3'),
          R('in', PWR, 'IEC', 1, 'AC In')],
         '1U Thunderbolt 3 video interface for Media Composer with 12G-SDI, HDMI 2.0, analog and AES audio.')]:
    AV(id, pn, name, 'Pro Tools' if id != 'artist-dnxiq' else 'Artist', 'audio' if id != 'artist-dnxiq' else 'converter', ru, ports,
       notes + ' Check: connector counts are from memory of the rear panel, not from an Avid drawing.',
       'Avid product information', 'https://www.avid.com/', verified=False, full=True)

# =====================================================================================
# Synology
# =====================================================================================
SY = lambda *a, **k: add('synology.json', 'synology-', 'Synology', *a, **k)
SY('sa3400', 'SA3400', 'SA3400 12-bay rackmount NAS', 'SA series', 'computer', 2,
   [R('io', ETH, 'RJ45', 4, '1GbE'), R('io', ETH, 'SFP+', 2, '10GbE'), R('io', 'Other', 'Card slot', 2, 'PCIe slot'),
    R('io', 'Other', 'Mini-SAS HD', 2, 'Expansion'), R('io', USB, 'USB-A', 2, 'USB 3.2'), R('in', PWR, 'IEC', 2, 'PSU')],
   '2U, 12 x 3.5/2.5 in hot-swap bays, Intel Xeon D-1541, 4 x 1GbE RJ45 and 2 x 10GbE SFP+ onboard, 2 PCIe 3.0 x8 slots, '
   '2 expansion ports for RX1217sas units, redundant PSUs. Rails needed (a support shelf is often fitted under it).',
   'Synology SA3400 datasheet', 'https://www.synology.com/en-global/products/SA3400', full=True)
SYC = 'Check: port counts are from Synology product knowledge, not checked against this model\'s datasheet.'
def syn(model, name, fam, ru, bays, cpu, lan, pcie, exp, psu, extra='', ten=None, sfp=None, exp_conn='Other'):
    ports = [R('io', ETH, 'RJ45', lan, '1GbE')]
    if ten: ports.append(R('io', ETH, 'RJ45', ten, '10GbE'))
    if sfp: ports.append(R('io', ETH, 'SFP+', sfp, '10GbE SFP+'))
    if pcie: ports.append(R('io', 'Other', 'Card slot', pcie, 'PCIe slot'))
    if exp: ports.append(R('io', 'Other', exp_conn, exp, 'Expansion'))
    ports += [R('io', USB, 'USB-A', 2, 'USB 3.2'), R('in', PWR, 'IEC', psu, 'PSU')]
    nets = f'{lan} x 1GbE' + (f' + {ten} x 10GbE RJ45' if ten else '') + (f' + {sfp} x 10GbE SFP+' if sfp else '')
    SY(model.lower().replace('+', '-plus'), model, f'{model} {name}', fam, 'computer', ru, ports,
       f'{ru}U, {bays}, {cpu}, {nets}, {pcie or "no"} PCIe slot{"s" if pcie != 1 else ""}, '
       f'{exp or "no"} expansion port{"s" if exp != 1 else ""}, {"redundant PSUs" if psu == 2 else "single PSU"}. {extra}{SYC}',
       'Synology product information', f'https://www.synology.com/en-global/products/{model}', verified=False, full=model != 'RS422+')
syn('RS422+', '4-bay rackmount NAS', 'RackStation', 1, '4 bays, short depth', 'AMD Ryzen R1600', 2, 0, 0, 1)
syn('RS822+', '4-bay rackmount NAS', 'RackStation', 1, '4 bays', 'AMD Ryzen V1500B', 4, 1, 1, 1, 'Expands with one RX418. ', exp_conn='Other')
syn('RS822RP+', '4-bay rackmount NAS, redundant PSU', 'RackStation', 1, '4 bays', 'AMD Ryzen V1500B', 4, 1, 1, 2, 'Expands with one RX418. ')
syn('RS1221+', '8-bay rackmount NAS', 'RackStation', 2, '8 bays', 'AMD Ryzen V1500B', 4, 1, 1, 1, 'Expands with one RX418. ')
syn('RS1221RP+', '8-bay rackmount NAS, redundant PSU', 'RackStation', 2, '8 bays', 'AMD Ryzen V1500B', 4, 1, 1, 2, 'Expands with one RX418. ')
syn('RS2421+', '12-bay rackmount NAS', 'RackStation', 2, '12 bays', 'AMD Ryzen V1780B', 4, 1, 1, 1, 'Expands with one RX1217. ')
syn('RS2421RP+', '12-bay rackmount NAS, redundant PSU', 'RackStation', 2, '12 bays', 'AMD Ryzen V1780B', 4, 1, 1, 2, 'Expands with one RX1217RP. ')
syn('RS2423+', '12-bay rackmount NAS', 'RackStation', 2, '12 bays', 'AMD Ryzen V1780B', 2, 1, 1, 1, 'Expands with one RX1223RP. ', ten=1)
syn('RS2423RP+', '12-bay rackmount NAS, redundant PSU', 'RackStation', 2, '12 bays', 'AMD Ryzen V1780B', 2, 1, 1, 2,
    'Expands with one RX1223RP. ', ten=1)
syn('RS2821RP+', '16-bay rackmount NAS', 'RackStation', 3, '16 bays', 'AMD Ryzen V1780B', 4, 1, 1, 2, 'Expands with one RX1217RP. ')
syn('RS3621xs+', '12-bay rackmount NAS', 'RackStation', 2, '12 bays', 'Intel Xeon D-1541', 4, 2, 2, 2, 'Expands with up to two RX1217RP. ', ten=2)
syn('RS3621RPxs', '12-bay rackmount NAS', 'RackStation', 2, '12 bays', 'Intel Xeon D-1531', 4, 2, 1, 2, 'Expands with one RX1217RP. ')
syn('RS4021xs+', '16-bay rackmount NAS', 'RackStation', 3, '16 bays', 'Intel Xeon D-1541', 4, 2, 2, 2, 'Expands with up to two RX1217RP. ', ten=2)
syn('SA3410', '12-bay rackmount storage', 'SA series', 2, '12 bays', 'Intel Xeon D-1541', 2, 2, 2, 2,
    'Expands with RX1223RP or RX1225RP units. ', ten=2, exp_conn='Mini-SAS HD')
syn('SA3610', '12-bay rackmount storage', 'SA series', 2, '12 bays', 'Intel Xeon D-1567', 2, 2, 2, 2,
    'Expands with RX1223RP units. ', ten=2, exp_conn='Mini-SAS HD')
syn('SA6400', '12-bay rackmount storage', 'SA series', 2, '12 bays', 'AMD EPYC 7272', 2, 6, 2, 2,
    'Expands with RX1225RP / RX6025sas units. ', ten=2, exp_conn='Mini-SAS HD')
syn('FS2500', '12-bay all-flash storage', 'FlashStation', 1, '12 x 2.5 in SSD bays', 'AMD Ryzen V1780B', 2, 1, 1, 2, ten=2,
    exp_conn='Mini-SAS HD')
syn('FS3410', '24-bay all-flash storage', 'FlashStation', 2, '24 x 2.5 in SSD bays', 'Intel Xeon D-1541', 2, 2, 2, 2, ten=2,
    exp_conn='Mini-SAS HD')
syn('FS6400', '24-bay all-flash storage', 'FlashStation', 2, '24 x 2.5 in SSD bays', '2 x Intel Xeon Silver 4110', 2, 4, 2, 2, ten=2,
    exp_conn='Mini-SAS HD')
syn('HD6500', '60-bay high-density storage', 'HD series', 4, '60 x 3.5 in top-loading bays', '2 x Intel Xeon Silver 4210R', 2, 4, 4, 2,
    'Expands with RX6022sas units. Needs a deep rack (about 1 m). ', ten=2, exp_conn='Mini-SAS HD')
syn('UC3400', 'dual-controller SAN storage', 'UC series', 2, '12 bays, dual active-active controllers', 'Intel Xeon D-1541 per controller',
    4, 2, 2, 2, 'Port counts are for both controllers together. ', ten=4, exp_conn='Mini-SAS HD')
for model, ru, bays, psu, conn, notes in [
        ('RX418', 1, '4 bays', 1, 'Other', 'For RS422+ class 1U and 2U units (eSATA link).'),
        ('RX1217', 2, '12 bays', 1, 'Other', 'For RS2421+ class units.'),
        ('RX1217RP', 2, '12 bays', 2, 'Other', 'For RS2421RP+, RS3621xs+ and RS4021xs+ class units.'),
        ('RX1223RP', 2, '12 bays', 2, 'Mini-SAS HD', 'For RS2423+ / SA3410 class units.'),
        ('RX1217sas', 2, '12 bays (SAS)', 2, 'Mini-SAS HD', 'For SA3400 and FS-series units.'),
        ('RX2417sas', 2, '24 x 2.5 in bays (SAS)', 2, 'Mini-SAS HD', 'For SA and FS-series units.'),
        ('RX6022sas', 4, '60 x 3.5 in bays (SAS)', 2, 'Mini-SAS HD', 'For the HD6500.')]:
    SY(model.lower(), model, f'{model} expansion unit', 'Expansion units', 'computer', ru,
       [R('io', 'Other', conn, 2 if 'sas' in model.lower() or 'RP' in model else 1, 'Expansion In/Out'), R('in', PWR, 'IEC', psu, 'PSU')],
       f'{ru}U drive expansion, {bays}, {"redundant PSUs" if psu == 2 else "single PSU"}. {notes} {SYC}',
       'Synology product information', f'https://www.synology.com/en-global/products/{model}', verified=False, full=ru > 1)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
