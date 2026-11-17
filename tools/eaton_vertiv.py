#!/usr/bin/env python3
"""More Eaton and Vertiv gear (added 2026-11-17; tools/power.py keeps writing eaton.json and vertiv.json):
  catalogue/eaton-more.json   Eaton 5P 1U rack UPSs, more 9PX (1-3 kVA 2U/3U, 6 kVA, 11 kVA power module) and their battery
                              modules, Rack ATS 16 transfer switches, Rack PDU G4 (ePDU) 0U strips.
  catalogue/vertiv-more.json  Vertiv Liebert GXE and GXT5 5-10 kVA UPSs and battery cabinets, legacy Liebert GXT4, Avocent
                              ACS 8000 serial console servers, MergePoint Unity 2 KVM over IP switches and the LRA185 LCD tray.
UPSs and transfer switches use category 'power' with their sockets as portGroups (like apc.json); strips use category 'pdu' with
a 'pdu' block (catalogue/README.md). Specs from the makers' data sheets and product pages (each entry's source); 'Check:' marks
anything the source did not give."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=12, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
def outlets(c13, c19=0, label='Outlet'):
    p = [R('out', 'Power', 'IEC C13', c13, label)] if c13 else []
    if c19: p.append(R('out', 'Power', 'IEC C19', c19, label + ' C19'))
    return p
BATT = lambda n=1, label='External battery (EBM)': R('io', 'Other', 'Battery connector', n, label)

# =====================================================================================================================
# Eaton
# =====================================================================================================================
EA = 'Eaton'
E = lambda id, *a, **k: add('eaton-more.json', 'eaton-' + id, EA, *a, **k)
E5P = ('Eaton 5P UPS data sheet', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-5p-ups.html')
E5P_COM = [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'Other', 'Terminal block', 1, 'Remote ON/OFF / RPO'),
           R('io', 'Other', 'Card slot', 1, 'Comms slot (Network-MS)')]
for va, w, c13, d, kg in ((650, 420, 4, 364, 8.6), (850, 600, 4, 509, 13.8), (1150, 770, 6, 509, 14.6), (1550, 1100, 6, 554, 19.4)):
    pn = f'5P{va}IR'
    E(pn.lower(), pn, f'5P {va} VA 1U rack UPS, 230 V', '5P', 'power', 1,
      [R('in', 'Power', 'IEC C14', 1, 'AC In')] + outlets(c13) + E5P_COM,
      f'Line-interactive, {va} VA / {w} W, 1U, {d} mm deep, {kg} kg. Internal batteries only (no battery module). USB and RS-232 '
      'cannot be used at the same time. Check: comms port positions.', *E5P, weightKg=kg)

E9 = ('Eaton 9PX UPS ANZ product page and data sheets', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-9px-ups.html')
E9_COM = [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'Other', 'Terminal block', 1, 'Remote power off'),
          R('io', 'Other', 'Terminal block', 1, 'Relay out (3 out, 1 in)'), R('io', 'Other', 'Card slot', 1, 'Comms slot'), BATT()]
for pn, va, ru, inlet, c13, c19, d, kg, ebm, chk in (
        ('9PX1000IRT2U', 1000, 2, 'IEC C14', 8, 0, 450, 17.4, '9PXEBM48RT2U', 'Check: outlet count (taken from the 9PX1500). '),
        ('9PX1500IRT2U', 1500, 2, 'IEC C14', 8, 0, 450, 18.9, '9PXEBM48RT2U', ''),
        ('9PX2200IRT2U', 2200, 2, 'IEC C20', 8, 2, 605, 25.0, '9PXEBM72RT2U', 'Check: outlet layout (taken from the 9PX3000IRT2U). '),
        ('9PX2200IRT3U', 2200, 3, 'IEC C20', 8, 2, 485, 24.5, '9PXEBM72RT3U', 'Check: outlet layout (taken from the 9PX3000IRT2U). '),
        ('9PX3000IRT3U', 3000, 3, 'IEC C20', 8, 2, 485, 27.4, '9PXEBM72RT3U', 'Check: outlet layout (taken from the 9PX3000IRT2U). ')):
    E(pn.lower(), pn, f'9PX {va} VA online rack/tower UPS {ru}U, 230 V', '9PX', 'power', ru,
      [R('in', 'Power', inlet, 1, 'AC In')] + outlets(c13, c19) + E9_COM,
      f'Double-conversion online, {va} VA / {va} W, {ru}U, {d} mm deep, {kg} kg. Extra runtime with up to 4 {ebm} battery modules. '
      f'ANZ order code {pn}ANZ. ' + chk, *E9, verified=not chk, weightKg=kg)
for pn, ru, d, kg, fits in (('9PXEBM48RT2U', 2, 450, 29.8, '9PX 1000/1500'), ('9PXEBM72RT2U', 2, 605, 39.2, '9PX 2000/2200/3000 2U'),
                            ('9PXEBM72RT3U', 3, 485, 38.2, '9PX 2200/3000 3U'), ('9PXEBM180', 3, 685, 68, '9PX 5/6 kVA'),
                            ('9PXEBM240', 3, 680, 65, '9PX 8/11 kVA and 3:1 models')):
    E(pn.lower(), pn, f'9PX external battery module {ru}U ({fits})', '9PX', 'power', ru, [BATT(2, 'Battery connector (in / daisy-chain)')],
      f'Battery module for the {fits}. {d} mm deep, {kg} kg. Chains to further modules. Check: connector positions.', *E9, weightKg=kg)
E('9px6ki', '9PX6Ki', '9PX 6 kVA online rack/tower UPS 3U, 230 V', '9PX', 'power', 3,
  [R('in', 'Power', 'Terminal block', 1, 'AC In (hardwired)'), R('out', 'Power', 'Terminal block', 1, 'Output (hardwired)')]
  + outlets(8, 2) + E9_COM,
  'Double-conversion online, 6 kVA / 5.4 kW, 3U with internal batteries, 685 mm deep, 48 kg. 9PX5Ki is the 5 kVA version. Extra '
  'runtime with 9PXEBM180 modules. Check: output sockets (8 x C13 + 2 x C19 assumed, as on the 6 kVA guide spec) and the hardwired '
  'input on ANZ models.', *E9, verified=False, weightKg=48)
E('9px11kipm', '9PX11KiPM', '9PX 11 kVA online UPS power module 3U, 230 V', '9PX', 'power', 3,
  [R('in', 'Power', 'Terminal block', 1, 'AC In (hardwired)'), R('out', 'Power', 'Terminal block', 1, 'Output (hardwired)')] + E9_COM,
  'Double-conversion online, 11 kVA / 10 kW power module with no batteries (pair with 9PXEBM240), 700 mm deep, 21 kg. 9PX8KiPM is '
  'the 8 kVA version; ...PM31 versions take 3-phase input. Output is hardwired; an optional rear distribution box adds sockets. '
  'Check: comms ports.', *E9, verified=False, weightKg=21)

ATS = ('Eaton ATS 16 product pages', 'https://www.eaton.com/au/en-gb/skuPage.EATS16N.html')
for pn, card in (('EATS16', ''), ('EATS16N', ' with network card')):
    ports = [R('in', 'Power', 'IEC C20', 2, 'AC In (A primary, B secondary)'), R('out', 'Power', 'IEC C13', 8, 'Outlet'),
             R('out', 'Power', 'IEC C19', 1, 'Outlet C19'), R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232')]
    if card: ports.append(R('io', 'Ethernet', 'RJ45', 1, 'Network-M2'))
    E(pn.lower(), pn, f'Rack ATS 16 A automatic transfer switch 1U{card}', 'ATS', 'power', 1, ports,
      '1U automatic transfer switch, 230 V 16 A: feeds the outlets from source A and switches to source B if A fails, so '
      'single-corded gear rides through a feed loss. Plug A and B into separate UPSs or circuits. Check: USB/RS-232 and network '
      'port positions.', *ATS)

G4 = ('Eaton Rack PDU G4 (EMEA) product page', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-rack-pdu-g4-emea.html')
METER = {'BA': ('basic', 'none'), 'MI': ('metered input', 'metered'), 'SW': ('switched', 'switched'), 'MA': ('managed', 'switched-outlet')}
def g4(pn, phase, amps, plug, c13, c39, length, ncirc):
    kind, met = METER[pn[2:4]]
    circ, outs = [], []
    for i in range(ncirc):
        c = dict(id='ABCDEF'[i], type='mcb' if ncirc > 1 or amps > 16 else 'none')
        if c['type'] == 'mcb': c['amps'] = 16
        if phase == 3: c['phase'] = 'L%d' % (i * 3 // ncirc + 1)
        circ.append(c)
        outs += [dict(type='c13', count=c13 // ncirc, circuit=c['id']), dict(type='c19', count=c39 // ncirc, circuit=c['id'])]
    ports = [] if kind == 'basic' else [R('io', 'Ethernet', 'RJ45', 1, 'Network'), R('io', 'USB', 'USB-A', 1, 'USB'),
                                        R('io', 'Other', 'RJ45', 1, 'Daisy chain / sensor')]
    v = 230 if phase == 1 else 400
    E(pn.lower(), pn, f'Rack PDU G4 {kind} 0U, {phase}-phase {amps} A, {c13} x C13 + {c39} x C39', 'Rack PDU G4', 'pdu', 1, ports,
      f'0U {kind} strip, {length} mm long, 52 x 53 mm section. C39 outlets are combination sockets that take a C14 or a C20 plug '
      f'(drawn as C19). {"No network" if kind == "basic" else "Network management card with daisy-chain"}. '
      f'Check: breaker layout ({ncirc} circuit{"s" if ncirc > 1 else ""} assumed) and outlet order along the strip.', *G4,
      pdu=dict(mount='v', lengthMm=length, widthMm=52, cordEnd='bottom', phase=phase, volts=v, amps=amps, plug=plug, cordM=3,
               metering=met, main=dict(type='none'), circuits=circ, outlets=outs))
g4('EVBAFC20A', 1, 16, 'c20', 12, 12, 1000, 1)
g4('EVBAF116A', 1, 16, 'cee16', 12, 12, 1000, 1)
g4('EVBAF132A', 1, 32, 'cee32', 12, 12, 1730, 2)
g4('EVMIF116A', 1, 16, 'cee16', 12, 12, 1000, 1)
g4('EVMIF132A', 1, 32, 'cee32', 12, 12, 1730, 2)
g4('EVMIF332X', 3, 32, 'cee3p32', 24, 18, 1730, 6)
g4('EVSWF116A', 1, 16, 'cee16', 12, 12, 1730, 1)
g4('EVMAF116A', 1, 16, 'cee16', 12, 12, 1000, 1)

# =====================================================================================================================
# Vertiv
# =====================================================================================================================
VT = 'Vertiv'
V = lambda id, *a, **k: add('vertiv-more.json', 'vertiv-' + id, VT, *a, **k)
GXE = ('Vertiv Liebert GXE 1-3 kVA data sheet (EMEA)', 'https://www.vertiv.com/en-emea/products-catalog/critical-power/uninterruptible-power-supplies-ups/vertiv-liebert-gxe-1000-3000va-racktower-230v-single-phase-ups/')
GXE_COM = [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'Other', 'Card slot', 1, 'IntelliSlot'), R('in', 'Other', 'Terminal block', 1, 'EPO'), BATT(1, 'External battery cabinet')]
for va, w, inlet, c19, d, kg, ebc in ((1000, 900, 'IEC C14', 0, 430, 16.0, 'GXE3-EBC24VRT2U'), (1500, 1350, 'IEC C14', 0, 430, 19.6, 'GXE3-EBC36VRT2U'),
                                      (2000, 1800, 'IEC C20', 0, 430, 22.7, 'GXE3-EBC48VRT2U'), (3000, 2700, 'IEC C20', 1, 630, 31.5, 'GXE3-EBC72VRT2U')):
    pn = f'GXE3-{va}IRT2UXL'
    V(pn.lower(), pn, f'Liebert GXE {va} VA online rack/tower UPS 2U, 230 V', 'Liebert GXE', 'power', 2,
      [R('in', 'Power', inlet, 1, 'AC In')] + outlets(8, c19) + GXE_COM,
      f'Double-conversion online, {va} VA / {w} W, 2U (86 mm), {d} mm deep, {kg} kg. Up to 4 {ebc} battery cabinets. IntelliSlot takes '
      'an IS-UNITY network card. Check: comms port positions.', *GXE, weightKg=kg)
for pn, d, kg in (('GXE3-EBC24VRT2U', 410, 16.2), ('GXE3-EBC36VRT2U', 410, 21.2), ('GXE3-EBC48VRT2U', 510, 28.6), ('GXE3-EBC72VRT2U', 630, 40.8)):
    V(pn.lower(), pn, f'Liebert GXE external battery cabinet 2U ({pn[9:12]})', 'Liebert GXE', 'power', 2,
      [BATT(2, 'Battery connector (in / daisy-chain)')], f'2U battery cabinet, {d} mm deep, {kg} kg. Check: connector positions.',
      *GXE, weightKg=kg)

GX5 = ('Vertiv Liebert GXT5 5-10 kVA brochure', 'https://www.vertiv.com/en-anz/products-catalog/critical-power/uninterruptible-power-supplies-ups/liebert-gxt5-ups-5-20kva/')
for va, nm in ((5000, '5000'), (6000, '6000'), (8000, '8000'), (10000, '10K')):
    pn = f'GXT5-{nm}IRT5UXLN'
    big = va >= 8000
    com = ([R('io', 'Other', 'Card slot', 1, 'IntelliSlot (RDU101 fitted)'), R('io', 'Other', 'Terminal block', 1, 'Dry contacts'), BATT(1, 'External battery cabinet')]
           + ([R('io', 'Other', 'Parallel port', 2, 'Parallel')] if va == 10000 else [])
           if big else
           [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Other', 'Terminal block', 1, 'RS-485'),
            R('io', 'Other', 'Card slot', 1, 'IntelliSlot (RDU101 fitted)'), R('in', 'Other', 'Terminal block', 1, 'REPO'),
            R('io', 'Other', 'Terminal block', 1, 'Dry contacts'), BATT(1, 'External battery cabinet')])
    socks = outlets(0, 5) if big else []
    V(pn.lower(), pn, f'Liebert GXT5 {va // 1000} kVA online rack/tower UPS 5U, 230 V', 'Liebert GXT5', 'power', 5,
      [R('in', 'Power', 'Terminal block', 1, 'AC In (hardwired, input breaker)'), R('out', 'Power', 'Terminal block', 1, 'Output (hardwired)')]
      + socks + com,
      f'Double-conversion online, {va // 1000} kVA, 430 x 630 x 217 mm (5U), about 71-75 kg. Hardwired output terminal block'
      + (', 5 x C19 sockets and programmable C13s' if big else ' plus programmable C13 sockets and breakers') +
      '; a rear power output distribution box (PD5-CE6HDWRMBS: 2 x C19 + 6 x C13, or PD5-CE10HDWRMBS: 4 x C19 + 4 x C13) adds more. '
      'Battery cabinet GXT5-EBC192VRT3U. ' + ('Check: C13 count (not given). ' if big else 'Check: C13 socket count (not given), add them as extra ports. '),
      *GX5, verified=False, full=True)
V('gxt5-ebc192vrt3u', 'GXT5-EBC192VRT3U', 'Liebert GXT5 external battery cabinet 3U (5-10 kVA)', 'Liebert GXT5', 'power', 3,
  [BATT(2, 'Battery connector (in / daisy-chain)')],
  '3U (130 mm) cabinet, 430 x 630 mm, 57.6 kg, 16 x 12 V VRLA. The UPS detects up to 6, supports up to 10. Check: connector positions.',
  *GX5, weightKg=57.6, full=True)
GX4 = ('Vertiv Liebert GXT4 product documentation', 'https://www.vertiv.com/en-anz/support/')
for va, inlet, c13, c19 in ((1000, 'IEC C14', 6, 0), (1500, 'IEC C14', 6, 0), (2000, 'IEC C20', 6, 0), (3000, 'IEC C20', 6, 1)):
    pn = f'GXT4-{va}RT230'
    V(pn.lower(), pn, f'Liebert GXT4 {va} VA online rack/tower UPS 2U, 230 V (legacy)', 'Liebert GXT4', 'power', 2,
      [R('in', 'Power', inlet, 1, 'AC In')] + outlets(c13, c19) +
      [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Other', 'Card slot', 1, 'IntelliSlot'), BATT(1, 'External battery cabinet')],
      'Double-conversion online UPS, replaced by the GXT5. Check: outlet count and comms ports (from the family pattern).',
      *GX4, verified=False)

ACS = ('Vertiv Avocent ACS 8000 data sheet', 'https://www.vertiv.com/en-anz/products-catalog/monitoring-control-and-management/serial-consoles-and-gateways/avocent-acs-8000-serial-consoles/')
for pn, n, psu, extra in (('ACS8008SAC-400', 8, 1, ''), ('ACS8016DAC-400', 16, 2, ''), ('ACS8032MDAC-400', 32, 2, ' Built-in analogue modem.'),
                          ('ACS8048DAC-400', 48, 2, '')):
    ports = [R('io', 'RS-232', 'RJ45', n, 'Serial'), R('io', 'Ethernet', 'RJ45', 2, 'Network 1GbE'), R('io', 'SFP', 'SFP', 2, '1G SFP'),
             R('io', 'Other', 'RJ45', 1, 'Console'), R('io', 'USB', 'USB-A', 2, 'USB'),
             R('in', 'Power', 'IEC C14', psu, 'PSU' if psu > 1 else 'AC In')]
    if 'modem' in extra: ports.insert(5, R('io', 'Other', 'RJ11', 1, 'Modem'))
    V(pn.lower(), pn, f'Avocent ACS 8000 {n}-port serial console server', 'Avocent ACS 8000', 'control', 1, ports,
      f'1U, 438 x 241 mm deep, 28 W max. Out-of-band access to the serial (RS-232 console) ports of routers, switches, servers, '
      f'PDUs and broadcast kit. Ports 1 and 2 can be RS-232, RS-422 or RS-485. {"Dual" if psu > 1 else "Single"} AC supply.{extra} '
      'SAC = single AC, DAC = dual AC, MDAC = dual AC + modem, -LN/-NA = 4G LTE, SDC/DDC = -48 V DC. Check: which panel holds the '
      'serial ports, and USB count (the data sheet lists 8 USB 2.0 ports; 2 drawn).', *ACS, verified=False)
MPU = ('Vertiv Avocent MergePoint Unity 2 data sheet (EMEA)', 'https://www.vertiv.com/en-anz/products-catalog/monitoring-control-and-management/ip-kvm/vertiv-avocentmergepointunity-2-kvm-over-ip-switches/')
for pn, n, paths in (('MPU2-108DAC-400', 8, 1), ('MPU2-2016DAC-400', 16, 2), ('MPU2-2032DAC-400', 32, 2), ('MPU2-4032DAC-400', 32, 4)):
    V(pn.lower(), pn, f'Avocent MergePoint Unity 2 KVM over IP switch, {n} ports, {paths} remote path{"s" if paths > 1 else ""}', 'Avocent MergePoint Unity 2',
      'control', 1,
      [R('io', 'KVM link', 'RJ45', n, 'Device port (Cat 5 to MPUIQ/DSRIQ module)'), R('io', 'Ethernet', 'RJ45', 2, 'Network'),
       R('out', 'Other', 'VGA', 1, 'Local console VGA'), R('io', 'USB', 'USB-A', 2, 'Local console USB'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
      f'1U KVM over IP switch, {n} servers through MPUIQ / DSRIQ server interface modules (VGA, DVI, DisplayPort or HDMI targets, '
      f'1920 x 1080), {paths} simultaneous remote sessions plus a local console (pairs with the LRA185KMM LCD tray). Serial targets '
      'through MPUIQ-SRL modules. Dual internal 100-240 V supplies, 4.9 kg. Check: local console USB count and port panel.', *MPU)
V('lra185kmm', 'LRA185KMM', 'Avocent LRA185 18.5 in LCD rack console tray, 1U', 'Avocent LCD tray', 'control', 1,
  [R('in', 'Other', 'VGA', 1, 'Video In'), R('in', 'USB', 'USB-A', 1, 'Keyboard/mouse (USB)'), R('in', 'Power', 'IEC C14', 1, 'AC In')],
  '1U slide-out 18.5 in LCD, keyboard and touch pad for the local console of an Avocent KVM switch. Check: connectors and power '
  'inlet (from similar trays).', *MPU, verified=False)

# =====================================================================================================================
ids = set(json.load(open(os.path.join(CAT, 'eaton.json'))) and [m['id'] for f in ('eaton.json', 'vertiv.json') for m in json.load(open(os.path.join(CAT, f)))])
for f, items in FILES.items():
    for m in items:
        assert m['id'] not in ids, m['id']; ids.add(m['id'])
        for gp in m['portGroups']: assert gp['count'] > 0, (m['id'], gp)
    json.dump(items, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    print(f, len(items))
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
