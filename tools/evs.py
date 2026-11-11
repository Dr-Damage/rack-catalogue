#!/usr/bin/env python3
"""Generates catalogue/evs.json (EVS rack-mount servers and Neuron processors).
EVS publishes server rear panels only as images (evs.com/backpanel), so server connector counts are
derived from channel counts and the panel's section list and are flagged verified=False."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
OUT = os.path.join(CAT, 'evs.json')
M = []
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=False, w=12, full=True, **kw):
    m = dict(id='evs-' + id, manufacturer='EVS', partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

CHECK = ('Check: EVS shows the rear panel only as a picture (evs.com/backpanel), so the SDI BNC count is set to the channel count '
         'and the control/audio connector counts are estimates. Correct them from your unit.')
def server(id, pn, name, ru, ch, sdi, notes, url, mv=True, sfp=2, extra=()):
    ports = [R('io', sdi, 'BNC', ch, 'SDI Ch (in/out)')]
    if mv: ports += [R('in', '3G-SDI', 'BNC', 2, 'MV Ext In'), R('out', '3G-SDI', 'BNC', 4, 'MV Out')]
    ports += [R('in', 'Reference', 'BNC', 1, 'Genlock'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop'),
              R('in', 'Timecode', 'BNC', 1, 'LTC In'), R('out', 'Timecode', 'BNC', 1, 'LTC Out'),
              R('io', 'RS-422', 'DB9', 6, 'RS-422'), R('io', 'Other', 'DB15', 1, 'GPIO'),
              R('io', 'AES/EBU', 'DA-15', 2, 'AES (DA-15)'), R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Out'),
              R('io', 'Ethernet', 'RJ45', 2, 'PC LAN'), R('io', 'Other', 'BNC', 1, 'XNet')]
    if sfp: ports.append(R('io', 'Ethernet', 'SFP+', sfp, '10GbE'))
    ports += list(extra) + [R('in', 'Power', 'IEC', 2, 'PSU')]
    add(id, pn, name, 'Live production servers', 'recorder', ru, ports, notes + ' ' + CHECK, 'EVS product page and back panel map', url)

server('xt-via', 'XT-VIA', 'XT-VIA live production server', 6, 12, '12G-SDI',
       '6U, 445 x 270 x 689 mm. 12 HD/1080p channels (6 UHD, 2 8K on the special edition, 6 fill/key), each SDI connector set to record or play; '
       '1.5G/3G/12G selectable. Embedded multiviewer (2 external inputs, 4 outputs). 10G SFP+ (100G via XHub-VIA), dual 10G media sharing, '
       'redundant 1G management LAN, XNet, embedded/AES/MADI audio (192 tracks), 18 TB internal, up to 54 TB. Also an IP-panel variant.',
       'https://evs.com/products/live-production-servers/xt-via')
server('xs-via', 'XS-VIA', 'XS-VIA studio production server', 6, 12, '12G-SDI',
       'Studio server on the XT-VIA platform: 12 channels (e.g. 6 rec + 6 play HD, 6 rec 12G UHD), embedded multiviewer (2 in, 4 out), '
       '10G SFP+ (100G option), dual 10G media sharing, redundant 1G management LAN, XNet/XNet-VIA, AES/MADI audio, 18 TB to 54 TB. '
       'Check: rack height (assumed 6U like XT-VIA).', 'https://evs.com/products/live-production-servers/xs-via')
server('xt-go', 'XT-GO', 'XT-GO replay server', 6, 8, '12G-SDI',
       'Entry-level replay server: 8 HD channels (4 UHD, 4 fill/key), 1.5G/3G/12G selectable, embedded multiviewer (2 in, 4 out), '
       '10G SFP+ (ST 2110), dual 10G XNet-GO, redundant 1G management LAN, AES/MADI audio (128 tracks), 11 TB internal (22 TB max). '
       '6U: EVS\'s back-panel picture shows the same chassis as the XT-VIA (two stacked PSUs). Check: rack height on your unit.', 'https://evs.com/products/live-production-servers/xt-go')
server('xt4k', 'XT4K', 'XT4K live production server (legacy)', 6, 12, '12G-SDI',
       '6U, 39 kg with 12 hot-swap drives. 4 codec modules, MADI on every unit, 2 PC LAN, XNet, up to 192 audio channels. Earlier generation still '
       'common in OB trucks.', 'https://evs.com/backpanel/xt4k.html')
server('xs4k', 'XS4K', 'XS4K studio production server (legacy)', 6, 12, '12G-SDI',
       'Studio version of the XT4K platform (6U): channels set to record or play, multiviewer, MADI, 2 PC LAN, XNet. Check: channel count '
       'and rack height (6U as drawn on site drawings).', 'https://evs.com/backpanel')
add('xhub3', 'XHub3', 'XHub3 XNet SDTI network hub', 'Networking', 'network', 1,
    [R('io', 'Other', 'BNC', 8, 'SDTI XNet'), F('io', 'USB', 'USB-A', 1, 'Upgrade USB'), R('in', 'Power', 'IEC', 1, 'Power')],
    '1RU hub for the EVS XNet SDTI network: 8 SDTI in/out connections with 8 branch status LEDs, USB 2 for upgrades. '
    'Check: SDTI connector layout (in/out pairs) and power inlet count.', 'Rental listings (Gravity Media, NEP)',
    'https://www.gravitymedia.com/au/product/evs-xhub-3/', full=False)
add('xfile3', 'XFile3', 'XFile3 media archiving station', 'Media management', 'computer', 2,
    [F('io', 'USB', 'USB-A', 6, 'USB 3'), F('io', 'Other', 'eSATA', 4, 'eSATA'), R('io', 'USB', 'USB-A', 5, 'USB 3'),
     R('io', 'Ethernet', 'RJ45', 2, 'GbE'), R('io', 'Ethernet', 'SFP+', 2, '10GbE'), R('in', 'Power', 'IEC', 2, 'PSU')],
    '2U platform (XF32-4301D) for backing up and restoring clips from EVS servers: 6 front USB 3, 4 front eSATA, 5 rear USB 3, '
    '2 x gigabit Ethernet (jumbo frames), 2 x 10GbE SFP+ (modules not included). Check: PSU count and video outputs.',
    'Rental listing (Gravity Media)', 'https://www.gravitymedia.com/product/evs-xfile3/')
server('xt3-6u', 'XT3 6U', 'XT3 6U server (legacy)', 6, 12, 'HD-SDI',
       'Previous-generation 6U XT3 with multiviewer loop, analog/digital/MADI audio options; configs such as 8 rec + 4 play or 6 rec + 2 play mix.',
       'https://evs.com/backpanel/xt36uMVW.html', sfp=0)

# ---------------- Neuron ----------------
NEU = 'https://evs.com/products/real-time-media-processing/neuron'
def neuron(id, name, sdi):
    b = 2
    ports = []
    if sdi:
        ports += [R('in', '12G-SDI', 'HD-BNC', 8 * b, '12G In'), R('out', '12G-SDI', 'HD-BNC', 8 * b, '12G Out'),
                  R('io', '3G-SDI', 'HD-BNC', 24 * b, '3G I/O')]
    ports += [R('in', 'Reference', 'HD-BNC', b, 'Ref In'), R('out', 'Reference', 'HD-BNC', 2 * b, 'Ref Out'),
              R('io', 'Fibre', 'QSFP28', 2 * b, '100GbE'), R('io', 'SFP', 'SFP+', 4 * b, 'SFP (MADI/10G)'),
              R('io', 'Ethernet', 'RJ45', 3 * b, 'GigE Control'), R('in', 'Power', 'IEC', 2, 'PSU')]
    add(id, 'Neuron 1RU frame' + (' + 2 x NEU-SDI40-BOARD' if sdi else ''), name, 'Neuron', 'converter', 1, ports,
        '1RU Neuron frame with 2 processing boards (NEU-BASE-BOARD), redundant hot-swap PSUs, about 250 W with 2 Bridge boards. Each board: '
        '2 x 100GbE QSFP28 (main/backup), 4 SFP+ (MADI or 10GbE), ref in with 2 loop/ref outs on HD-BNC, 3 GigE (control, GPI/O)'
        + ('; plus the SDI expansion board (8 x 12G in, 8 x 12G out, 24 x 3G bidirectional on HD-BNC, 40 per board)' if sdi else '') +
        '. Identity is set by licence: Bridge (SDI/IP gateway), Convert, Compress (JPEG XS), Shuffle (audio), View (multiviewer). '
        'Broadcast version has I/O at the rear, datacentre version at the front. Check: PSU inlet type and whether 3 GigE ports are per board or per frame.',
        'EVS Neuron product sheet (Oct 2026) and Neuron Bridge V7 datasheet', NEU, verified=True)
neuron('neuron-sdi', 'Neuron 1RU with SDI (2 boards)', True)
neuron('neuron-ip', 'Neuron 1RU IP only (2 boards)', False)

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(OUT, 'w'), indent=1)
print(len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'evs.json' not in idx: idx.append('evs.json')
json.dump(idx, open(ip, 'w')); print(idx)
