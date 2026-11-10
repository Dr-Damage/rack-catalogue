#!/usr/bin/env python3
"""Generates catalogue/vizrt.json (Vizrt / NewTek rack-mount products)."""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'vizrt.json')
M = []
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
def add(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=True, **kw):
    m = dict(id='vizrt-' + id, manufacturer='Vizrt (NewTek)', partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); M.append(m)

add('tricaster-vizion-1ru', 'TriCaster Vizion 1RU', 'TriCaster Vizion 1RU', 'TriCaster', 'switcher', 1,
    [R('io', '12G-SDI', 'HD-BNC', 16, 'SDI I/O'), R('in', 'Reference', 'HD-BNC', 1, 'Genlock'),
     R('out', 'DisplayPort', 'DisplayPort', 4, 'Multiview'), R('io', 'Ethernet', 'RJ45', 1, '10GbE'), R('io', 'Ethernet', 'RJ45', 1, '1GbE'),
     R('io', 'USB', 'USB-A', 7, 'USB 3.2'), R('io', 'USB', 'USB-C', 1, 'USB-C'), R('in', 'Power', 'IEC', 2, 'PSU')],
    '1RU, 25.7 x 17.2 x 1.7 in, 12.1 kg. Up to 16 configurable SDI ports (input or output, up to 8 at 12G) on HD-BNC with BNC pigtails, '
    'genlock per I/O board, 4 DisplayPort multiviewers, 10GbE + 1GbE, redundant 675 W PSUs. Audio is SDI embedded or Dante (licence). '
    'Tally over NDI, GPI via JLCooper eBox. Check: SDI port count for your hardware version and 10GbE connector type.',
    'Vizrt TriCaster Vizion tech specs', 'https://routing.vizrt.com/products/tricaster/vizion/tech-specs/')
add('tricaster-2-elite', 'TC2E3RU', 'TriCaster 2 Elite 3RU', 'TriCaster', 'switcher', 3,
    [R('in', '3G-SDI', 'BNC', 8, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
     R('out', 'HDMI', 'HDMI', 1, 'Multiview HDMI'), R('out', 'DisplayPort', 'DisplayPort', 3, 'Multiview DP'),
     R('io', 'Ethernet', 'SFP', 1, '10GbE SFP'), R('io', 'Ethernet', 'RJ45', 1, '1GbE'),
     R('in', 'Analog audio', 'XLR', 2, 'Audio In XLR'), R('in', 'Analog audio', '1/4" jack', 6, 'Audio In'),
     R('out', 'Analog audio', 'XLR', 2, 'Audio Out XLR'), R('out', 'Analog audio', '1/4" jack', 2, 'Audio Out'), R('out', 'Analog audio', '1/4" jack', 1, 'Headphones'),
     R('io', 'Other', 'HD15', 1, 'Tally/GPI'), R('io', 'USB', 'USB-A', 7, 'USB 3.2'), R('io', 'USB', 'USB-C', 1, 'USB-C'), R('in', 'Power', 'IEC', 2, 'PSU')],
    '3RU, 48.3 x 13.34 x 49.7 cm with ears. 8 x 3G SDI in, 8 x 3G SDI out, genlock, 1 HDMI + 3 DP multiviewer outputs, 10GbE SFP (bring your own SFP) '
    'and 1GbE, balanced XLR stereo in/out, 3 stereo 1/4" in pairs, 1/4" stereo out pair and headphones, HD15 tally, 650 W redundant PSU. '
    'Check: SDI connector type (BNC assumed).', 'TriCaster 2 Elite datasheet', 'https://www.fullcompass.com/prod/599126-vizrt-formerly-newtek-tricaster-2-elite-live-video-production-system')
add('nc2-studio-io', 'NC2 Studio I/O', 'NC2 Studio I/O module', 'NDI I/O', 'converter', 1,
    [R('io', '12G-SDI', 'HD-BNC', 8, 'SDI I/O'), R('in', 'Reference', 'HD-BNC', 1, 'Genlock'),
     R('io', 'Ethernet', 'RJ45', 1, '10GbE'), R('io', 'Ethernet', 'RJ45', 1, '1GbE'), R('in', 'Power', 'IEC', 2, 'PSU')],
    'SDI to NDI converter, 1RU (4.28 cm), 57.75 cm deep, rack kit included. 8 HD-BNC ports each set as input or output, up to 2 x 12G '
    '(or 2 x 12G plus 4 x 3G), genlock (bi-level, tri-level or NDI), 10GBASE-T + 1GbE, redundant PSU. Also sold as Viz Connect Studio I/O (2RU). '
    'Check: reference connector type.', 'Vizrt NC2 Studio I/O specifications (reseller page)', 'https://www.trm.fr/en/video-mixers/newtek-nc2-studio-io-module/')

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(OUT, 'w'), indent=1)
print(len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
