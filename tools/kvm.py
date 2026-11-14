#!/usr/bin/env python3
"""Generates catalogue/ihse.json: IHSE draco KVM equipment. Added 2026-11-14.

- draco tera compact, flex and enterprise KVM matrix switches (category router). Their I/O ports carry IHSE's own
  KVM link over Cat X (RJ45, type 'KVM link') or fibre (LC in SFP cages). These links are not Ethernet and never go
  through a network switch.
- draco vario chassis (474-BODY...) as card frames with system 'draco vario', and the draco vario / ultra extender
  modules (CPU units L4xx, CON units R4xx, upgrade boards) as cards. Every module takes one slot. All of a module's
  connectors are on the chassis' interface side, which the app draws as the rear (the cable side): each card has one
  included rear module holding its connectors.

Part numbers: L = CPU unit (at the computer), R = CON unit (at the console). The last letter of the module code is
the link: C = Cat X, S = single-mode fibre, X = 3.125 Gbit/s single-mode fibre; a trailing R adds a redundant link
port. Sources are the IHSE manuals and datasheets hosted by the UK distributor (each entry's source); verified=False
and a 'Check:' note mark what those documents leave open."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
def F(*a): return g('front', *a)
FILES = {}
def add(file, pre, mfr, id, pn, name, fam, cat, ru, ports, notes, src, url, verified=True, w=12, full=False, **kw):
    m = dict(id=pre + id, manufacturer=mfr, partNumber=pn, name=name, family=fam, category=cat,
             ru=ru, widthCols=w, fullDepth=full, verified=verified, source=src, productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); FILES.setdefault(file, []).append(m); return m

IH = lambda *a, **k: add('ihse.json', 'ihse-', 'IHSE', *a, **k)
SD = 'https://www.scene-double.co.uk/downloads/'
COMPACT_MAN = SD + 'draco-tera-compact-manual-29.pdf'
FLEX_DS = SD + 'draco-tera-flex-datasheet-175.pdf'
ENT_DS = 'https://www.eps-dc.com/wp-content/uploads/2020/06/EPS_KVM_Draco_Tera_Enterprise_KVM_Matrixswitche_Datenblatt.pdf'
CHASSIS_DS = SD + 'draco-vario-modular-chassis-121.pdf'
DVI_MAN = SD + 'draco-vario-dvi-manual-47.pdf'
DP_MAN = SD + 'draco-vario-display-port-manual-53.pdf'
HDMI_DS = SD + 'draco-vario-hdmi-datasheet-49.pdf'
DP12_DS = SD + 'draco-ultra-displayport-1.2-datasheet-122.pdf'
HDMI20_DS = SD + 'draco-ultra-hdmi-2.0-datasheet-133.pdf'

KVM = 'KVM link'
LINK_NOTE = ('Ports are IHSE KVM links: Cat X (RJ45, up to 140 m, 100 m for 3G) or fibre (LC, multi-mode up to 1 km, '
             'single-mode up to 10 km). They are not Ethernet: patch them straight to the extenders, never through a network switch. '
             'Any port can take a CPU unit (computer) or a CON unit (console).')
def cat_x(n, prefix='Port', face='front'): return g(face, 'io', KVM, 'RJ45', n, prefix)
def fibre(n, prefix='Port', face='front'): return g(face, 'io', 'Fibre', 'LC (SFP)', n, prefix)

# ======================= draco tera compact (480 series) =======================
# Manual: I/O ports on the front in groups of 16, plus a serial RJ45 and a network RJ45; on the back two power inlets
# (standard and redundant) and a ground stud. 64 and 80 port models are 2RU; 16 to 48 port models 1RU.
COMPACT_GONE = 'IHSE has replaced the 16 to 80 port compact models with draco tera flex; the 8-port compact stays as an entry-level model. '
COMPACT_KIND = {'C': ('Cat X', cat_x), 'F': ('fibre', fibre), 'X': ('3G (2.5 Gbit/s) fibre', fibre)}
for n in (16, 32, 48, 64, 80):
    for k, (kind, fn) in COMPACT_KIND.items():
        IH(f'k480-{n}{k.lower()}', f'K480-{n}{k}', f'draco tera compact {n}-port KVM matrix ({kind}, discontinued)', 'draco tera compact', 'router',
           2 if n >= 64 else 1,
           [fn(n), F('io', 'RS-232', 'RJ45', 1, 'Serial'), F('io', 'Ethernet', 'RJ45', 1, 'Network'),
            R('in', 'Power', 'IEC', 2, 'AC In')],
           f'{n} {kind} I/O ports on the front in {(n + 15) // 16} group{"s" if n > 16 else ""} of 16, serial and network RJ45 '
           'on the front; standard and redundant power inlets and a ground stud on the back. ' + COMPACT_GONE + LINK_NOTE +
           (' 2RU (per the distributor).' if n >= 64 else ' Check: 1RU height and the power inlet type (the manual does not say).'),
           'IHSE draco tera compact manual (480 series)', COMPACT_MAN, verified=n >= 64 or k == 'C')
for pn, ncat, nfib, kind in [('K480-48C16F', 48, 16, 'fibre'), ('K480-48C32F', 48, 32, 'fibre'), ('K480-48C32U', 48, 32, 'universal fibre')]:
    IH(pn.lower(), pn, f'draco tera compact {ncat + nfib}-port KVM matrix ({ncat} Cat X + {nfib} {kind}, discontinued)', 'draco tera compact', 'router', 2,
       [cat_x(ncat, 'Cat X port'), fibre(nfib, 'Fibre port'), F('io', 'RS-232', 'RJ45', 1, 'Serial'), F('io', 'Ethernet', 'RJ45', 1, 'Network'),
        R('in', 'Power', 'IEC', 2, 'AC In')],
       f'{ncat} Cat X ports and {nfib} {kind} ports (SFP) on the front, numbered 1-{ncat} and {ncat + 1}-{ncat + nfib} on the unit; '
       'serial and network RJ45 on the front; standard and redundant power inlets and a ground stud on the back. ' + COMPACT_GONE + LINK_NOTE +
       ' Check: 2RU height and the power inlet type.', 'IHSE draco tera compact manual (480 series)', COMPACT_MAN, verified=False)
for k, kind, fn in [('C', 'Cat X', cat_x), ('F', 'fibre', fibre), ('XV', '3G fibre', fibre), ('U', 'universal fibre', fibre)]:
    IH(f'k480-8{k.lower()}', f'K480-8{k}', f'draco tera compact 8-port KVM matrix ({kind})', 'draco tera compact', 'router', 1,
       [fn(8), F('io', 'RS-232', 'RJ45', 1, 'Serial'), F('io', 'Ethernet', 'RJ45', 1, 'Network'), F('in', 'Power', 'DC barrel', 1, '5V DC In')],
       f'Small 8-port matrix: 8 {kind} I/O ports, serial and network RJ45 and the power input all on one face. Redundant power is an '
       f'option. The same matrix comes as board B480-8{k} for a draco vario chassis. ' + LINK_NOTE +
       ' Check: housing width, power input type and the rack kit.', 'IHSE draco tera compact manual (480 series)', COMPACT_MAN,
       verified=False, w=6)

# ======================= draco tera flex (480 series, modular 8-port I/O boards) =======================
# Datasheet: 1RU 16/24/40 ports (44 x 442 x 449 mm, 7.7 kg, 100-240 V 3 A), 2RU 40-80 ports (90 mm, 11 kg, 4 A),
# 4RU 120-160 ports (177 mm, 19 kg, 5.8 A). Integrated dual PSU, 2 x RJ45 Gigabit Ethernet (redundant network).
FLEX_RU = lambda n: 1 if n <= 40 else 2 if n <= 80 else 4
FLEX_SIZE = {1: ('44 x 442 x 449 mm', 7.7, '3 A'), 2: ('90 x 442 x 449 mm', 11, '4 A'), 4: ('177 x 442 x 449 mm', 19, '5.8 A')}
def flex(pn, name, ports, n, extra='', ru=None, verified=True):
    ru = ru or FLEX_RU(n); size, kg, amps = FLEX_SIZE[ru]
    IH(pn.lower(), pn, name, 'draco tera flex', 'router', ru,
       ports + [F('io', 'Ethernet', 'RJ45', 2, 'Network'), R('in', 'Power', 'IEC C14', 2, 'AC In')],
       f'{ru}RU, {size} (H x W x D), about {kg} kg. Front: I/O ports in groups of 8, 2 x RJ45 Gigabit Ethernet (redundant network) '
       f'and a reset button. Back: two switched IEC C14 inlets, standard and redundant (dual integrated supplies, 100-240 V {amps}), and a ground stud. '
       f'Mounting brackets included. Built from 8-port I/O boards (F480-C8 Cat X, F480-CX8 Cat X 3G, F480-F8 fibre, F480-FX8 fibre 3G), so '
       f'boards can be swapped later. {extra}' + LINK_NOTE,
       'IHSE draco tera flex datasheet and manual', FLEX_DS, verified=verified, full=True, weightKg=kg)
FLEX_KIND = {'C': ('Cat X', cat_x), 'CX': ('Cat X 3G', cat_x), 'F': ('fibre', fibre), 'FX': ('fibre 3G', fibre)}
for n in (16, 24, 32, 40, 48, 64, 80, 120, 128, 144, 160):
    for k, (kind, fn) in FLEX_KIND.items():
        flex(f'K480-{k}{n}', f'draco tera flex {n}-port KVM matrix ({kind})', [fn(n)], n,
             '3G models carry 4K60 (Cat X XV up to 100 m). ' if 'X' in k else '')
for c, f_ in [(24, 16), (24, 40), (40, 24), (40, 40), (80, 40), (120, 40), (80, 80)]:
    for g3 in (False, True):
        ck, fk = ('CX', 'FX') if g3 else ('C', 'F')
        flex(f'K480-{ck}{c}{fk}{f_}', f'draco tera flex {c + f_}-port KVM matrix ({c} Cat X + {f_} fibre{", 3G" if g3 else ""})',
             [cat_x(c, 'Cat X port'), fibre(f_, 'Fibre port')], c + f_, 'Cat X ports are numbered first on the unit. ')
for k, kind, fn in [('C', 'Cat X', cat_x), ('F', 'fibre', fibre)]:
    flex(f'K480-{k}32G', f'draco tera flex 32-port KVM matrix with grid ({kind})', [fn(32), F('io', 'Fibre', 'SFP+', 1, 'Grid')], 32,
         'Grid version: a 10G fibre grid port (F480-G board) links it into a larger draco tera system. ')
    for ru in (2, 4):
        flex(f'K480-{k}32G-{ru}RU', f'draco tera flex 32-port KVM matrix with grid ({kind}), {ru}RU expandable', [fn(32), F('io', 'Fibre', 'SFP+', 1, 'Grid')],
             32, f'Custom-design starter kit with grid: a {ru}RU chassis with 32 ports and a 10G grid port, expandable to {80 if ru == 2 else 160} ports. ',
             ru=ru, verified=False)
for ru in (2, 4):
    for pn, name, ports in [('C40', '40 Cat X', [cat_x(40)]), ('F40', '40 fibre', [fibre(40)]), ('CX40', '40 Cat X 3G', [cat_x(40)]),
                            ('FX40', '40 fibre 3G', [fibre(40)]), ('C24F16', '24 Cat X + 16 fibre', [cat_x(24, 'Cat X port'), fibre(16, 'Fibre port')]),
                            ('CX24FX16', '24 Cat X + 16 fibre, 3G', [cat_x(24, 'Cat X port'), fibre(16, 'Fibre port')])]:
        flex(f'K480-{pn}-{ru}RU', f'draco tera flex {ru}RU expandable KVM matrix, {name} ports', ports, 40,
             f'Custom-design starter kit: a {ru}RU chassis fitted with 40 ports, expandable in the field to {80 if ru == 2 else 160} ports with '
             '8-port I/O boards. ', ru=ru, verified=False)
for k, kind, fn in [('C', 'Cat X', cat_x), ('F', 'fibre', fibre)]:
    IH(f'k480-{k.lower()}8', f'K480-{k}8', f'draco tera flex 8-port KVM matrix ({kind})', 'draco tera flex', 'router', 1,
       [fn(8), F('io', 'RS-232', 'RJ45', 1, 'Serial'), F('io', 'Ethernet', 'RJ45', 1, 'Network'), F('in', 'Power', 'DC barrel', 1, '5V DC In')],
       f'Entry-level 8-port matrix ({kind}), the small unit that carries on from the 8-port draco tera compact. ' + LINK_NOTE +
       ' Check: housing width, faces, power input and rack kit (taken from the 8-port compact).', 'IHSE draco tera flex product page',
       'https://www.ihse.com/apac/products/draco-tera-flex/', verified=False, w=6)

# ======================= draco tera enterprise (480 series) =======================
# EPS datasheet: height, controller cards and power supplies per model. Ports are Cat X or fibre in any mix on 8-port I/O boards.
for pn, n, ru, ctrl, psu, dims, amps in [
        ('K480-048-R1', 48, 3, '1 controller card', 1, '483 x 133 x 230', '5 A'),
        ('K480-080-R1', 80, 4, '1 controller card', 1, '483 x 178 x 230', '5 A'),
        ('K480-152-R1', 152, 9, '1 controller card (second one optional, automatic failover)', 2, '483 x 400 x 330', '9 A'),
        ('K480-160-R1', 160, 9, '1 controller card', 1, '483 x 400 x 330', '9 A'),
        ('K480-288-R1', 288, 13, '1 controller card', 1, '483 x 578 x 330', '12 A'),
        ('K480-576-R1', 576, 25, '2 controller cards', 2, '450 x 1108 x 435', '20 A'),
        ('K480-576S-R1', 576, 25, '2 controller cards', 2, '450 x 1108 x 435', '20 A')]:
    split = pn.startswith('K480-576S')
    io = [g('front', 'in', KVM, 'RJ45', 288, 'In'), g('front', 'out', KVM, 'RJ45', 288, 'Out')] if split else [cat_x(n)]
    IH(pn.lower(), pn, f'draco tera enterprise {n}-port KVM matrix' + (' (288 in / 288 out)' if split else ''), 'draco tera enterprise',
       'router', ru, io + [F('io', 'Ethernet', 'RJ45', 2, 'Network (controller)'), R('in', 'Power', 'IEC', psu, 'AC In')],
       f'{ru}RU, {dims} mm (W x H x D), {ctrl}, {psu} power suppl{"ies" if psu > 1 else "y"} (100-240 V {amps}). '
       + ('Fixed split: ports 1-288 are inputs (CPU side), 289-576 outputs (CON side). ' if split else
          'Ports sit on 8-port I/O boards and can be Cat X or fibre in any mix; shown here as Cat X, so change fibre boards in the editor. ')
       + LINK_NOTE + ' Check: power inlet type and face, and the controller network ports.',
       'IHSE draco tera enterprise datasheet (EPS)', ENT_DS, verified=False, full=ru >= 9)

# ======================= draco vario chassis (474 series) as card frames =======================
VARIO = 'draco vario'
CH_NOTE = (' Every draco vario / ultra module (CPU unit, CON unit, USB, audio, serial or SNMP board) takes one slot. IHSE calls the '
           'module side the interface side; the app draws it as the rear because that is where the cables go, so the front view '
           'shows the closed side and which module sits in each slot. Power cords are IEC C13, 2 m.')
def vario(id, pn, name, ru, slots, ports, notes, w=12, cols=3, orient='h', depth=None, verified=True, fam='draco vario chassis'):
    m = IH(id, pn, name, fam, 'frame', ru, ports, notes + CH_NOTE, 'IHSE draco vario modular chassis datasheet and 474 series manual',
           CHASSIS_DS, verified=verified, w=w, full=bool(depth and depth > 300))
    fr = dict(system=VARIO, slots=slots, slotOrder='ltr', rearAlign=1, door=False, orient=orient,
              controller='None: each module works on its own. An SNMP board (474-SNMP) or 474-CONTROL reports status.',
              front={'x0': 0.06, 'x1': 0.94, 'y0': 0.08, 'y1': 0.92}, rear={'x0': 0.06, 'x1': 0.94, 'y0': 0.08, 'y1': 0.92})
    if orient == 'h': fr['cols'] = cols
    m['frame'] = fr
    return m
AC = lambda n=1, face='rear', label='AC In': g(face, 'in', 'Power', 'IEC C14', n, label)
DC5 = lambda n=1, label='5V DC In', face='rear': g(face, 'in', 'Power', 'DC barrel', n, label)
SLOT_ORDER = ' The manual numbers slots from bottom left to top right; the app counts up each column from the bottom. Check: slot order.'
vario('474-body6r', '474-BODY6R-R1', 'draco vario 6-slot 1RU chassis (rack ears 474-6RMK)', 1, 6, [AC(), DC5(1, '5V DC In (redundant PSU)')],
      '1RU, 442 x 147 x 41 mm (W x D x H), 6 module slots in two rows of three, internal power supply (100-240 V, 8 A at 5 V) and a '
      'DC input for an optional external redundant supply, both on the interface side. Rack ears: 474-6RMK.' + SLOT_ORDER)
vario('474-body6bp', '474-BODY6BP', 'draco vario 6-slot 1RU chassis with backplane, rear PSUs (rack ears 474-6RMK)', 1, 6, [AC(2, 'front', 'AC In (PSU)')],
      '1RU, 442 x 250 x 41 mm, 6 hot-swappable module slots on an active backplane, two internal power supplies (8 A at 5 V) on the '
      'side opposite the modules (drawn as the front here). Optional fan 474-6FAN; -S and -SNMP versions exist. Rack ears: 474-6RMK (19 in, 1RU).' + SLOT_ORDER)
vario('474-body6bpf', '474-BODY6BPF', 'draco vario 6-slot 1RU chassis with backplane, front PSUs (rack ears 474-6RMK)', 1, 6, [AC(2, 'rear', 'AC In (PSU)')],
      '1RU, 442 x 250 x 41 mm, 6 hot-swappable module slots on an active backplane, two internal power supplies on the interface side '
      'next to the modules. Optional fan 474-6FAN. Rack ears: 474-6RMK (19 in, 1RU).' + SLOT_ORDER)
vario('474-body21-4u', '474-BODY21/4U-R1', 'draco vario 21-slot 4RU chassis', 4, 21, [AC(1, 'front', 'AC In (PSU)')],
      '4RU, 482 x 462 x 176 mm (W x D x H), 21 hot-swappable module slots standing upright, numbered 1-21 from the left, on an active '
      'backplane. One internal power supply (32 A at 5 V) on the side opposite the modules (drawn as the front here), with room for a '
      'second (474-BODY21/4UR-R1 has both).', orient='v', depth=462)
vario('474-body21-4ur', '474-BODY21/4UR-R1', 'draco vario 21-slot 4RU chassis, redundant PSUs', 4, 21, [AC(2, 'front', 'AC In (PSU)')],
      '4RU, 482 x 462 x 176 mm (W x D x H), 21 hot-swappable module slots standing upright, numbered 1-21 from the left, on an active '
      'backplane. Two internal power supplies on the side opposite the modules (drawn as the front here).', orient='v', depth=462)
for v in (12, 24, 48):
    vario(f'474-body6dc-{v}', f'474-BODY6DC-{v}', f'draco vario 6-slot 1RU chassis, {v} V DC supply (rack ears 474-6RMK)', 1, 6,
          [R('in', 'Power', 'Terminal block', 1, f'{v}V DC In'), DC5(1, '5V DC In (redundant PSU)')],
          f'1RU, 442 x 250 x 41 mm, 6 module slots in two rows of three, integrated {v} V DC power supply, set up for a redundant supply. '
          'For vehicles, ships and DC plant rooms.' + SLOT_ORDER + ' Check: DC input connector.', verified=False)
vario('474-body2bpf', '474-BODY2BPF', 'draco vario 2-slot chassis with backplane', 1, 2, [AC(), DC5(1, '5V DC In (redundant PSU, locking)')],
      'Two module slots one above the other on an active backplane, integrated power supply and a lockable input for an external '
      'redundant supply. -S and -SNMP versions exist. Check: size (assumed as 474-BODY2N) and rack kit.', w=6, cols=1, verified=False)
vario('474-body2n', '474-BODY2N', 'draco vario 2-slot chassis, internal PSU', 1, 2, [AC(), DC5(1, '5V DC In (redundant PSU)')],
      '221 x 147 x 41 mm, two module slots one above the other, internal power supply and a DC input for an optional external '
      'redundant supply. Rack kit 474-2NRMK; also stands on a desk or shelf.', w=6, cols=1)
m2nr = vario('474-body2n-2nrmk', '474-BODY2N + 474-2NRMK', 'draco vario 2-slot chassis, internal PSU, on 474-2NRMK 19 in 1RU rack ears', 1, 2,
      [AC(), DC5(1, '5V DC In (redundant PSU)')],
      'A 474-BODY2N (221 x 147 x 41 mm, two module slots one above the other, internal power supply, DC input for an optional external '
      'redundant supply) fitted with 474-2NRMK, IHSE\'s 19 in rack mount ears for the 2-slot chassis with built-in PSU. Fills a full 1RU '
      'width; the chassis sits in the middle. Use plain 474-BODY2N for a desk or shelf.', cols=1)
for fc in ('front', 'rear'):   # chassis 221 mm centred between 19 in ears
    m2nr['frame'][fc] = {'x0': 0.298, 'x1': 0.702, 'y0': 0.08, 'y1': 0.92}
vario('474-body2r', '474-BODY2R', 'draco vario 2-slot chassis, external PSU', 1, 2, [DC5(2)],
      '145 x 147 x 41 mm, two module slots one above the other, powered by an external 5 V supply (474-PSU2) with a second DC input for a '
      'redundant one. Rack kit 474-2RMK; also stands on a desk or shelf.', w=4, cols=1)
vario('474-body4r', '474-BODY4R', 'draco vario 4-slot chassis, external PSU', 1, 4, [DC5(2)],
      '293 x 147 x 41 mm, four module slots in two rows of two, powered by an external 5 V supply (474-PSU4) with a second DC input for '
      'a redundant one. Rack kit 474-4RMK; also stands on a desk or shelf.' + SLOT_ORDER, w=8, cols=2)

# ======================= draco vario / ultra modules as cards =======================
def module(pn, name, fam, ports, notes, src, url, watts, verified=True, slots=1):
    m = IH(pn.lower(), pn, name, fam, 'card', 0, [], notes, src, url, verified=verified, w=0)
    m['card'] = dict(fits=[VARIO], slotWidth=slots, watts=watts)
    m['rearModules'] = [dict(partNumber=pn, name='Module connectors', width=slots, cardsPerModule=1, cardOffset=0, default=True,
                             portGroups=ports, included=True)]
    return m
def link(code, n):
    if code == 'C': return R('io', KVM, 'RJ45', n, 'Link')
    return R('io', 'Fibre', 'LC', n, 'Link')
LINKS = {'C': 'Cat X', 'S': 'single-mode fibre', 'X': '3.125G single-mode fibre'}
SVC = R('io', 'USB', 'Mini-USB', 1, 'Service')
def hid(cpu): return R('in', 'USB', 'USB-B', 1, 'USB-HID (to computer)') if cpu else R('io', 'USB', 'USB-A', 2, 'USB-HID (keyboard, mouse)')
UNIT = {True: ('L', 'CPU unit'), False: ('R', 'CON unit')}
HID_CHECK = ' Check: USB-HID connector types and counts (the manual shows one USB-HID position per unit).'

def extender(series, code, vname, vtype, vconn, fam, src, url, links=('C', 'S', 'X'), red=(False, True), verified=True, extra=''):
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        for lk in links:
            for r in red:
                pn = f'{lr}{series}-{code}{lk}{"R" if r else ""}'
                video = R('in' if cpu else 'out', vtype, vconn, 1, f'{vname} {"In (from computer)" if cpu else "Out (to monitor)"}')
                module(pn, f'draco vario {vname} {unit} ({LINKS[lk]}{", redundant link" if r else ""})', fam,
                       [video, hid(cpu), link(lk, 2 if r else 1), SVC],
                       f'{unit[:3].upper()} unit module, single head: 1 x {vname}, USB-HID, {"two link ports (redundant)" if r else "one link port"} '
                       f'over {LINKS[lk]} ({"RJ45, up to 140 m" if lk == "C" else "LC, up to 10 km"}), mini-USB service port. Pairs with an '
                       f'{"R" if cpu else "L"}{series} unit or a draco tera matrix port. Draws up to {"1,050" if r else "800"} mA at 5 V from the chassis. '
                       f'{extra}Options (USB 2.0, audio, serial, PS/2) are separate one-slot boards next to it.' + HID_CHECK,
                       src, url, 5.25 if r else 4, verified=verified)

extender('474', 'BSH', 'DVI-D', 'DVI', 'DVI-D', 'draco vario DVI (474)', 'IHSE draco vario DVI manual (474 series)', DVI_MAN,
         extra='DVI single link, up to 1920 x 1200. ')
extender('474', 'BVH', 'DVI-I', 'DVI', 'DVI-I', 'draco vario DVI (474)', 'IHSE draco vario DVI manual (474 series)', DVI_MAN,
         links=('C',), red=(False,), extra='DVI-I single link (also takes analog VGA through an adapter). ')
extender('483', 'BPH', 'DisplayPort', 'DisplayPort', 'DisplayPort', 'draco vario DisplayPort (483)',
         'IHSE draco vario DisplayPort manual (483 series)', DP_MAN,
         extra='DisplayPort 1.1 with embedded audio, up to 2560 x 2048 at 60 Hz or 3840 x 2160 at 30 Hz. ')
extender('481', 'BHH', 'HDMI', 'HDMI', 'HDMI', 'draco vario HDMI (481)', 'IHSE draco vario HDMI datasheet (481 series)', HDMI_DS,
         red=(False,), verified=False, extra='HDMI with embedded audio, up to 1920 x 1200 at 60 Hz. Check: redundant-link versions. ')
extender('490', 'BPH', 'DisplayPort 1.2', 'DisplayPort', 'DisplayPort', 'draco ultra DisplayPort 1.2 (490)',
         'IHSE draco ultra DisplayPort 1.2 datasheet', DP12_DS, links=('X',), verified=False,
         extra='draco ultra: DisplayPort 1.2, 4K DCI / UHD at 60 Hz (30 bit), single-mode XV fibre up to 5 km. ')
for cpu in (True, False):
    lr, unit = UNIT[cpu]
    for lk, pn_tail in (('X', 'BHHXL'), ('X', 'BHHXLR'), ('C', 'BHHCXL' if cpu else 'BHHCX'), ('C', 'BHHCXLR' if cpu else 'BHHCXR')):
        r = pn_tail.endswith('R')
        pn = f'{lr}495-{pn_tail}'
        module(pn, f'draco ultra HDMI 2.0 {unit} ({"Cat X 3G" if lk == "C" else "single-mode XV fibre"}{", redundant link" if r else ""})',
               'draco ultra HDMI 2.0 (495)',
               [R('in' if cpu else 'out', 'HDMI', 'HDMI', 1, 'HDMI In (from computer)' if cpu else 'HDMI Out (to monitor)'), hid(cpu),
                link('C' if lk == 'C' else 'X', 2 if r else 1), SVC,
                R('out' if cpu else 'in', 'HDMI', 'Micro-HDMI', 1, 'Local HDMI Out' if cpu else 'Local HDMI In')],
               f'draco ultra HDMI 2.0 {unit}: UHD / 4K DCI at 60 Hz (30 bit), {"Cat X XV up to 100 m" if lk == "C" else "single-mode XV fibre up to 5 km"}, '
               f'{"two link ports (redundant)" if r else "one link port"}, Micro-HDMI local {"output" if cpu else "input"}. Part numbers as the '
               'datasheet lists them. Check: connector counts and the meaning of the L suffix.' + HID_CHECK,
               'IHSE draco ultra HDMI 2.0 datasheet (495 series)', HDMI20_DS, 5.25 if r else 4, verified=False)

# Upgrade boards: one slot each, next to the extender module they extend (same link)
for code, desc, cpu_ports, con_ports, ma in [
        ('BXH', '2 x USB-HID', [R('in', 'USB', 'USB-B', 1, 'USB-HID (to computer)')], [R('io', 'USB', 'USB-A', 2, 'USB-HID')], 300),
        ('BXE', 'USB 2.0', [R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')], [R('io', 'USB', 'USB-A', 1, 'USB 2.0')], 2500),
        ('BXE2', 'USB 2.0, two CON ports', [R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')], [R('io', 'USB', 'USB-A', 2, 'USB 2.0')], 2500),
        ('BAX', 'analog audio and RS-232', [R('in', 'Analog audio', '3.5mm jack', 1, 'Audio In'), R('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'),
                                             R('io', 'RS-232', 'D-sub 9', 1, 'RS-232')], None, 300),
        ('BSX', 'analog audio and RS-422', [R('in', 'Analog audio', '3.5mm jack', 1, 'Audio In'), R('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out'),
                                             R('io', 'RS-422', 'D-sub 9', 1, 'RS-422')], None, 150),
        ('BDX', 'digital audio, one way', [R('in', 'AES/EBU', 'Mini-XLR', 1, 'AES/EBU In'), R('in', 'Other', 'RCA', 1, 'S/PDIF In'),
                                            R('in', 'Other', 'TOSLINK', 1, 'S/PDIF optical In')],
         [R('out', 'AES/EBU', 'Mini-XLR', 1, 'AES/EBU Out'), R('out', 'Other', 'RCA', 1, 'S/PDIF Out'), R('out', 'Other', 'TOSLINK', 1, 'S/PDIF optical Out')], 300)]:
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        module(f'{lr}474-{code}', f'draco vario {desc} upgrade board ({unit})', 'draco vario upgrade boards',
               cpu_ports if cpu or con_ports is None else con_ports,
               f'One-slot upgrade board for the {unit} side of any draco vario / ultra extender (474, 481, 483, 490-495): {desc}. It travels '
               f'over the extender\'s own link, so it sits in the slot next to its extender module. Draws up to {ma:,} mA at 5 V.',
               'IHSE draco vario DVI and DisplayPort manuals', DP_MAN, round(ma * 5 / 1000, 2))
# draco SIRA CPU (L488): thin client + KVM transmitter in a vario module (IHSE draco SIRA CPU datasheet 159)
SIRA_DS = SD + 'draco-sira-cpu-datasheet-159.pdf'
for pn, lk, r in (('L488-BIPC-R1', 'C', False), ('L488-BIPCR', 'C', True), ('L488-BIPS', 'S', False), ('L488-BIPSR', 'S', True)):
    module(pn, f'draco SIRA CPU module ({"Cat X" if lk == "C" else "single-mode fibre"} 1G{", redundant link" if r else ""})', 'draco SIRA',
           [R('io', 'Ethernet', 'RJ45', 1, 'Network (TCP/IP, RDP/VNC/SSH/HTML5)'), link(lk, 2 if r else 1), SVC],
           'Thin client and KVM transmitter in one draco vario module: it opens remote sessions (RDP, RemoteFX, SSH, VNC, HTML5 kiosk) '
           'over its network port and sends them into the draco matrix or to a CON unit over its link port. USB 2.0 and 2-channel audio '
           'are embedded. Draws 3.0-3.5 A at 5 V from the chassis, so it needs a ventilated chassis (one with a backplane such as '
           '474-BODY6BPF, or a 474-MODFAN fan). 129 x 40 x 145 mm, 300 g: twice the 20 mm thickness of a normal module, so it '
           'takes two slots (in a 1RU chassis, both rows of one column: start it in an odd slot). ' +
           ('Invoice part number L488-BIPC-R1 is revision 1 of L488-BIPC. ' if pn == 'L488-BIPC-R1' else ''),
           'IHSE draco SIRA CPU datasheet', SIRA_DS, 17.5, slots=2)

module('474-SNMP', 'draco vario SNMP monitoring board', 'draco vario upgrade boards', [R('io', 'Ethernet', 'RJ45', 1, 'Network (SNMP)')],
       'One-slot board that reports the chassis\' power supplies and modules over SNMP. Not used in -SNMP chassis, which have it built in.',
       'IHSE draco vario DVI manual (474 series)', DVI_MAN, 1.5, verified=False)

# ======================= more draco products (gap check against the IHSE 2024 catalogue, 2026-11-14) =======================
CAT24 = SD + 'ihse-complete-product-catalogue-116.pdf'
CAT24_SRC = 'IHSE complete product catalogue (2024)'
LINKS.update({'CX': 'Cat X 3G', 'SX': '3G single-mode fibre'})
def link(code, n):   # Cat X codes (C, CX) are RJ45, the rest LC fibre
    if code.startswith('C'): return R('io', KVM, 'RJ45', n, 'Link')
    return R('io', 'Fibre', 'LC', n, 'Link')
LINK_TXT = {'C': 'RJ45, up to 140 m', 'CX': 'RJ45, up to 100 m', 'S': 'LC, up to 10 km', 'X': 'LC, up to 10 km', 'SX': 'LC, up to 10 km'}
HAVE = lambda pn: any(m['id'] == 'ihse-' + pn.lower() for m in FILES['ihse.json'])
def vio(cpu, t, c, n=1, what=None):   # main video port: input on a CPU unit, output on a CON unit
    w = what or c
    return R('in' if cpu else 'out', t, c, n, f'{w} In (from computer)' if cpu else f'{w} Out (to monitor)')
def loc(cpu, t, c, what=None):        # local port: monitor out on a CPU unit, local computer in on a CON unit
    w = what or c
    return R('out' if cpu else 'in', t, c, 1, f'Local {w} Out (local monitor)' if cpu else f'Local {w} In (local computer)')
OPTN = {'L': 'local video', 'W': 'local KVM switch', 'M': 'MST'}

def family(fam, desc, pn_fn, video, src, url, ma, links=('C', 'S', 'X'), red=(False, True), opts=None, verified=False,
           extra='', usb=True, slots=1, units=(True, False), svc=SVC, pairs=None):
    """CPU and CON modules for every link / option / redundancy. pn_fn(lr, lk, o, r) gives the part number;
    video(cpu, o) gives the video ports; opts maps cpu True/False to the option letters ('' = plain)."""
    opts = opts or {True: ('',), False: ('',)}
    for cpu in units:
        lr, unit = UNIT[cpu]
        for lk in links:
            for o in opts[cpu]:
                for r in red:
                    pn = pn_fn(lr, lk, o, r)
                    if not pn or HAVE(pn): continue
                    on = OPTN.get(o, '')
                    mA = ma[1 if r else 0] if isinstance(ma, tuple) else ma
                    module(pn, f'{desc} {unit} ({LINKS[lk]}{", " + on if on else ""}{", redundant link" if r else ""})', fam,
                           video(cpu, o) + ([hid(cpu)] if usb else []) + [link(lk, 2 if r else 1)] + ([svc] if svc else []),
                           f'{unit} module. {extra}{"Two link ports (redundant)" if r else "One link port"} over {LINKS[lk]} '
                           f'({LINK_TXT[lk]}). Pairs with {pairs or "the matching " + ("CON" if cpu else "CPU") + " unit"} or a draco tera '
                           f'matrix port. Draws up to {mA:,} mA at 5 V from the chassis. Options (USB 2.0, audio, serial) are separate '
                           f'one-slot boards next to it.' + ('' if verified else ' Check: connector types and counts.'),
                           src, url, round(mA * 5 / 1000, 2), verified=verified, slots=slots)

# --- 474 DVI-I: redundant and fibre versions, and the DVI-I/VGA CPU units of the DVI-D range
family('draco vario DVI (474)', 'draco vario DVI-I', lambda lr, lk, o, r: f'{lr}474-BVH{lk}{"R" if r else ""}',
       lambda cpu, o: [vio(cpu, 'DVI', 'DVI-I' if cpu else 'DVI-D', what='DVI-I' if cpu else 'DVI')],
       CAT24_SRC, CAT24, (800, 1050), links=('C', 'S'), verified=True,
       extra='DVI-I single link up to 1920 x 1200; the CPU unit also takes analog VGA through an adapter. ')
family('draco vario DVI (474)', 'draco vario DVI-I/VGA', lambda lr, lk, o, r: f'L474-BSH{lk}V', lambda cpu, o: [vio(cpu, 'DVI', 'DVI-I')],
       CAT24_SRC, CAT24, 800, red=(False,), units=(True,),
       extra='DVI-I input that takes DVI-D or analog VGA; pairs with any 474 DVI-D CON unit. ')

# --- 481 HDMI Full HD: redundant, local-video (CPU, L) and local-switch (CON, W) versions
def hdmi_fhd(cpu, o):
    p = [vio(cpu, 'HDMI', 'HDMI')]
    if o == 'L': p.append(loc(True, 'HDMI', 'HDMI'))
    if o == 'W': p += [loc(False, 'HDMI', 'HDMI'), R('in', 'USB', 'USB-B', 1, 'Local USB-HID (to local computer)')]
    return p
FHD_EXTRA = ('HDMI with embedded audio, up to 1920 x 1200 at 60 Hz. L versions add a local HDMI monitor output on the CPU unit; '
             'W versions add a switchable local HDMI + USB input on the CON unit (local KVM switch). ')
for s, fam, desc in (('481', 'draco vario HDMI (481)', 'draco vario HDMI'), ('491', 'draco ultra HDMI 1.3 (491)', 'draco ultra HDMI 1.3')):
    family(fam, desc, lambda lr, lk, o, r, s=s: f'{lr}{s}-BHH{lk}{o}{"R" if r else ""}', hdmi_fhd, CAT24_SRC, CAT24, (800, 1050),
           links=('C', 'S'), opts={True: ('', 'L'), False: ('', 'W')}, verified=(s == '481'), extra=FHD_EXTRA)
# --- 481 / 491 HDMI 4K30 with local video
for s, fam, desc in (('481', 'draco vario HDMI 4K (481)', 'draco vario HDMI 4K30'), ('491', 'draco ultra HDMI 1.4 4K (491)', 'draco ultra HDMI 1.4 4K30')):
    family(fam, desc, lambda lr, lk, o, r, s=s: f'{lr}{s}-BUH{lk}L{"R" if r else ""}',
           lambda cpu, o: [vio(cpu, 'HDMI', 'HDMI'), loc(cpu, 'HDMI', 'HDMI')], CAT24_SRC, CAT24, 1990,
           opts={True: ('',), False: ('',)}, extra='HDMI 1.4 up to 3840 x 2160 at 30 Hz, with a local HDMI output (CPU unit) or '
           'switchable local HDMI input (CON unit). ')

# --- 482 / 492 DVI dual link and dual head (DMS-59 on the module, adapter cables included)
for s, fam, ult in (('482', 'draco vario DVI dual link / dual head (482)', ''), ('492', 'draco ultra DVI dual link / dual head (492)', 'ultra ')):
    for code, n, what, ex in (('BDH', 1, 'DVI-D Dual Link', 'DVI-D dual link, 2560 x 2048 at 60 Hz or 4096 x 2160 at 30 Hz. '),
                              ('B2H', 2, 'DVI-D', 'dual head: two DVI-D single link, each up to 1920 x 1200. ')):
        family(fam, f'draco {"vario " if not ult else "vario ultra "}DVI {"dual link" if code == "BDH" else "dual head"}',
               lambda lr, lk, o, r, s=s, code=code: f'{lr}{s}-{code}{lk}{"R" if r else ""}{"-R1" if lr == "R" else ""}',
               lambda cpu, o, n=n, what=what: [R('in' if cpu else 'out', 'DVI', 'DVI-D', n,
                                                  f'{what} {"In" if cpu else "Out"} (on the DMS-59 adapter)')],
               'IHSE draco vario dual link / dual head and draco ultra datasheets', SD + 'draco-ultra-dual-head-dual-link-datasheet-125.pdf',
               1600, extra=f'{ex}The module has one DMS-59 socket; the supplied adapter breaks it out to DVI-D. ')

# --- 483 / 493 DisplayPort 1.1 dual head (DP + Mini DP)
for s, fam, desc, ds in (('483', 'draco vario DisplayPort dual head (483)', 'draco vario DP 1.1 dual head', 'draco-vario-displayport-1.1-dh-datasheet-173.pdf'),
                         ('493', 'draco ultra DisplayPort dual head (493)', 'draco vario ultra DP 1.1 dual head', 'draco-vario-ultra-displayport-1.1-dh-datasheet-174.pdf')):
    family(fam, desc, lambda lr, lk, o, r, s=s: f'{lr}{s}-B2H{lk}{"R" if r else ""}',
           lambda cpu, o: [vio(cpu, 'DisplayPort', 'DisplayPort', what='DisplayPort 1.1 (primary)'),
                           vio(cpu, 'DisplayPort', 'Mini DisplayPort', what='Mini DisplayPort 1.1 (secondary)')],
           'IHSE ' + desc + ' datasheet', SD + ds, 1600, verified=True,
           extra='DisplayPort 1.1 with embedded audio: one head up to 4096 x 2160 at 30 Hz, or two heads at 1920 x 1200 at 60 Hz. ')

# --- 486 / 496 SDI (HD-BNC in SFP cages; no USB on the base module)
for s, fam, desc, links, ver in (('486', 'draco vario SDI (486)', 'draco vario SDI', ('C', 'S', 'X'), True),
                                 ('496', 'draco ultra SDI (496)', 'draco vario ultra SDI', ('C', 'S'), False)):
    family(fam, desc, lambda lr, lk, o, r, s=s: f'{lr}{s}-BSD{lk}{"R" if r else ""}',
           lambda cpu, o: [vio(cpu, '3G-SDI', 'HD-BNC', what='SDI')], 'IHSE draco vario SDI manual (486 series)',
           SD + 'draco-vario-sdi-manual-142.pdf', 800, links=links, usb=False, verified=ver,
           extra='One SDI signal (SD, HD and 3G level A/B, with 2-channel embedded audio) on an HD-BNC SFP. SFP options: 459-PLB '
                 '(CPU, re-clocked loop-through) and 459-DTX (CON, two outputs); 459-BMB is a BNC to HD-BNC adapter cable. Up to '
                 '1,500 mA with SFPs fitted. USB-HID comes from an L/R474-BXH board. ')

# --- 490 DisplayPort 1.2: local-video (XL) and MST versions
family('draco ultra DisplayPort 1.2 (490)', 'draco ultra DP 1.2 4K60', lambda lr, lk, o, r: f'{lr}490-BPH{lk}L{"R" if r else ""}',
       lambda cpu, o: [vio(cpu, 'DisplayPort', 'DisplayPort', what='DisplayPort 1.2'), loc(cpu, 'DisplayPort', 'DisplayPort')],
       CAT24_SRC, CAT24, (800, 1050), links=('CX', 'X'), opts={True: ('L',), False: ('L',)},
       extra='DisplayPort 1.2, 4K at 60 Hz, with a local DisplayPort output (CPU unit) or input (CON unit). ')
family('draco ultra DisplayPort 1.2 (490)', 'draco ultra DP 1.2 MST', lambda lr, lk, o, r: f'{lr}490-BPH{lk}{"R" if r else ""}-M',
       lambda cpu, o: [vio(cpu, 'DisplayPort', 'DisplayPort', 1 if cpu else 2, what='DisplayPort 1.2 (MST)')],
       CAT24_SRC, CAT24, (800, 1050), links=('CX', 'X'), opts={True: ('M',), False: ('M',)},
       extra='DisplayPort 1.2 multi-stream: two 4K30 heads from one DP output, split to two monitors at the CON unit. ')

# --- draco vario XS (JPEG XS): DisplayPort 1.2 (490 ...-XS) and HDMI 2.0 (495 ...-XS)
XS_LINKS = {'C': 'C', 'S': 'S', 'X': 'X'}
family('draco vario XS DisplayPort 1.2', 'draco vario XS DP 1.2', lambda lr, lk, o, r: f'{lr}490-BPH{lk}{o}{"R" if r else ""}-XS',
       lambda cpu, o: [vio(cpu, 'DisplayPort', 'DisplayPort', what='DisplayPort 1.2')] + ([loc(cpu, 'DisplayPort', 'DisplayPort')] if o else []),
       'IHSE draco vario XS DisplayPort 1.2 datasheet', SD + 'draco-vario-xs-displayport-1.2-233.pdf', 1600,
       opts={True: ('', 'L'), False: ('', 'L')},
       extra='JPEG XS compression: 4K60 (up to 5K) over a 1G or 3G link. L versions add a local DisplayPort. ')
family('draco vario XS HDMI 2.0', 'draco vario XS HDMI 2.0', lambda lr, lk, o, r: f'{lr}495-BHH{lk}L{"R" if r else ""}-XS',
       lambda cpu, o: [vio(cpu, 'HDMI', 'HDMI', what='HDMI 2.0'), loc(cpu, 'HDMI', 'Micro-HDMI')],
       'IHSE draco vario XS HDMI 2.0 datasheet', 'https://scene-double.co.uk/downloads/draco-vario-xs-hdmi-2.0-datasheet-234.pdf', 1600,
       extra='JPEG XS compression: HDMI 2.0 4K60 (up to 5K) over a 1G or 3G link, with a Micro-HDMI local output (CPU) or switchable '
             'local input (CON). ')

# --- 489 / 499 USB-C CPU units (video and USB from one USB-C cable)
for s, fam, desc in (('489', 'draco vario USB-C (489)', 'draco vario USB-C'), ('499', 'draco ultra USB-C (499)', 'draco vario ultra USB-C')):
    family(fam, desc, lambda lr, lk, o, r, s=s: f'L{s}-BCHE2{lk}{"R" if r else ""}',
           lambda cpu, o: [R('in', 'USB', 'USB-C', 1, 'USB-C In (video, USB-HID and USB 2.0 from the computer)')],
           CAT24_SRC, CAT24, 1600, usb=False, units=(True,), pairs='a DisplayPort CON unit',
           extra='Takes video (DisplayPort alt mode), keyboard/mouse and embedded USB 2.0 from a laptop over one USB-C cable. '
                 'IHSE lists CPU units only. ')

# --- draco vario XStreme DisplayPort (8 resolution/head versions, x audio, audio + USB 2.0)
XSTREME_DS = SD + 'draco-vario-xstreme-displayport-datasheet-258.pdf'
XSTREME = [('SH', 'SL', '1G', 'single head up to 1920 x 1200'), ('SH', 'DL', '1G', 'single head up to 4K30'),
           ('SH', '4K', '1G', 'single head up to 4K60'), ('SH', '4K', '3G', 'single head up to 4K60'),
           ('SH', '8K', '3G', 'single head up to 8K30 (announced)'), ('DH', 'SL', '1G', 'dual head up to 1920 x 1200'),
           ('DH', 'DL', '1G', 'dual head up to 4K30'), ('DH', '4K', '3G', 'dual head up to 4K60')]
USB_V = {'A': 'audio', 'AU2': 'audio + USB 2.0 (2 x USB-A)', 'AU4': 'audio + USB 2.0 (4 x USB-A)'}
for cpu in (True, False):
    lr, unit = UNIT[cpu]
    for head, res, gb, rdesc in XSTREME:
        for base in ('C', 'S'):
            lk = base + ('X' if gb == '3G' else '')
            for usbv in (('A', 'AU2') if cpu else ('A', 'AU2', 'AU4')):
                for r in (False, True):
                    pn = f'{lr}-DP{head}-{res}-{usbv}-{lk}{"R" if r else ""}'
                    n = 2 if head == 'DH' else 1
                    ports = [vio(cpu, 'DisplayPort', 'Mini DisplayPort', n, what='Mini DisplayPort (locking)')]
                    if head == 'SH': ports.append(loc(cpu, 'DisplayPort', 'DisplayPort', 'DisplayPort 1.2' if cpu else 'DisplayPort 1.2 (notebook)'))
                    if cpu: ports.append(R('in', 'USB', 'USB-B', 1, 'USB-HID / USB 2.0 (to computer)' if usbv != 'A' else 'USB-HID (to computer)'))
                    else: ports.append(R('io', 'USB', 'USB-A', 4 if usbv == 'AU4' else 2, 'USB-HID / USB 2.0' if usbv != 'A' else 'USB-HID (keyboard, mouse)'))
                    ports += [R('in' if cpu else 'out', 'Analog audio', '3.5mm jack', 1, 'Audio In (analog / TOSLINK)' if cpu else 'Audio Out (analog / TOSLINK)'),
                              link(lk, 2 if r else 1), R('io', 'USB', 'USB-C', 1, 'Service')]
                    module(pn, f'draco vario XStreme DP {unit}, {rdesc}, {USB_V[usbv]} ({LINKS[lk]}{", redundant link" if r else ""})',
                           'draco vario XStreme DisplayPort', ports,
                           f'{unit} module of the draco vario XStreme range (JPEG XS): {rdesc} over a {gb} link, {"two link ports (redundant)" if r else "one link port"} '
                           f'over {LINKS[lk]} ({LINK_TXT[lk]}). Locking Mini DisplayPort, 8-channel embedded audio plus analog / TOSLINK on a 3.5 mm '
                           'jack, USB-C service port. XS-REDUPG-C/-CX/-S/-SX licences add link redundancy later. Check: slot count, power draw '
                           '(assumed 1,600 mA like other DP modules) and connector counts.', 'IHSE draco vario XStreme DisplayPort datasheet',
                           XSTREME_DS, 8, verified=False)

# --- IP Gateway CON modules (a CON unit that reaches a draco tera matrix over an IP network)
for pn, lk, r, vid, ma, ds in [(f'IP-R481-BUH{lk}L{"R" if r else ""}', lk, r, 'HDMI', 1990, 'draco-tera-ip-gateway-hdmi-con-datasheet-224.pdf')
                               for lk in ('C', 'S') for r in (False, True)] + \
                              [(f'IP-R483-B2H{lk}{"R" if r else ""}', lk, r, 'DP', 1600, 'draco-tera-ip-gateway-dp-con-datasheet-225.pdf')
                               for lk in ('C', 'S') for r in (False, True)]:
    net = R('io', 'Ethernet', 'RJ45', 2 if r else 1, 'Network (1G, to IP switch)') if lk == 'C' else \
          R('io', 'Fibre', 'LC (SFP)', 2 if r else 1, 'Network (1G single-mode, to IP switch)')
    video = ([R('out', 'HDMI', 'HDMI', 1, 'HDMI Out (to monitor)'), R('in', 'HDMI', 'HDMI', 1, 'Local HDMI In (local computer)')] if vid == 'HDMI' else
             [R('out', 'DisplayPort', 'DisplayPort', 1, 'DisplayPort 1.1 Out (primary)'), R('out', 'DisplayPort', 'Mini DisplayPort', 1, 'Mini DisplayPort 1.1 Out (secondary)')])
    module(pn, f'draco tera IP Gateway CON module, {"HDMI 4K30" if vid == "HDMI" else "DisplayPort dual head"} '
               f'({"Cat X" if lk == "C" else "single-mode fibre"} 1G{", redundant" if r else ""})', 'draco tera IP Gateway CON',
           video + [hid(False), net, SVC],
           f'CON unit that reaches a draco tera matrix through a draco tera IP Gateway over a standard IP network (not a direct KVM link): '
           f'{"HDMI up to 4K30 with a local HDMI input" if vid == "HDMI" else "DisplayPort 1.1, one head up to 4K30 or two at 1920 x 1080"}, '
           f'USB-HID, {"Cat X up to 100 m" if lk == "C" else "single-mode fibre up to 10 km"} to the network switch. Draws up to {ma:,} mA '
           '(5 V) from the chassis; 20 x 129 x 143 mm. Check: network connector (RJ45 / SFP) and USB-A count.',
           'IHSE draco tera IP Gateway CON datasheet', SD + ds, round(ma * 5 / 1000, 2), verified=False)

# --- draco SIRA CON (2-slot module) and SIRA stand-alone
SIRA_CON_DS = SD + 'draco-sira-con-datasheet-166.pdf'
for pn, lk, r in (('R488-BIPC', 'C', False), ('R488-BIPCR', 'C', True), ('R488-BIPS', 'S', False), ('R488-BIPSR', 'S', True)):
    module(pn, f'draco SIRA CON module ({"Cat X" if lk == "C" else "single-mode fibre"}{", redundant link" if r else ""})', 'draco SIRA',
           [R('out', 'HDMI', 'HDMI', 1, 'HDMI 1.4 Out (local access, up to 4K30)'), R('io', 'USB', 'USB-A', 2, 'USB (keyboard, mouse, service)'),
            R('io', 'Ethernet', 'RJ45', 1, 'Network (1G, remote IP access)'), link(lk, 2 if r else 1), SVC],
           'Remote IP access gateway into a draco tera matrix: it shows up as a CON port on the matrix and lets remote users (HTML5, '
           'draco CON App) reach matrix computers over the network, with a local HDMI + USB console. 40 x 129 x 145 mm, about 240 g, so '
           'it takes two slots (start it in an odd slot in a 1RU chassis). Draws 2,200 mA at 5 V from the chassis.',
           'IHSE draco SIRA CON datasheet', SIRA_CON_DS, 11, slots=2)
module('R488-BIPHHL', 'draco SIRA stand-alone module (HDMI, USB)', 'draco SIRA',
       [R('in', 'HDMI', 'HDMI', 1, 'HDMI In (from computer)'), R('in', 'USB', 'USB-B', 1, 'USB-HID (to computer)'),
        R('out', 'HDMI', 'HDMI', 1, 'Local HDMI Out'), R('io', 'USB', 'USB-A', 2, 'Local USB'),
        R('io', 'Ethernet', 'RJ45', 1, 'Network (1G, remote IP access)'), SVC],
       'SIRA without a matrix: a computer plugs straight into the module (HDMI + USB) and remote users reach it over the network. '
       'Check: connector counts and slot count (assumed two slots like the SIRA CON).', 'IHSE draco SIRA CON datasheet', SIRA_CON_DS,
       11, verified=False, slots=2)

# --- more add-on boards (one slot each, next to their extender)
def aud(cpu, what='Audio'): return [R('in', 'Analog audio', '3.5mm jack', 1, f'{what} In'), R('out', 'Analog audio', '3.5mm jack', 1, f'{what} Out')]
BLOCKS = {
    'A': lambda cpu: aud(cpu) + [R('io', 'RS-232', 'D-sub 9', 1, 'RS-232')],
    'S': lambda cpu: aud(cpu) + [R('io', 'RS-422', 'D-sub 9', 1, 'RS-422')],
    'SS': lambda cpu: aud(cpu, 'Audio 1') + aud(cpu, 'Audio 2') + [R('io', 'RS-422', 'D-sub 9', 1, 'RS-422')],
    'D': lambda cpu: [R('in' if cpu else 'out', t, c, 1, f'{l} {"In" if cpu else "Out"}') for t, c, l in
                      (('AES/EBU', 'Mini-XLR', 'AES/EBU'), ('Other', 'RCA', 'S/PDIF'), ('Other', 'TOSLINK', 'S/PDIF optical'))],
    'DD': lambda cpu: [R(d, t, c, 1, f'{l} {"In" if d == "in" else "Out"}') for d in ('in', 'out') for t, c, l in
                       (('AES/EBU', 'Mini-XLR', 'AES/EBU'), ('Other', 'RCA', 'S/PDIF'), ('Other', 'TOSLINK', 'S/PDIF optical'))],
    'B': lambda cpu: [R('in' if cpu else 'out', 'Analog audio', '6.35mm jack', 2, f'Balanced audio {"In" if cpu else "Out"}')],
    'B2': lambda cpu: [R('in', 'Analog audio', '6.35mm jack', 1, 'Balanced audio In'), R('out', 'Analog audio', '6.35mm jack', 1, 'Balanced audio Out')],
    'E': lambda cpu: [R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')] if cpu else [R('io', 'USB', 'USB-A', 1, 'USB 2.0')],
    'E2': lambda cpu: [R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')] if cpu else [R('io', 'USB', 'USB-A', 2, 'USB 2.0')],
    'H': lambda cpu: [R('in', 'USB', 'USB-B', 1, 'USB-HID (to computer)')] if cpu else [R('io', 'USB', 'USB-A', 2, 'USB-HID')],
    'UC': lambda cpu: ([R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')] if cpu else [R('io', 'USB', 'USB-A', 4, 'USB 2.0')]) + [link('C', 1)],
    'US': lambda cpu: ([R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)')] if cpu else [R('io', 'USB', 'USB-A', 4, 'USB 2.0')]) + [link('S', 1)]}
BLOCK_TXT = {'A': 'analog audio and RS-232 (115 kBd)', 'S': 'analog audio and RS-422', 'SS': '2 x analog audio and RS-422', 'D': 'digital audio, one way',
             'DD': 'digital audio, both ways', 'B': 'balanced analog audio, one way', 'B2': 'balanced (symmetrical) audio', 'E': 'USB 2.0 embedded',
             'E2': 'USB 2.0 embedded, flex speed', 'H': 'USB-HID', 'UC': 'USB 2.0 Hi-Speed on its own Cat X link',
             'US': 'USB 2.0 Hi-Speed on its own fibre link'}
BLOCK_MA = {'A': 300, 'S': 150, 'SS': 300, 'D': 300, 'DD': 400, 'B': 500, 'B2': 500, 'E': 2500, 'E2': 2500, 'H': 300, 'UC': 2500, 'US': 2500}
for code, parts, ver in [('BRX', ['A'], False), ('BBX', ['B'], True), ('BB2X', ['B2'], False), ('BDA', ['D', 'A'], False), ('BSS', ['SS'], False),
                         ('BDD', ['DD'], False), ('BXUC', ['UC'], False), ('BXUS', ['US'], False), ('BAE2', ['A', 'E2'], False),
                         ('BSE2', ['S', 'E2'], False), ('BB2E2', ['B2', 'E2'], False), ('BDE2', ['D', 'E2'], False), ('BRE2', ['A', 'E2'], False),
                         ('BAE', ['A', 'E'], False), ('BSE', ['S', 'E'], False), ('BDE', ['D', 'E'], False), ('BRE', ['A', 'E'], False),
                         ('BAH', ['A', 'H'], False), ('BSH', ['S', 'H'], False), ('BDH', ['D', 'H'], False)]:
    desc = ' + '.join(BLOCK_TXT[p] for p in parts); ma = min(3000, sum(BLOCK_MA[p] for p in parts))
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        module(f'{lr}474-{code}', f'draco vario {desc} upgrade board ({unit})', 'draco vario upgrade boards',
               [p for b in parts for p in BLOCKS[b](cpu)],
               f'One-slot upgrade board for the {unit} side of a draco vario / ultra extender: {desc}. It sits in the slot next to its '
               f'extender module{" and has its own link" if parts[0] in ("UC", "US") else " and travels over the extender\'s link"}. '
               f'Draws up to about {ma:,} mA at 5 V.' + ('' if ver else ' Check: connector types and counts.'),
               CAT24_SRC if not ver else 'IHSE draco vario SDI manual (486 series)', CAT24 if not ver else SD + 'draco-vario-sdi-manual-142.pdf',
               round(ma * 5 / 1000, 2), verified=ver)
module('R474-BGX', 'draco vario 8 x GPIO add-on board (CON unit)', 'draco vario upgrade boards', [R('io', 'GPIO', 'Other', 8, 'GPIO')],
       'CON-side add-on board with 8 GPIOs (buttons, LEDs, tally) next to its CON unit; 476-CTRL-GPIO is the matching accessory. '
       'Check: connector type.', CAT24_SRC, CAT24, 1, verified=False)
module('474-MODFAN', 'draco vario fan module', 'draco vario upgrade boards', [],
       'Fan cartridge in a module slot, for chassis without a backplane fan, e.g. next to a power-hungry SIRA module. Check: power draw.',
       CAT24_SRC, CAT24, 1, verified=False)
module('474-SNMPv3-R1', 'draco vario SNMPv3 monitoring module', 'draco vario upgrade boards', [R('io', 'Ethernet', 'RJ45', 1, 'Network (SNMPv3)')],
       'SNMPv3 module that reports the chassis\' power supplies and modules; slides into slot 5 of 474-BODY6BP / BODY6BPF or slot 21 of '
       '474-BODY21/4U-R1. Current version of 474-SNMP.', CAT24_SRC, CAT24, 1.5, verified=False)

# --- more chassis
EXTPSU = ' External 5 V power supply 474-PSU2 (2-slot) or 474-PSU4 (4-slot).'
VRMK = ' 474-VRMK holds up to three 2-slot chassis, or a 2-slot and a 4-slot chassis, in 1RU.'
vario('474-body2', '474-BODY2', 'draco vario 2-slot chassis, external PSU', 1, 2, [DC5(1)],
      '145 x 147 x 41 mm, two module slots one above the other, one external 5 V supply (no redundant input). Rack ears 474-2RMK.' + EXTPSU + VRMK,
      w=4, cols=1)
vario('474-body4', '474-BODY4', 'draco vario 4-slot chassis, external PSU', 1, 4, [DC5(1)],
      '293 x 147 x 41 mm, four module slots in two rows of two, one external 5 V supply (4,000 mA, no redundant input). Rack ears 474-4RMK.' +
      EXTPSU + VRMK + SLOT_ORDER, w=8, cols=2)
for v in (12, 24, 48):
    vario(f'474-body2dc-{v}', f'474-BODY2DC-{v}', f'draco vario 2-slot chassis, {v} V DC supply', 1, 2,
          [R('in', 'Power', 'Terminal block', 1, f'{v}V DC In'), DC5(1, '5V DC In (redundant PSU)')],
          f'221 x 147 x 41 mm, two module slots one above the other, integrated {v} V DC supply (2,400 mA), set up for a redundant '
          'supply. For vehicles, ships and DC plant rooms. Check: DC input connector and rack ears.', w=6, cols=1, verified=False)
for pn, base, extra_ports, desc in (('474-BODY2BPF-S', '474-body2bpf', [], 'silent fan fitted'),
                                    ('474-BODY2BPF-SNMP', '474-body2bpf', [R('io', 'Ethernet', 'RJ45', 1, 'Network (SNMP)')], 'SNMP monitoring built in'),
                                    ('474-BODY6BPF-S', '474-body6bpf', [], 'silent fan fitted'),
                                    ('474-BODY6BP-SNMP', '474-body6bp', [R('io', 'Ethernet', 'RJ45', 1, 'Network (SNMP)')], 'SNMP monitoring built in')):
    b = next(m for m in FILES['ihse.json'] if m['id'] == 'ihse-' + base)
    m = json.loads(json.dumps(b)); m.update(id='ihse-' + pn.lower(), partNumber=pn, verified=False,
                                            name=b['name'].replace(b['partNumber'], pn) + f', {desc}',
                                            notes=f'{b["partNumber"]} with {desc}. ' + b['notes'] + ' Check: where the network port sits.' * bool(extra_ports))
    m['portGroups'] = b['portGroups'] + extra_ports; m['source'] = CAT24_SRC; m['productUrl'] = CAT24
    FILES['ihse.json'].append(m)
for base, ears, mm in (('474-body2', '474-2RMK', 145), ('474-body2r', '474-2RMK', 145), ('474-body4', '474-4RMK', 293), ('474-body4r', '474-4RMK', 293)):
    b = next(m for m in FILES['ihse.json'] if m['id'] == 'ihse-' + base)
    m = json.loads(json.dumps(b)); f = mm / 482.6
    m.update(id=f'{b["id"]}-{ears.lower().split("-")[1]}', partNumber=f'{b["partNumber"]} + {ears}', widthCols=12, verified=False,
             name=f'{b["name"]}, on {ears} 19 in 1RU rack ears',
             notes=f'A {b["partNumber"]} fitted with {ears}, IHSE\'s 19 in rack mount ears for it. Fills a full 1RU width; the chassis '
                   f'is drawn in the middle. Use plain {b["partNumber"]} for a desk or shelf. ' + b['notes'] + ' Check: chassis position between the ears.')
    for fc in ('front', 'rear'): m['frame'][fc] = {'x0': round(0.5 - f / 2, 3), 'x1': round(0.5 + f / 2, 3), 'y0': 0.08, 'y1': 0.92}
    FILES['ihse.json'].append(m)

# --- draco MultiView 4K60 (1RU, BODY6-size)
MV_DS = SD + 'draco-multi-view-4k60-datasheet-157.pdf'
for pn, vt, vc, head in (('MV42-DPSH', 'DisplayPort', 'DisplayPort', 'SH'), ('MV42-H2SH', 'HDMI', 'HDMI', 'SH'),
                         ('MV42-DPDH', 'DisplayPort', 'DisplayPort', 'DH'), ('MV42-H2DH', 'HDMI', 'HDMI', 'DH')):
    nin, nout = (4, 2) if head == 'SH' else (8, 4)
    IH(pn.lower(), pn, f'draco MultiView 4K60 KVM multiviewer, {"DP 1.2" if vt == "DisplayPort" else "HDMI 2.0"} {"single" if head == "SH" else "dual"} head',
       'draco MultiView', 'switcher', 1,
       [R('in', vt, vc, nin, f'{vt} In (computer)'), R('in', 'USB', 'USB-B', 4, 'USB (computer)'),
        R('out', vt, vc, nout, f'{vt} Out (monitor)'), R('io', 'USB', 'USB-A', 2, 'USB-HID (keyboard, mouse)'),
        R('io', 'USB', 'USB-A', 2, 'USB 2.0'), R('out', 'Analog audio', '3.5mm jack', 1, 'Audio Out (speaker)'),
        R('io', 'GPIO', 'Other', 1, 'GPIO (buttons, LEDs)'), R('in', 'Power', 'IEC C14', 2, 'AC In (redundant PSU)')],
       f'Shows up to four computers ({"single" if head == "SH" else "dual"} head, up to 4K60) at once on {nout} monitor{"s" if nout > 1 else ""} '
       'with one keyboard and mouse that follows the cursor across windows. Built in a 1RU 6-slot draco vario chassis (474-6RMK ears) '
       'or under a desk; redundant power, SNMP. Check: connector counts, USB per computer and power inlets.',
       'IHSE draco MultiView 4K60 datasheet', MV_DS, verified=False)

# --- draco U-Switch (USB KVM switch, 221 mm half-width box)
US_DS = SD + 'draco-u-switch-datasheet-120.pdf'
for pn, ncpu, nhid, u2, desc in (('K476-4U', 4, 2, False, '4 computers, 2 USB-HID devices'), ('K476-4U2', 4, 4, False, '4 computers, 4 USB-HID devices'),
                                 ('K476-8U', 8, 2, False, '8 computers, 2 USB-HID devices'), ('K476-4U4T', 4, 2, True, '4 computers, 2 USB-HID + 2 USB 2.0 devices')):
    ports = [R('in', 'USB', 'USB-B', ncpu, 'USB-HID (computer)'), R('io', 'USB', 'USB-A', nhid, 'USB-HID (keyboard, mouse)')]
    if u2: ports += [R('in', 'USB', 'USB-B', 4, 'USB 2.0 (computer)'), R('io', 'USB', 'USB-A', 2, 'USB 2.0 (devices)')]
    ports += [R('in', 'GPI', 'Other', 1, 'Push buttons / contact closure'), R('in', 'Power', 'IEC C14', 1, 'AC In')]
    IH(pn.lower(), pn, f'draco U-Switch USB KVM switch ({desc})', 'draco U-Switch', 'control', 1, ports,
       f'Switches one keyboard and mouse{" plus USB 2.0 devices" if u2 else ""} between {ncpu} computers by hotkey, mouse move, buttons or '
       'contact closure (video is switched elsewhere). 221 x 147 x 43 mm, internal 90-240 V supply: two fit side by side in 1RU, one sits '
       'on 474-2NRMK ears. Check: connector types and counts.', 'IHSE draco U-Switch datasheet', US_DS, verified=False, w=6,
       boxMm={'w': 221, 'h': 43})

# --- draco compact extenders (477) and their 1RU rack kits (4 units side by side)
CMP_MAN = SD + 'draco-compact-manual-64.pdf'
FF1, FF2 = 'IHSE draco compact (1 board)', 'IHSE draco compact (2 boards)'
CMP = [('1SH', ('C', 'S', 'X'), '', 'DVI single head', 1),
       ('1SE', ('C', 'S', 'X'), 'A', 'DVI single head, USB 2.0, analog audio and RS-232', 2),
       ('1SE', ('C', 'S', 'X'), 'D', 'DVI single head, USB 2.0, digital audio', 2),
       ('1ST', ('C', 'S'), '', 'DVI single head, transparent USB 2.0', 2),
       ('1SH', ('C', 'S', 'X'), 'V', 'DVI-I / VGA single head', 1),
       ('2S4', ('C', 'S', 'X'), '', 'DVI dual head', 2)]
for code, links, sfx, desc, boards in CMP:
    for cpu in (True, False):
        lr, unit = UNIT[cpu]
        for lk in links:
            pn = f'{lr}477-{code}{lk}{sfx}'
            heads = 2 if code == '2S4' else 1
            p = [R('in' if cpu else 'out', 'DVI', 'DVI-I' if (sfx == 'V' and cpu) else 'DVI-D', heads, 'DVI In (from computer)' if cpu else 'DVI Out (to monitor)'),
                 R('in', 'USB', 'USB-B', heads, 'USB-HID (to computer)') if cpu else R('io', 'USB', 'USB-A', 2 * heads, 'USB-HID (keyboard, mouse)')]
            if code in ('1SE', '1ST'):
                p.append(R('in', 'USB', 'USB-B', 1, 'USB 2.0 (to computer)') if cpu else R('io', 'USB', 'USB-A', 4 if code == '1ST' else 2, 'USB 2.0'))
            if sfx == 'A': p += aud(cpu) + [R('io', 'RS-232', 'D-sub 9', 1, 'RS-232')]
            if sfx == 'D': p += BLOCKS['D'](cpu)
            nl = 2 if code in ('2S4', '1ST') else 1
            p += [link(lk, nl), R('io', 'USB', 'Mini-USB', 2 if code == '2S4' else 1, 'Service'), DC5(1, '5V DC In', 'rear')]
            h = 29 if boards == 1 else 43
            IH(pn.lower(), pn, f'draco compact {desc} KVM extender, {unit} ({LINKS[lk] if lk != "X" else "2.5G fibre"})', 'draco compact (477)', 'converter', 1, p,
               f'{unit} of the K477-{code}{lk}{sfx} extender pair: {desc}. Stand-alone box, {103} x 143 x {h} mm, all connectors on one side, '
               'external 5 V supply (260-5G / 477-5G). Four fit side by side in 1RU on a 455-4G (single board units) or 455-8G (all units) '
               'rack kit; leave 0.5RU free above for air.' + (' Check: USB 2.0 port count (the range table says 4, the device view shows 1).' if code == '1ST' else ''),
               'IHSE draco compact manual (477 series)', CMP_MAN, verified=(code != '1ST'), w=3, boxMm={'w': 103, 'h': h},
               formFactor=FF1 if boards == 1 else FF2, powerW=5)
IH('455-4g', '455-4G', 'draco compact 19 in 1RU rack kit for up to 4 single-head units', 'draco compact (477)', 'shelf', 1, [],
   '1RU tray for up to four draco compact (or DVXi) single-board units side by side.', 'IHSE draco compact datasheet',
   SD + 'draco-compact-datasheet-63.pdf', carrier={'bays': 4, 'fits': [FF1]})
IH('455-8g', '455-8G', 'draco compact 19 in 1RU rack kit for up to 4 units', 'draco compact (477)', 'shelf', 1, [],
   '1RU tray for up to four draco compact units of any height, or three units and a 455-PS power supply.', 'IHSE draco compact datasheet',
   SD + 'draco-compact-datasheet-63.pdf', carrier={'bays': 4, 'fits': [FF1, FF2, 'IHSE 455-PS']})
IH('455-ps', '455-PS', 'draco compact rack power supply for up to 3 units', 'draco compact (477)', 'power', 1,
   [R('in', 'Power', 'IEC C14', 1, 'AC In'), R('out', 'Power', 'DC barrel', 3, '5V DC Out')],
   'Power supply that sits in one bay of a 455-8G rack kit and feeds up to three draco compact units. Check: connectors.',
   'IHSE draco compact datasheet', SD + 'draco-compact-datasheet-63.pdf', verified=False, w=3, boxMm={'w': 103, 'h': 43},
   formFactor='IHSE 455-PS')

# 481 3G (X) versions came from the series pattern; IHSE's 2024 catalogue lists none
for m in FILES['ihse.json']:
    if m['id'] in ('ihse-l481-bhhx', 'ihse-r481-bhhx'): m['notes'] += ' Not in IHSE\'s 2024 catalogue, which lists Cat X and single-mode 1G only for 481 Full HD.'

# ======================= Raritan (KVM-over-IP, often next to a draco matrix) =======================
RA = lambda *a, **k: add('raritan.json', 'raritan-', 'Raritan', *a, **k)
RA_DS = 'https://www.raritan.com/assets/ram/resources/data_sheets/dominion-kx-iv-101-datasheet.pdf'
RA('dkx4-101', 'DKX4-101', 'Dominion KX IV-101 single-port 4K KVM-over-IP switch', 'Dominion KX IV', 'control', 1,
   [R('in', 'HDMI', 'HDMI', 1, 'Target HDMI In (locking)'), R('io', 'USB', 'USB-B', 1, 'Target USB (to computer)'),
    F('out', 'HDMI', 'HDMI', 1, 'Local HDMI Out (pass-through)'), F('io', 'USB', 'USB-A', 2, 'Local USB (keyboard, mouse)'),
    R('io', 'Ethernet', 'RJ45', 1, 'LAN (1G)'), R('io', 'RS-232', 'Other', 1, 'Admin serial'),
    R('io', 'GPI', 'Terminal block', 1, 'GPIO (relay out, dry in)'), R('in', 'Power', 'DC locking', 1, 'Power (AC adapter)')],
   'Remote KVM-over-IP access to one computer, up to 4K: HDMI and USB from the computer, a local HDMI + USB pass-through console, '
   '1 GbE, admin serial, a 5-pin terminal block (relay out, dry-contact in, virtual power button). 140 x 144 x 30 mm (W x D x H), '
   '0.65 kg, 100-240 V AC adapter with locking plug, 12.5 W typical, 20 W max. Ships with an L bracket for zero-U mounting; '
   'RACK-KIT-DKX4-101-3 holds three in 1RU. Check: which end each connector is on (drawn as target side = rear).',
   'Raritan Dominion KX IV-101 datasheet', RA_DS, w=4, powerW=20, weightKg=0.65, boxMm={'w': 140, 'h': 30},
   formFactor='Raritan DKX4-101')
RA('rack-kit-dkx4-101-3', 'RACK-KIT-DKX4-101-3', 'Rack kit for three Dominion KX IV-101 (1RU)', 'Dominion KX IV', 'shelf', 1, [],
   '19 in 1RU kit that holds three KX IV-101 units side by side.', 'Raritan Dominion KX IV-101 datasheet', RA_DS,
   carrier={'bays': 3, 'fits': ['Raritan DKX4-101']})

for f, ms in FILES.items():
    ids = [m['id'] for m in ms]; assert len(ids) == len(set(ids)), f
    json.dump(ms, open(os.path.join(CAT, f), 'w'), indent=1)
    print(f, len(ms), 'entries,', sum(m['verified'] for m in ms), 'verified,',
          sum(m['category'] == 'card' for m in ms), 'cards,', sum(m['category'] == 'frame' for m in ms), 'frames')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
for f in FILES:
    if f not in idx: idx.append(f)
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
