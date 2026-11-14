#!/usr/bin/env python3
"""Generates catalogue/kvmtec.json: kvm-tec KVM-over-IP extenders and their rack kits. Added 2026-11-14.

kvm-tec (Austria, owned by IHSE since 2021) makes small KVM extender boxes, 108 mm wide and 43 mm high, that
link over IP (copper RJ45 or fibre SFP), point to point or switched through a Layer 3 network as a matrix.
Four boxes sit side by side in 1RU on kvm-tec's rack kits, so each box carries a formFactor and boxMm and each
kit a 4-bay carrier. Part numbers: L = local unit (at the computer, CPU side), R = remote unit (at the console,
CON side). Sources are kvm-tec datasheets hosted by the UK distributor; verified=False and a 'Check:' note mark
what those documents leave open. Ecosmart (a USB-powered dongle) and the older Smartline / Masterline (SVX, MVX)
boxes are left out."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
MODELS = []
def add(id, pn, name, fam, cat, ports, notes, src, url, verified=True, **kw):
    m = dict(id='kvmtec-' + id, manufacturer='kvm-tec', partNumber=pn, name=name, family=fam, category=cat,
             ru=1, widthCols=kw.pop('w', 3), fullDepth=False, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); MODELS.append(m); return m

SD = 'https://www.scene-double.co.uk/downloads/'
FLEX_DS = SD + 'flexline-datasheet-240.pdf'
FF_FLEX = 'kvm-tec FLEXline (108 mm)'
FF_4K = 'kvm-tec 4K (media4Kconnect / Scalableline)'
BOX = ' Box 108 x 107.5 x 43 mm (W x D x H), 295 g, 12 V DC wall supply. Four fit side by side in 1RU on a KT-6232/6233/6234 rack kit; also DIN rail (KT-6235), VESA (KT-6236) or under a desk (KT-6231).'
NET = ('Links run over IP: point to point, or through a Layer 3 network switch as a matrix with the kvm-tec Switching '
       'Manager (up to 100 or 1,000 endpoints). Embedded stereo audio. ')
def dc(n=1): return R('in', 'Power', 'DC barrel', n, '12V DC In' if n == 1 else '12V DC In (redundant)')
def net(fibre, n, what='Link'):
    return R('io', 'Fibre', 'LC (SFP)', n, f'{what} (fibre SFP)') if fibre else R('io', 'Ethernet', 'RJ45', n, f'{what} (1G)')
def dvi(cpu, n, conn='DVI-D'):
    return R('in' if cpu else 'out', 'DVI', conn, n, 'DVI In (from computer)' if cpu else 'DVI Out (to monitor)')
def usb(cpu): return R('in', 'USB', 'USB-B', 1, 'USB (to computer)') if cpu else R('io', 'USB', 'USB-A', 4, 'USB (keyboard, mouse, devices)')
def audio(cpu):
    return [R('in', 'Analog audio', '3.5mm jack', 1, 'Line In'), R('out', 'Analog audio', '3.5mm jack', 1, 'Line Out' if cpu else 'Headphone / speaker Out')]
RS232 = R('io', 'RS-232', 'RJ12', 1, 'RS-232')
UNIT = {True: ('L', 'local unit (CPU)'), False: ('R', 'remote unit (CON)')}

def flex(base, fam, desc, heads, fibre, src, url, extras, notes, verified, pn_fmt='KT-{base}{lr}'):
    """One local and one remote FLEXline box. extras(cpu) adds audio / serial; masterflex and up have two links and two DC inputs."""
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        pn = pn_fmt.format(base=base, lr=lr)
        smart = fam == 'Smartflex'
        ports = [dvi(cpu, heads, 'DVI-I' if (cpu and not smart) else 'DVI-D')]
        if cpu and smart and heads == 1: ports.append(R('out', 'DVI', 'DVI-D', 1, 'DVI Out (local monitor)'))
        ports += [usb(cpu)] + extras(cpu)
        nl = heads if smart else 2
        ports += [net(fibre, nl, 'Link' if smart and heads == 1 else 'Link 1 / 2'), dc(1 if smart else 2)]
        add(pn.lower().replace('kt-', ''), pn, f'kvm-tec {fam} {desc} extender, {unit}{", fibre" if fibre else ""}', f'kvm-tec FLEXline {fam}',
            'converter', ports, f'{unit[0].upper() + unit[1:]} of the KT-{base} set: {desc}, up to 1920 x 1200 at 60 Hz, USB 2.0. ' + NET + notes + BOX +
            ('' if verified else ' Check: connector counts.'), src, url, verified=verified, powerW=6, weightKg=0.295,
            boxMm={'w': 108, 'h': 43}, formFactor=FF_FLEX)

none = lambda cpu: []
flex('6011', 'Smartflex', 'single head DVI', 1, False, 'kvm-tec Smartflex single head datasheet', SD + 'smartflex-single-head-catx-datasheet-193.pdf',
     none, 'The local unit has a DVI loop-out for a local monitor. Copper only. ', True)
flex('6021', 'Smartflex', 'dual head DVI', 2, False, 'kvm-tec Smartflex dual head datasheet', SD + 'smartflex-dual-head-catx-datasheet-194.pdf',
     none, 'Two RJ45 links, one per head. Copper only. ', False)
for base, heads, fibre, ver in (('6012', 1, False, False), ('6013', 1, True, False), ('6022', 2, False, True), ('6023', 2, True, False)):
    flex(base, 'Masterflex', f'{"single" if heads == 1 else "dual"} head DVI', heads, fibre, 'kvm-tec Masterflex datasheet',
         SD + 'masterflex-dual-head-catx-datasheet-197.pdf' if base == '6022' else FLEX_DS, audio,
         'Redundant link and power: two link ports and two DC inputs. Analog audio both ways; options KT-6041 sound, KT-6042 analog VGA, '
         'KT-6043 USB memory. ', ver)
for base, heads, fibre, ver in (('6014', 1, False, False), ('6016', 1, True, False), ('6024', 2, False, True), ('6026', 2, True, False)):
    flex(base, 'Maxflex', f'{"single" if heads == 1 else "dual"} head DVI', heads, fibre, 'kvm-tec Maxflex datasheet',
         SD + 'maxflex-dual-head-catx-datasheet-205.pdf' if base == '6024' else FLEX_DS, lambda cpu: audio(cpu) + [RS232],
         'Redundant link and power, analog audio both ways, RS-232 on RJ12 (KT-7095/7096 adapters), matrices up to 1,000 endpoints. ', ver)
flex('6016i', 'Industryflex', 'single head DVI (industrial, 55 °C)', 1, True, 'kvm-tec FLEXline datasheet', FLEX_DS,
     lambda cpu: audio(cpu) + [RS232], 'Maxflex rated for 55 °C ambient. ', False, pn_fmt='KT-6016i{lr}')
flex('6016s', 'Maxflex Encrypted', 'single head DVI, encrypted', 1, True, 'kvm-tec FLEXline datasheet', FLEX_DS,
     lambda cpu: audio(cpu) + [RS232], 'Maxflex with encrypted links. ', False, pn_fmt='KT-6016{lr}S')
for base, fibre in (('6031', False), ('6032', True)):
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        add(f'{base}{lr.lower()}', f'KT-{base}{lr}', f'kvm-tec USBflex USB 2.0 extender, {unit}{", fibre" if fibre else ""}', 'kvm-tec FLEXline USBflex',
            'converter', [usb(cpu), net(fibre, 1), dc()],
            f'{unit[0].upper() + unit[1:]} of the KT-{base} set: USB 2.0 up to 480 Mbit/s over IP, point to point or switched. ' + BOX +
            ' Check: connector counts.', 'kvm-tec FLEXline datasheet', FLEX_DS, verified=False, powerW=6, weightKg=0.295,
            boxMm={'w': 108, 'h': 43}, formFactor=FF_FLEX)

# 4K over 10G fibre: media4Kconnect (point to point) and Scalableline (switched)
M4K_DS = SD + 'media4kconnect-datasheet-243.pdf'
SCL_DS = SD + 'scalableline-datasheet-212.pdf'
BOX4K = (' Local box 108 x 107.5 x 43 mm, remote box 109 x 184 x 43 mm (W x D x H), about 0.6 kg, two 12 V / 3 A DC inputs. '
         'Four fit side by side in 1RU on a KT-6237/6238/6239 rack kit.')
for base, fam, desc, nsfp, src, url, ver, note in (
        ('6937', 'media4Kconnect', 'DisplayPort 1.2 4K60', 1, 'kvm-tec media4Kconnect datasheet', M4K_DS, True,
         'One 10G SFP+ link (a second is an option with KT-4023, which also adds uncompressed video and downscaling). '),
        ('6938', 'media4Kconnect PRO', 'DisplayPort 1.2 4K60, redundant, uncompressed', 2, 'kvm-tec media4Kconnect datasheet', M4K_DS, True,
         'Two 10G SFP+ links (redundant), uncompressed video and downscaling included. '),
        ('6990', 'Scalableline 4K', 'DisplayPort 1.2 4K60, switched', 2, 'kvm-tec Scalableline datasheet', SCL_DS, False,
         'Two 10G SFP+ ports; switched through a 10G network as a 4K matrix with the Switching Manager. '),
        ('6991', 'Scalableline 4K PRO', 'DisplayPort 1.2 4K60, switched', 2, 'kvm-tec Scalableline datasheet', SCL_DS, False,
         'Two 10G SFP+ ports; switched through a 10G network as a 4K matrix with the Switching Manager. ')):
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        ports = [R('in', 'DisplayPort', 'DisplayPort', 1, 'DisplayPort In (from computer)') if cpu else
                 R('out', 'DisplayPort', 'DisplayPort', 1, 'DisplayPort 1.2 Out (to monitor)'), usb(cpu)] + audio(cpu) + \
                [RS232, R('io', 'SFP', 'SFP+', nsfp, 'Link (10G SFP+)'), dc(2)]
        add(f'{base}{lr.lower()}', f'KT-{base}{lr}', f'kvm-tec {fam} {desc} extender, {unit}', f'kvm-tec {fam.split()[0]}', 'converter', ports,
            f'{unit[0].upper() + unit[1:]} of the KT-{base} set: {desc}, up to 4096 x 2160 or 5120 x 1440 at 60 Hz, USB 2.0, analog '
            f'audio both ways, RS-232 on RJ12. {note}SFP+ modules: KT-7013 (multi-mode 300 m), KT-7017 (single-mode 10 km), KT-7016 '
            '(Cat X 80 m).' + BOX4K + ('' if ver else ' Check: the datasheet swaps the local/remote labels on its connector table; '
            'drawn here with DP in and USB-B on the local unit.'), src, url, verified=ver, powerW=15,
            boxMm={'w': 108, 'h': 43}, formFactor=FF_4K)

# Rack kits: 1RU, four boxes side by side
for pn, short, desc, ac, fits, src, url in (
        ('KT-6232', 'RMK-FLEX-F', 'with front panel', 0, FF_FLEX, 'kvm-tec Smartflex datasheet', SD + 'smartflex-single-head-catx-datasheet-193.pdf'),
        ('KT-6233', 'RMK-FLEX-FN', 'with front panel and power supply', 1, FF_FLEX, 'kvm-tec Smartflex datasheet', SD + 'smartflex-single-head-catx-datasheet-193.pdf'),
        ('KT-6234', 'RMK-FLEX', 'with front panel and redundant power supply', 2, FF_FLEX, 'kvm-tec Smartflex datasheet', SD + 'smartflex-single-head-catx-datasheet-193.pdf'),
        ('KT-6237', 'RMK-4K-F', 'with front panel', 0, FF_4K, 'kvm-tec media4Kconnect datasheet', M4K_DS),
        ('KT-6238', 'RMK-4K-FN', 'with front panel and power supply', 1, FF_4K, 'kvm-tec media4Kconnect datasheet', M4K_DS),
        ('KT-6239', 'RMK-4K', 'with front panel and redundant power supply', 2, FF_4K, 'kvm-tec media4Kconnect datasheet', M4K_DS)):
    flexkit = fits == FF_FLEX
    ports = [R('in', 'Power', 'IEC C14', ac, 'AC In' if ac == 1 else 'AC In (redundant PSU)'),
             R('out', 'Power', 'DC barrel', 4 * ac, '12V DC Out (to boxes)')] if ac else []
    add(pn.lower().replace('kt-', ''), pn, f'kvm-tec 19 in 1RU rack kit for 4 {"FLEXline" if flexkit else "media4Kconnect / Scalableline"} boxes, {desc}',
        'kvm-tec rack kits', 'shelf', ports,
        f'{short}: 1RU shelf that holds four kvm-tec {"FLEXline (Smartflex, Masterflex, Maxflex, USBflex)" if flexkit else "media4Kconnect or Scalableline 4K"} '
        f'boxes side by side {desc}.' + (' Check: power connectors and how the supply feeds the boxes.' if ac else ''),
        src, url, verified=not ac, w=12, carrier={'bays': 4, 'fits': [fits]})

ids = [m['id'] for m in MODELS]; assert len(ids) == len(set(ids))
json.dump(MODELS, open(os.path.join(CAT, 'kvmtec.json'), 'w'), indent=1)
print('kvmtec.json', len(MODELS), 'entries,', sum(m['verified'] for m in MODELS), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'kvmtec.json' not in idx: idx.append('kvmtec.json')
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
