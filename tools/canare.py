#!/usr/bin/env python3
"""Generates catalogue/canare.json: Canare video/audio/data patchbays, connector panels, IP and fibre panels, optical platform.

Conventions for patchbays (dual "normal through" jacks):
  rear 'in'  = top row  (source: equipment outputs land here)
  rear 'out' = bottom row (destination: feeds equipment inputs)
  front 'io' = every front jack (2 per circuit)
Canare: W jack = Normal Through, S jack = Straight Through (two independent self-terminating jacks per circuit).
1.5RU panels are catalogued as ru 2 (the app works in whole RU) with ruExact 1.5.
"""
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
CA = lambda *a, **k: add('canare.json', 'canare-', 'Canare', *a, **k)
P = 'https://www.canare.co.jp/en/products/panels_and_patchbays/index.php?tid='
SRC = 'Canare product page (Panels and Patchbays)'
AA = 'Analog audio'
W_NOTE = ('W (Normal Through): unpatched, top and bottom rear BNC are joined; a plug in the top jack takes the source and terminates the bottom. ')
S_NOTE = ('S (Straight Through): two independent jacks per circuit, each self-terminating when unpatched. ')

def ruspec(ru):
    """Returns (ru for the app, extra fields, text)."""
    if ru == 1.5:
        return 2, dict(ruExact=1.5), '1.5RU panel (catalogued as 2RU of rack space; two fit in 3RU). '
    return ru, {}, f'{ru}RU. '

def dual_vpb(id, pn, name, fam, ru, n, sig, fconn, rconn, mode, tid, extra, verified=True):
    rr, kw, rtxt = ruspec(ru)
    ports = [F('io', sig, fconn, 2 * n, 'Jack'),
             R('in', sig, rconn, n, 'Top (source)'), R('out', sig, rconn, n, 'Bottom (dest)')]
    CA(id, pn, name, fam, 'patch', rr, ports,
       rtxt + f'{n} circuits ({2 * n} front jacks, {2 * n} rear {rconn}). ' + (W_NOTE if mode == 'W' else S_NOTE) + extra,
       SRC, P + tid, verified=verified, **kw)

# ---------- 12G-SDI: 32MCKA-ST series (Canare Micro front, staggered BNC rear) ----------
MCKA = ('12G-SDI (SMPTE ST 2082-1), return loss 15 dB at 1.5 GHz, 4 dB at 12 GHz; isolation 45 dB or more at 6 GHz. '
        'Front takes Canare Micro patch cords (MCVPC) only. Staggered BNC rear with vertical stud position. Dust-proof shutters, '
        'channel designator strip, 25 mm recess standard (1RU can recess 50/75 mm with M-MA1U02A brackets). About 2.8 kg. '
        'Unloaded frame: MJ2-M32CKA-*U. ')
for ru, suf in [(1, ''), (1.5, '-1.5U'), (2, '-2U')]:
    for mode, s in [('W', ''), ('S', 'S')]:
        pn = f'32MCKA-ST{s}{suf}'
        dual_vpb(pn.lower().replace('.', ''), pn,
                 f'{pn} 12G-SDI staggered micro video patchbay, 2x32' + (' (straight through)' if s else ''),
                 '12G Micro Video Patchbay', ru, 32, '12G-SDI', 'Canare Micro jack', 'BNC', mode, '5_015', MCKA)

# ---------- 12G-SDI: 48MCK-H series (Canare Micro front, Micro BNC rear) ----------
for mode, s in [('W', ''), ('S', 'S')]:
    pn = f'48MCK-H{s}'
    dual_vpb(pn.lower(), pn, f'{pn} 12G-SDI micro video patchbay, 2x48, Micro BNC rear' + (' (straight through)' if s else ''),
             '12G Micro Video Patchbay', 1, 48, '12G-SDI', 'Canare Micro jack', 'Micro BNC', mode, '5_045',
             '12G-SDI (SMPTE ST 2082-1). 48 channels of I/O in 1RU. Jacks MCVJHK-W/-S. Micro BNC rear (Canare HBC series; check '
             'mating with HD-BNC before ordering cables). Dust-proof shutters, channel designator strip, 25 mm recess. '
             'Unloaded frame: MJ2-M48CK-1U.')

# ---------- 12G-SDI: 32SVK-ST single-jack patchbay ----------
for ru, suf in [(1, ''), (1.5, '-1.5U')]:
    rr, kw, rtxt = ruspec(ru)
    pn = f'32SVK-ST{suf}'
    CA(pn.lower().replace('.', ''), pn, f'{pn} 12G-SDI single video jack patchbay, 64 jacks', '12G Single Video Patchbay', 'patch', rr,
       [F('io', '12G-SDI', 'Canare Single jack', 64, 'Jack'), R('io', '12G-SDI', 'BNC', 64, 'Rear')],
       rtxt + '32 x SVJK-L plus 32 x SVJK-S single jacks (long and short, staggered), 64 front jacks each wired to its own rear BNC. '
       'Not normalled; use SVP-ULK U-links to join pairs and SVP-TK termination plugs. 12G-SDI (SMPTE ST 2082-1), return loss 15 dB at 12 GHz.',
       SRC, P + '5_035', **kw)

# ---------- 3G-SDI: 48MC series (Canare Micro front, DIN 1.0/2.3 rear) ----------
for mode, s in [('W', ''), ('S', 'S')]:
    pn = f'48MC{s}'
    dual_vpb(pn.lower(), pn, f'{pn} 3G-SDI micro video patchbay, 2x48, DIN 1.0/2.3 rear' + (' (straight through)' if s else ''),
             'Micro Video Patchbay', 1, 48, '3G-SDI', 'Canare Micro jack', 'DIN 1.0/2.3', mode, '5_011',
             '3G-SDI (SMPTE ST 424). High-density 48 circuits in 1RU, jacks MCVJ-W/-S. Unloaded frame: MJ2-M48CK-1U.')

# ---------- 3G-SDI: 32MD-ST series (Mini-WECO front, BNC rear) ----------
for ru, suf, n in [(1, '', 32), (2, '-2U', 32), (4, '-4U', 96)]:
    for mode, s in [('W', ''), ('S', 'S')]:
        pn = f'32MD-ST{s}{suf}'
        dual_vpb(pn.lower(), pn, f'{pn} 3G-SDI staggered mid-size video patchbay, {"3x" if n == 96 else ""}2x32' + (' (straight through)' if s else ''),
                 'Mid-size Video Patchbay', ru, n, '3G-SDI', 'Mini-WECO jack', 'BNC', mode, '5_005',
                 '3G-ready (2K/4K, 3G-SDI, HD-SDI). Mini-WECO front jacks MDVJ-STW/-STS, staggered BNC rear.'
                 + (' 4RU version holds 3 rows of 32 circuits.' if n == 96 else ''))

# ---------- 3G/HD-SDI: DV series (WECO front, BNC rear) ----------
for n in (20, 24, 26):
    for ru, suf in [(1, ''), (2, '-2U')]:
        for mode, s in [('W', ''), ('S', 'S')]:
            pn = f'{n}DV{s}{suf}'
            dual_vpb(pn.lower(), pn, f'{pn} WECO video patchbay, 2x{n}' + (' (straight through)' if s else ''),
                     'DV Video Patchbay', ru, n, '3G-SDI', 'WECO jack', 'BNC', mode, '5_001',
                     '3G-ready HD-SDI patchbay (SMPTE ST 292, ST 424, ST 425). WECO standard front jacks DVJB-W/-S, BNC rear. '
                     f'Unloaded frame: VJ2-V{n}-{ru}U.')

# ---------- Connector panels (pre-loaded) ----------
CP = P + '5_010'
for ru, n in [(1, 16), (2, 32)]:
    CA(f'16{ru}u-jruk', f'16{ru}U-JRUK', f'16{ru}U-JRUK 12G-SDI BNC feedthrough panel, {n} x BNC',
       'Connector Panel', 'patch', ru,
       [F('io', '12G-SDI', 'BNC', n, 'BNC'), R('io', '12G-SDI', 'BNC', n, 'Rear')],
       f'{ru}RU, {n} x BCJ-JRUK BNC jack-to-jack (female-female) 12G-SDI receptacles' + (', 2 rows' if ru == 2 else '') + '.', SRC, CP)
XLRP = [('161u-x1f', '161U-X1F', 1, [F('io', AA, 'XLR3F', 16, 'XLR F')], '16 x XLR3-31F77 (XLR female, solder rear).'),
        ('161u-x2f', '161U-X2F', 1, [F('io', AA, 'XLR3M', 16, 'XLR M')], '16 x XLR3-32F77 (XLR male, solder rear).'),
        ('161u-x12f', '161U-X12F', 1, [F('io', AA, 'XLR3F', 8, 'XLR F'), F('io', AA, 'XLR3M', 8, 'XLR M')],
         '8 x XLR3-31F77 female (left) and 8 x XLR3-32F77 male (right), solder rear.'),
        ('161u-b1', '161U-B1', 1, [F('io', AA, 'XLR3F', 16, 'XLR F')], '16 x Neutrik NC3FD-LX-B (D-type XLR female, black).'),
        ('161u-b2', '161U-B2', 1, [F('io', AA, 'XLR3M', 16, 'XLR M')], '16 x Neutrik NC3MD-LX-B (D-type XLR male, black).')]
for id, pn, ru, fr, txt in XLRP:
    n = sum(p['count'] for p in fr)
    CA(id, pn, f'{pn} XLR connector panel, {n} x XLR', 'Connector Panel', 'patch', ru,
       fr + [R('io', AA, 'Solder', n, 'Rear')], f'{ru}RU. {txt} Rear is solder cups (hard-wired).', SRC, CP)
CA('162u-x21', '162U-X21', '162U-X21 XLR feedthrough panel, 16 male + 16 female', 'Connector Panel', 'patch', 2,
   [F('io', AA, 'XLR3M', 16, 'Upper XLR M'), F('io', AA, 'XLR3F', 16, 'Lower XLR F'),
    R('io', AA, 'XLR3F', 16, 'Upper rear XLR F'), R('io', AA, 'XLR3M', 16, 'Lower rear XLR M')],
   '2RU. Upper row 16 x XJ3M-P3FA (front XLR male, rear XLR female), lower row 16 x XJ3F-P3MA (front XLR female, rear XLR male). '
   'Plug-in on both sides, no soldering.', SRC, CP)
CA('162u-x22', '162U-X22', '162U-X22 XLR feedthrough panel, 32 x male-to-female', 'Connector Panel', 'patch', 2,
   [F('io', AA, 'XLR3M', 32, 'XLR M'), R('io', AA, 'XLR3F', 32, 'Rear XLR F')],
   '2RU, 2 rows of 16 x XJ3M-P3FA (front XLR male, rear XLR female).', SRC, CP)

# ---------- Unloaded A/V connector panels (AS series) ----------
AS = {1: ('flat panel', None), 3: ('flat panel with cable tie bar', 64.8), 5: ('variable panel with cable tie bar, short', 100),
      7: ('variable panel with cable tie bar, long', 217)}
for ru in (1, 2, 3):
    for t, (desc, d) in AS.items():
        n = 16 * ru
        kw = dict(depthMm=d) if d else {}
        CA(f'{ru}u-as{t}', f'{ru}U-AS{t}', f'{ru}U-AS{t} unloaded connector panel, {n} holes ({desc})', 'AS Connector Panel', 'patch', ru,
           [F('io', 'Other', 'XLR-D cutout', n, 'Hole')],
           f'{ru}RU, {ru} row(s) of 16 XLR F-77 / Neutrik D-size holes, {desc}' + (f', {d} mm deep' if d else '') + '. '
           'Unloaded: fit Canare recessed BNC, F, RCA or XLR (ITT XLR-F77 or Neutrik D) and change the port type to suit. '
           'A (D) variant is also listed; Canare does not define the suffix.', SRC, P + '5_026', **kw)

# ---------- Audio patchbays ----------
NORM = {'F': 'full normal (series)', 'H': 'half normal (half-parallel)', 'W': 'double normal (series-parallel)'}
for s, nd in NORM.items():
    CA(f'48wb-{s.lower()}', f'48WB-{s}', f'48WB-{s} bantam audio patchbay, 2x48, wired ({nd})', 'Bantam Patchbay', 'patch', 1,
       [F('io', AA, 'Bantam (TT)', 96, 'Jack'), R('io', AA, '90-602 multipin', 4, 'Multipin')],
       f'1RU, 96 bantam jacks (820AQ) in 2 rows of 48, wired box, {nd} normalling. Rear 4 x 90-602 multipin connectors '
       '(mate with 90-608). Top row = device outputs, bottom row = device inputs. Check: multipin pinout and which jacks each connector carries.',
       SRC, P + '5_020')
    CA(f'32wb-{s.lower()}', f'32WB-{s}', f'32WB-{s} Skini audio patchbay, 2x32, wired ({nd})', 'Skini Patchbay', 'patch', 1,
       [F('io', AA, 'Skini jack', 64, 'Jack'), R('io', AA, '90-602 multipin', 4, 'Multipin')],
       f'1RU, 64 Skini jacks (620A) in 2 rows of 32, wired box, {nd} normalling. Rear 4 x 90-602 multipin connectors (mate with 90-608). '
       'Check: multipin pinout.', SRC, P + '5_019')
    CA(f'48xp-{s.lower()}', f'48XP-{s}', f'48XP-{s} bantam audio patchbay, 2x48, wired to XLR panels ({nd})', 'Bantam Patchbay', 'patch', 1,
       [F('io', AA, 'Bantam (TT)', 96, 'Jack')],
       f'1RU jackfield (96 bantam jacks, 2x48, {nd}) pre-wired to two 3RU XLR panels with 48 x XLR3-31F77 female and 48 x XLR3-32F77 male '
       'in total. Add two "48XP rear XLR panel" entries for the XLR panels.', SRC, P + '5_020')
    CA(f'32xp-{s.lower()}', f'32XP-{s}', f'32XP-{s} Skini audio patchbay, 2x32, wired to XLR panel ({nd})', 'Skini Patchbay', 'patch', 1,
       [F('io', AA, 'Skini jack', 64, 'Jack')],
       f'1RU jackfield (64 Skini jacks, 2x32, {nd}) pre-wired to a 4RU XLR panel with 32 x XLR3-31F77 female and 32 x XLR3-32F77 male. '
       'Add the "32XP rear XLR panel" entry for the XLR panel.', SRC, P + '5_019')
CA('48xp-xlr-3u', '48XP (XLR panel)', '48XP rear XLR panel, 3RU, 24 F + 24 M', 'Bantam Patchbay', 'patch', 3,
   [F('in', AA, 'XLR3F', 24, 'XLR F (to top row)'), F('out', AA, 'XLR3M', 24, 'XLR M (from bottom row)')],
   'One of the two 3RU XLR panels supplied with a 48XP-F/H/W bantam patchbay (48 F + 48 M across both). Check: how Canare splits '
   'the 48 female and 48 male XLRs between the two panels.', SRC, P + '5_020', verified=False)
CA('32xp-xlr-4u', '32XP (XLR panel)', '32XP rear XLR panel, 4RU, 32 F + 32 M', 'Skini Patchbay', 'patch', 4,
   [F('in', AA, 'XLR3F', 32, 'XLR F (to top row)'), F('out', AA, 'XLR3M', 32, 'XLR M (from bottom row)')],
   '4RU XLR panel supplied with a 32XP-F/H/W Skini patchbay: 32 x XLR3-31F77 female and 32 x XLR3-32F77 male. '
   'Check: which row each gender feeds.', SRC, P + '5_019', verified=False)
CA('481u-820aq', '481U-820AQ', '481U-820AQ bantam patchbay, 2x48, unwired', 'Bantam Patchbay', 'patch', 1,
   [F('io', AA, 'Bantam (TT)', 96, 'Jack'), R('io', AA, 'Solder', 96, 'Rear')],
   '1RU, 96 bantam jack holes in 2 rows (820AQ jacks), unwired: rear terminations are made by the installer. Can be recessed 25 mm.',
   SRC, P + '5_020')
CA('32-12a-620a-eia', '32-12A/620A/EIA', '32-12A/620A/EIA Skini patchbay, 2x32, unwired', 'Skini Patchbay', 'patch', 1,
   [F('io', AA, 'Skini jack', 64, 'Jack'), R('io', AA, 'Solder', 64, 'Rear')],
   '1RU, 2 rows of 32 Skini (620A) jacks, unwired.', SRC, P + '5_019')

# ---------- RS-422 patchbays ----------
for ru, n in [(1, 16), (1, 24), (2, 32), (2, 48)]:
    CA(f'rs-422-{ru}u-{n}', f'RS-422-{ru}U-{n}', f'RS-422-{ru}U-{n} RS-422 bantam patchbay, {n} x DB9', 'RS-422 Patchbay', 'patch', ru,
       [F('io', 'RS-422', 'Bantam (TT)', 2 * n, 'Jack'), R('io', 'RS-422', 'DB9F', n, 'Port')],
       f'{ru}RU bantam jack panel for RS-422 serial data, full-normalled at the jacks, T/R/S wired to {n} x 9-pin D-sub female (M2.6 screws). '
       'Resold by Canare (made by another manufacturer). Check: front jack count (Canare does not list it; 2 per port assumed).',
       SRC, P + '5_023', verified=False)

# ---------- IP and fibre panels ----------
for id, pn, sh in [('24krj-6ajj', '24KRJ-6AJJ', 'unshielded'), ('24krjs-6ajj', '24KRJS-6AJJ', 'shielded')]:
    CA(id, pn, f'{pn} 24-port keystone Cat6A coupler panel ({sh})', 'Keystone IP Panel', 'patch', 1,
       [F('io', 'Ethernet', 'RJ45', 24, 'Port'), R('io', 'Ethernet', 'RJ45', 24, 'Rear')],
       f'1RU black keystone panel loaded with 24 RJ45 {sh} Cat6A couplers (jack-to-jack).', SRC, P + '5_042')
CA('k24s-1u-blk', 'K24S-1U-BLK', 'K24S-1U-BLK 24-hole keystone panel (unloaded)', 'Keystone IP Panel', 'patch', 1,
   [F('io', 'Other', 'Keystone', 24, 'Slot'), R('io', 'Other', 'Keystone', 24, 'Rear')],
   '1RU black, 24 keystone holes, unloaded. Modules: RJUJ-J6A / RJSJ-J6A RJ45, FKDLJ LC duplex, FKSJ SC, FKMPJ MPO, KBCJ-JRK BNC 12G, '
   'KBCJ-HBCJK BNC to Micro BNC, KBCJ-DCJ BNC to DIN, KHBCJ-JRK Micro BNC, KDCJ-JR DIN, BP-K blanks. Change the port types to the modules fitted.',
   SRC, P + '5_042')
FS = 'https://www.canare.co.jp/en/products/fiber_optic_systems/index.php?tid='
CA('48kfce-dlc-sjjs', '48KFCE-DLC-SJJS', '48KFCE-DLC-SJJS fibre splice panel, 24 x LC duplex SM', 'Fibre Splice Unit', 'patch', 1,
   [F('io', 'Fibre', 'LC duplex', 24, 'LC'), R('io', 'Fibre', 'Splice', 48, 'Splice')],
   '1RU splice unit, 48 fibres on 24 x FKDLJ-JS-S LC duplex single-mode couplers with shutters, 4 splice trays.',
   'Canare product page (Fiber-Optic Splice Unit)', FS + '1_059')
CA('24kfce-sc-sjjs', '24KFCE-SC-SJJS', '24KFCE-SC-SJJS fibre splice panel, 24 x SC SM', 'Fibre Splice Unit', 'patch', 1,
   [F('io', 'Fibre', 'SC', 24, 'SC'), R('io', 'Fibre', 'Splice', 24, 'Splice')],
   '1RU splice unit, 24 fibres on 24 x FKSJ-JS-S SC single-mode couplers with shutters, 2 splice trays.',
   'Canare product page (Fiber-Optic Splice Unit)', FS + '1_059')

# ---------- Optical converter platform ----------
CA('161upsc', '161UPSC', '161UPSC 1RU optical converter platform, 16 slots', 'Optical Platform', 'converter', 1,
   [R('io', 'Other', 'Card slot', 16, 'Module slot'), R('in', 'Power', 'IEC', 1, 'AC In'), R('out', 'Other', 'DB9F', 1, 'Alarm')],
   '1RU frame for up to 16 hot-swap Canare TRM plug-in converter modules (SDI, audio, Ethernet, RS-422 over fibre), 100-240 V AC, '
   'D-sub 9 female alarm output (4 alarm types). Add a PSM2 module for redundant power. Add each module\'s connectors as extra ports. '
   'Check: which face the modules load from, and the AC inlet type (Canare lists "AC3P jack").',
   'Canare product page (Platforms)', FS + '1_008', verified=False)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(idx)
