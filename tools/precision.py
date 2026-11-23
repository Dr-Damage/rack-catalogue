#!/usr/bin/env python3
"""Added 2026-11-24: catalogue/dell-precision.json, the Dell Precision desktop workstation family.
  Compact (3240, 3260, 3280), small form factor (3450, 3460), 36xx towers (3630 to 3680), 5000/7000 towers (5820, 7820, 7920,
  5860, 7865, 7875, 7960) and the 3930 Rack and 7920 Rack (moved here from tools/it.py, which keeps the 7960 Rack in dell.json).
Ports come from Dell spec sheets, setup-and-specifications manuals and technical guidebooks (each entry's source). Dell lists
no Precision 3360 desktop; the nearest models are the 3260/3280 Compact, the 3460 SFF and the 3660 Tower.

How each body sits in a rack:
  Compact, SFF and 36xx towers have no Dell rack kit: they are part-width units with boxMm (front width x height, mm) lying on
  their side on a shelf, the same way NUCs and Mac minis are drawn. formFactor names the body so a rack kit can list it later.
  5820/7820/5860/7865/7875 towers also lie on their side on a shelf (4U). The 7920 Tower and 7960 Tower have Dell's optional
  19-inch rack rail kit (5U, full width).
Card slots are drawn as PCIe slots so PCIe cards (DeckLink, KONA, GPUs, NICs) can be fitted from pcie-cards.json. Anything a
source did not give is marked 'Check:' and the entry has verified False."""
import json, math, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
FILE = 'dell-precision.json'
def add(id, pn, name, fam, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id='dell-precision-' + id, manufacturer='Dell', partNumber=pn, name=name, family=fam, category='computer', ru=ru,
             widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    ports = m['portGroups'] = [dict(x) for x in ports]
    rear = {x['prefix'] for x in ports if x['face'] == 'rear'}
    for x in ports:  # keep port names unique: a front group named like a rear one gets 'Front '
        if x['face'] == 'front' and x['prefix'] in rear: x['prefix'] = 'Front ' + x['prefix']
    m.update(kw); FILES.setdefault(FILE, []).append(m)

def USBA(n, label, face='rear'): return g(face, 'io', 'USB', 'USB-A', n, label)
def USBC(n, label, face='rear'): return g(face, 'io', 'USB', 'USB-C', n, label)
def DP(n, label='DisplayPort 1.4 (on board)', face='rear'): return g(face, 'out', 'DisplayPort', 'DisplayPort', n, label)
def RJ(n, label): return R('io', 'Ethernet', 'RJ45', n, label)
def UAJ(): return F('io', 'Analog audio', '3.5mm jack', 1, 'Universal audio jack')
def LINE(label='Line out'): return R('out', 'Analog audio', '3.5mm jack', 1, label)
def RETASK(face='rear'): return g(face, 'io', 'Analog audio', '3.5mm jack', 1, 'Line out / line in (re-tasking)')
def SERIAL(label='Serial'): return R('io', 'RS-232', 'DB9', 1, label)
def PS2(label='PS/2 keyboard / mouse'): return R('in', 'Other', 'Mini-DIN 6', 2, label)
def OPT(label='Optional video port (HDMI / DP / VGA / USB-C, or empty)'): return R('out', 'Other', 'Other', 1, label)
def SLOT(n, label='PCIe slot'): return R('io', 'Other', 'Card slot', n, label)
def GPU(n=4): return R('out', 'DisplayPort', 'DisplayPort', n, 'GPU outputs')
def DCIN(): return R('in', 'Power', 'DC barrel', 1, 'DC in (19.5 V, 7.4 mm barrel, external adapter)')
def AC(conn='IEC C14', n=1, label='AC In'): return R('in', 'Power', conn, n, label)

CW, RU = 482.6 / 12, 44.45
def side(w_mm, h_mm, ff):
    """Part-width body lying on its side on a shelf: front face w_mm wide, h_mm high."""
    return dict(ru=math.ceil(h_mm / RU - 0.02), w=min(12, math.ceil(w_mm / CW - 0.02)), boxMm={'w': w_mm, 'h': h_mm}, formFactor=ff)

GPU_NOTE = 'GPU DisplayPort count depends on the card fitted (4 drawn, as an NVIDIA RTX card). '
CARD_NOTE = ('Fit PCIe cards (DeckLink, KONA, NICs, GPUs) in the PCIe slots from the card list, or add their ports as extra '
             'ports. ')
OPT_NOTE = ('The optional rear video port is a factory-fitted module: HDMI, DisplayPort, VGA or USB-C with DP Alt mode; '
            'rename or delete the "Optional video port" if yours differs or is blank. ')
SHELF = 'No Dell rack kit: drawn lying on its side on a shelf. '

# =====================================================================================================================
# Compact (ultra small, external power adapter)
# =====================================================================================================================
FF_CPT = 'Dell Precision Compact'
add('3240-compact', 'Precision 3240 Compact', 'Precision 3240 Compact workstation', 'Precision Compact', ports=[
    USBC(1, 'USB 3.2 Gen 2 Type-C', 'front'), USBA(1, 'USB 3.2 Gen 2 (PowerShare)', 'front'),
    F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'), RETASK('front'),
    DP(2), USBA(2, 'USB 3.2 Gen 2'), USBA(2, 'USB 3.2 Gen 1 (1 SmartPower)'), RJ(1, '1GbE'), OPT(), SLOT(1, 'PCIe x8 slot (low profile)'),
    DCIN()],
  notes='Ultra-small workstation (10th gen Core / Xeon W, 2020). 188.1 x 70.2 x 178.65 mm (H x W x D), 1.71 kg. One low-profile '
  'PCIe x8 Gen3 slot for a Quadro P620 / P1000 (their mini-DP outputs: fit the card or add the ports). External 180 W adapter, '
  '240 W with a graphics card (19.5 V DC, 7.4 mm barrel; the adapter itself takes an IEC C5 or C13 cord, Check). VESA 100 mount '
  'points. ' + OPT_NOTE + SHELF, src='Dell Precision 3240 Compact visual guide (KB 000180594) and setup and specifications',
  url='https://www.dell.com/support/kbdoc/en-us/000180594/precision-3240-compact-visual-guide-to-your-computer',
  weightKg=1.71, powerW=240, **side(188.1, 70.2, FF_CPT))
add('3260-compact', 'Precision 3260 Compact', 'Precision 3260 Compact workstation', 'Precision Compact', ports=[
    USBC(1, 'USB 3.2 Gen 2x2 Type-C', 'front'), USBA(1, 'USB 3.2 Gen 2 (PowerShare)', 'front'), UAJ(), RETASK('front'),
    DP(3, 'DisplayPort 1.4a (on board)'), USBA(2, 'USB 3.2 Gen 2'), USBA(2, 'USB 3.2 Gen 1 (1 Smart Power On)'), RJ(1, '1GbE'),
    OPT('Optional port (HDMI / DP / VGA / USB-C / PS2-serial, or empty)'), SLOT(1, 'PCIe x8 slot (half height)'), DCIN()],
  notes='Ultra-small workstation (12th/13th gen Core, 2022-2024). 190 x 71.8 x 178 mm (H x W x D), 1.37 to 2.03 kg. One '
  'half-height PCIe Gen4 x8 slot for an NVIDIA T400 / T1000 / RTX 3000 class card. External 180 W or 240 W adapter (7.4 mm '
  'barrel). The optional rear port can be PS/2 + serial, HDMI 2.0b, DP 1.4a, VGA or USB-C with DP Alt. VESA 100 mount '
  'points. ' + SHELF, src='Dell Precision 3260 Compact spec sheet',
  url='https://www.delltechnologies.com/asset/en-gb/products/workstations/technical-support/precision-3260-spec-sheet.pdf',
  weightKg=2.03, powerW=240, **side(190, 71.8, FF_CPT))
add('3280-compact', 'Precision 3280 Compact', 'Precision 3280 Compact workstation', 'Precision Compact', ports=[
    USBC(1, 'USB 3.2 Gen 2x2 Type-C (20 Gb)', 'front'), USBA(2, 'USB 3.2 Gen 2 (1 PowerShare)', 'front'), UAJ(),
    DP(3, 'DisplayPort 1.4a (on board)'), USBA(3, 'USB 3.2 Gen 2'), USBA(2, 'USB 3.2 Gen 1 (1 Smart Power On)'), RJ(1, '1GbE'),
    OPT('Optional video port (HDMI 2.1 / DP / VGA / USB-C, or empty)'), SLOT(1, 'PCIe x8 slot (half height)'), DCIN()],
  notes='Compact workstation (14th gen Core, 2024). 206 x 79.3 x 178 mm (H x W x D), 1.83 to 2.54 kg. One PCIe x8 slot (75 W) '
  'for an RTX 4000 SFF Ada (4 x DP), RTX 2000 Ada / T1000 (4 x mini-DP) or T400 (3 x mini-DP). Serial only as a PCIe card. '
  'External 180 W or 280 W adapter (7.4 mm barrel). ' + SHELF,
  src='Dell Precision 3280 CFF technical guidebook (Rev A01, May 2024)',
  url='https://delltechnologies.com/asset/en-us/products/workstations/technical-support/precision-3280-cff-technical-guidebook.pdf.external',
  weightKg=2.54, powerW=280, **side(206, 79.3, FF_CPT))

# =====================================================================================================================
# Small form factor (internal PSU)
# =====================================================================================================================
FF_SFF = 'Dell Precision SFF'
SFF_FRONT = [USBA(2, 'USB 2.0 (1 PowerShare)', 'front'), USBA(1, 'USB 3.2 Gen 2', 'front'),
             USBC(1, 'USB 3.2 Gen 2x2 Type-C', 'front'), UAJ()]
add('3450-sff', 'Precision 3450 SFF', 'Precision 3450 Small Form Factor workstation', 'Precision SFF', ports=SFF_FRONT + [
    DP(2), USBA(2, 'USB 2.0 (Smart Power On)'), USBA(3, 'USB 3.2 Gen 1'), USBA(1, 'USB 3.2 Gen 2'), RJ(1, '1GbE (Intel i219-LM)'),
    RETASK(), SERIAL(), PS2(), OPT(), SLOT(1, 'PCIe x16 Gen4 slot (half height)'), SLOT(1, 'PCIe x4 Gen3 slot (half height)'),
    AC()],
  notes='SFF workstation (10th/11th gen Core, Xeon W, 2021). 290 x 92.6 x 292.8 mm (H x W x D), up to 5.96 kg. Two half-height '
  'PCIe slots (Gen4 x16, Gen3 x4) for a Quadro P400 to P1000 / Radeon Pro WX class card. Internal 260 W Bronze or 300 W '
  'Platinum PSU, 90-264 V AC. ' + OPT_NOTE + SHELF + 'Check: AC inlet (IEC C14 drawn, the spec says "AC-in").',
  src='Dell Precision 3450 SFF setup and specifications (Rev A02)',
  url='https://coloradosos.gov/pubs/elections/VotingSystems/DVS-DemocracySuite517/documentation/DellPrecision3450-SFFSetupandSpecifications.pdf',
  weightKg=5.96, powerW=300, **side(290, 92.6, FF_SFF))
add('3460-sff', 'Precision 3460 SFF', 'Precision 3460 Small Form Factor workstation', 'Precision SFF', ports=SFF_FRONT + [
    DP(3, 'DisplayPort 1.4a (on board)'), USBA(2, 'USB 2.0 (Smart Power On)'), USBA(3, 'USB 3.2 Gen 1'), USBA(1, 'USB 3.2 Gen 2'),
    RJ(1, '1GbE'), RETASK(), OPT(), SLOT(1, 'PCIe x16 Gen4 slot (half height)'), SLOT(1, 'PCIe x4 Gen3 slot (half height)'), AC()],
  notes='SFF workstation (12th to 14th gen Core, 2022-2024). 290 x 92.6 x 292.8 mm (H x W x D), 3.87 to 5.38 kg. Two '
  'half-height PCIe slots (Gen4 x16, Gen3 x4) for low-profile cards up to an RTX 4000 SFF Ada / RTX A2000. Optional rear '
  'serial / PS2 port (add it if fitted). Internal 260 W Bronze or 300 W Platinum PSU. ' + OPT_NOTE + SHELF +
  'Check: AC inlet (IEC C14 drawn) and the RJ45 speed (Dell papers give 1GbE i219 and 2.5GbE i225).',
  src='Dell Precision 3460 SFF spec sheet and technical guidebook (Rev A04)',
  url='https://www.delltechnologies.com/asset/en-ca/products/workstations/technical-support/precision-3460-sff-spec-sheet.pdf',
  weightKg=5.38, powerW=300, **side(290, 92.6, FF_SFF))

# =====================================================================================================================
# 36xx towers (mini tower, internal ATX PSU)
# =====================================================================================================================
FF_T3 = 'Dell Precision 36xx tower (on its side)'
T_SHELF = 'No Dell rack kit: drawn lying on its side on a shelf (stood upright it is 8U to 9U tall and 4 to 5 columns wide). '
add('3630-tower', 'Precision 3630 Tower', 'Precision 3630 Tower workstation', 'Precision 36xx Tower', ports=[
    USBA(2, 'USB 2.0', 'front'), USBA(1, 'USB 3.1 Gen 1', 'front'), USBC(1, 'USB 3.1 Gen 2 Type-C', 'front'),
    F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'),
    DP(2, 'DisplayPort (on board)'), USBA(4, 'USB 3.1 Gen 1'), USBA(2, 'USB 2.0'), RJ(1, '1GbE'), LINE(), SERIAL(), PS2(), OPT(),
    SLOT(1, 'PCIe x16 Gen3 slot'), SLOT(2, 'PCIe x4 Gen3 slot'), SLOT(1, 'PCI slot (legacy)'), AC()],
  notes='Mini tower workstation (8th/9th gen Core, Xeon E, 2018). 335 x 176.6 x 345 mm (H x W x D), 10.6 kg. 4 full-height '
  'slots: PCIe x16, 2 x PCIe x4 (open ended), legacy PCI. 300 W Bronze, 460 W or 850 W Gold PSU. ' + OPT_NOTE + CARD_NOTE + T_SHELF +
  'Check: AC inlet (IEC C14 drawn).', src='Dell Precision Tower 3630 technical guidebook (Rev A01)',
  url='https://japancatalog.dell.com/c/wp-content/uploads/Dell_Precision_Tower_3630_Technical_Guide_Book.pdf',
  weightKg=10.6, powerW=850, **side(335, 176.6, FF_T3))
add('3640-tower', 'Precision 3640 Tower', 'Precision 3640 Tower workstation', 'Precision 36xx Tower', ports=[
    USBA(2, 'USB 2.0', 'front'), USBA(1, 'USB 3.2 Gen 1 (PowerShare)', 'front'), USBC(1, 'USB 3.2 Gen 2 Type-C (PowerShare)', 'front'),
    F('out', 'Analog audio', '3.5mm jack', 1, 'Headphone'),
    DP(2), PS2(), USBA(2, 'USB 2.0 (Smart Power On)'), USBA(2, 'USB 3.2 Gen 2'), USBA(2, 'USB 3.2 Gen 1'),
    RJ(1, '1GbE (Intel i219-LM)'), RETASK(), OPT(), SLOT(1, 'PCIe x16 Gen3 slot'), SLOT(1, 'PCIe x4 Gen3 slot'),
    SLOT(1, 'PCI slot (legacy)'), AC()],
  notes='Mini tower workstation (10th gen Core, Xeon W-1200, 2020). 335 x 176.6 x 345 mm (H x W x D), 10.6 kg. Front shown is '
  'the standard I/O panel; the advanced panel has 3 USB-A, 1 USB-C and an SD reader. 3 full-height slots: PCIe x16, PCIe x4, '
  'legacy PCI. Serial only as an add-in card. 300 W to 1000 W PSU, 90-264 V AC. ' + OPT_NOTE + CARD_NOTE + T_SHELF +
  'Check: AC inlet (IEC C14 drawn).', src='Dell Precision 3640 Tower setup and specifications (Rev A02)',
  url='https://pcserverandparts.com/content/Spec%20Sheets/Workstations/Dell/Dell%20Precision%20T3640/Precision%203640%20Tower%20Setup%20and%20Specifications.pdf',
  weightKg=10.6, powerW=1000, **side(335, 176.6, FF_T3))
add('3650-tower', 'Precision 3650 Tower', 'Precision 3650 Tower workstation', 'Precision 36xx Tower', ports=[
    USBA(2, 'USB 2.0', 'front'), USBA(1, 'USB 3.2 Gen 1 (PowerShare)', 'front'), USBC(1, 'USB 3.2 Gen 2 Type-C (PowerShare)', 'front'),
    F('io', 'Analog audio', '3.5mm jack', 1, 'Headset'),
    DP(2), PS2(), USBA(2, 'USB 2.0 (Smart Power On)'), USBA(1, 'USB 3.2 Gen 2'), USBA(2, 'USB 3.2 Gen 1'),
    RJ(1, '1GbE (Intel i219-LM)'), LINE(), OPT(), SLOT(1, 'PCIe x16 Gen4 slot'), SLOT(1, 'PCIe x4 Gen3 slot'),
    SLOT(1, 'PCI slot (legacy)'), AC()],
  notes='Mini tower workstation (11th gen Core, Xeon W-1300, 2021). 335 x 176.6 x 345 mm (H x W x D), 8.5 kg. Front shown is the '
  'standard I/O panel (the advanced panel adds USB-A, a 20 Gb USB-C and an SD reader). Optional second RJ45 (2.5GbE): add it '
  'if fitted. 3 full-height slots: PCIe x16 Gen4 (graphics up to 350 W), PCIe x4, legacy PCI. 300 W to 1000 W Gold PSU. '
  + OPT_NOTE + CARD_NOTE + T_SHELF + 'Check: AC inlet (IEC C14 drawn).', src='Dell Precision 3650 Tower spec sheet',
  url='https://pcserverandparts.com/content/Spec%20Sheets/Workstations/Dell/Dell%20Precision%203650/Dell%20Precision%203650%20Tower%20Workstation%20Spec%20Sheet.pdf',
  weightKg=8.5, powerW=1000, **side(335, 176.6, FF_T3))
T36_NEW_FRONT = [USBA(2, 'USB 3.2 Gen 1 (1 PowerShare)', 'front'), USBC(1, 'USB 3.2 Gen 2 Type-C', 'front'),
                 USBC(1, 'USB 3.2 Gen 2x2 Type-C (PowerShare)', 'front'), UAJ()]
T36_NEW_REAR = [USBA(2, 'USB 2.0 (Smart Power On)'), USBA(2, 'USB 3.2 Gen 2'), USBC(2, 'USB 3.2 Gen 2 Type-C'),
                DP(2, 'DisplayPort 1.4a (on board)'), OPT(), RJ(1, '1GbE (Intel i219-LM)'), LINE()]
add('3660-tower', 'Precision 3660 Tower', 'Precision 3660 Tower workstation', 'Precision 36xx Tower', ports=T36_NEW_FRONT +
    T36_NEW_REAR + [SLOT(1, 'PCIe x16 Gen5 slot'), SLOT(1, 'PCIe x4 Gen4 slot'), SLOT(1, 'PCIe x4 Gen3 slot'), AC()],
  notes='Tower workstation (12th/13th gen Core, 2022-2023). 372.9 x 173 x 420.2 mm (H x W x D), 8.44 to 16.36 kg. SD reader and '
  'slim optical bay on the front. Optional 2.5GbE RJ45 (add it if fitted). No rear serial or PS/2 (add-in brackets). 3 slots: '
  'PCIe x16 Gen5 (graphics), x4 Gen4, x4 Gen3. 300 W to 1000 W Platinum PSU, 90-264 V AC. ' + OPT_NOTE + CARD_NOTE + T_SHELF +
  'Check: AC inlet (IEC C14 drawn).', src='Dell Precision 3660 Tower technical guidebook (Rev A03, June 2023)',
  url='https://delltechnologies.com/asset/en-us/products/workstations/technical-support/precision-3660t-technical-guidebook.pdf',
  weightKg=16.36, powerW=1000, **side(372.9, 173, FF_T3))
add('3680-tower', 'Precision 3680 Tower', 'Precision 3680 Tower workstation', 'Precision 36xx Tower', ports=T36_NEW_FRONT +
    T36_NEW_REAR + [SLOT(1, 'PCIe x16 slot'), SLOT(2, 'PCIe x4 slot'), AC()],
  notes='Tower workstation (14th gen Core, 2024-2025). 372.9 x 173 x 420.2 mm (H x W x D), 7.58 to 16.05 kg. SD slot on the '
  'front. Optional 2.5GbE RJ45 (add it if fitted). Serial only as a PCIe card. 3 slots: PCIe x16, Gen3 x4, Gen4 x4. 300 W, '
  '500 W or 1000 W Platinum PSU (1000 W for K-series CPUs). ' + OPT_NOTE + CARD_NOTE + T_SHELF +
  'Check: AC inlet (IEC C14 drawn).', src='Dell Precision 3680 Tower technical guidebook (Rev A02, June 2025)',
  url='https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/precision-3680-tower-technical-guidebook.pdf',
  weightKg=16.05, powerW=1000, **side(372.9, 173, FF_T3))

# =====================================================================================================================
# 5000 / 7000 towers
# =====================================================================================================================
FF_TB = 'Dell Precision 5000/7000 tower (on its side)'
B_SHELF = ('No Dell rack kit listed for this model: drawn lying on its side on a shelf (4U, about 520 mm deep with feet). ')
G1_FRONT = [USBA(2, 'USB 3.2 Gen 1', 'front'), USBC(2, 'USB 3.2 Gen 1 Type-C (1 DP / Power Delivery)', 'front'), UAJ()]
G1_REAR = [USBA(6, 'USB 3.2 Gen 1 (1 DP / Power Delivery)'), SERIAL(), PS2(), LINE(), R('in', 'Analog audio', '3.5mm jack', 1, 'Line in / mic')]
for code, txt, psu in [('5820', 'Single-socket Xeon W-2100/2200 tower (2017-2022). 425 W or 950 W Gold PSU. Up to 2 x 295 W '
                        'double-width GPUs.', 950),
                       ('7820', 'Dual-socket Xeon Scalable tower (2017-2022). 950 W Gold PSU. Up to 2 x 295 W double-width '
                        'GPUs (2 x 160 W single-width with the second CPU).', 950)]:
    add(f'{code}-tower', f'Precision {code} Tower', f'Precision {code} Tower workstation', 'Precision 5000/7000 Tower (2017)',
        ports=G1_FRONT + G1_REAR + [RJ(1, '1GbE (Intel i219)'), SLOT(5, 'PCIe slot'), SLOT(1, 'PCI slot (legacy)'), GPU(), AC()],
        notes=txt + ' 417.9 x 176.5 x 518.2 mm (H x W x D), 13.2 to 15.4 kg. SD slot on the front. 5 PCIe x16 physical slots (2 '
        'x16, x8, x4 and x1 wired) plus one legacy PCI. ' + GPU_NOTE + CARD_NOTE + B_SHELF + 'Check: AC inlet (IEC C14 drawn).',
        src=f'Dell Precision {code} Tower spec sheet and 5820/7820 technical guidebook',
        url=f'https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/Precision_{code}_Tower_Spec_Sheet.pdf'
        if code == '7820' else 'https://delltechnologies.com/asset/en-vn/products/workstations/technical-support/Precision_5820_Tower_Spec_Sheet.pdf',
        weightKg=15.4, powerW=psu, full=True, **side(417.9, 176.5, FF_TB))
add('7920-tower', 'Precision 7920 Tower', 'Precision 7920 Tower workstation on rack rails (5U)', 'Precision 5000/7000 Tower (2017)',
    5, [USBA(2, 'USB 3.1 Gen 1', 'front'), USBC(2, 'USB 3.1 Type-C (1 PowerShare)', 'front'), UAJ(),
        USBA(6, 'USB 3.1 Gen 1 (1 PowerShare)'), SERIAL(), PS2(), RJ(2, '1GbE (Intel i219 + i210, 1 AMT)'), LINE(),
        R('in', 'Analog audio', '3.5mm jack', 1, 'Line in / mic'), SLOT(1, 'PCIe x8 Gen3 slot'), SLOT(6, 'PCIe x16 Gen3 slot'),
        GPU(), AC()],
    'Dual-socket Xeon Scalable full tower (2017-2022). 433 x 218 x 566 mm (H x W x D), 20.4 to 24.3 kg. Optional Dell 19-inch '
    'rack rail kit: drawn 5U on its side (Dell gives no U figure; the 7960 Tower on the same kit takes 5U). 7 slots (slots 6 '
    'and 7 need the second CPU), up to 3 x 300 W double-width GPUs. 1400 W Gold PSU (1100 W at 108-180 V). Optional 10GbE '
    'X550-T2 card. SD slot on the front. ' + GPU_NOTE + CARD_NOTE + 'Check: rack height and the AC inlet (IEC C14 drawn; 1400 W '
    'units often take C19/C20).', 'Dell Precision 7920 Tower spec sheet and technical guidebook',
    'https://cdn.shopify.com/s/files/1/0248/8539/5502/files/Precision-7920-Tower-Spec-Sheet.pdf', verified=False, full=True,
    weightKg=24.3, powerW=1400)
G2_FRONT = lambda c2=('USB 3.2 Gen 2x2 Type-C (PowerShare)', 'USB 3.2 Gen 2 Type-C'): [
    USBA(2, 'USB 3.2 Gen 1', 'front'), USBC(1, c2[0], 'front'), USBC(1, c2[1], 'front'), UAJ()]
G2_REAR = [USBC(3, 'USB 3.2 Gen 2 Type-C'), USBA(3, 'USB 3.2 Gen 1 (1 Smart Power On)'), RJ(1, '1GbE'), RJ(1, '10GbE'), LINE()]
OPT_SP = 'Serial and PS/2 are optional on the rear (add them if fitted). '
add('5860-tower', 'Precision 5860 Tower', 'Precision 5860 Tower workstation', 'Precision 5000/7000 Tower (2023)',
    ports=G2_FRONT() + G2_REAR + [SLOT(1, 'PCIe x16 Gen5 slot'), SLOT(1, 'PCIe x16 Gen4 slot'), SLOT(3, 'PCIe x8 Gen4 slot'),
                                  GPU(), AC()],
    notes='Single-socket Xeon W-2400/2500 mid tower (2023-). 414 x 172.6 x 429.6 mm (417.9 x 176.5 x 452.1 mm with feet), 14.4 '
    'to 21.7 kg. SD slot on the front. 5 full-height slots (Gen5 x16, Gen4 x16, 3 x Gen4 x8, one wired x4), up to 2 GPUs. 750 W '
    'or 1350 W Platinum PSU. ' + OPT_SP + GPU_NOTE + CARD_NOTE + B_SHELF + 'Check: AC inlet (IEC C14 drawn; the 1350 W unit '
    'takes C20 on the 7875).', src='Dell Precision 5860 Tower spec sheet',
    url='https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/precision-5860-tower-spec-sheet.pdf',
    weightKg=21.7, powerW=1350, **side(417.9, 176.5, FF_TB))
add('7865-tower', 'Precision 7865 Tower', 'Precision 7865 Tower workstation (AMD Threadripper PRO)', 'Precision 5000/7000 Tower (2023)',
    ports=G2_FRONT(('USB 3.2 Gen 2 Type-C (PowerShare)', 'USB 3.2 Gen 2 Type-C')) + G2_REAR +
    [SLOT(2, 'PCIe x16 Gen4 slot'), SLOT(3, 'PCIe x8 Gen4 slot'), GPU(), AC('IEC C20')],
    notes='AMD Threadripper PRO 5000WX tower (2022-2023). 414 x 172.6 x 429.6 mm (417.9 x 176.5 x 452.1 mm with feet), 16.1 to '
    '21.9 kg. SD reader on the front. 5 full-height slots (2 x Gen4 x16, 3 x Gen4 x8), up to 2 x 300 W GPUs. 1350 W Platinum '
    'PSU. ' + OPT_SP + GPU_NOTE + CARD_NOTE + B_SHELF + 'Check: AC inlet (IEC C20 drawn, as the 1350 W unit on the 7875).',
    src='Dell Precision 7865 spec sheet', url='https://cdn.shopify.com/s/files/1/0593/9249/1689/files/precision-7865-spec-sheet.pdf',
    verified=False, weightKg=21.9, powerW=1350, **side(417.9, 176.5, FF_TB))
add('7875-tower', 'Precision 7875 Tower', 'Precision 7875 Tower workstation (AMD Threadripper PRO)', 'Precision 5000/7000 Tower (2023)',
    ports=G2_FRONT(('USB 3.2 Gen 2 Type-C (PowerShare)', 'USB 3.2 Gen 2 Type-C')) + G2_REAR +
    [SLOT(2, 'PCIe x16 slot (1 Gen5)'), SLOT(4, 'PCIe x8 slot (1 Gen5)'), GPU(), AC('IEC C20')],
    notes='AMD Threadripper PRO 7000WX / 9000WX tower (2023-). 442.7 x 172.6 x 465 mm (446.6 x 176.5 x 487.5 mm with feet), '
    '18.3 to 25.6 kg. SD slot on the front. 6 full-height slots, up to 2 x 300 W GPUs or one 500 W triple-wide card; no '
    'integrated graphics. 1350 W Platinum PSU on an IEC C20 inlet (the 1000 W option takes C14). ' + OPT_SP + GPU_NOTE +
    CARD_NOTE + B_SHELF, src='Dell Precision 7875 Tower spec sheet',
    url='https://pcserverandparts.com/content/Spec%20Sheets/Workstations/Dell/Dell%20Precision%207875/Dell%20Precision%207875%20Tower%20Spec%20Sheet.pdf',
    weightKg=25.6, powerW=1350, full=True, **side(446.6, 176.5, FF_TB))
add('7960-tower', 'Precision 7960 Tower', 'Precision 7960 Tower workstation on rack rails (5U)', 'Precision 5000/7000 Tower (2023)', 5,
    G2_FRONT() + G2_REAR + [SERIAL(), PS2(), SLOT(2, 'PCIe x16 Gen5 slot'), SLOT(2, 'PCIe x16 Gen4 slot'),
                            SLOT(4, 'PCIe x8 Gen4 slot'), GPU(), AC('IEC C20')],
    'Xeon W-3400/3500 full tower (2023-). 430.7 x 218 x 538.3 mm (434.2 x 218 x 569.2 mm with feet), 21 to 37.6 kg. Dell '
    '19-inch rack mount kit: 5U. SD slot and drive flex bays on the front. 8 slots (2 Gen5 x16, 2 Gen4 x16, 4 Gen4 x8, two of '
    'them wired x4), up to 4 double-width GPUs. 1100/1400 W Gold or 1500/2200 W Platinum PSU (low/high line). ' + GPU_NOTE +
    CARD_NOTE + 'Check: AC inlet (IEC C20 drawn: Dell gives C19/C20 cords for the 1500/2200 W units).',
    'Dell Precision 7960 Tower spec sheet and technical guidebook (Rev A02)',
    'https://www.delltechnologies.com/asset/en-us/products/workstations/technical-support/precision-7960-tower-spec-sheet.pdf',
    full=True, weightKg=37.6, powerW=2200)

# =====================================================================================================================
# Rack workstations (the 7960 Rack is in dell.json, tools/it.py)
# =====================================================================================================================
add('3930-rack', 'Precision 3930 Rack', 'Precision 3930 Rack 1U workstation', 'Precision Rack', 1,
    [UAJ(), USBC(1, 'USB 3.1 Type-C', 'front'), USBA(2, 'USB 3.1', 'front'),
     USBC(2, 'USB 3.1 Type-C / DisplayPort (iGPU)'), R('in', 'Other', 'Other', 1, 'Remote power switch'), SERIAL(),
     RJ(1, '1GbE (Intel)'), RJ(1, '10GbE (Aquantia)'), SLOT(1, 'PCIe x16 Gen3 slot (FH, double width)'),
     SLOT(1, 'PCIe x8 Gen3 slot (FH)'), SLOT(1, 'PCIe x4 Gen3 slot (FH)'), GPU(), AC('IEC C14', 2, 'PSU')],
    '1U short-depth rack workstation (Xeon E-2100/2200, 8th/9th gen Core, 2018-2022). 42.8 x 482 x 589.1 mm with bezel (577.6 '
    'without), 8.74 kg. SD reader on the front. 3 full-height slots: one double-width x16 GPU up to 295 W or two single-width '
    'x8. One or two hot-plug 550 W Platinum PSUs (two needed, non-redundant, for RTX 4000 x 2 / RTX 5000 / RTX 6000; change '
    'the count to 1 if only one is fitted). Optional legacy PCI riser. No iDRAC. ' + GPU_NOTE + CARD_NOTE +
    'Check: AC inlet (IEC C14 drawn).', 'Dell Precision 3930 Rack spec sheet',
    'https://cdn.shopify.com/s/files/1/0593/9249/1689/files/precision_3930_rack_spec_sheet.pdf', full=True, weightKg=8.74,
    powerW=1100)
add('7920-rack', 'Precision 7920 Rack', 'Precision 7920 Rack 2U workstation', 'Precision Rack', 2,
    [R('out', 'Other', 'VGA', 1, 'VGA (iDRAC)'), USBA(2, 'USB 2.0', 'front'), USBA(1, 'USB 2.0 iDRAC Direct', 'front'),
     g('front', 'out', 'Other', 'VGA', 1, 'VGA (iDRAC)'),
     USBA(2, 'USB 3.1'), RJ(4, '1GbE (Intel i350 quad)'), RJ(1, 'iDRAC9'), SERIAL(), SLOT(8, 'PCIe x16 Gen3 slot'), GPU(),
     AC('IEC C14', 2, 'PSU')],
    '2U dual-socket Xeon Scalable rack workstation (2018-2022). 86.8 x 482 x 715.5 mm (751.3 mm with bezel). iDRAC9 with its '
    'own RJ45 and VGA. Base network is an Intel i350 quad 1GbE (options: X550 dual 10GbE + i350, or X710 dual 10GbE SFP+; '
    'change the ports to suit). 8 PCIe Gen3 slots (x16 mechanical), up to 3 x 300 W double-width GPUs. One or two hot-plug '
    '1100 W Gold PSUs (1600 W at 220 V for big GPU builds; change the count to 1 if only one is fitted). ' + GPU_NOTE +
    CARD_NOTE + 'Check: AC inlet (IEC C14 drawn; 1600 W units take C20).', 'Dell Precision 7920 Rack (R7920XL) spec sheet',
    'https://new.abb.com/docs/librariesprovider104/pcp-global-sales-support/dell-precision-r7920xl.pdf', full=True, powerW=1600)

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
