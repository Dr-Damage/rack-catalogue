#!/usr/bin/env python3
"""Generates the modular frame and card catalogue files:
  catalogue/frames-opengear.json  openGear frames (non-Ross) and openGear cards (Blackmagic, Ross, AJA, Cobalt)
  catalogue/evertz-frames.json    Evertz 7800FR / 7800FR-QT / 7801FR / 570FR frames and 7700/7800 cards
  catalogue/gv-densite.json       Grass Valley Densite 3 / 3+ FR4 / 3+ FR1 frames and Densite cards
  catalogue/evs-synapse.json      EVS Synapse (ex Axon) SFR18 / SFR08 / SFR04 frames and Synapse cards
Schema: catalogue/FRAMES.md. The Ross OGX-FR and OG3-FR frames live in ross.json (tools/ross.py).
verified=True only where the ports come from the maker's manual, spec sheet or product page.
Notes start any doubt with "Check:"."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
CAT = os.path.join(HERE, '..', 'catalogue')

def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)

def frame(brand, id, mfr, pn, name, fam, ru, ports, fr, notes, src, url, verified=True, **kw):
    m = dict(id=f'{brand}-{id}', manufacturer=mfr, partNumber=pn, name=name, family=fam, category='frame',
             ru=ru, widthCols=12, fullDepth=True, verified=verified, source=src, productUrl=url, notes=notes,
             portGroups=ports, frame=fr)
    m.update(kw); return m

def card(brand, id, mfr, pn, name, fam, fits, rms, notes, src, url, verified=True, slotWidth=1, watts=None,
         edge=None, color=None, onlySlots=None, gen=None, **kw):
    c = dict(fits=fits, slotWidth=slotWidth)
    if watts: c['watts'] = watts
    if color: c['color'] = color
    if onlySlots: c['onlySlots'] = onlySlots
    if gen: c['gen'] = gen
    m = dict(id=f'{brand}-{id}', manufacturer=mfr, partNumber=pn, name=name, family=fam, category='card',
             ru=0, widthCols=0, fullDepth=False, verified=verified, source=src, productUrl=url, notes=notes,
             portGroups=edge or [], card=c, rearModules=rms)
    m.update(kw); return m

def rm(pn, name, width, ports, cpm=1, offset=0, default=False, cols=None, rows=None, gen=None, rm_notes=None):
    r = dict(partNumber=pn, name=name, width=width, cardsPerModule=cpm, cardOffset=offset, default=default, portGroups=ports)
    if cols or rows: r['layout'] = {k: v for k, v in (('cols', cols), ('rows', rows)) if v}
    if gen: r['gen'] = gen
    if rm_notes: r['notes'] = rm_notes
    return r

# =====================================================================================
# openGear
# =====================================================================================
OG = []
AJA_FR = 'https://www.aja.com/products/og-x-fr'
OG.append(frame('aja', 'og-x-fr', 'AJA Video Systems', 'OG-X-FR', 'openGear OG-X-FR 20-slot frame', 'openGear frames', 2,
    [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('in', 'Reference', 'BNC', 2, 'REF'), R('out', 'Reference', 'BNC', 2, 'REF Loop'),
     R('in', 'Power', 'IEC C14', 2, 'PS')],
    dict(system='openGear', rearGen=4, slots=20, slotOrder='ltr', rearAlign=2, door=True,
         controller='GFC-8322 frame controller in a dedicated slot; network card per frame option',
         front=dict(x0=0.10, x1=0.98, y0=0.05, y1=0.95), rear=dict(x0=0.02, x1=0.82, y0=0.05, y1=0.95)),
    'AJA-branded Ross OGX-FR: 2RU openGear frame, 20 card slots, two front-loading OG-X-PS supplies (500 W card power), '
    'two looping reference inputs (black burst, tri-level or AES DARS), fans in the front door. 483 x 427 x 90 mm, 9.1 kg with two PSUs. '
    'Rear modules cover two slots: full rear module = 1 card, split = 2 cards, double-wide = 4 slots. '
    'Check: rear position of the Ethernet, REF and power inlets (drawing fractions are estimates).',
    'AJA OG-X-FR spec sheet', AJA_FR))

# ---- Blackmagic openGear converters (BlackmagicOpenGearManual.pdf, pp. 9-18) ----
BMD_SRC = 'Blackmagic OpenGear Converters manual (connection diagrams pp. 9-18); part numbers from dealer listings'
BMD_URL = 'https://www.blackmagicdesign.com/products/openGearconverters'
BMD_NOTE = ('Blackmagic rear module supplied with the card. Fits 20-card 2RU openGear frames (OG3-FR, OGX-FR, DFR-8321). '
            'Check: rear module width assumed to be a full (2-slot) module, and port order on the module.')
def bmd(id, pn, name, ports, notes, edge=None):
    OG.append(card('bmdog', id, 'Blackmagic Design', pn, 'OpenGear Converter ' + name, 'Blackmagic OpenGear Converters',
                   ['openGear'], [rm(pn + ' rear', 'Blackmagic rear module', 2, ports, default=True, cols=2, rows=5, gen=2)],
                   notes + ' ' + BMD_NOTE, BMD_SRC, BMD_URL, edge=edge, gen=2))
USB = R('io', 'USB', 'USB mini-B', 1, 'USB')
bmd('sdi-analog', 'CONVOPENGASA', 'SDI to Analog',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', '3G-SDI', 'BNC', 1, 'SDI In Alt'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'),
     R('out', 'Analog video', 'BNC', 1, 'Y/Comp Out'), R('out', 'Analog video', 'BNC', 1, 'B-Y/Y Out'), R('out', 'Analog video', 'BNC', 1, 'R-Y/C Out'),
     R('out', 'Analog audio', 'XLR 3-pin', 1, 'Audio L/AES 1-2 Out'), R('out', 'Analog audio', 'XLR 3-pin', 1, 'Audio R Out'), USB],
    'HD/SD-SDI to analog component, NTSC or PAL with redundant SDI input and loop. Analog or AES/EBU audio out.')
bmd('analog-sdi', 'CONVOPENGAAS', 'Analog to SDI',
    [R('in', 'Analog video', 'BNC', 1, 'Y/Comp In'), R('in', 'Analog video', 'BNC', 1, 'B-Y In'), R('in', 'Analog video', 'BNC', 1, 'R-Y In'),
     R('out', '3G-SDI', 'BNC', 2, 'SDI Out'),
     R('in', 'Analog audio', 'XLR 3-pin', 1, 'Audio L/AES 1-2 In'), R('in', 'Analog audio', 'XLR 3-pin', 1, 'Audio R In'), USB],
    'Analog component/composite to HD/SD-SDI with analog or AES/EBU audio embedding.')
bmd('sdi-hdmi', 'CONVOPENGBSH', 'SDI to HDMI',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), USB],
    'SDI to HDMI with embedded HDMI audio. Connectors are integrated with the card.')
bmd('hdmi-sdi', 'CONVOPENGBHS', 'HDMI to SDI',
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'), USB],
    'HDMI (non copy protected) to SDI, both SDI outs carry the same signal.')
bmd('sdi-audio', 'CONVOPENGCSAUD', 'SDI to Audio',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', '3G-SDI', 'BNC', 1, 'SDI In Alt'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'),
     R('out', 'Analog audio', 'XLR 3-pin', 4, 'Audio/AES Out'), USB],
    'De-embeds 4 ch analog or 8 ch AES/EBU (4 pairs) from SDI.')
bmd('audio-sdi', 'CONVOPENGCAUDS', 'Audio to SDI',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('in', '3G-SDI', 'BNC', 1, 'SDI In Alt'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
     R('in', 'Analog audio', 'XLR 3-pin', 4, 'Audio/AES In'), USB],
    'Embeds 4 ch analog or 8 ch AES/EBU (4 pairs) into SDI.')
bmd('optical-fiber', 'CONVOPENGOF', 'Optical Fiber',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out')],
    'SDI to fibre and fibre to SDI, two independent directions. The LC fibre port is on a removable SFP at the card edge.',
    edge=[F('io', 'Fibre', 'LC (SFP)', 1, 'Fibre')])
bmd('sync-gen', 'CONVOPENGSYNC', 'Sync Generator',
    [R('out', 'Reference', 'BNC', 10, 'Ref Out'), USB],
    'Sync generator with 10 reference outputs (black burst / tri-level).')
bmd('udc', 'CONVOPENGUDC', 'UpDownCross',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('in', 'Reference', 'BNC', 1, 'Sync In'),
     R('out', '3G-SDI', 'BNC', 7, 'SDI Out'), USB],
    'Up, down and cross converter with 7 SDI outs. Check: the loop is passive (listed as "Passive Loop").')
bmd('sdi-da', 'CONVOPENGSDIDA', 'SDI Distribution',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 9, 'SDI Out')],
    '1 x 9 reclocking SDI distribution amplifier. No USB port.')

# ---- Ross openGear ----
ROSS_SRA = 'https://www.rossvideo.com/infrastructure/opengear-modular/distribution/sra-8901'
OG.append(card('ross', 'sra-8901-10', 'Ross Video', 'SRA-8901-10', 'SRA-8901-10 12G-SDI DA 1x10', 'openGear distribution', ['openGear'],
    [rm('R3-8901-10', 'Full rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 10, 'SDI Out')],
        default=True, cols=2, gen=3)],
    '12G/6G/3G/HD/SD/MADI reclocking DA, 1 in, 10 non-inverting outs. Sold as SRA-8901-10-R3 with the full rear module.',
    'Ross SRA-8901 product page', ROSS_SRA, gen=3))
OG.append(card('ross', 'sra-8901-4', 'Ross Video', 'SRA-8901-4', 'SRA-8901-4 12G-SDI DA 1x4', 'openGear distribution', ['openGear'],
    [rm('R3S-8901-4', 'Split rear module (2 cards)', 2, [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 4, 'SDI Out')],
        cpm=2, default=True, cols=1, rows=5, gen=3)],
    '12G/6G/3G/HD/SD/MADI reclocking DA, 1 in, 4 outs. Sold as SRA-8901-4-R3S: the split rear module serves this card and a second SRA-8901-4 in the next slot.',
    'Ross SRA-8901 product page', ROSS_SRA, gen=3))

# ---- more Ross openGear (Ross product pages and cut sheets, dealer listings) ----
RCS = 'https://documentation.rossvideo.com/files/Cut%20Sheets/Infrastructure/'
RDIST = 'https://www.rossvideo.com/infrastructure/opengear-modular/all'
def ross(id, pn, name, fam, rms, notes, src, url=RDIST, verified=True, gen=None, **kw):
    OG.append(card('ross', id, 'Ross Video', pn, name, fam, ['openGear'], rms, notes, src, url, verified=verified, gen=gen, **kw))
for n in (10, 16):
    ross(f'dra-8902-{n}', f'DRA-8902-{n}', f'DRA-8902-{n} dual 12G-SDI DA 2x{n}', 'openGear distribution',
        [rm(f'R3-8902-{n}', 'Full rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', n, 'SDI Out')], default=True, cols=2, gen=3)],
        f'Dual 12G/6G/3G/HD/SD/MADI reclocking DA, 2 in, {n} outs assignable to either input, or one DA with main/standby auto-failover. '
        'HD-BNC. OG3-FR and OGX-FR only. Sold as ' + f'DRA-8902-{n}-R3.', 'Ross 8900 Series cut sheet; DRA-8902-10-R3 dealer listing', gen=3)
ross('qra-8808', 'QRA-8808', 'QRA-8808 quad 3G reclocking DA', 'openGear distribution',
    [rm('R2H', 'High-density rear module (HD-BNC)', 2, [R('in', '3G-SDI', 'HD-BNC', 4, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', 14, 'SDI Out')], default=True, cols=2)],
    'Four DAs on one card: channels 1-2 are 1x4, channels 3-4 are 1x3 (18 HD-BNCs). Out 1-4 = ch 1, 5-8 = ch 2, 9-11 = ch 3, 12-14 = ch 4. '
    'Check: output numbering per channel.', 'Ross QRA-8808 product page', 'https://www.rossvideo.com/infrastructure/opengear-modular/distribution/qra-8808/')
ross('dra-8804', 'DRA-8804', 'DRA-8804 dual 3G reclocking DA', 'openGear distribution',
    [rm('R2', 'Standard 10 BNC rear module', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')], default=True, cols=2, rows=5),
     rm('R2H', 'HD-BNC rear module', 2, [R('in', '3G-SDI', 'HD-BNC', 2, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', 16, 'SDI Out')], cols=2)],
    'Dual 3G reclocking DA: dual 1x4 with -R2, dual 1x8 with -R2H, or a single 1x16 with A/B input failover.',
    'Ross DRA-8804 product page', 'https://www.rossvideo.com/infrastructure/opengear-modular/distribution/dra-8804/')
UDC_BASE = lambda c: [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'), R('in', 'Reference', 'BNC', 1, 'Ref In')]
ross('udc-8625a', 'UDC-8625A', 'UDC-8625A 3G/HD/SD up/down/cross converter', 'openGear conversion',
    [rm('R2H', 'HD-BNC audio rear module (UDC-8625A-A)', 2, UDC_BASE('HD-BNC') + [R('io', 'AES/EBU', 'HD-BNC', 8, 'AES I/O')], default=True, cols=2),
     rm('R2D', 'DIN audio rear module (UDC-8625A-A)', 2, UDC_BASE('DIN') + [R('io', 'AES/EBU', 'DIN 1.0/2.3', 8, 'AES I/O')], cols=2),
     rm('R2B', '110 ohm audio rear module (UDC-8625A-B)', 2, UDC_BASE('BNC') + [R('io', 'AES/EBU', 'Terminal', 8, 'AES I/O')], cols=2)],
    'Multi-function 3G/HD/SD format converter with frame sync, ARC, keyer and logo inserter. SDI In 1-2 have full frame sync. '
    'The 8 AES ports are set as 8 in, 4 in/4 out or 8 out (needs the audio daughter card). -A card = 75 ohm (R2H/R2D), -B card = 110 ohm (R2B). '
    'The card also has 4 GPI/O, an RS-232/485 port and 10/100 Ethernet. Check: which of these are on the rear module and their connectors.',
    'Ross UDC-8625A-A and UDC-8625A-B cut sheets', RCS + 'UDC-8625A-A.pdf')
for v, ohm, con, rmn in [('A', '75 ohm', 'BNC', 'R2A'), ('B', '110 ohm', 'WECO', 'R2B')]:
    ross(f'mux-8258-{v.lower()}', f'MUX-8258-{v}', f'MUX-8258-{v} 8 ch AES embedder ({ohm})', 'openGear audio',
        [rm(rmn, f'Rear module, {ohm}', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'AES/EBU', con, 8, 'AES In')], default=True, cols=2, rows=5)],
        f'Embeds 8 AES/EBU inputs ({ohm}) into HD/SD-SDI.' + (' Check: WECO vs BNC split on the R2B module.' if v == 'B' else ''),
        'MUX-8258 dealer listings (10-BNC rear module: 1 SDI in, 1 SDI out, 8 AES in)', verified=(v == 'A'))
    ross(f'dmx-8259-{v.lower()}', f'DMX-8259-{v}', f'DMX-8259-{v} 8 ch AES de-embedder ({ohm})', 'openGear audio',
        [rm(rmn, f'Rear module, {ohm}', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'AES/EBU', con, 8, 'AES Out')], default=True, cols=2, rows=5)],
        f'De-embeds 8 AES/EBU outputs ({ohm}) from 3G/HD/SD-SDI. Check: SDI in/out count on the 10-connector module (assumed 1 in, 1 out like MUX-8258).',
        'DMX-8259 dealer listings', verified=False)
ross('ada-8402-a', 'ADA-8402-A', 'ADA-8402-A AES/EBU DA (75 ohm)', 'openGear audio',
    [rm('R2AS', 'Split rear module (2 cards)', 2, [R('in', 'AES/EBU', 'BNC', 1, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out')], cpm=2, default=True, cols=1, rows=5),
     rm('R2A', 'Full rear module', 2, [R('in', 'AES/EBU', 'BNC', 1, 'AES In'), R('out', 'AES/EBU', 'BNC', 8, 'AES Out')], cols=2, rows=5)],
    'Reclocking AES-3id DA: 1 in, 4 outs with the split module or 8 with the full module. 2 W. Check: R2A full module part number (listings name R2B for the 110 ohm card).',
    'ADA-8402 dealer listings', verified=False)
ross('ada-8402-b', 'ADA-8402-B', 'ADA-8402-B AES/EBU DA (110 ohm)', 'openGear audio',
    [rm('R2B', 'Standard rear module, 110 ohm', 2, [R('in', 'AES/EBU', 'WECO', 1, 'AES In'), R('out', 'AES/EBU', 'WECO', 8, 'AES Out')], default=True, cols=2, rows=5),
     rm('R2BS', 'Split rear module, 110 ohm (2 cards)', 2, [R('in', 'AES/EBU', 'WECO', 1, 'AES In'), R('out', 'AES/EBU', 'WECO', 4, 'AES Out')], cpm=2, cols=1, rows=5)],
    'Reclocking balanced AES3 DA: 1 in, 8 outs with the full module or 4 with the split module. Check: connector type (WECO terminal assumed).',
    'ADA-8402-B-R2B dealer listing', verified=False)
ross('spg-8260', 'SPG-8260', 'SPG-8260 sync pulse generator', 'openGear sync',
    [rm('R2-8260', 'Full rear module', 2, [R('out', 'Reference', 'BNC', 8, 'Ref Out'), R('io', 'Reference', 'BNC', 1, 'Ext Ref In / AES Ref Out'), R('out', 'AES/EBU', 'BNC', 1, 'AES Out')],
        default=True, cols=2, rows=5),
     rm('R2S-8260', 'Split rear module (2 cards)', 2, [R('out', 'Reference', 'BNC', 4, 'Ref Out'), R('io', 'Reference', 'BNC', 1, 'Ext Ref In / AES Ref Out')], cpm=2, cols=1, rows=5)],
    'Sync generator: output pairs 1A-4A / 1B-4B each set to tri-level, black burst or colour bars; 48 kHz AES reference and AES tone. Locks to frame REF 1/2, its own ref input or internal. '
    'SPG-8260-W adds word clock. Check: which outputs the split module keeps.', 'Ross SPG-8260 cut sheet', RCS + 'SPG-8260.pdf')
ross('shc-8932-f', 'SHC-8932-F', 'SHC-8932-F dual 12G-SDI/fibre to HDMI converter', 'openGear conversion',
    [rm('R3F-8932', 'Full rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 2, 'SDI Out'),
        R('in', 'SFP', 'SFP (dual Rx)', 2, 'Fibre In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI Out')], default=True, gen=3)],
    'Low-latency dual UHD SDI or fibre to HDMI converter. Check: SDI connector type (HD-BNC assumed).', 'R3F-8932 dealer listing', verified=False, gen=3)
ross('amx-8952', 'AMX-8952', 'AMX-8952 12G embedder/de-embedder, frame sync', 'openGear audio',
    [rm('R3C-8952', 'Rear module, analog audio', 2, [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 2, 'SDI Out'),
        R('io', 'Analog audio', 'Terminal block', 8, 'Analog Audio')], default=True, gen=3)],
    '4K UHD 12G-SDI audio embedder/de-embedder and frame synchroniser. -C version: 8 balanced analog channels on a pluggable terminal block. -B version uses R3B-8952. '
    'Check: SDI in/out split of the 3 HD-BNCs, and analog in/out split.', 'R3C-8952 dealer listing', verified=False, gen=3)
ross('dac-8418-a', 'DAC-8418-A', 'DAC-8418-A dual AES to quad analog audio', 'openGear audio',
    [rm('R2A', 'Rear module', 2, [R('in', 'AES/EBU', 'BNC', 2, 'AES In'), R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out')], default=True)],
    'Converts 2 unbalanced AES inputs to 4 balanced analog outputs. Check: connector types.', 'DAC-8418-A-R2A dealer listing', verified=False)
ross('hdc-8223', 'HDC-8223', 'HDC-8223 HD monitoring down converter and DA', 'openGear conversion',
    [rm('R2', '10 BNC rear module', 2, [R('in', 'HD-SDI', 'BNC', 2, 'SDI In'), R('out', 'HD-SDI', 'BNC', 4, 'Out (SDI/composite)'), R('out', 'Analog audio', 'BNC', 1, 'Audio Out')],
        default=True, cols=2, rows=5)],
    '2 in (manual or auto failover), 4 outs each set to SDI or analog composite with HD down conversion, optional analog audio out. '
    'Check: connector allocation on the 10 BNC module.', 'HDC-8223-R2 dealer listing', verified=False)

# ---- AJA openGear ----
OG.append(card('aja', 'og-3gda-2x4', 'AJA Video Systems', 'OG-3GDA-2x4', 'OG-3GDA-2x4 3G-SDI DA (2x4 or 1x8)', 'AJA openGear', ['openGear'],
    [rm('OG-3GDA-2x4 rear', '10 BNC rear module', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')],
        default=True, cols=2, rows=5)],
    'Reclocking 3G-SDI DA, two 1x4 DAs (In 1 to Out 1-4, In 2 to Out 5-8) or one 1x8 (In 2 unused). Two slots per card, 10 BNC rear module included. '
    'Check: AJA spec table says 2 outs per DA while the overview says 4; drawn as 8 outs total.',
    'AJA OG-3GDA-2x4 specifications', 'https://www.aja.com/products/og-3gda-2x4', verified=False))
FIDO = 'https://www.aja.com/products/og-fido'
for sfx, desc, ports in [
        ('TR', 'single-mode transceiver', [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')]),
        ('T', 'single-mode transmitter', [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop Out'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')]),
        ('R', 'single-mode receiver', [R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')]),
        ('2T', 'dual single-mode transmitter', [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', 'Fibre', 'LC', 2, 'Fibre Out')]),
        ('2R', 'dual single-mode receiver', [R('in', 'Fibre', 'LC', 2, 'Fibre In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')])]:
    OG.append(card('aja', f'og-fido-{sfx.lower()}', 'AJA Video Systems', f'OG-FiDO-{sfx}', f'OG-FiDO-{sfx} 3G-SDI fibre {desc}', 'AJA openGear', ['openGear'],
        [rm(f'OG-FiDO-{sfx} rear', 'Rear module', 2, ports, default=True, cols=1)],
        f'3G-SDI/fibre {desc}, LC connectors. Occupies two frame slots. -MM multimode versions have the same connectors.'
        + (' Out 2 on R models is inverting (not DVB-ASI compatible).' if 'R' in sfx and sfx != 'TR' else ''),
        'AJA OG-FiDO Series manual v2.0.2', FIDO))

# ---- AJA openGear range (aja.com/family/opengear-infrastructure, spec sheets at aja.com/products/<model>/spec-sheet.pdf) ----
# AJA: "two slots required for each card" (front card plus rear module covering two frame slots); 40 FiDO-4 channels per
# 20-slot frame confirms 10 cards per frame. Frame reference comes over the backplane (no reference BNC on the modules).
def aja(slug, pn, name, ports, notes, watts=None, verified=True, cols=2, rows=None, src=None, url=None):
    OG.append(card('aja', slug, 'AJA Video Systems', pn, name, 'AJA openGear', ['openGear'],
        [rm(f'{pn} rear', f'{sum(p["count"] for p in ports)}-connector rear module', 2, ports, default=True, cols=cols, rows=rows)],
        notes, src or f'AJA {pn} spec sheet', url or f'https://www.aja.com/products/{slug}', verified=verified, watts=watts))
ATB = lambda d, n=2, p='Audio': R(d, 'Analog audio', 'Terminal block', n, p)
aja('og-3gda-1x9', 'OG-3GDA-1x9', 'OG-3GDA-1x9 3G-SDI reclocking DA (1x9)',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 9, 'SDI Out')],
    'Reclocking 3G-SDI DA, one input to nine outputs, 10 BNC rear module. 5 of the 9 outputs are noninverting.', 2.5, rows=5)
aja('og-12gda-2x4', 'OG-12GDA-2x4', 'OG-12GDA-2x4 12G-SDI reclocking DA (2x4 or 1x8)',
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 8, 'SDI Out')],
    'Reclocking 12G-SDI DA, two 1x4 or one 1x8, 10 BNC rear module, noninverting outputs.', 4.5, rows=5)
aja('og-gen10', 'OG-GEN10', 'OG-GEN10 sync generator',
    [R('out', 'Reference', 'BNC', 9, 'Sync Out'), R('out', 'AES/EBU', 'BNC', 1, 'AES-11 Out')],
    'SD/HD sync generator: 9 analog sync outputs in two independently set groups (black burst, 75% bars or tri-level, 19 HD formats), '
    'plus one AES-11 48 kHz output (silence or 1 kHz tone).', 6.75, rows=5)
aja('og-c10da', 'OG-C10DA', 'OG-C10DA analog video/reference DA',
    [R('in', 'Analog video', 'BNC', 1, 'Video In'), R('out', 'Analog video', 'BNC', 1, 'Loop Out'), R('out', 'Analog video', 'BNC', 8, 'Out')],
    'Analog video and reference DA: differential input with active or passive loop, 8 outputs.', 6.75, rows=5)
aja('og-12gm', 'OG-12GM', 'OG-12GM 12G-SDI multiplexer / demultiplexer',
    [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', '12G-SDI', 'BNC', 4, 'SDI Out')],
    'Converts between single-link 12G, dual 6G, quad 3G and dual 3G; each BNC accepts any of those configurations.', 13, rows=4)
aja('og-12g-am', 'OG-12G-AM', 'OG-12G-AM 12G-SDI AES embedder/disembedder',
    [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), R('io', 'AES/EBU', 'BNC', 8, 'AES')],
    '16 channels of AES audio in or out, set in pairs on 8 BNC connectors.', 6, rows=5)
aja('og-12g-ama', 'OG-12G-AMA', 'OG-12G-AMA 12G-SDI analog audio embedder/disembedder',
    [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), ATB('io', 8, 'Audio Ch')],
    '8 balanced analog audio channels on 3-pin terminal blocks, each pair set as input or output.', 8)
aja('og-3g-ama', 'OG-3G-AMA', 'OG-3G-AMA 3G-SDI analog audio embedder/disembedder',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), ATB('io', 8, 'Audio Ch')],
    '8 balanced analog audio channels on 3-pin terminal blocks, each pair set as input or output.', 5)
aja('og-3g-amd', 'OG-3G-AMD', 'OG-3G-AMD 3G-SDI AES embedder/disembedder',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out')],
    'AES3id embedder and disembedder, 10 BNC rear module.', 5, rows=5)
for sfx, fib, desc in [('', [], ''), ('-R', [R('in', 'Fibre', 'LC', 1, 'Fibre In')], ' with single-mode LC fibre receiver'),
                       ('-TR', [R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')], ' with single-mode LC fibre transceiver'),
                       ('-R-ST', [R('in', 'Fibre', 'ST', 1, 'Fibre In')], ' with single-mode ST fibre receiver')]:
    aja(f'og-hi5-12g{sfx.lower()}', f'OG-Hi5-12G{sfx}', f'OG-Hi5-12G{sfx} 12G-SDI to HDMI 2.0 converter{desc}',
        [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Loop Out')] + fib + [R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), ATB('out')],
        '12G-SDI to HDMI 2.0b (DVI fallback without audio), 2-channel balanced analog audio out. '
        'Check: the reclocked SDI loop-out is in the overview but not the spec table.', 13, verified=False,
        src='AJA OG-Hi5-12G spec sheet (covers -R, -TR, -R-ST)')
for sfx, fib, desc in [('', [], ''), ('-T', [R('out', 'Fibre', 'LC', 1, 'Fibre Out')], ' with single-mode LC fibre transmitter'),
                       ('-T-ST', [R('out', 'Fibre', 'ST', 1, 'Fibre Out')], ' with single-mode ST fibre transmitter')]:
    aja(f'og-ha5-12g{sfx.lower()}', f'OG-HA5-12G{sfx}', f'OG-HA5-12G{sfx} HDMI 2.0 to 12G-SDI converter{desc}',
        [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), ATB('in'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out')] + fib,
        'HDMI 2.0b to 12G-SDI with 2-channel balanced analog audio in. '
        'Check: the overview mentions two 12G-SDI outputs, the spec table lists one.', 14, verified=False,
        src='AJA OG-HA5-12G spec sheet (covers -T, -T-ST)')
aja('og-hi5-4k-plus', 'OG-Hi5-4K-Plus', 'OG-Hi5-4K-Plus quad 3G-SDI to HDMI 2.0 converter',
    [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out')],
    'Quad-link 3G-SDI (4K/UHD) to HDMI 2.0b, embedded audio to HDMI.', 12)
aja('og-ha5-4k', 'OG-HA5-4K', 'OG-HA5-4K HDMI 2.0 to quad 3G-SDI converter',
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')],
    'HDMI 2.0b to quad-link 3G-SDI (4K/UHD), 8-channel embedded audio.', 10)
aja('og-roi-hdmi', 'OG-ROI-HDMI', 'OG-ROI-HDMI HDMI to SDI scan converter',
    [R('in', 'HDMI', 'HDMI', 1, 'HDMI In'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Loop'), ATB('in'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out')],
    'Region-of-interest scan converter for computer or video HDMI, with HDMI loop-through and 2-channel analog audio in. Locks to frame reference.', 8)
aja('og-roi-sdi', 'OG-ROI-SDI', 'OG-ROI-SDI SDI scan converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), ATB('out')],
    'Region-of-interest scaler for SDI with loop-through, SDI and HDMI 1.4 outputs and 2-channel analog audio out. Locks to frame reference.', 7)
aja('og-roi-dvi', 'OG-ROI-DVI', 'OG-ROI-DVI DVI to SDI scan converter',
    [R('in', 'DVI', 'DVI', 1, 'DVI In'), R('out', 'DVI', 'DVI', 1, 'DVI Loop'), ATB('in'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out')],
    'Region-of-interest scan converter for DVI computer or video sources, 2-channel analog audio in. Locks to frame reference. '
    'Check: the spec table calls the loop-through HDMI; drawn as DVI.', 8, verified=False)
aja('og-udc', 'OG-UDC', 'OG-UDC 3G-SDI up/down/cross converter',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), ATB('out')],
    'Up, down and cross conversion with HDMI 1.4a monitor out and 2-channel analog audio out. Locks to frame reference.', 7)
aja('og-fs-mini', 'OG-FS-Mini', 'OG-FS-Mini 3G-SDI frame synchronizer',
    [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), ATB('out')],
    'Frame sync locked to frame reference (tri-level or black burst), HDMI monitor out and 2-channel analog audio out.', 7)
aja('og-colorbox', 'OG-ColorBox', 'OG-ColorBox 12G-SDI colour pipeline / LUT processor',
    [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'Ethernet', 'RJ45', 1, 'LAN')],
    'Colour management (LUTs, ORION-CONVERT, Colorfront, BBC HDR LUTs) with gigabit Ethernet for the web UI. '
    'Check: the spec lists a USB interface without saying where it is.', 19, verified=False)
aja('og-dante-12gam', 'OG-DANTE-12GAM', 'OG-DANTE-12GAM 12G-SDI / Dante audio embedder/disembedder',
    [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out'), R('io', 'Dante', 'RJ45', 2, 'Dante')],
    '64 channels between two 12G-SDI paths (16 embedded channels each way) and Dante, primary and secondary gigabit ports '
    '(RJ45, as in AJA\'s rear photo).', 15)
FIDO12 = [('TR-12G', 'transceiver', [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Out'), R('in', 'Fibre', 'LC', 1, 'Fibre In'), R('out', 'Fibre', 'LC', 1, 'Fibre Out')], True),
          ('2T-12G', 'dual transmitter', [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', 'Fibre', 'LC', 2, 'Fibre Out')], True),
          ('2R-12G', 'dual receiver', [R('in', 'Fibre', 'LC', 2, 'Fibre In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out')], True),
          ('4T-12G', '4-channel transmitter', [R('in', '12G-SDI', 'BNC', 4, 'SDI In'), R('out', 'Fibre', 'LC', 4, 'Fibre Out')], False),
          ('4R-12G', '4-channel receiver', [R('in', 'Fibre', 'LC', 4, 'Fibre In'), R('out', '12G-SDI', 'BNC', 4, 'SDI Out')], False),
          ('4X-12G', '4-channel 2 Tx / 2 Rx', [R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', 'Fibre', 'LC', 2, 'Fibre Out'), R('in', 'Fibre', 'LC', 2, 'Fibre In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out')], False),
          ('T-12G-ST', 'transmitter, ST', [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 1, 'SDI Loop Out'), R('out', 'Fibre', 'ST', 1, 'Fibre Out')], True),
          ('R-12G-ST', 'receiver, ST', [R('in', 'Fibre', 'ST', 1, 'Fibre In'), R('out', '12G-SDI', 'BNC', 2, 'SDI Out')], True)]
for sfx, desc, ports, ver in FIDO12:
    aja(f'og-fido-{sfx.lower()}', f'OG-FiDO-{sfx}', f'OG-FiDO-{sfx} 12G-SDI single-mode fibre {desc}', ports,
        f'12G-SDI / single-mode fibre {desc}, independent channels.'
        + ('' if ver else ' Check: port counts follow the model description; AJA publishes no spec sheet for the 4-channel models.'),
        3, verified=ver, cols=1 if sum(p['count'] for p in ports) <= 4 else 2)
FIDO3 = [('4T', '4-channel transmitter', [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', 'Fibre', 'LC', 4, 'Fibre Out')]),
         ('4R', '4-channel receiver', [R('in', 'Fibre', 'LC', 4, 'Fibre In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')]),
         ('4X', '4-channel 2 Tx / 2 Rx', [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', 'Fibre', 'LC', 2, 'Fibre Out'), R('in', 'Fibre', 'LC', 2, 'Fibre In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')])]
for sfx, desc, ports in FIDO3:
    aja(f'og-fido-{sfx.lower()}', f'OG-FiDO-{sfx}', f'OG-FiDO-{sfx} 3G-SDI single-mode fibre {desc}', ports,
        f'3G-SDI / single-mode LC fibre {desc}, independent isolated channels; 10 cards (40 channels) per 20-slot frame. '
        'Check: port counts follow the model description; AJA publishes no spec sheet for the 4-channel models.', verified=False)
# multimode (-MM, 850 nm LC) versions: same rear connectors as the single-mode cards above
for base in [m for m in list(OG) if m['id'] in ('aja-og-fido-tr', 'aja-og-fido-t', 'aja-og-fido-r', 'aja-og-fido-2t', 'aja-og-fido-2r',
                                                 'aja-og-fido-4t', 'aja-og-fido-4r', 'aja-og-fido-4x')]:
    mm = json.loads(json.dumps(base)); pn = base['partNumber'] + '-MM'
    mm.update(id=base['id'] + '-mm', partNumber=pn, name=base['name'].replace(base['partNumber'], pn).replace('single-mode', 'multimode'),
              notes=base['notes'].replace('single-mode', 'multimode (850 nm)').replace(' -MM multimode versions have the same connectors.', ''),
              productUrl=f'https://www.aja.com/products/{pn.lower()}')
    mm['rearModules'][0]['partNumber'] = pn + ' rear'
    OG.append(mm)

# ---- Cobalt openGear ----
C9904 = 'https://opengear.tv/card/9904-udx-4k/'
GPIO = lambda: R('io', 'GPIO', 'RJ45', 1, 'GPIO/COMM')
ETH = lambda: R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')
OG.append(card('cobalt', '9904-udx-4k', 'Cobalt Digital', '9904-UDX-4K', '9904-UDX-4K 12G UHD up/down/cross converter, frame sync', 'Cobalt openGear', ['openGear'],
    [rm('RM20-9904-D-HDBNC', 'Standard width', 2, [R('in', '12G-SDI', 'HD-BNC', 6, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 6, 'SDI Out'),
        R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), GPIO(), ETH()], default=True),
     rm('RM20-9904-B-HDBNC', 'Double width', 4, [R('in', '12G-SDI', 'HD-BNC', 6, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 8, 'SDI Out'),
        R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), R('in', 'HDMI', 'HDMI', 1, 'HDMI In (-H2S)'), R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), GPIO(), ETH()],
        offset=1, rm_notes='Card sits in the even slot and consumes the adjacent odd slot. Cannot be fitted in slots 19/20.'),
     rm('RM20-9904-C-HDBNC', 'Double width', 4, [R('in', '12G-SDI', 'HD-BNC', 6, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 4, 'SDI Out'),
        R('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), R('io', 'SFP', 'SFP', 2, 'SFP'), GPIO(), ETH()], offset=1),
     rm('RM20-9904-F-HDBNC', 'Rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 6, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 9, 'SDI Out'),
        R('io', 'AES/EBU', 'HD-BNC', 8, 'AES I/O'), R('io', 'SFP', 'SFP', 2, 'SFP'), GPIO(), ETH()], rm_notes='Check: width not stated.'),
     rm('RM20-9904-G-HDBNC', 'Rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 4, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 4, 'SDI Out'),
        R('io', 'AES/EBU', 'HD-BNC', 3, 'AES I/O'), R('io', 'SFP', 'SFP', 1, 'SFP'), GPIO()], rm_notes='Mates to card in odd slot. Check: width and SFP count.'),
     rm('RM20-9904-J-HDBNC', 'Rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 5, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 7, 'SDI Out'),
        R('out', '12G-SDI', 'HD-BNC', 1, 'SDI Out Relay'), R('io', 'AES/EBU', 'HD-BNC', 4, 'AES I/O'), GPIO()],
        rm_notes='Relay-protected out passes SDI In 5 on power loss. Mates to card in odd slot. Check: width.')],
    'UHD/HD/3G up/down/cross converter and frame sync, 12G single wire or quad 3G, embed/de-embed, HDR options. Up to 5 per OG3/HPF-9000 frame, 7 per oGx frame; leave 1RU above the frame. '
    'Variants -IP (2 x 10GigE) and -DSP use the same rear modules. Check: specs marked preliminary by Cobalt.',
    'openGear.tv 9904-UDX-4K card page', C9904, watts=None))
C9902 = 'https://www.opengear.tv/card/9902-2udx/'
OG.append(card('cobalt', '9902-2udx', 'Cobalt Digital', '9902-2UDX', '9902-2UDX dual 3G up/down/cross converter, frame sync', 'Cobalt openGear', ['openGear'],
    [rm('RM20-9902-2UDX-C', 'Standard width', 2, [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out'),
        R('out', '3G-SDI', 'BNC', 1, 'SDI Out Relay'), GPIO()], default=True),
     rm('RM20-9902-2UDX-A/S', 'Split (2 cards)', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 3, 'SDI Out')], cpm=2, cols=1, rows=5),
     rm('RM20-9902-2UDX-E-HDBNC', 'Standard width', 2, [R('in', '3G-SDI', 'HD-BNC', 4, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', 4, 'SDI Out'),
        R('in', 'AES/EBU', 'HD-BNC', 8, 'AES In'), R('out', 'AES/EBU', 'HD-BNC', 8, 'AES Out')]),
     rm('RM20-9902-2UDX-P-HDBNC', 'Standard width', 2, [R('in', '3G-SDI', 'HD-BNC', 4, 'SDI In'), R('out', '3G-SDI', 'HD-BNC', 8, 'SDI Out'), GPIO(), ETH()],
        rm_notes='SDI In 1-2 have independent relay bypass.'),
     rm('RM20-9902-2UDX-N-HDBNC', 'Double width', 4, [R('in', '3G-SDI', 'HD-BNC', 4, 'SDI In'), R('in', 'Analog video', 'HD-BNC', 1, 'CVBS In'),
        R('in', 'AES/EBU', 'HD-BNC', 8, 'AES In'), R('in', 'Analog audio', 'Terminal', 4, 'Analog In'),
        R('out', '3G-SDI', 'HD-BNC', 8, 'SDI Out'), R('out', 'Analog video', 'HD-BNC', 1, 'CVBS Out'), R('out', 'AES/EBU', 'HD-BNC', 8, 'AES Out'),
        R('out', 'Analog audio', 'Terminal', 4, 'Analog Out'), GPIO(), ETH()], offset=1, rm_notes='Check: analog audio connector type.')],
    'Two independent 3G/HD/SD paths: up/down/cross conversion, frame sync, audio embed/de-embed. Many more RM20-9902-2UDX rear modules exist (D, F, H, J, K, L, M/S): add them in the catalogue editor if needed.',
    'openGear.tv 9902-2UDX card page', C9902))

# ---- generic openGear templates ----
OG.append(card('tpl', 'og-card-full', 'Generic', 'openGear card (full rear)', 'openGear card, full rear module (template)', 'Templates', ['openGear'],
    [rm('Full rear module', 'Full rear module', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')], default=True, cols=2, rows=5)],
    'Template. Edit the part number and rear module ports to match your card.', 'Template', '', verified=False))
OG.append(card('tpl', 'og-card-split', 'Generic', 'openGear card (split rear)', 'openGear card, split rear module (template)', 'Templates', ['openGear'],
    [rm('Split rear module', 'Split rear module (2 cards)', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')], cpm=2, default=True, cols=1, rows=5)],
    'Template. Edit the part number and rear module ports to match your card.', 'Template', '', verified=False))

# =====================================================================================
# Evertz
# =====================================================================================
EV = []
EVF = 'https://evertz.com/products/infrastructure-conversion/multiframes-controllers-accessories/'
EV_FRAME = dict(system='Evertz 7700/7800', slotOrder='ltr', rearAlign=1, door=True,
                front=dict(x0=0.03, x1=0.97, y0=0.04, y1=0.96), rear=dict(x0=0.03, x1=0.84, y0=0.04, y1=0.96))
for id, pn, name, qt in [('7800fr', '7800FR', '7800FR 3RU 15-slot MultiFrame', False), ('7800fr-qt', '7800FR-QT', '7800FR-QT 3RU 15-slot quiet MultiFrame', True)]:
    EV.append(frame('evertz', id, 'Evertz', pn, name, 'Evertz frames', 3,
        [R('in', 'Power', 'IEC C14', 2, 'AC')],
        dict(EV_FRAME, slots=15, controllerSlot=1, controller='Optional 7800FC VistaLINK frame controller fits slot 1 (rightmost slot seen from the rear)'),
        ('Quiet (low noise) version. ' if qt else '') +
        '3RU multiframe for 15 single-slot 7700/7800 modules; dual-slot modules take two. Cards order with the +3RU rear plate. '
        'Slot 1 is on the right of the rear panel, so slot 1 is at the left seen from the front. Fit a 7800FC in slot 1 for Ethernet/SNMP control. '
        'Check: second (redundant) power supply is an option on some builds; power inlet position (drawing fractions are estimates).',
        'Evertz multiframes page and 7800 MultiFrame manual', EVF, verified=False))
EV.append(frame('evertz', '7801fr', 'Evertz', '7801FR', '7801FR 1RU 4-slot MultiFrame', 'Evertz frames', 1,
    [R('in', 'Power', 'IEC C14', 1, 'AC')],
    dict(EV_FRAME, slots=4, orient='h', controller='Optional 7801FC frame controller'),
    '1RU multiframe for up to 4 single-slot or 2 dual-slot 7700/7800 modules (+3RU rear plates). '
    'Check: cards are assumed to lie horizontally with slot 1 at the bottom; power inlet count.',
    'Evertz multiframes page', EVF, verified=False))
EV.append(frame('evertz', '570fr', 'Evertz', '570FR', '570FR 3RU 15-slot frame', 'Evertz frames', 3,
    [R('in', 'Power', 'IEC C14', 2, 'AC')],
    dict(EV_FRAME, system='Evertz 7700/7800', also=['Evertz 570'], slots=15, controllerSlot=1, controller='Optional 570FC VistaLINK PRO frame controller in slot 1'),
    '3RU high-density frame for 15 single-slot modules, compatible with all 7700/7800 and 570 series modules. One PSU standard, redundant hot-swap PSU option +57PS '
    '(separate inlets, 100-240 V). 750 W module load. 570FR-HF has high-flow fans. Check: frame rear connectors besides power.',
    'Evertz 570FR product page', 'https://evertz.com/products/570FR'))
EV.append(card('evertz', '7800fc', 'Evertz', '7800FC', '7800FC VistaLINK frame controller', 'Evertz frame controllers', ['Evertz 7700/7800'],
    [rm('7800FC+3RU', 'Rear plate', 1, [R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-232', 'DB9', 1, 'Serial')], default=True)],
    'Frame controller for 7700FR-C, 7800FR and 7800FR-QT: SNMP/VistaLINK control of all modules. Installs in slot 1 with its rear plate and 7700CM-2 connector module. '
    'Check: rear connectors (Ethernet and serial) from the manual\'s rear panel section.',
    'Evertz 7800 MultiFrame manual (7800FC installation)', 'https://evertz.com/products/7800FC', verified=False, onlySlots=[1]))
U4K = 'https://evertz.com/products/7814-4K'
EV.append(card('evertz', '7814udx-4k', 'Evertz', '7814UDX-4K', '7814UDX-4K UHD up/down/cross converter', 'Evertz 7800 conversion', ['Evertz 7700/7800'],
    [rm('7814UDX-4K+3RU', 'Dual-slot rear plate (DIN)', 2, [R('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI Out')], default=True),
     rm('7814UDX-AES8-4K+3RU', 'Dual-slot rear plate with AES', 2, [R('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI Out'),
        R('in', 'AES/EBU', 'DIN 1.0/2.3', 8, 'AES In'), R('out', 'AES/EBU', 'DIN 1.0/2.3', 8, 'AES Out')]),
     rm('7814UDX-4K-12G+3RU', 'Dual-slot rear plate with 12G SFPs', 2, [R('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 4, 'Quad SDI Out'),
        R('io', 'SFP', 'SFP', 2, '12G SFP')])],
    'UHD/HD/3G up/down/cross converter, 16 ch embedded audio. Each card occupies two slots (7 per 7800FR, 2 per 7801FR). Also 7814UC-4K, 7814HDC-4K, 7814XC-4K with the same rear plates. '
    'Check: quad SDI in/out counts are assumed (4 in, 4 out); Evertz page does not list connector counts.',
    'Evertz 7814-4K product page', U4K, verified=False, slotWidth=2))
# ---- more Evertz 7700/7800 modules (evertz.com product pages and manuals) ----
EVP = 'https://evertz.com/products/'
def ev(id, pn, name, fam, rms, notes, src, verified=True, **kw):
    EV.append(card('evertz', id, 'Evertz', pn, name, fam, ['Evertz 7700/7800'], rms, notes, src, EVP + pn, verified=verified, **kw))
for pn, std, typ in [('7700DA7', 'SD-SDI / DVB-ASI', 'SD-SDI'), ('7700DA7-3G', '3G/HD/SD-SDI', '3G-SDI')]:
    ev(pn.lower(), pn, f'{pn} {std} reclocking DA 1x7', 'Evertz 7700/7800 distribution',
       [rm(pn + '+3RU', 'Single-slot rear plate', 1, [R('in', typ, 'BNC', 1, 'SDI In'), R('out', typ, 'BNC', 7, 'SDI Out')], default=True, cols=1)],
       f'{std} reclocking DA: auto-equalised input, 7 isolated reclocked outputs. 1 slot.', f'Evertz {pn} product page')
ev('7800da8-12g', '7800DA8-12G', '7800DA8-12G 12G/3G/HD/SD reclocking DA 1x8', 'Evertz 7700/7800 distribution',
   [rm('7800DA8-12G+3RU', 'Rear plate', 1, [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 8, 'SDI Out')], default=True, cols=1)],
   '1 in, 8 isolated reclocked outputs. Check: connector type (BNC or HD-BNC) and slot width.', 'Evertz 7800DA8-12G product page', verified=False)
ev('7800ida8-3g-f', '7800IDA8-3G-F', '7800IDA8-3G-F intelligent 3G DA 1x8 with fibre outs', 'Evertz 7700/7800 distribution',
   [rm('7800IDA8-3G-F+3RU', 'Single-slot rear plate', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 8, 'SDI Out'),
       R('out', 'Fibre', 'LC (SFP)', 2, 'Fibre Out')], default=True, cols=1)],
   '3G/HD/SD intelligent DA: 1 BNC input, 8 reclocked DIN 1.0/2.3 outputs, optional dual Tx SFP (SFP3T13-2) for 2 fibre outputs. Needs 7800FC for full control.',
   'Evertz 7800IDA8-3G-F product page')
AE_LTC = [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 3, 'SDI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out (relay bypass)'),
          R('in', 'AES/EBU', 'DB15 (BNC breakout)', 8, 'AES In'), R('in', 'Timecode', 'DB15 (breakout)', 1, 'LTC In'), R('in', 'RS-422', 'DB15 (breakout)', 1, 'Metadata In')]
AE_B = [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out (relay bypass)'),
        R('in', 'AES/EBU', 'Terminal block', 8, 'AES In')]
ev('7821ae8-3g', '7821AE8-3G', '7821AE8-3G 8 AES embedder', 'Evertz 7700/7800 audio',
   [rm('7821AE8-LTC-3G+3RU', 'LTC model rear plate', 1, AE_LTC, default=True),
    rm('7821AE8-B-3G+3RU', 'Base model rear plate', 1, AE_B)],
   '3G/HD/SD 8 AES embedder. LTC model adds Dolby metadata insert and LTC embedding; AES, LTC and metadata come in on a DB15 with breakout cable. '
   'One output is bypass-relay protected. 1 slot in 7800FR (2 in 7700FR-C/350FR). -AESD version has 8 DIN AES inputs.', 'Evertz 7821AE8-3G product page')
AD_LTC = [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 3, 'SDI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out (relay bypass)'),
          R('out', 'AES/EBU', 'DB15 (BNC breakout)', 8, 'AES Out'), R('out', 'Timecode', 'DB15 (breakout)', 1, 'LTC Out'), R('out', 'RS-422', 'DB15 (breakout)', 1, 'Metadata Out')]
AD_B = [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out (relay bypass)'),
        R('out', 'AES/EBU', 'Terminal block', 8, 'AES Out')]
ev('7821ad8-3g', '7821AD8-3G', '7821AD8-3G 8 AES de-embedder', 'Evertz 7700/7800 audio',
   [rm('7821AD8-LTC-3G+3RU', 'LTC model rear plate', 1, AD_LTC, default=True),
    rm('7821AD8-B-3G+3RU', 'Base model rear plate', 1, AD_B)],
   '3G/HD/SD 8 AES de-embedder. LTC model adds Dolby metadata extraction and LTC out on a DB15 breakout. One output is bypass-relay protected. '
   '1 slot in 7800FR (2 in 7700FR-C/350FR).', 'Evertz 7821AD8-3G product page')
UDX = [R('in', '3G-SDI', 'BNC', 1, 'PGM In A'), R('in', '3G-SDI', 'BNC', 1, 'PGM In B'), R('out', '3G-SDI', 'BNC', 4, 'PGM Out'),
       R('in', 'Analog video', 'BNC', 1, 'Composite In'), R('out', 'Analog video', 'BNC', 1, 'Composite Out'),
       R('in', 'Analog audio', 'Terminal block', 4, 'Analog In'), R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out'),
       R('io', 'GPIO', 'DB15', 1, 'GPIO'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')]
ev('7812udx-aav', '7812UDX-AAV-3G', '7812UDX-AAV 3G/HD up/down/cross converter', 'Evertz 7700/7800 conversion',
   [rm('7812UDX-AAV-3G+3RU', 'Dual-slot rear plate', 2, UDX, default=True),
    rm('7812UDX-AES8-AAV-3G+3RU', 'Dual-slot rear plate with AES', 2, UDX + [R('in', 'AES/EBU', 'DB15', 8, 'AES In'), R('out', 'AES/EBU', 'DB15', 8, 'AES Out')])],
   'Up/down/cross converter with frame sync, analog audio/video I/O. Occupies 2 slots in 7800FR (3 in 7700FR-C). -F versions add dual SFP fibre in/out. '
   'Check: the AES8 ports are on DB15 connectors (counted as 8 in and 8 out here).',
   'Evertz 7812UDX-AAV series manual v1.0', slotWidth=2)
ev('7812udx-3g', '7812UDX-3G', '7812UDX-3G 3G/HD up/down/cross converter', 'Evertz 7700/7800 conversion',
   [rm('7812UDX-3G+3RU', 'Dual-slot rear plate', 2, [R('in', '3G-SDI', 'BNC', 1, 'PGM In A'), R('in', '3G-SDI', 'BNC', 1, 'PGM In B'), R('out', '3G-SDI', 'BNC', 4, 'PGM Out'),
       R('io', 'GPIO', 'DB15', 1, 'GPIO'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')], default=True),
    rm('7812UDX-AES8-3G+3RU', 'Dual-slot rear plate with AES', 2, [R('in', '3G-SDI', 'BNC', 2, 'PGM In'), R('out', '3G-SDI', 'BNC', 4, 'PGM Out'),
       R('in', 'AES/EBU', 'DB15', 8, 'AES In'), R('out', 'AES/EBU', 'DB15', 8, 'AES Out'), R('io', 'GPIO', 'DB15', 1, 'GPIO')])],
   'Up/down/cross converter with frame sync and external genlock. Check: ports are assumed to match the 7812UDX-AAV manual without the analog I/O; '
   'confirm against your rear plate.', 'Evertz 7812 series page and 7812UDX-AAV manual', verified=False, slotWidth=2)
ev('7708sfp-2', '7708SFP-2', '7708SFP-2 dual SFP carrier', 'Evertz 7700/7800 fibre',
   [rm('7708SFP-2+3RU', 'Single-slot rear plate', 1, [R('io', '3G-SDI', 'BNC', 2, 'SDI'), R('io', 'Fibre', 'LC (SFP)', 2, 'Fibre')], default=True, cols=1)],
   'Card carrier for 2 Evertz 3405-series SFPs (fibre transmitters, receivers or regenerators). The SFPs fitted decide the direction of each SDI and fibre port: '
   'set the ports to in or out to match. 7708SFP has 1 SFP; 7708SFP-2-DIN uses DIN connectors.', 'Evertz 3405/7708SFP product page', verified=False)
EV.append(card('tpl', 'ev-card', 'Generic', 'Evertz 7800 card', 'Evertz 7700/7800 single-slot card (template)', 'Templates', ['Evertz 7700/7800'],
    [rm('+3RU rear plate', 'Single-slot rear plate', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')], default=True)],
    'Template for any 7700/7800 module: edit the part number and rear plate ports to match your card.', 'Template', '', verified=False))

# =====================================================================================
# Grass Valley Densite
# =====================================================================================
GV = []
D3 = 'https://grassvalley.com/products/densite_3_frame'
D_FRAME = dict(system='Densite', slotOrder='ltr', rearAlign=1, door=True,
               front=dict(x0=0.04, x1=0.96, y0=0.05, y1=0.95), rear=dict(x0=0.03, x1=0.85, y0=0.05, y1=0.95))
GV.append(frame('gv', 'densite-3', 'Grass Valley', 'DENSITE-3', 'Densité 3 3RU 20-slot frame', 'Densité frames', 3,
    [R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('out', 'GPI', 'Terminal', 1, 'Alarm GPI'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
    dict(D_FRAME, slots=20, controller='Densité-CPU-ETH2 controller with front control panel, in its own slot'),
    '3RU frame for 20 Densité cards. Two hot-swap 300 W PSUs (100-240 V). Rear connector panels are blank until ordered with each card '
    '(single, double -3DRP or triple -3TRP width); the card sits in the right-most slot of a multi-slot panel. '
    'Check: rear position of Ethernet, GPI and power (drawing fractions are estimates).',
    'Grass Valley Densité 3 frame data sheet (3-0011B)', D3))
GV.append(frame('gv', 'densite-3plus-fr4', 'Grass Valley', 'DENSITE-3+FR4', 'Densité 3+ FR4 4RU 24-slot frame', 'Densité frames', 4,
    [R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('out', 'GPI', 'Terminal', 1, 'Alarm GPI'), R('in', 'Reference', 'BNC', 1, 'Ref'), R('out', 'Reference', 'BNC', 1, 'Ref Loop'),
     R('in', 'Power', 'IEC C14', 2, 'PSU')],
    dict(D_FRAME, slots=24, controller='Densité 3+ controller; ADV controller adds a second reference and LTC'),
    '4RU frame for 24 Densité cards at up to 25 W each. Two 700 W hot-swap PSUs, dual GbE, optional passive loop-through reference, alarm GPI. '
    'Check: reference loop is optional; rear layout (drawing fractions are estimates).',
    'Grass Valley Densité 3+ FR4 data sheet (GVB-1-0337D)', 'https://gvcmsumb.grassvalley.com/products/modular-processing/densite-3-fr4-frame', verified=False))
GV.append(frame('gv', 'densite-3plus-fr1', 'Grass Valley', 'DENSITE-3+FR1', 'Densité 3+ FR1 1RU 4-slot frame', 'Densité frames', 1,
    [R('io', 'Ethernet', 'RJ45', 2, 'Ethernet'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
    dict(D_FRAME, slots=4, orient='h', fixed=[dict(slot=4, label='System (REF-1801-D3+FR1)')]),
    '1RU frame for 4 cards including the system slot (REF-1801-D3+FR1). Two PSUs, 2 x 10/100 Ethernet. '
    'Check: cards assumed horizontal; which slot is the system slot.',
    'Grass Valley Densité 3+ FR1 data sheet', D3, verified=False))
XVP = 'https://grassvalley.com/products/xvp-3901-fs'
XVP_BASE = lambda c='BNC': [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out A'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out B'),
                            R('in', 'Reference', 'BNC', 1, 'Ref In'), R('io', 'GPI', 'DB26', 1, 'GPI/RS-422 B'), R('io', 'RS-422', 'RJ45', 1, 'RS-422 A')]
GV.append(card('gv', 'xvp-3901', 'Grass Valley', 'XVP-3901', 'XVP-3901 3G/HD/SD up/down/cross converter, frame sync', 'Densité video processing', ['Densite'],
    [rm('XVP-3901-75-3TRP', 'Triple rear panel, 75 ohm', 3, XVP_BASE() + [R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out')], offset=2, default=True),
     rm('XVP-3901-75-3TRP-F', 'Triple rear panel, 75 ohm, fibre', 3, XVP_BASE() + [R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out'), R('io', 'Fibre', 'LC (SFP)', 1, 'Fibre')], offset=2),
     rm('XVP-3901-110-3TRP', 'Triple rear panel, 110 ohm', 3, XVP_BASE() + [R('in', 'AES/EBU', 'WECO', 4, 'AES In'), R('out', 'AES/EBU', 'WECO', 4, 'AES Out')], offset=2),
     rm('XVP-3901-75-3DRP-F', 'Double rear panel, 75 ohm, fibre', 2, XVP_BASE() + [R('io', 'AES/EBU', 'DB26', 1, 'AES (D-sub)'), R('io', 'Fibre', 'LC (SFP)', 1, 'Fibre')], offset=1)],
    'Up/down/cross converter and frame sync with 4 AES in/out. The card goes in the right-most slot of its double or triple rear panel. '
    'Variants XVP-3901-FS, -DC, -DPI share the rear panels. Check: ref loop on some panels; fibre cartridge SFP-R-LC, SFP-RR-LC or SFP-RT-S13-LC sets the fibre ports.',
    'Grass Valley XVP-3901 data sheet and Installation Guide v3.11', XVP))
GV.append(card('gv', 'densite-card', 'Generic', 'Densité card', 'Densité card, single rear panel (template)', 'Templates', ['Densite'],
    [rm('Single rear panel', 'Single rear panel', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')], default=True)],
    'Template for any Densité card: edit the part number and rear panel ports to match your card.', 'Template', '', verified=False))

# =====================================================================================
# EVS Synapse (ex Axon)
# =====================================================================================
SY = []
SYF = 'https://evs.com/sites/default/files/2021-08/SFR04-08-18_PD.pdf'
SYC = 'https://evs.com/sites/default/files/2026-03/Synapse%20Catalog%20-%20January%202026.pdf'
SY_REAR = lambda refs: ([R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 1, 'Ref Loop')] if refs == 1 else
                        [R('in', 'Reference', 'BNC', 2, 'Ref In'), R('out', 'Reference', 'BNC', 2, 'Ref Loop')])
for id, pn, ru, slots, refs, ctl, psu, watts, orient in [
        ('sfr18', 'SFR18', 4, 18, 2, 'ERC118 / ERS118 (SNMP)', 2, 500, 'v'),
        ('sfr08', 'SFR08', 2, 8, 2, 'ERC108 / ERS108 (SNMP)', 2, 275, 'h'),
        ('sfr04', 'SFR04', 1, 4, 1, 'RRC04 / RRS04 (SNMP)', 1, 160, 'h')]:
    fr = dict(system='Synapse', slots=slots, slotOrder='ltr', rearAlign=1, door=False, orient=orient,
              controller=f'{ctl} rack controller in its own slot (not a card slot)',
              front=dict(x0=0.03, x1=0.97, y0=0.05, y1=0.95), rear=dict(x0=0.03, x1=0.84, y0=0.05, y1=0.95))
    if orient == 'h': fr['cols'] = 2
    SY.append(frame('evs', id, 'EVS', pn, f'Synapse {pn} {ru}RU {slots}-slot frame', 'EVS Synapse frames', ru,
        SY_REAR(refs) + [R('io', 'Ethernet', 'RJ45', 2 if slots > 4 else 1, 'Ethernet'), R('io', 'USB', 'USB-A', 1, 'USB'),
                         R('in', 'Power', 'IEC C14', psu, 'AC')], fr,
        f'Synapse (ex Axon) {ru}RU frame, {slots} card slots, {refs} genlock reference input{"s" if refs > 1 else ""}, {watts} W max. '
        f'Rack controller {ctl} sits in a separate slot. '
        + (f'{pn}R has redundant power supplies (one PSU as standard). ' if psu == 2 else 'Single PSU. ') +
        'Each card has its own back panel (BPH/BPL/BHX...) ordered separately. '
        + ('Check: card orientation and slot numbering (cards assumed flat, two columns, slot 1 bottom-left). ' if orient == 'h' else 'Check: slot numbering direction. ') +
        'Check: rear connector positions (drawing fractions are estimates).',
        'EVS SFR04/08/18 product data sheet; ERC/ERS108/118 data sheet', SYF, verified=False))
SY_NOTE = 'Synapse cards are all one slot wide, with a separate back panel. Check: back panel connector types (BNC assumed; high-density panels may differ).'
def syn(id, pn, name, fam, rms, notes):
    SY.append(card('evs', 'syn-' + id, 'EVS', pn, name, fam, ['Synapse'], rms, notes + ' ' + SY_NOTE, 'EVS Synapse catalogue (January 2026)', SYC, verified=False))
syn('gdr108', 'GDR108', 'GDR108 3G/HD/SD reclocking DA 1x8', 'Synapse distribution',
    [rm('BPH34', 'Back panel', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')], default=True, cols=1),
     rm('BHX34', 'Back panel with relay bypass', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')], cols=1),
     rm('BPH35R', 'Back panel with SFP input', 1, [R('in', 'SFP', 'SFP', 1, 'SFP In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out')], cols=1)],
    '1 in, 8 reclocked outs, ASI/DVB compatible. SDR108 is the SD-only version with the same panels.')
syn('gdr216', 'GDR216', 'GDR216 dual-input 3G reclocking DA, 16 outs', 'Synapse distribution',
    [rm('BPH37', 'Back panel', 1, [R('in', '3G-SDI', 'DIN 1.0/2.3', 2, 'SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 16, 'SDI Out'), R('io', 'GPI', 'RJ45', 1, 'GPI')], default=True, cols=2),
     rm('BHX37', 'Back panel with relay bypass', 1, [R('in', '3G-SDI', 'DIN 1.0/2.3', 2, 'SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 16, 'SDI Out'), R('io', 'GPI', 'RJ45', 1, 'GPI')], cols=2)],
    '2 in, 16 outs (as 2 x 1x8 or 1x16 with failover). BPH42/BHX42 BNC panels and BPH38T/BPH39R SFP panels have fewer outputs: add them in the catalogue editor if you use them. '
    'Check: DIN connectors assumed for 18 connectors in one slot; GPI connector.')
syn('gdr416', 'GDR416', 'GDR416 4K/3G quad reclocking DA', 'Synapse distribution',
    [rm('BPH43', 'Back panel', 1, [R('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 16, 'SDI Out'), R('io', 'GPI', 'RJ45', 1, 'GPI')], default=True, cols=2),
     rm('BHX43', 'Back panel with relay bypass', 1, [R('in', '3G-SDI', 'DIN 1.0/2.3', 4, 'SDI In'), R('out', '3G-SDI', 'DIN 1.0/2.3', 16, 'SDI Out'), R('io', 'GPI', 'RJ45', 1, 'GPI')], cols=2)],
    'Four 1x4 DAs, or quad-link 4K. BPH48T/BPH48R add SFPs. Check: DIN connectors assumed.')
syn('udr108', 'UDR108', 'UDR108 12G UHD reclocking DA 1x8', 'Synapse distribution',
    [rm('UDR108 back panel', 'Back panel', 1, [R('in', '12G-SDI', 'BNC', 1, 'SDI In'), R('out', '12G-SDI', 'BNC', 8, 'SDI Out')], default=True, cols=1)],
    'UHD/FHD/HD/SD single-wire 12G DA with 8 reclocked outs. Check: input count and back panel part number.')
syn('cdv29', 'CDV29', 'CDV29 reference DA (black burst / tri-level)', 'Synapse distribution',
    [rm('BPL01', 'Back panel', 1, [R('in', 'Reference', 'BNC', 1, 'Ref In'), R('out', 'Reference', 'BNC', 9, 'Ref Out')], default=True, cols=1)],
    'Black burst / tri-level reference DA with 9 outputs. Check: input on the panel.')
syn('dad08', 'DAD08', 'DAD08 AES/EBU DA 1x8', 'Synapse audio',
    [rm('BPL01', 'Back panel, 75 ohm', 1, [R('in', 'AES/EBU', 'BNC', 1, 'AES In'), R('out', 'AES/EBU', 'BNC', 8, 'AES Out')], default=True, cols=1),
     rm('BPL05D', 'Back panel, 110 ohm balanced', 1, [R('in', 'AES/EBU', 'D-sub', 1, 'AES In'), R('out', 'AES/EBU', 'D-sub', 8, 'AES Out')], cols=1)],
    'AES/EBU DA, 1 in, 8 outs. BPX01 adds relay bypass. Check: BPL05D connector type.')
syn('dwc08', 'DWC08', 'DWC08 word clock DA 1x8', 'Synapse distribution',
    [rm('BPL01', 'Back panel', 1, [R('in', 'Word clock', 'BNC', 1, 'WC In'), R('out', 'Word clock', 'BNC', 8, 'WC Out')], default=True, cols=1)],
    'Word clock DA, 1 in, 8 outs. DWC18 also generates video-locked word clock.')
syn('aad08', 'AAD08', 'AAD08 dual 1x8 analog audio DA', 'Synapse audio',
    [rm('BPL06', 'Back panel', 1, [R('in', 'Analog audio', 'Terminal block', 2, 'Audio In'), R('out', 'Analog audio', 'Terminal block', 16, 'Audio Out')], default=True, cols=2)],
    'Two channels of 1x8 analog audio distribution. Check: connector type (BPL06M is a variant).')
EMB = lambda sdi_in, aud: [R('in', '3G-SDI', 'BNC', sdi_in, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')] + aud + [R('io', 'GPI', 'D-sub', 1, 'GPI')]
for pn, kind, sdi_in, desc, typ, n in [
        ('GEB800', 'embedder', 1, '8 ch AES', 'AES/EBU', 4), ('GEB880', 'embedder', 1, '16 ch AES', 'AES/EBU', 8), ('GEB440', 'embedder', 1, '8 ch analog', 'Analog audio', 8),
        ('GEB990', 'embedder', 2, '16 ch AES, enhanced (TWINS)', 'AES/EBU', 8),
        ('GDB800', 'de-embedder', 1, '8 ch AES', 'AES/EBU', 4), ('GDB880', 'de-embedder', 1, '16 ch AES', 'AES/EBU', 8), ('GDB440', 'de-embedder', 1, '8 ch analog', 'Analog audio', 8),
        ('GDB990', 'de-embedder', 2, '16 ch AES, enhanced (TWINS)', 'AES/EBU', 8)]:
    d = 'in' if kind == 'embedder' else 'out'; lab = ('AES ' if typ == 'AES/EBU' else 'Audio ') + ('In' if d == 'in' else 'Out')
    syn(pn.lower(), pn, f'{pn} 3G/HD/SD {desc} {kind}', 'Synapse audio',
        [rm('BPH18', 'Back panel, unbalanced', 1, EMB(sdi_in, [R(d, typ, 'BNC' if typ == 'AES/EBU' else 'D-sub', n, lab)]), default=True, cols=2),
         rm('BPH18D', 'Back panel, balanced (D-sub)', 1, EMB(sdi_in, [R(d, typ, 'D-sub', n, lab)]), cols=2),
         rm('BHX18D', 'Back panel, balanced, relay bypass', 1, EMB(sdi_in, [R(d, typ, 'D-sub', n, lab)]), cols=2)],
        f'Audio {kind}: {sdi_in} SDI in, 2 SDI out. Audio counts are read as channels, so AES ports = channel pairs. '
        'Other models in the range: 400/440 (analog), 800/840/880 (AES), 500-990 enhanced with 2 SDI in. Check: audio port counts and GPI connector.')
syn('grf990', 'GRF990', 'GRF990 frame sync with AES re-embedder', 'Synapse audio',
    [rm('BPH18D', 'Back panel, balanced (D-sub)', 1, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'),
        R('in', 'AES/EBU', 'D-sub', 4, 'AES In'), R('out', 'AES/EBU', 'D-sub', 4, 'AES Out')], default=True, cols=2),
     rm('BHX18D', 'Back panel, relay bypass', 1, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out'),
        R('in', 'AES/EBU', 'D-sub', 4, 'AES In'), R('out', 'AES/EBU', 'D-sub', 4, 'AES Out')], cols=2)],
    'Frame synchroniser with audio de-embed/re-embed: 2 SDI in/out, 4 AES in and 4 AES out. GRF050-GRF950 are the analog/mixed versions.')
SY.append(card('tpl', 'syn-card', 'Generic', 'Synapse card', 'Synapse card with back panel (template)', 'Templates', ['Synapse'],
    [rm('Back panel', 'Back panel', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'SDI Out')], default=True)],
    'Template for any Synapse card: edit the part number and back panel ports to match your card.', 'Template', '', verified=False))

# rear modules ordered under the card's own part number or bundle (Blackmagic, AJA, Evertz +3RU, Ross -R2/-R3 suffix)
# are "included": the equipment list shows them on the card's line, not as a separate item.
# Cobalt RM20-... and Densite rear panels are ordered separately.
INCLUDED_MFRS = {'Blackmagic Design', 'AJA Video Systems', 'Evertz', 'Ross Video'}
for m in OG + EV + GV + SY:
    for r in m.get('rearModules', []):
        r['included'] = m['manufacturer'] in INCLUDED_MFRS

for fn, data in [('frames-opengear.json', OG), ('evertz-frames.json', EV), ('gv-densite.json', GV), ('evs-synapse.json', SY)]:
    ids = [m['id'] for m in data]; assert len(ids) == len(set(ids)), fn
    for m in data:
        for r in m.get('rearModules', []):
            assert sum(1 for x in m['rearModules'] if x['default']) == 1, m['id']
            assert 0 <= r['cardOffset'] < r['width'], (m['id'], r['partNumber'])
    with open(os.path.join(CAT, fn), 'w') as f: json.dump(data, f, indent=1, ensure_ascii=False)
    print(fn, len(data), 'entries')
