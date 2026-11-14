#!/usr/bin/env python3
"""Generates catalogue/bmd-desktop.json: Blackmagic Design's small and desktop units that the built-in list (tools/bmd.py) leaves out,
and the shelves that rack them. Added 2026-11-14.

- UltraStudio 4K Mini, UltraStudio Express Recorder/Monitor 3G, UltraStudio Mini Recorder/Monitor/Replay 12G
- Teranex Mini 12G range and Teranex Mini 8K HDR, MultiView 4 and MultiView 4 HD
- Mini Converters, Micro Converters, ATEM Streaming Bridge, ATEM Microphone Converter
- ATEM Mini Pro / Pro ISO / Extreme / Extreme ISO G2, ATEM SDI / SDI Pro ISO / SDI Extreme ISO
- Blackmagic Universal Rack Shelf and Teranex Mini Rack Shelf

Ports come from each family's blackmagicdesign.com tech specs page and its connection drawings; sizes and weights from the
'physical specifications' drawings on the same pages (inches, converted to mm). One-third and half rack width units sit straight in
the rack grid (ru 1, widthCols 4 or 6) and also fit a shelf bay by formFactor. Desktop boxes have boxMm (front face, w x h) and are drawn
at real size on a shelf; for boxes with connectors at both ends, the end with the SDI and power is 'rear' and the other end 'front'."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
M = []
BMD = 'https://www.blackmagicdesign.com/products/'
THIRD, HALF = 'Blackmagic 1/3 rack width', 'Blackmagic 1/2 rack width'
IN = 25.4
def mm(x): return round(x * IN)
def add(id, pn, name, fam, cat, ru, w, ports, notes, fampage, code, verified=True, **kw):
    m = dict(id='bmds-' + id, manufacturer='Blackmagic Design', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w,
             fullDepth=False, verified=verified, source=f'Blackmagic Design tech specs ({code})' if code else 'Blackmagic Design product page',
             productUrl=BMD + fampage + ('/techspecs/' + code if code else ''), notes=notes, portGroups=ports)
    if code: m['specId'] = code
    m.update(kw); M.append(m)
def box(w_in, h_in, d_in, kg=None):
    """boxMm for a desktop box from the drawing's inches (w = connector face width), plus a size note."""
    k = dict(boxMm={'w': mm(w_in), 'h': mm(h_in)})
    if kg: k['weightKg'] = kg
    return k
def sz(w_in, h_in, d_in, kg): return f'{mm(w_in)} x {mm(h_in)} x {mm(d_in)} mm (W x H x D), {kg} kg.'
def cols(w_in): return max(1, -(-mm(w_in) // 40))  # twelfths of 482.6 mm (40.2 mm each)
LB, OZ = 0.4536, 0.02835

SDI = lambda d, n, p, t='12G-SDI', face='rear': g(face, d, t, 'BNC', n, p)
HDMI = lambda d, p, face='rear': g(face, d, 'HDMI', 'HDMI', 1, p)
IEC = R('in', 'Power', 'IEC C14', 1, 'AC In')
ETH = lambda p='Ethernet', face='rear': g(face, 'io', 'Ethernet', 'RJ45', 1, p)
USBC = lambda p='USB-C', face='rear': g(face, 'io', 'USB', 'USB-C', 1, p)
TB = lambda gen, face='rear': g(face, 'io', 'USB', 'USB-C', 1, f'Thunderbolt {gen}')
DC12 = lambda p='12V DC In', face='rear': g(face, 'in', 'Power', 'DC locking', 1, p)
JACK = lambda d, n, p, face='front': g(face, d, 'Analog audio', '1/4" TRS', n, p)

# ======================= UltraStudio =======================
add('ultrastudio-4k-mini', 'UltraStudio 4K Mini', 'UltraStudio 4K Mini', 'UltraStudio', 'converter', 1, 6,
    [F('in', 'Analog audio', 'XLR3F', 1, 'Mic In (48V)'), F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones'),
     IEC, TB(3), USBC('USB-C (USB 3.1)'), R('io', 'RS-422', 'DB9', 1, 'Remote'),
     SDI('out', 2, 'SDI Out'), SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Loop'), HDMI('out', 'HDMI Out'), HDMI('in', 'HDMI In'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('in', 'Analog video', 'BNC', 3, 'Analog Video In'),
     JACK('out', 2, 'Analog Audio Out', 'rear'), JACK('in', 2, 'Analog Audio In', 'rear')],
    'Half rack width Thunderbolt 3 capture and playback, 4K up to 2160p60. Back: 12G-SDI in, loop and 2 program outs (A, B), HDMI 2.0b in '
    'and out, component YUV or composite in (3 BNC, Y doubles as composite), reference in, RS-422 deck control (DB9), 2 balanced 1/4 inch '
    'jack analog ins and outs, Thunderbolt 3 (charges the host at 45 W), USB-C 3.1 and an IEC C14 inlet. Front: XLR mic in with 48V phantom, '
    'headphone jack, SD card reader (UHS-II), LCD and buttons. 75.3 W max. ' + sz(8.27, 1.8, 7, 1.2) +
    ' Fits the Blackmagic Universal Rack Shelf, two per 1RU. Check: headphone jack size.',
    'ultrastudio', 'W-DLUS-11', powerW=75, weightKg=1.2, formFactor=HALF)
for id_, name, code, d, kg in [('ultrastudio-express-recorder-3g', 'UltraStudio Express Recorder 3G', 'W-DLUS-17', 'in', 5.57 * OZ),
                               ('ultrastudio-express-monitor-3g', 'UltraStudio Express Monitor 3G', 'W-DLUS-18', 'out', 5.64 * OZ)]:
    word = 'In' if d == 'in' else 'Out'
    add(id_, name, name, 'UltraStudio', 'converter', 1, cols(1.77),
        [SDI(d, 1, f'SDI {word}', '3G-SDI'), HDMI(d, f'HDMI {word}'), USBC('USB-C (USB 40Gb/s, power)', 'front')],
        f'Bus-powered USB {"capture" if d == "in" else "playback"} box, SD and HD up to 1080p60. One end: 3G-SDI {word.lower()} and HDMI '
        f'{word.lower()}; other end: USB-C, which needs a USB 40Gb/s (USB4 or Thunderbolt) port on the computer and powers the unit. '
        + sz(1.77, 0.98, 3.62, round(kg, 2)) + ' Sits on a rack shelf.',
        'ultrastudio', code, weightKg=round(kg, 2), **box(1.77, 0.98, 3.62))
TBMINI = ' Bus-powered from a Thunderbolt 4 USB-C port (Apple silicon Mac, Windows or Linux), 15 W. '
for id_, name, code, w_in, kg, ports, desc in [
        ('ultrastudio-mini-recorder-12g', 'UltraStudio Mini Recorder 12G', 'W-DLUS-14', 2.6, 8.11 * OZ,
         [SDI('in', 1, '12G-SDI In'), SDI('out', 1, 'Loop Out'), HDMI('in', 'HDMI In')],
         'Thunderbolt 4 capture up to 2160p60. One end: 12G-SDI in, SDI loop out and HDMI 2.0 in; other end: Thunderbolt 4.'),
        ('ultrastudio-mini-monitor-12g', 'UltraStudio Mini Monitor 12G', 'W-DLUS-15', 2.6, 8.11 * OZ,
         [HDMI('out', 'HDMI Out'), SDI('out', 1, '12G-SDI Fill'), SDI('out', 1, '12G-SDI Key')],
         'Thunderbolt 4 playback up to 2160p60. One end: HDMI 2.0 out and two 12G-SDI outs (fill and key); other end: Thunderbolt 4.'),
        ('ultrastudio-mini-replay-12g', 'UltraStudio Mini Replay 12G', 'W-DLUS-16', 3.19, 10.6 * OZ,
         [SDI('out', 1, '12G-SDI Fill'), SDI('out', 1, '12G-SDI Key'), SDI('out', 1, 'Monitor Out'), SDI('in', 1, '12G-SDI In')],
         'Thunderbolt 4 replay interface (DaVinci Resolve Replay). One end: 12G-SDI in, fill, key and monitor outs; other end: Thunderbolt 4.')]:
    add(id_, name, name, 'UltraStudio', 'converter', 1, cols(w_in), ports + [TB(4, 'front')],
        desc + TBMINI + sz(w_in, 1, 5.83, round(kg, 2)) + ' Sits on a rack shelf.',
        'ultrastudiomini', code, powerW=15, weightKg=round(kg, 2), **box(w_in, 1, 5.83))

# ======================= Teranex Mini (one-third rack width, 1RU) =======================
TM_FRONT = [F('io', 'USB', 'USB', 1, 'USB (under cover)')]
TM_BACK = [IEC, ETH('Ethernet (PoE+)')]
TMN = (' One-third rack width, 1RU: three per rack unit on the Blackmagic Universal Rack Shelf or Teranex Mini Rack Shelf. '
       'Power: IEC C14 (100-240V AC) or 48V PoE+ on the Ethernet port, 16 W. Front: USB and mini switches under a cover '
       '(an optional Teranex Mini Smart Panel adds an LCD and buttons). ')
XO = lambda: R('out', 'Analog audio', 'XLR3M', 2, 'Audio Out L/R (analog or AES/EBU, R = T/C)')
XI = lambda: R('in', 'Analog audio', 'XLR3F', 2, 'Audio In L/R (analog or AES/EBU, R = T/C)')
for slug, name, code, lb, ports, desc in [
        ('sdi-to-hdmi-12g', 'Teranex Mini SDI to HDMI 12G', 'W-TERAMIN-01', 1.28,
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Loop Out'), HDMI('out', 'HDMI Out'), XO()],
         '12G-SDI to HDMI 2.0 up to 2160p60 with 3D LUTs; 2 XLR outs for analog or 4 ch AES/EBU audio (right XLR can carry timecode).'),
        ('hdmi-to-sdi-12g', 'Teranex Mini HDMI to SDI 12G', 'W-TERAMIN-02', 1.28,
         [HDMI('in', 'HDMI In'), SDI('out', 2, 'SDI Out'), XI()],
         'HDMI 2.0 to two 12G-SDI outs; 2 XLR ins for analog or AES/EBU audio to embed.'),
        ('sdi-to-analog-12g', 'Teranex Mini SDI to Analog 12G', 'W-TERAMIN-03', 1.46,
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Loop Out'), R('out', 'Analog video', 'BNC', 3, 'Analog Out (Y/B-Y/R-Y, S-Video, composite)'), XO()],
         '12G-SDI to component, S-Video or composite (3 BNC), with 2 XLR audio outs.'),
        ('analog-to-sdi-12g', 'Teranex Mini Analog to SDI 12G', 'W-TERAMIN-04', 1.41,
         [R('in', 'Analog video', 'BNC', 3, 'Analog In (Y/B-Y/R-Y, S-Video, composite)'), SDI('out', 2, 'SDI Out'), XI()],
         'Component, S-Video or composite (3 BNC) to two 12G-SDI outs, with 2 XLR audio ins.'),
        ('sdi-to-audio-12g', 'Teranex Mini SDI to Audio 12G', 'W-TERAMIN-05', 1.33,
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Loop Out'), R('out', 'AES/EBU', 'TOSLINK', 1, 'Optical Audio Out'),
          R('out', 'Analog audio', 'RCA', 2, 'Stereo Out'), XO()],
         'De-embeds SDI audio to 2 XLR (analog or 4 ch AES/EBU), unbalanced RCA stereo and optical S/PDIF.'),
        ('audio-to-sdi-12g', 'Teranex Mini Audio to SDI 12G', 'W-TERAMIN-06', 1.32,
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Out'), R('in', 'AES/EBU', 'TOSLINK', 1, 'Optical Audio In'),
          R('in', 'Analog audio', 'RCA', 2, 'Stereo In'), XI()],
         'Embeds audio from 2 XLR (analog or AES/EBU), RCA stereo or optical S/PDIF into 12G-SDI.'),
        ('optical-to-hdmi-12g', 'Teranex Mini Optical to HDMI 12G', 'W-TERAMIN-07', 1.28,
         [SDI('in', 1, 'SDI In'), R('io', 'Fibre', 'LC (SFP)', 1, 'Optical Out/In (SFP)'), HDMI('out', 'HDMI Out'), XO()],
         'SMPTE optical fibre or 12G-SDI to HDMI 2.0; the optical SFP (single-mode 1310 nm, LC) is sold separately. 2 XLR audio outs.'),
        ('hdmi-to-optical-12g', 'Teranex Mini HDMI to Optical 12G', 'W-TERAMIN-08', 1.28,
         [HDMI('in', 'HDMI In'), SDI('out', 1, 'SDI Out'), R('io', 'Fibre', 'LC (SFP)', 1, 'Optical Out/In (SFP)'), XI()],
         'HDMI 2.0 to 12G-SDI and SMPTE optical fibre (SFP sold separately). 2 XLR audio ins.'),
        ('sdi-distribution-12g', 'Teranex Mini SDI Distribution 12G', 'W-TERAMIN-29', 1.28,
         [SDI('in', 1, 'SDI In'), SDI('out', 8, 'SDI Out')],
         '1 x 12G-SDI in to 8 reclocked 12G-SDI outs.'),
        ('12g-sdi-to-quad-sdi', 'Teranex Mini 12G-SDI to Quad SDI', 'W-TERAMIN-27', 1.28,
         [SDI('in', 1, '12G-SDI In'), SDI('out', 1, 'SDI Loop Out'), SDI('out', 4, 'Quad/Dual Link Out', '3G-SDI')],
         '12G-SDI to quad link (A-D) or dual link SDI for older 4K gear.'),
        ('quad-sdi-to-12g-sdi', 'Teranex Mini Quad SDI to 12G-SDI', 'W-TERAMIN-28', 1.28,
         [SDI('in', 4, 'Quad/Dual Link In'), SDI('out', 2, 'SDI Out')],
         'Quad link (A-D) or dual link SDI in to two 12G-SDI outs.'),
        ('ip-video-12g', 'Teranex Mini IP Video 12G', 'W-TERAMIN-30', 1.28,
         [SDI('in', 1, 'SDI In'), SDI('out', 2, 'SDI Out'), R('io', 'SFP', 'SFP+', 1, '10G Ethernet (SFP)')],
         'SMPTE 2022-6 / TICO IP video: 1080p60 on the built-in gigabit Ethernet (PoE+) or 2160p60 on the optional 10G SFP.')]:
    add('teranex-mini-' + slug, name, name, 'Teranex Mini', 'converter', 1, 4, TM_FRONT + TM_BACK + ports,
        desc + TMN + sz(5.51, 1.75, 6.69, round(lb * LB, 2)), 'teranexmini', code, powerW=16, weightKg=round(lb * LB, 2), formFactor=THIRD)

T8N = (' Half rack width, 1RU: two per rack unit on the Blackmagic Universal Rack Shelf. Front: LCD, buttons, knob and USB-C; back: IEC C14 '
       '(100-240V AC) and Ethernet for setup. ' + sz(8.27, 1.73, 6.93, 1.2))
for slug, name, code, watts, ports, desc in [
        ('sdi-to-hdmi-8k-hdr', 'Teranex Mini SDI to HDMI 8K HDR', 'W-TERAMIN-31', 25,
         [SDI('in', 4, '12G-SDI In'), SDI('out', 4, 'SDI Loop Out'), g('rear', 'out', 'HDMI', 'HDMI', 4, 'HDMI Out')],
         '8K monitoring converter: 4 x 12G-SDI in (single, dual or quad link up to 4320p60) with loops, 4 x HDMI 2.0 out (single link HD/4K or quad '
         'link 8K), HDR and 33-point 3D LUTs, RCA stereo out.'),
        ('sdi-to-displayport-8k-hdr', 'Teranex Mini SDI to DisplayPort 8K HDR', 'W-TERAMIN-32', 35,
         [SDI('in', 4, '12G-SDI In'), SDI('out', 4, 'SDI Loop Out'), g('rear', 'out', 'DisplayPort', 'DisplayPort', 2, 'DP Out'),
          R('out', 'DisplayPort', 'USB-C', 1, 'USB-C DisplayPort Out')],
         '8K monitoring converter: 4 x 12G-SDI in with loops to 2 x DisplayPort (one for 4K, both for 8K) and a USB-C DisplayPort out '
         '(passive cables only), HDR and 3D LUTs, RCA stereo out.')]:
    add('teranex-mini-' + slug, name, name, 'Teranex Mini', 'converter', 1, 6,
        [F('io', 'USB', 'USB-C', 1, 'USB-C'), IEC, ETH()] + ports + [R('out', 'Analog audio', 'RCA', 2, 'Stereo Out')],
        desc + f' {watts} W.' + T8N, 'teranexmini8k', code, powerW=watts, weightKg=1.2, formFactor=HALF)

# ======================= MultiView =======================
add('multiview-4', 'Blackmagic MultiView 4', 'Blackmagic MultiView 4', 'MultiView', 'monitor', 1, 4,
    TM_FRONT + TM_BACK + [SDI('in', 4, 'SDI In', '6G-SDI'), SDI('out', 4, 'SDI Loop Out', '6G-SDI'), SDI('out', 1, 'Multiview Out (HD/UHD)', '6G-SDI'),
                          HDMI('out', 'HDMI Out')],
    '4-view multiviewer: 4 x 6G-SDI in with loops, HD or Ultra HD multiview on 6G-SDI and HDMI, labels, tally and audio meters. ' + TMN
    + sz(5.51, 1.75, 6.69, 0.58), 'multiview', 'W-MVW-02', powerW=16, weightKg=0.58, formFactor=THIRD)
add('multiview-4-hd', 'Blackmagic MultiView 4 HD', 'Blackmagic MultiView 4 HD', 'MultiView', 'monitor', 1, cols(3.62),
    [F('in', '3G-SDI', 'BNC', 4, 'SDI In'), SDI('out', 1, 'SDI Out', '3G-SDI'), HDMI('out', 'HDMI Out'), DC12('6-30V DC In')],
    'Mini Converter sized 4-view HD multiviewer: 4 x SD/HD-SDI in on one end; HD-SDI multiview out, HDMI out and DC power on the other. '
    '12V supply included, 5.5 W. ' + sz(3.62, 0.86, 5.27, round(8.53 * OZ, 2)) + ' Sits on a rack shelf.',
    'multiview', 'W-MVW-03', powerW=5.5, weightKg=round(8.53 * OZ, 2), **box(3.62, 0.86, 5.27))

# ======================= Mini Converters (92 x 23 x 114 mm boxes) =======================
MC = ('Mini Converter box: connectors on both ends (SDI and DC power on one, the rest on the other), USB for setup and mini switches. '
      'Universal 12V supply included. Sits on a rack shelf. ')
MCSZ = lambda w_d=4.49: sz(3.63, 0.9, w_d, 0.25)
ALT = lambda: [SDI('in', 1, 'SDI In', '6G-SDI'), SDI('in', 1, 'ALT SDI In', '6G-SDI')]
AUD8 = lambda d: [g('front', d, 'Analog audio', '1/4" TRS', 4, f'CH 1-4 Analog / AES {"Out" if d == "out" else "In"}')]
for slug, name, code, watts, ports, desc, lo in [
        ('sdi-to-hdmi-6g', 'Mini Converter SDI to HDMI 6G', 'W-CONM-26', 5.2,
         ALT() + [SDI('out', 1, 'SDI Out', '6G-SDI'), HDMI('out', 'HDMI Out', 'front'), JACK('out', 2, 'L/R Analog or AES/EBU Out')],
         'SD/HD/6G-SDI (with failover ALT input) to HDMI with 3D LUT; 2 balanced 1/4 inch jacks for analog or AES/EBU audio out.', 12),
        ('hdmi-to-sdi-6g', 'Mini Converter HDMI to SDI 6G', 'W-CONM-27', 4.44,
         [SDI('out', 2, 'SDI Out', '6G-SDI'), HDMI('in', 'HDMI In', 'front'), JACK('in', 2, 'L/R Analog or AES/EBU In')],
         'HDMI to two 6G-SDI outs; 2 balanced 1/4 inch jacks for analog or AES/EBU audio in.', 12),
        ('sdi-to-audio-4k', 'Mini Converter SDI to Audio 4K', 'W-CONM-06', 5.52,
         ALT() + [SDI('out', 1, 'SDI Out', '6G-SDI')] + AUD8('out'),
         'De-embeds 4 ch analog or 8 ch AES/EBU from SD/HD/6G-SDI to 4 balanced 1/4 inch jacks.', 31),
        ('audio-to-sdi-4k', 'Mini Converter Audio to SDI 4K', 'W-CONM-05', 8.4,
         ALT() + [SDI('out', 1, 'SDI Out', '6G-SDI')] + AUD8('in'),
         'Embeds 4 ch analog or 8 ch AES/EBU from 4 balanced 1/4 inch jacks into SD/HD/6G-SDI.', 31),
        ('sdi-to-analog-4k', 'Mini Converter SDI to Analog 4K', 'W-CONM-19', 8.04,
         ALT() + [SDI('out', 1, 'SDI Out', '6G-SDI'), g('front', 'out', 'Analog video', 'BNC', 3, 'Analog Out (Y/B-Y/R-Y, S-Video, composite)'),
                  JACK('out', 2, 'L/R Analog or AES/EBU Out')],
         'SD/HD/6G-SDI to component, S-Video or composite (3 BNC, down-converted from Ultra HD), with 2 audio jacks.', 31),
        ('sdi-distribution-4k', 'Mini Converter SDI Distribution 4K', 'W-CONM-21', 4.8,
         [SDI('in', 1, 'SDI In', '6G-SDI'), SDI('out', 3, 'SDI Out', '6G-SDI'), g('front', 'out', '6G-SDI', 'BNC', 5, 'SDI Out')],
         '1 x SD/HD/6G-SDI in to 8 reclocked outs (3 beside the input, 5 on the other end). Passes ASI.', 31),
        ('sdi-to-audio', 'Mini Converter SDI to Audio', 'W-CONM-22', 5.52,
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('in', 1, 'ALT SDI In', '3G-SDI'), SDI('out', 1, 'SDI Out', '3G-SDI')] + AUD8('out'),
         'De-embeds 4 ch analog or 8 ch AES/EBU from SD/HD/3G-SDI to 4 balanced 1/4 inch jacks.', 15),
        ('audio-to-sdi', 'Mini Converter Audio to SDI', 'W-CONM-04', 8.4,
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('in', 1, 'ALT SDI In', '3G-SDI'), SDI('out', 1, 'SDI Out', '3G-SDI')] + AUD8('in'),
         'Embeds 4 ch analog or 8 ch AES/EBU from 4 balanced 1/4 inch jacks into SD/HD/3G-SDI.', 12),
        ('sdi-to-analog', 'Mini Converter SDI to Analog', 'W-CONM-01', 8.04,
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('in', 1, 'ALT SDI In', '3G-SDI'), SDI('out', 1, 'SDI Out', '3G-SDI'),
          g('front', 'out', 'Analog video', 'BNC', 3, 'Analog Out (Y/B-Y/R-Y, S-Video, composite)'), JACK('out', 2, 'L/R Analog or AES/EBU Out')],
         'SD/HD-SDI to component, S-Video or composite (3 BNC), with 2 audio jacks.', 15),
        ('analog-to-sdi', 'Mini Converter Analog to SDI', 'W-CONM-00', 6.5,
         [SDI('out', 2, 'SDI Out', '3G-SDI'), g('front', 'in', 'Analog video', 'BNC', 3, 'Analog In (Y/B-Y/R-Y, S-Video, composite)'),
          JACK('in', 2, 'L/R Analog or AES/EBU In')],
         'Component, S-Video or composite (3 BNC) to two SD/HD-SDI outs, with 2 audio jacks.', 31),
        ('optical-fiber-12g', 'Mini Converter Optical Fiber 12G', 'W-CONM-29', 2,
         [SDI('out', 1, '12G-SDI Out'), SDI('in', 1, '12G-SDI In'), g('front', 'io', 'Fibre', 'LC (SFP)', 1, 'Optical Out/In (SFP)')],
         'Bi-directional 12G-SDI to SMPTE optical fibre and back; the SFP module is sold separately. No user controls; passes ASI.', 36),
        ('sync-generator', 'Mini Converter Sync Generator', 'W-CONM-15', 3,
         [R('out', 'Reference', 'BNC', 3, 'Ref Out'), g('front', 'out', 'Reference', 'BNC', 3, 'Ref Out')],
         '6 black burst or tri-level reference outputs (3 on each end), SD and HD formats set by switches.', 12),
        ('sdi-distribution', 'Mini Converter SDI Distribution', 'W-CONM-13', 4.8,
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('out', 3, 'SDI Out', '3G-SDI'), g('front', 'out', '3G-SDI', 'BNC', 5, 'SDI Out')],
         '1 x SD/HD/3G-SDI in to 8 reclocked outs (3 beside the input, 5 on the other end). Passes ASI.', 31),
        ('updowncross-hd', 'Mini Converter UpDownCross HD', 'W-CONM-28', 5,
         [SDI('out', 2, 'SDI Out', '3G-SDI'), HDMI('out', 'HDMI Out'), SDI('in', 1, 'SDI In', '3G-SDI', 'front'), SDI('out', 1, 'SDI Loop', '3G-SDI', 'front'),
          HDMI('in', 'HDMI In', 'front'), g('front', 'in', 'Reference', 'BNC', 1, 'Ref In')],
         'Up, down and cross conversion between SD and HD (SDI or HDMI in, SDI and HDMI out) with reference input and audio delay.', 36)]:
    volts = {12: '12V DC', 15: '12-15V DC', 31: '12-31V DC', 36: '6-36V DC'}[lo]
    add('mini-converter-' + slug, name, name, 'Mini Converter', 'converter', 1, cols(3.63), ports + [DC12(volts + ' In')],
        desc + f' {watts} W, {volts}. ' + MC + MCSZ(), 'miniconverters', code, powerW=watts, weightKg=0.25, **box(3.63, 0.9, 4.49))

# ======================= Micro Converters (USB-C powered) =======================
for slug, name, code, psu_code, gen, ports, desc, d_in, watts in [
        ('sdi-to-hdmi-12g', 'Micro Converter SDI to HDMI 12G', 'W-CONU-18', 'W-CONU-21', '12G',
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Loop Out'), HDMI('out', 'HDMI Out', 'front')], 'SD/HD/6G/12G-SDI to HDMI 2.0 with 33-point 3D LUT.', 3.07, 4),
        ('hdmi-to-sdi-12g', 'Micro Converter HDMI to SDI 12G', 'W-CONU-17', 'W-CONU-20', '12G',
         [SDI('out', 2, 'SDI Out'), HDMI('in', 'HDMI In', 'front')], 'HDMI 2.0 to two 12G-SDI outs.', 3.07, 4),
        ('bidirectional-sdi-hdmi-12g', 'Micro Converter BiDirectional SDI/HDMI 12G', 'W-CONU-16', 'W-CONU-19', '12G',
         [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Out'), HDMI('in', 'HDMI In', 'front'), HDMI('out', 'HDMI Out', 'front')],
         'SDI to HDMI and HDMI to SDI at the same time, up to 2160p60, with camera control and tally.', 3.13, 5),
        ('sdi-to-hdmi-3g', 'Micro Converter SDI to HDMI 3G', 'W-CONU-12', 'W-CONU-14', '3G',
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('out', 1, 'SDI Loop Out', '3G-SDI'), HDMI('out', 'HDMI Out', 'front')], 'SD/HD-SDI to HDMI with 17-point LUT.', 3.13, 1.6),
        ('hdmi-to-sdi-3g', 'Micro Converter HDMI to SDI 3G', 'W-CONU-11', 'W-CONU-13', '3G',
         [SDI('out', 2, 'SDI Out', '3G-SDI'), HDMI('in', 'HDMI In', 'front')], 'HDMI to two SD/HD-SDI outs.', 3.13, 2),
        ('bidirectional-sdi-hdmi-3g', 'Micro Converter BiDirectional SDI/HDMI 3G', 'W-CONU-09', 'W-CONU-10', '3G',
         [SDI('in', 1, 'SDI In', '3G-SDI'), SDI('out', 1, 'SDI Out', '3G-SDI'), HDMI('in', 'HDMI In', 'front'), HDMI('out', 'HDMI Out', 'front')],
         'SD/HD SDI to HDMI and HDMI to SDI at the same time, with camera control and tally.', 3.13, 2.5)]:
    bidi = 'bidirectional' in slug
    dd = 2.32 if bidi else 1.8
    add('micro-converter-' + slug, name, name + ' (with or without PSU)', 'Micro Converter', 'converter', 1, cols(dd),
        ports + [USBC('USB-C (5V power, setup)', 'front')],
        desc + f' SDI on one end, HDMI and USB-C on the other. Powered by USB-C (5V, {watts} W); the "wPSU" version ({psu_code}) adds a '
        f'5V supply. Tiny metal box, sits on a rack shelf. ' + sz(dd, 0.98, d_in, 0.15 if not bidi else 0.17)
        + (' Check: 3G BiDirectional size taken from the 12G one.' if slug.endswith('3g') and bidi else ''),
        'microconverters', code, powerW=watts, weightKg=0.15 if not bidi else 0.17, **box(dd, 0.98, d_in))

# ======================= ATEM converters and streaming bridge =======================
add('atem-streaming-bridge', 'ATEM Streaming Bridge', 'ATEM Streaming Bridge', 'ATEM', 'converter', 1, cols(3.63),
    [g('front', 'io', 'Ethernet', 'RJ45', 1, 'Ethernet (stream in)'), g('front', 'in', 'Reference', 'BNC', 1, 'Ref In'),
     SDI('out', 2, 'SDI Out', '3G-SDI'), HDMI('out', 'HDMI Out'), USBC('USB-C (setup)'), DC12('12V DC In (6-30V)')],
    'Receives an H.264 stream from an ATEM Mini or ATEM SDI over a network or the internet and outputs it as SDI and HDMI (up to 1080p60). '
    'Ethernet and reference in on one end; 2 x 3G-SDI out, HDMI out, USB-C and DC power on the other. 12V supply included, 6 W. '
    + sz(3.63, 0.9, 5.28, 0.23) + ' Sits on a rack shelf.',
    'atem', 'W-APS-16', powerW=6, weightKg=0.23, **box(3.63, 0.9, 5.28))
add('atem-microphone-converter', 'ATEM Microphone Converter', 'ATEM Microphone Converter', 'ATEM', 'audio', 1, cols(4.92),
    [g('front', 'in', 'Analog audio', 'XLR/TRS combo', 4, 'Mic/Line In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Monitor Out'),
     R('out', 'MADI audio', 'BNC', 1, 'MADI Out'), R('in', 'MADI audio', 'BNC', 1, 'MADI In'), USBC('USB-C (locking)'), ETH(), DC12('12V DC In')],
    '4 mic/line combo XLR/TRS inputs with 48V phantom to 64-channel MADI, for ATEM switchers with MADI in. MADI in and out, HDMI monitor out '
    '(meters), USB-C and Ethernet. 12V supply with locking connector, 12 W. ' + sz(4.92, 1.6, 7.87, 0.85) + ' Sits on a rack shelf.',
    'atemtelevisionstudio', 'W-ATC-05', powerW=12, weightKg=0.85, **box(4.92, 1.6, 7.87))

# ======================= ATEM Mini and ATEM SDI (desktop switchers) =======================
SW = (' Desktop switcher: buttons on top, every connector on the back edge. Lying flat on a rack shelf it needs {ru}RU; '
      'the 12V supply has a locking DC plug.')
MIC2 = lambda: R('in', 'Analog audio', '3.5mm jack', 2, 'Mic In')
for slug, name, code, w_in, h_in, d_in, kg, watts, ports, desc, fam, page in [
        ('atem-mini-pro', 'ATEM Mini Pro', 'W-APS-14', 9.35, 1.38, 4.07, 19.4 * OZ, 30,
         [ETH('ATEM Control / Ethernet'), USBC('USB-C Out (webcam, disk)'), HDMI('out', 'HDMI Out'), g('rear', 'in', 'HDMI', 'HDMI', 4, 'HDMI In'), MIC2()],
         '4 x HDMI in, HDMI program out, live streaming over Ethernet, USB-C recording to disk and webcam out.', 'ATEM Mini', 'atemmini'),
        ('atem-mini-pro-iso', 'ATEM Mini Pro ISO', 'W-APS-15', 9.35, 1.38, 4.07, 19.4 * OZ, 36,
         [ETH('ATEM Control / Ethernet'), USBC('USB-C Out (webcam, disk)'), HDMI('out', 'HDMI Out'), g('rear', 'in', 'HDMI', 'HDMI', 4, 'HDMI In'), MIC2()],
         '4 x HDMI in, HDMI program out, streaming, and ISO recording of every input to a USB disk.', 'ATEM Mini', 'atemmini'),
        ('atem-mini-extreme', 'ATEM Mini Extreme', 'W-APS-17', 14.56, 1.56, 5.37, 2.72 * LB, 36,
         [ETH('ATEM Control / Ethernet'), g('rear', 'io', 'USB', 'USB-C', 2, 'USB-C'), g('rear', 'out', 'HDMI', 'HDMI', 2, 'HDMI Out'),
          g('rear', 'in', 'HDMI', 'HDMI', 8, 'HDMI In'), MIC2(), R('out', 'Analog audio', '3.5mm jack', 1, 'Headphones')],
         '8 x HDMI in, 2 x HDMI out (program, aux), streaming over Ethernet, 2 x USB-C for disks and webcam out.', 'ATEM Mini', 'atemmini'),
        ('atem-mini-extreme-iso-g2', 'ATEM Mini Extreme ISO G2', 'W-APS-44', 16.3, 1.97, 7.35, 4.09 * LB, 120,
         [ETH('1G Ethernet'), g('rear', 'io', 'Ethernet', 'RJ45', 1, '10G Ethernet'), g('rear', 'io', 'USB', 'USB-C', 2, 'USB-C'), TB('(USB-C)'),
          g('rear', 'out', 'HDMI', 'HDMI', 3, 'HDMI Out'), g('rear', 'in', 'HDMI', 'HDMI', 8, 'HDMI In'), R('in', 'MADI audio', 'BNC', 1, 'MADI In'),
          R('in', 'Analog audio', 'XLR/TRS combo', 2, 'Line/Mic In'), R('out', 'Analog audio', '1/4" TRS', 1, 'Headphones')],
         '8 x HDMI in, 3 x HDMI out, ISO recording, 1G and 10G Ethernet, 2 x USB-C and Thunderbolt, MADI in (32 ch) and 2 combo XLR mic/line '
         'ins with phantom power.', 'ATEM Mini', 'atemmini'),
        ('atem-sdi', 'ATEM SDI', 'W-APS-30', 9.35, 1.38, 4.67, 23.9 * OZ, 18,
         [ETH('ATEM Control / Ethernet'), USBC('USB-C (USB 2)'), SDI('out', 2, 'SDI Out', '3G-SDI'), SDI('in', 4, 'SDI In', '3G-SDI'), MIC2()],
         '4 x 3G-SDI in, 2 x 3G-SDI out (program, aux), Ethernet, USB-C webcam out.', 'ATEM SDI', 'atemsdi'),
        ('atem-sdi-pro-iso', 'ATEM SDI Pro ISO', 'W-APS-32', 9.35, 1.38, 4.67, 23.9 * OZ, 36,
         [ETH('ATEM Control / Ethernet'), USBC('USB-C Out (webcam, disk)'), SDI('out', 2, 'SDI Out', '3G-SDI'), SDI('in', 4, 'SDI In', '3G-SDI'), MIC2()],
         '4 x 3G-SDI in, 2 x 3G-SDI out, streaming and ISO recording to a USB disk.', 'ATEM SDI', 'atemsdi'),
        ('atem-sdi-extreme-iso', 'ATEM SDI Extreme ISO', 'W-APS-36', 14.56, 1.56, 5.94, 3.13 * LB, 36,
         [ETH('ATEM Control / Ethernet'), g('rear', 'io', 'USB', 'USB-C', 2, 'USB-C'), SDI('out', 4, 'SDI Out', '3G-SDI'), SDI('in', 8, 'SDI In', '3G-SDI'),
          MIC2(), R('out', 'Analog audio', '3.5mm jack', 1, 'Headphones')],
         '8 x 3G-SDI in, 4 x 3G-SDI out (program, aux), streaming and ISO recording.', 'ATEM SDI', 'atemsdi')]:
    ru = 1 if mm(h_in) <= 44 else 2
    add(slug, name, name, fam, 'switcher', ru, cols(w_in), ports + [DC12()],
        desc + f' {watts} W.' + SW.format(ru=ru) + ' ' + sz(w_in, h_in, d_in, round(kg, 2)),
        page, code, powerW=watts, weightKg=round(kg, 2), **box(w_in, h_in, d_in))

# ======================= Shelves =======================
URS = ('1RU rack shelf for Blackmagic one-third and half rack width units (Teranex Mini, MultiView 4, HyperDeck Studio HD Mini and HD Plus, '
       'Streaming Encoder and Decoder, UltraStudio 4K Mini and Express HD, Web Presenter, Studio Converter, Teranex Mini 8K), with blanking '
       'panels for empty spaces. ')
add('universal-rack-shelf-thirds', 'Blackmagic Universal Rack Shelf', 'Blackmagic Universal Rack Shelf (3 x 1/3 width)', 'Rack Shelf', 'shelf', 1, 12, [],
    URS + 'This entry is set up for three one-third width units. For two half width units use the other Universal Rack Shelf entry; '
    'for a mix, place the units straight into the rack at 1/3 and 1/2 width.', 'teranexmini8k', None,
    carrier={'bays': 3, 'fits': [THIRD]})
add('universal-rack-shelf-halves', 'Blackmagic Universal Rack Shelf', 'Blackmagic Universal Rack Shelf (2 x 1/2 width)', 'Rack Shelf', 'shelf', 1, 12, [],
    URS + 'This entry is set up for two half width units.', 'teranexmini8k', None, carrier={'bays': 2, 'fits': [HALF]})
add('teranex-mini-rack-shelf', 'Teranex Mini Rack Shelf', 'Teranex Mini Rack Shelf (3 x 1/3 width)', 'Rack Shelf', 'shelf', 1, 12, [],
    '1RU shelf for three Teranex Mini sized (one-third width) units: Teranex Mini, MultiView 4, HyperDeck Studio HD Mini and similar. '
    'Earlier model, largely replaced by the Universal Rack Shelf.', 'hyperdeckstudio', None, carrier={'bays': 3, 'fits': [THIRD]})

ids = [m['id'] for m in M]; assert len(ids) == len(set(ids))
json.dump(M, open(os.path.join(CAT, 'bmd-desktop.json'), 'w'), indent=1)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'bmd-desktop.json' not in idx:
    idx.append('bmd-desktop.json'); json.dump(idx, open(ip, 'w'))
print('bmd-desktop.json', len(M), 'entries,', sum(m['verified'] for m in M), 'verified')
