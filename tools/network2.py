#!/usr/bin/env python3
"""Generates catalogue/arista.json, juniper.json, aruba.json, fortinet.json and dell-network.json (data-centre and campus
switches and firewalls common in IP and SMPTE ST 2110 plants). Added 2026-11-14.
Port counts, power and sizes come from each maker's datasheet or hardware guide (each entry's source). Where the guide
does not say which panel carries the console and management ports, the entry says 'Check:' and verified is False.
Network ports are on the front; power supplies on the rear."""
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

def RJ(n, label, face='front'): return g(face, 'io', 'Ethernet', 'RJ45', n, label)
def CAGE(n, conn, label=None, face='front'): return g(face, 'io', 'SFP', conn, n, label or conn)
def mgmt(face='front', usb='USB-A', console='RJ45'):
    out = [g(face, 'io', 'Ethernet', 'RJ45', 1, 'Mgmt'), g(face, 'io', 'Other', console, 1, 'Console')]
    if usb: out.append(g(face, 'io', 'USB', usb, 1, 'USB'))
    return out
def PSU(n=2, conn='IEC C14'): return R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')

# ======================= Arista =======================
AR = lambda *a, **k: add('arista.json', 'arista-', 'Arista Networks', *a, **k)
A_R3 = ('Arista 7280R3 datasheet and quick start guide (front panel figures)', 'https://www.arista.com/en/products/7280r3-series')
A_X3 = ('Arista 7050X3 datasheet and 7050 1RU Gen3 quick start guide', 'https://www.arista.com/en/products/7050x3-series')
A_20 = ('Arista 7020R datasheet', 'https://www.arista.com/en/products/7020r-series')
A_XP = ('Arista 720XP datasheet and 1RU Gen3 quick start guide (rear panel)', 'https://www.arista.com/en/products/720xp-series')
def ar(pn, name, fam, ports, notes, src, ru=1, **k):
    AR(pn.lower(), 'DCS-' + pn if not pn.startswith('720') else 'CCS-' + pn, f'{pn} {name}', fam, 'network', ru, ports,
       notes, src[0], src[1], **k)
REAR_MG = 'Management Ethernet, RS-232 console (RJ45) and USB are on the rear next to the power supplies (not on the front legend). '
ar('7280SR3-48YC8', '48 x 25G + 8 x 100G deep-buffer switch', '7280R3',
   [CAGE(48, 'SFP28', '1/10/25G'), CAGE(8, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_MG + '154 W typical / 324 W max, 1+1 hot-swap PSUs, 467 mm deep, 9.2 kg. Also sold as 7280SR3K-48YC8 (larger tables).',
   A_R3, powerW=324, weightKg=9.2)
ar('7280SR3-40YC6', '40 x 25G + 6 x 100G deep-buffer switch', '7280R3',
   [CAGE(40, 'SFP28', '1/10/25G'), CAGE(6, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_MG + '130 W typical / 214 W max, 1+1 hot-swap PSUs, 469 mm deep, 9.6 kg. 7280SR3E-40YC6 adds SyncE / PTP grandmaster features.',
   A_R3, powerW=214, weightKg=9.6)
ar('7280TR3-40C6', '40 x 10GBASE-T + 6 x 100G switch', '7280R3',
   [RJ(40, '10GBASE-T'), CAGE(6, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   'Check: management and console panel (assumed rear, as on the 40YC6). 186 W typical / 242 W max, 1+1 hot-swap PSUs, 469 mm deep.',
   A_R3, verified=False, powerW=242, weightKg=9.6)
ar('7280CR3-32P4', '32 x 100G + 4 x 400G OSFP switch', '7280R3',
   [CAGE(32, 'QSFP28', '100G'), CAGE(4, 'OSFP', '400G')] + mgmt('rear') + [PSU()],
   REAR_MG + '535 W typical / 851 W max, 1+1 hot-swap PSUs, 559 mm deep, 12.3 kg. -32D4 is the same with 4 x QSFP-DD.',
   A_R3, powerW=851, weightKg=12.3, full=True)
ar('7280CR3-32D4', '32 x 100G + 4 x 400G QSFP-DD switch', '7280R3',
   [CAGE(32, 'QSFP28', '100G'), CAGE(4, 'QSFP-DD', '400G')] + mgmt('rear') + [PSU()],
   REAR_MG + '535 W typical / 851 W max, 1+1 hot-swap PSUs, 559 mm deep, 12.3 kg.', A_R3, powerW=851, weightKg=12.3, full=True)
ar('7280CR3-36S', '28 x 100G + 6 x 200G + 2 x 400G switch', '7280R3',
   [CAGE(28, 'QSFP28', '100G'), CAGE(6, 'QSFP56', '200G'), CAGE(2, 'QSFP-DD', '400G')] + mgmt('front') + [PSU()],
   'Management Ethernet, console and USB on the front. 254 W typical / 423 W max, 1+1 hot-swap PSUs, 472 mm deep, 10.5 kg.',
   A_R3, powerW=423, weightKg=10.5)
ar('7280CR3-96', '96 x 100G switch (2RU)', '7280R3',
   [CAGE(96, 'QSFP28', '100G')] + mgmt('front') + [PSU()],
   'Management Ethernet, console and USB on the front. 1003 W typical / 1803 W max, 1+1 hot-swap PSUs, 761 mm deep, 23.6 kg.',
   A_R3, ru=2, powerW=1803, weightKg=23.6, full=True)
ar('7280DR3-24', '24 x 400G QSFP-DD switch', '7280R3',
   [CAGE(24, 'QSFP-DD', '400G')] + mgmt('front') + [PSU()],
   'Check: management and console panel. 650 W typical / 1100 W max, 1+1 hot-swap PSUs, 574 mm deep, 12.7 kg. 7280PR3-24 is the OSFP version.',
   A_R3, verified=False, powerW=1100, weightKg=12.7, full=True)
REAR_X3 = 'Management Ethernet, console and USB are on the rear (not on the front legend). '
ar('7050SX3-48YC8', '48 x 25G + 8 x 100G switch', '7050X3',
   [CAGE(48, 'SFP28', '10/25G'), CAGE(8, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_X3 + '124 W typical / 301 W max, 1+1 hot-swap PSUs (reversible airflow), 467 mm deep, 9.5 kg. A common ST 2110 leaf.',
   A_X3, powerW=301, weightKg=9.5)
ar('7050SX3-48YC12', '48 x 25G + 12 x 100G switch', '7050X3',
   [CAGE(48, 'SFP28', '10/25G'), CAGE(12, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_X3 + '170 W typical / 325 W max, 1+1 hot-swap PSUs, front-to-rear airflow only, 445 mm deep, 9.2 kg.',
   A_X3, powerW=325, weightKg=9.2)
ar('7050SX3-48C8', '48 x 10G + 8 x 100G switch', '7050X3',
   [CAGE(48, 'SFP+', '10G'), CAGE(8, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_X3 + '106 W typical / 285 W max, 1+1 hot-swap PSUs, 9.5 kg.', A_X3, powerW=285, weightKg=9.5)
ar('7050TX3-48C8', '48 x 10GBASE-T + 8 x 100G switch', '7050X3',
   [RJ(48, '1/2.5/5/10GBASE-T'), CAGE(8, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_X3 + '212 W typical / 346 W max, 1+1 hot-swap PSUs, 9.4 kg.', A_X3, powerW=346, weightKg=9.4)
ar('7050CX3-32S', '32 x 100G switch', '7050X3',
   [CAGE(32, 'QSFP28', '100G'), CAGE(2, 'SFP+', '10G')] + mgmt('front') + [PSU()],
   'Management Ethernet, console and USB on the front. 168 W typical / 343 W max, 1+1 hot-swap PSUs, 406 mm deep, 9.1 kg.',
   A_X3, powerW=343, weightKg=9.1)
ar('7050SX3-96YC8', '96 x 25G + 8 x 100G switch (2RU)', '7050X3',
   [CAGE(96, 'SFP28', '10/25G'), CAGE(8, 'QSFP28', '100G'), CAGE(2, 'SFP+', '10G')] + mgmt('rear') + [PSU()],
   'Check: management and console panel (assumed rear as on the other SX3 models). 218 W typical / 453 W max, 1+1 hot-swap PSUs, '
   '503 mm deep, 19.5 kg.', A_X3, ru=2, verified=False, powerW=453, weightKg=19.5)
REAR_20 = 'Check: management and console panel (the 7020 guide says some models have them on the rear; assumed rear). '
ar('7020SR-24C2', '24 x 10G + 2 x 100G deep-buffer switch', '7020R',
   [CAGE(24, 'SFP+', '1/10G'), CAGE(2, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_20 + '95 W typical / 105 W max, 1+1 hot-swap PSUs, 401 mm deep, 7.5 kg. 7020SRG-24C2 adds IPsec.',
   A_20, verified=False, powerW=105, weightKg=7.5)
ar('7020SR-32C2', '32 x 10G + 2 x 100G deep-buffer switch', '7020R',
   [CAGE(32, 'SFP+', '1/10G'), CAGE(2, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_20 + '160 W typical / 189 W max, 1+1 hot-swap PSUs, 347 mm deep, 6.4 kg.', A_20, verified=False, powerW=189, weightKg=6.4)
ar('7020TR-48', '48 x 1G + 6 x 10G deep-buffer switch', '7020R',
   [RJ(48, '100M/1G'), CAGE(6, 'SFP+', '1/10G')] + mgmt('rear') + [g('rear', 'io', 'USB', 'USB-A', 1, 'USB 2')] + [PSU()],
   REAR_20 + '2 USB ports. 105 W typical / 115 W max, 1+1 hot-swap PSUs, 401 mm deep, 7.7 kg. 7020TRA-48 adds features.',
   A_20, verified=False, powerW=115, weightKg=7.7)
REAR_XP = 'Management Ethernet, console and USB on the rear with the power supplies and fans (maker rear panel figure). '
ar('720XP-24Y6', '24 x 1G PoE + 6 x 25G campus switch', '720XP',
   [RJ(24, '1G PoE+'), CAGE(6, 'SFP28', '25G')] + mgmt('rear') + [PSU()],
   REAR_XP + '30 W 802.3at PoE per port, 583 W PoE budget. One 650 W PSU fitted, second slot for redundancy. 318 mm deep, 6 kg.',
   A_XP, powerW=90, weightKg=6.0)
ar('720XP-48Y6', '48 x 1G PoE + 6 x 25G campus switch', '720XP',
   [RJ(48, '1G PoE+'), CAGE(6, 'SFP28', '25G')] + mgmt('rear') + [PSU()],
   REAR_XP + '30 W 802.3at PoE per port, 982 W PoE budget. One 1050 W PSU fitted, second slot for redundancy. 318 mm deep, 6.9 kg. '
   'Often used for Dante and NDI edge ports.', A_XP, powerW=93, weightKg=6.9)
ar('720XP-24ZY4', '24 x 2.5/5G PoE + 4 x 25G campus switch', '720XP',
   [RJ(16, '2.5G PoE+'), RJ(8, '5G 60 W PoE'), CAGE(4, 'SFP28', '25G')] + mgmt('rear') + [PSU()],
   REAR_XP + '509 W PoE budget. One 650 W PSU fitted, second slot for redundancy. 375 mm deep, 6.2 kg.', A_XP, powerW=156, weightKg=6.2)
ar('720XP-48ZC2', '48 x 2.5/5G PoE + 4 x 25G + 2 x 100G campus switch', '720XP',
   [RJ(40, '2.5G PoE+'), RJ(8, '5G 60 W PoE'), CAGE(4, 'SFP28', '25G'), CAGE(2, 'QSFP28', '100G')] + mgmt('rear') + [PSU()],
   REAR_XP + '909 W PoE budget. One 1050 W PSU fitted, second slot for redundancy. 318 mm deep, 7 kg.', A_XP, powerW=156, weightKg=7.0)
ar('720XP-96ZC2', '96 x 2.5/5G PoE + 4 x 25G + 2 x 100G campus switch (2RU)', '720XP',
   [RJ(80, '2.5G 60 W PoE'), RJ(16, '5G 60 W PoE'), CAGE(4, 'SFP28', '25G'), CAGE(2, 'QSFP28', '100G')] + mgmt('rear') + [PSU(4)],
   'Check: rear layout (the rear figure shown is the 1RU model). Two 1050 W PSUs fitted, up to four; 1727 W PoE budget. 404 mm deep, 14.1 kg.',
   A_XP, ru=2, verified=False, powerW=236, weightKg=14.1)

# ======================= Juniper =======================
JU = lambda *a, **k: add('juniper.json', 'juniper-', 'Juniper Networks', *a, **k)
J44 = ('Juniper EX4400 hardware guide (models and panels) and specs page', 'https://www.juniper.net/us/en/products/switches/ex-series/ex4400-ethernet-switch.html')
J34 = ('Juniper EX3400 hardware guide (system overview)', 'https://www.juniper.net/us/en/products/switches/ex-series/ex3400-ethernet-switch.html')
J23 = ('Juniper EX2300 specs page', 'https://www.juniper.net/us/en/products/switches/ex-series/ex2300-ethernet-switch.html')
J51 = ('Juniper QFX5120 specs page and hardware guide (chassis)', 'https://www.juniper.net/us/en/products/switches/qfx-series/qfx5120-data-center-switches.html')
def ju(pn, name, fam, ports, notes, src, **k): JU(pn.lower(), pn, f'{pn} {name}', fam, 'network', 1, ports, notes, src[0], src[1], **k)
for n, poe in ((24, False), (48, False), (24, True), (48, True)):
    pn = f'EX2300-{n}{"P" if poe else "T"}'
    ju(pn, f'{n}-port 1G {"PoE+ " if poe else ""}access switch', 'EX2300',
       [RJ(n, '1G PoE+' if poe else '1G'), CAGE(4, 'SFP+', '1/10G uplink')] + mgmt('rear', usb='USB-A') + [PSU(1)],
       f'Integrated PSU and fans. {"310" if n == 48 and poe else "259"} mm deep. Uplinks: 4 x SFP+ (also Virtual Chassis). '
       'Check: management, console and USB positions.', J23, verified=False)
for n, poe, psu in ((24, False, 150), (48, False, 150), (24, True, 600), (48, True, 920)):
    pn = f'EX3400-{n}{"P" if poe else "T"}'
    ju(pn, f'{n}-port 1G {"PoE+ " if poe else ""}access switch', 'EX3400',
       [RJ(n, '1G PoE+' if poe else '1G'), CAGE(4, 'SFP+', '1/10G uplink'), F('io', 'Other', 'USB mini-B', 1, 'Console (USB)'),
        CAGE(2, 'QSFP+', '40G VC port', face='rear'), R('io', 'Other', 'RJ45', 1, 'Console'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'),
        PSU()],
       f'Two hot-removable PSU slots ({psu} W AC fitted). 4 SFP+ uplinks on the front; 2 x 40G QSFP+ (Virtual Chassis ports by default) '
       'and the RJ45 console on the rear; mini-USB console on the front. 382 mm deep with a PSU. Check: management port position.',
       J34, verified=False)
for pn, acc, psu, mp in (('24T', [RJ(24, '1G')], 550, ''), ('24P', [RJ(24, '1G PoE-bt 90 W')], 1050, ''),
                         ('24MP', [RJ(24, '100M-10G PoE-bt 90 W')], 1050, ''), ('48T', [RJ(48, '1G')], 550, ''),
                         ('48P', [RJ(48, '1G PoE-bt 90 W')], 1600, ''),
                         ('48MP', [RJ(12, '100M-10G PoE-bt'), RJ(36, '100M-2.5G PoE-bt')], 1600, ''),
                         ('48F', [CAGE(36, 'SFP', '1G'), CAGE(12, 'SFP+', '1/10G')], 550, '')):
    ju('EX4400-' + pn, 'access / aggregation switch', 'EX4400',
       acc + [CAGE(4, 'SFP28', 'Uplink module slot (EX4400-EM-4Y)'), F('io', 'Other', 'USB-C', 1, 'Console (USB-C)'),
              CAGE(2, 'QSFP28', '100G (VC / uplink)', face='rear'), R('io', 'Other', 'RJ45', 1, 'Console'),
              R('io', 'Ethernet', 'RJ45', 1, 'Mgmt'), PSU()],
       f'Front extension slot takes the optional 4 x 10/25G uplink module (shown as 4 SFP28). 2 x 100G QSFP28 on the rear. USB-C console '
       f'on the front, RJ45 console (CON) and management (MGMT) on the rear. Two PSU slots, one {psu} W AC supply fitted. 399 mm deep.',
       J44)
ju('EX4400-24X', '24 x 10G SFP+ aggregation switch', 'EX4400',
   [CAGE(24, 'SFP+', '1/10G'), CAGE(4, 'SFP28', 'Uplink module slot (EX4400-EM-4Y)'), CAGE(2, 'QSFP28', '100G')] + mgmt('front', usb='USB-C') + [PSU()],
   'On this model the QSFP28 ports, console, management and USB-C are all on the front. Two PSU slots, one 550 W fitted. 399 mm deep.', J44)
ju('QFX5120-48Y', '48 x 25G + 8 x 100G data centre switch', 'QFX5120',
   [CAGE(48, 'SFP28', '1/10/25G'), CAGE(8, 'QSFP28', '40/100G'), R('io', 'Ethernet', 'RJ45', 1, 'Mgmt C0'), R('io', 'Ethernet', 'SFP', 1, 'Mgmt C1'),
    R('io', 'Other', 'RJ45', 1, 'Console'), R('io', 'USB', 'USB-A', 1, 'USB'), PSU()],
   'Two management ports on the rear (hardware guide). Check: console and USB panel (the guide figures disagree). 247 W typical / 272 W max, '
   'two PSUs, 520 mm deep.', J51, verified=False, powerW=272)
ju('QFX5120-48T', '48 x 10GBASE-T + 6 x 100G data centre switch', 'QFX5120',
   [RJ(48, '1/10GBASE-T'), CAGE(6, 'QSFP28', '40/100G')] + mgmt('rear') + [PSU()],
   'Management port on the rear (hardware guide). Check: console and USB panel. 213 W typical / 218 W max, two PSUs, 520 mm deep.',
   J51, verified=False, powerW=218)
ju('QFX5120-32C', '32 x 100G data centre switch', 'QFX5120',
   [CAGE(32, 'QSFP28', '40/100G')] + mgmt('front') + [PSU()],
   'Management port on the front (hardware guide). 291 W typical / 310 W max, two PSUs, 515 mm deep.', J51, powerW=310)

# ======================= HPE Aruba Networking =======================
HA = lambda *a, **k: add('aruba.json', 'aruba-', 'HPE Aruba Networking', *a, **k)
H83 = ('Aruba CX 8325 data sheet', 'https://www.hpe.com/us/en/aruba-cx-8325-switch-series.html')
H86 = ('Aruba CX 8360 data sheet', 'https://www.hpe.com/us/en/aruba-cx-8360-switch-series.html')
H63 = ('Aruba CX 6300 Start Here guide and data sheet', 'https://www.hpe.com/us/en/aruba-cx-6300-switch-series.html')
H29 = ('Aruba 2930F data sheet', 'https://www.hpe.com/us/en/aruba-2930f-switch-series.html')
CXM = [g('front', 'io', 'Other', 'RJ45', 1, 'Console'), g('front', 'io', 'Other', 'USB-C', 1, 'Console (USB-C)'),
       g('front', 'io', 'Ethernet', 'RJ45', 1, 'Mgmt'), g('front', 'io', 'USB', 'USB-A', 1, 'USB')]
CXN = 'Check: console and management positions (the data sheet does not say which panel; shown on the port side). '
def ha(sku, model, name, fam, ports, notes, src, **k):
    HA(sku.lower(), sku, f'{model} {name}', fam, 'network', 1, ports, notes, src[0], src[1], verified=False, **k)
ha('JL624A', 'CX 8325-48Y8C', '48 x 25G + 8 x 100G switch', 'CX 8325', [CAGE(48, 'SFP28', '1/10/25G'), CAGE(8, 'QSFP28', '40/100G')] + CXM + [PSU()],
   CXN + 'Port-to-power airflow (JL625A is power-to-port). Two 650 W hot-swap PSUs, 6 fans, 550 W max, 536 mm deep, 10 kg.', H83, powerW=550, weightKg=10)
ha('JL626A', 'CX 8325-32C', '32 x 100G switch', 'CX 8325', [CAGE(32, 'QSFP28', '40/100G')] + CXM + [PSU()],
   CXN + 'Port-to-power airflow (JL627A is power-to-port). Two 650 W hot-swap PSUs, 550 W max, 473 mm deep, 10.9 kg.', H83, powerW=550, weightKg=10.9)
for sku, model, name, ports, pw in (
        ('JL700A', '8360-32Y4C', '32 x 25G + 4 x 100G switch', [CAGE(32, 'SFP28', '1/10/25G (4 MACsec)'), CAGE(4, 'QSFP28', '40/100G')], 425),
        ('JL702A', '8360-16Y2C', '16 x 25G + 2 x 100G switch', [CAGE(16, 'SFP28', '1/10/25G'), CAGE(2, 'QSFP28', '40/100G')], 325),
        ('JL706A', '8360-48XT4C', '48 x 10GBASE-T + 4 x 100G switch', [RJ(48, '100M/1/10GBASE-T'), CAGE(4, 'QSFP28', '40/100G')], 500),
        ('JL708A', '8360-12C', '12 x 100G switch', [CAGE(12, 'QSFP28', '40/100G')], 375),
        ('JL710A', '8360-24XF2C', '24 x 10G + 2 x 100G switch', [CAGE(24, 'SFP+', '1/10G'), CAGE(2, 'QSFP28', '40/100G')], 375)):
    ha(sku, 'CX ' + model, name, 'CX 8360', ports + CXM + [PSU()],
       CXN + f'Port-to-power airflow (the next SKU up is power-to-port). Two 550 W hot-swap PSUs, {pw} W max, 406 mm deep.', H86, powerW=pw)
for sku, name, acc, poe in (('JL658A', '24 x 10G SFP+', [CAGE(24, 'SFP+', '1/10G')], False),
                            ('JL659A', '48 x 1-5G Smart Rate class 6 PoE', [RJ(48, '1-5G PoE class 6')], True),
                            ('JL660A', '24 x 1-5G Smart Rate class 6 PoE', [RJ(24, '1-5G PoE class 6')], True),
                            ('JL661A', '48 x 1G class 4 PoE', [RJ(48, '1G PoE+')], True),
                            ('JL662A', '24 x 1G class 4 PoE', [RJ(24, '1G PoE+')], True),
                            ('JL663A', '48 x 1G', [RJ(48, '1G')], False),
                            ('JL664A', '24 x 1G', [RJ(24, '1G')], False)):
    ha(sku, 'CX 6300M', name + ' + 4 x SFP56 switch', 'CX 6300M', acc + [CAGE(4, 'SFP56', '1/10/25/50G uplink')] + CXM + [PSU()],
       CXN + 'Modular 6300M: two hot-swap PSU slots (PSUs ordered separately), stacks with VSF over the SFP56 ports. 386 mm deep.', H63)
for sku, name, acc in (('JL665A', '48 x 1G class 4 PoE', [RJ(48, '1G PoE+')]), ('JL666A', '24 x 1G class 4 PoE', [RJ(24, '1G PoE+')]),
                       ('JL667A', '48 x 1G', [RJ(48, '1G')]), ('JL668A', '24 x 1G', [RJ(24, '1G')])):
    ha(sku, 'CX 6300F', name + ' + 4 x SFP56 switch', 'CX 6300F', acc + [CAGE(4, 'SFP56', '1/10/25/50G uplink')] + CXM + [PSU(1)],
       CXN + 'Fixed 6300F: built-in PSU. 328 mm deep. 24-port PoE models limit total power to 580 W.', H63)
for sku, name, n, up, poe, d, pw in (('JL253A', '24G 4SFP+', 24, 'SFP+', 0, 200, 29), ('JL254A', '48G 4SFP+', 48, 'SFP+', 0, 246, 47),
                                     ('JL255A', '24G PoE+ 4SFP+', 24, 'SFP+', 370, 304, 445), ('JL256A', '48G PoE+ 4SFP+', 48, 'SFP+', 370, 304, 459),
                                     ('JL259A', '24G 4SFP', 24, 'SFP', 0, 200, 29), ('JL260A', '48G 4SFP', 48, 'SFP', 0, 246, 47),
                                     ('JL261A', '24G PoE+ 4SFP', 24, 'SFP', 370, 304, 445), ('JL262A', '48G PoE+ 4SFP', 48, 'SFP', 370, 304, 459)):
    ha(sku, '2930F', name + ' switch', '2930F',
       [RJ(n, '1G PoE+' if poe else '1G'), CAGE(4, up, '1/10G uplink' if up == 'SFP+' else '1G uplink'),
        F('io', 'Other', 'RJ45', 1, 'Console (RJ45 or micro-USB)'), PSU(1)],
       f'One dual-personality console port (RJ45 or USB micro-B). {"PoE+ budget %d W. " % poe if poe else ""}{d} mm deep, {pw} W max. '
       'Check: console position and fixed PSU.', H29, powerW=pw)

# ======================= Fortinet =======================
FT = lambda *a, **k: add('fortinet.json', 'fortinet-', 'Fortinet', *a, **k)
def ft(pn, name, fam, ports, notes, src, url, **k): FT(pn.lower(), pn, f'{pn} {name}', fam, 'network', 1, ports, notes, src, url, **k)
FG_URL = 'https://www.fortinet.com/products/next-generation-firewall'
ft('FG-100F', 'FortiGate next-generation firewall', 'FortiGate',
   [RJ(12, 'GE'), RJ(2, 'WAN'), RJ(1, 'MGMT/DMZ'), RJ(2, 'HA'), F('io', 'Ethernet', 'RJ45/SFP combo', 4, 'Shared media pair'),
    CAGE(4, 'SFP', 'GE SFP'), CAGE(2, 'SFP+', '10G FortiLink'), F('io', 'Other', 'RJ45', 1, 'Console'), F('io', 'USB', 'USB-A', 1, 'USB'),
    R('in', 'Power', 'IEC C14', 2, 'PSU')],
   'Dual built-in AC supplies (not hot-swap). 39 W max, 254 mm deep, 3.3 kg. 101F adds a 480 GB SSD. Check: inlet type and side.',
   'FortiGate 100F series data sheet', FG_URL, verified=False, powerW=39, weightKg=3.3)
ft('FG-200F', 'FortiGate next-generation firewall', 'FortiGate',
   [RJ(16, 'GE'), RJ(1, 'MGMT'), RJ(1, 'HA'), CAGE(8, 'SFP', 'GE SFP'), CAGE(2, 'SFP+', '10G'), CAGE(2, 'SFP+', '10G FortiLink'),
    F('io', 'Other', 'RJ45', 1, 'Console'), F('io', 'USB', 'USB-A', 1, 'USB'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
   'Dual built-in AC supplies (1+1, not hot-swap). 119 W max, 342 mm deep, 4.5 kg. 201F adds a 480 GB SSD. Check: inlet type.',
   'FortiGate 200F series data sheet', FG_URL, powerW=119, weightKg=4.5)
ft('FG-400F', 'FortiGate next-generation firewall', 'FortiGate',
   [RJ(16, 'GE'), RJ(2, 'MGMT/HA'), CAGE(8, 'SFP', 'GE SFP'), CAGE(8, 'SFP+', '10G'), F('io', 'Other', 'RJ45', 1, 'Console'),
    F('io', 'USB', 'USB-A', 1, 'USB'), PSU()],
   'Check: interface counts and PSU type (from product knowledge, the 400F data sheet was not reachable). Dual hot-swap AC PSUs.',
   'Product knowledge (FortiGate 400F)', FG_URL, verified=False)
ft('FG-600F', 'FortiGate next-generation firewall', 'FortiGate',
   [RJ(16, 'GE'), RJ(2, 'MGMT/HA'), CAGE(8, 'SFP', 'GE SFP'), CAGE(4, 'SFP+', '10G'), CAGE(4, 'SFP28', '25G ultra-low-latency'),
    F('io', 'Other', 'RJ45', 1, 'Console'), F('io', 'USB', 'USB-A', 2, 'USB'), PSU()],
   'Dual hot-swap AC PSUs. 255 W max, 380 mm deep, 7.1 kg. 601F adds 2 x 240 GB SSD.', 'FortiGate 600F series data sheet', FG_URL,
   powerW=255, weightKg=7.1)
FS_SRC, FS_URL = 'FortiSwitch Secure Access series data sheet', 'https://www.fortinet.com/products/switching/fortiswitch'
for pn, acc, up, mg, psu, poe, d in (
        ('FS-148F', [RJ(48, '1G')], [CAGE(4, 'SFP+', '10G')], False, 1, 0, 260),
        ('FS-148F-POE', [RJ(24, '1G PoE+'), RJ(24, '1G')], [CAGE(4, 'SFP+', '10G')], False, 1, 370, 310),
        ('FS-148F-FPOE', [RJ(48, '1G PoE+')], [CAGE(4, 'SFP+', '10G')], False, 1, 740, 310),
        ('FS-424E', [RJ(24, '1G')], [CAGE(4, 'SFP+', '10G')], True, 2, 0, 260),
        ('FS-424E-FPOE', [RJ(24, '1G PoE+')], [CAGE(4, 'SFP+', '10G')], True, 2, 421, 410),
        ('FS-448E', [RJ(48, '1G')], [CAGE(4, 'SFP+', '10G')], True, 2, 0, 310),
        ('FS-448E-FPOE', [RJ(48, '1G PoE+')], [CAGE(4, 'SFP+', '10G')], True, 2, 772, 410),
        ('FS-524D', [RJ(24, '1G')], [CAGE(4, 'SFP+', '10G'), CAGE(2, 'QSFP+', '40G')], True, 2, 0, 350),
        ('FS-548D', [RJ(48, '1G')], [CAGE(4, 'SFP+', '10G'), CAGE(2, 'QSFP+', '40G')], True, 2, 0, 350)):
    ft(pn, 'FortiSwitch', 'FortiSwitch', acc + up + [F('io', 'Other', 'RJ45', 1, 'Console')] + ([F('io', 'Ethernet', 'RJ45', 1, 'Mgmt')] if mg else [])
       + [R('in', 'Power', 'IEC C14', psu, 'PSU' if psu > 1 else 'AC In')],
       (f'PoE budget {poe} W. ' if poe else '') + f'{d} mm deep. ' +
       ('Built-in AC supply plus a redundant AC input. ' if psu > 1 and pn.startswith('FS-4') else
        'Internal 150 W AC supply plus an optional FS-PSU-150 backup. ' if pn.startswith('FS-5') else 'Single built-in AC supply. ') +
       'Check: mains inlet positions.', FS_SRC, FS_URL)

# ======================= Dell PowerSwitch (networking) =======================
DN = lambda *a, **k: add('dell-network.json', 'dell-', 'Dell', *a, **k)
DS52 = ('Dell EMC PowerSwitch S5200-ON spec sheet', 'https://www.dell.com/en-us/shop/povw/networking-s-series-25-100gbe')
DN32 = ('Dell PowerSwitch N3200-ON spec sheet', 'https://www.dell.com/en-us/shop/ipovw/networking-n-series')
def dn(pn, name, fam, ports, notes, src, ru=1, **k): DN(pn.lower(), pn, f'PowerSwitch {pn} {name}', fam, 'network', ru, ports, notes, src[0], src[1], **k)
S52M = [g('front', 'io', 'Other', 'RJ45', 1, 'Console'), g('front', 'io', 'Ethernet', 'RJ45', 1, 'Mgmt'), g('front', 'io', 'USB', 'USB-A', 1, 'USB')]
S52N = 'Check: console, management and USB positions (the spec sheet lists an RJ45 console and management port only). '
dn('S5248F-ON', '48 x 25G + 100G switch', 'S5200-ON', [CAGE(48, 'SFP28', '10/25G'), CAGE(2, 'QSFP-DD', '2 x 100G'), CAGE(4, 'QSFP28', '100G')] + S52M + [PSU()],
   S52N + 'Two hot-swap AC PSUs. 310 W typical / 647 W max, 460 mm deep, 9.7 kg.', DS52, verified=False, powerW=647, weightKg=9.7)
dn('S5224F-ON', '24 x 25G + 4 x 100G switch', 'S5200-ON', [CAGE(24, 'SFP28', '10/25G'), CAGE(4, 'QSFP28', '100G')] + S52M + [PSU()],
   S52N + 'Two hot-swap AC PSUs. 200 W typical / 455 W max, 460 mm deep, 9.7 kg.', DS52, verified=False, powerW=455, weightKg=9.7)
dn('S5232F-ON', '32 x 100G switch', 'S5200-ON', [CAGE(32, 'QSFP28', '100G'), CAGE(2, 'SFP+', '10G')] + S52M + [PSU()],
   S52N + 'Two hot-swap AC PSUs. 360 W typical / 635 W max, 460 mm deep, 9.8 kg.', DS52, verified=False, powerW=635, weightKg=9.8)
dn('S5212F-ON', '12 x 25G + 3 x 100G half-width switch', 'S5200-ON', [CAGE(12, 'SFP28', '10/25G'), CAGE(3, 'QSFP28', '100G')] + S52M + [PSU()],
   S52N + 'Half-width (209 mm), two fit side by side in 1RU with a tandem tray. 140 W typical / 304 W max, 490 mm deep, 4.5 kg.',
   DS52, w=6, verified=False, powerW=304, weightKg=4.5, boxMm={'w': 209, 'h': 41})
dn('S5296F-ON', '96 x 25G + 8 x 100G switch (2RU)', 'S5200-ON', [CAGE(96, 'SFP28', '10/25G'), CAGE(8, 'QSFP28', '100G')] + S52M + [PSU()],
   S52N + 'Two hot-swap AC PSUs. 457 W typical / 893 W max, 511 mm deep, 15.1 kg.', DS52, ru=2, verified=False, powerW=893, weightKg=15.1)
N3M = [F('io', 'Other', 'RJ45', 1, 'Console'), F('io', 'Other', 'USB micro-B', 1, 'Console (USB)'), F('io', 'USB', 'USB-A', 1, 'USB'),
       R('io', 'Ethernet', 'RJ45', 1, 'Mgmt')]
for pn, name, acc, up, psu in (
        ('N3224T-ON', '24 x 1G switch', [RJ(24, '1G')], CAGE(4, 'SFP+', '10G'), 550),
        ('N3224P-ON', '24 x 1G PoE+ switch', [RJ(24, '1G PoE+')], CAGE(4, 'SFP+', '10G'), 1050),
        ('N3224F-ON', '24 x 1G SFP switch', [CAGE(24, 'SFP', '1G')], CAGE(4, 'SFP+', '10G'), 550),
        ('N3224PX-ON', '24 x 10G PoE-bt switch', [RJ(24, '100M-10G PoE-bt')], CAGE(4, 'SFP28', '25G'), 1600),
        ('N3248TE-ON', '48 x 1G switch', [RJ(48, '1G')], CAGE(4, 'SFP+', '10G'), 550),
        ('N3248P-ON', '48 x 1G PoE+ switch', [RJ(48, '1G PoE+')], CAGE(4, 'SFP+', '10G'), 1050),
        ('N3248X-ON', '48 x 10GBASE-T switch', [RJ(48, '100M-10G')], CAGE(4, 'SFP28', '25G'), 550),
        ('N3248PXE-ON', '48 x 10G PoE-bt switch', [RJ(48, '100M-10G PoE-bt')], CAGE(4, 'SFP28', '25G'), 1600)):
    dn(pn, name, 'N3200-ON', acc + [up] + N3M + [CAGE(2, 'QSFP28', '100G stacking', face='rear'), PSU()],
       f'2 x 100G QSFP28 stacking ports on the rear. Ships with one {psu} W hot-swap AC PSU, second slot for redundancy. 400 mm deep. '
       'Check: console and management positions.', DN32, verified=False)

idx_path = os.path.join(CAT, 'index.json')
idx = json.load(open(idx_path))
for f, models in FILES.items():
    ids = [m['id'] for m in models]; assert len(ids) == len(set(ids)), f
    json.dump(models, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    if f not in idx: idx.append(f)
    print(f, len(models))
json.dump(idx, open(idx_path, "w"))
