#!/usr/bin/env python3
"""Fuller catalogues for Wohler, Clear-Com, Miranda (Grass Valley legacy), Cobalt Digital, Chyron, Tektronix (Telestream) and Leader
(added 2026-11-15). Each brand already had a few entries from earlier scripts; this one writes separate *-more files so those
scripts can be re-run without losing anything:
  wohler-more.json     Wohler eSeries / iSeries audio and AV monitors, AMP legacy, rack LCD monitors (wohler.json: iAM-12G-SDI, iAM1-12G).
  clearcom-more.json   Clear-Com Eclipse HX-PiCo, V-Series Iris panels, FreeSpeak II / Edge base stations, LQ rack units, Encore
                       and HelixNet rack stations (clearcom.json: HX frames, Arcadia, HMS-4X). Rear panels counted from Clear-Com's
                       architectural drawing pack (back views).
  gv-miranda.json      Miranda / NVISION legacy (now Grass Valley): Kaleido-X, Kaleido-X16, Kaleido-Alto/Quad, NVISION routers and
                       NV5100MC, Imagestore. Densite frames and the XVP-3901 stay in gv-densite.json.
  cobalt-more.json     Cobalt Digital openGear cards, HPF-MAX / HPF-9500 / oGx frames, BBG standalone units, ARIA-2, WAVE RTR-36x36
                       (cobalt.json: 10 cards and the WAVE 32x32 / 64x64).
  chyron.json          Chyron (ChyronHego) PRIME rendering engine and legacy HyperX / Duet engines.
  telestream-more.json Tektronix / Telestream sync generators, changeovers and waveform monitors not already in telestream.json
                       (SPG9000, ECO8000) or telestream-video.json (PRISM MPP-200 / MPD-200, WVR8300).
  leader-more.json     Leader / PHABRIX rasterizers, waveform monitors, changeover (leader.json: LV5600W, LV5350, LT4670, QxL).
Not added: Wohler vMON 18.5-32 inch and HDM-215 desktop monitors, option cards and SFPs (they are options on the monitors), Clear-Com
beltpacks, transceivers, headsets and Eclipse interface cards, Chyron software products (LIVE, CAMIO, AXIS, Paint, Click Effects run on
off-the-shelf servers), Leader / PHABRIX handhelds. 'Check:' marks anything unconfirmed."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update({k: v for k, v in kw.items() if v is not None}); FILES.setdefault(file, []).append(m)
AC = lambda n=1, p=None: R('in', 'Power', 'IEC C14', n, p or ('PSU' if n > 1 else 'AC In'))
REF = [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop')]
LAN = lambda n=1, p='Ethernet': R('io', 'Ethernet', 'RJ45', n, p)
HP = F('out', 'Analog audio', '1/4" TRS', 1, 'Headphones')

# ======================= Wohler =======================
W, WF = 'Wohler', 'wohler-more.json'
WU = lambda s: 'https://www.wohler.com/product/' + s
WS = 'Wohler product page (2025)'
def wa(id, pn, name, fam, ru, ports, notes, verified=False, **kw):
    add(WF, 'wohler-' + id, W, pn, name, fam, 'audio', ru, ports, notes, WS, WU(pn.lower()), verified=verified, **kw)
SDI2 = [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out')]
ANA_XLR = [R('in', 'Analog audio', 'XLR3F', 2, 'Analog In L/R'), R('out', 'Analog audio', 'XLR3M', 2, 'Analog Out L/R')]
AES_HD15 = R('io', 'AES/EBU', 'HD15', 1, 'AES In/Out (option)')
ISER = lambda: [LAN(1, 'Ethernet'), F('io', 'USB', 'USB-A', 1, 'USB'), HP]
wa('eamp1-16-m', 'eAMP1-16-M', 'eAMP1-16-M 16-channel 3G-SDI audio monitor, 1RU', 'eSeries', 1,
   [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Loop'), R('out', 'Analog audio', 'XLR3M', 2, 'Analog Out L/R'),
    R('in', 'Other', 'DB9', 1, 'GPI'), AC(), HP],
   'Two SDI inputs, 16-channel metering, stereo speakers. 483 x 45 x 140 mm, 1.5 kg, 19 W. '
   'Check: SDI loop outputs and GPI connector (page confirms 2 SDI in and XLR-M analogue outs only).', powerW=19, weightKg=1.5)
wa('eamp1-8-m', 'eAMP1-8-M', 'eAMP1-8-M 8-channel 3G-SDI audio monitor, 1RU', 'eSeries', 1,
   [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Loop'), R('out', 'Analog audio', 'XLR3M', 2, 'Analog Out L/R'), AC(), HP],
   '8-channel version of the eAMP1-16-M. Check: SDI loop outputs.')
for pn, ch, sdi, txt in [('eAMP1-S16-MDA', 16, 2, '16-channel SDI, AES and analogue'), ('eAMP1-S16-2MDA', 16, 2, 'dual 3G-SDI, AES and analogue, 16-channel'),
                         ('eAMP1-S8-MDA', 8, 2, '8-channel SDI, AES and analogue'), ('eAMP1-S8-2MDA', 8, 2, 'dual 3G-SDI, AES and analogue, 8-channel'),
                         ('eAMP1-S8-DA', 8, 0, '8-channel AES and analogue (no SDI)')]:
    ports = ([R('in', '3G-SDI', 'BNC', sdi, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop')] if sdi else []) + \
            [R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('in', 'Analog audio', 'DB25', 1, 'Analog In (8 ch)'),
             R('out', 'Analog audio', 'XLR3M', 2, 'Analog Out L/R'), AC(), HP]
    wa(pn.lower(), pn, f'{pn} {txt} audio monitor, 1RU', 'eSeries', 1, ports,
       f'{txt.capitalize()} audio monitor with level meters and speakers. Check: AES and analogue connector types and counts.')
wa('eam1-mix-8-12g', 'eAM1-MIX-8-12G', 'eAM1-MIX-8-12G 12G-SDI audio monitor and mixer, 1RU', 'eSeries', 1,
   [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out')] + ANA_XLR + [AC(), HP],
   '8-channel 12G-SDI audio monitor and mixer. Check: rear connectors.')
wa('evam1-1', 'eVAM1-1', 'eVAM1-1 3G-SDI audio/video monitor, 1RU', 'eSeries', 1,
   SDI2 + [R('in', 'AES/EBU', 'BNC', 1, 'AES In')] + ANA_XLR + [AC(), HP],
   'Audio monitor with a small video screen: 3G-SDI, AES3 and analogue. eVAM1-1-PLUS adds presets and loudness. Check: rear connectors.')
wa('evam1-16-12g', 'eVAM1-16-12G', 'eVAM1-16-12G 12G-SDI audio/video monitor and mixer, 1RU', 'eSeries', 1,
   [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out')] + ANA_XLR + [AC(), HP],
   '16-channel 12G-SDI and analogue monitor with video thumbnail. Check: rear connectors.')
wa('iam-audio-1-plus', 'iAM-AUDIO-1-PLUS', 'iAM-AUDIO-1-PLUS 16-channel audio monitor, 1RU', 'iSeries', 1,
   SDI2 + ANA_XLR + [AES_HD15, R('io', 'SFP', 'SFP', 2, 'SFP (option)')] + ISER() + [AC()],
   '16-channel 3G-SDI and analogue monitor, Dante / AES67 by option card. Options add AES, MADI, Dolby, analogue/TOSLINK. '
   'Check: option slots fitted.')
wa('iam-audio-2-plus', 'iAM-AUDIO-2-PLUS', 'iAM-AUDIO-2-PLUS 16-channel audio monitor, 2RU', 'iSeries', 2,
   SDI2 + ANA_XLR + [AES_HD15, R('io', 'SFP', 'SFP', 2, 'SFP (option)')] + ISER() + [AC()],
   '2RU version of the iAM-AUDIO-1-PLUS with larger speakers. Check: option slots fitted.')
for n in (8, 16, 32):
    wa(f'iam-sum{n}', f'iAM-SUM{n}', f'iAM-SUM{n} {n}-channel audio monitor and mixer, 1RU', 'iSeries', 1,
       SDI2 + ANA_XLR + [AES_HD15, R('in', 'MADI audio', 'BNC', 1, 'MADI In (option)'), R('out', 'MADI audio', 'BNC', 1, 'MADI Loop (option)'),
                         R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec (option)')] + ISER() + [AC()],
       f'Monitor and mix any {n} channels from SDI, analogue, AES, MADI or Dante. Base: 2 x 3G-SDI in, 1 SDI out, 1 pair analogue in/out on XLR, '
       '65 W, 483 x 45 x 140 mm. Options as listed. Check: which options are fitted.', verified=(n == 16), powerW=65)
wa('iam1-8', 'iAM1-8', 'iAM1-8 8-channel audio monitor, 1RU', 'iSeries', 1, SDI2 + ANA_XLR + ISER() + [AC()],
   '8-channel 3G-SDI and analogue monitor, Dante / AES67 by option. Check: rear connectors.')
wa('iam2-8', 'iAM2-8', 'iAM2-8 8-channel audio monitor, 2RU', 'iSeries', 2, SDI2 + ANA_XLR + ISER() + [AC()],
   '2RU 8-channel 3G-SDI and analogue monitor, Dante / AES67 by option. Check: rear connectors.')
for pn, net in (('iAM1-16-AoIP-DANTE', 'Dante'), ('iAM1-16-AoIP-RAVENNA', 'RAVENNA'), ('iAM1-MIX-8-AoIP-DANTE', 'Dante'), ('iAM1-MIX-8-AoIP-RAVENNA', 'RAVENNA')):
    wa(pn.lower(), pn, f'{pn} MADI + {net} audio monitor, 1RU', 'iSeries AoIP', 1,
       [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Loop'), R('io', 'SFP', 'SFP', 1, 'MADI / network SFP'),
        R('io', 'Dante/AES67', 'RJ45', 2, f'{net} Pri/Sec')] + ANA_XLR + ISER() + [AC()],
       f'Audio-over-IP monitor ({"mixer, " if "MIX" in pn else ""}MADI and {net}). Check: rear connectors.')
wa('iam1-mix8-12g', 'iAM1-MIX8-12G', 'iAM1-MIX8-12G 12G-SDI audio monitor and mixer, 1RU', 'iSeries', 1,
   [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out')] + ANA_XLR + ISER() + [AC()], 'Check: rear connectors.')
wa('iam1-mix8-g', 'iAM1-MIX8-G', 'iAM1-MIX8-G 3G-SDI audio monitor and mixer, 1RU', 'iSeries', 1, SDI2 + ANA_XLR + ISER() + [AC()], 'Check: rear connectors.')
def wv(id, pn, name, ru, sdi, ports, notes, scr, verified=False, **kw):
    add(WF, 'wohler-' + id, W, pn, name, 'iSeries AV', 'audio', ru,
        [R('in', sdi, 'BNC', 2, 'SDI In'), R('out', sdi, 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')] + ANA_XLR + ports + ISER() + [AC()],
        notes, WS, WU(pn.lower()), verified=verified, screens=scr, **kw)
S1 = {'count': 1, 'sizeIn': 4.3, 'aspect': '16:9'}; S2 = {'count': 2, 'sizeIn': 4.3, 'aspect': '16:9'}
wv('ivam1-1-g', 'iVAM1-1-G', 'iVAM1-1-G 3G-SDI audio/video monitor, 1RU', 1, '3G-SDI', [], 'Audio monitor with 4.3-inch video screen, Dante / AES67 by option. Check: rear connectors.', S1)
wv('ivam1-3', 'iVAM1-3', 'iVAM1-3 3G-SDI audio/video monitor, 1RU', 1, '3G-SDI', [AES_HD15], 'Three screens for video and metering. Check: screen count and rear connectors.', {'count': 3, 'sizeIn': 4.3, 'aspect': '16:9'})
wv('ivam1-12g', 'iVAM1-12G', 'iVAM1-12G 12G-SDI audio/video monitor, 1RU', 1, '12G-SDI', [], 'Check: rear connectors.', S1)
wv('ivam1-sum8', 'iVAM1-SUM8', 'iVAM1-SUM8 audio/video monitor with MADI, 1RU', 1, '3G-SDI', [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 1, 'MADI Loop')], 'Check: rear connectors.', S1)
wv('ivam1-sum16-g', 'iVAM1-SUM16-G', 'iVAM1-SUM16-G 3G-SDI audio/video monitor and mixer, 1RU', 1, '3G-SDI', [AES_HD15], 'Check: rear connectors.', S1)
wv('ivam1-sum16-12g', 'iVAM1-SUM16-12G', 'iVAM1-SUM16-12G 12G-SDI audio/video monitor and mixer, 1RU', 1, '12G-SDI', [AES_HD15], 'Check: rear connectors.', S1)
wv('ivam2-12g', 'iVAM2-12G', 'iVAM2-12G 12G-SDI audio/video monitor, 2RU', 2, '12G-SDI',
   [R('in', 'MADI audio', 'BNC', 1, 'MADI In (option)'), R('out', 'MADI audio', 'BNC', 1, 'MADI Loop (option)'), AES_HD15,
    R('io', 'Analog audio', 'DB25', 1, 'Analog 8 ch (option)'), R('io', 'SFP', 'SFP', 2, 'SFP (option)')],
   'Two 4.3-inch touchscreens, 2 x SDI in, 1 SDI out, HDMI monitor out, analogue in/out on XLR; options add MADI, AES (HD15), '
   '8 analogue on DB25 plus TOSLINK, Dante / RAVENNA with SFP, 2 more SFP cages. 60 W.', S2, verified=True, powerW=60)
wv('ivam2-2-g', 'iVAM2-2-G', 'iVAM2-2-G SDI / ST 2110 audio/video monitor, 2RU', 2, '3G-SDI', [R('io', 'SFP', 'SFP', 2, 'ST 2110 SFP')], 'Check: rear connectors.', S2)
wv('ivam2-cmd', 'iVAM2-CMD', 'iVAM2-CMD HDMI 2.0 / 12G-SDI audio/video monitor, 2RU', 2, '12G-SDI', [R('in', 'HDMI', 'HDMI', 1, 'HDMI In')], 'Multi-channel HDMI 2.0 monitoring. Check: rear connectors.', S2)
wv('ivam2-mpeg', 'iVAM2-MPEG', 'iVAM2-MPEG MPEG TS and 12G-SDI monitor, 2RU', 2, '12G-SDI', [R('in', 'Other', 'BNC', 1, 'ASI In'), LAN(1, 'TSoIP')], 'Check: rear connectors.', S2)
wv('ivam2-st2110', 'iVAM2-ST2110', 'iVAM2-ST2110 ST 2110 audio/video monitor, 2RU', 2, '12G-SDI', [R('io', 'SFP', 'SFP28', 2, 'ST 2110 A/B'), LAN(1, 'NMOS control')], 'ST 2110 with out-of-band NMOS control and 12G-SDI. Check: rear connectors.', S2)
wa('amp1-2sda', 'AMP1-2SDA', 'AMP1-2SDA 2-channel audio monitor, 1RU', 'AMP', 1,
   [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('in', 'AES/EBU', 'BNC', 1, 'AES In'),
    R('in', 'Analog audio', 'XLR3F', 2, 'Analog In L/R'), AC(), HP],
   'Compact 2-channel audio monitor; AMP1-2SDA-PLUS adds features. Check: rear connectors.')
wa('amp1a-plus', 'AMP1A-PLUS', 'AMP1A-PLUS 2-channel analogue audio monitor, 1RU', 'AMP', 1,
   [R('in', 'Analog audio', 'XLR3F', 2, 'Analog In L/R'), R('out', 'Analog audio', 'XLR3M', 2, 'Analog Out L/R'), AC(), HP], 'Check: rear connectors.')
wa('vmq-4', 'VMQ-4', 'VMQ-4 4-channel analogue audio monitor, 1RU', 'AMP', 1,
   [R('in', 'Analog audio', 'XLR3F', 4, 'Analog In'), AC(), HP], 'Check: rear connectors.')
wa('hrs-1s', 'HRS-1S', 'HRS-1S self-powered 2-channel speaker system, 1RU', 'AMP', 1,
   [R('in', 'Analog audio', 'XLR3F', 2, 'Analog In L/R'), AC()], 'Check: rack height and rear connectors.')
add(WF, 'wohler-rmog-12g', W, 'RMoG-12G', 'RMoG-12G MAVRIC 12G-SDI remote monitoring probe (openGear card)', 'MAVRIC', 'card', 0,
    [], 'MAVRIC signal probe card for openGear frames; OPT-RMoG-DANTE / -RAVENNA add 64 ch AoIP. Check: rear module connectors.',
    WS, WU('rmog-12g'), verified=False, w=0, card={'fits': ['openGear'], 'slotWidth': 1},
    rearModules=[{'partNumber': 'RMoG-12G rear', 'name': 'Standard rear module', 'width': 2, 'cardsPerModule': 1, 'cardOffset': 0, 'default': True, 'included': True,
                  'portGroups': [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('io', 'SFP', 'SFP', 1, 'SFP'), LAN(1, 'Ethernet')]}])
def wm(id, pn, name, ru, scr, sdi, notes, verified=False, dc=False, **kw):
    add(WF, 'wohler-' + id, W, pn, name, 'Rack LCD', 'monitor', ru,
        [R('in', sdi, 'BNC', 2 * scr['count'], 'SDI In'), R('out', sdi, 'BNC', scr['count'], 'SDI Loop'), R('in', 'HDMI', 'HDMI', scr['count'], 'HDMI In'),
         LAN(1, 'Ethernet'), R('in', 'Other', 'DB9', 1, 'GPI'), (R('in', 'Power', 'XLR4M', 1, '12V DC') if dc else AC())],
        notes, WS, WU(pn.lower()), verified=verified, screens=scr, **kw)
wm('rm-2443ws-3g2', 'RM-2443WS-3G2', 'RM-2443WS-3G2 quad 4.3-inch rack LCD, 2RU', 2, {'count': 4, 'sizeIn': 4.3, 'aspect': '16:9'}, '3G-SDI', 'Quad 4.3-inch 3G-SDI monitor. Check: rear connectors.')
wm('rm-4210ws-3g2', 'RM-4210WS-3G2', 'RM-4210WS-3G2 dual 10-inch rack LCD, 4RU', 4, {'count': 2, 'sizeIn': 10.1, 'aspect': '16:10'}, '3G-SDI', 'Dual 10-inch 3G-SDI monitor. Check: rear connectors.')
wm('vmon-2440-4k', 'vMON-2440-4K', 'vMON-2440-4K quad 4.1-inch 12G-SDI rack LCD, 2RU', 2, {'count': 4, 'sizeIn': 4.1, 'aspect': '16:9'}, '12G-SDI', 'Check: rear connectors.', dc=True)
wm('vmon-3280-4k', 'vMON-3280-4K', 'vMON-3280-4K dual 8-inch 12G-SDI rack LCD, 3RU', 3, {'count': 2, 'sizeIn': 8, 'aspect': '16:9'}, '12G-SDI', 'Check: rear connectors.', dc=True)
wm('vmon-4210-4k', 'vMON-4210-4K', 'vMON-4210-4K dual 10.1-inch 12G-SDI rack LCD, 4RU', 4, {'count': 2, 'sizeIn': 10.1, 'aspect': '16:10'}, '12G-SDI',
   'Per screen: 2 x 12G-SDI in, HDMI, RJ45, GPI; 12 V DC, 37 W. Check: SDI loop outputs (not stated).', verified=True, dc=True, powerW=37)
wm('rmtf-170-3g-rm', 'RMTF-170-3G-RM', 'RMTF-170-3G-RM 17-inch rack LCD', 8, {'count': 1, 'sizeIn': 17, 'aspect': '16:9'}, '3G-SDI', 'Check: rack height (8RU assumed) and rear connectors.')

# ======================= Clear-Com =======================
C, CF = 'Clear-Com', 'clearcom-more.json'
CD = 'Clear-Com architectural drawings (back view) in the project files'
def cc(id, pn, name, fam, ru, ports, notes, url, verified=True, src=CD, cat='audio', **kw):
    add(CF, 'cc-' + id, C, pn, name, fam, cat, ru, ports, notes, src, url, verified=verified, **kw)
CU = 'https://www.clearcom.com/'
DC12 = R('in', 'Power', 'XLR4M', 1, '12V DC In')
for keys, kind, ru in ((12, 'L', 1), (12, 'R', 1), (12, 'P', 1), (32, 'L', 2), (24, 'R', 2), (24, 'P', 2)):
    k = {'L': 'lever', 'R': 'rotary', 'P': 'pushbutton'}[kind]
    cc(f'vi-pnl-{keys}{kind.lower()}', f'VI-PNL-{keys}{kind}-X4', f'V-Series Iris {keys}-key {k} panel, {ru}RU', 'V-Series Iris', ru,
       [DC12, R('io', 'Ethernet', 'RJ45', 2, 'LAN'), R('io', 'USB', 'USB-A', 1, 'USB 2.0'), R('io', 'GPIO', 'DB25', 1, 'GPIO'),
        R('io', 'Analog audio', 'DB25', 1, 'Aux Audio'), R('io', 'Analog audio', 'RJ45', 1, 'Matrix (analog)'), R('io', 'Other', 'RJ45', 1, 'Expansion'),
        F('io', 'Analog audio', 'XLR4M', 1, 'Headset'), F('in', 'Analog audio', '1/4" TRS', 1, 'Gooseneck mic')],
       f'Eclipse HX user panel, {keys} {k} keys, IP (two LAN) or analogue 4-wire to the matrix, 12 V DC from the external PSU. '
       'Suffix X4 = XLR4 headset; -X5 and -X7 have 5- and 7-pin headset connectors.', CU, src=CD + '; Clear-Com knowledge base panel list')
for keys, kind in ((16, 'L'), (12, 'R'), (12, 'P')):
    cc(f'vi-exp-{keys}{kind.lower()}', f'VI-EXP-{keys}{kind}', f'V-Series Iris {keys}-key expansion panel, 1RU', 'V-Series Iris', 1,
       [DC12, R('in', 'Other', 'RJ45', 1, 'Expansion In'), R('out', 'Other', 'RJ45', 1, 'Expansion Out')],
       'Key expansion for an Iris panel of the same key type, daisy-chained on the expansion ports.', CU)
cc('hx-pico', 'Eclipse HX-PiCo', 'Eclipse HX-PiCo matrix intercom, 1RU', 'Eclipse HX', 1,
   [R('io', 'Analog audio', 'RJ45', 8, 'Analog port (4-wire)'), R('io', 'Ethernet', 'RJ45', 2, 'LAN (IVC-32 / panels)'), R('io', 'GPIO', 'DB25', 1, 'GPIO'),
    R('io', 'Other', 'DB9', 1, 'Matrix link / alarm'), R('in', 'Power', 'IEC C14', 2, 'AC In A/B')],
   '1RU Eclipse matrix: 8 analogue 4-wire ports, 32 IP ports (IVC-32 built in), redundant PSUs. Check: all rear connectors (no drawing in the pack).',
   CU, verified=False, src='Clear-Com HX-PiCo listings')
cc('fsii-base-ii', 'FSII-BASE-II', 'FreeSpeak II Base II wireless intercom base station, 1RU', 'FreeSpeak II', 1,
   [AC(1), R('in', 'Power', 'XLR4M', 1, '12V DC'), R('io', 'SFP', 'SFP', 2, 'ANT 1/2 (fibre)'), R('io', 'Other', 'RJ45', 2, 'ANT 1/2 (copper)'),
    R('out', 'Other', 'RJ45', 1, 'Sync Out'), R('in', 'Other', 'RJ45', 1, 'Sync In'), R('io', 'Analog audio', 'XLR3F', 4, '2-wire A-D'),
    R('io', 'Analog audio', 'RJ45', 4, '4-wire 1-4'), R('in', 'Analog audio', 'XLR3F', 1, 'Program In'), R('out', 'Analog audio', 'XLR3M', 1, 'SA Out'),
    R('io', 'Ethernet', 'etherCON', 2, 'LAN 1/2'), R('io', 'GPIO', 'DB15', 1, 'GPIO')],
   'Base station for FreeSpeak II 1.9 GHz / 2.4 GHz / 5 GHz transceivers (two antenna ports, more through FSII-SPL splitters). '
   'Front has headset and display.', CU)
cc('fse-base', 'FSE-BASE', 'FreeSpeak Edge base station, 1RU', 'FreeSpeak Edge', 1,
   [AC(1), R('in', 'Power', 'XLR4M', 1, 'DC PWR 2'), R('io', 'GPIO', 'DB9', 2, 'GPIO 1/2'), R('io', 'Analog audio', 'XLR3F', 4, '2-wire'),
    R('io', 'Analog audio', 'RJ45', 8, '4-wire / SA / PGM'), R('out', 'Other', 'RJ45', 1, 'Sync Out'), R('in', 'Other', 'RJ45', 1, 'Sync In'),
    R('io', 'Other', 'RJ45', 4, 'SPL / TCVR 1-4'), R('io', 'Ethernet', 'RJ45', 4, 'LAN 1-4')],
   '5 GHz FreeSpeak Edge base: transceivers on the SPL/TCVR ports or over IP (FSE-TCVR-50-IP). Same chassis as Arcadia. '
   'Check: 2-wire ports are 2 channels with loop-throughs.', CU)
cc('fsii-spl', 'FSII-SPL', 'FreeSpeak II transceiver splitter (desktop / shelf)', 'FreeSpeak II', 1,
   [R('in', 'Power', 'XLR4M', 1, 'DC In'), R('io', 'Other', 'RJ45', 1, 'Base (copper)'), R('io', 'SFP', 'SFP', 1, 'Base (fibre)'),
    R('io', 'Other', 'etherCON', 5, 'Transceiver 1-5')],
   '222 mm wide splitter for five FreeSpeak II transceivers; sits on a shelf (shown as 5/12 of the rack width). Check: fibre option.', CU, w=5)
LQ = []
for pn, ports, txt in (
        ('LQ-R2W4', [R('io', 'Analog audio', 'XLR3F', 4, '2-wire A-D'), R('io', 'Analog audio', 'XLR3M', 4, '2-wire A-D loop')], '4 x 2-wire partyline'),
        ('LQ-R2W4-4W4', [R('io', 'Analog audio', 'XLR3F', 4, '2-wire A-D'), R('io', 'Analog audio', 'RJ45', 4, '4-wire E-H')], '4 x 2-wire + 4 x 4-wire'),
        ('LQ-R2W4-4WG4', [R('io', 'Analog audio', 'XLR3F', 4, '2-wire A-D'), R('io', 'Analog audio', 'DB9', 4, '4-wire + GPIO E-H')], '4 x 2-wire + 4 x 4-wire with GPIO'),
        ('LQ-R4W8', [R('io', 'Analog audio', 'RJ45', 8, '4-wire A-H')], '8 x 4-wire'),
        ('LQ-R4WG8', [R('io', 'Analog audio', 'DB9', 8, '4-wire + GPIO A-H')], '8 x 4-wire with GPIO')):
    cc(pn.lower(), pn, f'{pn} LQ IP interface, {txt}, 1RU', 'LQ', 1,
       ports + [R('io', 'Ethernet', 'etherCON', 2, 'LAN 1/2'), R('in', 'Power', 'XLR4M', 2, '12V PSU 1/2')],
       f'LQ rack-mount interface linking {txt} over IP (to other LQ units, Eclipse, Arcadia, Agent-IC). Two 12 V DC inputs for redundancy.', CU)
cc('hrm-4x', 'HRM-4X', 'HelixNet HRM-4X remote station, 1RU', 'HelixNet', 1,
   [R('in', 'Power', 'XLR4M', 1, '48V DC'), R('io', 'Other', 'XLR3F', 1, 'Digital Intercom'), R('io', 'Other', 'XLR3M', 1, 'Digital Intercom loop'),
    R('io', 'Ethernet', 'etherCON', 1, 'Ethernet'), R('io', 'Analog audio', 'DB9', 1, 'Audio + Control'), R('out', 'Analog audio', 'XLR3M', 1, 'SA / 4W Out'),
    R('in', 'Analog audio', 'XLR3F', 1, 'PGM / 4W In'), R('out', 'Analog audio', '1/4" TRS', 1, 'Hot Mic Out'),
    F('io', 'Analog audio', 'XLR4M', 1, 'Headset'), F('in', 'Analog audio', '1/4" TRS', 1, 'Gooseneck mic')],
   'Four-channel HelixNet rack station, powered over the HelixNet cable (or DC). HXII-RM is the earlier version with the same rear layout.', CU)
cc('if4w4', 'IF4W4', 'Encore IF4W4 four-channel 2-wire to 4-wire interface, 1RU', 'Encore', 1,
   [R('io', 'Analog audio', 'XLR3F', 4, 'Channel A-D (partyline)'), R('io', 'Analog audio', 'Terminal block', 4, '4-wire Tx/Rx A-D')],
   'Converts four Encore partyline channels to 4-wire, with transmit level switch per channel. Powered from the partyline.', CU)
cc('ms-702', 'MS-702', 'Encore MS-702 two-channel main station, 1RU', 'Encore', 1,
   [AC(1), R('io', 'Analog audio', 'XLR3F', 3, 'Intercom Channel A'), R('io', 'Analog audio', 'XLR3F', 3, 'Intercom Channel B'),
    R('in', 'Analog audio', 'XLR3F', 1, 'Program In'), R('out', 'Analog audio', 'XLR3M', 1, 'Announce Out'),
    R('out', 'Other', '1/4" TRS', 1, 'Relay Out'), R('out', 'Analog audio', '1/4" TRS', 1, 'Hot Mic / IFB'),
    F('io', 'Analog audio', 'XLR4M', 1, 'Headset'), F('in', 'Analog audio', '1/4" TRS', 1, 'Gooseneck mic')],
   'Two-channel partyline main station with built-in 30 V supply (1.2 A) for the line.', CU)
cc('ms-704', 'MS-704', 'Encore MS-704 four-channel main station, 2RU', 'Encore', 2,
   [AC(1), R('io', 'Analog audio', 'XLR3F', 8, 'Channel A-D (2 each)'), R('in', 'Analog audio', 'XLR3F', 1, 'Program In'),
    R('out', 'Analog audio', 'XLR3M', 1, 'Announce Out'), R('io', 'Other', 'DB15', 1, 'Auxiliary'), R('out', 'Analog audio', '1/4" TRS', 1, 'Hot Mic / IFB'),
    F('io', 'Analog audio', 'XLR4M', 1, 'Headset'), F('in', 'Analog audio', '1/4" TRS', 1, 'Gooseneck mic')],
   'Four-channel partyline main station with built-in 30 V supply.', CU)
cc('rm-704', 'RM-704', 'Encore RM-704 four-channel remote station, 2RU', 'Encore', 2,
   [R('io', 'Analog audio', 'XLR3F', 8, 'Channel A-D (2 each)'), R('in', 'Analog audio', 'XLR3F', 1, 'Program In'),
    R('out', 'Analog audio', 'XLR3M', 1, 'Announce Out'), R('io', 'Other', 'DB15', 1, 'Auxiliary'), R('out', 'Analog audio', '1/4" TRS', 1, 'Hot Mic / IFB'),
    F('io', 'Analog audio', 'XLR4M', 1, 'Headset'), F('in', 'Analog audio', '1/4" TRS', 1, 'Gooseneck mic')],
   'Four-channel remote station, powered from the partyline (no mains).', CU)
cc('ps-704', 'PS-704', 'Encore PS-704 four-channel partyline power supply, 1RU', 'Encore', 1,
   [AC(1), R('io', 'Analog audio', 'XLR3F', 8, 'Channel A-D (2 each)'), R('in', 'Analog audio', 'XLR3F', 1, 'Program In')],
   'Powers and terminates four partyline channels (30 V, 1.2 A), with program feed.', CU, cat='power')

# ======================= Miranda / NVISION (Grass Valley legacy) =======================
GF, GV = 'gv-miranda.json', 'Grass Valley'
GS = 'Miranda / Grass Valley legacy documentation'
def mi(id, pn, name, fam, cat, ru, ports, notes, url, verified=False, src=GS, **kw):
    add(GF, 'gv-' + id, GV, pn, name, fam, cat, ru, ports, notes, src, url, verified=verified, **kw)
KX = 'https://wwwapps.grassvalley.com/docs/DataSheets/multiviewers/Kaleido-X_DS-PUB-2-0230A-EN.pdf'
mi('kaleido-x-7ru', 'KXA-FR7-B', 'Miranda Kaleido-X 7RU multiviewer frame (96 in / 8 out)', 'Kaleido-X', 'monitor', 7,
   [R('in', '3G-SDI', 'BNC', 96, 'Video In'), R('out', 'DVI', 'DVI-D', 8, 'Head Out (DVI)'), R('out', 'HD-SDI', 'BNC', 8, 'Head Out SDI (KXO-HDM-B)'),
    R('in', 'DVI', 'DVI-D', 2, 'Background In'), R('out', 'Analog audio', 'DB25', 2, 'Analog Audio Out'), R('out', 'AES/EBU', 'BNC', 2, 'AES Out'),
    R('in', 'Timecode', 'BNC', 3, 'LTC In'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'GPI', 'DB37', 3, 'GPI A/B/C'),
    LAN(1), R('io', 'USB', 'USB-A', 1, 'USB'), R('io', 'RS-422', 'DB9', 1, 'RS-422'), AC(2)],
   'Six 16-input modules (3G/HD/SD/composite) and four dual-output modules; two frames link for 192 in / 12 out. 1500 W hot-swap PSUs. '
   'Check: GPI and audio connector types; inputs depend on modules fitted.', KX, src='Kaleido-X data sheet DS-PUB-2-0230A', full=True)
mi('kaleido-x-4ru', 'KXA-FR4', 'Miranda Kaleido-X 4RU multiviewer frame (48 in / 4 out)', 'Kaleido-X', 'monitor', 4,
   [R('in', '3G-SDI', 'BNC', 48, 'Video In'), R('out', 'DVI', 'DVI-D', 4, 'Head Out (DVI)'), R('out', 'HD-SDI', 'BNC', 4, 'Head Out SDI (option)'),
    R('in', 'Reference', 'BNC', 1, 'Ref In'), R('in', 'Timecode', 'BNC', 1, 'LTC In'), R('io', 'GPI', 'DB37', 1, 'GPI'), LAN(1), AC(2)],
   'Half-size Kaleido-X frame. Check: all counts.', 'https://wwwapps.grassvalley.com/docs/Manuals/purple/kaleido-x/M809-9905-110-Kaleido-X_4RU_QuickStartGuide.pdf', full=True)
mi('kaleido-x16', 'Kaleido-X16', 'Miranda Kaleido-X16 multiviewer with routing, 1RU', 'Kaleido-X', 'monitor', 1,
   [R('in', '3G-SDI', 'BNC', 16, 'Video In'), R('out', 'DVI', 'DVI-D', 2, 'Head Out'), R('out', 'HD-SDI', 'BNC', 2, 'Head Out SDI'),
    R('out', '3G-SDI', 'BNC', 4, 'Router Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'GPI', 'DB25', 1, 'GPI/LTC'), LAN(1), AC(2)],
   '16-input 1RU multiviewer with 2 heads and a built-in 16x4 router (16x2 on some models). Quiet fan for trucks. Check: router outputs and GPI.',
   'https://wwwapps.grassvalley.com/docs/Manuals/purple/kaleido-x16/M869-9902-113-Kaleido-X16_InstallationManual.pdf')
mi('kaleido-alto-hd', 'Kaleido-Alto-HD', 'Miranda Kaleido-Alto-HD multiviewer, 1RU (10 or 16 inputs)', 'Kaleido-Alto', 'monitor', 1,
   [R('in', 'HD-SDI', 'BNC', 16, 'Video In'), R('out', 'DVI', 'DVI-I', 1, 'Head Out'), R('out', 'HD-SDI', 'BNC', 1, 'Head Out SDI'),
    R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'GPI', 'DB25', 1, 'GPI / LTC'), LAN(1), R('io', 'RS-422', 'DB9', 1, 'RS-422'), R('in', 'Power', 'DC', 1, 'DC In')],
   'Single-head 1RU multiviewer, 10 or 16 auto-sensing inputs. Check: all counts.', 'https://www.gearwise.se/shop/video/image-processing/miranda-kaleido-alto-sd-hd-multiviewer/')
mi('kaleido-quad', 'Kaleido-Quad', 'Miranda Kaleido-Quad 4-input multiviewer, 1RU half width', 'Kaleido-Alto', 'monitor', 1,
   [R('in', 'HD-SDI', 'BNC', 4, 'Video In'), R('out', 'HD-SDI', 'BNC', 4, 'Video Loop'), R('out', 'DVI', 'DVI-I', 1, 'Head Out'),
    R('out', 'HD-SDI', 'BNC', 1, 'Head Out SDI'), LAN(1), R('in', 'Power', 'DC', 1, 'DC In')],
   'Quad split multiviewer; Kaleido-Quad-Dual has two heads. Check: all counts and width.', 'https://www.avbroadcast.fr/', w=6)
NV = 'https://www.manualsdir.com/manuals/796513/grass-valley-nv8288-v15.html?page=13'
for pn, ru, n, o, note, ver in (('NV8288', 10, 288, 576, 'Expands in 12-port steps from 12x12. 305 mm deep.', True),
                                ('NV8144', 8, 144, 288, 'Check: frame height and counts.', False),
                                ('NV8576', 32, 576, 1152, 'Check: frame height (two 16RU halves) and counts.', False),
                                ('NV8140', 4, 64, 64, 'Compact NVISION router. Check: frame height and counts.', False)):
    mi(pn.lower(), pn, f'NVISION {pn} router frame ({n}x{o})', 'NVISION', 'router', ru,
       [R('io', 'Other', 'Card slot', 1, 'Input / output card rears'), R('in', 'Reference', 'BNC', 2, 'Video Ref 1/2'), R('io', 'Ethernet', 'RJ45', 2, 'Control LAN'),
        R('io', 'RS-422', 'DB9', 2, 'Serial / diag'), R('io', 'Other', 'DB25', 1, 'Alarms'), AC(2)],
       f'Up to {n} inputs and {o} outputs (3G/HD/SD, coax or fibre cards); I/O is on the cards fitted, so add it per device. {note}',
       NV, verified=ver, src='NVISION NV8288 user manual v1.5' if ver else GS, full=True)
mi('nv5128', 'NV5128', 'NVISION NV5128 multi-format audio router', 'NVISION', 'router', 8,
   [R('io', 'Other', 'Card slot', 1, 'Audio I/O card rears (AES, MADI, analogue)'), R('in', 'Reference', 'BNC', 2, 'Ref'), R('io', 'Ethernet', 'RJ45', 2, 'Control LAN'), AC(2)],
   'Mono-level audio router for AES, MADI and analogue, 128-port blocks. Check: frame height and connectors.', NV)
mi('nv5100mc', 'NV5100MC', 'NVISION NV5100MC master control processor frame', 'NVISION', 'switcher', 4,
   [R('in', 'HD-SDI', 'BNC', 2, 'PGM / PST In'), R('out', 'HD-SDI', 'BNC', 4, 'PGM Out'), R('in', 'AES/EBU', 'BNC', 8, 'AES In'), R('out', 'AES/EBU', 'BNC', 8, 'AES Out'),
    R('in', 'Reference', 'BNC', 2, 'Ref'), R('io', 'GPI', 'DB37', 1, 'GPI'), R('io', 'Ethernet', 'RJ45', 2, 'LAN'), AC(2)],
   'Master control processor fed from an NVISION router. Check: all counts.', NV)
mi('imagestore-750', 'Imagestore 750', 'Miranda Imagestore 750 HD/SD master control and branding processor, 1RU', 'Imagestore', 'switcher', 1,
   [R('in', 'HD-SDI', 'BNC', 2, 'PGM / PST In'), R('out', 'HD-SDI', 'BNC', 2, 'PGM Out'), R('out', 'HD-SDI', 'BNC', 1, 'Preview Out'), R('in', 'HD-SDI', 'BNC', 2, 'Key / Fill In'),
    R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
    R('io', 'GPI', 'DB25', 1, 'GPI'), R('io', 'RS-422', 'DB9', 2, 'RS-422'), LAN(1), AC(2)],
   'Channel branding and master control (logos, DVE squeeze, voice-over); Imagestore 300 and Intuition XG are related models. Check: all counts.',
   'https://www.grassvalley.com/')

# ======================= Cobalt Digital =======================
CB, BF = 'Cobalt Digital', 'cobalt-more.json'
CBU = lambda s: f'https://cobaltdigital.com/products/{s}/'
CBS = 'Cobalt Digital openGear product list (2025)'
def cbc(pn, name, ports, notes, verified=False, rm=None, slot=1, fam='Cobalt openGear'):
    add(BF, 'cobalt-' + pn.lower().replace(' ', '-').replace('/', '-'), CB, pn, name, fam, 'card', 0, [], notes, CBS, CBU(pn.lower()),
        verified=verified, w=0, card={'fits': ['openGear'], 'slotWidth': slot},
        rearModules=[{'partNumber': rm or f'RM20-{pn.split("-")[0]}-B', 'name': 'Standard width', 'width': 2, 'cardsPerModule': 1, 'cardOffset': 0,
                      'default': True, 'included': False, 'layout': {'cols': 2}, 'portGroups': ports}])
SDI = lambda d, n, p, t='3G-SDI': R(d, t, 'BNC', n, p)
CHK = 'Check: rear module connector counts (standard RM20 module assumed).'
cbc('9904-UDX-4K', '9904-UDX-4K 12G UHD up/down/cross converter, frame sync, HDR', [SDI('in', 4, 'SDI In', '12G-SDI'), SDI('out', 4, 'SDI Out', '12G-SDI'), R('io', 'AES/EBU', 'BNC', 2, 'AES I/O')],
    '12G / quad-link UHD converter with HDR conversion; Dante and INDIGO 2110-DC-01 options. ' + CHK)
cbc('9904-UDX-4K-DSP', '9904-UDX-4K-DSP 12G UHD converter, frame sync, DSP audio', [SDI('in', 4, 'SDI In', '12G-SDI'), SDI('out', 4, 'SDI Out', '12G-SDI'), R('io', 'AES/EBU', 'BNC', 2, 'AES I/O')], CHK)
for pn, txt in (('9902-UDX', '3G up/down/cross converter, frame sync, auto-changeover'), ('9902-UDX-DSP', '3G converter, frame sync, DSP audio'),
                ('9902-2UDX', 'dual-channel 3G up/down/cross converter'), ('9902-2UDX-DI', 'dual-channel 3G converter with de-interlacer'),
                ('9902-UDX-FS', '3G converter + frame sync (two paths)'), ('9902-DC-4K', 'quad-input UHD downconverter')):
    cbc(pn, f'{pn} {txt}', [SDI('in', 4 if 'DC-4K' in pn else 2, 'SDI In'), SDI('out', 4, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 4, 'AES I/O')], CHK)
cbc('9903-UDX-ADDA', '9903-UDX-ADDA universal format converter, CVBS/YPbPr, AES and analogue audio',
    [SDI('in', 1, 'SDI In'), SDI('out', 2, 'SDI Out'), R('io', 'Analog video', 'BNC', 3, 'CVBS / YPbPr I/O'), R('io', 'AES/EBU', 'BNC', 2, 'AES I/O'),
     R('io', 'Analog audio', 'Terminal block', 1, 'Analog audio I/O')], CHK)
for pn, txt, n in (('9922-FS', '3G frame sync, CVBS I/O', 1), ('9922-2FS', 'dual-channel 3G frame sync', 2), ('9922-FS-DSP', '3G frame sync, DSP audio', 1)):
    cbc(pn, f'{pn} {txt}', [SDI('in', 2 * n, 'SDI In'), SDI('out', 2 * n, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 2, 'AES I/O')], CHK)
cbc('9924-4FS-12G', '9924-4FS-12G quad 12G frame sync, AES and MADI', [SDI('in', 4, 'SDI In', '12G-SDI'), SDI('out', 4, 'SDI Out', '12G-SDI'), R('io', 'MADI audio', 'BNC', 2, 'MADI / AES')], CHK)
cbc('9934-AUD-PRO-DSP', '9934-AUD-PRO-DSP 3G advanced audio processor', [SDI('in', 2, 'SDI In'), SDI('out', 2, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 4, 'AES I/O')], CHK)
for pn, aes in (('9933-EMDE-75', 'BNC'), ('9933-EMDE-110', 'DB25')):
    cbc(pn, f'{pn} 3G embedder / de-embedder, 16 ch AES', [SDI('in', 1, 'SDI In'), SDI('out', 2, 'SDI Out'), R('in', 'AES/EBU', aes, 4 if aes == 'BNC' else 1, 'AES In'),
                                                          R('out', 'AES/EBU', aes, 4 if aes == 'BNC' else 1, 'AES Out')], CHK, rm='RM20-9933-B' if aes == 'BNC' else 'RM20-9933-D')
cbc('9933-EMDE-ADDA', '9933-EMDE-ADDA 3G embedder / de-embedder, 16 AES + 8 analogue', [SDI('in', 1, 'SDI In'), SDI('out', 2, 'SDI Out'), R('io', 'AES/EBU', 'DB25', 1, 'AES I/O'), R('io', 'Analog audio', 'DB25', 1, 'Analog I/O')], CHK)
for pn, n in (('9935-AUD2-DANTE', 2), ('9935-AUD4-DANTE', 4)):
    cbc(pn, f'{pn} {n}-path 12G audio embedder / de-embedder with Dante', [SDI('in', n, 'SDI In', '12G-SDI'), SDI('out', n, 'SDI Out', '12G-SDI'),
                                                                        R('io', 'MADI audio', 'BNC', 1, 'MADI'), R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec')], CHK)
cbc('9940-ACO', '9940-ACO multi-input auto-changeover with trouble slate', [SDI('in', 4, 'SDI In'), SDI('out', 2, 'SDI Out')], CHK)
cbc('9940-4x1-CS', '9940-4x1-CS 4x1 clean bypass router, relay protected', [SDI('in', 4, 'SDI In'), SDI('out', 2, 'SDI Out'), R('io', 'GPI', 'RJ45', 1, 'GPIO')], CHK)
cbc('9121', '9121 3G / ASI redundancy switch', [SDI('in', 2, 'SDI/ASI In'), SDI('out', 2, 'SDI/ASI Out')], CHK)
for pn, n in (('9980-CSC-3G', 1), ('9980-2CSC-3G', 2)):
    cbc(pn, f'{pn} {"dual " if n == 2 else ""}RGB colour corrector with test generator', [SDI('in', n, 'SDI In'), SDI('out', 2 * n, 'SDI Out')], CHK)
cbc('9927-2StoH', '9927-2StoH dual SDI to HDMI converter', [SDI('in', 2, 'SDI In', '12G-SDI'), SDI('out', 2, 'SDI Loop', '12G-SDI'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out')], CHK, fam='Sapphire')
cbc('9926-2HtoS', '9926-2HtoS dual HDMI to SDI converter', [R('in', 'HDMI', 'HDMI', 2, 'HDMI In'), SDI('out', 4, 'SDI Out', '12G-SDI')], CHK, fam='Sapphire')
cbc('9928-BIDI-2H2S', '9928-BIDI-2H2S dual bidirectional SDI / HDMI converter', [R('io', 'HDMI', 'HDMI', 2, 'HDMI'), SDI('io', 4, 'SDI', '12G-SDI')], CHK, fam='Sapphire')
for pn, n, rck in (('9910DA-1Q-3G', 1, ''), ('9910DA-2Q-3G', 2, ''), ('9910DA-4Q-3G', 4, '')):
    cbc(pn, f'{pn} {n}-channel 3G / ASI distribution amplifier', [SDI('in', n, 'SDI In'), SDI('out', 10 - n if n < 4 else 4, 'SDI Out')], CHK)
cbc('9915DA-1x16-12G', '9915DA-1x16-12G 12G reclocking DA, 1 in / 16 out', [SDI('in', 1, 'SDI In', '12G-SDI'), SDI('out', 16, 'SDI Out', '12G-SDI')], CHK, rm='RM20-9915-HDBNC')
cbc('9915DA-2x16-XPT-12G', '9915DA-2x16-XPT-12G dual 12G reclocking DA with crosspoint', [SDI('in', 2, 'SDI In', '12G-SDI'), SDI('out', 16, 'SDI Out', '12G-SDI')], CHK, rm='RM20-9915-HDBNC')
cbc('9910DA-AV', '9910DA-AV analogue video DA', [R('in', 'Analog video', 'BNC', 1, 'Video In'), R('out', 'Analog video', 'BNC', 8, 'Video Out')], CHK)
cbc('9913DA-AES75-RG', '9913DA-AES75-RG 75 ohm AES DA with remote gain', [R('in', 'AES/EBU', 'BNC', 2, 'AES In'), R('out', 'AES/EBU', 'BNC', 8, 'AES Out')], CHK)
cbc('9257', '9257 1x9 MADI DA', [R('in', 'MADI audio', 'BNC', 1, 'MADI In'), R('out', 'MADI audio', 'BNC', 9, 'MADI Out')], CHK)
cbc('9910DA-WC', '9910DA-WC word clock DA', [R('in', 'Word clock', 'BNC', 1, 'WC In'), R('out', 'Word clock', 'BNC', 8, 'WC Out')], CHK)
cbc('9930ADC-AES75-RG', '9930ADC-AES75-RG 4-channel analogue to AES', [R('in', 'Analog audio', 'Terminal block', 4, 'Analog In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out')], CHK)
cbc('9930DAC-AES75-RG', '9930DAC-AES75-RG AES to 4-channel analogue', [R('in', 'AES/EBU', 'BNC', 2, 'AES In'), R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out')], CHK)
for pn, d in (('9440-2EO-12G', 'tx'), ('9440-2OE-12G', 'rx'), ('9440-EOOE-12G', 'trx'), ('9440-2EO-3G', 'tx'), ('9440-2OE-3G', 'rx'), ('9440-EOOE-3G', 'trx')):
    t = '12G-SDI' if '12G' in pn else '3G-SDI'
    ports = ([SDI('in', 2, 'SDI In', t), R('out', 'Fibre', 'LC', 2, 'Fibre Out')] if d == 'tx' else
             [R('in', 'Fibre', 'LC', 2, 'Fibre In'), SDI('out', 4, 'SDI Out', t)] if d == 'rx' else
             [SDI('in', 1, 'SDI In', t), R('out', 'Fibre', 'LC', 1, 'Fibre Out'), R('in', 'Fibre', 'LC', 1, 'Fibre In'), SDI('out', 2, 'SDI Out', t)])
    cbc(pn, f'{pn} {t} fibre {"transmitter" if d == "tx" else "receiver" if d == "rx" else "transceiver"} (SDI / ASI / MADI)', ports, 'Fibre via SFP. ' + CHK)
cbc('9923-DSK-LG', '9923-DSK-LG 3G downstream keyer with logo insertion', [SDI('in', 4, 'PGM / Key / Fill In'), SDI('out', 2, 'PGM Out')], CHK)
cbc('9978-ANC-MON', '9978-ANC-MON ancillary data monitoring probe', [SDI('in', 1, 'SDI In'), SDI('out', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'Display')], CHK)
cbc('9970-QS-MC', '9970-QS-MC master control multiviewer', [SDI('in', 5, 'SDI/CVBS In'), SDI('out', 2, 'MV Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), LAN(1)], CHK)
cbc('9960-TG2-REF1', '9960-TG2-REF1 dual 3G test signal generator with sync outputs', [SDI('out', 4, 'Test Out'), R('out', 'Reference', 'BNC', 4, 'Sync Out')], CHK)
cbc('9363', '9363 multi-format reference generator', [R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 8, 'Ref Out')], CHK)
for pn, txt in (('9992-DEC', 'PACIFIC AVC / MPEG-2 decoder'), ('9992-2DEC', 'PACIFIC dual decoder'), ('9992-4ENC-4K-HEVC', 'PACIFIC 4K HEVC encoder'), ('9992-2DEC-4K-HEVC', 'PACIFIC 4K HEVC decoder')):
    enc = 'ENC' in pn
    cbc(pn, f'{pn} {txt}', ([SDI('in', 4, 'SDI In', '12G-SDI'), R('out', 'Other', 'BNC', 2, 'ASI Out')] if enc else [R('in', 'Other', 'BNC', 2, 'ASI In'), SDI('out', 4, 'SDI Out', '12G-SDI')])
        + [R('io', 'Ethernet', 'RJ45', 2, 'IP streams')], CHK)
cbc('9990-RTR-16x16-MPEG-IP', '9990-RTR-16x16-MPEG-IP transport stream router / DA', [R('io', 'Ethernet', 'RJ45', 2, 'GigE'), R('in', 'Other', 'BNC', 4, 'ASI In'), R('out', 'Other', 'BNC', 4, 'ASI Out')], CHK)
cbc('OG-PC-x86-A', 'OG-PC-x86-A x86 PC card for openGear', [R('out', 'HDMI', 'HDMI', 1, 'Display'), R('io', 'USB', 'USB-A', 2, 'USB'), LAN(2)], 'Windows/Linux PC in a frame slot. ' + CHK)
add(BF, 'cobalt-hpf-max', CB, 'HPF-MAX', 'HPF-MAX 20-slot high-power openGear frame, 2RU', 'Cobalt frames', 'frame', 2,
    [R('in', 'Reference', 'BNC', 2, 'Frame Ref (looping)'), LAN(1, 'Ethernet (HPF-GE-FC)'), R('in', 'Power', 'IEC C14', 2, 'PS-MAX 1/2')],
    '20 slots, 600 W for cards, two front-loading hot-swap PS-MAX supplies (one standard), HPF-GE-FC network controller. '
    'Takes standard 20-slot openGear rear modules plus Cobalt high-density ones. 19 x 3.5 x 17 in.', 'Cobalt HPF-MAX product page', CBU('hpf-max'), full=True,
    frame={'system': 'openGear', 'rearGen': 4, 'slots': 20, 'slotOrder': 'ltr', 'rearAlign': 2, 'door': True,
           'controller': 'HPF-GE-FC network controller (built in)', 'front': {'x0': 0.1, 'x1': 0.98, 'y0': 0.05, 'y1': 0.95}, 'rear': {'x0': 0.02, 'x1': 0.82, 'y0': 0.05, 'y1': 0.95}})
for pn, txt in (('HPF-9500', '20-slot high-power openGear-compatible frame (PS-9000 supplies)'), ('oGx', '20-slot openGear frame (PS-oGx supplies)')):
    add(BF, 'cobalt-' + pn.lower(), CB, pn, f'{pn} {txt}, 2RU', 'Cobalt frames', 'frame', 2,
        [R('in', 'Reference', 'BNC', 2, 'Frame Ref (looping)'), LAN(1), R('in', 'Power', 'IEC C14', 2, 'PSU 1/2')],
        'Check: rear connectors and power budget.', CBS, CBU(pn.lower()), verified=False, full=True,
        frame={'system': 'openGear', 'rearGen': 4 if pn == 'oGx' else 3, 'slots': 20, 'slotOrder': 'ltr', 'rearAlign': 2, 'door': True,
               'controller': 'Network controller card', 'front': {'x0': 0.1, 'x1': 0.98, 'y0': 0.05, 'y1': 0.95}, 'rear': {'x0': 0.02, 'x1': 0.82, 'y0': 0.05, 'y1': 0.95}})
add(BF, 'cobalt-aria-2', CB, 'ARIA-2', 'ARIA-2 12G-SDI / MADI / ST 2110 audio monitor, 1RU', 'ARIA', 'audio', 1,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI / MADI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI / MADI Loop'), R('in', 'AES/EBU', 'BNC', 1, 'AES In'),
     R('io', 'SFP', 'SFP28', 2, 'SFP (fibre SDI / ST 2110)'), R('in', 'Analog audio', 'Terminal block', 1, 'Analog In (stereo)'),
     R('out', 'Analog audio', 'Terminal block', 1, 'Analog Monitor Out (stereo)'), R('in', 'GPI', 'Terminal block', 2, 'GPI (speaker mute)'),
     R('io', 'Ethernet', 'RJ45', 1, 'Ethernet / PoE++'), R('in', 'Power', 'DC', 2, 'DC In A/B'), HP],
    '7-inch touchscreen, 16 SDI or 64 MADI channel metering, 30 W speakers. Powered by external 24 V supply (one included) or PoE++. '
    'ST 2110-20/-30 by licence. 19 x 1.75 x 4 in, 1.4 kg.', 'Cobalt ARIA-2 product page', CBU('aria-2'), weightKg=1.4)
add(BF, 'cobalt-wave-rtr-36x36', CB, 'WAVE RTR-36x36', 'WAVE RTR-36x36 12G-SDI / ASI / MADI router, 2RU', 'WAVE', 'router', 2,
    [R('in', '12G-SDI', 'BNC', 36, 'SDI In'), R('out', '12G-SDI', 'BNC', 36, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In'), LAN(1), AC(2)],
    'Check: reference, control and power connectors.', 'Cobalt routers page', 'https://cobaltdigital.com/product-category/routers/', verified=False)
def bbg(pn, name, ports, notes='Check: rear connectors.'):
    add(BF, 'cobalt-' + pn.lower(), CB, pn, name, 'BBG standalone', 'converter', 1, ports + [R('in', 'Power', 'DC', 2, 'DC In (BBG-1000-PS)')],
        'BBG-1000 standalone (third-rack width, mounts in the BBG-1000-TRAY). ' + notes, 'Cobalt standalone products page', CBU(pn.lower()), verified=False, w=4)
bbg('BBG-1002-UDX', 'BBG-1002-UDX standalone 3G converter / frame sync', [SDI('in', 2, 'SDI In'), SDI('out', 4, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 2, 'AES'), LAN(1)])
bbg('BBG-1002-2UDX', 'BBG-1002-2UDX standalone dual 3G converter', [SDI('in', 2, 'SDI In'), SDI('out', 4, 'SDI Out'), LAN(1)])
bbg('BBG-1022-FS', 'BBG-1022-FS standalone 3G frame sync', [SDI('in', 2, 'SDI In'), SDI('out', 4, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 2, 'AES'), LAN(1)])
bbg('BBG-1040-ACO', 'BBG-1040-ACO standalone auto-changeover', [SDI('in', 4, 'SDI In'), SDI('out', 2, 'SDI Out'), LAN(1)])
bbg('BBG-1060-TG2-REF1', 'BBG-1060-TG2-REF1 standalone test generator and sync', [SDI('out', 4, 'Test Out'), R('out', 'Reference', 'BNC', 2, 'Sync Out'), LAN(1)])
bbg('BBG-1070-QS', 'BBG-1070-QS standalone multiviewer', [SDI('in', 5, 'SDI In'), SDI('out', 2, 'MV Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), LAN(1)])
add(BF, 'cobalt-bbg-1000-tray', CB, 'BBG-1000-TRAY', 'BBG-1000-TRAY 1RU tray for three BBG-1000 units', 'BBG standalone', 'shelf', 1, [],
    'Holds three third-width BBG-1000 standalone units.', 'Cobalt standalone products page', CBU('bbg-1000-tray'), verified=False, carrier={'bays': 3, 'fits': ['BBG-1000']})
add(BF, 'cobalt-bbg-1300-fr', CB, 'BBG-1300-FR', 'BBG-1300-FR one-card openGear desktop enclosure (1/3 rack, 1RU)', 'BBG standalone', 'frame', 1,
    [R('in', 'Power', 'DC', 1, 'DC In')], 'Turns one Cobalt card into a standalone unit; three fit the BBG-1300-TRAY. Check: card fit.',
    'Cobalt frames page', CBU('bbg-1300-fr'), verified=False, w=4,
    frame={'system': 'openGear', 'rearGen': 4, 'slots': 1, 'slotOrder': 'ltr', 'rearAlign': 1, 'door': False, 'orient': 'h', 'controller': 'none',
           'front': {'x0': 0.05, 'x1': 0.95, 'y0': 0.1, 'y1': 0.9}, 'rear': {'x0': 0.05, 'x1': 0.95, 'y0': 0.1, 'y1': 0.9}})

# ======================= Chyron =======================
CHF, CH = 'chyron.json', 'Chyron'
add(CHF, 'chyron-prime-engine', CH, 'PRIME rendering engine', 'PRIME graphics rendering engine, 3RU', 'PRIME', 'computer', 3,
    [R('io', 'HD-SDI', 'BNC', 8, 'SDI V/K (in or out)'), R('io', 'SFP', 'SFP', 2, 'ST 2110 (option)'), R('in', 'Reference', 'BNC', 1, 'Genlock'),
     R('in', 'AES/EBU', 'DB25', 1, 'AES In (4)'), R('io', 'GPIO', 'DB37', 1, 'GPI/O 8+8 (option)'), R('out', 'DVI', 'DVI-D', 4, 'Display'),
     R('io', 'Ethernet', 'RJ45', 2, 'LAN'), R('io', 'USB', 'USB-A', 4, 'USB'), AC(2)],
    'Chyron-supplied PRIME engine (Intel W-2265, RTX 5000): up to 8 SDI each set as fill or key and in or out, up to 4+4 ST 2110, 8 NDI, '
    'AES3id x4, optional 16 GPI/O, 800-1000 W redundant PSU. PRIME also runs on customer COTS servers or VMs. Check: connector types.',
    'Chyron PRIME product information sheet (10.2024)', 'https://chyron.com/products/all-in-one-production-systems/live-production-engine/', verified=False, full=True)
add(CHF, 'chyron-hyperx3', CH, 'HyperX3', 'HyperX3 HD/SD character generator (legacy), 4RU', 'HyperX', 'computer', 4,
    [R('out', 'HD-SDI', 'BNC', 4, 'Fill / Key Out (2 ch)'), R('in', 'HD-SDI', 'BNC', 2, 'Video In'), R('in', 'Reference', 'BNC', 2, 'Ref In/Loop'),
     R('io', 'GPI', 'DB25', 1, 'GPI'), R('io', 'RS-422', 'DB9', 1, 'Serial'), R('out', 'DVI', 'DVI-D', 1, 'Display'), R('io', 'Ethernet', 'RJ45', 2, 'LAN'), AC(2)],
    'Legacy Lyric-based CG (HyperX2/X3, Duet and LEX are similar). Check: chassis height and all counts.', 'Chyron HyperX device notes (Ross Vision setup)',
    'https://help.rossvideo.com/acuity-device/Topics/Devices/CG/Chyron-HyperX.html', verified=False, full=True)

# ======================= Tektronix / Telestream =======================
TF, TK = 'telestream-more.json', 'Tektronix'
add(TF, 'tektronix-spg8000a', TK, 'SPG8000A', 'SPG8000A master sync and clock reference generator, 1RU', 'SPG', 'other', 1,
    [R('out', 'Reference', 'BNC', 3, 'Black / Tri-level 1-3'), R('out', 'Reference', 'BNC', 4, 'Black 4-5 / CMPST 1-2 (opt BG)'),
     R('out', '3G-SDI', 'BNC', 4, 'SDI Test Out (opt SDI)'), R('out', 'AES/EBU', 'BNC', 4, 'AES Test Out (opt AG)'), R('out', 'AES/EBU', 'BNC', 1, 'DARS (opt AG)'),
     R('out', 'Word clock', 'BNC', 1, 'Word Clock 48 kHz'), R('io', 'Timecode', 'DB15', 1, 'LTC 1-4 / GPI'), R('in', 'RF', 'BNC', 1, 'GPS Antenna (opt GPS)'),
     R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop'), LAN(1),
     R('io', 'Ethernet', 'RJ45', 1, 'PTP (opt PTP)'), R('io', 'SFP', 'SFP', 1, 'PTP SFP (opt PTP)'), AC(2, 'AC In (2nd: opt DPW)')],
    'Master sync, PTP grandmaster (ST 2059), GPS lock, test signals by option. 559 mm deep, 4.85 kg, 130 VA. Now sold by Telestream.',
    'Tektronix SPG8000A specifications', 'https://www.markertek.com/Attachments/Specifications/Tektronix/SPG8000A-Specifications.pdf', full=True, weightKg=4.85)
add(TF, 'tektronix-spg700', TK, 'SPG700', 'SPG700 multiformat reference sync generator, 1RU', 'SPG', 'other', 1,
    [R('out', 'Reference', 'BNC', 3, 'Black / Tri-level'), R('out', 'Reference', 'BNC', 2, 'Black 4-5 (opt BG)'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out (opt SDI)'),
     R('out', 'AES/EBU', 'BNC', 1, 'DARS / AES (opt)'), R('out', 'Word clock', 'BNC', 1, 'Word Clock'), R('io', 'Timecode', 'DB15', 1, 'LTC / GPI'),
     R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop'), R('in', 'RF', 'BNC', 1, 'GPS (opt)'), LAN(1), AC(2, 'AC In (2nd optional)')],
    'Smaller sibling of the SPG8000A. Check: all counts.', 'Tektronix SPG700 listings', 'https://shop.cnrood.com/spg700', verified=False, full=True)
add(TF, 'tektronix-tg8000', TK, 'TG8000', 'TG8000 multiformat test signal generator platform, 2RU', 'TG', 'other', 2,
    [R('io', 'Other', 'Card slot', 1, 'Generator module rears (SDI, analogue, AES)'), R('out', 'Reference', 'BNC', 3, 'Black'), R('io', 'Timecode', 'DB15', 1, 'LTC / GPI'),
     R('in', 'Reference', 'BNC', 2, 'Genlock In/Loop'), LAN(1), AC(2)],
    'Modular generator with up to 8 module slots (BG7, HDVG7, SDI7, AG7, GPS7...). I/O depends on modules. Check: chassis height.',
    'Tektronix TG8000 listings', 'https://www.tek.com/', verified=False, full=True)
add(TF, 'tektronix-eco422d', TK, 'ECO422D', 'ECO422D automatic changeover for sync generators, 1RU', 'ECO', 'other', 1,
    [R('in', 'Reference', 'BNC', 10, 'Primary In'), R('in', 'Reference', 'BNC', 10, 'Backup In'), R('out', 'Reference', 'BNC', 10, 'Out'),
     R('io', 'Other', 'DB9', 1, 'Remote / alarm'), AC(2)],
    'Changeover for 10 signals (black, SDI, AES, LTC) between two SPGs. ECO8000 / ECO8020 (in telestream.json) replace it. Check: counts.',
    'Tektronix ECO422D listings', 'https://www.tek.com/', verified=False)
def wfm(pn, name, ru, w, ports, notes, url='https://www.tek.com/'):
    add(TF, 'tektronix-' + pn.lower(), TK, pn, name, pn[:3] + pn[3:4] + '000', 'other', ru, ports, notes + ' Check: rear counts.',
        'Tektronix waveform monitor listings', url, verified=False, w=w)
WSDI = lambda t: [R('in', t, 'BNC', 2, 'SDI In A/B'), R('out', t, 'BNC', 2, 'SDI Loop'), R('out', t, 'BNC', 1, 'Pix Mon Out')]
WREST = [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'), R('io', 'GPI', 'DB15', 1, 'Remote / GPI'), LAN(1)]
wfm('WFM8300', 'WFM8300 3G/HD/SD waveform monitor, 3RU half rack', 3, 6, WSDI('3G-SDI') + WREST + [R('in', 'Power', 'IEC C14', 1, 'AC In')], 'Half-rack waveform monitor with 6.5-inch screen; WFM8200 is the 3G-less version. Two fit a WFM7FC dual rack adapter.')
wfm('WFM8200', 'WFM8200 HD/SD waveform monitor, 3RU half rack', 3, 6, WSDI('HD-SDI') + WREST + [R('in', 'Power', 'IEC C14', 1, 'AC In')], 'Half-rack waveform monitor.')
wfm('WVR8200', 'WVR8200 HD/SD waveform rasterizer, 1RU', 1, 12, WSDI('HD-SDI') + [R('out', 'DVI', 'DVI-I', 1, 'XGA/DVI Out')] + WREST + [AC()], 'Rasterizer version of the WFM8200.')
wfm('WFM7200', 'WFM7200 multi-format waveform monitor, 3RU half rack', 3, 6, WSDI('3G-SDI') + WREST + [R('in', 'Power', 'IEC C14', 1, 'AC In')], 'Legacy half-rack monitor.')
wfm('WVR7200', 'WVR7200 multi-format waveform rasterizer, 1RU', 1, 12, WSDI('3G-SDI') + [R('out', 'DVI', 'DVI-I', 1, 'XGA/DVI Out')] + WREST + [AC()], 'Legacy rasterizer.')
wfm('WFM5200', 'WFM5200 compact waveform monitor, half rack', 3, 6, WSDI('3G-SDI') + WREST + [R('in', 'Power', 'XLR4M', 1, '12V DC')], 'Compact half-rack monitor with a 6.5-inch screen; WFM5000 is the earlier one.')
wfm('WVR5200', 'WVR5200 compact waveform rasterizer, 1RU half rack', 1, 6, WSDI('3G-SDI') + [R('out', 'DVI', 'DVI-I', 1, 'DVI Out')] + WREST + [R('in', 'Power', 'XLR4M', 1, '12V DC')], 'Compact rasterizer.')
wfm('WFM2300', 'WFM2300 portable waveform monitor (rack adapter)', 3, 6, WSDI('3G-SDI') + [R('in', 'Reference', 'BNC', 1, 'Ref'), R('in', 'Power', 'XLR4M', 1, 'DC In')], 'Portable; rack-mounts with a half-rack adapter.')
add(TF, 'telestream-prism-mpx2', 'Telestream', 'MPX2', 'PRISM MPX2 IP/SDI waveform monitor platform, 1RU', 'PRISM', 'other', 1,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), R('io', 'SFP', 'SFP28', 2, '25GE IP'), R('out', 'DisplayPort', 'DisplayPort', 2, 'Display'),
     R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'Ethernet', 'RJ45', 2, 'Mgmt / PTP'), R('io', 'USB', 'USB-A', 2, 'USB'), AC(2)],
    'PRISM rasterizer for ST 2110 / 2022-6 and 12G-SDI; MPI2 is the IP-only version. Check: all counts.', 'Telestream PRISM product sheet', 'https://www.telestream.com/prism/', verified=False)
add(TF, 'telestream-prism-mpi2', 'Telestream', 'MPI2', 'PRISM MPI2 IP waveform monitor platform, 1RU', 'PRISM', 'other', 1,
    [R('io', 'SFP', 'SFP28', 2, '25GE IP'), R('out', 'DisplayPort', 'DisplayPort', 2, 'Display'), R('in', 'Reference', 'BNC', 1, 'Ref In'),
     R('io', 'Ethernet', 'RJ45', 2, 'Mgmt / PTP'), R('io', 'USB', 'USB-A', 2, 'USB'), AC(2)],
    'IP-only PRISM. Check: all counts.', 'Telestream PRISM product sheet', 'https://www.telestream.com/prism/', verified=False)

# ======================= Leader / PHABRIX =======================
LF, LD = 'leader-more.json', 'Leader'
LU = lambda s: 'https://leaderphabrix.com/products/' + s + '/'
LS = 'LeaderPhabrix product page (2025)'
add(LF, 'leader-lv7600w', LD, 'LV7600W', 'LV7600W 12G-SDI / IP rasterizer, 1RU', 'ZEN', 'other', 1,
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In (SER01)'), R('out', '12G-SDI', 'BNC', 4, 'SDI Out'), R('io', 'SFP', 'SFP28', 2, 'IP1 / IP2 (SER06)'),
     R('in', 'Reference', 'BNC', 1, 'Ext Ref'), R('out', 'HDMI', 'HDMI', 1, 'Monitor Out'), R('out', 'DisplayPort', 'DisplayPort', 1, 'Monitor Out'), LAN(1), AC(1)],
    'Rasterizer version of the LV5600W. Check: monitor output and power connectors (page lists SDI and IP only).', LS, LU('lv7600w-rasterizer'), verified=False)
add(LF, 'leader-lv7300', LD, 'LV7300', 'LV7300 multi-SDI rasterizer, 1RU', 'LV7300', 'other', 1,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'),
     R('out', 'DVI', 'DVI-D', 1, 'Display Out'), LAN(1), AC(1)], 'Check: all counts.', LS, LU('lv7300-rasterizer'), verified=False)
add(LF, 'leader-lv5300a', LD, 'LV5300A', 'LV5300A multi-SDI waveform monitor, 3U half rack', 'LV5300', 'other', 3,
    [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'), LAN(1), R('in', 'Power', 'XLR4M', 1, '10-18V DC')],
    'Half-rack monitor with screen (eye pattern on ch 1); LV5350 in leader.json is the newer version. Check: counts.', LS, LU('lv5300a-waveform-monitor'), verified=False, w=6)
add(LF, 'leader-lv5900a', LD, 'LV5900A', 'LV5900A 12G-SDI / IP waveform monitor (LR2490 rack adapter)', 'LV5900', 'other', 4,
    [R('io', '12G-SDI', 'BNC', 8, 'SDI In/Out'), R('out', '12G-SDI', 'BNC', 1, 'Monitor SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'TMDS Out'),
     R('in', 'MADI audio', 'BNC', 1, 'MADI'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'), R('io', 'Other', 'DB15', 1, 'Remote'), LAN(1), AC(1)],
    'Benchtop unit (223 x 172 x 360 mm); rack-mounts with the LR2490 adapter. Check: rack height and counts.', LS, LU('lv5900a-waveform-monitor'), verified=False, w=6)
add(LF, 'leader-lt4448', LD, 'LT4448', 'LT4448 sync changeover, 1RU', 'SPG', 'other', 1,
    [R('in', 'Reference', 'BNC', 11, 'Primary In'), R('in', 'Reference', 'BNC', 11, 'Backup In'), R('out', 'Reference', 'BNC', 11, 'Out'),
     R('in', 'Timecode', 'XLR3F', 6, 'LTC In (3 x 2)'), R('out', 'Timecode', 'XLR3M', 9, 'LTC Out (3 x 3)'), R('io', 'Other', 'DB15', 1, 'Remote / alarm'), LAN(1), AC(2)],
    '11 channels (primary, backup, output) plus 3 LTC systems; redundant PSU option. Check: connector types.', LS, LU('lt4448-changeover'), verified=False)
add(LF, 'leader-lvb440', LD, 'LVB440', 'LVB440 ST 2110 / 2022 IP analyser, 1RU', 'IP', 'other', 1,
    [R('io', 'SFP', 'QSFP28', 2, '100GE IP'), R('io', 'SFP', 'SFP28', 2, '25GE IP'), R('in', 'Reference', 'BNC', 1, 'Ref / PPS'), LAN(2), AC(2)],
    'Server-based IP analyser and rasterizer. Check: all counts.', LS, LU('lvb440-ip-analyser'), verified=False, full=True)
add(LF, 'phabrix-qx', 'PHABRIX', 'PHQX', 'Qx 12G-SDI / IP rasterizer, 1U half rack', 'Qx', 'other', 1,
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Gen/Thru Out'), R('in', '12G-SDI', 'BNC', 1, 'SDI Eye In'),
     R('io', 'SFP', 'SFP+', 2, '10GE IP'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'), R('out', 'HDMI', 'HDMI', 1, 'Instrument Out'), LAN(1), R('in', 'Power', 'XLR4M', 1, '10-18V DC')],
    '10G version of the QxL (leader.json). Check: counts.', LS, LU('qx'), verified=False, w=6)
add(LF, 'phabrix-rx2000', 'PHABRIX', 'Rx2000', 'Rx2000 rasterizer, 1RU', 'Rx', 'other', 1,
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Gen Out'), R('in', 'Reference', 'BNC', 1, 'Ext Ref'),
     R('out', 'DVI', 'DVI-D', 1, 'Display'), LAN(1), AC(1)], 'Rx series rasterizer (Rx500 / Rx1000 / Rx2000). Check: counts.', LS, 'https://leaderphabrix.com/rx-series/', verified=False)

# ======================= write =======================
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
allids = set()
for f in idx:
    if f in FILES: continue
    try: allids |= {m['id'] for m in json.load(open(os.path.join(CAT, f)))}
    except Exception: pass
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    dup = allids & set(ids)
    if dup: print('  skipped, already in another file:', sorted(dup)); ms[:] = [m for m in ms if m['id'] not in dup]
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    print(f, len(ms))
idx = json.load(open(ip))  # re-read just before appending
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
