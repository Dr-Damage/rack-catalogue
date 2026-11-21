#!/usr/bin/env python3
"""Added 2026-11-21:
  catalogue/dell-nx.json    Dell PowerVault NX / Dell Storage NX Windows Storage Server NAS appliances (NX400 to NX3340).
                            tools/it.py keeps writing dell.json (PowerEdge servers, Precision racks, tape) and is untouched.
  catalogue/hp-z.json       HP Z440 / Z640 / Z840 rackable towers, a Z840 fitted with a Blackmagic DeckLink Quad 2 (8 SDI
                            in/outs), and the Z6 G4, Z6 G5 / G5 A and Z8 G5 towers that hp.json (tools/enterprise_it.py) lacks.
  catalogue/sprolink.json   Sprolink SG-UHD 4K test signal generator and Sprolink's rack-mount gear.
Specs come from each maker's owner's manuals, support matrices, QuickSpecs and data sheets (each entry's source). Anything the
source did not give is marked 'Check:' and the entry has verified False. NX appliances are PowerEdge servers underneath; where Dell
names the platform, the rear panel follows that PowerEdge's rear panel. Card slots are drawn as card slots: add the ports of the
cards fitted (SAS HBA / PERC H840 to MD-series shelves, 10/25GbE NICs) as extra ports."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, id, mfr, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat, ru=ru, widthCols=w, fullDepth=full,
             verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m)
def RJ(n, label, face='rear'): return g(face, 'io', 'Ethernet', 'RJ45', n, label)
def SLOT(n, label='PCIe slot', face='rear'): return g(face, 'io', 'Other', 'Card slot', n, label)
def USBA(n, label, face='rear'): return g(face, 'io', 'USB', 'USB-A', n, label)
def VGA(face='rear'): return g(face, 'out', 'Other', 'VGA', 1, 'VGA')
def SERIAL(): return R('io', 'RS-232', 'DB9', 1, 'Serial')
def PSU(n=2, conn='IEC C14'): return R('in', 'Power', conn, n, 'PSU' if n > 1 else 'AC In')

# =====================================================================================================================
# Dell PowerVault NX (Windows Storage Server NAS)
# =====================================================================================================================
D = lambda id, *a, **k: add('dell-nx.json', 'dell-' + id, 'Dell', *a, **k)
URL = 'https://www.dell.com/en-au/shop/ipovw/powervault-nx'
MX = 'Dell PowerVault NX Series Product Support Matrix (Rev A10)'
CARDS = ('Card slots: add the ports of the cards fitted (PERC H840 or SAS HBA to MD1200/MD1400 shelves, 10/25GbE NICs, tape '
         'HBA) as extra ports. ')
F14 = [VGA('front'), USBA(1, 'USB 2.0', 'front'), F('io', 'USB', 'Micro-USB', 1, 'iDRAC Direct')]
F13 = [VGA('front'), USBA(1, 'USB 2.0', 'front'), USBA(1, 'USB management (iDRAC Direct)', 'front')]
def nx_rear(nic, nic_label, pcie, psu=2, usb=2, usb_label='USB 3.0', idrac=True):
    p = [VGA(), SERIAL(), USBA(usb, usb_label)]
    if idrac: p.append(RJ(1, 'iDRAC'))
    p += [RJ(nic, nic_label), SLOT(pcie), PSU(psu)]
    return p

D('nx3240', 'NX3240', 'PowerVault NX3240 2U NAS, 12 x 3.5 in (Windows Storage Server 2016)', 'PowerVault NX (14G)', 'computer', 2,
  F14 + nx_rear(4, '1GbE NDC (Broadcom 5720 QP)', 3),
  'Windows Storage Server 2016 Standard NAS on the PowerEdge R740xd. 12 x 3.5 in hot-swap front bays for data, 4 x 3.5 in '
  'mid-bay (not set up at the factory) and 2 rear hot-swap bays for the OS. Broadcom 5720 quad 1GbE daughter card standard '
  '(25GbE SFP28 or 10GbE SFP+ cards optional), iDRAC9 Enterprise, up to three PCIe 3.0 x8 slots. One 750 W hot-plug PSU '
  'standard; a second 750 W or 1100 W makes it 1+1 redundant (change the PSU count to 1 if only one fitted). ' + CARDS,
  MX, URL, full=True)
D('nx3340', 'NX3340', 'PowerVault NX3340 1U NAS gateway, 8 x 2.5 in (Windows Storage Server 2016)', 'PowerVault NX (14G)',
  'computer', 1, F14 + nx_rear(4, '1GbE NDC (Broadcom 5720 QP)', 3),
  'Windows Storage Server 2016 Standard NAS head on the PowerEdge R640: 8 x 2.5 in hot-swap bays (2 or 4 for the OS, the rest '
  'free). Serves storage on PowerVault ME/MD, Compellent or EqualLogic arrays, or clusters. Quad 1GbE daughter card standard, '
  'iDRAC9 Enterprise, three PCIe 3.0 x16 slots (put SAS HBAs in slots 1 and 3). One 750 W hot-plug PSU standard, second '
  'optional (1+1). ' + CARDS, MX, URL, full=True)
D('nx440', 'NX440', 'PowerVault NX440 1U NAS, 4 x 3.5 in (Windows Storage Server 2016)', 'PowerVault NX (14G)', 'computer', 1,
  [USBA(1, 'USB 2.0', 'front'), F('io', 'USB', 'Micro-USB', 1, 'iDRAC Direct')] + nx_rear(2, '1GbE LOM', 2),
  'Entry Windows Storage Server 2016 Standard or Workgroup NAS on the PowerEdge R340: 4 x 3.5 in hot-swap SAS/SATA bays, 482 x '
  '42.8 x 534.5 mm deep, up to 13.2 kg. Two 1GbE ports and a dedicated iDRAC9 port on the back, two PCIe 3.0 slots (x8 low '
  'profile, x16). One 350 W hot-plug PSU standard, a second makes it redundant. ' + CARDS,
  'Dell Storage NX440 owner\'s manual and ' + MX, URL, weightKg=13.2)
D('nx430', 'NX430', 'PowerVault NX430 1U NAS, 4 x 3.5 in (Windows Storage Server 2016)', 'PowerVault NX (13G)', 'computer', 1,
  [USBA(1, 'USB 2.0', 'front')] + nx_rear(2, '1GbE LOM', 2),
  'Windows Storage Server 2016 Standard or Workgroup NAS on the PowerEdge R330 (2016-2019, replaced by the NX440): 4 x 3.5 in '
  'hot-swap bays, two PCIe 3.0 slots (x8, x16). Hot-plug 350 W PSU, second optional. The matrix lists a Broadcom 5720 quad 1GbE '
  'NIC as standard. Check: rear panel taken from the R330 (2 x 1GbE, iDRAC, VGA, serial, 2 x USB 3.0); if the quad NIC card is '
  'fitted, add 4 more 1GbE ports. ' + CARDS,
  'Dell Storage NX430 support matrix', URL, verified=False)
D('nx3230', 'NX3230', 'Storage NX3230 2U NAS, 12 x 3.5 in + 2 rear 2.5 in (Windows Storage Server 2012 R2 / 2016)',
  'PowerVault NX (13G)', 'computer', 2, F13 + nx_rear(4, 'NDC NIC', 6),
  'Windows Storage Server NAS (2014-2018, replaced by the NX3240): 12 x 3.5 in hot-swap data bays plus 2 x 2.5 in rear OS bays, '
  'up to two Xeon E5-2600 v3. 87.3 x 482 x 755.8 mm, up to 36.5 kg. Network daughter card: 4 x 1GbE, 2 x 1GbE + 2 x 10GBASE-T '
  '(QLogic 57800, a common build) or 4 x 10GbE. 750 W or 1100 W PSUs. Check: the dedicated iDRAC8 port (the PowerEdge R730xd it '
  'matches has one), the PCIe slot count (6 drawn) and the PSU count (redundant pair drawn). ' + CARDS,
  'Dell Storage NX3230 owner\'s manual (technical specifications) and Icecat listing',
  'https://www.dell.com/support/manuals/en-us/storage-nx3230/nx3230ompub/about-your-system', verified=False, full=True,
  weightKg=36.5)
D('nx3330', 'NX3330', 'Storage NX3330 1U NAS gateway (Windows Storage Server 2012 R2 / 2016)', 'PowerVault NX (13G)', 'computer', 1,
  F13 + nx_rear(4, 'NDC NIC', 3),
  'Windows Storage Server NAS head (2014-2018, replaced by the NX3340): 2 or 4 x 2.5 in OS drives only; serves storage on '
  'PowerVault MD3, EqualLogic or Compellent arrays. Two Xeon E5-2600 v3, iDRAC8 Enterprise, three low-profile PCIe 3.0 slots '
  '(two x16, one x8), 750 W hot-plug PSUs (redundant or single). 42.8 x 482.3 x 700.5 mm, up to 16.9 kg. Check: NDC port mix '
  '(customer selectable; 4 x 1GbE drawn). ' + CARDS, 'Dell Storage NX3330 spec sheet',
  'https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/SS_Dell_Storage_NX3330_121114.pdf',
  verified=False, full=True, weightKg=16.9)
D('nx3200', 'NX3200', 'PowerVault NX3200 2U NAS, 12 x 3.5 in (Windows Storage Server 2012)', 'PowerVault NX (12G)', 'computer', 2,
  [VGA('front'), USBA(2, 'USB 2.0', 'front')] + nx_rear(4, '1GbE NDC', 6, usb_label='USB 2.0'),
  'Windows Storage Server 2012 / 2012 R2 NAS on the PowerEdge R720xd (2012-2014): 12 x 3.5 in hot-swap data bays (up to 48 TB) '
  'plus 2 x 2.5 in OS drives, iDRAC7 Enterprise, six PCIe slots (two x16 and one x8 full height, three x8 half height). 495 W, '
  '750 W or 1100 W hot-plug PSUs. 87.3 x 482 x 755.8 mm, up to 32.5 kg. Add a PERC card for MD1200 shelves. Check: NDC port mix '
  '(4 x 1GbE drawn) and front USB count. ' + CARDS, 'Dell PowerVault NX3200 spec sheet',
  'https://i.dell.com/sites/doccontent/shared-content/data-sheets/en/Documents/ESG-PowerVault-NX3200-Spec-Sheet.pdf',
  verified=False, full=True, weightKg=32.5)
D('nx3300', 'NX3300', 'PowerVault NX3300 1U NAS gateway (Windows Storage Server 2012)', 'PowerVault NX (12G)', 'computer', 1,
  [VGA('front'), USBA(2, 'USB 2.0', 'front')] + nx_rear(4, '1GbE NDC', 3, usb_label='USB 2.0'),
  'Windows Storage Server 2012 / 2012 R2 NAS head on the PowerEdge R620 (2012-2014): 2 or 4 x 2.5 in OS drives, no data bays; '
  'gateway to Compellent, EqualLogic or PowerVault MD3 arrays, clusters up to 8 nodes. Two Xeon E5-2600. Check: rear panel taken '
  'from the R620 (4-port NDC, iDRAC7, 3 PCIe, 2 PSUs). ' + CARDS, 'Microsoft Storage Server team blog (Dell NX on WSS 2012 R2)',
  'https://learn.microsoft.com/en-us/archive/blogs/storageserver/dell-powervault-nx-now-available-with-windows-storage-server-2012-r2',
  verified=False, full=True)
D('nx400', 'NX400', 'PowerVault NX400 1U NAS, 4 x 3.5 in (Windows Storage Server 2012 R2)', 'PowerVault NX (12G)', 'computer', 1,
  [VGA('front'), USBA(2, 'USB 2.0', 'front')] + nx_rear(2, '1GbE LOM', 2, usb_label='USB 2.0'),
  'Entry Windows Storage Server NAS on the PowerEdge R320 (2012-2016): up to 4 x 3.5 in hot-swap NL-SAS/SATA drives (16 TB), one '
  'Xeon E5-2400, redundant 550 W PSUs. MD1200 / MD1220 shelves for more space. Check: rear panel taken from the R320 (2 x 1GbE, '
  'iDRAC7 port with the Enterprise licence, 2 PCIe slots). ' + CARDS, 'Dell PowerVault NX400 product page',
  'https://www.dell.com/en-au/shop/ipovw/powervault-nx400', verified=False)

# =====================================================================================================================
# HP Z workstations (towers on rack rails). hp.json (tools/enterprise_it.py) has the Z4 Rack G5, ZCentral 4R, Z4 G4/G5,
# Z8 G4, Z8 Fury G5 and Z2 Mini G9; these fill the rest of the family.
# =====================================================================================================================
H = lambda id, *a, **k: add('hp-z.json', 'hp-' + id, 'HP', *a, **k)
GPU = lambda n=4: R('out', 'DisplayPort', 'DisplayPort', n, 'GPU outputs')
AUD = lambda: [R('in', 'Analog audio', '3.5mm jack', 1, 'Line in'), R('out', 'Analog audio', '3.5mm jack', 1, 'Line out')]
PS2 = lambda: R('in', 'Other', 'Mini-DIN 6', 2, 'PS/2 keyboard / mouse')
FRONT_G2 = [USBA(4, 'USB 3.0', 'front'), F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'),
            F('in', 'Analog audio', '3.5mm jack', 1, 'Microphone')]
GPU_NOTE = 'GPU DisplayPort count depends on the card fitted (4 drawn, as a Quadro/RTX card). '
CORD = 'Check: PSU inlet (IEC C14 drawn). '

def z840_ports(slots=7):
    return FRONT_G2 + [USBA(4, 'USB 3.0'), USBA(2, 'USB 2.0'), SERIAL(), PS2(), RJ(2, '1GbE (Intel I218LM / I210AT)')] + AUD() + \
        [SLOT(slots), GPU(), PSU(1)]
Z840_SRC = ('HP Z840 Workstation QuickSpecs (v34)',
            'https://pcserverandparts.com/content/Spec%20Sheets/Workstations/HP/HP%20Z840/HP%20Z840%20Workstation%20QuickSpecs.pdf')
Z840_TXT = ('Dual-socket Xeon E5-2600 v3/v4 tower (2014-2018), rackable: 5U on the HP Z6/8 Adjustable Rail Rack Kit, Flush Mount '
            '(B8S55AA) or the Z640/Z840/Z8 G4 Rail Rack Kit (2FZ77AA). 444.5 x 203.2 x 525.8 mm (H x W x D), 22.8 kg typical. '
            '850 W or 1125 W PSU (the 1125 W gives 1450 W on 200-240 V). 7 slots: 1 Gen3 x4, 2 Gen3 x16, 3 Gen3 x8 (2nd CPU), '
            '4 Gen3 x16 (2nd CPU), 5 Gen2 x4 (Gen3 x8 with the 2nd CPU), 6 Gen3 x16, 7 Gen2 x1. ')
H('z840', 'Z840', 'Z840 tower workstation on rack rails (5U, legacy)', 'Z by HP tower (G2)', 'computer', 5, z840_ports(),
  Z840_TXT + 'A common host for broadcast graphics, playout and capture (DeckLink, AJA KONA) cards: add the card ports as extra '
  'ports, or use the "with DeckLink Quad 2" entry. ' + GPU_NOTE + CORD, *Z840_SRC, full=True, weightKg=22.8)
H('z840-decklink-quad2', 'Z840 + DeckLink Quad 2', 'Z840 workstation with Blackmagic DeckLink Quad 2 (8 x 3G-SDI in/out), 5U',
  'Z by HP tower (G2)', 'computer', 5,
  z840_ports(6) + [R('io', '3G-SDI', 'DIN 1.0/2.3', 8, 'DeckLink SDI'), R('in', 'Reference', 'DIN 1.0/2.3', 1, 'DeckLink Ref In')],
  'HP Z840 fitted with a Blackmagic DeckLink Quad 2 (BDLKDVQD2): 8 SD/HD/3G-SDI channels on DIN 1.0/2.3 connectors, each set '
  'as an input or an output in Blackmagic Desktop Video Setup (wire each one either way; pairs can run key and fill), 16 '
  'channels of embedded audio per channel, tri-level or black burst sync input, PCIe Gen2 x8, 22 W. The card comes with no '
  'cables: use DIN 1.0/2.3 to BNC leads (set the cable connector to DIN 1.0/2.3 at the card end). Fit it in slot 2 or 6 (x16) '
  'on a single-CPU machine; one card slot is used, 6 left. ' + Z840_TXT + GPU_NOTE + CORD +
  'Check: the reference input connector on the card bracket.',
  'HP Z840 QuickSpecs and Blackmagic DeckLink Quad 2 tech specs',
  'https://www.bhphotovideo.com/c/product/1186263-REG/blackmagic_design_bdlkdvqd2_decklink_quad_2_8_channel.html/specs', full=True, weightKg=22.8)
H('z640', 'Z640', 'Z640 tower workstation on rack rails (4U, legacy)', 'Z by HP tower (G2)', 'computer', 4,
  FRONT_G2 + [USBA(4, 'USB 3.0'), USBA(2, 'USB 2.0'), PS2(), RJ(1, '1GbE (Intel I218LM)')] + AUD() + [SLOT(6, 'PCIe / PCI slot'), GPU(), PSU(1)],
  'Xeon E5-1600/2600 v3/v4 tower (2014-2018, second CPU on a riser), rackable minitower: 4U on the HP Z6/8 Adjustable Rail Rack '
  'Kit, Flush Mount (B8S55AA). 442.9 x 171.5 x 464.8 mm (H x W x D), 17 kg typical. 925 W PSU. 6 slots: 1 Gen2 x1 (lost with '
  'the 2nd CPU), 2 Gen3 x16, 3 Gen2 x4, 4 Gen3 x8, 5 Gen3 x16, 6 legacy PCI. A serial port is an optional PCI-bracket cable. '
  + GPU_NOTE + CORD, 'HP Z640 Workstation QuickSpecs (v17)',
  'https://pcserverandparts.com/content/Spec%20Sheets/Workstations/HP/HP%20Z640/HP%20Z640%20Workstation%20Quickspecs.pdf', full=True, weightKg=17)
H('z440', 'Z440', 'Z440 tower workstation on rack rails (4U, legacy)', 'Z by HP tower (G2)', 'computer', 4,
  FRONT_G2 + [USBA(4, 'USB 3.0'), USBA(2, 'USB 2.0'), PS2(), RJ(1, '1GbE (Intel I218LM)')] + AUD() + [SLOT(6, 'PCIe / PCI slot'), GPU(), PSU(1)],
  'Single-socket Xeon E5-1600/2600 v3/v4 tower (2014-2018) on the HP Z240/Z440 Depth Adjust Fixed Rail Rack Kit (WH340AA), 4U. '
  '431.8 x 168.9 x 444.7 mm (H x W x D), 13.5 kg typical. 525 W or 700 W PSU (700 W needed for graphics over 75 W, up to 225 W). '
  '6 slots: 1 Gen2 x1, 2 Gen3 x16, 3 Gen2 x4, 4 Gen3 x8, 5 Gen3 x16, 6 legacy PCI. A serial port is an optional PCI-bracket '
  'cable. ' + GPU_NOTE + CORD, 'HP Z440 Workstation QuickSpecs (v37)',
  'https://manualmachine.com/hp/z440/24305858-quickspecs', full=True, weightKg=13.5)

H('z820', 'Z820', 'Z820 tower workstation on rack rails (5U, legacy)', 'Z by HP tower (G1)', 'computer', 5,
  [USBA(2, 'USB 3.0', 'front'), USBA(1, 'USB 2.0', 'front'), F('io', 'Other', 'FireWire 400', 1, 'IEEE 1394a'),
   F('out', 'Analog audio', '3.5mm jack', 1, 'Headphone'), F('in', 'Analog audio', '3.5mm jack', 1, 'Microphone'),
   USBA(2, 'USB 3.0'), USBA(4, 'USB 2.0'), R('io', 'Other', 'FireWire 400', 1, 'IEEE 1394a'), SERIAL(), PS2(),
   RJ(2, '1GbE')] + AUD() + [R('in', 'Analog audio', '3.5mm jack', 1, 'Microphone'), SLOT(7, 'PCIe / PCI slot'), GPU(), PSU(1)],
  'Dual-socket Xeon E5-2600 tower (2012-2015), rackable minitower on the HP Z6/8 Adjustable Rail Rack Kit, Flush Mount (B8S55AA). '
  '444 x 203 x 525 mm (H x W x D, the same chassis as the Z840), 22.8 kg typical. 850 W or 1125 W PSU. 6 PCIe slots (three need '
  'the 2nd CPU) plus one legacy PCI slot. Long the standard host for Vizrt engines, playout and DeckLink capture. '
  + GPU_NOTE + CORD + 'Check: rack height (5U drawn, as the Z840; the QuickSpecs give no U figure).',
  'HP Z820 Workstation QuickSpecs (v48)',
  'https://pcserverandparts.com/content/Spec%20Sheets/Workstations/HP/HP%20Z820/HP%20Z820%20Workstation%20QuickSpecs.pdf',
  verified=False, full=True, weightKg=22.8)
H('z6-g4', 'Z6 G4', 'Z6 G4 tower workstation on rack rails (4U)', 'Z by HP tower (G4)', 'computer', 4,
  [USBA(4, 'USB 3.1 Gen 1', 'front'), F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'), USBA(6, 'USB 3.1 Gen 1'),
   RJ(2, '1GbE (1 with AMT)'), PS2()] + AUD() + [SLOT(6), GPU(), PSU(1)],
  'Xeon Scalable tower (2017-2023, second CPU on a riser), 4U on the HP Z4/Z6 Depth Adjustable Fixed Rail Rack Kit (2HW42AA) or '
  'the Z2/Z4/Z6 kit (2A8Y5AA). 445 x 169 x 465 mm (H x W x D), 13.6 kg standard. 1000 W PSU. 6 PCIe slots. The Premium front '
  'panel swaps two USB-A for two 10 Gb USB-C. Serial is optional. ' + GPU_NOTE + CORD,
  'HP Z6 G4 Workstation QuickSpecs (v51)',
  'https://pcserverandparts.com/content/Spec%20Sheets/Workstations/HP/HP%20Z6%20G4/HP%20Z6%20G4%20Workstation%20QuickSpecs.pdf',
  full=True, weightKg=13.6)
H('z8-g5', 'Z8 G5', 'Z8 G5 tower workstation on rack rails (5U)', 'Z by HP tower (G5)', 'computer', 5,
  [USBA(4, 'USB 5Gb', 'front'), F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'), USBA(6, 'USB 5Gb'),
   RJ(2, '1GbE (1 with AMT)')] + AUD() + [SLOT(7), GPU(), PSU(1, 'IEC C20')],
  'Dual Xeon Scalable (4th gen) tower, 5U on the HP Z640/Z840/Z8 G4 Rail Rack Kit (2FZ77AA) or the Z8 Rack Rail Upgrade Kit '
  '(2FZ76AA). 444.5 x 215.9 x 551.2 mm (H x W x D), 24.3 kg typical. 1125 W, 1450 W or 1700 W PSU. 7 PCIe slots (Gen3 to Gen5) '
  'plus 2 M.2 personality slots; optional 2 x 10GbE, internal serial and PS/2 kit. ' + GPU_NOTE +
  'Check: PSU inlet (IEC C20 drawn; HP says the 1700 W needs a C19/C20 cord, the smaller ones may take C13/C14).',
  'HP Z8 G5 Workstation QuickSpecs (v37)', 'https://cdn.iceshop.nl/objects/mmo_113710094_1787535595_1892_2552343.pdf',
  full=True, weightKg=24.3)

# =====================================================================================================================
# Sprolink (Shenzhen; store.sprolink.com). Most of the range is desktop streaming switchers with built-in screens and
# HDMI extenders; only the units below are rack-mount or sit on a rack shelf.
# =====================================================================================================================
S = lambda id, *a, **k: add('sprolink.json', 'sprolink-' + id, 'Sprolink', *a, **k)
S('sg-uhd', 'SG-UHD', 'SG-UHD 4K UHD HDMI 2.0 / 3G-SDI / fibre test signal generator', 'SG', 'other', 1,
  [R('out', '3G-SDI', 'BNC', 2, 'SDI Out'),
   R('out', 'SFP', 'SFP', 1, 'Fibre SDI Out (SFP)'), R('out', 'HDMI', 'HDMI', 1, 'HDMI 2.0 Out'),
   R('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'), R('in', 'Power', 'USB-C', 1, 'USB-C (5 V power / control)'),
   R('in', 'Power', 'DC barrel', 1, 'DC 12V In')],
  'Pocket test pattern and tone generator, 135.2 x 117.2 x 35.6 mm, 310 g, metal case, 4.3 in colour screen with buttons. '
  'Patterns (colour bars, grey bars, ramps, your own images), tone -60 to 0 dB, 20 Hz-20 kHz with 0/90/180/270 degree phase, '
  'LTC/VITC timecode, 16 ch embedded SDI audio and 8 ch HDMI audio. SDI: SD 525/625, HD 720p/1080i/p, 2K, 3G Level A/B up to '
  '1080p60; HDMI 2.0 up to 4096 x 2160 and VESA up to 240 Hz. Power 5 V over USB-C or 12 V DC. Sits on a rack shelf '
  '(4 columns drawn). Check: no genlock input is listed; the analogue audio jack and the 12 V DC socket are on one retailer\'s '
  'spec list only; SFP module type (SDI over fibre) is not stated.',
  'Adorama and AVLGEAR SG-UHD listings',
  'https://www.adorama.com/sprolink-sg-uhd-4k-ultra-hd-hdmi-3g-sdi-signal-generator/p/sprsguhd', verified=False, w=4,
  boxMm=dict(w=135, h=36), weightKg=0.31)
S('vd-8k-2u', 'VD-8K 2U', 'VD-8K 2U 8K video wall processor (HDMI 2.1 / DP in, 4 x HDMI 2.0 out)', 'VD', 'switcher', 2,
  [R('in', 'HDMI', 'HDMI', 2, 'HDMI 2.1 In'), R('in', 'DisplayPort', 'DisplayPort', 2, 'DP 1.4 In'),
   R('in', 'DisplayPort', 'DisplayPort', 1, 'DP 2.1 In'), R('in', 'USB', 'USB-C', 2, 'USB-C video In'),
   R('out', 'HDMI', 'HDMI', 4, 'HDMI 2.0 Out'), R('out', 'Analog audio', '3.5mm jack', 4, 'Audio Out'),
   R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 1, 'Genlock Loop'),
   R('io', 'RS-232', 'DB9', 2, 'RS-232'), RJ(1, 'LAN (control)'), PSU(2)],
  '2U video wall splicer / processor for LED and LCD walls: up to 8K input split over four 4K HDMI outputs, with genlock. '
  '485 x 325 x 90 mm, 150 W max. Check: RS-232 connector (DB9 drawn), the redundant PSU inlets (two IEC C14 drawn) and '
  'whether HDMI ins are 2.0 or 2.1 (the listing says both).',
  'Adorama and AVLGEAR VD-8K 2U listings', 'https://www.adorama.com/sprolink-vd-8k-2u-hdmi-2-0-video-wall-processor/p/sprvd8k2u',
  verified=False, powerW=150)
S('vf4-pro', 'VF4 PRO', 'VF4 PRO 4K60 multi-format seamless switcher / scaler', 'VF', 'switcher', 2,
  [R('in', 'HDMI', 'HDMI', 4, 'HDMI 2.0 In'), R('in', 'DisplayPort', 'DisplayPort', 2, 'DP 1.2 In'),
   R('in', '3G-SDI', 'BNC', 2, 'SDI In'), R('in', 'DVI', 'DVI-I', 2, 'DVI In'), R('out', 'HDMI', 'HDMI', 2, 'HDMI 2.0 Out'),
   R('in', 'Reference', 'BNC', 1, 'Genlock In'), R('out', 'Reference', 'BNC', 1, 'Genlock Out'), RJ(1, 'LAN'),
   R('io', 'RS-232', 'RJ45', 1, 'RS-232'), USBA(1, 'USB'), PSU(1)],
  '4K60 HDMI 2.0 presentation / LED processor with seamless switching and layers. 480 x 350 x 90 mm (2U high), 8.2 kg, AC '
  '100-264 V internal, 20 W max. An optional extra HDMI 2.0 loop out. Check: rack ears (2U size, rack-mount not stated), '
  'genlock connector type and the IEC inlet.', 'Sprolink VF4 PRO brochure (2021)',
  'https://cdn.shopify.com/s/files/1/0610/0418/5813/files/VF4PRO_Brochure_EN_V1.0_20210105.pdf', verified=False, powerW=20,
  weightKg=8.2)
for pn, outs in (('SD8', 8), ('SD6', 4)):
    S(pn.lower(), pn, f'{pn} video wall sending box, 4 x DVI in, {outs} x DVI out', 'SD', 'switcher', 2,
      [R('in', 'DVI', 'DVI-I', 4, 'DVI In'), R('out', 'DVI', 'DVI-I', outs, 'DVI Out'), PSU(1)],
      f'LED/LCD wall sending (distribution) box with built-in fan. 480 x 283 x 89 mm (2U high), 3.8 kg, AC 100-264 V internal, '
      f'50 W max. Check: rack ears (not stated), the DVI in/out split (read from the catalogue table) and any control port.',
      'Sprolink product catalogue (2020)', 'https://cdn.shopify.com/s/files/1/0610/0418/5813/files/SPROLINK_Catalog_2020_V1.0_EN_20220318_B.pdf',
      verified=False, powerW=50, weightKg=3.8)

# =====================================================================================================================
taken = set()
for f in os.listdir(CAT):
    if f.endswith('.json') and f not in FILES and f not in ('index.json', 'manifest.json'):
        try: d = json.load(open(os.path.join(CAT, f)))
        except Exception: continue
        if isinstance(d, list): taken |= {m.get('id') for m in d if isinstance(m, dict)}
for f, items in FILES.items():
    for m in items:
        assert m['id'] not in taken, m['id']; taken.add(m['id'])
        for gp in m['portGroups']: assert gp['count'] > 0, (m['id'], gp)
    json.dump(items, open(os.path.join(CAT, f), 'w'), indent=1, ensure_ascii=False)
    print(f, len(items))
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
