#!/usr/bin/env python3
"""Foxtel set-top boxes and the Foxtel Business iQ head end (2026-11-16). Writes catalogue/foxtel.json.

These are desktop boxes, so each one has boxMm and sits on a rack shelf (ru from its height, widthCols from its width,
one column = 1/12 of the 19-inch width, about 40 mm). Foxtel publishes few hardware specs, so:
  verified=True   size and connectors come from a Foxtel / maker manual (iQ, iQ2) or a measured review (Foxtel Now box).
  verified=False  size or some connectors are estimated; 'Check:' in the notes says what.
Satellite boxes are listed; cable versions (iQ, iQ2, iQ3) have one cable F input in place of the satellite inputs.
Kept the ids foxtel-iq3 / iq4 / iq5 from contribution.py so saved projects still find them.
"""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def R(d, t, c, n, p): return dict(face='rear', dir=d, type=t, connector=c, count=n, prefix=p)
OUT = []
def box(id, pn, name, w, h, ports, notes, src, url, verified, depth=None, mfr='Foxtel', fam='Set-top boxes', cat='converter', **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat,
             ru=1 if h <= 43 else -(-h // 44), widthCols=min(12, max(2, -(-w // 40))), fullDepth=False,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports, boxMm={'w': w, 'h': h})
    if depth: m['depthMm'] = depth
    m.update(kw); OUT.append(m)

SHELF = ' Desktop box: put it on a rack shelf.'
# common rear connectors
SAT = lambda n, p='Satellite In': R('in', 'RF', 'F', n, p)
ANT = R('in', 'RF', 'PAL', 1, 'Aerial In')
HDMI = lambda p='HDMI Out': R('out', 'HDMI', 'HDMI', 1, p)
OPT = R('out', 'AES/EBU', 'TOSLINK', 1, 'Optical audio out (S/PDIF)')
COAX = R('out', 'AES/EBU', 'RCA', 1, 'Digital audio out (coax S/PDIF)')
ETH = lambda p='Ethernet': R('io', 'Ethernet', 'RJ45', 1, p)
USB = lambda n=1, p='USB': R('io', 'USB', 'USB-A', n, p)
DC = lambda p='12V DC In': R('in', 'Power', 'DC barrel', 1, p)
AL, AR = R('out', 'Analog audio', 'RCA', 1, 'Audio L'), R('out', 'Analog audio', 'RCA', 1, 'Audio R')
TEL = R('io', 'Other', 'RJ11', 1, 'Telephone line')
FX = 'https://www.foxtel.com.au/'

box('foxtel-iq', 'iQ', 'Foxtel iQ set-top box (first generation PDR, satellite)', 325, 56,
    [SAT(2, 'Input'), R('out', 'Analog video', 'SCART', 1, 'TV SCART'), R('io', 'Analog video', 'SCART', 1, 'VCR SCART'),
     AL, AR, R('out', 'Analog audio', 'RCA', 2, 'VCR fixed audio'), COAX, OPT, HDMI('HDMI (SD, HDCP)'), ETH(), USB(), TEL,
     DC('12V DC In (3.5 A max)')],
    'Original Foxtel personal digital recorder (Pace). 325 x 56 x 235 mm (W x H x D), 42 W max, 12 V DC from an external 240 V '
    'supply. Ethernet and USB were marked "for future use". The cable version has one cable F input instead of Input 1 and 2.' + SHELF,
    'Foxtel iQ user manual, rear view and specification (manualslib 676006, pages 78 and 90)',
    'https://www.manualslib.com/manual/676006/Foxtel-Iq.html', True, depth=235, powerW=42)

box('foxtel-iq2', 'iQ2', 'Foxtel iQ2 HD set-top box (satellite)', 404, 60,
    [SAT(4, 'Input'), TEL, USB(), R('io', 'Other', 'eSATA', 1, 'eSATA'), ETH(), HDMI(), OPT, COAX, AL, AR,
     R('out', 'Analog video', 'RCA', 1, 'Composite video out'), R('out', 'Analog video', 'RCA', 3, 'SD component out (Y/Pb/Pr)'),
     R('in', 'Power', 'IEC C8', 1, 'Mains In (240 V)')],
    'HD PVR. 404 x 60 x 294 mm (W x H x D), 45 W max, mains powered (2-pin IEC "figure 8" inlet). eSATA is not on every '
    'unit. The cable version has one cable F input instead of Input 1 to 4.' + SHELF,
    'Foxtel iQ2 user manual, rear view and specification (manualslib 3097228, pages 80 and 91)',
    'https://www.manualslib.com/manual/3097228/Foxtel-Iq2.html', True, depth=294, powerW=45)

box('foxtel-iq3', 'iQ3', 'Foxtel iQ3 set-top box (satellite)', 330, 75,
    [SAT(2, 'Input'), ANT, HDMI(), OPT, COAX, ETH(), USB(3, 'USB (back and side)'), DC()],
    'HD PVR made by Pace (2015): 10 tuners (8 on cable), 1 TB drive, Wi-Fi, SIM card in the rear (no smart card). '
    'The cable version has one cable F input and no aerial input. Narrower than the iQ2 but taller. '
    'Check: size (Foxtel does not publish it; estimated about 330 x 75 mm) and which USB ports are on the side.' + SHELF,
    'Foxtel iQ3 domestic installation manual (manualslib 1267695); ChannelNews and EFTM launch articles',
    'https://www.manualslib.com/manual/1267695/Foxtel-Iq3.html', False)

box('foxtel-iq4', 'iQ4', 'Foxtel iQ4 set-top box (satellite, 4K)', 330, 75,
    [SAT(2, 'SAT IN'), ANT, HDMI('HDMI Out (2.0, 4K)'), OPT, ETH(), USB(), DC('12V DC In (5 A)')],
    'Satellite 4K PVR based on the ARRIS (CommScope) MS6505: 8 satellite + 2 terrestrial tuners, 1 TB drive. 4K channels need '
    'both satellite inputs fed (dual-output dish). Looks almost the same as the iQ3 (two buttons on the right of the front). '
    'Power is a 12 V 5 A plug pack with a 2.1 mm plug (from replacement supplies). '
    'Check: size (not published; estimated as the iQ3) and whether there is a coax digital audio out.' + SHELF,
    'CompareTV iQ4 review; Foxtel iQ4 welcome guide; MAD Electronics iQ4 power supply listing',
    'https://www.comparetv.com.au/review/foxtel-iq4k-streaming-tv-review', False)

box('foxtel-iq5', 'iQ5', 'Foxtel iQ5 streaming set-top box (satellite or internet, 4K)', 210, 40,
    [SAT(1, 'SAT IN 1'), SAT(1, 'SAT IN 2'), R('in', 'RF', 'PAL', 1, 'ANT IN'), HDMI('HDMI Out (2.1, 4K HDR)'), OPT, ETH(), DC()],
    'Made by CommScope (ARRIS on the label), 2021. Streams over the internet and also takes satellite: one cable in SAT IN 1, '
    'or both for dual tuning; ANT IN for free-to-air. About half the size of earlier iQ boxes; the optional 1 TB drive module '
    'stacks under it. Check: size (not published; estimated about 210 x 40 mm) and the power supply rating.' + SHELF,
    'ChannelNews and techAU iQ5 reviews; Jim\'s Antennas iQ5 connection guide; Good Design Award entry',
    'https://www.channelnews.com.au/review-new-foxtel-iq5-box-has-a-lot-of-surprises/', False)

box('foxtel-now-box', 'Foxtel Now Box', 'Foxtel Now Box streaming player (Android TV, DVB-T)', 104, 72,
    [R('in', 'RF', 'PAL', 1, 'Aerial In'), HDMI('HDMI Out (2.0, HDCP 2.2)'), ETH(), R('io', 'USB', 'USB-A', 1, 'USB 3.0'), OPT, DC()],
    'Technicolor DWT765FXT (2017): Android TV with a free-to-air tuner, no satellite. 104 x 83 x 72 mm, 0.27 kg, 12 V DC '
    'plug pack. Check: which way up the 72 mm and 83 mm sides go.' + SHELF,
    'TechRadar Foxtel Now Box review; tvsfaq DWT765FXT listing', 'https://www.techradar.com/reviews/foxtel-now-box', True,
    depth=83, weightKg=0.27)

box('foxtel-hubbl-puck', 'Hubbl Puck', 'Hubbl Puck streaming box (Foxtel Group)', 108, 18,
    [HDMI('HDMI Out (2.1)'), ETH('Ethernet (100 Mb)'), DC('DC In')],
    'Foxtel Group\'s Hubbl streaming box (2023), the Sky Stream puck hardware: internet only, no tuner or aerial input, '
    'Wi-Fi or Ethernet. About 108 x 108 x 18 mm. Check: power supply voltage.' + SHELF,
    'Choose.co.uk Sky Stream puck review; CyberShack Hubbl article', 'https://www.hubbl.com.au/', False, depth=108)

box('foxtel-biq', 'Business iQ (BiQ)', 'Foxtel Business iQ (BiQ) set-back box for hotels and venues', 160, 30,
    [R('in', 'RF', 'F', 1, 'RF1'), R('in', 'RF', 'F', 1, 'RF2'), HDMI('HDMI Out (2.0b, 4K)'), ETH('Ethernet (10/100)'),
     R('in', 'Other', '3.5mm jack', 1, 'IR (prism dongle)'), DC()],
    'Foxtel Commercial set-back box on the ADB Ariel v2 platform (vuTyme client): 4 DVB-S2 satellite tuners (DiSEqC on RF1/RF2, '
    'Unicable), 1 DVB-T2 tuner, Wi-Fi ac, Chromecast, Irdeto cardless. Feeds: satellite on RF1, terrestrial or a second '
    'lateral on RF2, or IPTV multicast over Ethernet from a vuStreamer head end. Wall-mount 12 V DC plug pack. '
    'Check: size (not published; estimated) and the IR port connector.' + SHELF,
    'Foxtel Business iQ installation guide (manualslib 1982086, pages 8, 9, 17, 18)',
    'https://www.manualslib.com/manual/1982086/Foxtel-Business-Iq.html', False)

box('foxtel-vustreamer', 'vuStreamer', 'ADB vuStreamer IPTV head end (Foxtel Business iQ)', 430, 44,
    [R('in', 'RF', 'F', 1, 'SAT In (Multistacker H/Lo)'), R('in', 'RF', 'F', 1, 'Ter In (FTA)'), ETH('Ethernet 1 (Mgmt)'),
     R('out', 'Ethernet', 'RJ45', 1, 'Ethernet 2 (IPTV out)'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
    'Rack head end that turns satellite (from a multistacker) and free-to-air RF into multicast IPTV for Business iQ boxes. '
    'Tuner cards with front status LEDs, cooling fans, two PSUs, earth point. Needs IGMPv2 and an IGMP querier on the IPTV '
    'VLAN; leave 1RU free above it. Check: height (ADB does not publish it; drawn as 1RU), tuner card count and the AC inlets.',
    'Foxtel BiQ self help troubleshooting guide (manualslib 2299611, pages 25 to 30); ADB vuTyme companion products',
    'https://www.adbglobal.com/business-tv-vutyme/companion-products/', False, mfr='ADB', fam='Foxtel Business iQ')
# the head end is a rack unit, not a shelf box
OUT[-1].pop('boxMm'); OUT[-1].update(ru=1, widthCols=12)

ids = [m['id'] for m in OUT]; assert len(ids) == len(set(ids))
json.dump(OUT, open(os.path.join(CAT, 'foxtel.json'), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'foxtel.json' not in idx: idx.append('foxtel.json'); json.dump(idx, open(ip, 'w'))
print('foxtel.json', len(OUT))
for m in OUT: print(f"  {m['id']:22} {m['ru']}RU x {m['widthCols']}/12  verified={m['verified']}")
