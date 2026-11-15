#!/usr/bin/env python3
"""Rack hardware and signal distribution (added 2026-11-15).
  catalogue/rack-hardware.json        Blank, vented and brush panels, horizontal cable managers (D-ring, micro-clip, hinged), lacing bars,
                                      fixed and sliding shelves, keyboard shelves and drawers: Middle Atlantic, Penn Elcom and generic templates.
  catalogue/signal-distribution.json  L-band splitters (ETL), timecode (LTC) DAs (ESE, Brainstorm, Alice), analogue video / black burst DA (ESE),
                                      GPIO breakout panels (TSL BP-32, Evertz TR-4800E-BHP) and generic GPIO, RS-422, RF and SDI templates.
Drawing flags: vent:true (slots) and brush:true (brush strip) are drawn by the app. cableMgr ('dring', 'clip', 'cover', 'finger', 'lacing')
says what a cable manager looks like; until the app draws it, it shows as a plain panel. Lacing bars carry mountDefault:'rear'
(they normally go on the rear rails; set "Mounted on" to Rear rails when placing).
Not added here (other generators own them): tie-line and D-series panels, jackfields, wall/floor boxes (tiepanels.py, jackfields.py);
master clocks, sync generators and IRDs (timing_rf.py); openGear/densite/Synapse DA cards (already in the frame files).
verified=True only where the maker's sheet or a dealer listing gave the layout; the rest have notes starting "Check:"."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
HW, SD = 'rack-hardware.json', 'signal-distribution.json'
def model(file, **m):
    m = dict(dict(widthCols=12, fullDepth=False, verified=False, portGroups=[]), **m)
    FILES.setdefault(file, []).append(m)

# ============================ Middle Atlantic ============================
MA = 'Middle Atlantic'
MA_EB = ('Middle Atlantic EB series blank panel specifications', 'https://manualmachine.com/middleatlantic/df1269/24513113-blank-panelseb-series-specifications')
MA_CM = ('Middle Atlantic cable management product guide', 'https://media.onlinecomponents.com/productfiles/mf-mda/pgurl_cablem.pdf')
MA_U = ('Middle Atlantic U series shelves specifications', 'https://manualmachine.com/middleatlantic/df2979/24513073-u-series-shelves-specifications')
def ma(id, pn, name, family, cat, ru, src, notes, verified=True, **kw):
    model(HW, id='middleatlantic-' + id, manufacturer=MA, partNumber=pn, name=name, family=family, category=cat, ru=ru,
          verified=verified, source=src[0], productUrl=src[1], notes=notes, **kw)
for n in range(1, 7):
    ma(f'eb{n}', f'EB{n}', f'EB{n} blank panel, {n}U, flanged steel, black', 'Blank panels', 'blank', n, MA_EB,
       f'{n}U flanged steel blank, black powder coat. SB{n} is the textured version' + (f' and BL{n} the black aluminium one' if n <= 4 else '') + '.',
       depthMm=15)
for n in range(1, 5):
    ma(f'vt{n}', f'VT{n}', f'VT{n} vent panel, {n}U, perforated, 63% open', 'Vent panels', 'blank', n,
       ('Middle Atlantic VT1 listing (Creation Networks)', 'https://creationnetworks.net/products/middle-atlantic-vt1-1sp-perforated-vent-panel'),
       f'{n}U perforated steel vent panel, about 63% open area. VTF-{n} is the 23% open version. Check: part number spelling (VT{n} or VT-{n}).',
       verified=False, vent=True, depthMm=15)
for n in (1, 2):
    ma(f'br{n}', f'BR{n}', f'BR{n} brush grommet panel with cable tray, {n}U', 'Cable management', 'blank', n, MA_CM,
       f'{n}U brush grommet panel for passing cables front to back, with a built-in cable tray behind it.', brush=True, depthMm=100)
for pn, n, kind, desc in (('HCM-1', 1, 'clip', 'micro-clip horizontal cable manager'), ('HCM-1D', 1, 'dring', 'D-ring horizontal cable manager'),
                          ('HCM-2D', 2, 'dring', 'D-ring horizontal cable manager'), ('HCM-1DR', 1, 'dring', 'D-ring horizontal cable manager, front and rear rings'),
                          ('HCM-2DR', 2, 'dring', 'D-ring horizontal cable manager, front and rear rings'),
                          ('HHCM-1', 1, 'cover', 'hinged horizontal cable manager, 3.5 in deep'), ('HHCM-2', 2, 'cover', 'hinged horizontal cable manager, 3.5 in deep')):
    ma(pn.lower(), pn, f'{pn} {desc}, {n}U', 'Cable management', 'blank', n, MA_CM,
       f'{n}U {desc}. ' + ('HCM-%dDV adds end rings. ' % n if pn.endswith('D') else '') + 'Leave one between patch panels and the gear they feed.',
       cableMgr=kind, depthMm=90 if kind != 'cover' else 89)
for pn, desc in (('LBP-1A', 'straight L bar with cable-tie slots'), ('LBP-2A', 'L bar, 2 in offset'), ('LBP-4A', 'L bar, 4 in offset'),
                 ('LBP-6A', 'L bar, 6 in offset'), ('LBP-1R', 'straight round rod'), ('LBP-1.5', 'round rod, 1.5 in offset'),
                 ('LBP-1R4', 'round rod, 4 in offset'), ('LBP-1S', 'rectangular aluminium bar')):
    ma(pn.lower().replace('.', '-'), pn, f'{pn} lacing bar, {desc}', 'Lacing bars', 'blank', 1, MA_CM,
       f'Lacing bar ({desc}) for tying cables at the back of the rack; sold in packs of 10. It fixes to the rails at one RU and normally goes '
       'on the rear rails: set "Mounted on" to Rear rails.', cableMgr='lacing', mountDefault='rear', depthMm=25)
for pn, ru, d, cap, extra in (('U1', 1, 273, 16, ''), ('U2', 2, 370, 23, ''), ('U3', 3, 370, 32, ''), ('U4', 4, 394, 39, ''),
                              ('U317', 3, 454, 27, ' Slotted rear flange for cable management.')):
    ma(pn.lower(), pn, f'{pn} vented rack shelf, {ru}U, {d} mm deep', 'Rack shelves', 'shelf', ru, MA_U,
       f'{ru}U front-mount vented cantilever shelf, {d} mm deep, holds about {cap} kg.{extra}', depthMm=d)
ma('sshd-28', 'SSHD-28', 'SSHD-28 heavy-duty sliding shelf, 2U, 714 mm', 'Rack shelves', 'shelf', 2, MA_U,
   '2U sliding shelf on four-post rails, 714 mm (28.1 in) deep, holds about 91 kg. Check: depth range of the rails.', verified=False,
   fullDepth=True, depthMm=714)
ma('kb-ss', 'KB-SS', 'KB-SS keyboard sliding shelf, 1U', 'Rack shelves', 'shelf', 1,
   ('Middle Atlantic KB-SS listing (Pacific Radio)', 'https://pacrad.com/middle-atlantic-kb-ss-1ru-keyboard-sliding-shelf.html'),
   '1U sliding keyboard shelf for four-post racks with 17 to 25 in (432 to 635 mm) between rails. Keyboard up to 15-15/16 x 9-3/8 in.',
   fullDepth=True, depthMm=432)

# ============================ Penn Elcom ============================
PE = 'Penn Elcom'
def pe(pn, name, family, ru, src, notes, verified=False, **kw):
    model(HW, id='pennelcom-' + pn.lower().replace('/', '-'), manufacturer=PE, partNumber=pn, name=name, family=family, category='blank',
          ru=ru, verified=verified, source=src[0], productUrl=src[1], notes=notes, **kw)
for n in range(1, 5):
    pe(f'R1268/{n}UK', f'R1268/{n}UK blank rack panel, {n}U, flanged black steel', 'Blank panels', n,
       ('Penn Elcom R1268/1UK listing (Farnell)', 'https://uk.farnell.com/penn-elcom/r1268-1uk/1u-blank-plate/dp/3371430'),
       f'{n}U flanged blank panel, black steel.' + ('' if n == 1 else ' Check: part number (same series as R1268/1UK).'), verified=n == 1, depthMm=15)
for n in range(1, 4):
    pe(f'R1268/{n}UVK', f'R1268/{n}UVK vented rack panel, {n}U, louvred, black', 'Vent panels', n,
       ('Penn Elcom R1268/1UVK product page', 'https://www.penn-elcom.com/us/1u-black-flanged-rack-panel-with-louvered-vents-r1268-1uvk'),
       f'{n}U flanged black steel panel with louvred vents.', verified=True, vent=True, depthMm=15)
pe('R1268/1UK-PBS', 'R1268/1UK-PBS brush panel, 1U, cable access slot with brushes', 'Cable management', 1,
   ('Penn Elcom R1268/1UK-PBS product page', 'https://penn-elcom.com/cn/1u-black-rack-panel-with-cable-access-slot-and-brushes-r1268-1uk-pbs'),
   '1U black panel with a brush-sealed slot for passing cables through.', verified=True, brush=True, depthMm=15)
pe('R1268/1UK-PBSO', 'R1268/1UK-PBSO open brush panel, 1U (slot open at one end)', 'Cable management', 1,
   ('Penn Elcom R1268/1UK-PBSO product page', 'https://www.penn-elcom.com/ca/1u-open-black-rack-panel-with-cable-access-slot-and-brushes-r1268-1uk-pbso'),
   'As R1268/1UK-PBS but the slot is open at one end, so cables with connectors already fitted can be dropped in.', verified=True, brush=True, depthMm=15)

# ============================ Generic rack hardware templates ============================
def gen(id, pn, name, family, cat, ru, notes, **kw):
    model(HW, id='hw-generic-' + id, manufacturer='Generic', partNumber=pn, name=name, family=family, category=cat, ru=ru,
          source='Generic template', notes=notes + ' Template: set the maker and part number.', **kw)
gen('brush-2u', 'Brush panel 2U', 'Brush panel, 2U', 'Cable management', 'blank', 2, '2U panel with a brush-sealed cable slot.', brush=True, depthMm=15)
for n in (1, 2):
    gen(f'dring-{n}u', f'D-ring cable manager {n}U', f'D-ring horizontal cable manager, {n}U', 'Cable management', 'blank', n,
        f'{n}U horizontal cable manager with D-rings.', cableMgr='dring', depthMm=90)
    gen(f'finger-{n}u', f'Finger duct cable manager {n}U', f'Finger duct horizontal cable manager with cover, {n}U', 'Cable management', 'blank', n,
        f'{n}U slotted finger duct (horizontal wire manager) with a snap-on cover, as used between patch panels and switches.', cableMgr='finger', depthMm=80)
gen('lacing-bar', 'Lacing bar', 'Lacing bar (rear)', 'Lacing bars', 'blank', 1,
    'Cable lacing bar at the back of the rack. Set "Mounted on" to Rear rails.', cableMgr='lacing', mountDefault='rear', depthMm=25)
gen('shelf-vented-1u', 'Vented shelf 1U', 'Vented cantilever rack shelf, 1U', 'Rack shelves', 'shelf', 1,
    '1U front-mount vented shelf, about 300 mm deep.', depthMm=300)
gen('shelf-sliding-1u', 'Sliding shelf 1U', 'Sliding rack shelf, 1U, four-post', 'Rack shelves', 'shelf', 1,
    '1U sliding shelf on telescopic rails for four-post racks.', fullDepth=True, depthMm=600)
gen('kbd-drawer-1u', 'Keyboard drawer 1U', 'Keyboard and mouse drawer, 1U, sliding', 'Rack shelves', 'shelf', 1,
    '1U sliding keyboard and mouse tray for four-post racks.', fullDepth=True, depthMm=450)
for n in (2, 3, 4):
    gen(f'drawer-{n}u', f'Rack drawer {n}U', f'Lockable rack drawer, {n}U', 'Rack drawers', 'shelf', n,
        f'{n}U lockable sliding drawer for cables, adaptors and tools.', depthMm=400)

# ============================ L-band / RF splitters ============================
ETL = 'ETL Systems'
model(SD, id='etl-d0108d1ulp-22429', manufacturer=ETL, partNumber='D0108D1ULP-22429-xxxx', name='Dual 8-way passive L-band splitter, 1U (DC and 10 MHz pass on port 1)',
      family='L-band splitters', category='other', ru=1, verified=True, depthMm=350,
      source='ETL Systems data sheet D0108D1ULP-22429', productUrl='https://etlsystems.com/sites/default/files/products/downloads/D0108D1ULP-22429-xxxx%20V1.1.pdf',
      notes='Two passive 8-way L-band (850-2150 MHz) splitter/combiners in 1U, 350 mm deep. Inputs on the rear, outputs on the front. DC and 10 MHz '
            'pass on port 1 only (for LNB power and reference). The -xxxx suffix sets the connectors: 50 ohm SMA, N or BNC, 75 ohm BNC or F (shown as 75 ohm F).',
      portGroups=[R('in', 'RF', 'F', 2, 'RF In'), F('out', 'RF', 'F', 16, 'RF Out')])
model(SD, id='etl-d0108s1ula-22351', manufacturer=ETL, partNumber='D0108S1ULA-22351-xxxx', name='Active 8-way L-band splitter, 1U, dual PSU',
      family='L-band splitters', category='other', ru=1, depthMm=350, powerW=20,
      source='ETL Systems product page', productUrl='https://www.etlsystems.com/catalogue/rack-systems/splitter-divider/l-band-splitter-active-8-way-10mhz-pass',
      notes='Active (gain-compensated) 8-way L-band splitter, 1U, 350 mm deep, dual redundant PSUs, 10 MHz pass between port 1 and common. Connector suffix: '
            'B5B5 50 ohm BNC, B7B7 75 ohm BNC, F7F7 75 ohm F, N5N5 N, S5S5 SMA (shown as F). Check: which face the ports are on, and power draw.',
      portGroups=[R('in', 'RF', 'F', 1, 'RF In'), F('out', 'RF', 'F', 8, 'RF Out'), R('in', 'Power', 'IEC', 2, 'PSU')])
model(SD, id='sd-generic-rf-splitter-4x4', manufacturer='Generic', partNumber='RF splitter panel 4 x 1:4', name='Passive RF / L-band splitter panel, 4 x 1:4, 1U',
      family='RF splitters', category='other', ru=1, source='Generic template', depthMm=150,
      notes='Four passive 4-way splitters (5-2400 MHz) on F connectors, inputs on the rear and outputs on the front. One port usually passes DC for LNB '
            'power. Template: set the maker, part number and connectors.',
      portGroups=[R('in', 'RF', 'F', 4, 'RF In'), F('out', 'RF', 'F', 16, 'RF Out')])
model(SD, id='sd-generic-sdi-da-2x8', manufacturer='Generic', partNumber='SDI DA 2 x 1:8', name='12G-SDI reclocking distribution amplifier, 2 x 1:8, 1U',
      family='SDI DAs', category='converter', ru=1, source='Generic template', powerW=15,
      notes='Two 1-in, 8-out reclocking 12G/3G/HD-SDI DAs in 1U with dual PSUs. SDI should not be split passively: use a reclocking DA. '
            'For openGear, densite or Synapse frames use their DA cards instead. Template: set the maker and part number.',
      portGroups=[R('in', '12G-SDI', 'BNC', 2, 'SDI In'), R('out', '12G-SDI', 'BNC', 16, 'SDI Out'), R('in', 'Power', 'IEC', 2, 'PSU')])

# ============================ Timecode, reference and analogue video DAs ============================
model(SD, id='ese-es-246-bnc', manufacturer='ESE', partNumber='ES-246/BNC', name='ES-246/BNC quad 1x6 SMPTE LTC / IRIG time code DA, BNC',
      family='Time code DAs', category='other', ru=1, powerW=5,
      source='ESE ES-246/BNC listing (B&H)', productUrl='https://www.bhphotovideo.com/c/product/1206155-REG/ese_es_246_bnc_quad_1_x_6.html',
      notes='Four independent 1x6 time code DAs, each with an input and a loop-through, six unbalanced 600 ohm outputs, all on rear BNCs. '
            'Check: rack height (1U shown) and whether the loop is a separate BNC.',
      portGroups=[R('in', 'Timecode', 'BNC', 4, 'TC In'), R('out', 'Timecode', 'BNC', 4, 'TC Loop'), R('out', 'Timecode', 'BNC', 24, 'TC Out'),
                  R('in', 'Power', 'IEC', 1, 'AC')])
model(SD, id='ese-es-246-xlr', manufacturer='ESE', partNumber='ES-246/XLR', name='ES-246/XLR quad 1x6 audio / time code DA, XLR',
      family='Time code DAs', category='audio', ru=1, powerW=5,
      source='ESE ES-246/XLR listing (Markertek)', productUrl='https://www.markertek.com/product/es-246-xlr/ese-es-246-quad-1x6-rack-mount-audio-distribution-amplifier-with-xlr-option-110-120-vac',
      notes='Four 1x6 balanced audio DAs on XLRs, 20 Hz-20 kHz, inputs switchable 600 ohm / 100 kohm; also used for SMPTE and IRIG time code. '
            'Listed as no longer available. Check: rack height (1U shown).',
      portGroups=[R('in', 'Analog audio', 'XLR3F', 4, 'In'), R('out', 'Analog audio', 'XLR3M', 24, 'Out'), R('in', 'Power', 'IEC', 1, 'AC')])
model(SD, id='ese-es-247e', manufacturer='ESE', partNumber='ES-247E', name='ES-247E quad 1x6 composite video / black burst DA, 1U',
      family='Video DAs', category='converter', ru=1,
      source='ESE ES-247E listing (Markertek)', productUrl='https://www.markertek.com/product/es-247e-bk/ese-quad-1x6-video-da-1-rack-space-black',
      notes='Four 1x6 analogue composite video DAs on BNCs in 1U; often used to distribute black burst reference. Black or clear faceplate. '
            'Check: looping inputs and tri-level sync support.',
      portGroups=[R('in', 'Analog video', 'BNC', 4, 'Video In'), R('out', 'Analog video', 'BNC', 24, 'Video Out'), R('in', 'Power', 'IEC', 1, 'AC')])
model(SD, id='brainstorm-sr-28', manufacturer='Brainstorm Electronics', partNumber='SR-28', name='SR-28 time code distributor / reshaper, 2 in, 8 out',
      family='Time code DAs', category='other', ru=1, verified=True, depthMm=206, powerW=16,
      source='Brainstorm SR-28 listing (Full Compass)', productUrl='https://fullcompass.com/prod/232153-brainstorm-electronics-sr-28-time-code-distributor-reshaper',
      notes='1U time code distributor and reshaper: two XLR time code inputs, eight outputs on one DB25, 206 mm deep. 12 V DC 1.3 A on two '
            '4-pin inputs for redundant supplies with automatic changeover.',
      portGroups=[R('in', 'Timecode', 'XLR3F', 2, 'TC In'), R('out', 'Timecode', 'DB25', 1, 'TC Out 1-8'), R('in', 'Power', 'Other', 2, 'DC In (4-pin)')])
ALICE = ('Alice LTC Timecode DA tech spec (HHB)', 'https://www.hhb.co.uk/wp-content/uploads/Alice-TC-DA-Rack-LTC-Tech-Spec-v5.pdf')
for t, inp, outs, desc in (('A', ('XLR3F', 'XLR'), [('XLR3M', 6), ('BNC', 6)], 'XLR in, 6 XLR + 6 BNC out'), ('C', ('BNC', 'BNC'), [('BNC', 12)], 'BNC in, 12 BNC out')):
    model(SD, id=f'alice-tc-da-{t.lower()}', manufacturer='Alice', partNumber=f'Timecode DA type {t}', name=f'LTC timecode DA, 1U, type {t} ({desc})',
          family='Time code DAs', category='other', ru=1, verified=True, powerW=20, source=ALICE[0], productUrl=ALICE[1],
          notes=f'1U LTC distribution amplifier: one input, twelve outputs in two banks of six, 85-285 V AC. Type {t}: {desc}. Other types: '
                'B XLR in / 12 XLR, D BNC in / 12 XLR, E BNC in / 6 XLR + 6 BNC, F XLR in / 12 BNC.',
          portGroups=[R('in', 'Timecode', inp[0], 1, 'TC In')] + [R('out', 'Timecode', c, n, f'TC Out {c[:3]}') for c, n in outs] + [R('in', 'Power', 'IEC', 1, 'AC')])

# ============================ GPIO and RS-422 breakout panels ============================
model(SD, id='tsl-bp-32', manufacturer='TSL', partNumber='BP-32', name='BP-32 GPIO breakout panel, 32 GPI + 32 GPO, 2U',
      family='GPIO breakout', category='other', ru=2,
      source='TSL BP-32 product page (formerly DNF Controls)', productUrl='https://www.tslproducts.com/products/tsl-control/control-glue/gpio-breakout-panel/bp-32',
      notes='2U breakout for the GTP-32 GPI/tally processor, USP3 switch panels and AIB interface boxes: 32 GPI and 32 GPO on pluggable 2-pin '
            'terminals, wet or dry per point by jumper, dual power supplies included. Cable kit: four DB37 cables (GTP-32) or four DB25 (USP3/AIB). '
            'Check: which face the terminals are on (all shown on the rear) and the power inlet.',
      portGroups=[R('in', 'GPIO', 'DB37', 2, 'GPI link'), R('out', 'GPIO', 'DB37', 2, 'GPO link'), R('in', 'GPIO', 'Phoenix', 32, 'GPI'),
                  R('out', 'GPIO', 'Phoenix', 32, 'GPO'), R('in', 'Power', 'Other', 2, 'PSU')])
model(SD, id='evertz-tr-4800e-bhp', manufacturer='Evertz', partNumber='TR-4800E-BHP', name='TR-4800E-BHP GPIO bulkhead panel for the TR-4800E tally router, 2U',
      family='GPIO breakout', category='other', ru=2,
      source='Evertz TR4800-BHP product page', productUrl='https://evertz.com/products/TR4800-BHP',
      notes='2U bulkhead panel that breaks the TR-4800E tally router GPIO DB37s out to 2-pin terminal blocks so the wiring can be remote. '
            'Per-point wet/dry slide switches, strain-relief bar, five 2 m DB37 cables included. Check: GPI count (the page says 32 and 48).',
      portGroups=[R('in', 'GPIO', 'DB37', 1, 'GPI link'), R('out', 'GPIO', 'DB37', 1, 'GPO link'), R('in', 'GPIO', 'Terminal block', 32, 'GPI'),
                  R('out', 'GPIO', 'Terminal block', 48, 'GPO')])
model(SD, id='sd-generic-gpio-breakout-1u', manufacturer='Generic', partNumber='GPIO breakout 1U 2xDB25', name='GPIO breakout panel, 1U, 2 x DB25 to 48 terminals',
      family='GPIO breakout', category='patch', ru=1, source='Generic template',
      notes='Passive panel that breaks two DB25 GPI/GPO cables out to 48 screw or Phoenix terminals (24 each). Template: set the maker, part number and pinout.',
      portGroups=[R('io', 'GPIO', 'DB25', 2, 'GPIO link'), F('io', 'GPIO', 'Phoenix', 48, 'GPIO')])
model(SD, id='sd-generic-rs422-breakout-1u-16', manufacturer='Generic', partNumber='RS-422 breakout 1U 16', name='RS-422 breakout panel, 1U, 16 x DB9 to terminals',
      family='RS-422 breakout', category='patch', ru=1, source='Generic template',
      notes='Passive panel for machine-control tie lines: 16 DB9 female (Sony 9-pin) on the front, each wired to a 5-way terminal on the rear '
            '(Tx+, Tx-, Rx+, Rx-, ground). Template: set the maker and part number.',
      portGroups=[F('io', 'RS-422', 'DB9F', 16, 'RS-422'), R('io', 'RS-422', 'Phoenix', 16, 'RS-422 wire')])

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
