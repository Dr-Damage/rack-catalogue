#!/usr/bin/env python3
"""Generates enterprise IT gear: catalogue/hpe-more.json (HPE ProLiant servers Gen8 to Gen12, MSA storage, StoreEver tape,
G2 PDUs, KVM console, FlexFabric and OfficeConnect switches), hp.json (HP Inc Z workstations), aruba-more.json (HPE Aruba
Networking CX 6100/6200F/8100/9300/10000, CX 6400 chassis and line modules, 2540, Instant On, 9240 gateway), ibm.json (Power10 /
Power11 servers, HMC, FlashSystem, tape, legacy System x), oracle.json (Oracle Server X9-2/X9-2L, SPARC, StorageTek SL150),
f5.json (BIG-IP iSeries, rSeries, VELOS chassis and blade) and vmware.json (VMware SD-WAN / VeloCloud Edge appliances; VMware
itself sells software only). Added 2026-11-17.

Port counts come from each maker's QuickSpecs, platform guide or data sheet (each entry's source). Where the source does not
give a detail, the entry says 'Check:' and verified is False. Server card slots (PCIe, OCP, FlexibleLOM) are drawn as card
slots: add the ports of the cards fitted as extra ports.
Existing files left alone: hpe.json (DL360p Gen8, misc_brands.py), aruba.json (CX 8325/8360/6300, 2930F, network2.py)."""
import json, os, math
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
def SLOT(n, label, face='rear'): return g(face, 'io', 'Other', 'Card slot', n, label)
def USBA(n, label='USB', face='rear'): return g(face, 'io', 'USB', 'USB-A', n, label)
def VGA(face='rear', label='VGA'): return g(face, 'out', 'Other', 'VGA', 1, label)
def CONS(face='front', conn='RJ45', label='Console'): return g(face, 'io', 'Other', conn, 1, label)
def PSU(n=2, conn='IEC C14', label=None): return R('in', 'Power', conn, n, label or ('PSU' if n > 1 else 'AC In'))
def GPU(n=4): return R('out', 'DisplayPort', 'DisplayPort', n, 'GPU outputs')

# =====================================================================================================================
# HPE ProLiant servers
# =====================================================================================================================
HP_ = lambda *a, **k: add('hpe-more.json', 'hpe-', 'HPE', *a, **k)
QS = 'https://www.hpe.com/psnow/doc/'
CARDS = 'Add NIC, GPU, HBA and SDI card ports as extra ports for the cards fitted. '
FLEX = ('Flex Slot hot-plug PSUs: 500/800/1000 W take C13/C14 cords; 1600 W runs on 200-240 V only; '
        'Check: the inlet on 1800-2200 W Titanium supplies. ')

def pl(front, rear_usb, emb=0, emb_label='1GbE embedded', ilo=True, ocp=0, flom=False, pcie=3, psu=2, vga=True, dp_rear=False,
       serial=False, ilo_shared=False):
    """ProLiant port set. front: list of front groups."""
    p = list(front)
    if vga: p.append(VGA())
    if dp_rear: p.append(R('out', 'DisplayPort', 'DisplayPort', 1, 'DisplayPort'))
    if serial: p.append(R('io', 'Other', 'DB9', 1, 'Serial'))
    p.append(USBA(rear_usb, 'USB 3.2 Gen 1' if rear_usb else 'USB'))
    if ilo: p.append(RJ(1, 'iLO', 'rear'))
    if emb: p.append(RJ(emb, emb_label, 'rear'))
    if flom: p.append(SLOT(1, 'FlexibleLOM'))
    if ocp: p.append(SLOT(ocp, 'OCP 3.0 NIC'))
    p.append(SLOT(pcie, 'PCIe slot'))
    p.append(PSU(psu))
    return p

F_G11 = [F('io', 'USB', 'USB-A', 1, 'USB 3.2 Gen 1'), F('io', 'USB', 'Micro-USB', 1, 'iLO service port')]
F_G12 = [F('io', 'USB', 'USB-A', 1, 'USB 3.2 Gen 1'), F('io', 'USB', 'USB-C', 1, 'iLO service port')]
F_G10 = [F('io', 'USB', 'USB-A', 1, 'USB 3.0'), F('io', 'USB', 'Micro-USB', 1, 'iLO service port')]
F_G9 = [F('io', 'USB', 'USB-A', 1, 'USB 3.0')]
ILOSVC = 'Check: iLO service port connector (micro-USB assumed; Gen12 uses USB-C). '

# --- Gen12 (iLO 7) ---
HP_('dl380-gen12', 'ProLiant Compute DL380 Gen12', 'ProLiant Compute DL380 Gen12 2U server', 'ProLiant Gen12', 'computer', 2,
    pl(F_G12, 2, ocp=2, pcie=8),
    '2U two-socket Intel Xeon 6 server, iLO 7. No built-in NIC: ports come from the OCP 3.0 (A standard, B optional) and PCIe '
    'cards fitted. Up to 8 PCIe Gen5 slots (6 x16 + 2 x8). Optional front DisplayPort and 2 x USB 2.0 via the Universal Media Bay; '
    'optional rear serial port. 1 or 2 Flex Slot PSUs 800-2200 W (1600 W and up need 200-240 V). ' + CARDS,
    'HPE ProLiant Compute DL380 Gen12 QuickSpecs', 'https://www.hpe.com/us/en/collaterals/collateral.a00073551enw.html', full=True)
HP_('dl360-gen12', 'ProLiant Compute DL360 Gen12', 'ProLiant Compute DL360 Gen12 1U server', 'ProLiant Gen12', 'computer', 1,
    pl(F_G12, 2, ocp=2, pcie=3),
    '1U two-socket Intel Xeon 6 server, iLO 7. No built-in NIC: ports come from the OCP 3.0 and PCIe cards fitted. '
    'Check: PCIe slot count (3 assumed, as on the Gen11) and front ports (taken from the DL380 Gen12). ' + CARDS,
    'HPE ProLiant Compute DL360 Gen12 product page', 'https://www.hpe.com/us/en/hpe-proliant-compute-dl360-gen12.html',
    verified=False, full=True)

# --- Gen11 (iLO 6) ---
HP_('dl360-gen11', 'ProLiant DL360 Gen11', 'ProLiant DL360 Gen11 1U server', 'ProLiant Gen11', 'computer', 1,
    pl(F_G11, 2, ocp=2, pcie=3),
    '1U two-socket 4th/5th gen Intel Xeon server, iLO 6. No built-in NIC: ports come from the OCP 3.0 (slot 2 needs CPU 2) and '
    'PCIe cards (2 standard, slot 3 needs CPU 2). Pre-configured models often carry a 4 x 1GbE BCM5719 OCP3 or 2 x 10GBASE-T '
    'BCM57416 card. Optional front DisplayPort (not active together with the rear VGA) and front USB 2.0; optional rear serial port. '
    + FLEX + ILOSVC + CARDS,
    'HPE ProLiant DL360 Gen11 QuickSpecs', 'https://www.hpe.com/us/en/collaterals/collateral.a50004306enw.html', full=True)
HP_('dl380-gen11', 'ProLiant DL380 Gen11', 'ProLiant DL380 Gen11 2U server', 'ProLiant Gen11', 'computer', 2,
    pl(F_G11, 2, ocp=2, pcie=8),
    '2U two-socket 4th/5th gen Intel Xeon server, iLO 6. No built-in NIC: ports come from the OCP 3.0 and PCIe cards fitted. '
    'Up to 8 PCIe slots (3 primary, 3 secondary, 2 tertiary riser). Optional front DisplayPort and USB 2.0 via the Universal Media '
    'Bay; optional rear serial port. A common host for broadcast software (playout, graphics, MAM). ' + FLEX + ILOSVC + CARDS,
    'HPE ProLiant DL380 Gen11 QuickSpecs', 'https://www.hpe.com/us/en/collaterals/collateral.a50004307enw.html', full=True)
HP_('dl20-gen11', 'ProLiant DL20 Gen11', 'ProLiant DL20 Gen11 1U short-depth server', 'ProLiant Gen11', 'computer', 1,
    [F('io', 'USB', 'USB-A', 1, 'USB 3.2 Gen 1'), F('io', 'USB', 'USB-A', 1, 'USB 2.0 (iLO service)'),
     VGA(), R('out', 'DisplayPort', 'DisplayPort', 1, 'DisplayPort'), USBA(4, 'USB 3.2 Gen 1'),
     RJ(4, '1GbE embedded (port 1 shared with iLO)', 'rear'), SLOT(1, 'OCP 3.0 NIC'), SLOT(1, 'PCIe slot'), PSU(1)],
    'Short-depth 1U single-socket Intel Xeon E-2400 server, 378 mm deep (SFF). 4 x 1GbE BCM5719 embedded; NIC 1 is shared with '
    'iLO. A dedicated iLO port and serial port come with the LP Serial/iLO/M.2 enablement kit (P65407-B21). Standard 290 W '
    'non-hot-plug PSU; redundant Flex Slot PSUs (500/800/1000 W) optional, so change the PSU count to 2 if fitted.',
    'HPE ProLiant DL20 Gen11 QuickSpecs', 'https://www.hpe.com/us/en/collaterals/collateral.a50007009enw.html')
GEN11_X = 'Check: rear layout taken from the DL360/DL380 Gen11 (VGA, 2 x USB, iLO, OCP 3.0, PCIe); slot counts from the product page. '
HP_('dl320-gen11', 'ProLiant DL320 Gen11', 'ProLiant DL320 Gen11 1U single-socket server', 'ProLiant Gen11', 'computer', 1,
    pl(F_G11, 2, ocp=2, pcie=3), '1U single-socket Intel Xeon server for edge and VDI/GPU work. ' + GEN11_X + CARDS,
    'HPE ProLiant DL320 Gen11 product page', 'https://www.hpe.com/us/en/hpe-proliant-dl320-gen11.html', verified=False, full=True)
for mid, ru, sock, pcie in [('dl325', 1, 'single-socket', 3), ('dl365', 1, 'two-socket', 3), ('dl345', 2, 'single-socket', 8),
                            ('dl385', 2, 'two-socket', 8)]:
    M = mid.upper()
    HP_(f'{mid}-gen11', f'ProLiant {M} Gen11', f'ProLiant {M} Gen11 {ru}U {sock} AMD EPYC server', 'ProLiant Gen11', 'computer', ru,
        pl(F_G11, 2, ocp=2, pcie=pcie), f'{ru}U {sock} AMD EPYC 9004/9005 server, iLO 6. ' + GEN11_X + CARDS,
        f'HPE ProLiant {M} Gen11 product page', f'https://www.hpe.com/us/en/hpe-proliant-{mid}-gen11.html', verified=False, full=True)

# --- Gen10 Plus ---
G10P = ('Check: rear ports from the Gen10 Plus family (VGA, 2 x USB 3.0, iLO 5, OCP 3.0, PCIe; no embedded NIC); '
        'confirm OCP and PCIe counts in the QuickSpecs. ')
HP_('dl360-gen10plus', 'ProLiant DL360 Gen10 Plus', 'ProLiant DL360 Gen10 Plus 1U server', 'ProLiant Gen10 Plus', 'computer', 1,
    pl(F_G10, 2, ocp=1, pcie=3), '1U two-socket 3rd gen Intel Xeon server, iLO 5. ' + G10P + CARDS,
    'HPE ProLiant DL360 Gen10 Plus QuickSpecs', 'https://www.hpe.com/psnow/doc/a50000080enw', verified=False, full=True)
HP_('dl380-gen10plus', 'ProLiant DL380 Gen10 Plus', 'ProLiant DL380 Gen10 Plus 2U server', 'ProLiant Gen10 Plus', 'computer', 2,
    pl(F_G10, 2, ocp=1, pcie=8), '2U two-socket 3rd gen Intel Xeon server, iLO 5. ' + G10P + CARDS,
    'HPE ProLiant DL380 Gen10 Plus QuickSpecs', 'https://www.hpe.com/psnow/doc/a50000081enw', verified=False, full=True)
HP_('dl325-gen10plus-v2', 'ProLiant DL325 Gen10 Plus v2', 'ProLiant DL325 Gen10 Plus v2 1U AMD EPYC server', 'ProLiant Gen10 Plus',
    'computer', 1, pl(F_G10, 2, ocp=1, pcie=2), '1U single-socket AMD EPYC 7003 server, iLO 5. ' + G10P + CARDS,
    'HPE ProLiant DL325 Gen10 Plus v2 QuickSpecs', 'https://www.hpe.com/us/en/hpe-proliant-dl325-gen10-plus-v2.html',
    verified=False, full=True)
HP_('dl385-gen10plus-v2', 'ProLiant DL385 Gen10 Plus v2', 'ProLiant DL385 Gen10 Plus v2 2U AMD EPYC server', 'ProLiant Gen10 Plus',
    'computer', 2, pl(F_G10, 2, ocp=2, pcie=8), '2U two-socket AMD EPYC 7003 server, iLO 5. ' + G10P + CARDS,
    'HPE ProLiant DL385 Gen10 Plus v2 QuickSpecs', 'https://www.hpe.com/us/en/hpe-proliant-dl385-gen10-plus-v2.html',
    verified=False, full=True)

# --- Gen10 ---
G10 = ('Check: rear ports from the Gen10 family (VGA, 2 x USB 3.0, iLO 5, embedded HPE 369i 4 x 1GbE, FlexibleLOM slot, PCIe); '
       'serial port optional. ')
HP_('dl360-gen10', 'ProLiant DL360 Gen10', 'ProLiant DL360 Gen10 1U server', 'ProLiant Gen10', 'computer', 1,
    pl(F_G10, 2, emb=4, flom=True, pcie=3), '1U two-socket Intel Xeon Scalable server (2017-2021), iLO 5. Slot 3 needs CPU 2. '
    + G10 + CARDS, 'HPE ProLiant DL360 Gen10 QuickSpecs', 'https://www.hpe.com/psnow/doc/a00008180enw', verified=False, full=True)
HP_('dl380-gen10', 'ProLiant DL380 Gen10', 'ProLiant DL380 Gen10 2U server', 'ProLiant Gen10', 'computer', 2,
    pl(F_G10, 2, emb=4, flom=True, pcie=8), '2U two-socket Intel Xeon Scalable server (2017-2021), iLO 5. Up to 8 PCIe slots over '
    'three risers. Very common under broadcast software (Avid, Grass Valley, Harmonic, Imagine). ' + G10 + CARDS,
    'HPE ProLiant DL380 Gen10 QuickSpecs', 'https://www.hpe.com/psnow/doc/a00008181enw', verified=False, full=True)
HP_('dl20-gen10', 'ProLiant DL20 Gen10', 'ProLiant DL20 Gen10 1U short-depth server', 'ProLiant Gen10', 'computer', 1,
    [F('io', 'USB', 'USB-A', 1, 'USB 3.0'), VGA(), USBA(2, 'USB 3.0'), RJ(2, '1GbE embedded (port 1 shared with iLO)', 'rear'),
     SLOT(2, 'PCIe slot'), PSU(1)],
    'Short-depth 1U single-socket Xeon E-2100/2200 server, iLO 5. Embedded 2 x 1GbE; optional dedicated iLO port and serial port '
    'kit. Single non-hot-plug PSU standard, redundant PSUs optional. Check: rear USB count.',
    'HPE ProLiant DL20 Gen10 QuickSpecs', 'https://www.hpe.com/psnow/doc/a00008179enw', verified=False)

# --- Gen9 / Gen8 (sold as HP before the November 2015 split) ---
G9 = ('Sold as HP ProLiant (before HP split into HP Inc and HPE in 2015). Check: rear ports from the Gen9 family (VGA, serial, '
      '2 x USB 3.0, iLO 4, embedded HP 331i 4 x 1GbE, FlexibleLOM slot, PCIe). ')
HP_('dl360-gen9', 'ProLiant DL360 Gen9', 'ProLiant DL360 Gen9 1U server (legacy)', 'ProLiant Gen9', 'computer', 1,
    pl(F_G9, 2, emb=4, flom=True, pcie=3, serial=True), '1U two-socket Xeon E5-2600 v3/v4 server (2014-2017). ' + G9 + CARDS,
    'HPE ProLiant DL360 Gen9 QuickSpecs', 'https://www.hpe.com/psnow/doc/c04375623', verified=False, full=True)
HP_('dl380-gen9', 'ProLiant DL380 Gen9', 'ProLiant DL380 Gen9 2U server (legacy)', 'ProLiant Gen9', 'computer', 2,
    pl(F_G9, 2, emb=4, flom=True, pcie=6, serial=True), '2U two-socket Xeon E5-2600 v3/v4 server (2014-2017). Up to 6 PCIe slots. '
    + G9 + CARDS, 'HPE ProLiant DL380 Gen9 QuickSpecs', 'https://www.hpe.com/psnow/doc/c04346247', verified=False, full=True)
HP_('dl380p-gen8', 'ProLiant DL380p Gen8', 'ProLiant DL380p Gen8 2U server (legacy)', 'ProLiant', 'computer', 2,
    [VGA(), R('io', 'Other', 'DB9', 1, 'Serial'), USBA(4, 'USB 2.0'), RJ(4, '1GbE FlexibleLOM', 'rear'), RJ(1, 'iLO 4', 'rear'),
     SLOT(6, 'PCIe slot'), PSU(2)],
    'Sold as HP ProLiant. 2U two-socket Xeon E5-2600 / v2 server (2012-2015), FlexibleLOM 4 x 1GbE (or 2 x 10GbE), dedicated iLO 4, '
    'up to 6 PCIe slots (3 with one CPU), redundant Flex Slot PSUs. Check: FlexibleLOM fitted and PCIe cards.',
    'HPE QuickSpecs DL380p Gen8', 'https://www.hpe.com/psnow/doc/c04123076', verified=False, full=True)

# =====================================================================================================================
# HPE storage and tape
# =====================================================================================================================
MSA = ('2U array with two controllers; each controller has 4 host ports, 1 SAS expansion port (mini-SAS HD), 1 RJ45 management '
       'port and a CLI port, and the enclosure has 2 hot-plug PSUs. Up to 9 expansion enclosures. '
       'Check: CLI port connector and PSU inlet. ')
MSA_SRC = ('HPE MSA 2060 / 2062 data sheets', 'https://www.hpe.com/us/en/storage/msa-shared-storage.html')
def msa_ports(host_type, host_conn, host_label):
    p = []
    for c in ('A', 'B'):
        p += [R('io', host_type, host_conn, 4, f'Ctrl {c} host {host_label}'),
              R('io', 'Other', 'Mini-SAS HD', 1, f'Ctrl {c} SAS expansion'),
              R('io', 'Ethernet', 'RJ45', 1, f'Ctrl {c} Mgmt'),
              R('io', 'USB', 'Micro-USB', 1, f'Ctrl {c} CLI')]
    return p + [PSU(2)]
HP_('msa2062-fc-sff', 'R0Q80A', 'MSA 2062 16Gb FC SFF storage array (24 x 2.5 in)', 'MSA storage', 'computer', 2,
    msa_ports('Fibre', 'SFP+', '16Gb FC'), MSA + '24 SFF bays, 2 x 16Gb FC 4-port controllers. MSA 2062 is the 2060 bundled '
    'with two SSDs and the advanced data services licence. 508 mm deep.', *MSA_SRC, verified=False, full=True)
HP_('msa2060-fc-sff', 'MSA 2060 FC SFF', 'MSA 2060 16Gb FC SFF storage array (24 x 2.5 in)', 'MSA storage', 'computer', 2,
    msa_ports('Fibre', 'SFP+', '16Gb FC'), MSA + '24 SFF bays. Also sold in 12 LFF. Check: part number for your region.',
    *MSA_SRC, verified=False, full=True)
HP_('msa2060-iscsi-sff', 'MSA 2060 10GbE iSCSI SFF', 'MSA 2060 10GbE iSCSI SFF storage array (24 x 2.5 in)', 'MSA storage',
    'computer', 2, msa_ports('SFP', 'SFP+', '10GbE iSCSI'), MSA + '24 SFF bays. A 10GBASE-T iSCSI version is also sold (RJ45 '
    'host ports). Check: part number.', *MSA_SRC, verified=False, full=True)
HP_('msa2060-sas-sff', 'MSA 2060 12Gb SAS SFF', 'MSA 2060 12Gb SAS SFF storage array (24 x 2.5 in)', 'MSA storage', 'computer', 2,
    msa_ports('Other', 'Mini-SAS HD', '12Gb SAS'), MSA + '24 SFF bays, direct-attached to up to 4 hosts per controller pair. '
    'Check: part number.', *MSA_SRC, verified=False, full=True)
HP_('msa2060-lff-drive-enc', 'MSA 2060 LFF Disk Enclosure', 'MSA 2060 LFF disk enclosure (12 x 3.5 in)', 'MSA storage', 'computer', 2,
    [R('io', 'Other', 'Mini-SAS HD', 3, 'IOM A SAS'), R('io', 'Other', 'Mini-SAS HD', 3, 'IOM B SAS'), PSU(2)],
    'Expansion shelf for MSA 2060/2062. Two I/O modules. Check: SAS ports per I/O module (3 assumed) and part number.',
    *MSA_SRC, verified=False, full=True)

HP_('msl3040-base', 'MSL3040 Base Module', 'StoreEver MSL3040 tape library base module (3U, 40 slots)', 'StoreEver tape',
    'computer', 3,
    [SLOT(3, 'LTO drive bay (SAS or FC)'), RJ(1, 'Mgmt', 'rear'), USBA(1, 'USB', 'rear'), PSU(1)],
    '3U base module, 40 cartridge slots, LTO-7/8/9 half-height SAS or FC drives. Scales to 48U (15 x 3U expansion modules) and '
    '640 slots. Add each drive\'s SAS (mini-SAS HD) or FC (LC) port as an extra port. Check: drive bays per module (3 assumed), '
    'management and USB ports, PSU count (second PSU optional).',
    'HPE StoreEver MSL3040 data sheet', 'https://www.hpe.com/us/en/product-catalog/storage/tape-storage/pip.hpe-storeever-msl3040-tape-library.html',
    verified=False, full=True)
HP_('msl3040-exp', 'MSL3040 Expansion Module', 'StoreEver MSL3040 tape library expansion module (3U)', 'StoreEver tape',
    'computer', 3, [SLOT(3, 'LTO drive bay (SAS or FC)'), PSU(1)],
    '3U expansion module for the MSL3040, mounted below the base module. Check: drive bays, slot count and PSU.',
    'HPE StoreEver MSL3040 data sheet', 'https://www.hpe.com/us/en/product-catalog/storage/tape-storage/pip.hpe-storeever-msl3040-tape-library.html',
    verified=False, full=True)
HP_('msl-1-8-g2', 'MSL 1/8 G2', 'StoreEver 1/8 G2 tape autoloader (1U, 8 slots)', 'StoreEver tape', 'computer', 1,
    [R('io', 'Other', 'Mini-SAS HD', 1, 'Drive SAS'), RJ(1, 'Mgmt', 'rear'), PSU(1)],
    '1U autoloader with one half-height LTO drive and 8 cartridge slots (two 4-slot magazines). Check: SAS connector (older '
    'units have mini-SAS) and FC drive versions.',
    'HPE StoreEver 1/8 G2 autoloader QuickSpecs', 'https://www.hpe.com/us/en/product-catalog/storage/tape-storage.html',
    verified=False, full=True)

# =====================================================================================================================
# HPE rack power and KVM
# =====================================================================================================================
G2 = ('HPE G2 Basic PDUs QuickSpecs (INTL models)', 'https://www.hpe.com/us/en/collaterals/collateral.c05324691.html')
def pdu(pn, name, mount, phase, amps, plug, cord, outlets, ncirc, length=None, kva=None, note=''):
    circ = []
    for i in range(ncirc):
        c = dict(id='ABCDEF'[i], type='mcb', amps=16)
        if phase == 3: c['phase'] = 'L%d' % (i * 3 // ncirc + 1)
        circ.append(c)
    outs = []
    for i in range(ncirc):
        for t, n in outlets: outs.append(dict(type=t, count=n // ncirc, circuit='ABCDEF'[i]))
    blk = dict(mount=mount, phase=phase, volts=230 if phase == 1 else 400, amps=amps, plug=plug, cordM=cord, metering='none',
               main=dict(type='none'), circuits=circ, outlets=outs)
    if mount == 'v': blk.update(lengthMm=length, widthMm=52, cordEnd='bottom')
    total = ', '.join(f'{n} x {t.upper()}' for t, n in outlets)
    HP_(pn.lower(), pn, f'G2 Basic PDU {name}, {total}', 'G2 PDU', 'pdu', 1, [],
        f'{kva} kVA basic (unmetered) PDU, {ncirc} x 16 A single-pole breakers. ' + note +
        ('Check: strip length (estimated). ' if mount == 'v' else 'Mounts in 1U or in the 0U space at the side of an HPE rack. '),
        *G2, pdu=blk)
pdu('P9Q43A', '1U 32 A single phase', 'h', 1, 32, 'cee32', 3.6, [('c19', 6)], 2, kva=7.3)
pdu('P9Q44A', '1U 32 A single phase', 'h', 1, 32, 'cee32', 3.6, [('c13', 12)], 2, kva=7.3)
pdu('P9Q45A', 'half-height 32 A single phase', 'v', 1, 32, 'cee32', 3.0, [('c13', 20)], 2, length=1000, kva=7.3)
pdu('P9Q46A', 'mid-height 32 A single phase', 'v', 1, 32, 'cee32', 3.0, [('c13', 36), ('c19', 6)], 2, length=1400, kva=7.3)
pdu('P9Q63A', '1U 32 A three phase', 'h', 3, 32, 'cee3p32', 3.6, [('c19', 6)], 6, kva=22)
pdu('P9Q65A', 'full-height 32 A three phase', 'v', 3, 32, 'cee3p32', 3.0, [('c13', 36), ('c19', 12)], 6, length=1800, kva=22,
    note='High-density strip mounted on its side, outlets facing the back of the rack. ')

HP_('tft7600-g2', 'TFT7600 G2', 'TFT7600 G2 KVM console, 17.3 in LCD and keyboard, 1U', 'KVM consoles', 'control', 1,
    [R('in', 'Other', 'VGA', 1, 'Video In'), R('in', 'USB', 'USB-A', 1, 'Keyboard/mouse (USB)'),
     R('in', 'Other', 'Mini-DIN 6', 2, 'Keyboard/mouse (PS/2)'), F('io', 'USB', 'USB-A', 1, 'USB pass-through'), PSU(1)],
    '1U slide-out console, 17.3 in 1440 x 900 LCD, keyboard and touch pad (regional keyboard SKUs AZ870A to AZ879A). No KVM '
    'switch inside: pair it with an HPE KVM console switch or wire it to one server. Check: rear connectors and power inlet.',
    'HPE TFT7600 G2 listings', 'https://buy.hpe.com/us/en/rack-power-infrastructure-products/rack-options/rack-console-options/c/1009830188',
    verified=False)
HP_('af621a', 'AF621A', '0x2x16 G2 KVM IP console switch, 1U', 'KVM consoles', 'control', 1,
    [R('io', 'KVM link', 'RJ45', 16, 'ARI port (Cat 5 to interface adapter)'), RJ(2, 'LAN (remote users)', 'rear'),
     R('out', 'Other', 'VGA', 1, 'Local console VGA'), R('io', 'USB', 'USB-A', 2, 'Local console USB'), PSU(2)],
    '16 server ports over Cat 5 to HPE KVM interface adapters (USB or PS/2 + VGA), 2 remote IP users plus one local console '
    '(pairs with the TFT7600). Check: local console connectors, setup port and PSU count.',
    'HPE KVM switch QuickSpecs', 'https://buy.hpe.com/us/en/rack-power-infrastructure-products/rack-options/kvm-switches/c/1009830189',
    verified=False)

# =====================================================================================================================
# HPE (non-Aruba) switches: FlexFabric and OfficeConnect
# =====================================================================================================================
FF = 'Console (RJ45), management Ethernet and USB on the port side. Check: panel positions. '
HP_('jq074a', 'JQ074A', 'FlexFabric 5945 48SFP28 8QSFP28 switch', 'FlexFabric 5945', 'network', 1,
    [CAGE(48, 'SFP28', '1/10/25G'), CAGE(8, 'QSFP28', '40/100G'), CONS(), RJ(1, 'Mgmt'), USBA(1, 'USB', 'front'), PSU(2)],
    FF + 'Two hot-swap PSUs and five fan trays, port-to-power or power-to-port airflow (ordered separately). Data centre ToR '
    'switch running Comware 7.', 'HPE FlexFabric 5945 Switch Series QuickSpecs',
    'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-flexfabric-5945-switch-series/p/1010952223',
    verified=False)
HP_('jq077a', 'JQ077A', 'FlexFabric 5945 32QSFP28 switch', 'FlexFabric 5945', 'network', 1,
    [CAGE(32, 'QSFP28', '40/100G'), CONS(), RJ(1, 'Mgmt'), USBA(1, 'USB', 'front'), PSU(2)],
    FF + 'Two hot-swap PSUs, fan trays ordered separately. Check: RU (1U assumed).', 'HPE FlexFabric 5945 Switch Series QuickSpecs',
    'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-flexfabric-5945-switch-series/p/1010952223',
    verified=False)
OC = 'Front: ports, console. Rear: fixed internal PSU (C14). Check: console connector. '
for pn, nm, rj, poe in [('JG960A', '24G 2SFP+ 2XGT', 24, ''), ('JG961A', '48G 2SFP+ 2XGT', 48, ''),
                        ('JG962A', '24G 2SFP+ 2XGT PoE+ 370W', 24, ' PoE+'), ('JG963A', '48G 2SFP+ 2XGT PoE+ 370W', 48, ' PoE+')]:
    HP_(pn.lower(), pn, f'OfficeConnect 1950 {nm} switch', 'OfficeConnect 1950', 'network', 1,
        [RJ(rj, '1G' + poe), RJ(2, '10GBASE-T'), CAGE(2, 'SFP+', '10G SFP+'), CONS(), PSU(1)],
        OC + 'Web-managed smart switch, stacks over the 10G ports.', 'HPE OfficeConnect 1950 data sheet',
        'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-officeconnect-1950-switch-series/p/7074854',
        verified=False)
for pn, nm, rj, sfp in [('JL381A', '24G 2SFP', 24, 2), ('JL382A', '48G 4SFP', 48, 4)]:
    HP_(pn.lower(), pn, f'OfficeConnect 1920S {nm} switch', 'OfficeConnect 1920S', 'network', 1,
        [RJ(rj, '1G'), CAGE(sfp, 'SFP', '1G SFP'), PSU(1)],
        'Web-managed smart switch, fanless, no console port. Check: PSU (internal assumed).', 'HPE OfficeConnect 1920S data sheet',
        'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-officeconnect-1920s-switch-series/p/1009148840',
        verified=False)

# =====================================================================================================================
# HP Inc workstations (rack and rack-mountable)
# =====================================================================================================================
HPI = lambda *a, **k: add('hp.json', 'hp-', 'HP', *a, **k)
HPI('z4-rack-g5', 'Z4 Rack G5', 'Z4 Rack G5 1U rack workstation', 'Z by HP rack', 'computer', 1,
    [F('io', 'USB', 'USB-C', 2, 'USB-C 20Gb'), F('io', 'USB', 'USB-A', 2, 'USB-A 5Gb'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headset'),
     USBA(2, 'USB-A 5Gb'), RJ(1, '1GbE (AMT)', 'rear'), SLOT(1, 'Flex port (serial, 10GbE, 2.5GbE or fibre)'),
     SLOT(3, 'PCIe Gen5 slot'), GPU(), PSU(2)],
    '1U Intel Xeon W-2400/2500 workstation, 43 x 487 x 675 mm, from 9.5 kg. Front ports shown for the Premium front panel (Entry has '
    '4 x USB-A). 1 PCIe Gen5 x16 slot standard, 2 more optional; 1 or 2 x 675 W PSUs (redundant or 1350 W combined). Remote '
    'management through HP Anyware Remote System Controller options. GPU DisplayPort count depends on the card (4 assumed). '
    'Check: PSU inlet (C14 assumed).',
    'StorageReview HP Z4 Rack G5 review (HP spec table)', 'https://www.hp.com/us-en/workstations/z4-rack.html', full=True)
HPI('zcentral-4r', 'ZCentral 4R', 'ZCentral 4R 1U rack workstation (legacy)', 'Z by HP rack', 'computer', 1,
    [F('io', 'USB', 'USB-A', 2, 'USB-A'), USBA(2, 'USB-A'), RJ(1, '1GbE', 'rear'), SLOT(3, 'PCIe slot'), GPU(), PSU(2)],
    '1U Intel Xeon W-2200 workstation (2020-2023), forerunner of the Z4 Rack G5. Optional redundant 675 W PSUs. Check: front and '
    'rear port counts.', 'HP ZCentral 4R QuickSpecs', 'https://www.hp.com/us-en/workstations/zcentral-4r.html', verified=False, full=True)
ZRAIL = ('Tower lying on its side on the HP Z2/Z4/Z6 Depth Adjustable Fixed Rail Rack Kit (2A8Y5AA), 4U. ')
HPI('z4-g5', 'Z4 G5', 'Z4 G5 tower workstation on rack rails (4U)', 'Z by HP tower', 'computer', 4,
    [F('io', 'USB', 'USB-C', 2, 'USB-C'), F('io', 'USB', 'USB-A', 2, 'USB-A'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headset'),
     USBA(4, 'USB-A'), RJ(1, '1GbE', 'rear'), R('io', 'Analog audio', '3.5mm jack', 2, 'Line in / out'), SLOT(4, 'PCIe slot'), GPU(), PSU(1)],
    ZRAIL + 'Intel Xeon W-2400 tower. A common host for broadcast graphics and replay software. Check: port counts and the rack '
    'kit for G5 (the 2A8Y5AA kit lists Z4 G5).', 'HP Z4 G5 QuickSpecs and HP workstation rack mounting guide',
    'https://www.hp.com/us-en/workstations/z4.html', verified=False, full=True)
HPI('z4-g4', 'Z4 G4', 'Z4 G4 tower workstation on rack rails (4U, legacy)', 'Z by HP tower', 'computer', 4,
    [F('io', 'USB', 'USB-A', 4, 'USB-A'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headset'), USBA(4, 'USB-A'), RJ(1, '1GbE', 'rear'),
     R('io', 'Analog audio', '3.5mm jack', 2, 'Line in / out'), SLOT(5, 'PCIe slot'), GPU(), PSU(1)],
    ZRAIL + 'Intel Xeon W-2100/2200 tower (2017-2022), widely used under broadcast graphics engines. Check: port counts.',
    'HP workstation rack mounting guide', 'https://support.hp.com/us-en/product/details/hp-z4-g4-workstation/16449016',
    verified=False, full=True)
HPI('z8-g4', 'Z8 G4', 'Z8 G4 tower workstation on rack rails (5U, legacy)', 'Z by HP tower', 'computer', 5,
    [F('io', 'USB', 'USB-A', 4, 'USB-A'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headset'), USBA(4, 'USB-A'),
     RJ(2, '1GbE', 'rear'), R('io', 'Analog audio', '3.5mm jack', 2, 'Line in / out'), SLOT(7, 'PCIe slot'), GPU(), PSU(1)],
    'Dual Xeon Scalable tower (2017-2023) on the HP Z640/Z840/Z8 G4 Rail Rack Kit (2FZ77AA), 5U. A common host for Vizrt and '
    'other broadcast graphics engines. 1125 W or 1450 W PSU (1700 W needs a C19/C20 cord). Check: port counts.',
    'HP workstation rack mounting guide', 'https://support.hp.com/us-en/product/details/hp-z8-g4-workstation/16449030',
    verified=False, full=True)
HPI('z8-fury-g5', 'Z8 Fury G5', 'Z8 Fury G5 tower workstation on rack rails (5U)', 'Z by HP tower', 'computer', 5,
    [F('io', 'USB', 'USB-C', 2, 'USB-C'), F('io', 'USB', 'USB-A', 2, 'USB-A'), F('out', 'Analog audio', '3.5mm jack', 1, 'Headset'),
     USBA(4, 'USB-A'), RJ(1, '10GbE', 'rear'), RJ(1, '1GbE', 'rear'), SLOT(7, 'PCIe slot'), GPU(), PSU(1)],
    'Xeon W-3400 tower with up to four double-width GPUs. Check: rack kit and height (5U assumed, as the Z8 G4) and port counts.',
    'HP Z8 Fury G5 QuickSpecs', 'https://www.hp.com/us-en/workstations/z8-fury.html', verified=False, full=True)
HPI('z2-mini-g9', 'Z2 Mini G9', 'Z2 Mini G9 mini workstation', 'Z by HP mini', 'computer', 2,
    [F('io', 'USB', 'USB-C', 2, 'USB-C 20Gb (side)'), F('io', 'USB', 'USB-A', 1, 'USB-A 10Gb (side)'),
     F('out', 'Analog audio', '3.5mm jack', 1, 'Headset (side)'), R('out', 'DisplayPort', 'DisplayPort', 2, 'DisplayPort 1.4'),
     USBA(3, 'USB-A 10Gb'), RJ(1, '1GbE', 'rear'), SLOT(2, 'Flex IO'), R('in', 'Power', 'DC barrel', 1, 'DC In')],
    'Mini workstation, 211 x 218 x 69 mm, 2.4 kg, external 180 W or 280 W adapter. Two Flex IO bays (serial, extra USB, DP, HDMI, '
    'VGA, Thunderbolt 3, 2.5GbE, 10GbE or fibre). With a discrete GPU (RTX A2000 etc.) add its mini DisplayPorts. Sits on a shelf, '
    'or up to 7 stand upright in 5U with HP rack brackets.',
    'StorageReview HP Z2 Mini G9 review (HP spec table)', 'https://www.hp.com/us-en/workstations/z2-mini.html',
    w=6, boxMm=dict(w=211, h=69), formFactor='HP Z2 Mini')

# =====================================================================================================================
# HPE Aruba Networking (gaps beyond aruba.json)
# =====================================================================================================================
AR = lambda *a, **k: add('aruba-more.json', 'aruba-', 'HPE Aruba Networking', *a, **k)
U62 = 'https://www.hpe.com/us/en/aruba-cx-6200-switch-series.html'
for pn, nm, rj, poe, pw in [('JL724A', '24G 4SFP+', 24, '', ''), ('JL725A', '24G Class4 PoE 4SFP+ 370W', 24, ' Class 4 PoE', '370 W PoE. '),
                            ('JL726A', '48G 4SFP+', 48, '', ''), ('JL727A', '48G Class4 PoE 4SFP+ 370W', 48, ' Class 4 PoE', '370 W PoE. '),
                            ('JL728A', '48G Class4 PoE 4SFP+ 740W', 48, ' Class 4 PoE', '740 W PoE. ')]:
    AR(pn.lower(), pn, f'CX 6200F {nm} switch', 'CX 6200F', 'network', 1,
       [RJ(rj, '1G' + poe), CAGE(4, 'SFP+', '1/10G uplink (VSF stacking)'), CONS(conn='USB-C', label='Console (USB-C)'),
        RJ(1, 'OOBM'), USBA(1, 'USB', 'front'), PSU(1)],
       pw + 'Fixed internal PSU, stacks (VSF) over the SFP+ ports. Check: positions of console, OOBM and USB (drawn on the port side) '
       'and that the JL724A is the non-PoE model.', 'HPE Aruba Networking CX 6200 data sheet', U62, verified=False)
U61 = 'https://www.hpe.com/us/en/aruba-cx-6100-switch-series.html'
for pn, nm, rj, poe, pw, w in [('JL675A', '48G Class4 PoE 4SFP+ 370W', 48, ' Class 4 PoE', '370 W PoE. ', 12),
                               ('JL676A', '48G 4SFP+', 48, '', '', 12),
                               ('JL677A', '24G Class4 PoE 4SFP+ 370W', 24, ' Class 4 PoE', '370 W PoE. ', 12),
                               ('JL678A', '24G 4SFP+', 24, '', '', 12)]:
    AR(pn.lower(), pn, f'CX 6100 {nm} switch', 'CX 6100', 'network', 1,
       [RJ(rj, '1G' + poe), CAGE(4, 'SFP+', '1/10G uplink'), CONS(conn='USB-C', label='Console (USB-C)'), PSU(1)],
       pw + 'Entry access switch, fixed internal PSU. Check: console connector (USB-C assumed) and any OOBM port.',
       'HPE Aruba Networking CX 6100 data sheet', U61, verified=False)
AR('jl679a', 'JL679A', 'CX 6100 12G Class4 PoE 2G/2SFP+ 139W switch', 'CX 6100', 'network', 1,
   [RJ(12, '1G Class 4 PoE'), RJ(2, '1G uplink'), CAGE(2, 'SFP+', '1/10G uplink'), CONS(conn='USB-C', label='Console (USB-C)'),
    PSU(1)],
   'Compact fanless desktop / rack switch, 139 W PoE, half-width (rack kit). Check: console connector and PSU (internal assumed).',
   'HPE Aruba Networking CX 6100 listing', U61, verified=False, w=6)
AR('r9w86a', 'R9W86A', 'CX 8100 24 x 10G SFP+ + 4 x 40/100G QSFP28 switch', 'CX 8100', 'network', 1,
   [CAGE(24, 'SFP+', '1/10G'), CAGE(4, 'QSFP28', '40/100G'), CONS(), RJ(1, 'OOBM'), USBA(1, 'USB', 'front'), PSU(2)],
   'Bundle with front-to-back airflow, 3 fans and 2 AC PSUs. Collapsed-core / aggregation switch. Check: console, OOBM and USB '
   'positions.', 'HPE Aruba Networking CX 8100 listing',
   'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-aruba-networking-cx-8100-switch-series/p/1014733547',
   verified=False)
AR('cx8100-40xt8xf4c', 'CX 8100-40XT8XF4C', 'CX 8100 40 x 10GBASE-T + 8 x 10G SFP+ + 4 x 40/100G QSFP28 switch', 'CX 8100',
   'network', 1, [RJ(40, '1/10GBASE-T'), CAGE(8, 'SFP+', '1/10G'), CAGE(4, 'QSFP28', '40/100G'), CONS(), RJ(1, 'OOBM'),
                  USBA(1, 'USB', 'front'), PSU(2)],
   'Two hot-swap AC PSUs. Check: order number for your airflow and region, and console/OOBM positions.',
   'HPE Aruba Networking CX 8100 listing',
   'https://buy.hpe.com/us/en/networking/switches/fixed-port-l3-managed-ethernet-switches/hpe-aruba-networking-cx-8100-switch-series/p/1014733547',
   verified=False)
AR('r9a29a', 'R9A29A', 'CX 9300-32D 32 x 400G QSFP-DD switch', 'CX 9300', 'network', 1,
   [CAGE(32, 'QSFP-DD', '100/200/400G'), CAGE(2, 'SFP+', '10G'), CONS(), F('io', 'USB', 'Micro-USB', 1, 'Console (USB)'),
    RJ(1, 'OOBM'), PSU(2)],
   'Front-to-back airflow bundle (R9A30A is back-to-front) with 6 fans and 2 x 1500 W hot-swap PSUs. 675 W at full traffic, '
   '590 mm deep, 11.9 kg. Spine / high-bandwidth ST 2110 core. Check: console and OOBM panel.',
   'HPE Aruba Networking CX 9300 data sheet', 'https://www.hpe.com/us/en/aruba-cx-9300-switch-series.html', powerW=675,
   weightKg=11.9, full=True)
AR('cx10000-48y6c', 'CX 10000-48Y6C', 'CX 10000 48 x 25G + 6 x 100G distributed services switch', 'CX 10000', 'network', 1,
   [CAGE(48, 'SFP28', '1/10/25G'), CAGE(6, 'QSFP28', '40/100G'), CONS(), RJ(1, 'OOBM'), USBA(1, 'USB', 'front'), PSU(2)],
   'Data centre ToR switch with AMD Pensando DPUs for stateful firewall and telemetry. Two hot-swap PSUs. Check: order number, '
   'console/OOBM positions.', 'HPE Aruba Networking CX 10000 data sheet',
   'https://www.hpe.com/us/en/aruba-cx-10000-switch-series.html', verified=False, full=True)
for pn, nm, rj, poe in [('JL354A', '24G 4SFP+', 24, ''), ('JL355A', '48G 4SFP+', 48, ''),
                        ('JL356A', '24G PoE+ 4SFP+', 24, ' PoE+'), ('JL357A', '48G PoE+ 4SFP+', 48, ' PoE+')]:
    AR(pn.lower(), pn, f'2540 {nm} switch', '2540', 'network', 1,
       [RJ(rj, '1G' + poe), CAGE(4, 'SFP+', '1/10G uplink'), CONS(), PSU(1)],
       'ArubaOS-Switch access switch, fixed PSU. Check: console connector and PoE budget.', 'Aruba 2540 data sheet',
       'https://www.hpe.com/us/en/aruba-2540-switch-series.html', verified=False)
IO = 'https://www.arubainstanton.com/products/switches/'
for pn, nm, rj, xgt, sfp, conn, poe in [
        ('JL682A', '1930 24G 4SFP/SFP+', 24, 0, 4, 'SFP+', ''), ('JL683A', '1930 24G Class4 PoE 4SFP/SFP+ 195W', 24, 0, 4, 'SFP+', ' PoE (195 W)'),
        ('JL684B', '1930 24G Class4 PoE 4SFP/SFP+ 370W', 24, 0, 4, 'SFP+', ' PoE (370 W)'), ('JL685A', '1930 48G 4SFP/SFP+', 48, 0, 4, 'SFP+', ''),
        ('JL686B', '1930 48G Class4 PoE 4SFP/SFP+ 370W', 48, 0, 4, 'SFP+', ' PoE (370 W)'),
        ('JL805A', '1960 12XGT 4SFP+', 0, 12, 4, 'SFP+', ''), ('JL806A', '1960 24G 2XGT 2SFP+', 24, 2, 2, 'SFP+', ''),
        ('JL807A', '1960 24G 20p Class4 4p Class6 PoE 2XGT 2SFP+ 370W', 24, 2, 2, 'SFP+', ' PoE (370 W)'),
        ('JL808A', '1960 48G 2XGT 2SFP+', 48, 2, 2, 'SFP+', ''),
        ('JL809A', '1960 48G 40p Class4 8p Class6 PoE 2XGT 2SFP+ 600W', 48, 2, 2, 'SFP+', ' PoE (600 W)')]:
    p = []
    if rj: p.append(RJ(rj, '1G' + poe))
    if xgt: p.append(RJ(xgt, '1/10GBASE-T'))
    p += [CAGE(sfp, conn, '1/10G uplink'), PSU(1)]
    AR(pn.lower(), pn, f'Instant On {nm} switch', 'Instant On ' + nm[:4], 'network', 1, p,
       'Cloud or web managed small-business switch (Instant On app), no console port, 1U with rack ears. Check: PoE budget and '
       'port split from the order name, and uplink count on the 48G 1960 (some lists give 4 SFP+).',
       'HPE Aruba Networking Instant On switch comparison', IO, verified=False)

AR('r7h97a', 'R7H97A', '9240 campus gateway (RW), 4 x SFP28', '9200 gateway', 'network', 1,
   [CAGE(4, 'SFP28', '1/10/25G'), RJ(1, 'OOBM'), CONS(), F('io', 'USB', 'USB-C', 1, 'Console (USB-C)'), USBA(2, 'USB 3.0', 'front'),
    SLOT(1, 'Expansion slot (reserved)', 'front'), PSU(2)],
   'Wireless/SD-Branch gateway (mobility controller), up to 2K APs with the Gold licence, 190 W max, 440 x 442 x 396 mm, 8.2 kg. '
   'One 550 W PSU plus a redundant slot (change the count to 1 if only one fitted). US model R7H95A, FIPS/TAA R7J02A/R7J03A. '
   'Check: which panel holds console and OOBM.', 'HPE Aruba Networking 9200 Series data sheet',
   'https://www.hpe.com/us/en/aruba-9200-series-campus-gateways.html', powerW=190, weightKg=8.2)

# --- CX 6400 modular chassis (frames) and line modules (cards) ---
CX64 = 'Aruba CX 6400'
MM = []
for i in (1, 2):
    MM += [F('io', 'Other', 'RJ45', 1, f'MM{i} Console'), F('io', 'USB', 'USB-C', 1, f'MM{i} Console (USB-C)'),
           F('io', 'Ethernet', 'RJ45', 1, f'MM{i} OOBM'), F('io', 'USB', 'USB-A', 1, f'MM{i} USB')]
for pn, nm, ru, slots, fans in [('R0X26A', '6405', 7, 5, 2), ('R0X27A', '6410', 12, 10, 4)]:
    AR(pn.lower(), pn, f'CX {nm} chassis, {slots} line module slots', 'CX 6400', 'frame', ru,
       MM + [R('in', 'Power', 'IEC C16', 4, 'PSU')],
       f'{ru}U modular switch: 2 management modules (R0X31A, slots 1-2, shown as fixed frame ports) and {slots} line modules '
       f'(chassis slots 3 to {slots + 2}; app slot n is chassis slot n + 2). Up to 4 PSUs: 1800 W R0X35A (C16 inlet) or 3000 W '
       f'R0X36A (C20 inlet), not mixed. {fans} fan trays. Check: line module orientation and slot order on the drawing.',
       'Aruba 6400 Installation and Getting Started Guide', 'https://www.hpe.com/us/en/aruba-cx-6400-switch-series.html',
       verified=True, full=True,
       frame=dict(system=CX64, slots=slots, slotOrder='ltr', orient='h', rearAlign=1, door=False,
                  controller='Two R0X31A management modules (console, USB-C console, OOBM, USB each)',
                  front=dict(x0=0.05, x1=0.95, y0=0.04, y1=0.80 if slots == 5 else 0.88),
                  rear=dict(x0=0.05, x1=0.95, y0=0.04, y1=0.96)))
NOREAR = [dict(partNumber='none', name='No rear connections (front-loading module)', width=1, cardsPerModule=1, cardOffset=0,
               default=True, portGroups=[], included=True)]
for pn, nm, ports in [
        ('R0X39C', '48p 1GbE Class 4 PoE and 4p SFP56 v2 module', [RJ(48, '1G Class 4 PoE'), CAGE(4, 'SFP56', '1/10/25/50G')]),
        ('R0X40C', '48p 1GbE Class 6 PoE and 4p SFP56 v2 module', [RJ(48, '1G Class 6 PoE'), CAGE(4, 'SFP56', '1/10/25/50G')]),
        ('R0X41C', '48p Smart Rate 1/2.5/5GbE Class 6 PoE and 4p SFP56 v2 module', [RJ(48, '1/2.5/5G Class 6 PoE'), CAGE(4, 'SFP56', '1/10/25/50G')]),
        ('R0X42C', '24p 10GBASE-T and 4p SFP56 v2 module', [RJ(24, '1/10GBASE-T'), CAGE(4, 'SFP56', '1/10/25/50G')]),
        ('R0X43C', '24p SFP+ and 4p SFP56 v2 module', [CAGE(24, 'SFP+', '1/10G'), CAGE(4, 'SFP56', '1/10/25/50G')]),
        ('R0X44C', '48p 1/10/25GbE SFP28 extended tables v2 module', [CAGE(48, 'SFP28', '1/10/25G')]),
        ('R0X45C', '12p 40/100GbE QSFP28 extended tables v2 module', [CAGE(12, 'QSFP28', '40/100G')])]:
    AR(pn.lower(), pn, f'6400 {nm}', 'CX 6400 modules', 'card', 0, ports,
       'Line module for the CX 6405 / 6410 (ports on the module face). B and A versions have the same ports.',
       'Aruba 6400 Installation and Getting Started Guide', 'https://www.hpe.com/us/en/aruba-cx-6400-switch-series.html',
       w=0, card=dict(fits=[CX64], slotWidth=1), rearModules=NOREAR)

# =====================================================================================================================
# IBM
# =====================================================================================================================
IB = lambda *a, **k: add('ibm.json', 'ibm-', 'IBM', *a, **k)
P10 = ('IBM Power10 S1012/S1014/S1022s/S1022/S1024 Redpaper REDP-5675', 'https://www.redbooks.ibm.com/redpapers/pdfs/redp5675.pdf')
def pw_ports(pcie, psu, conn='IEC C14'):
    return [F('io', 'USB', 'USB-A', 1, 'USB 3.0'), USBA(2, 'USB 3.0'), RJ(2, 'HMC 1GbE', 'rear'),
            R('io', 'Other', 'RJ45', 1, 'System port'), SLOT(pcie, 'PCIe slot'), PSU(psu, conn)]
PWN = 'Network, Fibre Channel and SAS ports come from the PCIe adapters fitted: add them as extra ports. '
IB('9105-41b', '9105-41B', 'Power S1014 4U single-socket Power10 server', 'Power10', 'computer', 4, pw_ports(5, 2),
   '4U rack (also a desk-side tower). 5 usable PCIe slots (4 Gen5, 1 Gen4), up to 10 with an expansion drawer. Two hot-swap PSUs: '
   '1200 W (100-127 or 200-240 V) or 1600 W (200-240 V, needed for the 24-core option). eBMC management. ' + PWN +
   'Check: PSU inlet (C14 assumed).', *P10, full=True)
IB('9105-22b', '9105-22B', 'Power S1022s 2U Power10 server', 'Power10', 'computer', 2, pw_ports(10, 2),
   '2U, one or two sockets. 10 PCIe slots (5 usable with one socket; 8 Gen5, 2 Gen4). Two 1000 W PSUs (100-127 or 200-240 V). '
   + PWN + 'Check: PSU inlet.', *P10, full=True)
IB('9105-22a', '9105-22A', 'Power S1022 2U Power10 server', 'Power10', 'computer', 2, pw_ports(10, 2),
   '2U, one or two sockets. 10 PCIe slots (5 usable with one socket). Two 2000 W PSUs, 200-240 V only. ' + PWN +
   'Check: PSU inlet (C14 assumed; 2000 W supplies may take C20).', *P10, full=True)
IB('9105-42a', '9105-42A', 'Power S1024 4U Power10 server', 'Power10', 'computer', 4, pw_ports(10, 4),
   '4U, one or two sockets. 10 PCIe slots (5 usable with one socket). Four 1600 W PSUs, 200-240 V only. ' + PWN +
   'Check: PSU inlet.', *P10, full=True)
IB('9043-mrx', '9043-MRX', 'Power E1050 4U four-socket Power10 server', 'Power10', 'computer', 4, pw_ports(11, 4),
   '4U, two to four sockets, eBMC management. Check: PCIe slot count (11 assumed), PSU count and rating (4 x 2300 W assumed), '
   'and front/rear USB.', 'IBM Power E1050 Redpaper REDP-5684', 'https://www.redbooks.ibm.com/redpapers/pdfs/redp5684.pdf',
   verified=False, full=True)
IB('9824-22a', '9824-22A', 'Power S1122 2U Power11 server', 'Power11', 'computer', 2, pw_ports(10, 2),
   'Power11 successor to the S1022 (2025). Check: ports, PCIe slots and PSUs (taken from the S1022).',
   'IBM Power11 documentation (9824-22A)', 'https://www.ibm.com/docs/en/power11/9824-22A', verified=False, full=True)
IB('9824-42a', '9824-42A', 'Power S1124 4U Power11 server', 'Power11', 'computer', 4, pw_ports(10, 4),
   'Power11 successor to the S1024 (2025). Check: ports, PCIe slots and PSUs (taken from the S1024).',
   'IBM Power11 documentation', 'https://www.ibm.com/products/power-s1124', verified=False, full=True)
IB('7063-cr2', '7063-CR2', 'Hardware Management Console (HMC) 1U', 'Power HMC', 'computer', 1,
   [VGA(), USBA(2, 'USB'), RJ(4, '1GbE', 'rear'), RJ(1, 'BMC', 'rear'), PSU(2)],
   'Rack-mount HMC appliance for managing Power servers (connects to their HMC ports). Check: all ports (from the 7063-CR1 '
   'cabling guide pattern).', 'IBM 7063 HMC cabling documentation', 'https://www.ibm.com/docs/en/power10?topic=hmc-7063-cr2',
   verified=False, full=True)
FS = ('IBM FlashSystem portfolio specifications', 'https://www.ibm.com/flashsystem')
def fs_ports(onboard, slots):
    p = []
    for c in ('1', '2'):
        p += [R('io', 'Ethernet', 'RJ45', 1, f'Canister {c} Mgmt / tech port')]
        if onboard: p.append(onboard(c))
        p.append(SLOT(slots, f'Canister {c} host adapter slot'))
    return p + [PSU(2)]
FSN = 'Two node canisters; host interface adapters (FC 32/64G, iSCSI/NVMe-TCP 10/25/100GbE) go in the canister slots: add their ports. '
IB('fs5015', 'FlashSystem 5015', 'FlashSystem 5015 2U storage (12 LFF or 24 SFF)', 'FlashSystem', 'computer', 2,
   fs_ports(lambda c: R('io', 'Ethernet', 'RJ45', 2, f'Canister {c} 1GbE iSCSI'), 1),
   'Entry hybrid array, 1 Gb iSCSI standard; options FC 16G, iSCSI 10G, SAS 12G. Up to 8 host ports. ' + FSN +
   'Check: onboard ports and slots per canister.', *FS, verified=False, full=True)
IB('fs5045', 'FlashSystem 5045', 'FlashSystem 5045 2U storage (12 LFF or 24 SFF)', 'FlashSystem', 'computer', 2,
   fs_ports(lambda c: R('io', 'SFP', 'SFP+', 2, f'Canister {c} 10GbE iSCSI'), 1),
   'Entry hybrid array, 10 Gb iSCSI standard; options FC 16G, iSCSI 10G, SAS 12G. Up to 8 host ports. ' + FSN +
   'Check: onboard ports and slots per canister.', *FS, verified=False, full=True)
IB('fs5300', 'FlashSystem 5300', 'FlashSystem 5300 1U NVMe storage (12 x 2.5 in)', 'FlashSystem', 'computer', 1,
   fs_ports(lambda c: R('io', 'SFP', 'SFP28', 2, f'Canister {c} 25GbE'), 1),
   '1U all-flash NVMe array, 25/10 Gb iSCSI or NVMe/TCP standard; options FC 32G/64G. Up to 16 host ports. ' + FSN +
   'Check: onboard ports and slots per canister.', *FS, verified=False, full=True)
IB('fs7300', 'FlashSystem 7300', 'FlashSystem 7300 2U NVMe storage (24 x 2.5 in)', 'FlashSystem', 'computer', 2,
   fs_ports(lambda c: R('io', 'SFP', 'SFP+', 4, f'Canister {c} 10GbE'), 3),
   '2U all-flash NVMe array, 10 Gb iSCSI standard; options FC 32G/64G, 25/100 Gb iSCSI or NVMe/TCP. Up to 24 host ports. ' + FSN +
   'Check: onboard ports and slots per canister.', *FS, verified=False, full=True)
IB('fs9500', 'FlashSystem 9500', 'FlashSystem 9500 4U NVMe storage (48 x 2.5 in)', 'FlashSystem', 'computer', 4,
   fs_ports(None, 6) + [PSU(2, label='PSU (second pair)')],
   '4U all-flash array, 48 FlashCore Modules, up to 48 host ports (FC 32G/64G, 10/25/100 Gb iSCSI or NVMe/TCP). ' + FSN +
   'Check: adapter slots per canister and PSU count (4 assumed).', *FS, verified=False, full=True)
IB('ts4300', 'TS4300 3555-L3A', 'TS4300 tape library base module (3U)', 'IBM tape', 'computer', 3,
   [SLOT(3, 'LTO drive bay (SAS or FC)'), RJ(1, 'Mgmt', 'rear'), USBA(1, 'USB', 'rear'), PSU(1)],
   '3U modular LTO library, up to 3 half-height drives and 40 slots per module, stacks to 7 modules (21U). Add each drive\'s SAS or '
   'FC port. Check: drive bays and slots per module, PSU count.', 'IBM TS4300 product page',
   'https://www.ibm.com/products/ts4300-tape-library', verified=False, full=True)
IB('ts2900', 'TS2900 3572-S4H', 'TS2900 tape autoloader (1U, 9 slots)', 'IBM tape', 'computer', 1,
   [R('io', 'Other', 'Mini-SAS HD', 1, 'Drive SAS'), RJ(1, 'Mgmt', 'rear'), PSU(1)],
   '1U autoloader, one half-height LTO SAS drive, 9-slot magazine. Check: SAS connector and part number.',
   'IBM TS2900 product page', 'https://www.ibm.com/products/ts2900-tape-autoloader', verified=False, full=True)
SX = ('Legacy IBM System x server (the x86 server line moved to Lenovo in 2014; later units are Lenovo System x). '
      'Check: rear ports from the M5 family (VGA, serial, 2 x USB 3.0, IMM2 port, 4 x 1GbE, PCIe). ')
IB('x3550-m5', 'System x3550 M5 (8869)', 'System x3550 M5 1U server (legacy)', 'System x', 'computer', 1,
   [F('io', 'USB', 'USB-A', 2, 'USB'), VGA(), R('io', 'Other', 'DB9', 1, 'Serial'), USBA(2, 'USB 3.0'), RJ(1, 'IMM2', 'rear'),
    RJ(4, '1GbE', 'rear'), SLOT(3, 'PCIe slot'), PSU(2)], SX + CARDS, 'Lenovo Press x3550 M5 product guide',
   'https://lenovopress.lenovo.com/', verified=False, full=True)
IB('x3650-m5', 'System x3650 M5 (8871)', 'System x3650 M5 2U server (legacy)', 'System x', 'computer', 2,
   [F('io', 'USB', 'USB-A', 2, 'USB'), VGA(), R('io', 'Other', 'DB9', 1, 'Serial'), USBA(2, 'USB 3.0'), RJ(1, 'IMM2', 'rear'),
    RJ(4, '1GbE', 'rear'), SLOT(8, 'PCIe slot'), PSU(2)], SX + CARDS, 'Lenovo Press x3650 M5 product guide',
   'https://lenovopress.lenovo.com/', verified=False, full=True)

# =====================================================================================================================
# Oracle
# =====================================================================================================================
OR = lambda *a, **k: add('oracle.json', 'oracle-', 'Oracle', *a, **k)
OR('server-x9-2', 'Oracle Server X9-2', 'Server X9-2 1U two-socket server', 'Oracle x86 servers', 'computer', 1,
   [RJ(1, 'NET MGT (ILOM)', 'rear'), RJ(1, 'NET 0 1GbE', 'rear'), R('io', 'Other', 'RJ45', 1, 'SER MGT'), USBA(1, 'USB 3.0'),
    SLOT(1, 'OCP 3.0 NIC (2 x QSFP)'), SLOT(3, 'PCIe slot'), PSU(2)],
   '1U Intel Xeon (3rd gen) server, 4 NVMe bays. PCIe slot 1 works only with two CPUs. Optional OCP 3.0 NIC with two QSFP ports '
   '(10-200 Gb). Two hot-plug 1200 W (or 1400 W) PSUs. No VGA on the back panel. Also the base of Oracle Database Appliance '
   'X9-2S/L and Exadata X9M database servers. Check: PSU inlet.', 'Oracle Server X9-2 Service Manual (back panel components)',
   'https://docs.oracle.com/en/servers/x86/x9-2/service-manual/oracle-server-x9-2.html', full=True)
OR('server-x9-2l', 'Oracle Server X9-2L', 'Server X9-2L 2U two-socket server', 'Oracle x86 servers', 'computer', 2,
   [RJ(1, 'NET MGT (ILOM)', 'rear'), RJ(1, 'NET 0 1GbE', 'rear'), R('io', 'Other', 'RJ45', 1, 'SER MGT'), USBA(1, 'USB 3.0'),
    SLOT(10, 'PCIe slot'), PSU(2)],
   '2U Intel Xeon (3rd gen) server, 12 x 3.5 in bays. 10 PCIe slots (slots 1-5 need the second CPU). Two hot-plug PSUs. No VGA on '
   'the back panel. Check: PSU rating and inlet.', 'Oracle Server X9-2L Service Manual (back panel components)',
   'https://docs.oracle.com/en/servers/x86/x9-2l/service-manual/oracle-server-x9-2l.html', full=True)
SP = 'Check: ports from the SPARC T8/S7 family pattern (NET 0-3 10GBASE-T, NET MGT, SER MGT, VGA, USB). '
for mid, pn, ru, nm, pcie in [('sparc-t8-1', 'SPARC T8-1', 2, 'one-socket SPARC M8', 6), ('sparc-t8-2', 'SPARC T8-2', 3, 'two-socket SPARC M8', 8),
                              ('sparc-s7-2', 'SPARC S7-2', 1, 'two-socket SPARC S7', 3), ('sparc-s7-2l', 'SPARC S7-2L', 2, 'two-socket SPARC S7', 6)]:
    OR(mid, pn, f'{pn} {ru}U {nm} server', 'SPARC servers', 'computer', ru,
       [RJ(4, '10GBASE-T NET 0-3', 'rear'), RJ(1, 'NET MGT (ILOM)', 'rear'), R('io', 'Other', 'RJ45', 1, 'SER MGT'), VGA(),
        USBA(2, 'USB'), SLOT(pcie, 'PCIe slot'), PSU(2)], f'{ru}U Oracle Solaris server. ' + SP + CARDS,
       f'Oracle {pn} documentation', 'https://docs.oracle.com/en/servers/sparc/', verified=False, full=True)
OR('sl150-base', 'SL150 Base Module', 'StorageTek SL150 tape library base module (3U, 30 slots)', 'StorageTek tape', 'computer', 3,
   [SLOT(2, 'LTO drive bay (SAS or FC)'), RJ(1, 'Mgmt', 'rear'), USBA(9, 'Expansion module link', 'rear'), PSU(2)],
   '3U base module, always at the top of the library: two 15-slot magazines, a 4-slot mailslot (19 with the expanded mailslot), '
   'one LTO drive with room for a second, one PSU with an optional second (change the count to 1 if only one fitted). Expansion '
   'modules hang below on the USB links. Add each drive\'s SAS or FC port as an extra port. A common archive library behind '
   'broadcast MAM systems.', 'Oracle StorageTek SL150 Library Guide (Base Module)',
   'https://docs.oracle.com/en/storage/tape-storage/storagetek-sl150-modular-tape-library/slofs/base-module1.html', full=True)
OR('sl150-exp', 'SL150 Expansion Module', 'StorageTek SL150 tape library expansion module (2U, 30 slots)', 'StorageTek tape',
   'computer', 2, [SLOT(2, 'LTO drive bay (SAS or FC)'), R('io', 'USB', 'USB-A', 1, 'Link to base module')],
   '2U module below the base module: two 15-slot magazines and room for two drives; up to 9 per library (300 slots, 20 drives). '
   'Check: module height (2U) and link cable.', 'Oracle StorageTek SL150 Library Guide',
   'https://docs.oracle.com/en/storage/tape-storage/storagetek-sl150-modular-tape-library/slofs/sl150-library.html',
   verified=False, full=True)

# =====================================================================================================================
# F5
# =====================================================================================================================
F5 = lambda *a, **k: add('f5.json', 'f5-', 'F5', *a, **k)
F5_FRONT = 'Network ports, management port, console and USB on the front (LCD panel too); PSUs on the rear. '
ISER = {'i2': ('platform-guide-i2000i4000-series', 'BIG-IP iSeries Platform Guide: i2000/i4000'),
        'i5': ('platform-guide-i5000i7000i10000i11000-series', 'BIG-IP iSeries Platform Guide: i5000-i11000'),
        'i15': ('platform-guide-i15000-series', 'BIG-IP iSeries Platform Guide: i15000')}
def iseries(models, ports, ru, psus, guide, note, **kw):
    path, title = ISER[guide]
    for m in models:
        F5(m.lower(), f'BIG-IP {m}', f'BIG-IP {m} application delivery controller', 'BIG-IP iSeries', 'network', ru,
           ports + [RJ(1, 'Mgmt'), CONS(), USBA(1, 'USB', 'front'), PSU(psus)], F5_FRONT + note, title,
           f'https://techdocs.f5.com/en-us/hw-platforms/{path}/title--platform-specifications.html', **kw)
iseries(['i2600', 'i2800'], [CAGE(4, 'SFP', '1G SFP'), CAGE(2, 'SFP+', '10G SFP+')], 1, 1, 'i2',
        '1 x 250 W AC PSU (second optional, or 650 W DC), 572 mm deep, 9.1 kg, 120 W max.', powerW=120, weightKg=9.1)
iseries(['i4600', 'i4800'], [CAGE(8, 'SFP', '1G SFP'), CAGE(4, 'SFP+', '10G SFP+')], 1, 1, 'i2',
        '1 x 250 W AC PSU (second optional, or 650 W DC), 572 mm deep, 9.1 kg, 165 W max.', powerW=165, weightKg=9.1)
iseries(['i5600', 'i5800', 'i5820-DF'], [CAGE(8, 'SFP+', '10G SFP+'), CAGE(4, 'QSFP+', '40G QSFP+')], 1, 1, 'i5',
        '1 x 650 W AC PSU (second optional), 777 mm deep, 11.1 kg, 330-420 W max. -DF is the FIPS (HSM) model.', powerW=420,
        weightKg=11.1, full=True)
iseries(['i7600', 'i7800', 'i7820-DF'], [CAGE(8, 'SFP+', '10G SFP+'), CAGE(4, 'QSFP+', '40G QSFP+')], 1, 2, 'i5',
        '2 x 650 W AC PSUs, 777 mm deep, 13.6 kg, 390-470 W max. -DF is the FIPS (HSM) model.', powerW=470, weightKg=13.6, full=True)
iseries(['i10600', 'i10800'], [CAGE(8, 'SFP+', '10G SFP+'), CAGE(6, 'QSFP+', '40G QSFP+')], 1, 2, 'i5',
        '2 x 650 W AC PSUs, 777 mm deep, 16.3 kg, 525 W max.', powerW=525, weightKg=16.3, full=True)
iseries(['i11600', 'i11800'], [CAGE(8, 'SFP+', '10G SFP+'), CAGE(6, 'QSFP+', '40G QSFP+')], 1, 2, 'i5',
        '2 x 650 W AC PSUs, 777 mm deep, 16.3 kg, 570 W max.', powerW=570, weightKg=16.3, full=True)
iseries(['i15600', 'i15800', 'i15820-DF'], [CAGE(8, 'QSFP+', '40G QSFP+'), CAGE(4, 'QSFP28', '100G QSFP28')], 2, 2, 'i15',
        '2 x 1500 W AC or DC PSUs, 767 mm deep, 34.5 kg, 1110 W max. The management port is 10GbE. -DF is the FIPS (HSM) model.',
        powerW=1110, weightKg=34.5, full=True)
RS = ('F5 rSeries data sheet', 'https://www.f5.com/products/big-ip-services/rseries-adc-hardware-appliance')
RNOTE = (F5_FRONT + 'Runs F5OS-A with BIG-IP tenants. Check: panel positions of management, console and USB (the data sheet does '
         'not say). ')
for models, ports, psu, note, kw in [
        (['r2600', 'r2800'], [RJ(4, '1/10GBASE-T'), CAGE(4, 'SFP28', '1/10/25G')], 1, '1 x 250 W PSU (second optional), 429 mm deep, '
         '9.1 kg, 85 W typical.', dict(weightKg=9.1)),
        (['r4600', 'r4800'], [RJ(4, '1/10GBASE-T'), CAGE(4, 'SFP28', '1/10/25G')], 1, '1 x 250 W PSU (second optional), 429 mm deep, '
         '9.1 kg, 105 W typical.', dict(weightKg=9.1)),
        (['r5600', 'r5800', 'r5900'], [CAGE(8, 'SFP28', '10/25G'), CAGE(2, 'QSFP28', '40/100G')], 1, '1 x 650 W PSU (second '
         'optional), 777 mm deep, 16.3 kg, 425 W typical.', dict(weightKg=16.3, full=True)),
        (['r10600', 'r10800', 'r10900'], [CAGE(16, 'SFP28', '10/25G'), CAGE(4, 'QSFP28', '40/100G')], 2, '2 x 1200 W AC or DC PSUs, '
         '777 mm deep, 16.3 kg, 680 W typical. Check: height (the data sheet says 1U).', dict(weightKg=16.3, full=True)),
        (['r12600-DS', 'r12800-DS', 'r12900-DS'], [CAGE(16, 'SFP28', '10/25G'), CAGE(4, 'QSFP28', '40/100G')], 2, '2 x 1224 W AC, DC '
         'or HVDC PSUs, 777 mm deep, 19 kg, 855 W typical. -DS models carry the hardware security module.', dict(weightKg=19, full=True))]:
    for m in models:
        F5(m.lower(), f'rSeries {m}', f'rSeries {m} application delivery appliance', 'rSeries', 'network', 1,
           ports + [RJ(1, 'Mgmt'), CONS(), USBA(1, 'USB 3.0', 'front'), PSU(psu)], RNOTE + note, *RS, **kw)
VEL = 'F5 VELOS'
F5('velos-cx410', 'VELOS CX410', 'VELOS CX410 4U chassis, 8 blade slots', 'VELOS', 'frame', 4,
   [F('io', 'Ethernet', 'RJ45', 2, 'SX410 controller Mgmt'), F('io', 'Other', 'RJ45', 2, 'SX410 controller Console'),
    PSU(4, label='PSU (2 standard, up to 4)')],
   '4U chassis with eight quarter-width BX110 blade slots and two SX410 system controllers (fitted as standard; console and '
   'out-of-band management are on the controllers). 2 PSUs standard, up to 4 (AC or DC); front-to-back airflow, one fan tray. '
   'Change the PSU count to the number fitted. Check: controller port types and blade slot layout on the drawing.',
   'F5 VELOS training guide (components)', 'https://www.f5.com/products/big-ip-services/velos-hardware-chassis-and-blades',
   verified=False, full=True,
   frame=dict(system=VEL, slots=8, slotOrder='ltr', orient='h', cols=4, rearAlign=1, door=False,
              controller='Two SX410 system controllers (fixed, not slots)',
              front=dict(x0=0.04, x1=0.96, y0=0.04, y1=0.70), rear=dict(x0=0.04, x1=0.96, y0=0.04, y1=0.96)))
F5('velos-bx110', 'VELOS BX110', 'VELOS BX110 blade, 2 x 100G QSFP28', 'VELOS', 'card', 0,
   [CAGE(2, 'QSFP28', '40/100G (or 4 x 10/25G breakout)')],
   'Quarter-width blade for the CX410 / CX1610. Each port runs at 40G or 100G, or 4 x 25G / 4 x 10G with breakout cables. No '
   'management ports on the blade.', 'F5 VELOS training guide (components)',
   'https://www.f5.com/products/big-ip-services/velos-hardware-chassis-and-blades', w=0,
   card=dict(fits=[VEL], slotWidth=1), rearModules=NOREAR)

# =====================================================================================================================
# VMware: software only; its hardware is the VMware SD-WAN (VeloCloud) Edge range, now Arista VeloCloud
# =====================================================================================================================
VM = lambda *a, **k: add('vmware.json', 'vmware-', 'VMware SD-WAN (VeloCloud)', *a, **k)
VMN = ('VMware SD-WAN by VeloCloud edge appliance. VMware (now part of Broadcom) sells vSphere, vSAN and NSX as software on '
       'other makers\' servers; the SD-WAN edges are its only hardware, and the VeloCloud business moved to Arista in 2025. ')
VDS = ('VMware SD-WAN by VeloCloud Edge data sheet', 'https://www.arista.com/en/products/velocloud-sd-wan')
VM('edge-840', 'Edge 840', 'SD-WAN Edge 840, 1U', 'VMware SD-WAN Edge (VeloCloud)', 'network', 1,
   [RJ(6, '1G LAN/WAN'), CAGE(2, 'SFP+', '1/10G'), CONS(), USBA(2, 'USB 3.0', 'front'), PSU(1)],
   VMN + '40 W typical / 70 W max, single PSU. Check: panel positions, console (RJ45, VGA also listed) and size.', *VDS,
   verified=False, powerW=70)
VM('edge-2000', 'Edge 2000', 'SD-WAN Edge 2000, 1U', 'VMware SD-WAN Edge (VeloCloud)', 'network', 1,
   [RJ(6, '1G LAN/WAN'), CAGE(2, 'SFP+', '1/10G'), CONS(), USBA(4, 'USB', 'front'), PSU(2)],
   VMN + '150 W typical / 200 W max, redundant 1+1 PSUs. Check: panel positions and size.', *VDS, verified=False, powerW=200)
for pn, typ in [('3400', 165), ('3800', 200), ('3810', 200)]:
    VM(f'edge-{pn}', f'Edge {pn}', f'SD-WAN Edge {pn}, 1U', 'VMware SD-WAN Edge (VeloCloud)', 'network', 1,
       [RJ(6, '1G LAN/WAN'), CAGE(4, 'SFP+', '1/10G'), CONS(), USBA(2, 'USB 3.0', 'front'), PSU(2)],
       VMN + f'{typ} W typical / 400 W max, redundant 1+1 internal PSUs, about 434 x 381 x 44 mm. Also sold by Dell as the SD-WAN '
       'Edge 3000 series. ' + ('Check: the 3810 port mix (taken from the 3800). ' if pn == '3810' else '') +
       'Check: panel positions.', *VDS, verified=False, powerW=400)
VM('edge-4100', 'Edge 4100', 'VeloCloud SD-WAN Edge 4100, 1U', 'VMware SD-WAN Edge (VeloCloud)', 'network', 1,
   [RJ(8, '1G LAN/WAN'), CAGE(8, 'SFP+', '1/10G'), RJ(2, '1G Mgmt'), CONS(), RJ(1, 'IPMI'), USBA(2, 'USB 3.0', 'front'), PSU(2)],
   VMN + 'Current model (Arista VeloCloud). 438 x 420 x 44 mm, 7.7 kg, 195 W typical / 270 W max, redundant 1+1 internal AC PSUs.',
   'Arista VeloCloud SD-WAN Edge 4100/5100 data sheet and quick start guide',
   'https://www.arista.com/en/products/velocloud-4100-5100-series', powerW=270)
VM('edge-5100', 'Edge 5100', 'VeloCloud SD-WAN Edge 5100, 1U', 'VMware SD-WAN Edge (VeloCloud)', 'network', 1,
   [CAGE(8, 'SFP+', '1/10G'), CAGE(4, 'SFP28', '25G'), CAGE(2, 'QSFP+', '40G'), RJ(2, '1G Mgmt'), CONS(), RJ(1, 'IPMI'),
    USBA(2, 'USB 3.0', 'front'), PSU(2)],
   VMN + 'Current model (Arista VeloCloud). 11.8 kg, 300 W typical / 500 W max, redundant 1+1 internal AC PSUs, about 600 mm deep.',
   'Arista VeloCloud SD-WAN Edge 4100/5100 data sheet and quick start guide',
   'https://www.arista.com/en/products/velocloud-4100-5100-series', powerW=500, full=True)

# =====================================================================================================================
ids = set()
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
