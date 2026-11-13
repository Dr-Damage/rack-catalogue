#!/usr/bin/env python3
"""Generates catalogue/mikrotik.json, cisco.json and ubiquiti.json (rack-mount network switches, routers, firewalls and
gateways). Added 2026-11-13. Port counts come from the makers' product pages and datasheets (each entry's source);
verified=False and a 'Check:' note mark anything taken from product knowledge instead.
Faces: network ports, console and management are drawn on the front, power inlets on the rear, unless noted."""
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

# front-panel helpers
def RJ(n, label): return F('io', 'Ethernet', 'RJ45', n, label)
def CAGE(n, conn, label=None): return F('io', 'SFP', conn, n, label or conn)
CON = F('io', 'Other', 'RJ45', 1, 'Console')
MGMT = F('io', 'Ethernet', 'RJ45', 1, 'Mgmt')
USB = F('io', 'USB', 'USB-A', 1, 'USB')
def AC(n=1, conn='IEC C14'): return R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')
def DCJ(label='DC In'): return R('in', 'Power', 'DC barrel', 1, label)

# ======================= MikroTik =======================
MK = lambda *a, **k: add('mikrotik.json', 'mikrotik-', 'MikroTik', *a, **k)
MKU = 'https://mikrotik.com/product/'
def mk(code, slug, name, fam, ports, notes, **k):
    MK(slug, code, f'{code} {name}', fam, 'network', 1, ports, '1RU, rack ears included. ' + notes, f'MikroTik {code} product page', MKU + k.pop('url', slug), **k)
mk('CRS326-24G-2S+RM', 'crs326-24g-2s-rm', '24-port Gigabit switch', 'CRS',
   [RJ(24, '1GbE'), CAGE(2, 'SFP+'), CON, DCJ('DC In 10-30 V')],
   '443 x 144 mm deep, 24 W. Dual boot RouterOS / SwOS. Powered by a 24 V adapter (included) or passive PoE-in on port 1. '
   'Check: DC jack side (drawn on the rear).', url='CRS326-24G-2SplusRM')
mk('CSS326-24G-2S+RM', 'css326-24g-2s-rm', '24-port Gigabit switch (SwOS)', 'CSS',
   [RJ(24, '1GbE'), CAGE(2, 'SFP+'), DCJ('DC In 10-30 V')],
   '443 x 144 mm deep, 19 W. SwOS only. Powered by a 24 V adapter (included) or passive PoE-in on port 1. Check: DC jack side.',
   url='CSS326-24G-2SplusRM')
mk('CRS328-24P-4S+RM', 'crs328-24p-4s-rm', '24-port PoE switch', 'CRS',
   [RJ(24, '1GbE PoE+'), CAGE(4, 'SFP+'), CON, AC(1)],
   '443 x 300 mm deep. PoE-out on all 24 ports (802.3af/at and passive), 450 W PoE budget, internal 500 W PSU. Dual boot RouterOS / SwOS.',
   url='crs328_24p_4s_rm')
mk('CRS317-1G-16S+RM', 'crs317-1g-16s-rm', '16-port SFP+ switch', 'CRS',
   [CAGE(16, 'SFP+'), RJ(1, '1GbE'), CON, AC(2)],
   '443 x 224 mm deep, 44 W. Dual redundant AC supplies.', url='crs317_1g_16s_rm')
mk('CRS326-24S+2Q+RM', 'crs326-24s-2q-rm', '24-port SFP+ switch with 40G uplinks', 'CRS',
   [CAGE(24, 'SFP+'), CAGE(2, 'QSFP+'), MGMT, CON, USB, AC(2)],
   '443 x 200 mm deep, 69 W. 10/100 management port, dual redundant AC supplies.', url='crs326_24s_2q_rm')
mk('CRS312-4C+8XG-RM', 'crs312-4c-8xg-rm', '12-port 10G switch', 'CRS',
   [RJ(8, '10GbE'), F('io', 'Ethernet', 'RJ45/SFP+ combo', 4, '10G combo'), MGMT, CON, USB, AC(2)],
   '443 x 183 mm deep, 60 W. 8 x 10G RJ45 plus 4 combo ports (10G RJ45 or SFP+), 10/100 management port, dual redundant AC supplies.',
   url='crs312_4c_8xg_rm')
mk('CRS328-4C-20S-4S+RM', 'crs328-4c-20s-4s-rm', '28-port SFP switch', 'CRS',
   [CAGE(20, 'SFP'), F('io', 'Ethernet', 'RJ45/SFP combo', 4, '1G combo'), CAGE(4, 'SFP+'), CON, AC(2)],
   '443 x 194 mm deep, 43 W. 20 x 1G SFP, 4 combo ports (1G RJ45 or SFP), 4 x SFP+, dual AC supplies with failover.',
   url='crs328_4c_20s_4s_rm')
mk('CRS354-48G-4S+2Q+RM', 'crs354-48g-4s-2q-rm', '48-port Gigabit switch with 40G uplinks', 'CRS',
   [RJ(48, '1GbE'), CAGE(4, 'SFP+'), CAGE(2, 'QSFP+'), MGMT, CON, AC(2)],
   '443 x 297 mm deep, 60 W. 10/100 management port, two AC PSU slots.', url='crs354_48g_4splus2qplusrm')
mk('CRS354-48P-4S+2Q+RM', 'crs354-48p-4s-2q-rm', '48-port PoE switch with 40G uplinks', 'CRS',
   [RJ(48, '1GbE PoE+'), CAGE(4, 'SFP+'), CAGE(2, 'QSFP+'), MGMT, CON, AC(1)],
   '443 x 382 mm deep. PoE-out on all 48 ports (802.3af/at and passive), 700 W PoE budget, single 750 W PSU, 800 W max. '
   'Rear support ears and cable bracket included.', url='crs354_48p_4s_2q_rm', full=True)
mk('CRS326-4C+20G+2Q+RM', 'crs326-4c-20g-2q-rm', '2.5G switch with 40G uplinks', 'CRS',
   [RJ(20, '2.5GbE'), F('io', 'Ethernet', 'RJ45/SFP+ combo', 4, '2.5G/10G combo'), CAGE(2, 'QSFP+'), MGMT, CON, AC(2)],
   '70 W. 20 x 2.5G RJ45, 4 combo ports (2.5G RJ45 or 10G SFP+), 2 x 40G QSFP+, 10/100 management port, dual redundant AC supplies.',
   url='crs326_4c_20g_2q_rm')
mk('CRS320-8P-8B-4S+RM', 'crs320-8p-8b-4s-rm', '16-port PoE++ switch', 'CRS',
   [RJ(8, '1GbE PoE+'), RJ(8, '1GbE PoE++ (bt)'), CAGE(4, 'SFP+'), MGMT, CON, R('in', 'Power', 'IEC C14', 2, 'PSU')],
   'Ports 1-8 802.3af/at, ports 9-16 802.3bt up to 90 W. Ships with one 600 W hot-swap PSU (963 W PoE total with a second PSU '
   'fitted, 1150 W). Gigabit management port. Check: depth (see the maker drawing).', url='crs320_8p_8b_4s_rm')
mk('CRS418-8P-8G-2S+RM', 'crs418-8p-8g-2s-rm', '16-port switch with 8 PoE ports', 'CRS',
   [RJ(8, '1GbE'), RJ(8, '1GbE PoE+'), CAGE(2, 'SFP+'), MGMT, CON, USB, AC(2)],
   'Ports 9-16 PoE-out (802.3af/at and 24 V passive), 150 W budget. Gigabit management port to the CPU, USB 3.0, '
   'dual redundant AC supplies, 215 W max.', url='crs418_8p_8g_2s_rm')
mk('CRS518-16XS-2XQ-RM', 'crs518-16xs-2xq-rm', '25G / 100G switch', 'CRS',
   [CAGE(16, 'SFP28'), CAGE(2, 'QSFP28'), MGMT, CON, USB, AC(2)],
   '95 W max. 10/100 management port, dual redundant hot-swap AC supplies and fans.', url='crs518_16xs_2xq')
mk('CRS520-4XS-16XQ-RM', 'crs520-4xs-16xq-rm', '100G switch', 'CRS',
   [CAGE(16, 'QSFP28'), CAGE(4, 'SFP28'), RJ(2, '10GbE'), CON, AC(2)],
   '220 W max. 2 x 10G RJ45, 2 hot-swap 150 W AC supplies (optional -48 V DC unit), 4 hot-swap fans. Rear support ears included.',
   url='crs520_4xs_16xq_rm', full=True)
mk('CRS804-4DDQ-hRM', 'crs804-4ddq', 'CRS804 DDQ 400G switch', 'CRS',
   [CAGE(4, 'QSFP56-DD', '400G QSFP56-DD'), RJ(2, '10GbE'), CON, AC(2)],
   '123 W max. 4 x 400G QSFP56-DD (break-out to 10-200G), 2 x 10G RJ45, dual redundant hot-swap AC supplies, 2 hot-swap fans.',
   url='crs804_ddq')
mk('CCR2004-16G-2S+', 'ccr2004-16g-2s', 'cloud core router', 'CCR',
   [RJ(16, '1GbE'), CAGE(2, 'SFP+'), CON, USB, AC(2)],
   '443 x 210 mm deep, 48 W. Dual redundant AC supplies.', url='ccr2004_16g_2splus')
mk('CCR2004-1G-12S+2XS', 'ccr2004-1g-12s-2xs', 'cloud core router', 'CCR',
   [CAGE(12, 'SFP+'), CAGE(2, 'SFP28'), RJ(1, '1GbE'), CON, AC(2)],
   '443 x 224 mm deep, 60 W. Dual redundant AC supplies.', url='ccr2004_1g_12s_2xs')
mk('CCR2116-12G-4S+', 'ccr2116-12g-4s', 'cloud core router', 'CCR',
   [RJ(12, '1GbE'), CAGE(4, 'SFP+'), MGMT, CON, AC(2)],
   '443 x 199 mm deep, 83 W. Gigabit management port to the CPU, M.2 slot, dual redundant AC supplies.', url='ccr2116_12g_4splus')
mk('CCR2216-1G-12XS-2XQ', 'ccr2216-1g-12xs-2xq', 'cloud core router', 'CCR',
   [CAGE(12, 'SFP28'), CAGE(2, 'QSFP28'), RJ(1, '1GbE'), CON, AC(2)],
   '443 x 367 mm deep, 128 W. 2 x M.2 (SATA), dual redundant hot-swap AC supplies.', url='ccr2216_1g_12xs_2xq')
mk('RB1100AHx4', 'rb1100ahx4', 'router', 'RouterBOARD',
   [RJ(13, '1GbE'), CON, AC(2), R('in', 'Power', 'Terminal block', 2, 'DC In')],
   '443 x 148 mm deep, 20 W. 13 x Gigabit, RS232 console, microSD, dual redundant AC supplies plus 2 DC terminal inputs '
   '(-48 V or 12-57 V) and PoE-in. The Dude Edition (RB1100Dx4) adds a 60 GB M.2 drive.', url='rb1100ahx4')
mk('RB4011iGS+RM', 'rb4011igs-rm', 'router', 'RouterBOARD',
   [RJ(10, '1GbE'), CAGE(1, 'SFP+'), CON, DCJ('DC In 12-57 V')],
   'Desktop case (228 x 120 mm) on 1U rack ears. Port 10 has passive PoE-out; powered by DC jack or passive PoE-in on port 1. '
   'Check: DC jack side.', url='rb4011igs_rm')

# ======================= Cisco =======================
CI = lambda *a, **k: add('cisco.json', 'cisco-', 'Cisco', *a, **k)
C92 = 'https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9200-series-switches/nb-06-cat9200-ser-data-sheet-cte-en.html'
C93 = 'https://www.cisco.com/c/en/us/products/collateral/switches/catalyst-9300-series-switches/nb-06-cat9300-ser-data-sheet-cte-en.html'
N93 = 'https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-744052.html'
N9C = 'https://www.cisco.com/c/dam/en/us/products/switches/nexus-9000-series-switches/nexus-9300-40GE-switches-comparison.html'
CONS = [CON, F('io', 'USB', 'Mini-USB', 1, 'USB Console'), MGMT]
SIDE = ' Check: console and management port side (drawn on the front).'
# Catalyst 9200L: fixed uplinks, two PSU slots, fixed fans
for pn, dl, up, poe in [('C9200L-24T-4G', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None),
                        ('C9200L-24P-4G', [RJ(24, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 370),
                        ('C9200L-48T-4G', [RJ(48, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None),
                        ('C9200L-48P-4G', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 740),
                        ('C9200L-24T-4X', [RJ(24, '1GbE')], CAGE(4, 'SFP+', '10G SFP+'), None),
                        ('C9200L-24P-4X', [RJ(24, '1GbE PoE+')], CAGE(4, 'SFP+', '10G SFP+'), 370),
                        ('C9200L-48T-4X', [RJ(48, '1GbE')], CAGE(4, 'SFP+', '10G SFP+'), None),
                        ('C9200L-48P-4X', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP+', '10G SFP+'), 740),
                        ('C9200L-48PXG-4X', [RJ(12, 'mGig 10G PoE+'), RJ(36, '1GbE PoE+')], CAGE(4, 'SFP+', '10G SFP+'), 740)]:
    CI(pn.lower(), pn, f'Catalyst {pn} switch', 'Catalyst 9200', 'network', 1, dl + [up] + CONS + [R('in', 'Power', 'IEC C14', 2, 'PSU')],
       f'1RU, {"35.0" if "PXG" in pn else "28.8"} cm deep. Fixed uplinks, '
       + (f'{poe} W PoE+ budget with one PSU (second PSU adds redundancy or PoE), ' if poe else 'one PSU fitted, second slot for redundancy, ')
       + 'two field-replaceable PSU slots (rear), fixed fans, RJ45 and mini-USB console, RJ45 management port. StackWise-160 on the rear.' + SIDE,
       'Cisco Catalyst 9200 Series data sheet', C92)
# Catalyst 9300 (modular uplinks) and 9300L
for pn, dl, poe, psu in [('C9300-24T', [RJ(24, '1GbE')], None, 350), ('C9300-48T', [RJ(48, '1GbE')], None, 350),
                         ('C9300-24P', [RJ(24, '1GbE PoE+')], 445, 715), ('C9300-48P', [RJ(48, '1GbE PoE+')], 437, 715),
                         ('C9300-48U', [RJ(48, '1GbE UPOE')], 822, 1100), ('C9300-24UX', [RJ(24, 'mGig 10G UPOE')], 560, 1100),
                         ('C9300-48UXM', [RJ(36, '2.5GbE UPOE'), RJ(12, 'mGig 10G UPOE')], 490, 1100)]:
    CI(pn.lower(), pn, f'Catalyst {pn} switch', 'Catalyst 9300', 'network', 1,
       dl + [F('io', 'Other', 'Network module', 1, 'Uplink module')] + CONS + [USB, R('io', 'Other', 'StackWise', 2, 'StackWise-480'),
       R('io', 'Other', 'StackPower', 2, 'StackPower'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
       f'1RU. Modular uplinks (network module: 4 x 1G, 8 x 10G, 2 x 25G or 2 x 40G). Ships with one {psu} W AC PSU'
       + (f', {poe} W PoE budget' if poe else '') + '; second slot for redundancy. StackWise-480 and StackPower on the rear. '
       'Add the uplink module ports as extra ports.' + SIDE, 'Cisco Catalyst 9300 Series data sheet', C93, full=True)
for pn, dl, up, poe in [('C9300L-24T-4G', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None),
                        ('C9300L-48P-4X', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP+', '10G SFP+'), 505)]:
    CI(pn.lower(), pn, f'Catalyst {pn} switch', 'Catalyst 9300', 'network', 1,
       dl + [up] + CONS + [USB, R('io', 'Other', 'StackWise', 2, 'StackWise-320'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
       '1RU. Fixed uplinks, StackWise-320 on the rear, two PSU slots' + (f', {poe} W PoE+ budget with the 715 W PSU.' if poe else ' (350 W PSU).') + SIDE,
       'Cisco Catalyst 9300 Series data sheet', C93, full=True)
# Nexus 9300 (data centre and broadcast IP fabrics)
NXR = lambda n: [F('io', 'Ethernet', 'RJ45', 1, 'Mgmt0'), CON, USB, R('in', 'Power', 'IEC C14', 2, 'PSU')]  # n = fan modules (not drawn)
CI('n9k-c93180yc-fx3', 'N9K-C93180YC-FX3', 'Nexus 93180YC-FX3 switch', 'Nexus 9300', 'network', 1,
   [CAGE(48, 'SFP28', '1/10/25G SFP28'), CAGE(6, 'QSFP28', '40/100G QSFP28')] + NXR(4),
   '1RU. 48 x 1/10/25G SFP28 and 6 x 40/100G QSFP28. Up to 2 hot-swap PSUs (650 W AC, 930 W DC or 1200 W HVAC/HVDC), 4 hot-swap fans, '
   'port-side intake or exhaust. Widely used for SMPTE ST 2110 fabrics with NBM.' + SIDE, 'Cisco Nexus 9300-FX3 data sheet', N93, full=True)
CI('n9k-c93108tc-fx3p', 'N9K-C93108TC-FX3P', 'Nexus 93108TC-FX3P switch', 'Nexus 9300', 'network', 1,
   [RJ(48, 'mGig 10G UPOE'), CAGE(6, 'QSFP28', '40/100G QSFP28')] + [F('io', 'SFP', 'SFP', 1, 'Mgmt SFP')] + NXR(4),
   '1RU. 48 x 100M-10G multigig RJ45 with PoE/PoE+/UPOE (60 W), 6 x 40/100G QSFP28. Up to 2 PSUs (1100 W or 1900 W AC), 4 fans.' + SIDE,
   'Cisco Nexus 9300-FX3 data sheet', N93, full=True)
CI('n9k-c93108tc-fx3', 'N9K-C93108TC-FX3', 'Nexus 93108TC-FX3 switch', 'Nexus 9300', 'network', 1,
   [RJ(48, '10GBASE-T'), CAGE(6, 'QSFP28', '40/100G QSFP28')] + [F('io', 'SFP', 'SFP', 1, 'Mgmt SFP')] + NXR(4),
   '1RU. 48 x 100M/1/10G RJ45, 6 x 40/100G QSFP28. Up to 2 PSUs (500 W AC, 930 W DC or 1200 W HVAC/HVDC), 4 fans.' + SIDE,
   'Cisco Nexus 9300-FX3 data sheet', N93, full=True)
CI('n9k-c9348gc-fx3', 'N9K-C9348GC-FX3', 'Nexus 9348GC-FX3 switch', 'Nexus 9300', 'network', 1,
   [RJ(48, '1GbE'), CAGE(4, 'SFP28', '10/25G SFP28'), CAGE(2, 'QSFP28', '40/100G QSFP28')] + [F('io', 'SFP', 'SFP', 1, 'Mgmt SFP')] + NXR(3),
   '1RU. 48 x 10M/100M/1G RJ45, 4 x 10/25G SFP28, 2 x 40/100G QSFP28. Up to 2 PSUs (350 W AC, 440 W DC), 3 fans. '
   'Often used as a management / out-of-band switch.' + SIDE, 'Cisco Nexus 9300-FX3 data sheet', N93, full=True)
CI('n9k-c9336c-fx2', 'N9K-C9336C-FX2', 'Nexus 9336C-FX2 switch', 'Nexus 9300', 'network', 1,
   [CAGE(36, 'QSFP28', '40/100G QSFP28')] + NXR(6),
   '1RU spine / leaf, 36 x 40/100G QSFP28 (breakout to 4 x 10/25G). 2 x 1100 W PSUs. Common spine for ST 2110 fabrics. '
   'Check: fan module count.' + SIDE, 'Cisco Nexus 9300 40/100G comparison', N9C, verified=False, full=True)
CI('n9k-c9332c', 'N9K-C9332C', 'Nexus 9332C switch', 'Nexus 9300', 'network', 1,
   [CAGE(32, 'QSFP28', '40/100G QSFP28'), CAGE(2, 'SFP+', '1/10G SFP+')] + NXR(6),
   '1RU, 32 x 40/100G QSFP28 and 2 x 1/10G SFP+. 2 x 1100 W PSUs. Check: fan module count.' + SIDE,
   'Cisco Nexus 9300 40/100G comparison', N9C, verified=False, full=True)
CI('n9k-c9364c-gx', 'N9K-C9364C-GX', 'Nexus 9364C-GX switch', 'Nexus 9300', 'network', 2,
   [CAGE(64, 'QSFP28', '40/100G QSFP28')] + NXR(4),
   '2RU spine, 64 x 40/100G QSFP28. 2 x 2000 W PSUs. Check: fan module count.' + SIDE,
   'Cisco Nexus 9300 40/100G comparison', N9C, verified=False, full=True)
CI('n9k-c93600cd-gx', 'N9K-C93600CD-GX', 'Nexus 93600CD-GX switch', 'Nexus 9300', 'network', 1,
   [CAGE(28, 'QSFP28', '40/100G QSFP28'), CAGE(8, 'QSFP-DD', '400G QSFP-DD')] + NXR(6),
   '1RU, 28 x 40/100G QSFP28 and 8 x 400G QSFP-DD. 2 PSUs. Check: port counts, PSUs and fans are from Cisco product knowledge.' + SIDE,
   'Cisco Nexus 9300-GX product information', 'https://www.cisco.com/c/en/us/products/switches/nexus-9000-series-switches/index.html',
   verified=False, full=True)
# Small-business and legacy Catalyst (port counts are in the model numbers)
for pn, fam, dl, up, poe, url in [
        ('C1000-24T-4G-L', 'Catalyst 1000', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None, 'catalyst-1000-series-switches'),
        ('C1000-48P-4G-L', 'Catalyst 1000', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 370, 'catalyst-1000-series-switches'),
        ('C1300-24T-4G', 'Catalyst 1300', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None, 'catalyst-1300-series-switches'),
        ('C1300-48P-4X', 'Catalyst 1300', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP+', '10G SFP+'), 375, 'catalyst-1300-series-switches'),
        ('CBS350-24T-4G', 'Business 350', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None, 'business-350-series-managed-switches'),
        ('CBS350-48P-4G', 'Business 350', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 370, 'business-350-series-managed-switches'),
        ('WS-C2960X-24TS-L', 'Catalyst 2960-X', [RJ(24, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None, 'catalyst-2960-x-series-switches'),
        ('WS-C2960X-48TS-L', 'Catalyst 2960-X', [RJ(48, '1GbE')], CAGE(4, 'SFP', '1G SFP'), None, 'catalyst-2960-x-series-switches'),
        ('WS-C2960X-24PS-L', 'Catalyst 2960-X', [RJ(24, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 370, 'catalyst-2960-x-series-switches'),
        ('WS-C2960X-48FPS-L', 'Catalyst 2960-X', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), 740, 'catalyst-2960-x-series-switches')]:
    legacy = pn.startswith('WS-')
    CI(pn.lower(), pn, f'{fam} {pn} switch' + (' (legacy)' if legacy else ''), fam, 'network', 1,
       dl + [up, CON] + ([R('io', 'Other', 'FlexStack', 2, 'FlexStack')] if legacy else []) + [AC(1)],
       '1RU, fixed uplinks, internal AC PSU' + (f', about {poe} W PoE budget' if poe else '') + '.'
       + (' End of sale; FlexStack-Plus module optional on the rear.' if legacy else '')
       + ' Check: PoE budget, console type and whether a management port is fitted (from Cisco product knowledge).',
       f'Cisco {fam} product information', f'https://www.cisco.com/c/en/us/products/switches/{url}/index.html', verified=False)
# Routers and firewalls (from product knowledge: check against the data sheet for the unit on site)
RT = [('isr4331', 'ISR4331/K9', 'ISR 4331 integrated services router', 'ISR 4000', 1,
       [RJ(2, '1GbE'), CAGE(1, 'SFP', '1G SFP'), F('io', 'Other', 'NIM slot', 2, 'NIM'), F('io', 'Other', 'SM slot', 1, 'SM'),
        CON, F('io', 'Other', 'RJ45', 1, 'Aux'), MGMT, USB, AC(1)],
       '1RU branch router, 3 onboard GE (2 RJ45 + 1 SFP), 2 NIM slots and 1 service-module slot, single internal AC PSU (PoE option). End of sale.',
       'isr-4000-series-integrated-services-routers'),
      ('isr4431', 'ISR4431/K9', 'ISR 4431 integrated services router', 'ISR 4000', 1,
       [F('io', 'Ethernet', 'RJ45/SFP combo', 4, '1GbE combo'), F('io', 'Other', 'NIM slot', 3, 'NIM'), CON, F('io', 'Other', 'RJ45', 1, 'Aux'),
        MGMT, USB, R('in', 'Power', 'IEC C14', 2, 'PSU')],
       '1RU router, 4 onboard GE (RJ45 or SFP), 3 NIM slots, dual hot-swap PSUs. End of sale.', 'isr-4000-series-integrated-services-routers'),
      ('c8200-1n-4t', 'C8200-1N-4T', 'Catalyst 8200 edge platform', 'Catalyst 8000', 1,
       [RJ(2, '1GbE'), CAGE(2, 'SFP', '1G SFP'), F('io', 'Other', 'NIM slot', 1, 'NIM'), F('io', 'Other', 'PIM slot', 1, 'PIM'), CON, MGMT, USB, AC(1)],
       '1RU SD-WAN / branch router, 4 x 1G (2 RJ45 + 2 SFP), 1 NIM and 1 PIM slot.', 'catalyst-8200-series-edge-platforms'),
      ('c8300-1n1s-6t', 'C8300-1N1S-6T', 'Catalyst 8300 edge platform', 'Catalyst 8000', 1,
       [RJ(4, '1GbE'), CAGE(2, 'SFP', '1G SFP'), F('io', 'Other', 'NIM slot', 1, 'NIM'), F('io', 'Other', 'SM slot', 1, 'SM'), CON, MGMT, USB,
        R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU branch router, 6 x 1G (4 RJ45 + 2 SFP), 1 NIM and 1 SM slot, dual PSUs.',
       'catalyst-8300-series-edge-platforms'),
      ('asr1001-x', 'ASR1001-X', 'ASR 1001-X aggregation services router', 'ASR 1000', 1,
       [CAGE(6, 'SFP', '1G SFP'), CAGE(2, 'SFP+', '10G SFP+'), F('io', 'Other', 'NIM slot', 1, 'NIM'), CON, F('io', 'Other', 'RJ45', 1, 'Aux'), MGMT, USB,
        R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU, 6 x 1G SFP, 2 x 10G SFP+, 1 NIM slot, dual PSUs.', 'asr-1000-series-aggregation-services-routers'),
      ('fpr1140', 'FPR1140-NGFW-K9', 'Firepower 1140 firewall', 'Firepower', 1,
       [RJ(8, '1GbE'), CAGE(4, 'SFP', '1G SFP'), CON, F('io', 'USB', 'Mini-USB', 1, 'USB Console'), MGMT, USB, AC(1)],
       '1RU next-generation firewall, 8 x 1G RJ45, 4 x 1G SFP, single AC PSU.', 'security/firepower-1000-series'),
      ('fpr3110', 'FPR3110-NGFW-K9', 'Secure Firewall 3110', 'Secure Firewall 3100', 1,
       [RJ(8, '1GbE'), CAGE(8, 'SFP+', '10G SFP+'), F('io', 'Other', 'Network module', 1, 'Network module'), CON, MGMT, USB,
        R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU firewall, 8 x 1G RJ45, 8 x 10G SFP+, one network-module slot, dual hot-swap PSUs.',
       'security/secure-firewall-3100-series'),
      ('asa5525-x', 'ASA5525-K9', 'ASA 5525-X firewall (legacy)', 'ASA 5500-X', 1,
       [RJ(8, '1GbE'), F('io', 'Other', 'Expansion slot', 1, 'I/O card'), CON, MGMT, USB, AC(1)],
       '1RU firewall, 8 x 1G RJ45, one I/O expansion slot, optional second PSU. End of sale.', 'security/asa-5500-series-next-generation-firewalls')]
for id, pn, name, fam, ru, ports, notes, url in RT:
    CI(id, pn, name, fam, 'network', ru, ports, notes + ' Check: ports and PSU arrangement are from Cisco product knowledge.',
       f'Cisco {fam} product information', f'https://www.cisco.com/c/en/us/products/{url}/index.html', verified=False)
# Meraki (cloud managed)
MR = 'https://documentation.meraki.com/'
for id, pn, name, ports, notes in [
        ('ms120-24p', 'MS120-24P', 'Meraki MS120-24P switch', [RJ(24, '1GbE PoE+'), CAGE(4, 'SFP', '1G SFP'), AC(1)],
         '1RU, 370 W PoE budget, internal PSU.'),
        ('ms225-48fp', 'MS225-48FP', 'Meraki MS225-48FP switch', [RJ(48, '1GbE PoE+'), CAGE(4, 'SFP+', '10G SFP+'), R('io', 'Other', 'Stack', 2, 'Stack'), AC(1)],
         '1RU, 740 W PoE budget, physical stacking on the rear.'),
        ('ms250-48fp', 'MS250-48FP', 'Meraki MS250-48FP switch', [RJ(48, '1GbE PoE+'), CAGE(4, 'SFP+', '10G SFP+'), R('io', 'Other', 'Stack', 2, 'Stack'),
         R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU, 740 W PoE budget, dual field-replaceable PSUs, stacking on the rear.'),
        ('mx105', 'MX105', 'Meraki MX105 security appliance', [RJ(2, '1GbE WAN'), CAGE(2, 'SFP+', '10G SFP+ WAN'), RJ(6, '1GbE LAN'),
         CAGE(2, 'SFP+', '10G SFP+ LAN'), R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU SD-WAN appliance, dual PSU slots.'),
        ('mx250', 'MX250', 'Meraki MX250 security appliance', [RJ(8, '1GbE'), CAGE(8, 'SFP', '1G SFP'), CAGE(8, 'SFP+', '10G SFP+'),
         R('in', 'Power', 'IEC C14', 2, 'PSU')], '1RU SD-WAN appliance, dual hot-swap PSUs.')]:
    CI('meraki-' + id, pn, name, 'Meraki', 'network', 1, ports,
       notes + ' Cloud managed (no console port). Check: port counts and PSUs are from Meraki product knowledge.',
       'Cisco Meraki product information', MR, verified=False)

# ======================= Ubiquiti =======================
UB = lambda *a, **k: add('ubiquiti.json', 'ubiquiti-', 'Ubiquiti', *a, **k)
UST = 'https://store.ui.com/us/en/category/'
DS = 'https://download.axilogi.com/Ubiquiti/Datasheet/'
RPS = R('in', 'Power', 'DC (USP-RPS)', 1, 'RPS In')
def uw(sku, name, fam, ports, notes, src, url, verified=True, ru=1, rps=True, full=False, w=12):
    UB(sku.lower().replace('.', '-'), sku, name, fam, 'network', ru, ports + [AC(1)] + ([RPS] if rps else []), notes, src, url,
       verified=verified, full=full, w=w)
STORE = 'UniFi store switching list'
# UniFi Pro Max / Pro HD / Pro XG (Etherlighting, touchscreen, no console port)
uw('USW-Pro-Max-24-PoE', 'UniFi Switch Pro Max 24 PoE', 'UniFi Pro Max', [RJ(16, '1GbE PoE'), RJ(8, '2.5GbE PoE'), CAGE(2, 'SFP+')],
   '1RU, 442 x 325 mm deep. 8 ports PoE/PoE+ and 16 ports PoE++ (60 W), 400 W PoE budget, internal 450 W PSU, USP-RPS DC input. '
   'Layer 3, Etherlighting, 1.3 in touchscreen. Check: which port group carries PoE++.',
   'UniFi USW-Pro-Max-24-PoE datasheet', DS + 'USW-Pro-Max-24-PoE.pdf')
uw('USW-Pro-Max-24', 'UniFi Switch Pro Max 24', 'UniFi Pro Max', [RJ(16, '1GbE'), RJ(8, '2.5GbE'), CAGE(2, 'SFP+')],
   '1RU, 442 x 325 mm deep, 50 W. Layer 3, Etherlighting, touchscreen, USP-RPS DC input.', 'UniFi USW-Pro-Max-24 datasheet', DS + 'USW-Pro-Max-24.pdf')
uw('USW-Pro-Max-48-PoE', 'UniFi Switch Pro Max 48 PoE', 'UniFi Pro Max', [RJ(32, '1GbE PoE+'), RJ(16, '2.5GbE PoE++'), CAGE(4, 'SFP+')],
   '1RU, 442 x 400 mm deep. 720 W PoE budget, internal 820 W PSU, USP-RPS DC input. Layer 3, Etherlighting, touchscreen.',
   'UniFi USW-Pro-Max-48-PoE datasheet', DS + 'USW-Pro-Max-48-PoE.pdf')
uw('USW-Pro-Max-48', 'UniFi Switch Pro Max 48', 'UniFi Pro Max', [RJ(32, '1GbE'), RJ(16, '2.5GbE'), CAGE(4, 'SFP+')],
   '1RU, Layer 3, Etherlighting, touchscreen, USP-RPS DC input.', STORE, UST + 'switching-professional-max-xg/products/usw-pro-max-48')
uw('USW-Pro-HD-24-PoE', 'UniFi Switch Pro HD 24 PoE', 'UniFi Pro HD', [RJ(22, '2.5GbE PoE++'), RJ(2, '10GbE PoE++'), CAGE(4, 'SFP+')],
   '1RU, 442 x 400 mm deep. PoE++ on all 24 RJ45 ports (64 W max), 600 W PoE budget, internal 660 W PSU, RPS DC input. Touchscreen.',
   'UniFi USW-Pro-HD-24-PoE datasheet', DS + 'USW-Pro-HD-24-PoE.pdf')
uw('USW-Pro-HD-24', 'UniFi Switch Pro HD 24', 'UniFi Pro HD', [RJ(22, '2.5GbE'), RJ(2, '10GbE'), CAGE(4, 'SFP+')],
   '1RU, Layer 3, touchscreen, RPS DC input.', STORE, UST + 'switching-professional-max-xg/products/usw-pro-hd-24')
uw('USW-Pro-XG-48-PoE', 'UniFi Switch Pro XG 48 PoE', 'UniFi Pro XG', [RJ(16, '2.5GbE PoE'), RJ(32, '10GbE PoE'), CAGE(4, 'SFP28')],
   '1RU, 442 x 480 mm deep, 8.8 kg. PoE on all RJ45 ports, 1080 W PoE budget at 200-240 V (972 W at 100-120 V), internal 1350 W PSU, RPS DC input.',
   'UniFi USW-Pro-XG-48-PoE datasheet', DS + 'USW-Pro-XG-48-PoE.pdf', full=True)
uw('USW-Pro-XG-48', 'UniFi Switch Pro XG 48', 'UniFi Pro XG', [RJ(16, '2.5GbE'), RJ(32, '10GbE'), CAGE(4, 'SFP28')],
   '1RU, Layer 3, RPS DC input.', STORE, UST + 'switching-professional-max-xg/products/usw-pro-xg-48')
uw('USW-Pro-XG-24-PoE', 'UniFi Switch Pro XG 24 PoE', 'UniFi Pro XG', [RJ(8, '2.5GbE PoE'), RJ(16, '10GbE PoE'), CAGE(2, 'SFP28')],
   '1RU, Layer 3, RPS DC input. Check: PoE budget.', STORE, UST + 'switching-professional-max-xg/products/usw-pro-xg-24-poe')
uw('USW-Pro-XG-24', 'UniFi Switch Pro XG 24', 'UniFi Pro XG', [RJ(8, '2.5GbE'), RJ(16, '10GbE'), CAGE(2, 'SFP28')],
   '1RU, Layer 3, RPS DC input.', STORE, UST + 'switching-professional-max-xg/products/usw-pro-xg-24')
# UniFi Pro (Gen 2) and Standard
for sku, dl, up, notes, path in [
        ('USW-Pro-24-PoE', [RJ(24, '1GbE PoE+')], CAGE(2, 'SFP+'), 'PoE+/PoE++ ports, about 400 W PoE budget.', 'switching-professional/products/usw-pro-24-poe'),
        ('USW-Pro-48-PoE', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP+'), 'PoE+/PoE++ ports, about 600 W PoE budget.', 'switching-professional/products/usw-pro-48-poe'),
        ('USW-Pro-24', [RJ(24, '1GbE')], CAGE(2, 'SFP+'), '', 'switching-professional'),
        ('USW-Pro-48', [RJ(48, '1GbE')], CAGE(4, 'SFP+'), '', 'switching-professional'),
        ('USW-24-PoE', [RJ(24, '1GbE PoE+')], CAGE(2, 'SFP', '1G SFP'), '16 PoE+ ports, about 95 W PoE budget.', 'switching-standard/products/usw-24-poe'),
        ('USW-48-PoE', [RJ(48, '1GbE PoE+')], CAGE(4, 'SFP', '1G SFP'), '32 PoE+ ports, about 195 W PoE budget.', 'switching-standard/products/usw-48-poe'),
        ('USW-24', [RJ(24, '1GbE')], CAGE(2, 'SFP', '1G SFP'), '', 'switching-standard/products/usw-24'),
        ('USW-48', [RJ(48, '1GbE')], CAGE(4, 'SFP', '1G SFP'), '', 'switching-standard/products/usw-48')]:
    pro = 'Pro' in sku
    uw(sku, 'UniFi ' + sku.replace('USW-', 'Switch ').replace('-', ' '), 'UniFi Pro' if pro else 'UniFi Standard', dl + [up],
       '1RU, ' + ('Layer 3, touchscreen, RPS DC input. ' if pro else 'Layer 2, front status display. ') + notes
       + ' Check: PoE budget and which ports carry PoE (port counts from the UniFi store).',
       STORE, UST + path, verified=False, rps=pro)
# Aggregation and enterprise
uw('USW-Pro-Aggregation', 'UniFi Switch Hi-Capacity Aggregation', 'UniFi Aggregation', [CAGE(28, 'SFP+'), CAGE(4, 'SFP28')],
   '1RU, Layer 3 aggregation, 28 x 10G SFP+ and 4 x 25G SFP28. Check: PSU arrangement (drawn as internal AC plus RPS).',
   STORE, UST + 'switching-aggregation/products/usw-pro-aggregation', verified=False)
uw('USW-Pro-XG-Aggregation', 'UniFi Switch Pro XG Aggregation', 'UniFi Aggregation', [CAGE(32, 'SFP28')],
   '1RU, 32 x 25G SFP28. Check: PSU arrangement.', STORE, UST + 'switching-aggregation/products/usw-pro-xg-aggregation', verified=False)
uw('USW-Aggregation', 'UniFi Switch Aggregation', 'UniFi Aggregation', [CAGE(8, 'SFP+')],
   '1RU, 8 x 10G SFP+, Layer 2. Check: width and power inlet (drawn full width with an AC inlet).', STORE,
   UST + 'switching-aggregation/products/usw-aggregation', verified=False, rps=False)
uw('ECS-Aggregation', 'UniFi Enterprise Campus Aggregation', 'UniFi Enterprise Campus', [CAGE(48, 'SFP28'), CAGE(6, 'QSFP28')],
   '1RU, 48 x 25G SFP28 and 6 x 100G QSFP28. Check: PSU arrangement (likely dual hot-swap).', STORE,
   UST + 'switching-enterprise/collections/enterprise-campus-aggregation/products/ecs-aggregation', verified=False, rps=False, full=True)
uw('ECS-Core', 'UniFi Enterprise Campus Switch Core', 'UniFi Enterprise Campus', [CAGE(32, 'QSFP28')],
   '1RU, 32 x 100G QSFP28. Check: PSU arrangement (likely dual hot-swap).', STORE,
   UST + 'switching-enterprise/collections/enterprise-campus-aggregation/products/ecs-core', verified=False, rps=False, full=True)
uw('ECS-48-PoE', 'UniFi Enterprise Campus 48 PoE', 'UniFi Enterprise Campus', [RJ(16, '2.5GbE PoE'), RJ(32, '10GbE PoE'), CAGE(4, 'SFP28')],
   '1RU. Check: PoE budget and PSUs.', STORE, UST + 'switching-enterprise/collections/enterprise-campus/products/ecs-48-poe', verified=False, full=True)
uw('ECS-24-PoE', 'UniFi Enterprise Campus 24 PoE', 'UniFi Enterprise Campus', [RJ(8, '2.5GbE PoE'), RJ(16, '10GbE PoE'), CAGE(4, 'SFP28')],
   '1RU. Check: PoE budget and PSUs.', STORE, UST + 'switching-enterprise/collections/enterprise-campus/products/ecs-24-poe', verified=False)
uw('EAV-XG-24-PoE', 'UniFi Enterprise Audio/Video XG 24 PoE', 'UniFi Enterprise AV', [RJ(24, '10GbE PoE'), CAGE(4, 'QSFP28')],
   '1RU AV-over-IP switch (Dante / AES67 / IPMX profiles), 24 x 10G PoE, 4 x 100G QSFP28. Check: PoE budget and PSUs.', STORE,
   UST + 'switching-enterprise/collections/enterprise-audiovideo/products/eav-xg-24-poe', verified=False)
uw('EAV-Fiber', 'UniFi Enterprise Audio/Video Fiber', 'UniFi Enterprise AV', [CAGE(20, 'SFP+'), CAGE(2, 'QSFP28')],
   '1RU AV-over-IP fibre switch, 20 x 10G, 2 x 100G QSFP28. Check: whether the 10G ports are SFP+ cages, and PSUs.', STORE,
   UST + 'switching-enterprise/collections/enterprise-audiovideo/products/eav-fiber', verified=False)
uw('USW-Enterprise-24-PoE', 'UniFi Switch Enterprise 24 PoE (legacy)', 'UniFi Enterprise', [RJ(12, '2.5GbE PoE+'), RJ(12, '1GbE PoE+'), CAGE(2, 'SFP+')],
   '1RU, 400 W PoE budget, RPS DC input. Replaced by the Pro Max range. Check: from product knowledge.', 'UniFi product information',
   UST + 'switching-enterprise', verified=False)
uw('USW-EnterpriseXG-24', 'UniFi Switch Enterprise XG 24 (legacy)', 'UniFi Enterprise', [RJ(24, '10GbE'), CAGE(2, 'SFP28')],
   '1RU, 24 x 10G RJ45, 2 x 25G SFP28, dual hot-swap PSUs. Replaced by the Pro XG range. Check: from product knowledge.',
   'UniFi product information', UST + 'switching-enterprise', verified=False, rps=False)
# UniFi gateways, NVRs and storage
UB('udm-pro', 'UDM-Pro', 'UniFi Dream Machine Pro', 'UniFi Cloud Gateway', 'network', 1,
   [RJ(1, '1GbE WAN'), CAGE(1, 'SFP+', '10G SFP+ WAN'), RJ(8, '1GbE LAN'), CAGE(1, 'SFP+', '10G SFP+ LAN'), F('io', 'Other', '3.5in bay', 1, 'HDD bay'),
    AC(1), RPS],
   '1RU, 442 x 286 mm deep, 33 W. Gateway with UniFi Network and Protect, one 3.5 in drive bay, internal 50 W PSU, USP-RPS DC input.',
   'UniFi UDM-Pro datasheet', DS + 'UDM-Pro.pdf')
UB('udm-pro-max', 'UDM-Pro-Max', 'UniFi Dream Machine Pro Max', 'UniFi Cloud Gateway', 'network', 1,
   [RJ(1, '2.5GbE WAN'), CAGE(1, 'SFP+', '10G SFP+ WAN'), RJ(8, '1GbE LAN'), CAGE(1, 'SFP+', '10G SFP+ LAN'), F('io', 'Other', '3.5in bay', 2, 'HDD bay'),
    AC(1), RPS],
   '1RU, 442 x 286 mm deep, 100 W. Internal 100 W PSU, RPS DC input (11.5 V). Check: two drive bays (from product knowledge).',
   'UniFi UDM-Pro-Max datasheet', DS + 'UDM-Pro-Max.pdf', verified=False)
UB('udm-se', 'UDM-SE', 'UniFi Dream Machine Special Edition', 'UniFi Cloud Gateway', 'network', 1,
   [RJ(1, '2.5GbE WAN'), CAGE(1, 'SFP+', '10G SFP+ WAN'), RJ(8, '1GbE LAN PoE'), CAGE(1, 'SFP+', '10G SFP+ LAN'), F('io', 'Other', '3.5in bay', 1, 'HDD bay'),
    AC(1), RPS],
   '1RU gateway with 8 PoE LAN ports (2 PoE+), about 180 W PoE budget, one 3.5 in drive bay, RPS DC input. Check: from product knowledge.',
   'UniFi product information', UST + 'cloud-gateways', verified=False)
UB('unvr', 'UNVR', 'UniFi Network Video Recorder', 'UniFi Protect', 'recorder', 1,
   [RJ(1, '1GbE'), CAGE(1, 'SFP+'), F('io', 'Other', '3.5in bay', 4, 'HDD bay'), AC(1), RPS],
   '1RU, 442 x 325 mm deep, 4 front drive bays, internal 120 W PSU, USP-RPS DC input, 100 W max.', 'UniFi UNVR datasheet', DS + 'UNVR.pdf')
UB('unvr-pro', 'UNVR-Pro', 'UniFi Network Video Recorder Pro', 'UniFi Protect', 'recorder', 2,
   [RJ(1, '1GbE'), CAGE(1, 'SFP+'), F('io', 'Other', '3.5in bay', 7, 'HDD bay'), AC(1), RPS],
   '2RU, 7 front drive bays, touchscreen, RPS DC input. Check: from product knowledge.', 'UniFi product information', UST + 'unifi-protect', verified=False)
UB('unas-pro', 'UNAS-Pro', 'UniFi NAS Pro', 'UniFi Storage', 'computer', 2,
   [RJ(1, '1GbE'), CAGE(1, 'SFP+'), F('io', 'Other', '3.5in bay', 7, 'HDD bay'), AC(1), RPS],
   '2RU NAS, 7 front drive bays, 1G RJ45 and 10G SFP+. Check: from product knowledge.', 'UniFi product information', UST + 'unifi-storage', verified=False)
# EdgeMax (EdgeRouter and EdgeSwitch: discontinued but widely installed; from product knowledge)
EM = ' EdgeMax (discontinued). Check: from Ubiquiti product knowledge.'
EMU = 'https://help.ui.com/hc/en-us/categories/6583256751383'
UB('er-8-xg', 'ER-8-XG', 'EdgeRouter Infinity', 'EdgeRouter', 'network', 1,
   [CAGE(8, 'SFP+'), RJ(1, '1GbE'), CON, USB, R('in', 'Power', 'IEC C14', 2, 'PSU')],
   '1RU router, 8 x 10G SFP+, 1 x 1G RJ45, dual hot-swap AC PSUs.' + EM, 'Ubiquiti EdgeMax product information', EMU, verified=False)
UB('erpro-8', 'ERPro-8', 'EdgeRouter Pro', 'EdgeRouter', 'network', 1,
   [RJ(6, '1GbE'), F('io', 'Ethernet', 'RJ45/SFP combo', 2, '1G combo'), CON, AC(1)],
   '1RU router, 6 x 1G RJ45 plus 2 combo ports (RJ45 or SFP), internal AC PSU.' + EM, 'Ubiquiti EdgeMax product information', EMU, verified=False)
UB('er-12', 'ER-12', 'EdgeRouter 12', 'EdgeRouter', 'network', 1,
   [RJ(10, '1GbE'), CAGE(2, 'SFP', '1G SFP'), CON, DCJ()],
   'Desktop router (rack ears optional), 10 x 1G RJ45 (passive PoE in/out on some ports), 2 x SFP, external DC adapter.' + EM,
   'Ubiquiti EdgeMax product information', EMU, verified=False, w=8)
for sku, dl, up, notes in [
        ('ES-24-250W', [RJ(24, '1GbE PoE+')], [CAGE(2, 'SFP', '1G SFP')], '802.3af/at and 24 V passive PoE, 250 W total.'),
        ('ES-24-500W', [RJ(24, '1GbE PoE+')], [CAGE(2, 'SFP', '1G SFP')], '802.3af/at and 24 V passive PoE, 500 W total.'),
        ('ES-48-500W', [RJ(48, '1GbE PoE+')], [CAGE(2, 'SFP+'), CAGE(2, 'SFP', '1G SFP')], '802.3af/at and 24 V passive PoE, 500 W total.'),
        ('ES-48-750W', [RJ(48, '1GbE PoE+')], [CAGE(2, 'SFP+'), CAGE(2, 'SFP', '1G SFP')], '802.3af/at and 24 V passive PoE, 750 W total.'),
        ('ES-24-Lite', [RJ(24, '1GbE')], [CAGE(2, 'SFP', '1G SFP')], 'No PoE.'),
        ('ES-48-Lite', [RJ(48, '1GbE')], [CAGE(2, 'SFP+'), CAGE(2, 'SFP', '1G SFP')], 'No PoE.'),
        ('ES-16-XG', [CAGE(12, 'SFP+'), RJ(4, '10GbE')], [], '12 x 10G SFP+ and 4 x 10GBASE-T.'),
        ('ES-16-150W', [RJ(16, '1GbE PoE+')], [CAGE(2, 'SFP', '1G SFP')], '802.3af/at and 24 V passive PoE, 150 W total.')]:
    UB(sku.lower(), sku, 'EdgeSwitch ' + sku[3:], 'EdgeSwitch', 'network', 1, dl + up + [CON, AC(1)],
       '1RU managed switch, RJ45 serial console, internal AC PSU. ' + notes + EM, 'Ubiquiti EdgeMax product information', EMU, verified=False)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
