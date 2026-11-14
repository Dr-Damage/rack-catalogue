#!/usr/bin/env python3
"""Generates catalogue/aten.json: ATEN rack KVM gear. Added 2026-11-14.

- KN Cat 5 KVM over IP switches (VB and VA generations), KH Cat 5 KVM switches and KM Cat 5 matrix KVM switches.
  Their computer ports are RJ45 for ATEN's KA7xxx computer adapters (one per server, carries video + USB/PS2 over
  Cat 5e/6); they are not Ethernet, so they use type 'KVM link'.
- LCD KVM switches (1U slide-out drawer with screen, keyboard and touchpad plus a built-in KVM switch) and LCD
  consoles (drawer only). CL15/57/58/13/31 switches take ATEN KVM cables on SPHD-15 ports; KL switches take Cat 5.
  Model suffix N = 19 in screen, M = 17 in, MW = 17.3 in wide, NW/NX = 18.5 in wide.
Sources are ATEN product pages (aten.com/au); verified=False and a 'Check:' note mark entries whose connectors were
taken from a sibling model."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
MODELS = []
AU = 'https://www.aten.com/au/en/products/kvm/'
def add(id, pn, name, fam, cat, ru, ports, notes, url, verified=False, src='ATEN product page', **kw):
    m = dict(id='aten-' + id, manufacturer='ATEN', partNumber=pn, name=name, family=fam, category=cat, ru=ru,
             widthCols=kw.pop('w', 12), fullDepth=kw.pop('full', True), verified=verified, source=src, productUrl=url, notes=notes,
             portGroups=ports)
    m.update(kw); MODELS.append(m); return m
KVM = 'KVM link'
def cat5(n, p='KVM port (Cat 5, KA7xxx adapter)'): return R('io', KVM, 'RJ45', n, p)
def sphd(n): return R('io', KVM, 'SPHD-15', n, 'KVM port (ATEN KVM cable)')
AC = lambda n=1: R('in', 'Power', 'IEC C14', n, 'AC In' if n == 1 else 'AC In (dual PSU)')
CHK = ' Check: connectors (taken from a sibling model).'

# ---------------- KN Cat 5 KVM over IP switches (VB generation, current) ----------------
VB = [('KN1132VB', 1, 32, 1), ('KN2116VB', 2, 16, 1), ('KN2124VB', 2, 24, 1), ('KN2132VB', 2, 32, 1),
      ('KN4016VB', 4, 16, 1), ('KN4024VB', 4, 24, 1), ('KN4032VB', 4, 32, 1), ('KN4064VB', 4, 64, 2),
      ('KN8032VB', 8, 32, 1), ('KN8064VB', 8, 64, 2)]
for pn, remote, n, ru in VB:
    add(pn.lower(), pn, f'{pn} {n}-port Cat 5 KVM over IP switch (1 local / {remote} remote)', 'ATEN KN KVM over IP (VB)', 'control', ru,
        [cat5(n), R('io', 'USB', 'USB-A', 2, 'Local console USB (keyboard, mouse)'), R('out', 'HDMI', 'HDMI', 1, 'Local console HDMI Out'),
         R('out', 'VGA', 'HD15', 1, 'Local console VGA Out'), R('io', 'USB', 'USB-A', 3, 'USB (virtual media / peripherals)'),
         R('io', 'Analog audio', '3.5mm jack', 2, 'Console audio (mic / speaker)'), R('io', 'USB', 'Mini-USB', 1, 'Laptop USB Console (LUC)'),
         R('io', 'RS-232', 'RJ45', 1, 'Serial'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)'),
         R('io', 'Ethernet', 'RJ45', 2, 'LAN (1G, dual)'), AC(2)],
        f'Multi-interface KVM over IP switch: {n} computer ports for KA7xxx computer adapters (VGA, DVI, HDMI or DisplayPort; USB or PS/2), '
        f'cascades to 512 computers, one local console and {remote} concurrent remote users over two gigabit LAN ports with virtual media. '
        f'{ru}U, dual power. ' + ('43.4 x 41.3 x 8.8 cm, 7.1 kg, about 50 W.' if ru == 2 else 'About 40-50 W.') + ('' if pn == 'KN4064VB' else CHK),
        AU + 'kvm-over-ip-switches/' + pn.lower() + '/', verified=(pn == 'KN4064VB'), powerW=50)
# ---------------- KN VA generation (8/16 port with virtual media, plus the discontinued KN2132VA) ----------------
for pn, n in (('KN1108VA', 8), ('KN1116VA', 16)):
    add(pn.lower(), pn, f'{pn} {n}-port Cat 5 KVM over IP switch with virtual media (1 local / 1 remote)', 'ATEN KN KVM over IP (VA)', 'control', 1,
        [cat5(n), R('io', 'USB', 'USB-A', 2, 'Local console USB'), R('out', 'VGA', 'HD15', 1, 'Local console VGA Out'),
         R('io', 'USB', 'USB-A', 1, 'USB (virtual media)'), R('io', 'Ethernet', 'RJ45', 1, 'LAN (1G)'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)'),
         AC(1)],
        f'{n} computer ports for KA7xxx adapters, one local VGA/USB console and one remote user, virtual media, 1920 x 1200. 1U.' + CHK,
        AU + 'kvm-over-ip-switches/' + pn.lower() + '/', powerW=30)
add('kn2132va', 'KN2132VA', 'KN2132VA 32-port Cat 5 KVM over IP switch (1 local / 2 remote, discontinued)', 'ATEN KN KVM over IP (VA)', 'control', 1,
    [cat5(32), R('io', 'USB', 'USB-A', 2, 'Local console USB (keyboard, mouse)'), R('out', 'DVI', 'DVI-D', 1, 'Local console DVI Out'),
     R('out', 'VGA', 'HD15', 1, 'Local console VGA Out'), R('io', 'Other', 'RJ45', 1, 'Local console (Cat 5 remote console)'),
     R('io', 'Analog audio', '3.5mm jack', 2, 'Console audio'), R('io', 'USB', 'USB-A', 3, 'USB (virtual media)'),
     R('io', 'USB', 'Mini-USB', 1, 'Laptop USB Console (LUC)'), R('io', 'RS-232', 'RJ45', 1, 'Serial / modem'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)'),
     R('io', 'Ethernet', 'RJ45', 2, 'LAN (1G, dual)'), AC(2)],
    'Discontinued; replaced by KN2132VB. 32 computer ports for KA7xxx adapters, cascades to 512, 1U, 43.4 x 41.2 x 4.4 cm, 5.7 kg, 40 W.',
    AU + 'kvm-over-ip-switches/kn2132va/', verified=True, powerW=40, weightKg=5.69)
add('kn4116va', 'KN4116VA', 'KN4116VA 16-port Cat 5 KVM over IP switch (1 local / 4 remote)', 'ATEN KN KVM over IP (VA)', 'control', 1,
    [cat5(16), R('io', 'USB', 'USB-A', 2, 'Local console USB'), R('out', 'DVI', 'DVI-D', 1, 'Local console DVI Out'), R('out', 'VGA', 'HD15', 1, 'Local console VGA Out'),
     R('io', 'Analog audio', '3.5mm jack', 2, 'Console audio'), R('io', 'USB', 'USB-A', 3, 'USB (virtual media)'), R('io', 'RS-232', 'RJ45', 1, 'Serial / modem'),
     R('io', 'Other', 'RJ45', 1, 'PON (power switch)'), R('io', 'Ethernet', 'RJ45', 2, 'LAN (1G, dual)'), AC(2)],
    '16 computer ports for KA7xxx adapters, 1 local + 4 remote users, 1U.' + CHK, AU + 'kvm-over-ip-switches/kn4116va/', powerW=40)

# ---------------- KH Cat 5 KVM switches (short-depth 1U) ----------------
for pn, cons, n, ip in (('KH1508A', 1, 8, False), ('KH1516A', 1, 16, False), ('KH1532A', 1, 32, False), ('KH2508A', 2, 8, False),
                        ('KH2516A', 2, 16, False), ('KH1508Ai', 1, 8, True), ('KH1516Ai', 1, 16, True)):
    ports = [cat5(n), R('io', 'USB', 'USB-A', 2 * cons, 'Console USB (keyboard, mouse)'),
             R('in', 'Other', 'Mini-DIN 6', cons, 'Console PS/2 keyboard'), R('in', 'Other', 'Mini-DIN 6', cons, 'Console PS/2 mouse'),
             R('out', 'VGA', 'HD15', cons, 'Console VGA Out')]
    if ip: ports += [R('io', 'Ethernet', 'RJ45', 1, 'LAN (remote access)'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)')]
    else: ports += [R('io', 'Other', 'DB-25', 2, 'Daisy chain (in / out)'), R('io', 'Other', 'RJ11', 1, 'Firmware upgrade')]
    ports.append(AC(1))
    add(pn.lower(), pn, f'{pn} {"2-console " if cons == 2 else ""}{n}-port Cat 5 KVM switch{" over IP (1 local / remote shared)" if ip else ""}',
        'ATEN KH Cat 5 KVM', 'control', 1, ports,
        f'{n} computer ports for KA7xxx adapters (DisplayPort, HDMI, DVI or VGA computers), {cons} PS/2 or USB console{"s" if cons > 1 else ""}, '
        f'{"remote IP access, " if ip else "daisy-chains to 256 computers, "}1U short-depth metal housing (43.7 x 15.6 x 4.4 cm for KH2516A, 2.85 kg, '
        'about 10 W), rack kit included.' + ('' if pn == 'KH2516A' else CHK), AU + 'cat-5-kvm-switches/' + pn.lower() + '/',
        verified=(pn == 'KH2516A'), full=False, powerW=11)

# ---------------- KM Cat 5 matrix KVM switches ----------------
for pn, cons in (('KM0932', 9), ('KM0532', 5), ('KM0432', 4), ('KM0032', 0)):
    ports = [cat5(32)] + ([R('io', KVM, 'RJ45', cons, 'Console port (KA7240 / KA7230 console adapter)')] if cons else []) + \
            [R('io', 'Other', 'VHDCI-68', 1, 'Daisy chain'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)'), AC(2)]
    add(pn.lower(), pn, f'{pn} {"32-port matrix KVM expansion switch" if not cons else f"{cons}-console 32-port Cat 5 matrix KVM switch"}', 'ATEN KM matrix KVM',
        'router', 1, ports,
        (f'{cons} independent consoles (each on a Cat 5 console adapter) reach any of 32 computers (KA7xxx adapters); ' if cons else
         'Adds 32 computer ports to a KM0932 / KM0532 / KM0432; ') + 'up to 7 units daisy-chain on the VHDCI port. 1U, 43.8 x 41.1 x 4.4 cm, '
        'about 6 kg, 50 W, dual power. Discontinued at ATEN; the KE matrix (KVM over IP extenders) replaces it.' + ('' if pn == 'KM0932' else CHK),
        AU + 'matrix-kvm-switches/' + pn.lower() + '/', verified=(pn == 'KM0932'), powerW=54, weightKg=6.08)

# ---------------- LCD KVM switches (1U drawer with a built-in KVM switch) ----------------
LCD = AU + 'lcd-kvm-switches--consoles/'
def lcd(pn, desc, n, kind, ip=False, dual=False, screens='', extra='', alt='', cl57=False):
    port = {'sphd': sphd(n), 'cat5': cat5(n), 'hdmi': R('io', KVM, 'Other', n, 'KVM port (ATEN USB HDMI KVM cable)'),
            'dvi': R('io', KVM, 'Other', n, 'KVM port (ATEN USB DVI KVM cable)')}[kind]
    if cl57:  # CL5708N/CL5716N datasheet: SPHD-18 external console, USB mouse, DB-25 daisy chain, RJ-11 firmware port
        ports = [port, R('io', KVM, 'SPHD-18', 1, 'External console (Console 2)'), R('io', 'USB', 'USB-A', 1, 'External mouse'),
                 R('out', KVM, 'DB25', 1, 'Daisy-chain (Chain Out)'), R('io', 'Other', 'RJ11', 1, 'Firmware upgrade'),
                 F('io', 'USB', 'USB-A', 1, 'USB (LCD module)')]
    else:
        ports = [port, R('out', 'VGA', 'HD15', 1, 'External console VGA Out'), R('io', 'USB', 'USB-A', 2, 'External console USB')]
    if ip: ports += [R('io', 'Ethernet', 'RJ45', 1, 'LAN (remote access)'), R('io', 'Other', 'RJ45', 1, 'PON (power switch)')]
    ports.append(AC(1))
    add(pn.lower(), pn, f'{pn} {desc} LCD KVM {"over IP " if ip else ""}switch, {n} ports{", dual rail" if dual else ""}{alt}', 'ATEN LCD KVM switches', 'control', 1, ports,
        f'1U slide-out drawer with LCD screen{" (" + screens + ")" if screens else ""}, keyboard and touchpad, and a built-in {n}-port KVM switch'
        f'{" with remote IP access" if ip else ""}. {"Dual rail: the screen and the keyboard slide out separately. " if dual else ""}{extra}'
        f'{"Computer ports take ATEN KVM cables (SPHD-15 to VGA + USB/PS2). " if kind == "sphd" else "Computer ports take KA7xxx Cat 5 adapters. " if kind == "cat5" else ""}'
        + ('Rear connectors from the CL5708N/CL5716N datasheet (SPHD-18 external console, DB-25 daisy chain, RJ-11 firmware port). '
           if cl57 else 'Check: rear connectors (external console and power taken as a typical ATEN LCD KVM switch).'), LCD + pn.lower() + '/', powerW=40)
lcd('CL5708N', 'PS/2-USB VGA single rail', 8, 'sphd', cl57=True, screens='CL5708N 19 in, CL5708M 17 in', alt=' (CL5708M 17 in)')
lcd('CL5716N', 'PS/2-USB VGA single rail', 16, 'sphd', cl57=True, screens='CL5716N 19 in, CL5716M 17 in', alt=' (CL5716M 17 in)')
lcd('CL5708iN', 'PS/2-USB VGA single rail', 8, 'sphd', cl57=True, ip=True, screens='CL5708iN 19 in, CL5708iM 17 in', alt=' (CL5708iM 17 in)')
lcd('CL5716iN', 'PS/2-USB VGA single rail', 16, 'sphd', cl57=True, ip=True, screens='CL5716iN 19 in, CL5716iM 17 in', alt=' (CL5716iM 17 in)')
lcd('CL5808N', 'PS/2-USB VGA', 8, 'sphd', dual=True, screens='19 in')
lcd('CL5816N', 'PS/2-USB VGA', 16, 'sphd', dual=True, screens='19 in')
lcd('CL1308N', 'PS/2-USB VGA single rail', 8, 'sphd', screens='19 in')
lcd('CL1316N', 'PS/2-USB VGA single rail', 16, 'sphd', screens='19 in')
lcd('CL3108NX', 'PS/2-USB VGA single rail widescreen', 8, 'sphd', screens='18.5 in wide')
lcd('CL3116NX', 'PS/2-USB VGA single rail widescreen', 16, 'sphd', screens='18.5 in wide')
lcd('CL3708NW', 'USB HDMI single rail widescreen', 8, 'hdmi', screens='18.5 in wide')
lcd('CL3716NW', 'USB HDMI single rail widescreen', 16, 'hdmi', screens='18.5 in wide')
lcd('CL3708iNW', 'USB HDMI single rail widescreen FHD', 8, 'hdmi', ip=True, screens='18.5 in wide')
lcd('CL3716iNW', 'USB HDMI single rail widescreen FHD', 16, 'hdmi', ip=True, screens='18.5 in wide')
lcd('CL6708MW', 'USB DVI single rail widescreen', 8, 'dvi', screens='17.3 in wide')
lcd('KL1508AN', 'multi-interface Cat 5', 8, 'cat5', dual=True, screens='KL1508AN 19 in, KL1508AM 17 in', alt=' (KL1508AM 17 in)')
lcd('KL1516AN', 'multi-interface Cat 5', 16, 'cat5', dual=True, screens='KL1516AN 19 in, KL1516AM 17 in', alt=' (KL1516AM 17 in)')
lcd('KL1508AiN', 'multi-interface Cat 5', 8, 'cat5', ip=True, dual=True, screens='KL1508AiN 19 in, KL1508AiM 17 in', alt=' (KL1508AiM 17 in)')
lcd('KL1516AiN', 'multi-interface Cat 5', 16, 'cat5', ip=True, dual=True, screens='KL1516AiN 19 in, KL1516AiM 17 in', alt=' (KL1516AiM 17 in)')
lcd('KL1108VN', 'multi-interface Cat 5 (1 local / 1 remote)', 8, 'cat5', ip=True, dual=True, screens='19 in')
lcd('KL1116VN', 'multi-interface Cat 5 (1 local / 1 remote)', 16, 'cat5', ip=True, dual=True, screens='19 in')
add('cl3884nw', 'CL3884NW', 'CL3884NW 4-port USB HDMI multi-view dual rail widescreen LCD KVM switch', 'ATEN LCD KVM switches', 'control', 1,
    [R('in', 'HDMI', 'HDMI', 4, 'Computer HDMI In'), R('in', 'USB', 'USB-B', 4, 'Computer USB'), R('out', 'HDMI', 'HDMI', 1, 'External console HDMI Out'),
     R('io', 'USB', 'USB-A', 2, 'External console USB'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
    '1U dual-rail drawer with an 18.5 in widescreen showing up to four computers at once (multi-view), keyboard and touchpad. '
    'Check: rear connectors.', LCD + 'cl3884nw/', powerW=40)

# ---------------- LCD consoles (drawer only, feeds a separate KVM switch or one server) ----------------
for pn, desc, vids, dual, short, scr in (
        ('CL1000N', 'PS/2-USB VGA single rail', ['VGA'], False, False, '19 in (CL1000M 17 in)'),
        ('CL5800N', 'PS/2-USB VGA dual rail', ['VGA'], True, False, '19 in'),
        ('CL6700MW', 'USB HDMI/DVI/VGA single rail', ['HDMI', 'DVI', 'VGA'], False, False, '17.3 in wide (CL6700N 19 in)'),
        ('CL3100NX', 'ultra short depth USB VGA single rail widescreen', ['VGA'], False, True, '18.5 in wide'),
        ('CL3700NW', 'ultra short depth USB HDMI single rail widescreen', ['HDMI'], False, True, '18.5 in wide (also CL3700NX)'),
        ('CL3800NW', 'ultra short depth USB HDMI/DVI/VGA dual rail widescreen', ['HDMI', 'DVI', 'VGA'], True, True, '18.5 in wide (also CL3800NX)')):
    conn = {'VGA': ('VGA', 'HD15'), 'HDMI': ('HDMI', 'HDMI'), 'DVI': ('DVI', 'DVI-D')}
    ports = [R('in', conn[v][0], conn[v][1], 1, f'{v} In (from KVM switch or computer)') for v in vids] + \
            [R('io', 'USB', 'USB-B', 1, 'USB (keyboard, touchpad to KVM switch or computer)')]
    if 'PS/2' in desc: ports += [R('out', 'Other', 'Mini-DIN 6', 2, 'PS/2 keyboard / mouse')]
    ports.append(R('in', 'Power', 'IEC C14', 1, 'AC In'))
    add(pn.lower(), pn, f'{pn} {desc} LCD console', 'ATEN LCD consoles', 'control', 1, ports,
        f'1U slide-out LCD console ({scr}) with keyboard and touchpad, no KVM switch inside: it is the rack console for a separate KVM '
        f'switch or one server. {"Dual rail: screen and keyboard slide out separately. " if dual else ""}'
        f'{"Ultra short depth, for shallow racks. " if short else ""}Check: rear connectors.', LCD + pn.lower().rstrip('nwxm') + '/',
        full=not short, powerW=30)

ids = [m['id'] for m in MODELS]; assert len(ids) == len(set(ids))
json.dump(MODELS, open(os.path.join(CAT, 'aten.json'), 'w'), indent=1)
print('aten.json', len(MODELS), 'entries,', sum(m['verified'] for m in MODELS), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'aten.json' not in idx: idx.append('aten.json')
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
