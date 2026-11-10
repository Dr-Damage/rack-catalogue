#!/usr/bin/env python3
"""Generates catalogue/dell.json (PowerEdge rack servers, Precision rack workstations, Dell Smart-UPS) and
catalogue/apc.json (APC Smart-UPS rack UPSs and battery packs). Added 2026-11-11."""
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

# ======================= Dell PowerEdge =======================
DE = lambda *a, **k: add('dell.json', 'dell-', 'Dell', *a, **k)
def pe_ports(pcie, psu=2, ocp=True, lom=2, rndc=0, front_usb=1, rear_usb2=1, rear_usb3=1, serial=True):
    p = [F('out', 'Other', 'VGA', 1, 'VGA'), F('io', 'USB', 'USB-A', front_usb, 'USB 2.0'), F('io', 'USB', 'Micro-USB', 1, 'iDRAC Direct'),
         R('out', 'Other', 'VGA', 1, 'VGA'), R('io', 'USB', 'USB-A', rear_usb2, 'USB 2.0'), R('io', 'USB', 'USB-A', rear_usb3, 'USB 3.0'),
         R('io', 'Ethernet', 'RJ45', 1, 'iDRAC')]
    if serial: p.append(R('io', 'Other', 'DB9', 1, 'Serial'))
    if lom: p.append(R('io', 'Ethernet', 'RJ45', lom, '1GbE LOM'))
    if rndc: p.append(R('io', 'Ethernet', 'RJ45', rndc, 'rNDC NIC'))
    if ocp: p.append(R('io', 'Other', 'Card slot', 1, 'OCP 3.0 NIC'))
    p.append(R('io', 'Other', 'Card slot', pcie, 'PCIe slot'))
    p.append(R('in', 'Power', 'IEC C14', psu, 'PSU'))
    return p
PSU_NOTE = 'PSUs up to 1400 W take C13/C14 cords; 1800 W and larger take C19/C20. '
NIC_NOTE = 'Add NIC, GPU and SDI card ports as extra ports for the cards fitted. '
PE = 'https://www.dell.com/en-au/shop/ipovw/poweredge-'

DE('poweredge-r660', 'PowerEdge R660', 'PowerEdge R660 1U two-socket server', 'PowerEdge 16G', 'computer', 1, pe_ports(3),
   '1U, 42.8 x 482 x 822.9 mm with bezel (809 mm without). Intel Xeon 4th/5th gen. Up to 3 PCIe, optional 2 x 1GbE LOM and/or OCP 3.0, '
   'hot-swap redundant PSUs 700-1800 W (and -48 V DC). Serial optional. ' + PSU_NOTE + NIC_NOTE,
   'Dell PowerEdge R660 spec sheet', PE + 'r660', full=True)
DE('poweredge-r760', 'PowerEdge R760', 'PowerEdge R760 2U two-socket server', 'PowerEdge 16G', 'computer', 2, pe_ports(8),
   '2U, 86.8 x 482 x 772.1 mm with bezel. Intel Xeon 4th/5th gen. Up to 8 PCIe Gen4/Gen5, optional 2 x 1GbE LOM and/or OCP 3.0, '
   'hot-swap redundant PSUs 700-2800 W. Common for GPU, media server and playout builds. ' + PSU_NOTE + NIC_NOTE,
   'PowerEdge R760 technical specifications', PE + 'r760', full=True)
for code, ru, pcie in [('R660xs', 1, 3), ('R760xs', 2, 6), ('R6615', 1, 3), ('R7615', 2, 8), ('R6625', 1, 3), ('R7625', 2, 8)]:
    amd = code[1] in '67' and len(code) == 5
    DE(f'poweredge-{code.lower()}', f'PowerEdge {code}', f'PowerEdge {code} {ru}U {"AMD EPYC" if amd else "Intel Xeon"} server',
       'PowerEdge 16G', 'computer', ru, pe_ports(pcie),
       f'{ru}U 16th-generation PowerEdge ({"AMD EPYC" if amd else "Intel Xeon"}), same rear I/O layout as the R660/R760: iDRAC, VGA, USB, '
       'optional serial, LOM and OCP 3.0, redundant PSUs. ' + PSU_NOTE + NIC_NOTE + f'Check: PCIe slot count ({pcie} assumed) and LOM option.',
       'Dell PowerEdge 16G family (R660/R760 spec sheets for shared I/O)', PE + code.lower(), verified=False, full=True)
DE('poweredge-r250', 'PowerEdge R250', 'PowerEdge R250 1U single-socket server', 'PowerEdge 15G', 'computer', 1,
   pe_ports(2, psu=1, ocp=False),
   '1U, 42.8 x 482 x 598.6 mm with bezel. Intel Xeon E-2300. 2 low-profile PCIe Gen4, 2 x 1GbE embedded, single cabled PSU 450 or 700 W. '
   'Short depth, good for edge and control racks.', 'Dell EMC PowerEdge R250 spec sheet', PE + 'r250', full=False)
for code, ru, pcie, psu, notes in [
        ('R350', 1, 2, 2, 'Intel Xeon E-2300, short depth, optional redundant hot-plug PSUs.'),
        ('R450', 1, 2, 2, 'Two-socket Intel Xeon 3rd gen, OCP 3.0 option.'),
        ('R550', 2, 5, 2, 'Two-socket Intel Xeon 3rd gen.'),
        ('R650', 1, 3, 2, 'Two-socket Intel Xeon 3rd gen.'),
        ('R750', 2, 8, 2, 'Two-socket Intel Xeon 3rd gen, GPU capable.'),
        ('R650xs', 1, 3, 2, 'Two-socket Intel Xeon 3rd gen, scale-out version.'),
        ('R750xs', 2, 5, 2, 'Two-socket Intel Xeon 3rd gen, scale-out version.')]:
    DE(f'poweredge-{code.lower()}', f'PowerEdge {code}', f'PowerEdge {code} {ru}U server', 'PowerEdge 15G', 'computer', ru,
       pe_ports(pcie, psu=psu, ocp=(code != 'R350')),
       f'{ru}U 15th-generation PowerEdge. {notes} iDRAC9, VGA, USB 2.0/3.0, serial, 2 x 1GbE LOM. ' + PSU_NOTE + NIC_NOTE +
       f'Check: PCIe slot count ({pcie} assumed), PSU count and OCP option.', 'Dell PowerEdge 15G family (R250/R660 spec sheets for shared I/O)',
       PE + code.lower(), verified=False, full=(code not in ('R350',)))
for code, ru, pcie in [('R640', 1, 3), ('R740', 2, 8), ('R440', 1, 2), ('R540', 2, 5)]:
    DE(f'poweredge-{code.lower()}', f'PowerEdge {code}', f'PowerEdge {code} {ru}U server (14G)', 'PowerEdge 14G', 'computer', ru,
       pe_ports(pcie, ocp=False, lom=0 if code in ('R640', 'R740') else 2, rndc=4 if code in ('R640', 'R740') else 0,
                rear_usb2=0, rear_usb3=2),
       f'{ru}U 14th-generation PowerEdge (2017-2021), still common in broadcast installs. Rear: VGA, serial, 2 x USB 3.0, iDRAC9, '
       + ('rNDC network daughter card (4 ports, 1GbE or 10GbE RJ45/SFP+). ' if code in ('R640', 'R740') else '2 x 1GbE LOM. ')
       + PSU_NOTE + NIC_NOTE + f'Check: PCIe slot count ({pcie} assumed) and front USB count.',
       'Dell PowerEdge 14G owner\'s manuals (from memory of the platform; not re-checked)', PE + code.lower(), verified=False, full=True)
for code, ru, pcie in [('R670', 1, 3), ('R770', 2, 8)]:
    DE(f'poweredge-{code.lower()}', f'PowerEdge {code}', f'PowerEdge {code} {ru}U server (17G)', 'PowerEdge 17G', 'computer', ru, pe_ports(pcie),
       f'{ru}U 17th-generation PowerEdge (Intel Xeon 6, 2025). Rear I/O assumed the same as the 16G R660/R760. ' + PSU_NOTE + NIC_NOTE +
       'Check: all ports against the Dell spec sheet.', 'Dell PowerEdge 17G (ports assumed from 16G)', PE + code.lower(), verified=False, full=True)

# ---- Precision rack workstations ----
DE('precision-7960-rack', 'Precision 7960 Rack', 'Precision 7960 Rack 2U workstation', 'Precision Rack', 'computer', 2,
   [F('out', 'Other', 'VGA', 1, 'VGA (iDRAC)'), F('io', 'USB', 'USB-A', 1, 'USB 2.0'), F('io', 'USB', 'Micro-USB', 1, 'iDRAC Direct'),
    R('out', 'Other', 'VGA', 1, 'VGA (iDRAC)'), R('io', 'USB', 'USB-A', 1, 'USB 2.0'), R('io', 'USB', 'USB-A', 1, 'USB 3.0'),
    R('io', 'Ethernet', 'RJ45', 1, 'iDRAC'), R('io', 'Ethernet', 'RJ45', 2, '1GbE LOM'), R('io', 'Other', 'Card slot', 1, 'OCP 3.0 NIC'),
    R('io', 'Other', 'Card slot', 7, 'PCIe slot'), R('out', 'DisplayPort', 'DisplayPort', 4, 'GPU outputs'), R('in', 'Power', 'IEC C14', 2, 'PSU')],
   '2U, 86.8 x 482 x 772 mm. Intel Xeon W-3400. 7 PCIe slots with dual CPUs, up to 2 double-wide GPUs (RTX Pro 6000 / RTX 6000 Ada), '
   'one or two hot-plug PSUs 800-2400 W (1400/2400 W need C19 cords). GPU DisplayPort count depends on the card fitted (4 assumed). '
   'Serial only via PCIe card.', 'Dell Precision 7960 Rack spec sheet',
   'https://www.dell.com/en-au/shop/desktop-computers/precision-7960-rack/spd/precision-r7960-workstation', full=True)
for code, ru, notes in [('7920', 2, 'Two-socket Xeon Scalable, up to 3 double-wide GPUs, iDRAC9, dual PSUs.'),
                        ('3930', 1, 'Single-socket Xeon E / Core, short depth, up to 1 GPU, 1 or 2 PSUs.')]:
    DE(f'precision-{code}-rack', f'Precision {code} Rack', f'Precision {code} Rack {ru}U workstation', 'Precision Rack', 'computer', ru,
       [F('io', 'USB', 'USB-A', 2, 'USB'), R('out', 'Other', 'VGA', 1, 'VGA'), R('io', 'USB', 'USB-A', 4, 'USB'),
        R('io', 'Ethernet', 'RJ45', 2, '1GbE'), R('io', 'Ethernet', 'RJ45', 1, 'iDRAC/Remote mgmt'), R('io', 'Other', 'DB9', 1, 'Serial'),
        R('io', 'Other', 'Card slot', 3 if ru == 1 else 6, 'PCIe slot'), R('out', 'DisplayPort', 'DisplayPort', 4, 'GPU outputs'),
        R('in', 'Power', 'IEC C14', 2, 'PSU')],
       f'{ru}U rack workstation (previous generation). {notes} Check: every port count (catalogued from the platform family, not the spec sheet).',
       'Dell Precision rack workstation family', 'https://www.dell.com/en-au/shop/workstations', verified=False, full=(ru == 2))

# ---- Dell Smart-UPS (APC-built, same hardware as APC SMT) ----
for va, w, out, inp in [(1500, 1000, [('IEC C13', 4)], 'IEC C14'), (3000, 2700, [('IEC C13', 8), ('IEC C19', 1)], 'IEC C20')]:
    DE(f'dlt{va}rmi2uc', f'DLT{va}RMI2UC', f'Dell Smart-UPS {va}VA LCD RM 2U 230V with SmartConnect', 'Dell Smart-UPS', 'power', 2,
       [R('in', 'Power', inp, 1, 'AC In')] + [R('out', 'Power', c, n, 'Outlet') for c, n in out] +
       [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'Other', 'RJ45', 1, 'Serial'), R('io', 'Ethernet', 'RJ45', 1, 'SmartConnect'),
        R('io', 'Other', 'Card slot', 1, 'SmartSlot (NMC)')],
       f'2U line-interactive {va} VA / {w} W, 230 V. Dell-branded APC Smart-UPS (same unit as APC SMT{va}RMI2UC). SmartConnect cloud port, '
       'SmartSlot for an AP9640/AP9641 network card.', 'Dell Smart-UPS listing and APC SMT data', 'https://www.dell.com/en-au/shop/ipovw/ups')

# ======================= APC =======================
AP = lambda *a, **k: add('apc.json', 'apc-', 'APC (Schneider Electric)', *a, **k)
APCU = 'https://www.apc.com/shop/au/en/products/'
SRC = 'APC Smart-UPS datasheets and APC solutions guide 2022'
def smt_ports(inp, out, connect=True):
    p = [R('in', 'Power', inp, 1, 'AC In')] + [R('out', 'Power', c, n, 'Outlet') for c, n in out] + \
        [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'Other', 'RJ45', 1, 'Serial'), R('io', 'Other', 'Card slot', 1, 'SmartSlot (NMC)')]
    if connect: p.append(R('io', 'Ethernet', 'RJ45', 1, 'SmartConnect'))
    return p
for va, w, out, inp in [(750, 500, [('IEC C13', 4)], 'IEC C14'), (1000, 700, [('IEC C13', 4)], 'IEC C14'),
                        (1500, 1000, [('IEC C13', 4)], 'IEC C14'), (2200, 1980, [('IEC C13', 8), ('IEC C19', 1)], 'IEC C20'),
                        (3000, 2700, [('IEC C13', 8), ('IEC C19', 1)], 'IEC C20')]:
    AP(f'smt{va}rmi2uc', f'SMT{va}RMI2UC', f'Smart-UPS {va}VA LCD RM 2U 230V with SmartConnect', 'Smart-UPS SMT', 'power', 2, smt_ports(inp, out),
       f'2U line-interactive {va} VA / {w} W, 230 V, LCD. Input {inp}. SmartSlot takes an AP9640/AP9641 network card. '
       f'SMT{va}RMI2U (no C) is the same without the SmartConnect port; SMT{va}RMI2UNC ships with a network card.',
       SRC, APCU + f'P-SMT{va}RMI2UC', full=False)
for va, w, out, inp in [(1500, 1200, [('IEC C13', 8)], 'IEC C14')]:
    AP('smx1500rmi2u', 'SMX1500RMI2U', 'Smart-UPS X 1500VA rack/tower 2U 230V', 'Smart-UPS SMX', 'power', 2,
       smt_ports(inp, out, connect=False) + [R('io', 'Other', 'Battery connector', 1, 'External battery pack')],
       '2U rack/tower line-interactive 1500 VA / 1200 W, extended runtime with SMX48RMBP2U packs. Check: interface ports.', SRC,
       APCU + 'P-SMX1500RMI2U', verified=False)
for va, w in [(2200, 1980), (3000, 2700)]:
    AP(f'smx{va}rmhv2u', f'SMX{va}RMHV2U', f'Smart-UPS X {va}VA rack/tower 2U 200-240V', 'Smart-UPS SMX', 'power', 2,
       smt_ports('IEC C20', [('IEC C13', 8), ('IEC C19', 1)], connect=False) + [R('io', 'Other', 'Battery connector', 1, 'External battery pack')],
       f'2U rack/tower line-interactive {va} VA / {w} W, extended runtime with SMX120RMBP2U packs. Check: interface ports.', SRC,
       APCU + f'P-SMX{va}RMHV2U', verified=False)
def srt_ports(inp, out, nc):
    p = [R('in', 'Power', inp, 1, 'AC In')] + [R('out', 'Power', c, n, 'Outlet') for c, n in out] + \
        [R('io', 'USB', 'USB-B', 1, 'USB'), R('io', 'Other', 'RJ45', 1, 'Serial'), R('in', 'Other', 'Terminal block', 1, 'EPO'),
         R('io', 'Other', 'Battery connector', 1, 'External battery pack')]
    p.append(R('io', 'Ethernet', 'RJ45', 1, 'Network card (AP9641)') if nc else R('io', 'Other', 'Card slot', 1, 'SmartSlot (NMC)'))
    return p
for va, w, out, inp, ok, bp in [(1000, 1000, [('IEC C13', 6)], 'IEC C14', True, 'SRT48RMBP'),
                                (1500, 1500, [('IEC C13', 6)], 'IEC C14', False, 'SRT48RMBP'),
                                (2200, 1980, [('IEC C13', 8), ('IEC C19', 2)], 'IEC C20', False, 'SRT72RMBP'),
                                (3000, 2700, [('IEC C13', 8), ('IEC C19', 2)], 'IEC C20', True, 'SRT96RMBP')]:
    for nc in (False, True):
        sfx = '-NC' if nc else ''
        AP(f'srt{va}rmxli{sfx.lower()}', f'SRT{va}RMXLI{sfx}', f'Smart-UPS On-Line SRT {va}VA RM 2U 230V' + (' with network card' if nc else ''),
           'Smart-UPS SRT', 'power', 2, srt_ports(inp, out, nc),
           f'2U double-conversion online {va} VA / {w} W, 230 V, input {inp}, EPO, extended runtime with {bp} 2U battery packs.'
           + (' Ships with an AP9641 network management card (environmental monitoring).' if nc else '')
           + ('' if ok else ' Check: outlet count and battery pack model.'), SRC, APCU + f'P-SRT{va}RMXLI{sfx}', verified=ok)
AP('srt5krmxli', 'SRT5KRMXLI', 'Smart-UPS On-Line SRT 5kVA RM 230V', 'Smart-UPS SRT', 'power', 3,
   srt_ports('Hardwire', [('IEC C13', 6), ('IEC C19', 4)], False),
   '5000 VA / 4500 W double-conversion online, 230 V, hardwired input, 6 x C13 + 4 x C19 outlets. Rack kit included (tower/rack). '
   'Check: rack height (3U assumed) and input terminal type.', SRC, APCU + 'P-SRT5KRMXLI', verified=False, full=True)
for va, w, ru in [(1000, 900, 3), (1500, 1350, 3)]:
    AP(f'srtl{va}rmxli', f'SRTL{va}RMXLI', f'Smart-UPS On-Line Li-Ion SRTL {va}VA RM 3U 230V', 'Smart-UPS SRTL', 'power', ru,
       srt_ports('IEC C14', [('IEC C13', 8)], False),
       f'{ru}U lithium-ion double-conversion online {va} VA / {w} W, 8 x C13, input C14. -NC version includes an AP9641. Check: interface ports.',
       SRC, APCU + f'P-SRTL{va}RMXLI', verified=False)
for va, w in [(2200, 1980), (3000, 2700)]:
    AP(f'srtl{va}rmxli', f'SRTL{va}RMXLI', f'Smart-UPS On-Line Li-Ion SRTL {va}VA RM 3U 230V', 'Smart-UPS SRTL', 'power', 3,
       srt_ports('IEC C20', [('IEC C13', 6), ('IEC C19', 2)], False),
       f'3U lithium-ion double-conversion online {va} VA / {w} W, 6 x C13 + 2 x C19, input C20. -NC version includes an AP9641. '
       'Check: interface ports.', SRC, APCU + f'P-SRTL{va}RMXLI', verified=False)
for pn, ru, fits in [('SRT48RMBP', 2, 'SRT1000/1500RMXLI'), ('SRT72RMBP', 2, 'SRT2200RMXLI'), ('SRT96RMBP', 2, 'SRT3000RMXLI'),
                     ('SMX48RMBP2U', 2, 'SMX750/1000/1500 (48 V)'), ('SMX120RMBP2U', 2, 'SMX2200/3000 (120 V)')]:
    AP(pn.lower(), pn, f'{pn} external battery pack', 'Battery packs', 'power', ru,
       [R('io', 'Other', 'Battery connector', 2, 'Battery link')],
       f'{ru}U rack battery pack for {fits}; daisy-chains for longer runtime. Heavy: mount low in the rack. '
       'Check: rack height and connector count (two assumed, in and out).', SRC, APCU + f'P-{pn}', verified=False)

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
