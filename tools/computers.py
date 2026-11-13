#!/usr/bin/env python3
"""Generates catalogue/apple.json (Mac mini, Mac Studio, Mac Pro rack), intel.json and asus.json (NUC mini PCs), and the
rack kits that carry them: sonnet.json, pennelcom.json, myelectronics.json. Added 2026-11-13.

Desktop computers are part-width units with boxMm (front width x height, mm), so the app draws them at real size
sitting on a shelf. ru is the rack space a unit needs on a shelf; widthCols is its width in twelfths of 482.6 mm.
formFactor names the body shape; a kit's carrier.fits lists the formFactors it holds and carrier.bays how many.
Ports come from the makers' tech specs pages (each entry's source); verified=False and a 'Check:' note mark the rest."""
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

def TB(n, gen, face='rear'): return g(face, 'io', 'USB', 'USB-C', n, f'Thunderbolt {gen}')
def UA(n, label='USB-A', face='rear'): return g(face, 'io', 'USB', 'USB-A', n, label)
def UC(n, label='USB-C', face='front'): return g(face, 'io', 'USB', 'USB-C', n, label)
def HD(n=1, label='HDMI'): return R('out', 'HDMI', 'HDMI', n, label)
def LAN(n=1, label='Ethernet'): return R('io', 'Ethernet', 'RJ45', n, label)
def HP(face='rear', label='Headphones'): return g(face, 'out', 'Analog audio', '3.5mm jack', 1, label)
APPLE_AC = R('in', 'Power', 'IEC C8 inlet (figure-8)', 1, 'AC In')
def DCIN(label='DC In 19V'): return R('in', 'Power', 'DC barrel', 1, label)

# ======================= Apple =======================
AP = lambda *a, **k: add('apple.json', 'apple-', 'Apple', *a, **k)
SUP = 'https://support.apple.com/'
SHELF = ' Sits on a rack shelf or in a rack kit (Sonnet, Penn Elcom).'
CORD = ' AC inlet is a figure-8 IEC C8 (C7 cord), per Apple\'s port drawings.'
SCORD = ' AC inlet is a cloverleaf IEC C6 (C5 cord), per Apple\'s port drawings.'
STUDIO_AC = R('in', 'Power', 'IEC C6 inlet (cloverleaf)', 1, 'AC In')

# Mac mini, 2024 and later: 127 x 127 x 50 mm, front USB-C and headphones, power button underneath
for chip, yr, pn, tb, lan, w_kg, url in [
        ('M6', 2026, 'Mac mini (M6)', 4, '2.5Gb Ethernet (10Gb option)', 0.67, SUP + '128108'),
        ('M5 Pro', 2026, 'Mac mini (M5 Pro)', 5, '2.5Gb Ethernet (10Gb option)', 0.73, SUP + '128108'),
        ('M4', 2024, 'Mac mini (M4)', 4, 'Gigabit Ethernet (10Gb option)', 0.67, SUP + '121555'),
        ('M4 Pro', 2024, 'Mac mini (M4 Pro)', 5, 'Gigabit Ethernet (10Gb option)', 0.73, SUP + '121555')]:
    AP(f'mac-mini-{chip.lower().replace(" ", "-")}', pn, f'Mac mini ({chip}, {yr})', 'Mac mini', 'computer', 2,
       [UC(2, 'USB-C (USB 3)'), HP('front'), TB(3, tb), HD(), LAN(1, lan.split(' (')[0]), APPLE_AC],
       f'127 x 127 x 50 mm, {w_kg} kg, 155 W max. Back: {lan}, HDMI, 3 x Thunderbolt {tb} (USB-C, also DisplayPort). '
       'Front: 2 x USB-C (USB 3, 10 Gb/s) and a 3.5 mm headphone jack. Power button on the underside. '
       + ('Genlock on the Thunderbolt 5 ports. ' if chip == 'M5 Pro' else '') + 'Needs 2RU on a shelf (50 mm tall).' + SHELF + CORD,
       f'Apple Mac mini ({yr}) tech specs', url, w=4, boxMm={'w': 127, 'h': 50}, powerW=155, formFactor='Mac mini (2024+)')

# Mac mini, 2018 to 2023: 197 x 197 x 36 mm, every port on the back
for id_, pn, name, tb, tbgen, usba, watts, kg, url in [
        ('mac-mini-m2-pro', 'Mac mini (M2 Pro)', 'Mac mini (M2 Pro, 2023)', 4, '4', 2, 185, 1.28, SUP + '111837'),
        ('mac-mini-m2', 'Mac mini (M2)', 'Mac mini (M2, 2023)', 2, '4', 2, 150, 1.18, SUP + '111837'),
        ('mac-mini-m1', 'Mac mini (M1)', 'Mac mini (M1, 2020)', 2, '/ USB 4', 2, 150, 1.2, SUP + '111894')]:
    AP(id_, pn, name, 'Mac mini', 'computer', 1,
       [TB(tb, tbgen), UA(usba, 'USB-A (5 Gb/s)'), HD(), LAN(1, 'Gigabit Ethernet'), HP(), APPLE_AC],
       f'197 x 197 x 36 mm, {kg} kg, {watts} W max. Every port is on the back: {tb} x Thunderbolt {tbgen} (USB-C), {usba} x USB-A, HDMI, '
       'Gigabit Ethernet (10Gb option), 3.5 mm headphone jack. Front: status light only. Fits 1RU on a shelf; two side by side '
       'in a Sonnet RackMac mini (2018-2023).' + SHELF + CORD,
       f'Apple {name} tech specs', url, w=5, boxMm={'w': 197, 'h': 36}, powerW=watts, formFactor='Mac mini (2018-2023)')
AP('mac-mini-2018', 'Mac mini (2018)', 'Mac mini (2018, Intel)', 'Mac mini', 'computer', 1,
   [TB(4, '3'), UA(2, 'USB-A (5 Gb/s)'), HD(1, 'HDMI 2.0'), LAN(1, 'Gigabit Ethernet'), HP(), APPLE_AC],
   '197 x 197 x 36 mm, 1.3 kg, 150 W max, Intel Core i3/i5/i7. Every port is on the back: 4 x Thunderbolt 3 (USB-C), 2 x USB-A, HDMI 2.0, '
   'Gigabit Ethernet (10Gb option), 3.5 mm headphone jack. Fits 1RU on a shelf.' + SHELF + CORD,
   'Apple Mac mini (2018) tech specs', SUP + '111912', w=5, boxMm={'w': 197, 'h': 36}, powerW=150, formFactor='Mac mini (2018-2023)')

# Mac Studio: 197 x 197 x 95 mm. Front: 2 x USB-C (Max) or 2 x Thunderbolt (Ultra) plus SDXC; back: 4 x Thunderbolt, 2 x USB-A, HDMI, 10GbE, headphones
for yr, chip, tb, watts, kg, url in [
        (2026, 'M5 Max', 5, 480, 2.7, SUP + '128107'), (2026, 'M5 Ultra', 5, 480, 3.6, SUP + '128107'),
        (2025, 'M4 Max', 5, 480, 2.74, SUP + '122211'), (2025, 'M3 Ultra', 5, 480, 3.64, SUP + '122211'),
        (2023, 'M2 Max', 4, 370, 2.7, SUP + '111835'), (2023, 'M2 Ultra', 4, 370, 3.6, SUP + '111835'),
        (2022, 'M1 Max', 4, 370, 2.7, SUP + '111900'), (2022, 'M1 Ultra', 4, 370, 3.6, SUP + '111900')]:
    ultra = 'Ultra' in chip
    front = TB(2, tb, 'front') if ultra else UC(2, 'USB-C (10 Gb/s)')
    AP(f'mac-studio-{chip.lower().replace(" ", "-")}', f'Mac Studio ({chip})', f'Mac Studio ({chip}, {yr})', 'Mac Studio', 'computer', 3,
       [front, TB(4, tb), UA(2, 'USB-A (5 Gb/s)'), HD(1, 'HDMI 2.1' if yr >= 2025 else 'HDMI'), LAN(1, '10Gb Ethernet'), HP(), STUDIO_AC],
       f'197 x 197 x 95 mm, {kg} kg, {watts} W max. Back: 4 x Thunderbolt {tb} (USB-C), 2 x USB-A, HDMI, 10Gb Ethernet (RJ45, '
       '1/2.5/5/10Gb), 3.5 mm headphone jack. Front: ' + (f'2 x Thunderbolt {tb}' if ultra else '2 x USB-C (10 Gb/s)')
       + ' and an SDXC card slot; power button on the back. Needs 3RU on a shelf; one or two in a Sonnet RackMac Studio (3U).' + SHELF + SCORD,
       f'Apple Mac Studio ({yr}) tech specs', url, w=5, boxMm={'w': 197, 'h': 95}, powerW=watts, formFactor='Mac Studio')

AP('mac-pro-rack-2023', 'Mac Pro (Rack, 2023)', 'Mac Pro (Rack, 2023) M2 Ultra 5U', 'Mac Pro', 'computer', 5,
   [TB(2, 4, 'front'), TB(6, 4), UA(2, 'USB-A (5 Gb/s)'), HD(2), LAN(2, '10Gb Ethernet'), HP(),
    R('io', 'Other', 'Card slot', 6, 'PCIe Gen 4 slot'), R('in', 'Power', 'IEC C14 inlet', 1, 'AC In')],
   '5U rack-mount, 482 mm wide, 493.5 mm deep from the fascia (539.5 mm with handles), fits racks 610 to 1067 mm deep; 17.2 kg. '
   'Front: power button, status light, 2 x Thunderbolt 4. Back: 6 x Thunderbolt 4, 2 x USB-A, 2 x HDMI, 2 x 10Gb Ethernet, '
   '3.5 mm headphone jack, power. 6 full-length PCIe Gen 4 slots (2 x16, 4 x8) plus the Apple I/O card slot; add capture, '
   'SDI and network card ports as extra ports. 1280 W max (12 A at 100-125 V, 6 A at 220-240 V); IEC C14 inlet per Apple\'s drawing.',
   'Apple Mac Pro (Rack, 2023) tech specs and Mac Pro (Rack) tour', SUP + '111836', full=True, powerW=1280)

# ======================= Intel NUC (Intel-branded kits, now supported by ASUS) =======================
NUC_W = 3   # 117 mm wide: 3 twelfths
def nuc(file, pre, mfr, id_, pn, name, fam, tall, front, rear, notes, src, url, verified=True, w=NUC_W, wmm=117, hmm=None, ff='NUC 4x4', **k):
    h = hmm or (54 if tall else 37)
    add(file, pre, mfr, id_, pn, name, fam, 'computer', 2 if h > 42 else 1, front + rear,
        f'{wmm} x 112 x {h} mm ({"tall" if tall else "slim"} chassis). ' + notes
        + f' Needs {2 if h > 42 else 1}RU on a shelf; three per MyElectronics {"1.5U" if h > 42 else "1U"} NUC rack kit.',
        src, url, verified=verified, w=w, boxMm={'w': wmm, 'h': h}, formFactor=ff + (' tall' if tall else ' slim'), **k)

IN = lambda *a, **k: nuc('intel.json', 'intel-', 'Intel', *a, **k)
FRONT12 = [UA(2, 'USB 3.2 Gen 2', 'front'), HP('front', 'Headset')]
REAR12 = [TB(2, 4), UA(1, 'USB 3.2 Gen 2'), UA(1, 'USB 2.0'), HD(2, 'HDMI'), LAN(1, '2.5GbE'), DCIN('DC In 12-20V')]
for tall in (True, False):
    s = 'H' if tall else 'K'
    IN(f'nuc13an{s.lower()}', f'NUC13AN{s}', f'NUC 13 Pro kit, {"tall" if tall else "slim"} (NUC13AN{s})', 'NUC 13 Pro', tall,
       FRONT12, [TB(2, 4), UA(1, 'USB 3.2 Gen 2'), UA(1, 'USB 2.0'), HD(2, 'HDMI 2.1'), LAN(1, '2.5GbE'), DCIN('DC In 19-20V')],
       '13th gen Intel Core (Arena Canyon). Front: 2 x USB 3.2 Gen 2 Type-A, 3.5 mm headset jack, power button. Back: 2 x Thunderbolt 4 '
       '(USB-C with DisplayPort 1.4), USB 3.2 Gen 2 Type-A, USB 2.0 Type-A, 2 x HDMI 2.1, 2.5GbE (Intel I226), DC in. 90 W 19 V (i3) or '
       '120 W 20 V (i5/i7) adapter.', 'ASUS NUC 13 Pro tech specs',
       'https://www.asus.com/in/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-13-pro/techspec/', powerW=120)
    IN(f'nuc12ws{s.lower()}', f'NUC12WS{s}', f'NUC 12 Pro kit, {"tall" if tall else "slim"} (NUC12WS{s})', 'NUC 12 Pro', tall,
       FRONT12, REAR12,
       '12th gen Intel Core (Wall Street Canyon). Front: 2 x USB 3.2 Gen 2 Type-A, 3.5 mm headset jack, power button. Back: 12-20 V DC '
       'jack, 2 x HDMI 2.0b, 2.5GbE (Intel I225), USB 3.2 Gen 2 Type-A, USB 2.0 Type-A, 2 x Thunderbolt 4 (USB-C; not on Lite models). '
       '90 W 19 V (i3) or 120 W 20 V (i5/i7) adapter.', 'Intel NUC12WS Technical Product Specification',
       'https://www.intel.com/content/dam/support/us/en/documents/intel-nuc/NUC12WS_TechProdSpec.pdf', powerW=120)
    IN(f'nuc11tn{s.lower()}', f'NUC11TN{s}', f'NUC 11 Pro kit, {"tall" if tall else "slim"} (NUC11TN{s})', 'NUC 11 Pro', tall,
       [UA(2, 'USB 3.2 Gen 2', 'front')],
       [TB(1, 4), g('rear', 'io', 'USB', 'USB-C', 1, 'Thunderbolt 3'), UA(1, 'USB 3.2 Gen 2'), UA(1, 'USB 2.0'), HD(2, 'HDMI 2.0b'),
        LAN(1, '2.5GbE'), DCIN()],
       '11th gen Intel Core (Tiger Canyon). Front: 2 x USB 3.2 Gen 2 Type-A, power button. Back: 1 x Thunderbolt 4 and 1 x Thunderbolt 3 '
       '(USB-C), 2 x HDMI 2.0b, 2.5GbE, 19 V DC. Check: rear USB-A count (the product brief lists both one and three USB 2.0 ports).',
       'Simply NUC NUC11TN product brief', 'https://simplynuc.com/wp-content/uploads/briefs/SimplyNUCProductBrief-11TNHi5.pdf',
       verified=False)

# ======================= ASUS NUC =======================
AS = lambda *a, **k: nuc('asus.json', 'asus-', 'ASUS', *a, **k)
FRONT14 = [UC(1, 'USB 3.2 Gen 2x2'), UA(2, 'USB 3.2 Gen 2', 'front')]
def rear14(dp): return [TB(2, 4), UA(1, 'USB 3.2 Gen 2'), UA(1, 'USB 2.0'), HD(2, 'HDMI 2.1'), LAN(1, '2.5GbE'), DCIN()]
for tall in (True, False):
    s = 'H' if tall else 'K'
    AS(f'nuc15cr{s.lower()}', f'NUC15CR{s}', f'NUC 15 Pro, {"tall" if tall else "slim"} (NUC15CR{s})', 'NUC 15 Pro', tall,
       FRONT14, rear14('2.1'),
       'Intel Core Ultra 200H (Arrow Lake). Front: USB 3.2 Gen 2x2 Type-C, 2 x USB 3.2 Gen 2 Type-A. Back: 2 x HDMI 2.1, 2 x Thunderbolt 4 '
       '(DisplayPort 2.1, USB4), USB 3.2 Gen 2 Type-A, USB 2.0 Type-A, 2.5GbE (Intel I226), DC in. 120 W 19 V adapter (90 W for Core 3).',
       'ASUS NUC 15 Pro tech specs', 'https://www.asus.com/us/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-15-pro/techspec/',
       hmm=None if tall else 36.8, powerW=120)
    AS(f'nuc14rv{s.lower()}', f'NUC14RV{s}', f'NUC 14 Pro, {"tall" if tall else "slim"} (NUC14RV{s})', 'NUC 14 Pro', tall,
       FRONT14, rear14('1.4'),
       'Intel Core Ultra (Meteor Lake). Front: USB 3.2 Gen 2x2 Type-C, 2 x USB 3.2 Gen 2 Type-A. Back: 2 x Thunderbolt 4 (USB-C with '
       'DisplayPort 1.4), USB 3.2 Gen 2 Type-A, USB 2.0 Type-A, 2 x HDMI 2.1, 2.5GbE (Intel I226), DC in. 90 W or 120 W 19 V adapter.',
       'ASUS NUC 14 Pro tech specs', 'https://asus.com/displays-desktops/nucs/nuc-mini-pcs/asus-nuc-14-pro/techspec', powerW=120)
AS('nuc14rvs', 'NUC14RVS', 'NUC 14 Pro+ (NUC14RVS)', 'NUC 14 Pro+', False, FRONT14, rear14('2.1'),
   'Intel Core Ultra (Meteor Lake), aluminium tool-less chassis. Front: USB 3.2 Gen 2x2 Type-C, 2 x USB 3.2 Gen 2 Type-A. Back: 2 x '
   'Thunderbolt 4 (USB-C with DisplayPort 2.1), USB 3.2 Gen 2 Type-A, USB 2.0 Type-A, 2 x HDMI 2.1, 2.5GbE (Intel I226), DC in. 150 W 19.5 V '
   '(Core Ultra 9) or 120 W 19 V adapter.', 'ASUS NUC 14 Pro+ datasheet',
   'https://dlcdnwebimgs.asus.com/files/media/4c4cc2ec-f3e9-4d35-b413-29c8524857a3/asus-nuc-14-pro-plus-datasheet.pdf',
   w=4, wmm=144, hmm=41, ff='NUC Pro+', powerW=150)

# ======================= Rack kits that carry them =======================
SON = lambda *a, **k: add('sonnet.json', 'sonnet-', 'Sonnet Technologies', *a, **k)
SON('rack-min-3x', 'RACK-MIN-3X', 'RackMac mini (2024+) 2U enclosure for 3 Mac mini', 'RackMac', 'shelf', 2, [],
    '2U steel enclosure, 483 x 131 mm deep (5.2 in mounting depth), 2.7 kg. Holds one to three Mac mini (2024 and later) side by side. '
    'Each bay has a front power button that presses the Mac\'s underside button; front and rear openings reach all the Macs\' ports; '
    'space under each Mac for a 4 x 4 x 0.5 in USB SSD. Add each Mac mini as its own device.',
    'Sonnet RackMac mini (2024+) dealer listing (Adorama)', 'https://www.adorama.com/snrackmin3x.html',
    carrier={'bays': 3, 'fits': ['Mac mini (2024+)']})
SON('rack-min-2xa', 'RACK-MIN-2XA', 'RackMac mini (2018-2023) 1U enclosure for 2 Mac mini', 'RackMac', 'shelf', 1, [],
    '1U steel enclosure, 483 x 216 mm (8.25 in mounting depth), 3 kg. Holds two Mac mini (2011 to 2023, Intel, M1 and M2) side by side. '
    'Front: a power button and a USB 3 port for each Mac; open back with cable tie points. Add each Mac mini as its own device.',
    'Sonnet RackMac mini (2018) dealer listing (B&H)',
    'https://www.bhphotovideo.com/c/product/1449876-REG/sonnet_rack_min_2xa_rackmac_mini_rackmount_enclosure.html',
    carrier={'bays': 2, 'fits': ['Mac mini (2018-2023)']})
SON('rack-std-2x', 'RACK-STD-2X', 'RackMac Studio 3U enclosure for 1 or 2 Mac Studio', 'RackMac', 'shelf', 3, [],
    '3U steel enclosure, 9.5 in (241 mm) mounting depth. Holds one or two Mac Studio. Removable front panel with a power button for each '
    'Mac, pass-through USB-A ports, and access to the Macs\' front ports and SD slots; open back. Space under each Mac for up to three '
    'Thunderbolt or USB SSDs. Add each Mac Studio as its own device.', 'Sonnet RackMac Studio product page',
    'https://www.sonnetstore.com/products/rackmac-studio', carrier={'bays': 2, 'fits': ['Mac Studio']})

PE = lambda *a, **k: add('pennelcom.json', 'pennelcom-', 'Penn Elcom', *a, **k)
PE('r1498-3uk-macstudio', 'R1498/3UK-MACSTUDIO', '3U vented rack shelf with magnetic faceplate for 1 Mac Studio', 'R1498', 'shelf', 3, [],
   '3U vented 2 mm steel shelf, 366 mm deep, 3.6 kg, 38 kg load. CNC-cut magnetic faceplate for one Mac Studio and an R1288/CBK clamp bar. '
   'Lift the faceplate off to reach the Mac\'s power button. Add the Mac Studio as its own device.',
   'Penn Elcom product page', 'https://penn-elcom.com/es_en/3u-vented-rack-shelf-with-cnc-cut-magnetic-faceplates-for-1-x-mac-studio',
   carrier={'bays': 1, 'fits': ['Mac Studio']})
PE('r1498-2uk-macmini', 'R1498/2UK-MACMINI', '2U vented rack shelf with magnetic faceplate for 1 Mac mini', 'R1498', 'shelf', 2, [],
   '2U vented steel shelf with a CNC-cut magnetic faceplate for one Mac mini. Add the Mac mini as its own device. '
   'Check: full part number (listed as R1498/2UK-MACMINI13) and which Mac mini generation the faceplate is cut for.',
   'Penn Elcom product listing', 'https://www.penn-elcom.com/es/estanteria-con-ventilacion-2u-con-placa-frontal-magnetica-para-1x-mac-mini-r1498-2uk-mac-mini-13',
   verified=False, carrier={'bays': 1, 'fits': ['Mac mini (2024+)', 'Mac mini (2018-2023)']})

ME = lambda *a, **k: add('myelectronics.json', 'myelectronics-', 'MyElectronics', *a, **k)
MEU = 'https://www.myelectronics.nl/us/'
ME('6514', '6514', '19" 1U rack mount for 1-3 slim NUCs', 'NUC rack mounts', 'shelf', 1, [],
   '1U, three bays for slim (K) 4 x 4 in NUCs: NUC 7 to NUC 15 Pro. Three blanked openings on the front for optional LAN, USB, USB-C, '
   'HDMI, DisplayPort or audio feed-through inserts; blank covers for empty bays sold separately. Add each NUC as its own device.',
   'MyElectronics product page', MEU + 'nuc-minipc-19-rackmount-kit-1-3-nucs.html',
   carrier={'bays': 3, 'fits': ['NUC 4x4 slim']})
ME('6534', '6534', '19" 1.5U rack mount for 1-3 tall NUCs', 'NUC rack mounts', 'shelf', 2, [],
   '1.5U (shown as 2RU), three bays for tall (H) 4 x 4 in NUCs: NUC 8 to NUC 15 Pro. Three blanked openings on the front for optional '
   'connector inserts. Add each NUC as its own device.', 'MyElectronics product page', MEU + 'nuc-minipc-15u-19-rackmount-kit.html',
   carrier={'bays': 3, 'fits': ['NUC 4x4 tall', 'NUC 4x4 slim']})
ME('6547', '6547', '19" 3U rack for 1-8 NUCs (expandable to 12)', 'NUC rack mounts', 'shelf', 3, [],
   '3U, 8 mounting plates for tall (H) NUCs, or up to 12 slim (K) NUCs with 4 extra plates; tall and slim can be mixed. NUC 10 to NUC 13 Pro, '
   'NUC 14 and NUC 15 Pro (not NUC 15 Pro+). Optional front LAN, USB 3.0 and HDMI inserts. Add each NUC as its own device.',
   'MyElectronics product page', MEU + 'nuc-minipc-19-3u-rackmount-kit-for-1-12-nucs.html',
   carrier={'bays': 12, 'fits': ['NUC 4x4 tall', 'NUC 4x4 slim']})
ME('nuc-pro-plus-1u', '1U NUC Essential/Pro/Pro+', '19" 1U rack mount for 1-3 NUC Essential, Pro or Pro+', 'NUC rack mounts', 'shelf', 1, [],
   '1U, three bays for ASUS NUC Essential, Pro and Pro+ units. Add each NUC as its own device. Check: article number and which heights fit.',
   'MyElectronics NUC rack mounts list', MEU + '19-inch-1u-rack-mount-for-13-nuc-essential-pro-pro.html', verified=False,
   carrier={'bays': 3, 'fits': ['NUC 4x4 slim', 'NUC Pro+ slim']})

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
