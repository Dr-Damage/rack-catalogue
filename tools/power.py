#!/usr/bin/env python3
"""Rack UPSs and power strips from Eaton, Vertiv (Liebert / Geist) and Raritan (added 2026-11-14):
  catalogue/eaton.json        Eaton 5PX G2 and 9PX rack/tower UPSs (230 V), ePDU G3 metered input 0U strip.
  catalogue/vertiv.json       Vertiv Liebert GXT5 rack/tower online UPSs (230 V), Vertiv Geist rPDU basic 0U strip.
  catalogue/raritan-pdu.json  Raritan PX3 intelligent PDU (raritan.json holds the Raritan KVM gear from tools/kvm.py).
UPSs use category 'power' like apc.json (outlets as portGroups). Strips use category 'pdu' with a 'pdu' block (catalogue/README.md).
Specs from the makers' data sheets (each entry's source)."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=12, fullDepth=False,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
def ups(file, id, mfr, pn, name, fam, ru, inlet, c13, c19, comms, notes, src, url, **kw):
    ports = [R('in', 'Power', inlet, 1, 'AC In'), R('out', 'Power', 'IEC C13', c13, 'Outlet')]
    if c19: ports.append(R('out', 'Power', 'IEC C19', c19, 'Outlet C19'))
    add(file, id, mfr, pn, name, fam, 'power', ru, ports + comms, notes, src, url, **kw)

# ======================= Eaton =======================
EA = 'Eaton'
E5_SRC, E5_URL = 'Eaton 5PX G2 data sheet (ANZ)', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-5px-g2-ups.html'
E5_COM = [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'Other', 'Terminal block', 1, 'Remote ON/OFF / RPO'),
          R('io', 'Other', 'Card slot', 1, 'Comms slot (NETWORK-M2)'), R('io', 'Other', 'Battery connector', 1, 'External battery (EBM)')]
for va, inlet, c13, c19, ebm, d, kg, chk in ((1500, 'IEC C14', 8, 0, 'EBM48RT2U', 448, 22.4, ''), (2000, 'IEC C14', 8, 0, 'EBM72RT2U', 603, 28.0, ''),
                                             (2200, 'IEC C20', 8, 2, 'EBM72RT2U', 603, 28.2, ''),
                                             (3000, 'IEC C20', 8, 2, 'EBM72RT2U', 603, 31.7, 'Check: outlet layout (the data sheet table is unclear; shown as on the 2200). ')):
    pn = f'5PX{va}IRT2UG2' if va < 2200 else f'5PX{va}IRT2UAUG2'
    ups('eaton.json', 'eaton-' + pn.lower(), EA, pn, f'5PX G2 {va} VA rack/tower UPS 2U, 230 V', '5PX G2', 2, inlet, c13, c19, E5_COM,
        f'Line-interactive, {va} VA / {va} W, 2U rack/tower. Outlets in switchable groups. Extended runtime with {ebm} battery modules. '
        f'{d} mm deep, {kg} kg. ' + ('3U version: 5PX%dIRT3UAUG2 (483 mm deep). ' % va if va >= 2200 else '') + chk
        + 'Check: comms port positions (from the 3000 VA listing).', E5_SRC, E5_URL, verified=not chk, weightKg=kg)
ups('eaton.json', 'eaton-9px3000irt2u', EA, '9PX3000IRT2U', '9PX 3000 VA online rack/tower UPS 2U, 230 V', '9PX', 2, 'IEC C20', 8, 2,
    [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('in', 'Other', 'Terminal block', 1, 'Remote power off'),
     R('io', 'Other', 'Terminal block', 1, 'Relay out (3 out, 1 in)'), R('io', 'Other', 'Card slot', 1, 'Comms slot'),
     R('io', 'Other', 'Battery connector', 1, 'External battery (EBM)')],
    'Double-conversion online, 3000 VA / 3000 W. Up to 4 EBMs. 605 mm deep, 27.6 kg. 1.8 m C20 input cord.',
    'Eaton 9PX3000IRT2U product data sheet', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-9px-ups.html',
    weightKg=27.6)
add('eaton.json', 'eaton-emib04', EA, 'EMIB04', 'ePDU G3 metered input 0U, 16 A, 20 x C13 + 4 x C19', 'ePDU G3', 'pdu', 1,
    [R('io', 'Ethernet', 'RJ45', 1, 'LAN'), R('io', 'USB', 'USB-A', 1, 'USB')],
    '0U metered-input strip, 3.7 kW, billing-grade input metering with a hot-swap meter and LCD. Up to four strips daisy-chain on one '
    'network connection. 1070 mm long, 52 x 53 mm section, 3 kg. IEC 60309 16 A plug on a 3 m cord. Check: breaker layout (not given).',
    'Eaton EMIB04 listing (Redcorp)', 'https://www.eaton.com/au/en-gb/catalog/backup-power-ups-surge-it-power-distribution/eaton-epdu-g3-metered-input.html',
    pdu=dict(mount='v', lengthMm=1070, widthMm=52, cordEnd='bottom', phase=1, volts=230, amps=16, plug='cee16', cordM=3, metering='meter',
             circuits=[dict(id='A', type='none')], outlets=[dict(type='c13', count=10, circuit='A'), dict(type='c19', count=4, circuit='A'),
                                                            dict(type='c13', count=10, circuit='A')]))

# ======================= Vertiv =======================
VT = 'Vertiv'
GX_SRC, GX_URL = 'Vertiv Liebert GXT5 750-3000 VA 230 V brochure (EMEA rev 4)', 'https://www.vertiv.com/en-emea/products-catalog/critical-power/uninterruptible-power-supplies-ups/liebert-gxt5-ups-500-3000va/'
GX_COM = [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'RS-232', 'DB9', 1, 'RS-232'), R('io', 'Other', 'Card slot', 1, 'IntelliSlot'),
          R('io', 'Other', 'Terminal block', 1, 'Dry contacts (4)'), R('io', 'Other', 'Battery connector', 1, 'External battery cabinet')]
for va, inlet, c13, c19, ebc, d, kg in ((750, 'IEC C14', 8, 0, 'GXT5-EBC36VRT2U', 400, 16.8), (1000, 'IEC C14', 8, 0, 'GXT5-EBC36VRT2U', 400, 16.8),
                                        (1500, 'IEC C14', 8, 0, 'GXT5-EBC48VRT2U', 470, 21.4), (2000, 'IEC C20', 8, 0, 'GXT5-EBC48VRT2U', 470, 21.4),
                                        (3000, 'IEC C20', 6, 1, 'GXT5-EBC72VRT2U', 540, 28.5)):
    pn = f'GXT5-{va}IRT2UXL'
    ups('vertiv.json', 'vertiv-' + pn.lower(), VT, pn, f'Liebert GXT5 {va} VA online rack/tower UPS 2U, 230 V', 'Liebert GXT5', 2, inlet, c13, c19, GX_COM,
        f'Double-conversion online, {va} VA / {va} W, 2U (85 mm) rack/tower. Programmable outlet groups. External battery cabinet {ebc}. '
        f'{d} mm deep, {kg} kg. The ...UXLN version ships with an RDU120 network card in the IntelliSlot. Check: comms port positions.',
        GX_SRC, GX_URL, weightKg=kg)
add('vertiv.json', 'vertiv-vp7551', VT, 'VP7551', 'Geist rPDU basic 0U, 16 A, 20 x C13 + 4 x C19', 'Geist rPDU', 'pdu', 1, [],
    'Basic (unmetered) 0U strip, 3.6 kW. C13s in banks of 4, 6, 6 and 4; C19s individual. No breakers. 978 mm long, 51 x 51 mm section. '
    'IEC 60309 16 A IP44 plug on a 3 m cord. Check: outlet order along the strip.',
    'Vertiv Geist rPDU VP7551 data sheet', 'https://www.vertiv.com/en-emea/products-catalog/critical-power/power-distribution/',
    pdu=dict(mount='v', lengthMm=978, widthMm=51, cordEnd='bottom', phase=1, volts=230, amps=16, plug='cee16', cordM=3, metering='none',
             circuits=[dict(id='A', type='none')],
             outlets=[dict(type='c13', count=4, circuit='A'), dict(type='c19', count=2, circuit='A'), dict(type='c13', count=6, circuit='A'),
                      dict(type='c13', count=6, circuit='A'), dict(type='c19', count=2, circuit='A'), dict(type='c13', count=4, circuit='A')]))

# ======================= Raritan =======================
add('raritan-pdu.json', 'raritan-px3-5190r', 'Raritan', 'PX3-5190R', 'PX3 1U intelligent PDU, 16 A, 8 x C13, outlet metered and switched',
    'PX3', 'pdu', 1,
    [g('front', 'io', 'Ethernet', 'RJ45', 1, 'LAN'), g('front', 'io', 'USB', 'USB-A', 2, 'USB-A'), g('front', 'io', 'USB', 'USB-B', 1, 'USB-B'),
     g('front', 'io', 'RS-232', 'RJ45', 1, 'Serial'), g('front', 'io', 'Other', 'RJ45', 1, 'Sensor')],
    '1U horizontal strip, 3.68 kVA, billing-grade metering per inlet and per outlet, remote switching of each outlet (latching relays), '
    'colour LCD. Up to 32 environmental sensors, Wi-Fi and webcam by USB. 440 x 183 x 44 mm, 1.25 kg. IEC 60309 16 A plug. '
    'Check: which face carries the outlets and which the controller.', 'Raritan PX3-5190R listing (kvm-switch.de)',
    'https://www.raritan.com/products/power/power-distribution/rack-pdu', verified=False,
    pdu=dict(mount='h', phase=1, volts=230, amps=16, plug='cee16', metering='switched-outlet', circuits=[dict(id='A', type='none')],
             outlets=[dict(type='c13', count=8, circuit='A')]))

ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(ms))
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
