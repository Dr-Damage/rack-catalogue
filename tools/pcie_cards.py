#!/usr/bin/env python3
"""PCIe add-in cards that go in a computer's PCIe slots (catalogue/pcie-cards.json), and
USB / Thunderbolt connected interfaces (catalogue/usb-interfaces.json).

A PCIe card is a frame card (see catalogue/FRAMES.md) with card.fits ["PCIe"]. Its connectors are on
its one rear module, the slot bracket (included: true). Computers whose entry lists "Card slot" ports
named PCIe take these cards in the app (the app turns those slots into a rear-only PCIe frame).

Port data comes from the makers' product and tech spec pages as published; nothing here was traced from
a manual, so every entry is verified: false ("check specs"). Run: python3 tools/pcie_cards.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, '..', 'catalogue')


def g(face, d, t, conn, n, prefix):
    return {'face': face, 'dir': d, 'type': t, 'connector': conn, 'count': n, 'prefix': prefix}


def r(d, t, conn, n, prefix):
    return g('rear', d, t, conn, n, prefix)


def card(id, mfr, pn, name, family, ports, *, width=1, watts=0, lanes='', low=False, color='', notes='', url='', source='',
         bracket=None):
    bk = bracket or ('Low-profile bracket' if low else 'Full-height bracket')
    return {
        'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': 'card',
        'ru': 0, 'widthCols': 0, 'fullDepth': False, 'verified': False,
        'source': source or f'{mfr} product / tech specs page', 'productUrl': url,
        'notes': (f'PCIe {lanes} card. ' if lanes else 'PCIe card. ') + ('Low profile (full-height bracket usually in the box). ' if low else '')
                 + (f'Takes {width} slots. ' if width > 1 else '') + notes,
        'card': {'fits': ['PCIe'], 'slotWidth': width, **({'watts': watts} if watts else {}), **({'color': color} if color else {})},
        'portGroups': [],
        'rearModules': [{'partNumber': 'bracket', 'name': bk, 'width': width, 'default': True, 'included': True, 'portGroups': ports}],
        **({'powerW': watts} if watts else {}),
    }


BMD = 'Blackmagic Design'
BU = 'https://www.blackmagicdesign.com/products/decklink/techspecs'
B_INK = '#3b3f46'
cards = []
add = cards.append

# ---------- Blackmagic DeckLink ----------
add(card('bmdcard-decklink-mini-recorder', BMD, 'DeckLink Mini Recorder', 'DeckLink Mini Recorder (HD capture)', 'DeckLink', [
    r('in', '3G-SDI', 'BNC', 1, 'SDI In'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In')], lanes='x1 Gen 1', low=True, watts=5, url=BU))
add(card('bmdcard-decklink-mini-monitor', BMD, 'DeckLink Mini Monitor', 'DeckLink Mini Monitor (HD playback)', 'DeckLink', [
    r('out', '3G-SDI', 'BNC', 1, 'SDI Out'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out')], lanes='x1 Gen 1', low=True, watts=5, url=BU))
add(card('bmdcard-decklink-mini-recorder-4k', BMD, 'DeckLink Mini Recorder 4K', 'DeckLink Mini Recorder 4K', 'DeckLink', [
    r('in', '6G-SDI', 'BNC', 1, 'SDI In'), r('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In')], lanes='x4 Gen 2', low=True, watts=7, url=BU))
add(card('bmdcard-decklink-mini-monitor-4k', BMD, 'DeckLink Mini Monitor 4K', 'DeckLink Mini Monitor 4K', 'DeckLink', [
    r('out', '6G-SDI', 'BNC', 1, 'SDI Out'), r('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Out')], lanes='x4 Gen 2', low=True, watts=7, url=BU))
add(card('bmdcard-decklink-duo-2', BMD, 'DeckLink Duo 2', 'DeckLink Duo 2 (4 x 3G-SDI, each in or out)', 'DeckLink', [
    r('io', '3G-SDI', 'DIN 1.0/2.3', 4, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x4 Gen 2', watts=12, url=BU,
    notes='Each SDI connector is set as an input or output in Desktop Video. DIN to BNC adapter cables in the box. Check: reference connector.'))
add(card('bmdcard-decklink-duo-2-mini', BMD, 'DeckLink Duo 2 Mini', 'DeckLink Duo 2 Mini (2 in, 2 out 3G-SDI)', 'DeckLink', [
    r('in', '3G-SDI', 'DIN 1.0/2.3', 2, 'SDI In'), r('out', '3G-SDI', 'DIN 1.0/2.3', 2, 'SDI Out')], lanes='x4 Gen 2', low=True, watts=10, url=BU))
add(card('bmdcard-decklink-quad-2', BMD, 'DeckLink Quad 2', 'DeckLink Quad 2 (8 x 3G-SDI, each in or out)', 'DeckLink', [
    r('io', '3G-SDI', 'DIN 1.0/2.3', 8, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x8 Gen 2', watts=22, url=BU,
    notes='8 mini DIN SDI connections, each set as an input or output (tech specs). Reference Tri-Sync or black burst. Check: reference connector.'))
add(card('bmdcard-decklink-quad-hdmi-recorder', BMD, 'DeckLink Quad HDMI Recorder', 'DeckLink Quad HDMI Recorder (4 x HDMI 2.0 in)', 'DeckLink', [
    r('in', 'HDMI', 'HDMI', 4, 'HDMI In')], lanes='x8 Gen 3', watts=23, url=BU))
add(card('bmdcard-decklink-8k-pro', BMD, 'DeckLink 8K Pro', 'DeckLink 8K Pro (4 x 12G-SDI bidirectional)', 'DeckLink', [
    r('io', '12G-SDI', 'DIN 1.0/2.3', 4, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x8 Gen 3', watts=25, url=BU,
    notes='Each 12G-SDI connector can be an input or output (dual and quad link 8K). Check: connectors.'))
add(card('bmdcard-decklink-8k-pro-g2', BMD, 'DeckLink 8K Pro G2', 'DeckLink 8K Pro G2 (4 x 12G-SDI, HDMI 2.1 in/out)', 'DeckLink', [
    r('io', '12G-SDI', 'DIN 1.0/2.3', 4, 'SDI'), r('in', 'HDMI', 'HDMI', 1, 'HDMI 2.1 In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI 2.1 Out'),
    r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In'), r('out', 'RS-422', 'Other', 1, 'RS-422 Out')], width=2, lanes='x8 Gen 3', watts=30,
    url=BU + '/W-DLK-33', source='Blackmagic DeckLink 8K Pro G2 tech specs (W-DLK-33)',
    notes='Tech specs: 4 bidirectional 12G-SDI, HDMI 2.1 in and out, Tri-Sync or black burst reference, RS-422 out, needs 2 PCI slots, 30 W. Check: SDI and RS-422 connector types.'))
add(card('bmdcard-decklink-8k-pro-mini', BMD, 'DeckLink 8K Pro Mini', 'DeckLink 8K Pro Mini (4 x 12G-SDI, low profile)', 'DeckLink', [
    r('io', '12G-SDI', 'Micro BNC', 4, 'SDI'), r('in', 'Reference', 'Micro BNC', 1, 'Ref In')], lanes='x8 Gen 3', low=True, watts=18,
    url=BU + '/W-DLK-33', source='Blackmagic DeckLink 8K Pro Mini tech specs', notes='Tech specs: 4 bidirectional 12G-SDI on Micro BNC, Tri-Sync or black burst reference, 18 W. Check: reference connector.'))
add(card('bmdcard-decklink-4k-extreme-12g', BMD, 'DeckLink 4K Extreme 12G', 'DeckLink 4K Extreme 12G (with breakout cable)', 'DeckLink', [
    r('in', '12G-SDI', 'BNC', 2, 'SDI In'), r('out', '12G-SDI', 'BNC', 2, 'SDI Out'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
    r('in', 'Reference', 'BNC', 1, 'Ref In'), r('in', 'Analog video', 'BNC (breakout)', 3, 'Component In'), r('out', 'Analog video', 'BNC (breakout)', 3, 'Component Out'),
    r('in', 'Analog audio', 'XLR3F (breakout)', 2, 'Analog In'), r('out', 'Analog audio', 'XLR3M (breakout)', 2, 'Analog Out'),
    r('in', 'AES/EBU', 'BNC (breakout)', 2, 'AES In'), r('out', 'AES/EBU', 'BNC (breakout)', 2, 'AES Out'), r('io', 'RS-422', 'DB9 (breakout)', 1, 'RS-422')],
    width=2, lanes='x8 Gen 2', watts=30, url=BU + '/W-DLK-33', source='Blackmagic DeckLink 4K Extreme 12G tech specs',
    notes='Main card plus HDMI or SDI mezzanine card, so it takes 2 slots. Analog, AES and RS-422 are on the breakout cable. Optional 12G optical fibre in/out (SFP) not drawn.'))
add(card('bmdcard-decklink-studio-4k', BMD, 'DeckLink Studio 4K', 'DeckLink Studio 4K (with breakout cable)', 'DeckLink', [
    r('in', '6G-SDI', 'BNC', 1, 'SDI In'), r('out', '6G-SDI', 'BNC', 1, 'SDI Out'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
    r('in', 'Reference', 'BNC', 1, 'Ref In'), r('in', 'Analog audio', '1/4" TRS (breakout)', 4, 'Analog In'), r('out', 'Analog audio', '1/4" TRS (breakout)', 4, 'Analog Out'),
    r('in', 'AES/EBU', 'BNC (breakout)', 2, 'AES In'), r('out', 'AES/EBU', 'BNC (breakout)', 2, 'AES Out'), r('io', 'RS-422', 'DB9 (breakout)', 1, 'RS-422')],
    lanes='x4 Gen 2', watts=22, url=BU, notes='Analog audio, AES and RS-422 on the included breakout cable. Check: AES counts.'))
add(card('bmdcard-decklink-sdi-4k', BMD, 'DeckLink SDI 4K', 'DeckLink SDI 4K', 'DeckLink', [
    r('in', '6G-SDI', 'BNC', 1, 'SDI In'), r('out', '6G-SDI', 'BNC', 1, 'SDI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In'), r('io', 'RS-422', 'DB9', 1, 'RS-422')],
    lanes='x4 Gen 2', watts=11, url=BU, notes='Check: RS-422 connector (breakout).'))
add(card('bmdcard-decklink-sdi-micro', BMD, 'DeckLink SDI Micro', 'DeckLink SDI Micro (1 in, 1 out 3G-SDI)', 'DeckLink', [
    r('in', '3G-SDI', 'BNC', 1, 'SDI In'), r('out', '3G-SDI', 'BNC', 1, 'SDI Out')], lanes='x1 Gen 2', low=True, watts=5, url=BU))
add(card('bmdcard-decklink-micro-recorder', BMD, 'DeckLink Micro Recorder', 'DeckLink Micro Recorder (SDI and HDMI in)', 'DeckLink', [
    r('in', '3G-SDI', 'BNC', 1, 'SDI In'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In')], lanes='x1 Gen 2', low=True, watts=4, url=BU))
add(card('bmdcard-decklink-ip-hd', BMD, 'DeckLink IP HD', 'DeckLink IP HD (SMPTE 2110 over 10G Ethernet)', 'DeckLink IP', [
    r('io', 'SFP', 'SFP+', 2, '10G SFP')], lanes='x4 Gen 2', low=True, watts=10, url=BU,
    notes='SMPTE ST 2110 video, audio and ancillary as 2 HD channels. Check: SFP count.'))
add(card('bmdcard-decklink-ip-hd-optical', BMD, 'DeckLink IP HD Optical', 'DeckLink IP HD Optical (2110, fibre)', 'DeckLink IP', [
    r('io', 'Fibre', 'LC duplex', 1, '10G Optical')], lanes='x4 Gen 2', low=True, watts=10, url=BU, notes='Check: connector count.'))
add(card('bmdcard-decklink-ip-uhd', BMD, 'DeckLink IP 25G', 'DeckLink IP 25G (SMPTE 2110 UHD)', 'DeckLink IP', [
    r('io', 'SFP', 'SFP28', 2, '25G SFP')], lanes='x8 Gen 3', watts=15, url=BU, notes='Check: model name and port count with Blackmagic.'))
# Intensity (HDMI / analog)
add(card('bmdcard-intensity-pro-4k', BMD, 'Intensity Pro 4K', 'Intensity Pro 4K (HDMI and analog)', 'Intensity', [
    r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
    r('in', 'Analog video', 'RCA (breakout)', 3, 'Component In'), r('out', 'Analog video', 'RCA (breakout)', 3, 'Component Out'),
    r('in', 'Analog audio', 'RCA (breakout)', 2, 'Audio In'), r('out', 'Analog audio', 'RCA (breakout)', 2, 'Audio Out'), r('out', 'Other', 'TOSLINK', 1, 'Optical Audio Out')],
    lanes='x4 Gen 2', watts=10, url='https://www.blackmagicdesign.com/products/intensity', notes='Analog on the breakout cable.'))

# ---------- AJA ----------
AJA = 'AJA'
add(card('ajacard-kona-5', AJA, 'KONA 5', 'KONA 5 (4 x 12G-SDI bidirectional, HDMI 2.0 out)', 'KONA', [
    r('io', '12G-SDI', 'HD-BNC', 4, 'SDI'), r('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Out'), r('in', 'Reference', 'HD-BNC (breakout)', 1, 'Ref In'),
    r('in', 'Timecode', 'BNC (breakout)', 1, 'LTC In'), r('out', 'Timecode', 'BNC (breakout)', 1, 'LTC Out'), r('io', 'RS-422', 'DB9 (breakout)', 1, 'RS-422'),
    r('in', 'AES/EBU', 'BNC (breakout)', 8, 'AES In'), r('out', 'AES/EBU', 'BNC (breakout)', 8, 'AES Out')], lanes='x8 Gen 3', watts=30,
    url='https://www.aja.com/products/kona-5', source='AJA KONA 5 product page',
    notes='Product page: 4 x HD-BNC 12G-SDI bidirectional, full-size HDMI 2.0 out, reference, LTC, RS-422 and 8 AES in / 8 out on the included breakout. Check: AES channel vs connector count (AES pairs).'))
add(card('ajacard-kona-x', AJA, 'KONA X', 'KONA X (2 x 12G-SDI, HDMI 2.0 in and out)', 'KONA', [
    r('io', '12G-SDI', 'BNC', 2, 'SDI'), r('in', 'HDMI', 'HDMI', 1, 'HDMI 2.0 In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Out')], lanes='x4 Gen 3', watts=25,
    url='https://www.aja.com/products/kona-x', source='AJA KONA X product page',
    notes='Optional KONA Xpand adds reference (BNC), LTC in/out, RS-422, 8 ch AES and 2 ch analog (add as extra ports or a second card).'))
add(card('ajacard-kona-xm', AJA, 'KONA XM', 'KONA XM (2 x 12G-SDI, HDMI, low profile)', 'KONA', [
    r('io', '12G-SDI', 'Micro BNC', 2, 'SDI'), r('out', 'HDMI', 'Mini HDMI', 1, 'HDMI Out')], lanes='x4 Gen 3', low=True, watts=20,
    url='https://www.aja.com/products/kona-xm', notes='Check: connector types and HDMI direction.'))
add(card('ajacard-kona-4', AJA, 'KONA 4', 'KONA 4 (4 x 3G-SDI bidirectional, with breakout)', 'KONA', [
    r('io', '3G-SDI', 'BNC', 4, 'SDI'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), r('in', 'Reference', 'BNC (breakout)', 1, 'Ref In'),
    r('in', 'Timecode', 'BNC (breakout)', 1, 'LTC In'), r('out', 'Timecode', 'BNC (breakout)', 1, 'LTC Out'), r('io', 'RS-422', 'DB9 (breakout)', 1, 'RS-422'),
    r('in', 'AES/EBU', 'BNC (breakout)', 8, 'AES In'), r('out', 'AES/EBU', 'BNC (breakout)', 8, 'AES Out'),
    r('in', 'Analog audio', 'XLR (breakout)', 4, 'Analog In'), r('out', 'Analog audio', 'XLR (breakout)', 4, 'Analog Out')],
    lanes='x8 Gen 2', watts=25, url='https://www.aja.com/products/kona-4', notes='Check: analog channel counts on the breakout.'))
add(card('ajacard-kona-1', AJA, 'KONA 1', 'KONA 1 (3G-SDI in/out, low profile)', 'KONA', [
    r('in', '3G-SDI', 'HD-BNC', 1, 'SDI In'), r('out', '3G-SDI', 'HD-BNC', 1, 'SDI Out'), r('in', 'Reference', 'HD-BNC', 1, 'Ref In')],
    lanes='x4 Gen 2', low=True, watts=10, url='https://www.aja.com/products/kona-1', notes='Check: SDI in/out counts (some firmware makes them bidirectional).'))
add(card('ajacard-kona-hdmi', AJA, 'KONA HDMI', 'KONA HDMI (4 x HDMI in)', 'KONA', [
    r('in', 'HDMI', 'HDMI', 4, 'HDMI In')], lanes='x8 Gen 2', watts=20, url='https://www.aja.com/products/kona-hdmi',
    source='AJA KONA HDMI product page', notes='Inputs 1-2 HDMI 2.0, 3-4 HDMI 1.4b.'))
add(card('ajacard-kona-lhe-plus', AJA, 'KONA LHe Plus', 'KONA LHe Plus (HD-SDI and analog, with breakout)', 'KONA', [
    r('in', 'HD-SDI', 'BNC', 1, 'SDI In'), r('out', 'HD-SDI', 'BNC', 2, 'SDI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In'),
    r('in', 'Analog video', 'BNC (breakout)', 3, 'Component In'), r('out', 'Analog video', 'BNC (breakout)', 3, 'Component Out'),
    r('in', 'Analog audio', 'XLR (breakout)', 2, 'Analog In'), r('out', 'Analog audio', 'XLR (breakout)', 2, 'Analog Out'), r('io', 'RS-422', 'DB9 (breakout)', 1, 'RS-422')],
    lanes='x1 Gen 1', watts=12, url='https://www.aja.com/products/kona-lhe-plus', notes='Legacy. Check: counts.'))
add(card('ajacard-kona-ip25', AJA, 'KONA IP25', 'KONA IP25 (SMPTE 2110, 2 x 10/25G SFP)', 'KONA IP', [
    r('io', 'SFP', 'SFP28', 2, '10/25G SFP'), r('io', 'Ethernet', 'RJ45', 1, '1GbE Control')], lanes='x8 Gen 4', watts=25,
    url='https://www.aja.com/products/kona-ip25', source='AJA KONA IP25 product page', notes='SMPTE ST 2110, 2022-6 and 2022-7.'))
add(card('ajacard-corvid-88', AJA, 'Corvid 88', 'Corvid 88 (8 x 3G-SDI bidirectional, OEM)', 'Corvid', [
    r('io', '3G-SDI', 'DIN 1.0/2.3', 8, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x8 Gen 2', watts=25,
    url='https://www.aja.com/products/corvid-88', notes='OEM card used in playout and graphics servers. Check: reference connector.'))
add(card('ajacard-corvid-44-12g', AJA, 'Corvid 44 12G', 'Corvid 44 12G (4 x 12G-SDI bidirectional, OEM)', 'Corvid', [
    r('io', '12G-SDI', 'HD-BNC', 4, 'SDI'), r('in', 'Reference', 'HD-BNC', 1, 'Ref In')], lanes='x8 Gen 3', watts=25,
    url='https://www.aja.com/products/corvid-44-12g', notes='A BNC version exists (Corvid 44 12G BNC). Check: connectors.'))
add(card('ajacard-corvid-44', AJA, 'Corvid 44', 'Corvid 44 (4 x 3G-SDI bidirectional, OEM)', 'Corvid', [
    r('io', '3G-SDI', 'DIN 1.0/2.3', 4, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x8 Gen 2', low=True, watts=15,
    url='https://www.aja.com/products/corvid-44'))

# ---------- other video I/O ----------
add(card('magewell-pro-capture-quad-sdi', 'Magewell', '11040', 'Pro Capture Quad SDI (4 x 3G-SDI in)', 'Pro Capture', [
    r('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'SDI In')], lanes='x4 Gen 2', watts=10, url='https://www.magewell.com/products/pro-capture-quad-sdi', notes='Check: connector (DIN breakout to BNC).'))
add(card('magewell-pro-capture-dual-sdi', 'Magewell', '11030', 'Pro Capture Dual SDI (2 x 3G-SDI in)', 'Pro Capture', [
    r('in', '3G-SDI', 'BNC', 2, 'SDI In')], lanes='x2 Gen 2', low=True, watts=6, url='https://www.magewell.com/products/pro-capture-dual-sdi'))
add(card('magewell-pro-capture-quad-hdmi', 'Magewell', '11080', 'Pro Capture Quad HDMI (4 x HDMI in)', 'Pro Capture', [
    r('in', 'HDMI', 'HDMI', 4, 'HDMI In')], lanes='x4 Gen 2', watts=10, url='https://www.magewell.com/products/pro-capture-quad-hdmi'))
add(card('magewell-pro-capture-hdmi-4k-plus', 'Magewell', '11100', 'Pro Capture HDMI 4K Plus (HDMI in, loop out)', 'Pro Capture', [
    r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Loop Out')], lanes='x4 Gen 2', low=True, watts=6, url='https://www.magewell.com'))
add(card('bluefish-kronos-k8', 'Bluefish444', 'KRONOS K8', 'KRONOS K8 (8 x 12G-SDI bidirectional)', 'KRONOS', [
    r('io', '12G-SDI', 'DIN 1.0/2.3', 8, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Monitor Out')], lanes='x8 Gen 3', watts=30,
    url='https://www.bluefish444.com', notes='Check: port count and HDMI.'))
add(card('deltacast-delta-12g-elp-h-4c', 'DELTACAST', 'DELTA-12G-elp-h 4c', 'DELTA-12G-elp-h 4c (4 x 12G-SDI bidirectional)', 'DELTA', [
    r('io', '12G-SDI', 'HD-BNC', 4, 'SDI'), r('in', 'Reference', 'HD-BNC', 1, 'Ref In')], lanes='x8 Gen 3', low=True, watts=20, url='https://www.deltacast.tv'))
add(card('deltacast-delta-3g-elp-d-8c', 'DELTACAST', 'DELTA-3G-elp-d 8c', 'DELTA-3G-elp-d 8c (8 x 3G-SDI bidirectional)', 'DELTA', [
    r('io', '3G-SDI', 'DIN 1.0/2.3', 8, 'SDI'), r('in', 'Reference', 'DIN 1.0/2.3', 1, 'Ref In')], lanes='x4 Gen 2', low=True, watts=15, url='https://www.deltacast.tv'))
add(card('matroxcard-xmio5-q25', 'Matrox', 'X.mio5 Q25', 'X.mio5 Q25 (SMPTE 2110, 4 x 25G SFP)', 'X.mio', [
    r('io', 'SFP', 'SFP28', 4, '25G SFP')], lanes='x16 Gen 3', watts=75, url='https://video.matrox.com', notes='Check: port count and model naming (X.mio5 Q25).'))

# ---------- Avid ----------
AV = 'Avid'
add(card('avidcard-hdx', AV, '9900-65163-00', 'Pro Tools | HDX PCIe card (2 x DigiLink Mini)', 'Pro Tools HDX', [
    r('io', 'Other', 'DigiLink Mini', 2, 'DigiLink Port'), r('io', 'Other', 'Mini-DIN', 1, 'Loop Sync / expansion')], lanes='x1 Gen 1', watts=25,
    url='https://www.avid.com/products/pro-tools-hdx', notes='Connects to HD I/O, HD OMNI, HD MADI and MTRX (DigiLink cable). Up to 64 ch per card. Check: the expansion port.'))
add(card('avidcard-hd-native', AV, '9900-65102-00', 'Pro Tools | HD Native PCIe card (1 x DigiLink Mini)', 'Pro Tools HD Native', [
    r('io', 'Other', 'DigiLink Mini', 1, 'DigiLink Port')], lanes='x1 Gen 1', watts=10, url='https://www.avid.com', notes='Legacy. Check: part number.'))
add(card('avidcard-dnxid', AV, 'Artist | DNxID', 'Artist | DNxID (Media Composer video I/O, rebadged AJA KONA)', 'Artist', [
    r('io', '3G-SDI', 'BNC', 2, 'SDI'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In')], lanes='x4 Gen 2', watts=20,
    url='https://www.avid.com', notes='Check: model and ports; Avid now qualifies Blackmagic and AJA cards for Media Composer.'))

# ---------- network (NVIDIA Mellanox, Intel, Broadcom) ----------
NV = 'NVIDIA (Mellanox)'
NU = 'https://www.nvidia.com/en-us/networking/ethernet-adapters/'
add(card('nvcard-connectx-4-lx-25g', NV, 'MCX4121A-ACAT', 'ConnectX-4 Lx 2 x 25GbE SFP28', 'ConnectX-4 Lx', [r('io', 'SFP', 'SFP28', 2, '25GbE')], lanes='x8 Gen 3', low=True, watts=10, url=NU))
add(card('nvcard-connectx-5-25g', NV, 'MCX512A-ACAT', 'ConnectX-5 2 x 25GbE SFP28', 'ConnectX-5', [r('io', 'SFP', 'SFP28', 2, '25GbE')], lanes='x8 Gen 3', low=True, watts=12, url=NU))
add(card('nvcard-connectx-5-100g', NV, 'MCX516A-CCAT', 'ConnectX-5 2 x 100GbE QSFP28', 'ConnectX-5', [r('io', 'SFP', 'QSFP28', 2, '100GbE')], lanes='x16 Gen 3', low=True, watts=19, url=NU))
add(card('nvcard-connectx-6-lx-25g', NV, 'MCX631102AN-ADAT', 'ConnectX-6 Lx 2 x 25GbE SFP28 (ST 2110 / Rivermax)', 'ConnectX-6 Lx', [r('io', 'SFP', 'SFP28', 2, '25GbE')], lanes='x8 Gen 4', low=True, watts=12, url=NU,
    notes='PTP hardware timestamping and packet pacing for SMPTE ST 2110 with NVIDIA Rivermax.'))
add(card('nvcard-connectx-6-dx-25g', NV, 'MCX623102AN-ADAT', 'ConnectX-6 Dx 2 x 25GbE SFP56 (ST 2110 / Rivermax)', 'ConnectX-6 Dx', [r('io', 'SFP', 'SFP56', 2, '25GbE')], lanes='x16 Gen 4', low=True, watts=15, url=NU))
add(card('nvcard-connectx-6-dx-100g', NV, 'MCX623106AN-CDAT', 'ConnectX-6 Dx 2 x 100GbE QSFP56 (ST 2110 / Rivermax)', 'ConnectX-6 Dx', [r('io', 'SFP', 'QSFP28', 2, '100GbE')], lanes='x16 Gen 4', low=True, watts=21, url=NU))
add(card('nvcard-connectx-7-200g', NV, 'MCX713106AC-VEAT', 'ConnectX-7 2 x 200GbE QSFP112', 'ConnectX-7', [r('io', 'SFP', 'QSFP112', 2, '200GbE')], lanes='x16 Gen 5', low=True, watts=25, url=NU, notes='Check: part number and port speed.'))
add(card('nvcard-connectx-7-400g', NV, 'MCX75310AAS-NEAT', 'ConnectX-7 1 x 400G OSFP', 'ConnectX-7', [r('io', 'SFP', 'OSFP', 1, '400G')], lanes='x16 Gen 5', low=True, watts=25, url=NU, notes='Check: InfiniBand / Ethernet variant.'))
add(card('nvcard-bluefield-2-100g', NV, 'MBF2M516A-CEEOT', 'BlueField-2 DPU 2 x 100GbE QSFP56', 'BlueField', [r('io', 'SFP', 'QSFP28', 2, '100GbE'), r('io', 'Ethernet', 'RJ45', 1, '1GbE OOB')], lanes='x16 Gen 4', watts=75, url=NU))
add(card('nvcard-bluefield-3-200g', NV, 'B3220', 'BlueField-3 DPU 2 x 200GbE QSFP112', 'BlueField', [r('io', 'SFP', 'QSFP112', 2, '200GbE'), r('io', 'Ethernet', 'RJ45', 1, '1GbE OOB')], lanes='x16 Gen 5', watts=150, url=NU))
IN = 'Intel'
add(card('intelcard-x710-da2', IN, 'X710-DA2', 'Ethernet X710-DA2 2 x 10GbE SFP+', 'Ethernet 700', [r('io', 'SFP', 'SFP+', 2, '10GbE')], lanes='x8 Gen 3', low=True, watts=4, url='https://www.intel.com'))
add(card('intelcard-x710-da4', IN, 'X710-DA4', 'Ethernet X710-DA4 4 x 10GbE SFP+', 'Ethernet 700', [r('io', 'SFP', 'SFP+', 4, '10GbE')], lanes='x8 Gen 3', low=True, watts=7, url='https://www.intel.com'))
add(card('intelcard-x550-t2', IN, 'X550-T2', 'Ethernet X550-T2 2 x 10GBASE-T', 'Ethernet 500', [r('io', 'Ethernet', 'RJ45', 2, '10GbE')], lanes='x4 Gen 3', low=True, watts=11, url='https://www.intel.com'))
add(card('intelcard-x710-t4l', IN, 'X710-T4L', 'Ethernet X710-T4L 4 x 10GBASE-T', 'Ethernet 700', [r('io', 'Ethernet', 'RJ45', 4, '10GbE')], lanes='x8 Gen 3', low=True, watts=14, url='https://www.intel.com'))
add(card('intelcard-e810-xxvda2', IN, 'E810-XXVDA2', 'Ethernet E810-XXVDA2 2 x 25GbE SFP28', 'Ethernet 800', [r('io', 'SFP', 'SFP28', 2, '25GbE')], lanes='x8 Gen 4', low=True, watts=12, url='https://www.intel.com'))
add(card('intelcard-e810-xxvda4', IN, 'E810-XXVDA4', 'Ethernet E810-XXVDA4 4 x 25GbE SFP28', 'Ethernet 800', [r('io', 'SFP', 'SFP28', 4, '25GbE')], lanes='x16 Gen 4', watts=18, url='https://www.intel.com'))
add(card('intelcard-e810-cqda2', IN, 'E810-CQDA2', 'Ethernet E810-CQDA2 2 x 100GbE QSFP28', 'Ethernet 800', [r('io', 'SFP', 'QSFP28', 2, '100GbE')], lanes='x16 Gen 4', low=True, watts=20, url='https://www.intel.com'))
add(card('intelcard-i350-t4', IN, 'I350-T4', 'Ethernet I350-T4 4 x 1GbE', 'Ethernet 300', [r('io', 'Ethernet', 'RJ45', 4, '1GbE')], lanes='x4 Gen 2', low=True, watts=5, url='https://www.intel.com'))
add(card('intelcard-x520-da2', IN, 'X520-DA2', 'Ethernet X520-DA2 2 x 10GbE SFP+ (legacy)', 'Ethernet 500', [r('io', 'SFP', 'SFP+', 2, '10GbE')], lanes='x8 Gen 2', low=True, watts=8, url='https://www.intel.com'))
add(card('broadcomcard-p225p', 'Broadcom', 'BCM957414A4142CC', 'NetXtreme-E P225P 2 x 25GbE SFP28', 'NetXtreme-E', [r('io', 'SFP', 'SFP28', 2, '25GbE')], lanes='x8 Gen 3', low=True, watts=10, url='https://www.broadcom.com'))
add(card('atto-fastframe3-tlns', 'ATTO', 'FFRM-NS12', 'FastFrame 3 2 x 10GbE SFP+', 'FastFrame', [r('io', 'SFP', 'SFP+', 2, '10GbE')], lanes='x8 Gen 3', low=True, watts=8, url='https://www.atto.com', notes='Common in Mac Pro and media storage workstations. Check: part number.'))
add(card('atto-celerity-fc-32', 'ATTO', 'CTFC-322E', 'Celerity FC-322E 2 x 32Gb Fibre Channel', 'Celerity', [r('io', 'SFP', 'SFP+', 2, '32Gb FC')], lanes='x8 Gen 3', low=True, watts=12, url='https://www.atto.com', notes='Fibre Channel SAN storage (Avid / Xsan). Check: part number.'))

# ---------- GPUs (outputs) ----------
NG = 'NVIDIA'
add(card('nvgpu-rtx-a2000', NG, 'RTX A2000', 'RTX A2000 graphics (4 x mini DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'Mini DisplayPort', 4, 'mDP')], width=2, lanes='x16 Gen 4', low=True, watts=70, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-a4000', NG, 'RTX A4000', 'RTX A4000 graphics (4 x DisplayPort, single slot)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], lanes='x16 Gen 4', watts=140, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-a5000', NG, 'RTX A5000', 'RTX A5000 graphics (4 x DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], width=2, lanes='x16 Gen 4', watts=230, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-a6000', NG, 'RTX A6000', 'RTX A6000 graphics (4 x DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], width=2, lanes='x16 Gen 4', watts=300, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-2000-ada', NG, 'RTX 2000 Ada', 'RTX 2000 Ada graphics (4 x mini DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'Mini DisplayPort', 4, 'mDP')], width=2, lanes='x8 Gen 4', low=True, watts=70, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-4000-ada', NG, 'RTX 4000 Ada', 'RTX 4000 Ada graphics (4 x DisplayPort, single slot)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], lanes='x16 Gen 4', watts=130, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-5000-ada', NG, 'RTX 5000 Ada', 'RTX 5000 Ada graphics (4 x DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], width=2, lanes='x16 Gen 4', watts=250, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-6000-ada', NG, 'RTX 6000 Ada', 'RTX 6000 Ada graphics (4 x DisplayPort)', 'NVIDIA RTX', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP')], width=2, lanes='x16 Gen 4', watts=300, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-rtx-pro-6000-blackwell', NG, 'RTX PRO 6000 Blackwell', 'RTX PRO 6000 Blackwell Workstation (4 x DisplayPort 2.1)', 'NVIDIA RTX PRO', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP 2.1')], width=2, lanes='x16 Gen 5', watts=600, url='https://www.nvidia.com', color='#1f2a1a'))
add(card('nvgpu-quadro-sync-ii', NG, 'Quadro Sync II', 'Quadro Sync II (frame lock / genlock for RTX cards)', 'NVIDIA RTX', [
    r('in', 'Reference', 'BNC', 1, 'House Sync In'), r('io', 'Other', 'RJ45', 2, 'Frame Lock')], lanes='(no PCIe link; bracket only)', watts=10, url='https://www.nvidia.com',
    notes='Ribbon cables to up to 4 RTX cards; draws its power from the slot/PSU. Use for genlocked video walls and LED processors.'))
add(card('amdgpu-radeon-pro-w7800', 'AMD', 'Radeon PRO W7800', 'Radeon PRO W7800 graphics (DisplayPort 2.1)', 'Radeon PRO', [r('out', 'DisplayPort', 'DisplayPort', 3, 'DP 2.1'), r('out', 'DisplayPort', 'Mini DisplayPort', 1, 'mDP 2.1')], width=2, lanes='x16 Gen 4', watts=260, url='https://www.amd.com', notes='Check: output mix.'))
add(card('amdgpu-radeon-pro-w7600', 'AMD', 'Radeon PRO W7600', 'Radeon PRO W7600 graphics (4 x DisplayPort 2.1, single slot)', 'Radeon PRO', [r('out', 'DisplayPort', 'DisplayPort', 4, 'DP 2.1')], lanes='x8 Gen 4', watts=130, url='https://www.amd.com'))

# ---------- audio cards (MADI, Dante, AES, DigiLink) ----------
RM = 'RME'
add(card('rmecard-hdspe-madi-fx', RM, 'HDSPe MADI FX', 'HDSPe MADI FX (3 x MADI, 390 channels)', 'HDSPe', [
    r('in', 'MADI audio', 'SC', 2, 'MADI Optical In'), r('out', 'MADI audio', 'SC', 2, 'MADI Optical Out'), r('in', 'MADI audio', 'BNC (breakout)', 1, 'MADI Coax In'), r('out', 'MADI audio', 'BNC (breakout)', 1, 'MADI Coax Out'),
    r('in', 'AES/EBU', 'XLR (breakout)', 1, 'AES In'), r('out', 'AES/EBU', 'XLR (breakout)', 1, 'AES Out'), r('in', 'Word clock', 'BNC (breakout)', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC (breakout)', 1, 'Word Clock Out'),
    r('io', 'Other', 'MIDI DIN (breakout)', 3, 'MIDI'), r('out', 'Analog audio', '1/4" TRS', 1, 'Headphones')], lanes='x1 Gen 1', watts=10, url='https://www.rme-audio.de/hdspe-madi-fx.html',
    notes='Two optical MADI on the bracket, third MADI (coax), AES, word clock and MIDI on the breakout cable. Check: layout.'))
add(card('rmecard-hdspe-madi', RM, 'HDSPe MADI', 'HDSPe MADI (64 x 64 channels, optical and coax)', 'HDSPe', [
    r('in', 'MADI audio', 'SC', 1, 'MADI Optical In'), r('out', 'MADI audio', 'SC', 1, 'MADI Optical Out'), r('in', 'MADI audio', 'BNC', 1, 'MADI Coax In'), r('out', 'MADI audio', 'BNC', 1, 'MADI Coax Out'),
    r('in', 'Word clock', 'BNC (breakout)', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC (breakout)', 1, 'Word Clock Out')], lanes='x1 Gen 1', watts=8, url='https://www.rme-audio.de'))
add(card('rmecard-hdspe-raydat', RM, 'HDSPe RayDAT', 'HDSPe RayDAT (4 x ADAT, AES, 72 ch)', 'HDSPe', [
    r('in', 'Other', 'TOSLINK', 4, 'ADAT In'), r('out', 'Other', 'TOSLINK', 4, 'ADAT Out'), r('in', 'AES/EBU', 'XLR (breakout)', 1, 'AES In'), r('out', 'AES/EBU', 'XLR (breakout)', 1, 'AES Out'),
    r('in', 'Word clock', 'BNC (breakout)', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC (breakout)', 1, 'Word Clock Out')], lanes='x1 Gen 1', watts=8, url='https://www.rme-audio.de'))
add(card('rmecard-hdspe-aio-pro', RM, 'HDSPe AIO Pro', 'HDSPe AIO Pro (analog, AES, ADAT, with breakout)', 'HDSPe', [
    r('in', 'Analog audio', 'XLR (breakout)', 2, 'Analog In'), r('out', 'Analog audio', 'XLR (breakout)', 4, 'Analog Out'), r('out', 'Analog audio', '1/4" TRS', 1, 'Phones'),
    r('in', 'AES/EBU', 'XLR (breakout)', 1, 'AES In'), r('out', 'AES/EBU', 'XLR (breakout)', 1, 'AES Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF Out')],
    lanes='x1 Gen 1', watts=8, url='https://www.rme-audio.de', notes='Check: analog counts.'))
add(card('focusritecard-rednet-pcier', 'Focusrite', 'RedNet PCIeR', 'RedNet PCIeR (Dante PCIe card, 128 x 128, redundant)', 'RedNet', [
    r('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec')], lanes='x1 Gen 2', low=True, watts=5, url='https://focusrite.com/rednet-pcier',
    notes='Dante primary and secondary Ethernet. Mac and Windows, low latency for Pro Tools and other DAWs. Check: connectors (some revisions use SFP).'))
add(card('digigramcard-lx-dante', 'Digigram', 'LX-DANTE', 'LX-DANTE (Dante PCIe sound card, 128 x 128)', 'LX', [
    r('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec')], lanes='x1 Gen 2', low=True, watts=6, url='https://www.digigram.com', notes='Used in radio playout and automation PCs.'))
add(card('digigramcard-lx-madi', 'Digigram', 'LX-MADI', 'LX-MADI (MADI PCIe sound card, 64 x 64)', 'LX', [
    r('in', 'MADI audio', 'BNC', 1, 'MADI In'), r('out', 'MADI audio', 'BNC', 1, 'MADI Out'), r('in', 'MADI audio', 'SC', 1, 'MADI Optical In'), r('out', 'MADI audio', 'SC', 1, 'MADI Optical Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In')],
    lanes='x1 Gen 2', low=True, watts=6, url='https://www.digigram.com', notes='Check: connectors.'))
add(card('digigramcard-lx-ip-madi', 'Digigram', 'LX-IP-MADI', 'LX-IP-MADI (AES67/RAVENNA and MADI, 256 ch)', 'LX', [
    r('io', 'Dante/AES67', 'RJ45', 2, 'AES67 / RAVENNA'), r('in', 'MADI audio', 'BNC', 1, 'MADI In'), r('out', 'MADI audio', 'BNC', 1, 'MADI Out')], lanes='x1 Gen 2', low=True, watts=6, url='https://www.digigram.com', notes='Check: ports.'))
add(card('lynxcard-aes16e', 'Lynx Studio', 'AES16e', 'AES16e (16 ch AES/EBU in and out, with breakout)', 'AES16e', [
    r('in', 'AES/EBU', 'XLR3F (breakout)', 8, 'AES In'), r('out', 'AES/EBU', 'XLR3M (breakout)', 8, 'AES Out'), r('in', 'Word clock', 'BNC (breakout)', 1, 'Word Clock In')],
    lanes='x1 Gen 1', watts=6, url='https://www.lynxstudio.com', notes='Two VHDCI ports on the bracket go to AES breakout cables. 8 AES pairs each way = 16 channels.'))
add(card('marian-clara-e', 'MARIAN', 'Clara E', 'Clara E (MADI PCIe card, 64 x 64)', 'Clara', [
    r('in', 'MADI audio', 'SC', 1, 'MADI In'), r('out', 'MADI audio', 'SC', 1, 'MADI Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out')],
    lanes='x1 Gen 1', low=True, watts=5, url='https://www.marian.de', notes='Check: connectors.'))

# ---------- I/O, USB, Thunderbolt, timing, storage ----------
add(card('asuscard-thunderboltex-4', 'ASUS', 'ThunderboltEX 4', 'ThunderboltEX 4 card (2 x Thunderbolt 4, 2 x DisplayPort in)', 'ThunderboltEX', [
    r('io', 'USB', 'USB-C (Thunderbolt 4)', 2, 'Thunderbolt'), r('in', 'DisplayPort', 'Mini DisplayPort', 2, 'DP In (from GPU)')], lanes='x4 Gen 3', watts=10, url='https://www.asus.com',
    notes='Needs a motherboard with a Thunderbolt header. Lets a PC drive UltraStudio, AJA Io and UA Apollo Thunderbolt gear.'))
add(card('sonnet-allegro-usb-c-4', 'Sonnet', 'USB3C-4PM-E', 'Allegro USB-C 4-port PCIe card', 'Allegro', [r('io', 'USB', 'USB-C', 4, 'USB-C 10Gb')], lanes='x8 Gen 3', watts=10, url='https://www.sonnettech.com'))
add(card('generic-pcie-usb3-4a', 'Generic', 'PCIe USB 3.0 4-port', 'USB 3.0 card, 4 x USB-A', 'Generic PCIe', [r('io', 'USB', 'USB-A', 4, 'USB 3.0')], lanes='x1 Gen 2', low=True, watts=5))
add(card('generic-pcie-serial-2', 'Generic', 'PCIe RS-232/422 2-port', 'Serial card, 2 x DB9 (RS-232/422/485)', 'Generic PCIe', [r('io', 'RS-422', 'DB9', 2, 'COM')], lanes='x1 Gen 1', low=True, watts=3,
    notes='For VTR / router / PTZ serial control. Set each port to RS-232, 422 or 485 in its driver.'))
add(card('generic-pcie-gpio-16', 'Generic', 'PCIe GPIO 16', 'GPI/O card (8 in, 8 out, DB37)', 'Generic PCIe', [r('io', 'GPIO', 'DB37', 1, 'GPIO')], lanes='x1 Gen 1', low=True, watts=3, notes='For tally and automation triggers.'))
add(card('generic-pcie-nvme-4', 'Generic', 'PCIe NVMe x4', 'NVMe carrier card (4 x M.2 SSD, no external ports)', 'Generic PCIe', [], lanes='x16 Gen 4', watts=30, notes='Takes a slot but has no connectors; storage for record and playout cache.'))
add(card('generic-pcie-blank', 'Generic', 'Blank slot cover', 'Blank PCIe slot cover', 'Generic PCIe', [], lanes='(none)'))
add(card('meinberg-gps180pex', 'Meinberg', 'GPS180PEX', 'GPS180PEX GPS clock card (time code, PPS)', 'PCIe clocks', [
    r('in', 'RF', 'SMA', 1, 'GPS Antenna'), r('out', 'Timecode', 'DB9 (breakout)', 1, 'IRIG / PPS Out')], lanes='x1 Gen 1', low=True, watts=6, url='https://www.meinberg.de', notes='Check: connectors.'))
add(card('meinberg-tcr180pex', 'Meinberg', 'TCR180PEX', 'TCR180PEX time code reader card (IRIG / LTC in)', 'PCIe clocks', [
    r('in', 'Timecode', 'BNC', 1, 'Time Code In'), r('out', 'Timecode', 'DB9 (breakout)', 1, 'PPS / Serial Out')], lanes='x1 Gen 1', low=True, watts=4, url='https://www.meinberg.de', notes='Check: connectors.'))
add(card('generic-pcie-ltc', 'Generic', 'PCIe LTC reader', 'LTC timecode reader/generator card', 'Generic PCIe', [
    r('in', 'Timecode', 'XLR3F', 1, 'LTC In'), r('out', 'Timecode', 'XLR3M', 1, 'LTC Out')], lanes='x1 Gen 1', low=True, watts=3))

# ---------- computers and expansion chassis that hold PCIe cards (explicit frames) ----------
def pc(id, mfr, pn, name, family, ru, slots, ports, *, orient='v', rear=None, notes='', url='', boxMm=None, widthCols=12, kg=0, watts=0, fixed=None, fullDepth=True):
    m = {'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': 'computer', 'ru': ru, 'widthCols': widthCols,
         'fullDepth': fullDepth, 'verified': False, 'source': f'{mfr} product page', 'productUrl': url, 'notes': notes, 'portGroups': ports,
         'frame': {'system': 'PCIe', 'slots': slots, 'rearOnly': True, 'orient': orient, 'rearAlign': 1,
                   'rear': rear or ({'x0': .38, 'x1': .9, 'y0': .08, 'y1': .92} if orient == 'v' else {'x0': .5, 'x1': .95, 'y0': .1, 'y1': .9})}}
    if orient == 'h' and ru == 1: m['frame']['cols'] = min(slots, 4)
    if fixed: m['frame']['fixed'] = fixed
    if boxMm: m['boxMm'] = boxMm
    if kg: m['weightKg'] = kg
    if watts: m['powerW'] = watts
    return m

pcs = [
    pc('sonnet-echo-iii-rack', 'Sonnet', 'ECHO-III-R1', 'Echo III Rackmount Thunderbolt 3 to PCIe expansion (3 slots, 1U)', 'Echo', 1, 3, [
        r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'IEC C14', 1, 'AC In')], orient='h',
        url='https://www.sonnettech.com', notes='Puts full-length PCIe cards (DeckLink, KONA, RedNet PCIeR, HDX, NICs) on a Mac or Thunderbolt PC. 2 Thunderbolt ports (host and daisy chain).', watts=400),
    pc('sonnet-echo-i-desktop', 'Sonnet', 'ECHO-I-TB3', 'Echo I Desktop Thunderbolt 3 to PCIe expansion (1 slot)', 'Echo', 2, 1, [
        r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'DC barrel', 1, 'DC In')], url='https://www.sonnettech.com',
        boxMm={'w': 110, 'h': 80}, widthCols=4, fullDepth=False, notes='Desktop box; put it on a shelf. Check: size.'),
    pc('sonnet-xmac-studio-echo', 'Sonnet', 'XMAC-STUDIO', 'xMac Studio: Mac Studio rack enclosure with 2 PCIe slots (4U)', 'xMac', 4, 2, [
        r('io', 'USB', 'USB-C (Thunderbolt)', 2, 'Thunderbolt'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url='https://www.sonnettech.com',
        notes='A Mac Studio sits inside; 2 full-length PCIe slots through Thunderbolt. Check: RU and slot count.'),
    pc('generic-ws-4u-7slot', 'Generic', '4U rackmount workstation', '4U rackmount workstation, 7 PCIe slots', 'Generic PC', 4, 7, [
        r('io', 'USB', 'USB-A', 6, 'USB 3'), r('io', 'USB', 'USB-C', 2, 'USB-C'), r('io', 'Ethernet', 'RJ45', 2, 'LAN'), r('out', 'Analog audio', '3.5mm jack', 1, 'Line Out'),
        r('in', 'Power', 'IEC C14', 1, 'AC In'), g('front', 'io', 'USB', 'USB-A', 2, 'Front USB')], notes='Template for a broadcast graphics / playout / capture PC. Add cards in its slots on the rear view.'),
    pc('generic-server-2u-6slot', 'Generic', '2U rackmount server', '2U rackmount server, 6 PCIe slots', 'Generic PC', 2, 6, [
        r('io', 'USB', 'USB-A', 2, 'USB 3'), r('io', 'Ethernet', 'RJ45', 2, 'LAN'), r('io', 'Ethernet', 'RJ45', 1, 'BMC / IPMI'), r('out', 'VGA', 'HD15', 1, 'VGA'),
        r('in', 'Power', 'IEC C14', 2, 'PSU')], notes='Template for an encoder, ingest or media server.'),
    pc('generic-server-1u-3slot', 'Generic', '1U rackmount server', '1U rackmount server, 3 PCIe slots', 'Generic PC', 1, 3, [
        r('io', 'USB', 'USB-A', 2, 'USB 3'), r('io', 'Ethernet', 'RJ45', 2, 'LAN'), r('io', 'Ethernet', 'RJ45', 1, 'BMC / IPMI'), r('out', 'VGA', 'HD15', 1, 'VGA'),
        r('in', 'Power', 'IEC C14', 2, 'PSU')], orient='h'),
]

for m in cards:
    assert m['id'] and m['rearModules'][0]['partNumber']
ids = [m['id'] for m in cards + pcs]
assert len(ids) == len(set(ids)), 'duplicate ids'

# ---------- USB / Thunderbolt interfaces ----------
def usb(id, mfr, pn, name, family, ports, *, ru=1, cols=12, box=None, notes='', url='', bus='USB', watts=0, cat='audio'):
    m = {'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': cat, 'ru': ru, 'widthCols': cols,
         'fullDepth': False, 'verified': False, 'source': f'{mfr} product page', 'productUrl': url,
         'notes': f'{bus} connected: cable its {bus} port to a USB / Thunderbolt port on the computer. ' + notes, 'portGroups': ports}
    if box: m['boxMm'] = box
    if watts: m['powerW'] = watts
    return m

def fr(d, t, c, n, p): return g('front', d, t, c, n, p)

CMB = 'XLR/TRS combo'
FO = 'Focusrite'; FU = 'https://focusrite.com'
U = []
U += [
    usb('focusrite-scarlett-solo-4', FO, 'Scarlett Solo 4th Gen', 'Scarlett Solo 4th Gen USB audio interface', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', 'XLR3F', 1, 'Mic In'), fr('in', 'Analog audio', '1/4" TRS', 1, 'Inst In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'),
        r('out', 'Analog audio', '1/4" TRS', 2, 'Line Out'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=1, cols=4, box={'w': 144, 'h': 44}, url=FU, notes='Bus powered.'),
    usb('focusrite-scarlett-2i2-4', FO, 'Scarlett 2i2 4th Gen', 'Scarlett 2i2 4th Gen USB audio interface', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 2, 'Line Out'), r('io', 'USB', 'USB-C', 1, 'USB')],
        ru=2, cols=5, box={'w': 180, 'h': 47}, url=FU, notes='Bus powered.'),
    usb('focusrite-scarlett-4i4-4', FO, 'Scarlett 4i4 4th Gen', 'Scarlett 4i4 4th Gen USB audio interface', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 2, 'Line In 3-4'),
        r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'USB-C', 1, 'Power')],
        ru=2, cols=5, box={'w': 180, 'h': 47}, url=FU),
    usb('focusrite-scarlett-16i16-4', FO, 'Scarlett 16i16 4th Gen', 'Scarlett 16i16 4th Gen USB audio interface', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 2, 'Line In 3-4'),
        r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF Out'), r('in', 'Other', 'RCA', 1, 'S/PDIF In'), r('out', 'Other', 'RCA', 1, 'S/PDIF Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')],
        ru=2, cols=6, box={'w': 230, 'h': 50}, url=FU, notes='Check: rear counts.'),
    usb('focusrite-scarlett-18i16-4', FO, 'Scarlett 18i16 4th Gen', 'Scarlett 18i16 4th Gen USB audio interface', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', CMB, 4, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 4, 'Line In'),
        r('out', 'Analog audio', '1/4" TRS', 6, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('in', 'Other', 'RCA', 1, 'S/PDIF In'), r('out', 'Other', 'RCA', 1, 'S/PDIF Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')],
        ru=2, cols=8, box={'w': 290, 'h': 50}, url=FU, notes='Check: rear counts.'),
    usb('focusrite-scarlett-18i20-4', FO, 'Scarlett 18i20 4th Gen', 'Scarlett 18i20 4th Gen USB audio interface (1U)', 'Scarlett 4th Gen', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 6, 'Input'),
        r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'Other', 'RCA', 1, 'S/PDIF In'), r('out', 'Other', 'RCA', 1, 'S/PDIF Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url=FU, notes='Rack mount 1U. Check: word clock (some revisions only have out).'),
    usb('focusrite-clarett-plus-2pre', FO, 'Clarett+ 2Pre', 'Clarett+ 2Pre USB audio interface', 'Clarett+', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 2, 'Line In 3-4'),
        r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], ru=2, cols=5, box={'w': 180, 'h': 47}, url=FU),
    usb('focusrite-clarett-plus-4pre', FO, 'Clarett+ 4Pre', 'Clarett+ 4Pre USB audio interface', 'Clarett+', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 2, 'Input 3-4'), r('in', 'Analog audio', '1/4" TRS', 4, 'Line In 5-8'),
        r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('in', 'Other', 'RCA', 1, 'S/PDIF In'), r('out', 'Other', 'RCA', 1, 'S/PDIF Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], ru=2, cols=7, box={'w': 270, 'h': 47}, url=FU, notes='Check: rear counts.'),
    usb('focusrite-clarett-plus-8pre', FO, 'Clarett+ 8Pre', 'Clarett+ 8Pre USB audio interface (1U)', 'Clarett+', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 6, 'Input'),
        r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'Other', 'RCA', 1, 'S/PDIF In'), r('out', 'Other', 'RCA', 1, 'S/PDIF Out'),
        r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url=FU),
    usb('focusrite-vocaster-two', FO, 'Vocaster Two', 'Vocaster Two podcast USB interface', 'Vocaster', [
        r('in', 'Analog audio', 'XLR3F', 2, 'Mic In'), r('out', 'Analog audio', '3.5mm jack', 2, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 2, 'Speaker Out'),
        r('in', 'Analog audio', '3.5mm TRRS', 1, 'Phone In/Out'), r('io', 'USB', 'USB-C', 1, 'USB Host'), r('io', 'USB', 'USB-C', 1, 'USB Power')], ru=2, cols=5, box={'w': 190, 'h': 50}, url=FU, notes='Check: ports.'),
    usb('focusrite-rednet-x2p', FO, 'RedNet X2P', 'RedNet X2P 2 x 2 Dante interface with mic pres', 'RedNet', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', 'XLR3M', 2, 'Line Out'),
        r('io', 'Dante/AES67', 'RJ45', 1, 'Dante (PoE)')], ru=1, cols=6, box={'w': 220, 'h': 44}, url=FU, bus='Dante', notes='Network audio, not USB: PoE powered. Half rack.'),
]
UA = 'Universal Audio'; UAU = 'https://www.uaudio.com'
U += [
    usb('ua-apollo-twin-x-duo', UA, 'Apollo Twin X DUO', 'Apollo Twin X DUO Thunderbolt 3 interface', 'Apollo', [
        fr('in', 'Analog audio', '1/4" TRS', 1, 'Hi-Z In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', CMB, 2, 'Mic/Line In'),
        r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 1, 'Thunderbolt 3'), r('in', 'Power', 'DC locking', 1, 'DC In')],
        ru=2, cols=5, box={'w': 160, 'h': 70}, url=UAU, bus='Thunderbolt'),
    usb('ua-apollo-x4', UA, 'Apollo x4', 'Apollo x4 Thunderbolt 3 interface (desktop)', 'Apollo', [
        fr('in', 'Analog audio', '1/4" TRS', 2, 'Hi-Z In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 4, 'Mic/Line In'),
        r('out', 'Analog audio', '1/4" TRS', 6, 'Line Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'),
        r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'DC locking', 1, 'DC In')], ru=2, cols=7, box={'w': 270, 'h': 70}, url=UAU, bus='Thunderbolt', notes='Check: counts.'),
    usb('ua-apollo-x8', UA, 'Apollo x8', 'Apollo x8 Thunderbolt 3 interface (1U)', 'Apollo', [
        fr('in', 'Analog audio', '1/4" TRS', 2, 'Hi-Z In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 4, 'Mic/Line In'), r('in', 'Analog audio', 'DB25 (8 ch)', 1, 'Line In 5-8'),
        r('out', 'Analog audio', '1/4" TRS', 2, 'Monitor Out'), r('out', 'Analog audio', 'DB25 (8 ch)', 1, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'IEC C14', 1, 'AC In')],
        url=UAU, bus='Thunderbolt', notes='Check: rear analog layout (TRS vs DB25).'),
    usb('ua-apollo-x8p', UA, 'Apollo x8p', 'Apollo x8p Thunderbolt 3 interface, 8 mic pres (1U)', 'Apollo', [
        fr('in', 'Analog audio', '1/4" TRS', 2, 'Hi-Z In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 8, 'Mic/Line In'),
        r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'IEC C14', 1, 'AC In')],
        url=UAU, bus='Thunderbolt'),
    usb('ua-apollo-x16', UA, 'Apollo x16', 'Apollo x16 Thunderbolt 3 interface, 16 x 16 line (1U)', 'Apollo', [
        fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', 'DB25 (8 ch)', 2, 'Line In'), r('out', 'Analog audio', 'DB25 (8 ch)', 2, 'Line Out'),
        r('out', 'Analog audio', 'XLR3M', 2, 'Monitor Out'), r('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), r('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'IEC C14', 1, 'AC In')],
        url=UAU, bus='Thunderbolt'),
    usb('ua-volt-276', UA, 'Volt 276', 'Volt 276 USB-C audio interface', 'Volt', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 2, 'Monitor Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=5, box={'w': 190, 'h': 80}, url=UAU),
]
RMU = 'https://www.rme-audio.de'
U += [
    usb('rme-fireface-ufx-iii', RM, 'Fireface UFX III', 'Fireface UFX III USB 3 interface, 94 ch with MADI (1U)', 'Fireface', [
        fr('in', 'Analog audio', CMB, 4, 'Mic/Line In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 8, 'Line In 5-12'),
        r('out', 'Analog audio', '1/4" TRS', 6, 'Line Out 3-8'), r('out', 'Analog audio', 'XLR3M', 2, 'Main Out'), r('in', 'MADI audio', 'SC', 1, 'MADI In'), r('out', 'MADI audio', 'SC', 1, 'MADI Out'),
        r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), r('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'Other', 'MIDI DIN', 2, 'MIDI'), r('io', 'USB', 'USB-B', 1, 'USB 3'), r('in', 'Power', 'IEC C14', 1, 'AC In')],
        url=RMU, notes='Check: rear counts. MADI optical in and out.'),
    usb('rme-ucx-ii', RM, 'Fireface UCX II', 'Fireface UCX II USB interface (half rack)', 'Fireface', [
        fr('in', 'Analog audio', CMB, 2, 'Mic/Line In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 6, 'Line In 3-8'),
        r('out', 'Analog audio', '1/4" TRS', 6, 'Line Out'), r('out', 'Analog audio', 'XLR3M', 2, 'Main Out'), r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-B', 1, 'USB'), r('in', 'Power', 'DC locking', 1, 'DC In')],
        cols=6, url=RMU, notes='Half rack 1U. Check: counts.'),
    usb('rme-802-fs', RM, 'Fireface 802 FS', 'Fireface 802 FS USB interface (1U)', 'Fireface', [
        fr('in', 'Analog audio', CMB, 4, 'Mic/Line In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 8, 'Line In'),
        r('out', 'Analog audio', '1/4" TRS', 8, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), r('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-B', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url=RMU, notes='Check: counts.'),
    usb('rme-babyface-pro-fs', RM, 'Babyface Pro FS', 'Babyface Pro FS USB interface', 'Babyface', [
        r('in', 'Analog audio', 'XLR3F', 2, 'Mic In'), r('out', 'Analog audio', 'XLR3M', 2, 'Line Out'), r('in', 'Analog audio', '1/4" TRS', 2, 'Inst In'), r('out', 'Analog audio', '1/4" TRS', 1, 'Phones'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF Out'), r('io', 'USB', 'USB-B', 1, 'USB')], ru=2, cols=3, box={'w': 108, 'h': 35}, url=RMU, notes='Bus powered.'),
    usb('rme-madiface-usb', RM, 'MADIface USB', 'MADIface USB: 64 ch MADI to USB', 'MADIface', [
        r('in', 'MADI audio', 'BNC', 1, 'MADI In'), r('out', 'MADI audio', 'BNC', 1, 'MADI Out'), r('out', 'Analog audio', '3.5mm jack', 1, 'Phones'), r('io', 'USB', 'USB-B', 1, 'USB')],
        ru=1, cols=3, box={'w': 110, 'h': 30}, url=RMU, notes='Coax MADI. Bus powered.'),
    usb('rme-madiface-xt-ii', RM, 'MADIface XT II', 'MADIface XT II: 3 x MADI to USB 3 / PCIe (1U)', 'MADIface', [
        r('in', 'MADI audio', 'SC', 2, 'MADI Optical In'), r('out', 'MADI audio', 'SC', 2, 'MADI Optical Out'), r('in', 'MADI audio', 'BNC', 1, 'MADI Coax In'), r('out', 'MADI audio', 'BNC', 1, 'MADI Coax Out'),
        fr('in', 'Analog audio', 'XLR3F', 2, 'Mic/Line In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', 'XLR3M', 2, 'Line Out'), r('in', 'AES/EBU', 'XLR3F', 1, 'AES In'), r('out', 'AES/EBU', 'XLR3M', 1, 'AES Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'USB', 'USB-B', 1, 'USB 3'), r('io', 'Ethernet', 'RJ45', 1, 'DAW net'), r('in', 'Power', 'IEC C14', 1, 'AC In')],
        cols=6, url=RMU, notes='Half rack. Check: ports.'),
    usb('rme-digiface-dante', RM, 'Digiface Dante', 'Digiface Dante: 256 ch Dante to USB 3 interface', 'Digiface', [
        r('io', 'Dante/AES67', 'SFP', 2, 'Dante Pri/Sec'), r('io', 'Dante/AES67', 'RJ45', 1, 'Dante'), r('in', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT/SPDIF Out'),
        r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('io', 'USB', 'USB-B', 1, 'USB 3')],
        ru=1, cols=4, box={'w': 140, 'h': 40}, url=RMU, notes='Check: SFP / RJ45 mix.'),
]
U += [
    usb('motu-m4', 'MOTU', 'M4', 'M4 USB-C audio interface', 'M Series', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 2, 'Line In 3-4'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=5, box={'w': 190, 'h': 45}, url='https://motu.com'),
    usb('motu-ultralite-mk5', 'MOTU', 'UltraLite-mk5', 'UltraLite-mk5 USB interface (half rack)', 'UltraLite', [
        fr('in', 'Analog audio', CMB, 2, 'Mic In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 6, 'Line In'), r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'Optical In'), r('out', 'Other', 'TOSLINK', 1, 'Optical Out'), r('io', 'Other', 'MIDI DIN', 2, 'MIDI'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')],
        cols=6, url='https://motu.com', notes='Check: counts.'),
    usb('motu-828-2024', 'MOTU', '828', '828 USB-C audio interface (1U, 2024)', '828', [
        fr('in', 'Analog audio', CMB, 2, 'Mic In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', '1/4" TRS', 8, 'Line In'), r('out', 'Analog audio', '1/4" TRS', 8, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url='https://motu.com', notes='Check: counts.'),
    usb('motu-8pre-es', 'MOTU', '8pre-es', '8pre-es USB / AVB interface (1U)', 'AVB', [
        fr('in', 'Analog audio', CMB, 8, 'Mic In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 8, 'Line Out'), r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'),
        r('io', 'Ethernet', 'RJ45', 1, 'AVB'), r('io', 'USB', 'USB-B', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url='https://motu.com', notes='Check: counts.'),
    usb('audient-id14-mkii', 'Audient', 'iD14 MKII', 'iD14 MKII USB-C audio interface', 'iD', [
        fr('in', 'Analog audio', '1/4" TRS', 1, 'DI In'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('in', 'Analog audio', CMB, 2, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=5, box={'w': 180, 'h': 70}, url='https://audient.com'),
    usb('audient-id44-mkii', 'Audient', 'iD44 MKII', 'iD44 MKII USB-C audio interface', 'iD', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 2, 'Mic/Line In 3-4'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], ru=2, cols=7, box={'w': 250, 'h': 80}, url='https://audient.com', notes='Check: counts.'),
    usb('audient-evo-8', 'Audient', 'EVO 8', 'EVO 8 USB audio interface', 'EVO', [
        fr('in', 'Analog audio', '1/4" TRS', 2, 'Inst In'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 4, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=6, box={'w': 230, 'h': 70}, url='https://audient.com'),
    usb('ssl-2-plus-mkii', 'Solid State Logic', 'SSL 2+ MKII', 'SSL 2+ MKII USB-C audio interface', 'SSL', [
        r('in', 'Analog audio', CMB, 2, 'Input'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('out', 'Analog audio', '1/4" TRS', 2, 'Phones'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=6, box={'w': 234, 'h': 67}, url='https://www.solidstatelogic.com'),
    usb('ssl-12', 'Solid State Logic', 'SSL 12', 'SSL 12 USB audio interface', 'SSL', [
        r('in', 'Analog audio', CMB, 4, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 4, 'Line Out'), r('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Other', 'TOSLINK', 1, 'ADAT In'),
        r('out', 'Other', 'TOSLINK', 0, 'ADAT Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], ru=2, cols=7, box={'w': 270, 'h': 70}, url='https://www.solidstatelogic.com', notes='Check: counts.'),
    usb('presonus-studio-1824c', 'PreSonus', 'Studio 1824c', 'Studio 1824c USB-C audio interface (1U)', 'Studio', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 6, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT Out'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'Other', 'MIDI DIN', 2, 'MIDI'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], url='https://www.presonus.com', notes='Check: counts.'),
    usb('presonus-quantum-hd8', 'PreSonus', 'Quantum HD 8', 'Quantum HD 8 USB-C interface (1U)', 'Quantum', [
        fr('in', 'Analog audio', CMB, 4, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 4, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url='https://www.presonus.com', notes='Check: counts.'),
    usb('antelope-orion-32-gen4', 'Antelope Audio', 'Orion 32+ Gen 4', 'Orion 32+ Gen 4: 64 ch AD/DA, MADI, USB / Thunderbolt (1U)', 'Orion', [
        r('in', 'Analog audio', 'DB25 (8 ch)', 4, 'Line In'), r('out', 'Analog audio', 'DB25 (8 ch)', 4, 'Line Out'), r('in', 'MADI audio', 'SC', 2, 'MADI In'), r('out', 'MADI audio', 'SC', 2, 'MADI Out'),
        r('in', 'Other', 'TOSLINK', 2, 'ADAT In'), r('out', 'Other', 'TOSLINK', 2, 'ADAT Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 4, 'Word Clock Out'),
        r('io', 'USB', 'USB-C (Thunderbolt 3)', 1, 'Thunderbolt 3'), r('io', 'USB', 'USB-B', 1, 'USB'), r('in', 'Power', 'IEC C14', 1, 'AC In')], url='https://en.antelopeaudio.com', bus='USB / Thunderbolt', notes='Check: counts.'),
    usb('behringer-umc204hd', 'Behringer', 'UMC204HD', 'U-PHORIA UMC204HD USB audio interface', 'U-PHORIA', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 2, 'Main Out'), r('out', 'Analog audio', 'RCA', 2, 'Line Out 3-4'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-B', 1, 'USB')], ru=2, cols=5, box={'w': 185, 'h': 50}, url='https://www.behringer.com'),
    usb('behringer-umc1820', 'Behringer', 'UMC1820', 'U-PHORIA UMC1820 USB audio interface (1U)', 'U-PHORIA', [
        fr('in', 'Analog audio', CMB, 8, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 10, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT Out'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'), r('io', 'Other', 'MIDI DIN', 2, 'MIDI'), r('io', 'USB', 'USB-B', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')],
        url='https://www.behringer.com', notes='Check: counts.'),
    usb('steinberg-ur816c', 'Steinberg', 'UR816C', 'UR816C USB-C audio interface (1U)', 'UR-C', [
        fr('in', 'Analog audio', CMB, 2, 'Front Input'), fr('out', 'Analog audio', '1/4" TRS', 2, 'Phones'), r('in', 'Analog audio', CMB, 6, 'Mic/Line In'), r('out', 'Analog audio', '1/4" TRS', 8, 'Line Out'),
        r('in', 'Other', 'TOSLINK', 1, 'ADAT In'), r('out', 'Other', 'TOSLINK', 1, 'ADAT Out'), r('in', 'Word clock', 'BNC', 1, 'Word Clock In'), r('out', 'Word clock', 'BNC', 1, 'Word Clock Out'),
        r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'DC barrel', 1, 'DC In')], url='https://www.steinberg.net', notes='Check: counts.'),
    usb('steinberg-ur22c', 'Steinberg', 'UR22C', 'UR22C USB-C audio interface', 'UR-C', [
        fr('in', 'Analog audio', CMB, 2, 'Input'), fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('out', 'Analog audio', '1/4" TRS', 2, 'Line Out'),
        r('in', 'Other', 'MIDI DIN', 1, 'MIDI In'), r('out', 'Other', 'MIDI DIN', 1, 'MIDI Out'), r('io', 'USB', 'USB-C', 1, 'USB'), r('in', 'Power', 'USB-C', 1, '5V DC')], ru=2, cols=4, box={'w': 159, 'h': 47}, url='https://www.steinberg.net'),
    usb('yamaha-ag06-mk2', 'Yamaha', 'AG06MK2', 'AG06MK2 live streaming mixer / USB interface', 'AG', [
        fr('in', 'Analog audio', CMB, 1, 'Mic In'), fr('in', 'Analog audio', '1/4" TRS', 2, 'Line In'), fr('out', 'Analog audio', '3.5mm jack', 1, 'Phones'),
        r('out', 'Analog audio', '1/4" TRS', 2, 'Monitor Out'), r('io', 'USB', 'USB-C', 1, 'USB')], ru=2, cols=4, box={'w': 126, 'h': 63}, url='https://usa.yamaha.com', notes='Check: ports.'),
]
# USB / Thunderbolt video I/O
VB = dict(cat='converter')
U += [
    usb('aja-io-x3', AJA, 'Io X3', 'Io X3 Thunderbolt 3 video I/O (4 x 3G-SDI, HDMI)', 'Io', [
        r('io', '3G-SDI', 'BNC', 4, 'SDI'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In'),
        r('in', 'Timecode', 'BNC', 1, 'LTC In'), r('out', 'Timecode', 'BNC', 1, 'LTC Out'), r('io', 'RS-422', 'DB9', 1, 'RS-422'), r('in', 'Analog audio', 'DB25 (8 ch)', 1, 'Analog Audio'),
        fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'XLR4M', 1, '12V DC')],
        ru=1, cols=6, box={'w': 222, 'h': 45}, url='https://www.aja.com/products/io-x3', bus='Thunderbolt', notes='Half rack wide. Check: counts.', **VB),
    usb('aja-io-4k-plus', AJA, 'Io 4K Plus', 'Io 4K Plus Thunderbolt 3 video I/O (12G-SDI, HDMI 2.0)', 'Io', [
        r('io', '12G-SDI', 'BNC', 4, 'SDI'), r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In'),
        r('in', 'Timecode', 'BNC', 1, 'LTC In'), r('out', 'Timecode', 'BNC', 1, 'LTC Out'), r('io', 'RS-422', 'DB9', 1, 'RS-422'), r('io', 'Analog audio', 'DB25 (8 ch)', 1, 'Analog Audio'),
        fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'XLR4M', 1, '12V DC')],
        ru=2, cols=6, box={'w': 222, 'h': 60}, url='https://www.aja.com/products/io-4k-plus', bus='Thunderbolt', notes='Check: counts.', **VB),
    usb('aja-t-tap-pro', AJA, 'T-TAP Pro', 'T-TAP Pro Thunderbolt 3 output (12G-SDI, HDMI 2.0)', 'T-TAP', [
        r('out', '12G-SDI', 'BNC', 2, 'SDI Out'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), r('in', 'Reference', 'BNC', 1, 'Ref In'), r('out', 'Analog audio', '1/4" TRS', 2, 'Analog Out'),
        fr('out', 'Analog audio', '1/4" TRS', 1, 'Phones'), r('io', 'USB', 'USB-C (Thunderbolt 3)', 2, 'Thunderbolt 3'), r('in', 'Power', 'DC locking', 1, '12V DC')],
        ru=1, cols=4, box={'w': 150, 'h': 40}, url='https://www.aja.com/products/t-tap-pro', bus='Thunderbolt', **VB),
    usb('aja-u-tap-sdi', AJA, 'U-TAP SDI', 'U-TAP SDI USB 3 capture', 'U-TAP', [
        r('in', '3G-SDI', 'BNC', 1, 'SDI In'), r('io', 'USB', 'USB-B', 1, 'USB 3')], ru=1, cols=2, box={'w': 70, 'h': 25}, url='https://www.aja.com/products/u-tap', notes='Bus powered.', **VB),
    usb('aja-u-tap-hdmi', AJA, 'U-TAP HDMI', 'U-TAP HDMI USB 3 capture', 'U-TAP', [
        r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('io', 'USB', 'USB-B', 1, 'USB 3')], ru=1, cols=2, box={'w': 70, 'h': 25}, url='https://www.aja.com/products/u-tap', notes='Bus powered.', **VB),
    usb('magewell-usb-capture-sdi-gen2', 'Magewell', '32060', 'USB Capture SDI Gen 2', 'USB Capture', [
        r('in', '3G-SDI', 'BNC', 1, 'SDI In'), r('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'), r('io', 'USB', 'USB-B', 1, 'USB 3')], ru=1, cols=2, box={'w': 63, 'h': 21}, url='https://www.magewell.com', notes='Bus powered. Check: loop out.', **VB),
    usb('magewell-usb-capture-hdmi-gen2', 'Magewell', '32090', 'USB Capture HDMI Gen 2', 'USB Capture', [
        r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('io', 'USB', 'USB-B', 1, 'USB 3')], ru=1, cols=2, box={'w': 63, 'h': 21}, url='https://www.magewell.com', notes='Bus powered.', **VB),
    usb('magewell-usb-capture-hdmi-4k-plus', 'Magewell', '32100', 'USB Capture HDMI 4K Plus', 'USB Capture', [
        r('in', 'HDMI', 'HDMI', 1, 'HDMI In'), r('out', 'HDMI', 'HDMI', 1, 'HDMI Loop Out'), r('in', 'Analog audio', '3.5mm jack', 1, 'Line In'), r('out', 'Analog audio', '3.5mm jack', 1, 'Line Out'), r('io', 'USB', 'USB-C', 1, 'USB 3')],
        ru=1, cols=3, box={'w': 110, 'h': 25}, url='https://www.magewell.com', notes='Check: ports.', **VB),
]
ids2 = [m['id'] for m in U]
assert len(ids2) == len(set(ids2)) and not set(ids2) & set(ids)
for m in U:
    m['portGroups'] = [x for x in m['portGroups'] if x['count'] > 0]


def write(name, rows):
    with open(os.path.join(CAT, name), 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=1, ensure_ascii=False)
        f.write('\n')
    print(name, len(rows))


write('pcie-cards.json', cards + pcs)
write('usb-interfaces.json', U)
idx_p = os.path.join(CAT, 'index.json')
idx = json.load(open(idx_p))
for n in ('pcie-cards.json', 'usb-interfaces.json'):
    if n not in idx:
        idx.append(n)
json.dump(idx, open(idx_p, 'w'), indent=1)
print('index', len(idx))
