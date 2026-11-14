#!/usr/bin/env python3
"""Generates two Ross Video files, added 2026-11-14 after a sweep of Ross's current range:
  catalogue/ross-opengear.json  current Ross openGear cards that frames.py did not have (cards for openGear frames)
  catalogue/ross-more.json      Ross rack units that ross.py did not have (AirCleaner-2, XPression servers, Tria+ UHD,
                                Tria/Kiva Express Duet, Kiva+, CWDM 1RU chassis, RCM-8120 panel, UltriGPI, TXI-48)
Rear module connectors come from the rear module drawings on each Ross product page (rossvideo.com/products/
signal-processing/opengear/...). Gator cards (MC1, Toolbox, Sync, TES-8943) are two slots wide and use the shared
Gator rear modules: R4 (2 slots, oGx frames only), R4F (2 slots, fibre), R3A / R3B (4 slots, unbalanced / balanced AES).
verified=False and a 'Check:' note mark anything a Ross document doesn't settle."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
OGP = 'https://www.rossvideo.com/products/signal-processing/opengear/'

# ======================= openGear cards =======================
OG = []
def rm(pn, name, width, ports, cpm=1, default=False, cols=None, rows=None, gen=None, notes=None):
    r = dict(partNumber=pn, name=name, width=width, cardsPerModule=cpm, cardOffset=0, default=default, portGroups=ports, included=True)
    if cols or rows: r['layout'] = {k: v for k, v in (('cols', cols), ('rows', rows)) if v}
    if gen: r['gen'] = gen
    if notes: r['notes'] = notes
    return r
def card(id, pn, name, fam, rms, notes, src, url, verified=True, slotWidth=1, watts=None, gen=None):
    c = dict(fits=['openGear'], slotWidth=slotWidth)
    if watts is not None: c['watts'] = watts
    if gen: c['gen'] = gen
    if not any(r['default'] for r in rms): rms[0]['default'] = True
    OG.append(dict(id='ross-' + id, manufacturer='Ross Video', partNumber=pn, name=name, family=fam, category='card', ru=0, widthCols=0,
                   fullDepth=False, verified=verified, source=src, productUrl=url, notes=notes, portGroups=[], card=c, rearModules=rms))

# ---- 12G distribution ----
card('sra-8901a', 'SRA-8901A', 'SRA-8901A 12G-SDI reclocking DA (1x10 or 1x5)', 'openGear distribution',
     [rm('R3', 'Full rear module (1 in, 10 out)', 2, [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 10, 'SDI Out')], cols=2, gen=3),
      rm('R3S', 'Split rear module (2 cards, 1 in, 5 out each)', 2, [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 5, 'SDI Out')],
         cpm=2, cols=1, gen=3)],
     'Current version of the SRA-8901: 12G/6G/3G/HD/SD, DVB-ASI and MADI reclocking DA with long-reach equalisation, all outputs non-inverting. '
     'Ordered as SRA-8901A-R3 (1x10) or SRA-8901A-R3S (1x5, the split module takes a second card). The R3 module has a position B under '
     'the input that the single-channel card leaves unused. Under 5.6 W. OG3-FR and OGX-FR only.',
     'Ross SRA-8901A product page and rear module drawings', OGP + 'sra-8901a/', watts=5.6, gen=3)
card('dra-8902a', 'DRA-8902A', 'DRA-8902A dual-input 12G-SDI DA (2 in, 10 out)', 'openGear distribution',
     [rm('R3', 'Full rear module', 2, [R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 10, 'SDI Out')], cols=2, gen=3)],
     'Current dual-input 12G/6G/3G/HD/SD/ASI/MADI DA: inputs A and B feed an internal crosspoint to 10 outputs; each output pair follows '
     'either input or fails over automatically. Ordered as DRA-8902A-R3. Under 5.6 W. OG3-FR and OGX-FR only.',
     'Ross DRA-8902A product page and rear module drawing', OGP + 'dra-8902a/', watts=5.6, gen=3)
card('sra-8901-r', 'SRA-8901-R', 'SRA-8901-R 12G bypass protection switch with DA', 'openGear distribution',
     [rm('R3S-8901-R', 'Split rear module (2 cards)', 2,
         [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('in', '12G-SDI', 'HD-BNC', 1, 'Bypass In'),
          R('out', '12G-SDI', 'HD-BNC', 1, 'Protected Out'), R('out', '12G-SDI', 'HD-BNC', 3, 'SDI Out')], cpm=2, cols=1, gen=3)],
     'Relay bypass protection: on loss of the primary input the protected output switches to the bypass input (manual or automatic return). '
     'Outputs 2-4 are reclocked copies of the primary. Single slot, up to 20 per OG3-FR/OGX-FR, 5 W max. Ordered as SRA-8901-R-R3S; one '
     'R3S-8901-R module serves two cards. Pairs with MC1 for master control protection.',
     'Ross SRA-8901-R product page and rear module cabling drawing', OGP + 'gator/sra-8901-r/', watts=5, gen=3)

# ---- Gator (2-slot cards) ----
GATOR_R4 = lambda ins, outs, extra=(): [R('in', '12G-SDI', 'HD-BNC', ins, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', outs, 'SDI Out'),
                                         R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), *extra]
GNOTE = ' Gator cards take two front slots. R4 modules fit oGx frames (OGX-FR-CN/CNS) only; R3A/R3B modules are 4 slots wide (5 cards per frame).'
card('gator-mc1', 'GATOR-MC1', 'MC1-UHD master control (Gator openGear card)', 'openGear master control',
     [rm('GATOR-MC1-2-R4', 'R4 rear module (2 slots, no discrete audio)', 2,
         GATOR_R4(6, 6, [R('io', 'GPIO', 'Terminal block', 4, 'GPIO')]), cols=3, gen=4),
      rm('GATOR-MC1-4A-R3A', 'R3A rear module (4 slots, 8 unbalanced AES)', 4,
         GATOR_R4(6, 6, [R('io', 'AES/EBU', 'HD-BNC', 8, 'AES'), R('io', 'GPIO', 'Terminal block', 6, 'GPIO'), R('io', 'RS-422', 'RJ45', 1, 'Serial')]), gen=3),
      rm('GATOR-MC1-4B-R3B', 'R3B rear module (4 slots, 8 balanced AES)', 4,
         GATOR_R4(6, 6, [R('io', 'AES/EBU', 'Terminal block', 8, 'AES'), R('io', 'GPIO', 'Terminal block', 6, 'GPIO'), R('io', 'RS-422', 'RJ45', 1, 'Serial')]), gen=3)],
     'Master control switcher on a Gator card: 6 SD/HD/3G/12G-SDI in and 6 out on HD-BNC, frame reference or its own Ref In, TTL GPI/tally '
     'on terminal blocks, TSL 3.1 and automation over IP or serial. Licences: MC1-12G-LICENSE (UHD), MC1-MASTERCTRL-LICENSE, '
     'MC1-DVE-1CH-LICENSE; optional MC1-PANEL-16 hardware panel. Often paired with an SRA-8901-R bypass card.' + GNOTE +
     ' Check: GPIO count on the R3A/R3B modules and whether the RS-422 port is RJ45.',
     'Ross MC1 product page and rear module drawings', 'https://www.rossvideo.com/products/signal-processing/mc1/', slotWidth=2, gen=3)
card('gator-toolbox', 'GATOR-TOOLBOX', 'GATOR-TOOLBOX UHD up/down/cross, HDR and frame sync', 'openGear conversion',
     [rm('GATOR-TOOLBOX-2-R4', 'R4 rear module (2 slots)', 2, GATOR_R4(4, 4), cols=3, gen=4),
      rm('GATOR-TOOLBOX-2F-R4F', 'R4F rear module (2 slots, fibre)', 2,
         [R('in', '12G-SDI', 'HD-BNC', 1, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 1, 'SDI Out'), R('io', '12G-SDI', 'HD-BNC', 3, 'SDI Bi-dir'),
          R('io', 'SFP', 'SFP', 1, 'SDI fibre (SFP)'), R('io', 'SFP', 'SFP', 1, 'MADI fibre (SFP)'), R('io', 'RS-422', 'RJ45', 1, 'Serial'),
          R('io', 'GPIO', 'Terminal block', 4, 'GPIO')], gen=4),
      rm('GATOR-TOOLBOX-4A-R3A', 'R3A rear module (4 slots, 8 unbalanced AES)', 4,
         GATOR_R4(4, 4, [R('io', 'AES/EBU', 'HD-BNC', 8, 'AES')]), gen=3),
      rm('GATOR-TOOLBOX-4B-R3B', 'R3B rear module (4 slots, 8 balanced AES)', 4,
         GATOR_R4(4, 4, [R('io', 'AES/EBU', 'Terminal block', 8, 'AES')]), gen=3)],
     'UHD/HD up/down/cross conversion, HDR conversion, frame sync and optional frame-rate standards conversion over 12G-SDI. SDI is set as '
     '4 in / 1 out (quad-link to single) or 1 in / 4 out; the R4 module has 12 HD-BNC positions, 4 of them unused (N/C).' + GNOTE,
     'Ross GATOR-TOOLBOX product page and rear module drawings', OGP + 'gator/toolbox/', slotWidth=2, gen=3)
card('gator-sync', 'GATOR-SYNC', 'GATOR-SYNC quad 12G frame synchroniser', 'openGear timing',
     [rm('GATOR-SYNC-2-R4', 'R4 rear module (2 slots)', 2, GATOR_R4(4, 4), cols=3, gen=4)],
     'Four independent frame synchronisers (HD/3G/12G, each at its own format) with multi-frame delay (79 frames HD, 14 UHD) and 16 embedded '
     'audio channels per stream with +/-500 ms offset. Discrete audio rear modules are planned.' + GNOTE +
     ' Check: SDI positions (assumed 4 in, 4 out like the Toolbox R4 drawing).',
     'Ross GATOR-SYNC product page', OGP + 'gator/sync/', verified=False, slotWidth=2, gen=4)
card('tes-8943', 'TES-8943', 'TES-8943 VANC data processor (SCTE-104)', 'openGear processing',
     [rm('TES-8943-2-R4', 'R4-GATOR rear module (2 slots)', 2, GATOR_R4(4, 4, [R('io', 'GPI', 'Terminal block', 4, 'GPI'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')]),
         cols=3, gen=4),
      rm('TES-8943-4B-R3B', 'R3B-GATOR rear module (4 slots)', 4, GATOR_R4(4, 4, [R('io', 'GPI', 'Terminal block', 8, 'GPI'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
                                                                              R('io', 'RS-422', 'Other', 1, 'RS-422')]), gen=3)],
     'Inserts, processes and extracts VANC data; SCTE-104 insertion and detection; data in or out over TCP/IP or serial. SD/HD/3G standard, '
     '6G/12G with TES-8943-12G-LICENSE. R4 needs OGX-FR-CN/CNS; R3B also fits OG3-FR-CN/CNS.' + GNOTE +
     ' Check: SDI positions on the Gator modules for this card (assumed 4 in, 4 out).',
     'Ross TES-8943 product page', OGP + 'tes-8943/', verified=False, slotWidth=2, gen=3)

# ---- compressed transport and fibre ----
card('osg-8971', 'OSG-8971', 'OSG-8971 SRT encoder/decoder (6 SDI I/O)', 'openGear transport',
     [rm('OSG-8971-R4', 'Two-slot rear module', 2, [R('io', '3G-SDI', 'HD-BNC', 6, 'SDI I/O'), R('io', 'Ethernet', 'RJ45', 1, 'Network (SRT)')], cols=2, gen=4)],
     'Hardware SRT encoder and decoder (H.264 and H.265): each of the six HD-BNC ports is set as input or output, so one card encodes and '
     'decodes at once; up to 6 HD/3G or 2 UHD streams (OSG-8971-UHD-LICENSE), key+fill pairs, 8 audio channels per stream (16 with '
     'OSG-8971-A16-LICENSE). Up to 10 per oGx frame with an advanced network controller.',
     'Ross OSG-8971 product page', OGP + 'osg-8971/', gen=4)
card('sfc-6901', 'SFC-6901', 'SFC-6901 12G-SDI fibre transport (4 SDI, 4 SFP)', 'openGear fibre',
     [rm('SFC-6901-R3F', 'Two-slot rear module', 2, [R('io', '12G-SDI', 'HD-BNC', 4, 'SDI I/O'), R('io', 'SFP', 'SFP+', 4, 'Fibre SFP')], cols=2, gen=3)],
     'SD to 12G-SDI and ASI electrical/optical conversion with CWDM support and an on-board gearbox for quad-link UHD/8K. The 4 HD-BNCs are each '
     'set as input or output; the 4 SFP+ cages take dual Tx, dual Rx or transceiver SFPs (SFP-FIBER-12G-2T / -2R / -2R-H, SFP-FIBER-12G, '
     'CWDM -2T-xx/yy), ordered separately. 5 W. OG3 and OGX frames.',
     'Ross SFC-6901 product page', OGP + 'sfc-6901/', watts=5, gen=3)

# ---- SD/HD and analog distribution ----
def da_r2(t, conn='BNC'):
    return [rm('R2', '10 BNC rear module (1 in, 8 out)', 2, [R('in', t, conn, 1, 'In'), R('out', t, conn, 8, 'Out')], cols=2, rows=5),
            rm('R2S', 'Split rear module (2 cards, 1 in, 4 out each)', 2, [R('in', t, conn, 1, 'In'), R('out', t, conn, 4, 'Out')], cpm=2, cols=1, rows=5)]
card('wda-8409', 'WDA-8409', 'WDA-8409 word clock DA', 'openGear distribution',
     [rm('R2L-8409', 'Full rear module with loop (1 in, 8 out)', 2, [R('in', 'Word clock', 'BNC', 1, 'WC In'), R('out', 'Word clock', 'BNC', 1, 'WC Loop Out'),
                                                                     R('out', 'Word clock', 'BNC', 8, 'WC Out')], cols=2, rows=5),
      rm('R2S-8409', 'Split rear module (2 cards, 1 in, 4 out each)', 2, [R('in', 'Word clock', 'BNC', 1, 'WC In'), R('out', 'Word clock', 'BNC', 4, 'WC Out')],
         cpm=2, cols=1, rows=5)],
     'Word clock DA up to 192 kHz: Hi-Z or 75 ohm input, 75 ohm outputs. Ordered as WDA-8409-R2L or WDA-8409-R2S. Under 2 W. '
     'DFR-8321, OG3-FR and OGX-FR.', 'Ross WDA-8409 product page and rear module drawings', OGP + 'distribution/wda-8409/', watts=2)
for id, pn, name, note, w in (('vea-8707a', 'VEA-8707A', 'VEA-8707A analog video equalising DA',
                               'Analog video DA with cable equalisation (3 cable types, up to 300 m), differential input, +/-3 dB gain; also tri-level sync.', 1.6),
                              ('uda-8705a', 'UDA-8705A', 'UDA-8705A analog utility DA',
                               'General-purpose analog DA for composite video and tri-level sync, DC coupled, +/-3 dB gain.', 1.5)):
    card(id, pn, name, 'openGear distribution',
         [rm('R2', 'Rear module (1 in, 8 out)', 2, [R('in', 'Analog video', 'BNC', 1, 'Analog In'), R('out', 'Analog video', 'BNC', 8, 'Analog Out')], cols=2, rows=5),
          rm('R2L', 'Looping rear module (1 in + loop, 8 out)', 2, [R('in', 'Analog video', 'BNC', 1, 'Analog In'), R('out', 'Analog video', 'BNC', 1, 'Analog Loop'),
                                                                    R('out', 'Analog video', 'BNC', 8, 'Analog Out')], cols=2, rows=5),
          rm('R2S', 'Split rear module (2 cards, 1 in, 4 out each)', 2, [R('in', 'Analog video', 'BNC', 1, 'Analog In'), R('out', 'Analog video', 'BNC', 4, 'Analog Out')],
             cpm=2, cols=1, rows=5)],
         note + f' {w} W. The R2 module leaves position 2 unused.', f'Ross {pn} product page and rear module drawings',
         OGP + f'distribution/{id}/', watts=w)
card('sra-8802', 'SRA-8802', 'SRA-8802 3G/HD/SD reclocking DA with A/B failover', 'openGear distribution',
     da_r2('3G-SDI') + [rm('R2R', 'Rear module with relay bypass (input to first output)', 2, [R('in', '3G-SDI', 'BNC', 1, 'In'), R('out', '3G-SDI', 'BNC', 8, 'Out')], cols=2, rows=5)],
     'Reclocking 3G/HD/SD DA (also DVB-ASI) with long-reach input EQ: 1x8 with R2 (A/B input failover), 1x4 with the split R2S, or R2R with a '
     'relay bypass from the input to the first output. Check: R2R layout (no drawing on the page) and which R2 position is the B input.',
     'Ross SRA-8802 product page and rear module drawings', OGP + 'distribution/sra-8802/', verified=False)
card('sea-8803', 'SEA-8803', 'SEA-8803 HD/SD equalising DA', 'openGear distribution', da_r2('HD-SDI'),
     'HD/SD-SDI equalising DA (also DVB-ASI), 200 m at HD, 500 m at SD: 1x8 with R2, 1x4 with the split R2S.',
     'Ross SEA-8803 product page and rear module drawings', OGP + 'distribution/sea-8803/')
card('dea-8805', 'DEA-8805', 'DEA-8805 dual HD/SD equalising DA', 'openGear distribution',
     [rm('R2', '10 BNC rear module (dual 1x4)', 2, [R('in', 'HD-SDI', 'BNC', 1, 'In Ch A'), R('in', 'HD-SDI', 'BNC', 1, 'In Ch B'),
                                                    R('out', 'HD-SDI', 'BNC', 4, 'Out A'), R('out', 'HD-SDI', 'BNC', 4, 'Out B')], cols=2, rows=5),
      rm('R2H', '18 HD-BNC rear module (dual 1x8)', 2, [R('in', 'HD-SDI', 'HD-BNC', 1, 'In Ch A'), R('in', 'HD-SDI', 'HD-BNC', 1, 'In Ch B'),
                                                       R('out', 'HD-SDI', 'HD-BNC', 8, 'Out A'), R('out', 'HD-SDI', 'HD-BNC', 8, 'Out B')], cols=2)],
     'Two independent HD/SD-SDI equalising DAs, each channel at its own rate: dual 1x4 with R2 or dual 1x8 with R2H.',
     'Ross DEA-8805 product page and rear module drawings', OGP + 'distribution/dea-8805/')
card('ada-8405-c', 'ADA-8405-C', 'ADA-8405-C analog audio DA (1x8 or dual 1x4)', 'openGear audio',
     [rm('R2C', 'Rear module (2 in, 8 out)', 2, [R('in', 'Analog audio', 'Terminal block', 2, 'Analog In'), R('out', 'Analog audio', 'Terminal block', 8, 'Analog Out')], cols=2, rows=5),
      rm('R2CS', 'Split rear module (2 cards, 1 in, 4 out each)', 2, [R('in', 'Analog audio', 'Terminal block', 1, 'Analog In'),
                                                                     R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out')], cpm=2, cols=1, rows=5)],
     'Balanced analog audio DA with +/-15 dB software gain and summing: 8 copies of a mono input or 4 of each of a stereo pair (Out 1-1 to 1-4 '
     'follow In 1, Out 2-1 to 2-4 follow In 2). Also distributes LTC. 2.6 W. 3-pin pluggable terminal blocks.',
     'Ross ADA-8405-C product page and rear module drawings', OGP + 'distribution/ada-8405-c/', watts=2.6)

# ---- conversion, embedding, audio ----
card('hdc-8223a-s', 'HDC-8223A-S', 'HDC-8223A-S 3G/HD/SD DA with down converter and frame sync', 'openGear conversion',
     [rm('R2', 'Rear module', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 4, 'Reclocked Copy Out'),
                                  R('out', 'Analog video', 'BNC', 4, 'SDI/CVBS Out')], cols=2, rows=5),
      rm('R2C', 'Analog audio rear module', 2, [R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'Reclocked Copy Out'),
                                               R('out', 'Analog audio', 'Terminal block', 4, 'Analog Audio Out'), R('out', 'Analog video', 'BNC', 2, 'SDI/CVBS Out')], cols=2, rows=5)],
     '2 in (A/B) / 4 out reclocking DA whose SDI/CVBS outputs can each be SDI or analog composite with 10-bit HD down conversion; the -S version '
     'adds a frame synchroniser and audio sample-rate conversion. The same rear modules fit the HDC-8223A (no frame sync). 8 W.',
     'Ross HDC-8223A-S product page and rear module drawings', OGP + 'conversion/hdc-8223a-s/', watts=8)
for v, n, w in (('4C', 4, 9.5), ('8C', 8, 11)):
    card(f'mux-8258-{v.lower()}', f'MUX-8258-{v}', f'MUX-8258-{v} {n} ch analog audio embedder', 'openGear audio',
         [rm('R2C', 'Rear module', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
                                       R('in', 'Analog audio', 'Terminal block', n, 'Analog In')], cols=2, rows=5)],
         f'Embeds {n} balanced analog audio channels into 3G/HD/SD-SDI with per-input gain, invert, delay and summing. {w} W.'
         + (' The shared R2C module has 8 analog positions; the -4C uses the first 4.' if n == 4 else ''),
         'Ross MUX-8258-4C/8C product page and rear module drawing', OGP + 'audio-embedding/mux-8258-4c-8c/', watts=w)
    card(f'dmx-8259-{v.lower()}', f'DMX-8259-{v}', f'DMX-8259-{v} {n} ch analog audio de-embedder', 'openGear audio',
         [rm('R2C', 'Rear module', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
                                       R('out', 'Analog audio', 'Terminal block', n, 'Analog Out')], cols=2, rows=5)],
         f'De-embeds {n} channels from 3G/HD/SD-SDI to balanced analog outputs; any embedded channel to any output, with gain, delay and invert. {w} W.',
         'Ross DMX-8259-4C/8C product page and rear module drawing', OGP + 'audio-embedding/dmx-8259-4c-8c/', watts=w)
card('adc-8434-a', 'ADC-8434-A', 'ADC-8434-A quad analog to dual AES converter', 'openGear audio',
     [rm('R2A', '75 ohm rear module', 2, [R('in', 'Analog audio', 'Terminal block', 4, 'Analog In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out')], cols=2, rows=5)],
     '4 balanced analog channels to 2 unbalanced AES3 streams (24-bit, 32-96 kHz); each AES stream comes out on two BNCs (AES Out 1, 1, 2, 2). 4 W.',
     'Ross ADC-8434-A product page and rear module drawing', OGP + 'conversion/adc-8434-a/', watts=4)
card('aap-8644', 'AAP-8644', 'AAP-8644 advanced audio processor (Dolby, loudness)', 'openGear audio',
     [rm('R2C-8644', 'Double-width rear module (4 slots) with SDI relay bypass', 4,
         [R('in', '3G-SDI', 'BNC', 4, 'SDI In'), R('out', '3G-SDI', 'BNC', 8, 'SDI Out'), R('in', 'AES/EBU', 'BNC', 8, 'AES In'),
          R('out', 'AES/EBU', 'BNC', 8, 'AES Out'), R('in', 'Analog audio', 'Terminal block', 4, 'Analog In'), R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out'),
          R('in', 'Analog video', 'BNC', 1, 'CVBS In'), R('out', 'Analog video', 'BNC', 1, 'CVBS Out'), R('io', 'GPIO', 'RJ45', 1, 'GPIO/COMM'),
          R('io', 'Ethernet', 'RJ45', 1, 'Ethernet')])],
     '3G/HD/SD audio processor: Dolby encode/decode, real-time loudness levelling, upmix, embed/de-embed, optional A/V QC with hardware relay '
     'bypass. 24 W with DSP options. Double-width card on a 4-slot rear module. Check: exact BNC split on the R2C-8644 module (counts from the '
     'spec table: up to 4 SDI in, 4 x 2 SDI out, 8 AES in, 8 AES out).',
     'Ross AAP-8644 product page', OGP + 'processing-monitoring/aap-8644/', verified=False, slotWidth=2, watts=24)

# ---- timing ----
card('spg-8260-w', 'SPG-8260-W', 'SPG-8260-W sync pulse generator with word clock', 'openGear sync',
     [rm('R2', 'Full rear module', 2, [R('out', 'Reference', 'BNC', 8, 'Ref Out'), R('out', 'Word clock', 'BNC', 2, 'Word Clock')], cols=2, rows=5),
      rm('R2S', 'Split rear module (2 cards)', 2, [R('out', 'Reference', 'BNC', 4, 'Ref Out'), R('io', 'Reference', 'BNC', 1, 'Ref In / Word Clock')], cpm=2, cols=1, rows=5)],
     '4 output pairs (1A-4A, 1B-4B), each tri-level, black burst or colour bars at its own frame rate and timing; 48 kHz TTL word clock. Locks '
     'to frame REF 1/2, a local reference or its internal oscillator. 6 W. Check: whether one of the two R2 word clock BNCs is the local ref input.',
     'Ross SPG-8260-W product page and rear module drawings', OGP + 'timing-synchronization/spg-8260-w/', watts=6, verified=False)
SFS = OGP + 'timing-synchronization/sfs-8622-a/'
SFS_SDI = [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 2, 'SDI Out')]
for sfx, mod, name, extra in (
        ('A', 'R2A', '6 AES (75 ohm)', [R('io', 'AES/EBU', 'BNC', 6, 'AES I/O')]),
        ('AIC', 'R2AC', '4 analog in, 4 AES', [R('in', 'Analog audio', 'Terminal block', 4, 'Analog In'), R('io', 'AES/EBU', 'BNC', 4, 'AES I/O')]),
        ('AOC', 'R2AC', '4 analog out, 4 AES', [R('out', 'Analog audio', 'Terminal block', 4, 'Analog Out'), R('io', 'AES/EBU', 'BNC', 4, 'AES I/O')]),
        ('IC', 'R2C', '8 analog in', [R('in', 'Analog audio', 'Terminal block', 8, 'Analog In')]),
        ('OC', 'R2C', '8 analog out', [R('out', 'Analog audio', 'Terminal block', 8, 'Analog Out')]),
        ('B', 'R2B', '8 balanced AES', [R('io', 'AES/EBU', 'Terminal block', 8, 'AES I/O')])):
    card(f'sfs-8622-{sfx.lower()}', f'SFS-8622-{sfx}', f'SFS-8622-{sfx} 3G/HD/SD frame sync, {name}', 'openGear timing',
         [rm(mod, f'{mod} rear module', 2, SFS_SDI + extra, cols=2, rows=5)],
         f'A/V frame synchroniser with up to 28 frames of delay, 16-channel embed/de-embed, format auto-detect and a test pattern on input loss. '
         f'Ordered as SFS-8622-{sfx}-{mod if sfx not in ("AIC", "AOC") else "R2" + sfx}. The rear module adds {name}.',
         'Ross SFS-8622-A product page and rear module drawings', SFS)
card('dss-8224', 'DSS-8224', 'DSS-8224 dual HD/SD video switch (2x1 or 4x2)', 'openGear switching',
     [rm('R2', 'Rear module (4x2)', 2, [R('in', 'HD-SDI', 'BNC', 4, 'In'), R('out', 'HD-SDI', 'BNC', 4, 'Out (1A, 1B, 2A, 2B)'),
                                        R('in', 'GPI', 'BNC', 2, 'Panel / GPI')], cols=2, rows=5),
      rm('R2S', 'Split rear module (2 cards, 2x1 each)', 2, [R('in', 'HD-SDI', 'BNC', 2, 'In'), R('out', 'HD-SDI', 'BNC', 2, 'Out'),
                                                            R('in', 'GPI', 'BNC', 1, 'Panel / GPI')], cpm=2, cols=1, rows=5)],
     'Vertical-interval video switch timed to frame reference: two independent 2x1 switches or one 4x2, reclocked outputs. Controlled from '
     'DashBoard, GPI or an RCM-8120 panel over BNC. 4.5 W.', 'Ross DSS-8224 product page and rear module drawings',
     OGP + 'processing-monitoring/dss-8224/', watts=4.5)

# ---- monitoring, data ----
card('nwe-3ga', 'NWE-3GA', 'NWE-3GA Nielsen watermark encoder', 'openGear audience measurement',
     [rm('R2', 'Rear module with relay bypass', 2, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out'),
                                                    R('in', 'AES/EBU', 'BNC', 4, 'AES In'), R('out', 'AES/EBU', 'BNC', 4, 'AES Out'),
                                                    R('in', 'Timecode', 'Terminal block', 1, 'LTC (balanced)'), R('in', 'Timecode', 'BNC', 1, 'LTC (unbalanced)'),
                                                    R('io', 'RS-232', 'RJ45', 1, 'Serial')])],
     'Inserts Nielsen watermarks into up to 16 PCM channels from the 16 embedded and 8 AES channels; relay bypass of video and AES on the rear '
     'module. Power-hungry: up to 5 per 2RU frame, or 1 alongside up to 16 other cards.',
     'Ross NWE-3GA product page and rear module drawing', OGP + 'processing-monitoring/nwe-3ga/')
for v, i, o in (('I16', 16, 0), ('I32', 32, 0), ('O16', 0, 16), ('O32', 0, 32), ('I16-O16', 16, 16)):
    ports = ([R('in', 'GPI', 'DB37', i // 16, 'GPI In (16 per D-sub)')] if i else []) + ([R('out', 'GPI', 'DB37', o // 16, 'GPI Out (16 per D-sub)')] if o else [])
    card(f'gpi-8941-{v.lower()}', f'GPI-8941-{v}', f'GPI-8941-{v} GPI card ({i} in, {o} out)'.replace(' (0 in, ', ' (').replace(', 0 out)', ')'),
         'openGear GPIO', [rm('R3', 'Rear module', 2, ports, gen=3)],
         'General purpose interface card: opto-isolated inputs (contact closure or voltage sense) and isolated relay outputs (contact closure or '
         'voltage source); each bank of 16 is on a 37-pin D-sub. Up to 10 per 2RU frame.',
         'Ross GPI-8941 product page', OGP + 'data-solutions/gpi-8941/', gen=3)

# ---- passive optical ----
CW = OGP + 'fiber/cwdm/'
for pn, kind, lam, exp in (('FCM-6844', 'mux', '1350, 1370, 1430, 1450', True), ('FCD-6845', 'demux', '1350, 1370, 1430, 1450', True),
                           ('FCM-6846', 'mux', '1270-1450', False), ('FCD-6847', 'demux', '1270-1450', False),
                           ('FCM-6848', 'mux', '1470-1610', True), ('FCD-6849', 'demux', '1470-1610', True)):
    n = 4 if lam.count(',') == 3 else 8
    ports = [R('io', 'Fibre', 'LC', 1, 'Common')] + ([R('io', 'Fibre', 'LC', 1, 'Expansion')] if exp else []) + \
            [R('in' if kind == 'mux' else 'out', 'Fibre', 'LC', n, 'Channel')]
    card(pn.lower(), pn, f'{pn} {n}-channel CWDM {"multiplexer" if kind == "mux" else "demultiplexer"}', 'openGear fibre',
         [rm(pn, 'Integrated rear', 2, ports)],
         f'Passive {n}-channel CWDM {kind} ({lam} nm), LC/UPC, no power. Card and rear are one piece (no separate rear module). '
         + ('The expansion port cascades a second module for 12 or 16 channels.' if exp else 'No expansion port.'),
         'Ross CWDM product page and module drawings', CW, watts=0)
for pn, dual, n in (('FSS-6802', False, 2), ('FDS-6803', True, 2), ('FSS-6804', False, 4), ('FDS-6805', True, 4), ('FSS-6808', False, 8)):
    k = 2 if dual else 1
    card(pn.lower(), pn, f'{pn} {"dual " if dual else ""}1x{n} optical splitter', 'openGear fibre',
         [rm(pn, 'Latching rear', 2, [R('in', 'Fibre', 'LC', k, 'Optical In'), R('out', 'Fibre', 'LC', k * n, 'Optical Out')])],
         f'Passive {"dual " if dual else ""}1x{n} optical splitter, 1270-1620 nm, LC/UPC, no power. Check: rear module width and LC layout.',
         'Ross optical splitters product page', OGP + 'fiber/optical-splitters/', verified=False, watts=0)

# ======================= rack units =======================
U = []
def unit(id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=True, **kw):
    m = dict(id='ross-' + id, manufacturer='Ross Video', partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w,
             fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); U.append(m)
IEC2 = lambda: R('in', 'Power', 'IEC C14', 2, 'PSU')
AC = 'https://www.rossvideo.com/master-control/live-event-protection-delay/aircleaner-2/specifications/'
for mdl, dly in (('A', '80 s HD / 40 s 1080p / 10 s UHD'), ('B', '160 s HD / 80 s 1080p / 20 s UHD'), ('C', '360 s HD / 180 s 1080p / 45 s UHD')):
    unit(f'aircleaner-2-{mdl.lower()}', f'AirCleaner-2 Model-{mdl}', f'AirCleaner-2 Model-{mdl} live event delay', 'AirCleaner', 'other', 2,
         [IEC2(), R('io', 'SFP', 'QSFP28', 2, 'IP Video (100G)'), R('in', '12G-SDI', 'HD-BNC', 1, 'AUX In'), R('out', '12G-SDI', 'HD-BNC', 1, 'TAP Out'),
          R('in', '12G-SDI', 'HD-BNC', 1, 'PGM In'), R('out', '12G-SDI', 'HD-BNC', 1, 'PGM Out'), R('in', 'Reference', 'HD-BNC', 1, 'Ref In'),
          R('out', 'Reference', 'HD-BNC', 1, 'Ref Loop'), R('io', 'GPI', 'DB9', 1, 'GPI I/O (panels, tally)'), R('io', 'AES/EBU', 'DB25', 1, 'AES I/O (8 ch, Tascam)'),
          R('out', 'Analog audio', '3.5mm jack', 1, 'Monitor'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'USB', 'USB-A', 1, 'USB 2.0')],
         f'Live profanity/event delay ({dly} at 59.94) with jumble/bleep and panic buttons; 16 embedded audio tracks per SDI; 2110 over two QSFP28 '
         'links. 2RU, 600 mm deep, about 12 kg, two hot-swap supplies, under 500 W; power-loss bypass battery. Optional AirCleaner hardware '
         'control panel (two panic buttons) on the GPI port.', 'Ross AirCleaner-2 specifications page and rear photo', AC, powerW=500, weightKg=12.25)
XP = 'https://www.rossvideo.com/products/graphics-and-virtual/xpression/'
XPV = lambda bi, ins=0, extra=(): [R('out', '12G-SDI', 'HD-BNC', 4, 'SDI Out')] if not bi else [R('io', '12G-SDI', 'HD-BNC', 4, 'SDI I/O (bi-dir)')] + \
    ([R('in', '12G-SDI', 'HD-BNC', ins, 'SDI In')] if ins else []) + list(extra)
XPC = lambda eth: [R('in', 'Reference', 'BNC', 1, 'Ref In')] + eth + [R('out', 'DisplayPort', 'DisplayPort', 4, 'GPU DP'), R('io', 'RS-232', 'DB9', 1, 'RS-232')]
unit('xpn-1ru-m9', 'XPN-1RU-M9', 'XPression 1RU SDI graphics server (M9)', 'XPression', 'graphics', 1,
     [IEC2(), R('out', '3G-SDI', 'HD-BNC', 4, 'SDI Out'), R('io', '3G-SDI', 'HD-BNC', 4, 'SDI I/O (bi-dir)')] +
     XPC([R('io', 'Ethernet', 'RJ45', 1, '1G'), R('io', 'Ethernet', 'RJ45', 1, '10G')]) + [R('io', 'USB', 'USB-A', 2, 'USB 3.1'), F('io', 'USB', 'USB-A', 2, 'USB 3.1'), F('io', 'USB', 'USB-C', 2, 'USB-C')],
     'Up to 4 channels (video/key pairs) of 1080p, or 1 quad-link UHD out. Embedded audio only; GPI is RossTalk over TCP/IP. HP Z4 G5 '
     'rackmount, 438 x 656 x 43 mm, 12.4 kg, 2 x 675 W redundant supplies.',
     'XPression 1RU SDI hardware specs (3509DR-549)', XP, depth_mm=656, weightKg=12.42, powerW=675)
unit('xpn-1ru-12g-m9', 'XPN-1RU-12G-M9', 'XPression 1RU 12G graphics server (M9)', 'XPression', 'graphics', 1,
     [IEC2(), R('io', '12G-SDI', 'HD-BNC', 4, 'SDI I/O (bi-dir)'), R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In')] +
     XPC([R('io', 'Ethernet', 'RJ45', 1, '1G'), R('io', 'Ethernet', 'RJ45', 1, '10G')]) + [R('io', 'USB', 'USB-A', 2, 'USB 3.1'), F('io', 'USB', 'USB-A', 2, 'USB 3.1'), F('io', 'USB', 'USB-C', 2, 'USB-C')],
     '4 bi-directional 12G channels (video/key pairs up to UHD) plus 2 inputs up to UHD. Embedded audio only; GPI over TCP/IP. 438 x 656 x 43 mm, '
     '12.4 kg, 2 x 675 W redundant supplies.', 'XPression 1RU 12G hardware specs (3509DR-562)', XP, weightKg=12.42, powerW=675)
unit('xpression-2ru-sdi', 'XPression 2RU SDI (M9)', 'XPression 2RU SDI graphics server (M9)', 'XPression', 'graphics', 2,
     [IEC2(), R('out', '3G-SDI', 'HD-BNC', 4, 'SDI Out'), R('io', '3G-SDI', 'HD-BNC', 4, 'SDI I/O (bi-dir)')] +
     XPC([R('io', 'Ethernet', 'RJ45', 1, '1G'), R('io', 'Ethernet', 'RJ45', 1, '2.5G'), R('io', 'Ethernet', 'RJ45', 2, '10G'), R('io', 'Ethernet', 'RJ45', 1, 'IPMI')]) +
     [R('io', 'USB', 'USB-A', 6, 'USB'), R('out', 'Other', 'VGA', 1, 'VGA')],
     'Up to 4 video/key pairs of 1080p or 1 quad-link UHD out; embedded audio only. 482 x 525 x 88 mm, 12.4 kg, 2 x 550 W supplies. '
     'Also 2RU 12G and 2RU IP D25L versions.', 'XPression 2RU SDI hardware specs (3509DR-515-01)', XP, weightKg=12.42, powerW=550)
unit('xpression-4ru-12g', 'XPression 4RU 12G (M9)', 'XPression 4RU 12G graphics server (M9)', 'XPression', 'graphics', 4,
     [IEC2(), R('io', '12G-SDI', 'HD-BNC', 4, 'SDI I/O (bi-dir)'), R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In'), R('io', 'GPI', 'DB25', 1, 'GPI (12 in, 12 out)'),
      R('in', 'Timecode', 'Other', 1, 'LTC In')] +
     XPC([R('io', 'Ethernet', 'RJ45', 1, '1G'), R('io', 'Ethernet', 'RJ45', 1, '2.5G'), R('io', 'Ethernet', 'RJ45', 2, '10G'), R('io', 'Ethernet', 'RJ45', 1, 'IPMI')]) +
     [R('io', 'USB', 'USB-A', 6, 'USB'), R('out', 'Other', 'VGA', 1, 'VGA')],
     'One UHD video/key channel on 4 bi-directional 12G HD-BNCs plus 2 UHD inputs; physical GPI (12 in, 12 out on a 25-pin D-sub) and LTC in. '
     '430 x 592 x 176 mm, 25.9 kg, 2 x 960 W hot-swap redundant supplies. Also 4RU SDI, 12G LL and IP versions. Check: LTC connector.',
     'XPression 4RU 12G hardware specs (3509DR-568-01)', XP, weightKg=25.9, powerW=960)
TUHD = 'https://www.rossvideo.com/live-production/video-servers-replay/production-servers/tria-uhd/specifications/'
unit('tria-plus-uhd', 'Tria+ UHD', 'Tria+ UHD 2-channel 12G production server', 'Tria', 'recorder', 3,
     [IEC2(), R('in', '12G-SDI', 'HD-BNC', 2, 'SDI In'), R('out', '12G-SDI', 'HD-BNC', 2, 'SDI Out'), R('in', 'Reference', 'HD-BNC', 1, 'Ref In'),
      R('in', 'Timecode', 'XLR', 1, 'LTC In'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet (10G)'), R('io', 'USB', 'USB-A', 6, 'USB'), R('io', 'USB', 'USB-C', 1, 'USB-C'),
      R('out', 'DisplayPort', 'Mini DisplayPort', 4, 'GUI Display')],
     'Two bi-directional 12G channels (2160p or 1080p, record or play). 3RU, 651 mm deep, up to 34 kg, dual hot-swap supplies (12 A at 100 V). '
     'SSD storage 9.5 or 28.8 TB RAID-5. Check: LTC XLR (seen on the rear photo; not in the spec table).',
     'Ross Tria+ UHD specifications page and rear photo', TUHD, weightKg=34)
TED = 'https://www.rossvideo.com/live-production/video-servers-replay/production-servers/tria-express-duet/specifications/'
for ch in (2, 4):
    unit(f'tria-express-duet-{ch}ch', f'Tria Express Duet {ch} channel', f'Tria Express Duet {ch}-channel production server', 'Tria', 'recorder', 2,
         [IEC2(), R('in', '3G-SDI', 'BNC', ch, 'SDI In'), R('out', '3G-SDI', 'BNC', ch, 'SDI Out'), R('out', '3G-SDI', 'BNC', 1, 'Quad Viewer'),
          R('in', 'Reference', 'BNC', 1, 'Ref In'), R('in', 'Timecode', 'XLR', 1, 'LTC In'), R('io', 'RS-422', 'DB9', 2, 'RS-422'),
          R('io', 'Ethernet', 'RJ45', 1, 'Ethernet (1G)'), R('io', 'AES/EBU', 'DB25', 1, 'AES I/O (8 in, 8 out)'), R('out', 'Analog audio', '3.5mm jack', 1, 'Monitor'),
          R('io', 'USB', 'USB-A', 6, 'USB'), R('out', 'DisplayPort', 'DisplayPort', 2, 'GUI Display'), R('out', 'HDMI', 'HDMI', 1, 'GUI Display')],
         f'Compact production server, {ch} bi-directional HD/3G channels (AVC-Intra 100), each record or play; the 2-channel model upgrades to 4 in '
         'the field. 2RU, 406 mm deep, up to 13.6 kg, dual hot-swap supplies. SSD storage options.',
         'Ross Tria Express Duet specifications page and rear photo', TED, full=False, weightKg=13.6)
KP = 'https://www.rossvideo.com/live-production/video-servers-replay/presentation-server/kiva-plus/'
for n in (1, 2, 3):
    unit(f'kiva-plus-{n}', f'Kiva+ {n} channel pair{"s" if n > 1 else ""}', f'Kiva+ presentation server, {n} channel pair{"s" if n > 1 else ""}', 'Kiva', 'recorder', 3,
         [IEC2(), R('in', '3G-SDI', 'HD-BNC', n, 'SDI In (record)'), R('out', '3G-SDI', 'HD-BNC', 4 * n, 'PVW/PGM Video+Key Out'),
          R('out', '3G-SDI', 'HD-BNC', n, 'Quad Viewer'), R('in', 'Reference', 'HD-BNC', 1, 'Ref In'), R('in', 'Timecode', 'XLR', 1, 'LTC In'),
          R('io', 'AES/EBU', 'DB25', 2, 'AES I/O'), R('io', 'RS-422', 'RJ45', 8, 'RS-422 (octal breakout to D9)'), R('io', 'Ethernet', 'RJ45', 2, 'Ethernet (10G)'),
          R('io', 'USB', 'USB-A', 6, 'USB'), R('io', 'USB', 'USB-C', 1, 'USB-C'), R('out', 'DisplayPort', 'Mini DisplayPort', 4, 'GUI Display'),
          R('out', 'Analog audio', '3.5mm jack', n, 'Monitor')],
         f'Presentation server for screens and video walls: each channel pair is a record input plus PVW and PGM players with video and key '
         f'outputs and a quad viewer. Same 3RU chassis as Tria+ (651 mm deep, up to 34 kg, dual hot-swap supplies); pairs are added as PCIe video '
         'cards. Check: SDI out count per pair (spec page tables disagree; drawn as 4: PVW and PGM video+key).',
         'Ross Kiva+ specifications page and rear photo', KP, verified=False, weightKg=34)
KED = 'https://www.rossvideo.com/live-production/video-servers-replay/presentation-server/kiva-express-duet/specifications/'
unit('kiva-express-duet', 'Kiva Express Duet', 'Kiva Express Duet presentation server (1 channel pair)', 'Kiva', 'recorder', 2,
     [IEC2(), R('in', '3G-SDI', 'BNC', 1, 'SDI In (record)'), R('out', '3G-SDI', 'BNC', 4, 'PVW/PGM Video+Key Out'), R('out', '3G-SDI', 'BNC', 1, 'Quad Viewer'),
      R('in', 'Reference', 'BNC', 1, 'Ref In'), R('in', 'Timecode', 'XLR', 1, 'LTC In'), R('io', 'RS-422', 'DB9', 2, 'RS-422 (PGM, PVW)'),
      R('io', 'Ethernet', 'RJ45', 1, 'Ethernet (1G)'), R('io', 'AES/EBU', 'DB25', 1, 'AES I/O (8 in, 8 out)'), R('out', 'Analog audio', '3.5mm jack', 1, 'Monitor'),
      R('io', 'USB', 'USB-A', 6, 'USB'), R('out', 'DisplayPort', 'DisplayPort', 2, 'GUI Display'), R('out', 'HDMI', 'HDMI', 1, 'GUI Display')],
     'Compact presentation server: one record input, PVW and PGM players with video and key outputs, quad viewer. 2RU, 406 mm deep, up to '
     '13.6 kg, dual hot-swap supplies, 1.9 or 3.84 TB SSD.', 'Ross Kiva Express Duet specifications page and rear photo', KED, full=False, weightKg=13.6)
unit('rm-9940', 'RM-9940', 'RM-9940 1RU passive CWDM chassis (3 modules)', 'openGear fibre', 'shelf', 1, [],
     'Passive 1RU chassis for up to three 16-channel CWDM modules (FCM-9941-16 mux, FCD-9942-16 demux), 483 x 250 x 44 mm. No power.',
     'Ross CWDM product page', OGP + 'fiber/cwdm/', full=False, carrier={'bays': 3, 'fits': ['Ross RM-9940 CWDM module']})
for pn, kind in (('FCM-9941-16', 'multiplexer'), ('FCD-9942-16', 'demultiplexer')):
    unit(pn.lower(), pn, f'{pn} 16-channel CWDM {kind} module', 'openGear fibre', 'converter', 1,
         [R('io', 'Fibre', 'LC', 1, 'Common'), R('in' if kind == 'multiplexer' else 'out', 'Fibre', 'LC', 16, 'Channel')],
         f'Passive 16-channel CWDM {kind} (1270-1610 nm), LC/UPC, for the RM-9940 chassis (three per 1RU). Check: connector layout.',
         'Ross CWDM product page', OGP + 'fiber/cwdm/', verified=False, w=4, full=False, formFactor='Ross RM-9940 CWDM module')
RCM = 'https://www.rossvideo.com/products/signal-processing/opengear/processing-monitoring/rcm-8120/'
unit('mrp-8120', 'MRP-8120', 'MRP-8120 1RU panel for five RCM-8120 modules', 'openGear switching', 'shelf', 1, [],
     '1RU 19 in mounting panel that holds up to five RCM-8120 / RCM-8120-1 remote control modules; BPM-8120 blanks the empty positions.',
     'Ross RCM-8120 product page', RCM, full=False, carrier={'bays': 5, 'fits': ['Ross RCM-8120 module']})
for pn, btn in (('RCM-8120', 4), ('RCM-8120-1', 2)):
    unit(pn.lower(), pn, f'{pn} {btn}-button remote control module', 'openGear switching', 'control', 1,
         [R('out', 'GPI', 'BNC', 1, 'Logic control (to DSS-8224 / AVS-8764)'), R('in', 'GPI', 'Terminal block', 1, 'Panel Enable'),
          R('io', 'GPI', 'Terminal block', 2, 'GPI')],
         f'{btn} lit selector buttons for a DSS-8224 or AVS-8764 switch card ({"4x1 or dual 2x1" if btn == 4 else "2x1"}); the logic signal runs '
         'over ordinary BNC video cable to the card\'s Panel/GPI input. Fits the MRP-8120 1RU panel (five per RU). Check: connector types.',
         'Ross RCM-8120 product page', RCM, verified=False, w=2, full=False, formFactor='Ross RCM-8120 module')
unit('ultrigpi', 'ULTRIGPI', 'UltriGPI 16 in / 16 out GPI network bridge', 'Ultrix', 'control', 1,
     [R('in', 'GPI', 'Terminal block', 1, 'GPI In (16, spring clamp)'), R('out', 'GPI', 'Terminal block', 1, 'GPI Out (16, spring clamp)'),
      R('io', 'Ethernet', 'RJ45', 1, 'Network (PoE 802.3af)'), R('in', 'Power', 'DC barrel', 1, 'DC In (9-30 V)')],
     '16 GPI inputs and 16 outputs bridged to the network for Ultricore/Ultrix control. Powered by PoE or the included 15 V supply (ULTRIGPI-PS '
     'spare); 5 W max. 119 x 162 x 44 mm stackable box, no rack kit listed. Check: which end each connector is on.',
     'Ross UltriGPI specifications PDF', 'https://www.rossvideo.com/infrastructure/routing-systems/ultrigpi/', w=3, full=False,
     powerW=5, boxMm={'w': 119, 'h': 44})
unit('txi-48', 'TXI-48', 'TXI-48 tally expansion interface (48 GPI)', 'Tally', 'control', 1,
     [R('io', 'GPI', 'D-sub', 3, 'GPI I/O (16 per connector)'), R('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), R('io', 'RS-422', 'Other', 1, 'RS-422/485 cascade')],
     'Up to 48 tally/GPI points in 1RU, 16 per I/O connector, each connector set as inputs or outputs (dry or jumper-set wet inputs, isolated '
     'relay outputs). Ethernet to the TSI tally controller; cascade over TCP/IP or RS-422/485. Check: connector types, power input.',
     'Ross TXI-48 product page', 'https://www.rossvideo.com/products/signal-processing/txi-48/', verified=False, full=False)

for fn, data in (('ross-opengear.json', OG), ('ross-more.json', U)):
    ids = [m['id'] for m in data]; assert len(ids) == len(set(ids)), fn
    for m in data:
        for r in m.get('rearModules', []):
            assert sum(1 for x in m['rearModules'] if x['default']) == 1, m['id']
            assert r['width'] >= m['card']['slotWidth'] or r['cardsPerModule'] > 1, m['id']
    json.dump(data, open(os.path.join(CAT, fn), 'w'), indent=1, ensure_ascii=False)
    print(fn, len(data), 'entries,', sum(m['verified'] for m in data), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for fn in ('ross-opengear.json', 'ross-more.json'):
    if fn not in idx: idx.append(fn)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
