#!/usr/bin/env python3
"""Generates catalogue/allenheath-more.json, roland-more.json and mackie.json (added 2026-11-14).

allenheath-more.json  Allen & Heath gear missing from allenheath.json (tools/audio.py): AHM matrix processors, dLive DM0,
                      DX012, GX4816, DT168, DX Hub, ME-U and the GLD AR2412 AudioRack.
roland-more.json      Roland REAC digital snakes (S-2416, S-1608, S-0816), S-MADI bridge, S-4000D splitter, XS-42H and
                      V-1200HD. The XS-82H/83H/84H matrices stay in roland.json (tools/streaming.py).
mackie.json           Mackie DL series rack mixers (DL32R, DL32S, DL32SE, DL16S, DL16SE).

verified=True only where the port counts come from the maker's datasheet or spec page. Notes start any doubt with
"Check:" (usually which panel a connector is on, which datasheets rarely say)."""
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
AA, AO = 'Analog audio', 'AES/EBU'
IEC = lambda face='rear', n=1, p='AC In': g(face, 'in', 'Power', 'IEC', n, p)

# ---------------- Allen & Heath ----------------
A = lambda *a, **k: add('allenheath-more.json', 'ah-', 'Allen & Heath', *a, **k)
AHM = 'https://www.allen-heath.com/hardware/ahm/'
A('ahm-64', 'AHM-64', 'AHM-64 64x64 audio matrix processor', 'AHM', 'audio', 2,
  [R('in', AA, 'Phoenix', 12, 'Mic/Line In'), R('out', AA, 'Phoenix', 12, 'Line Out'), R('io', 'Other', 'Card slot', 1, 'I/O Port'),
   R('io', 'Other', 'etherCON', 1, 'SLink'), R('io', 'Ethernet', 'RJ45', 1, 'Control Network'), R('io', 'GPIO', 'Phoenix', 1, 'GPIO (2 in, 2 relay out)'),
   IEC(), R('in', 'Power', 'Phoenix', 1, '12 V DC backup')],
  '2U, 482.6 x 364 x 91 mm, 7 kg, 70 W max. 64x64 matrix processor for installed audio: 12 mic/line inputs (+48 V) and 12 outputs on '
  'pluggable Phoenix blocks, SLink port (128x128, to DX/GX expanders, AudioRacks or an SQ), one I/O Port slot (128x128, e.g. Dante 64x64), '
  'control network for System Manager and IP remotes, 2 GPI and 2 relay outputs, mains IEC plus 12 V DC backup input. '
  'Check: SLink connector type (the datasheet only says Cat5e).', 'AHM-64 technical datasheet',
  'https://goknight.com/content/documentation/AH-AHM-64%2064x64%20Audio%20Matrix%20Processor%20Spec%20Sheet.pdf', powerW=70, weightKg=7)
A('ahm-32', 'AHM-32', 'AHM-32 32x32 audio matrix processor', 'AHM', 'audio', 1,
  [R('in', AA, 'Phoenix', 12, 'Mic/Line In'), R('out', AA, 'Phoenix', 12, 'Line Out'), R('io', 'Other', 'Card slot', 1, 'I/O Port'),
   R('io', 'Other', 'Card slot', 1, 'Processing module (AEC)'), R('io', 'Ethernet', 'RJ45', 1, 'Control Network'),
   R('io', 'GPIO', 'Phoenix', 1, 'GPIO (2 in, 2 relay out)'), IEC()],
  '1U, 482.6 x 270 x 44 mm, 4 kg, 70 W max. 12 mic/line inputs (+48 V) and 12 outputs on Phoenix blocks, one I/O Port slot (128x128, '
  'Dante or SLink card), one processing module slot (e.g. AEC), control network, 2 GPI and 2 relay outputs. Front: screen and 8 SoftKeys.',
  'AHM-32 spec sheet', 'https://fullcompass.com/common/files/90205-AHM32SpecSheet.pdf', powerW=70, weightKg=4)
A('ahm-16', 'AHM-16', 'AHM-16 16x16 audio matrix processor', 'AHM', 'audio', 1,
  [R('in', AA, 'Phoenix', 8, 'Mic/Line In'), R('out', AA, 'Phoenix', 8, 'Line Out'), R('io', 'Other', 'Card slot', 1, 'I/O Port'),
   R('io', 'Ethernet', 'RJ45', 1, 'Control Network'), R('io', 'GPIO', 'Phoenix', 1, 'GPIO (2 in, 2 relay out)'), IEC()],
  '1U, 482.6 x 270 x 44 mm, 3.8 kg, 65 W max. 8 mic/line inputs and 8 outputs on Phoenix blocks, one I/O Port slot (Dante or SLink), '
  'control network, 2 GPI and 2 relay outputs. Front: screen and 4 SoftKeys.',
  'AHM-16 technical datasheet', 'https://www.allen-heath.com/content/uploads/2023/06/AHM-16-Tech-Datasheet.pdf', powerW=65, weightKg=3.8)
A('dlive-dm0', 'dLive DM0', 'dLive DM0 MixRack (no local I/O)', 'dLive', 'audio', 4,
  [R('io', 'Other', 'Card slot', 3, 'I/O Port'), R('io', 'Other', 'etherCON', 2, 'gigaACE'), R('io', 'Other', 'etherCON', 4, 'DX'),
   R('out', 'Other', 'etherCON', 1, 'ME'), R('io', 'Ethernet', 'RJ45', 2, 'Network'), R('in', 'Other', 'BNC', 1, 'Word Clock In'),
   R('out', 'Other', 'BNC', 1, 'Word Clock Out'), R('out', AA, '1/4" TRS', 1, 'Phones'), IEC(n=2, p='PSU')],
  '4U (176 mm), 482.6 x 355 mm deep, 12 kg. Full XCVI core (128 inputs, 64 buses) with no analogue I/O: audio comes in on 3 I/O Port cards '
  '(128 ch at 96 kHz each), DX expanders and the surface. 2 gigaACE (redundant surface link), DX ports for 2 redundant DX expanders, ME port, '
  '2 gigabit network, word clock, dual-redundant hot-swap PSUs (90 W max each) with their own IEC and switch. Reversible rack ears. '
  'DM0U is the same rack with UltraFX. Check: DX port count (datasheet sections differ) and which face the phones socket is on.',
  'dLive DM0 datasheet', 'https://goknight.com/content/documentation/DLIVE%20DM0%20Spec%20Sheet.pdf', powerW=180, weightKg=12)
A('dx012', 'DX012', 'DX012 12-output DX expander (analogue/AES)', 'DX', 'audio', 1,
  [F('out', AA, 'XLR', 12, 'Out (analogue or AES pairs)'), F('io', 'Other', 'etherCON', 1, 'DX A'), F('io', 'Other', 'etherCON', 1, 'DX B'), IEC()],
  '1U, 482.6 x 215 mm deep, 2.95 kg, 35 W max. 12 XLR outputs set as 12 analogue, 8 analogue + 4 stereo AES3 or 4 analogue + 8 stereo AES3; '
  'DX A and DX B (daisy chain or redundant). For dLive, Avantis, SQ and AHM-64 at 96 kHz. Reversible rack ears. '
  'Check: which face the XLRs and DX ports are on (the datasheet only puts the IEC on the rear).',
  'DX012 datasheet', 'https://www.allen-heath.com/content/uploads/2023/06/DX012-Datasheet.pdf', powerW=35, weightKg=2.95)
A('gx4816', 'GX4816', 'GX4816 48x16 96kHz expander', 'GX', 'audio', 5,
  [F('in', AA, 'XLR', 48, 'Mic In'), F('out', AA, 'XLR', 16, 'Line Out'), F('io', 'Other', 'etherCON', 1, 'GX'),
   F('io', 'Other', 'etherCON', 2, 'DX'), IEC('front')],
  '481.6 x 255 x 229.5 mm, 8 kg, 80 W max. 48 mic/line inputs (+48 V), 16 XLR outputs, GX port to the mixer (dLive, Avantis, SQ, AHM-64 '
  'through a GX card or SLink), 2 DX ports for further expanders (one can feed ME personal mixers on Avantis/SQ). The IEC is on the front panel. '
  'Check: rack height (5U assumed from 229.5 mm with feet).', 'GX4816 datasheet', 'https://media.musson.com/mti/docs/g/x/gx4816-datasheet.pdf',
  powerW=80, weightKg=8)
A('dt168', 'DT168', 'DT168 Dante expander 16x8', 'Dante expanders', 'audio', 4,
  [F('in', AA, 'XLR', 16, 'Mic In'), F('out', AA, 'XLR', 8, 'Line Out'), R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Primary'),
   R('io', 'Dante/AES67', 'etherCON', 1, 'Dante Secondary'), IEC()],
  'Portable 16 x 8 Dante stagebox: 410 x 190 x 185 mm, 4.6 kg, 40 W max. 16 mic inputs (+48 V), 8 relay-protected XLR outputs, Dante primary '
  'and secondary (daisy chain or redundant) on etherCON. 4U with the optional 19-inch rack kit (same body as AB168/DX168). '
  'Check: which face the etherCONs are on.', 'DT168 technical datasheet',
  'https://www.allen-heath.com/content/uploads/2023/06/DT168-Technical-Datasheet.pdf', powerW=40, weightKg=4.6)
A('dx-hub', 'DX Hub', 'DX Hub 4-port DX expander hub (half rack)', 'DX', 'audio', 1,
  [R('io', 'Other', 'etherCON', 1, 'Link (SLink / gigaACE)'), R('io', 'Other', 'etherCON', 4, 'DX'), IEC()],
  'Half-width 1U box, 171 x 203 x 43 mm, 1.2 kg. Connects to an SQ SLink port or a dLive gigaACE card and fans out to 4 DX links '
  '(32x32 at 96 kHz each); 2 hubs on one gigaACE card give 4 redundant DX links. Mounts half-space or two side by side with the 1U kit. '
  'Check: power inlet type and which face the ports are on.', 'DX Hub brochure and weights/dims sheet',
  'https://www.allen-heath.com/content/uploads/2023/06/DX-Hub-Weights-and-Dims.pdf', w=6, boxMm={'w': 171, 'h': 43}, weightKg=1.2)
A('me-u', 'ME-U', 'ME-U 10-port personal mixing hub', 'ME', 'audio', 2,
  [F('out', 'Other', 'etherCON', 10, 'ME (PoE)'), F('in', 'Other', 'etherCON', 1, 'Input card'), F('io', 'Ethernet', 'RJ45', 1, 'Network'), IEC()],
  '2U, 483 x 253 x 92 mm, 4.6 kg, 250 W max. 10 ME outputs with PoE (15 W each) for ME-1 / ME-500 mixers; removable input card '
  '(dLive, SQ, Qu, GLD, iLive or A-Net, or M-DANTE / M-MADI / M-WAVES2); network port for browser setup. Rear power switch. '
  'Check: which face the network port is on.', 'ME-U datasheet', 'https://www.allen-heath.com/content/uploads/2023/06/ME-U-Datasheet-WEB.pdf',
  powerW=250, weightKg=4.6)
A('ar2412', 'AR2412', 'AR2412 AudioRack 24x12 (GLD / SQ / Qu)', 'AudioRack', 'audio', 4,
  [F('in', AA, 'XLR', 24, 'Mic In'), F('out', AA, 'XLR', 12, 'Line Out'), R('io', 'Other', 'etherCON', 1, 'dSNAKE'),
   R('io', 'Other', 'etherCON', 1, 'Expander'), R('out', 'Other', 'etherCON', 1, 'ME'), IEC()],
  '4U stagebox, 24 mic inputs, 12 XLR outputs, dSNAKE to a GLD, SQ (SLink) or Qu mixer, expander port for an AR84 or AB168, ME port for '
  'personal mixers. Check: AES output, port faces and power figures (cut sheet gives only the counts above).',
  'AR2412 cut sheet', 'https://shop.ccisolutions.com/StoreFront/jsp/pdf/AR2412-Cut-Sheet.pdf', verified=False)

# ---------------- Roland ----------------
RO = lambda *a, **k: add('roland-more.json', 'roland-', 'Roland', *a, **k)
RP = 'https://proav.roland.com/global/products/'
RO('s-2416', 'S-2416', 'S-2416 REAC digital snake 24x16', 'REAC', 'audio', 4,
  [F('in', AA, 'XLR', 24, 'Mic In'), F('out', AA, 'XLR', 16, 'Out'), R('io', AO, 'DB25', 1, 'AES/EBU 8 in / 8 out'),
   R('io', 'Other', 'etherCON', 2, 'REAC (main / backup)'), R('in', 'Other', 'BNC', 1, 'Word Clock In'), R('out', 'Other', 'BNC', 1, 'Word Clock Out'),
   R('in', 'RS-232', 'DB9', 1, 'Remote'), R('io', 'USB', 'USB-B', 1, 'Computer (RCS)'), IEC()],
  '4U, 482 x 348 x 177 mm, 9.7 kg, 62 W. 24 mic inputs (+48 V), 16 XLR outputs, 8 x 8 AES/EBU on DB-25 (32 in, 24 out in all), '
  'two REAC ports for redundancy or a cascaded second unit, word clock, RS-232 remote and USB for S-4000 RCS. '
  'Check: word clock in/out count and which face each group is on.', 'Roland S-2416 specifications', RP + 's-2416/', powerW=62, weightKg=9.7)
for pn, i, o, url in [('S-1608', 16, 8, RP + 's-1608/'), ('S-0816', 8, 16, RP + 's-0816/')]:
    RO(pn.lower(), pn, f'{pn} REAC digital snake {i}x{o}', 'REAC', 'audio', 4,
       [F('in', AA, 'XLR', i, 'Mic In'), F('out', AA, 'XLR', o, 'Out'), R('io', 'Other', 'etherCON', 1, 'REAC'),
        R('out', 'Other', 'TOSLINK', 1, 'Digital Out'), R('in', 'RS-232', 'DB9', 1, 'Remote'), IEC()],
       f'401 x 135 x 177 mm (4U with the rack-mount angles), 5.5 kg, 45 W. {i} XLR inputs (+48 V, remote-controlled preamps on the stage unit), '
       f'{o} XLR outputs, one REAC port (split with an S-4000D or a gigabit switch), optical digital out, RS-232 remote. '
       f'{"Stage unit" if i > o else "FOH unit"}; pairs with the {"S-0816" if i > o else "S-1608"} or an M-series console. '
       'Check: power inlet type and which face the REAC port is on.', f'Roland {pn} specifications', url, powerW=45, weightKg=5.5)
RO('s-madi', 'S-MADI', 'S-MADI REAC to MADI bridge', 'REAC', 'audio', 1,
  [F('in', 'RS-232', 'DB9', 1, 'Remote'), R('io', 'Other', 'etherCON', 1, 'REAC Main'), R('out', 'Other', 'etherCON', 1, 'REAC Split Out (powered)'),
   R('in', 'Other', 'BNC', 1, 'Word Clock In'), R('out', 'Other', 'BNC', 1, 'Word Clock Out'), R('in', 'MADI', 'BNC', 1, 'MADI In (coax)'),
   R('out', 'MADI', 'BNC', 1, 'MADI Out (coax)'), R('io', 'MADI', 'SC', 1, 'MADI optical (SC duplex)'), IEC()],
  '1U, 482 x 303 x 44 mm, 3.5 kg. Bridges 40 channels between REAC and MADI (coax and optical), with a powered REAC split output. '
  'Check: power inlet type.', 'Roland S-MADI specifications', 'https://proav.roland.com/products/s-madi/', weightKg=3.5)
RO('s-4000d', 'S-4000D', 'S-4000D REAC splitter and power distributor', 'REAC', 'audio', 2,
  [R('io', 'Other', 'etherCON', 2, 'REAC'), R('out', 'Other', 'etherCON', 8, 'REAC (embedded power)'), IEC()],
  '2U, 482 x 285 x 88 mm, 4.2 kg. Splits REAC to up to 10 ports; 8 carry REAC Embedded Power for M-48 personal mixers (needed with the M-48). '
  'Discontinued. Check: which face the ports are on and the power inlet.', 'Roland S-4000D specifications', RP + 's-4000d', weightKg=4.2)
RO('xs-42h', 'XS-42H', 'XS-42H 4 x 2 HDMI matrix switcher (half rack)', 'XS', 'router', 1,
  [R('in', 'HDMI', 'HDMI', 4, 'HDMI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('in', AA, 'RCA', 2, 'Audio In L/R'),
   R('out', AA, 'RCA', 2, 'Audio Out L/R'), R('in', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Ethernet', 'RJ45', 1, 'LAN'),
   R('io', 'USB', 'USB-A', 1, 'USB (expansion)'), F('in', AA, '3.5mm TRS', 1, 'Line In'), F('out', AA, '3.5mm TRS', 1, 'Phones'),
   F('io', 'USB', 'USB-A', 1, 'USB memory'), R('in', 'Power', 'DC barrel', 1, 'DC In (AC adaptor)')],
  'Half-rack 1U, 242 x 125 x 44 mm, 1.2 kg, 25 W, AC adaptor. 4 x 2 HDMI matrix with scaling and an audio mixer; rack-mount angle set '
  'optional. Same body as the VP-42H. Check: RCA audio counts and which face each group is on.', 'Roland XS-42H specifications',
  'https://resource.holdan.co.uk/Roland/specs/Roland_XS-42H.pdf', w=6, boxMm={'w': 242, 'h': 44}, powerW=25, weightKg=1.2)
RO('v-1200hd', 'V-1200HD', 'V-1200HD multi-format video switcher (processor)', 'V-1200HD', 'switcher', 3,
  [R('in', 'SDI', 'BNC', 10, 'SDI In'), R('out', 'SDI', 'BNC', 6, 'SDI Out'), R('in', 'HDMI', 'HDMI', 4, 'HDMI In'),
   R('out', 'HDMI', 'HDMI', 2, 'HDMI Out'), R('out', 'HDMI', 'HDMI', 2, 'Multi-view Out'), R('in', AA, 'XLR/TRS combo', 2, 'Audio In (analogue / AES)'),
   R('out', AA, 'XLR', 2, 'Audio Out (analogue / AES)'), R('in', 'Reference', 'BNC', 1, 'Reference In'), R('out', 'Reference', 'BNC', 1, 'Reference Thru'),
   R('io', 'Ethernet', 'RJ45', 1, 'LAN (to V-1200HDR)'), R('in', 'RS-232', 'DB9', 1, 'RS-232'), R('out', 'RS-422', 'DB9', 1, 'RS-422 (VISCA)'),
   R('io', 'GPIO', 'DB25', 1, 'Tally/GPIO (8 in, 16 out)'), R('io', 'Other', 'Card slot', 2, 'Expansion'), F('io', 'USB', 'USB-A', 2, 'USB'),
   IEC(), R('in', 'Power', 'XLR4', 1, 'DC 24 V (redundant)')],
  '3U (EIA, rack angles included), 430 x 357 x 132.5 mm, 9 kg, 240 W. 16-input switcher processor: 10 3G-SDI and 4 HDMI in, 6 SDI out, '
  '2 HDMI out and 2 multi-view HDMI out, AES/analogue audio, reference, VISCA camera control, 8/16 tally GPIO, 2 expansion slots. '
  'Pairs with the V-1200HDR control surface (desktop). Discontinued. Check: which face the USB ports are on.',
  'Roland V-1200HD specifications', 'https://resource.holdan.co.uk/Roland/specs/Roland_V-1200HD.pdf', powerW=240, weightKg=9)

# ---------------- Mackie ----------------
M = lambda *a, **k: add('mackie.json', 'mackie-', 'Mackie', *a, **k)
M('dl32r', 'DL32R', 'DL32R 32-channel rack digital mixer', 'DL', 'audio', 3,
  [F('in', AA, 'XLR', 24, 'Mic In'), F('in', AA, 'XLR/TRS combo', 8, 'Mic/Line In'), F('out', AA, 'XLR', 12, 'Out'),
   F('out', AO, 'XLR', 1, 'AES Out'), F('out', AA, '1/4" TRS', 2, 'Monitor Out L/R'), F('out', AA, '1/4" TRS', 1, 'Phones'),
   F('io', 'USB', 'USB-B', 1, 'USB audio (32x32)'), F('io', 'USB', 'USB-A', 1, 'USB drive (record/play)'),
   R('io', 'Other', 'Card slot', 1, 'Network/Dante option card'), IEC()],
  '3U, 483 x 443 x 138 mm, 8.2 kg, 100 W. 32 Onyx+ preamps (24 XLR + 8 combo), 12 XLR outputs, AES out, monitor and phones, '
  'USB-B audio interface and USB-A multitrack recording; option slot for the network card (wired control) or Dante card. iPad control. '
  'Check: which face the option slot is on.', 'Mackie DL32R specifications (Full Compass)',
  'https://www.fullcompass.com/prod/269613-mackie-dl32r-32-channel-rackmount-digital-mixer-with-ios-connectivity', powerW=100, weightKg=8.2)
for pn, ru, xl, combo, outs, wmm, kg, watts, url in [
        ('DL32S', 4, 16, 16, 10, 414, 4.0, 60, 'https://fullcompass.com/prod/550991-mackie-dl32s-32-channel-wireless-digital-live-sound-mixer'),
        ('DL32SE', 4, 16, 16, 10, 414, 4.0, 60, 'https://mackie.com/img/file_resources/DL16SE_DL32SE_SS[99].pdf'),
        ('DL16S', 3, 8, 8, 8, 358, 2.8, 40, 'https://www.fullcompass.com/prod/550990-mackie-dl16s-16-channel-wireless-digital-live-sound-mixer'),
        ('DL16SE', 3, 8, 8, 8, 358, 2.8, 40, 'https://mackie.com/img/file_resources/DL16SE_DL32SE_SS[99].pdf')]:
    n = xl + combo
    se = pn.endswith('SE')
    M(pn.lower(), pn, f'{pn} {n}-channel {"digital rack mixer (SE)" if se else "wireless digital mixer"}', 'DL', 'audio', ru,
      [F('in', AA, 'XLR', xl, 'Mic In'), F('in', AA, 'XLR/TRS combo', combo, 'Mic/Line In'), F('out', AA, 'XLR', outs, 'Out'),
       F('out', AA, '1/4" TRS', 1, 'Phones'), F('io', 'USB', 'USB-B', 1, f'USB audio ({n}x{n})'), F('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
       F('io', 'RF', 'SMA', 1, 'Wi-Fi antenna'), IEC()],
      f'{ru}U, {wmm} mm wide x 147 mm deep, {kg} kg, {watts} W. {n} Onyx preamps ({xl} XLR + {combo} combo, last two Hi-Z), {outs} XLR outputs, '
      f'phones, USB-B audio interface, 100 Mb Ethernet and built-in Wi-Fi (external SMA antenna). '
      + ('SE version: same I/O, ships with the Master Fader SE control software. ' if se else '')
      + f'Check: rack ears (the body is {wmm} mm wide) and which face the Ethernet and IEC are on.',
      f'Mackie {pn} specifications', url, powerW=watts, weightKg=kg)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
