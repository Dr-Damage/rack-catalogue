#!/usr/bin/env python3
"""Generates catalogue/netgear.json: NETGEAR fully managed switches for AV and IT (M4250 and M4350 'AV Line',
plus the main M4300 models). Added 2026-11-14.

Port and PoE counts come from NETGEAR's knowledge-base tables for the M4250 and M4350 series (each entry's productUrl).
Front-panel ports are drawn on the front; power inlets on the rear. Console, management and USB ports and the
power-supply arrangement are typical for the series and marked with a 'Check:' note."""
import json, os
CAT = os.path.join(os.path.dirname(__file__), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def F(*a): return g('front', *a)
def R(*a): return g('rear', *a)
MODELS = []
def add(sku, name, fam, ports, notes, url, verified=True, ru=1, w=12, **kw):
    m = dict(id='netgear-' + sku.lower(), manufacturer='NETGEAR', partNumber=sku, name=name, family=fam, category='network', ru=ru,
             widthCols=w, fullDepth=False, verified=verified, source=f'NETGEAR {fam} port and PoE table', productUrl=url, notes=notes, portGroups=ports)
    m.update(kw); MODELS.append(m); return m
KB4250 = 'https://kb.netgear.com/000064904/NETGEAR-AV-Line-of-Fully-Managed-Switches-M4250-Series'
KB4350 = 'https://kb.netgear.com/000066110/NETGEAR-AV-and-IT-Managed-Switches-M4350-Series'
def rj(n, speed, poe=''): return F('io', 'Ethernet', 'RJ45', n, f'{speed}{" " + poe if poe else ""}')
def sfp(n, kind):
    conn = {'1G SFP': 'SFP', '2.5G SFP': 'SFP', '10G SFP+': 'SFP+', '25G SFP28': 'SFP28', '100G QSFP28': 'QSFP28'}[kind]
    return F('io', 'SFP', conn, n, kind)
CONSOLE = [F('io', 'RS-232', 'RJ45', 1, 'Console'), F('io', 'USB', 'USB-C', 1, 'USB console'), F('io', 'USB', 'USB-A', 1, 'USB storage')]
OOB = F('io', 'Ethernet', 'RJ45', 1, 'Out-of-band mgmt')

# ---------------- M4250 (AV Line) ----------------
M4250 = [
    # sku, name, [ports], poe budget W, psus, form note, w
    ('GSM4210PD', 'M4250-9G1F-PoE+', [rj(8, '1G', 'PoE+'), rj(1, '1G'), sfp(1, '1G SFP')], 110, 1, 'desktop', 6),
    ('GSM4210PX', 'M4250-8G2XF-PoE+', [rj(8, '1G', 'PoE+'), sfp(2, '10G SFP+')], 220, 1, 'desktop', 6),
    ('GSM4212P', 'M4250-10G2F-PoE+', [rj(8, '1G', 'PoE+'), rj(2, '1G'), sfp(2, '1G SFP')], 125, 1, '1U', 12),
    ('GSM4212PX', 'M4250-10G2XF-PoE+', [rj(8, '1G', 'PoE+'), rj(2, '1G'), sfp(2, '10G SFP+')], 240, 1, '1U', 12),
    ('GSM4212UX', 'M4250-10G2XF-PoE++', [rj(8, '1G', 'PoE++'), rj(2, '1G'), sfp(2, '10G SFP+')], 720, 1, '1U', 12),
    ('GSM4230P', 'M4250-26G4F-PoE+', [rj(24, '1G', 'PoE+'), rj(2, '1G'), sfp(4, '1G SFP')], 300, 1, '1U', 12),
    ('GSM4230PX', 'M4250-26G4XF-PoE+', [rj(24, '1G', 'PoE+'), rj(2, '1G'), sfp(4, '10G SFP+')], 480, 1, '1U', 12),
    ('GSM4230UP', 'M4250-26G4F-PoE++', [rj(24, '1G', 'PoE++'), rj(2, '1G'), sfp(4, '1G SFP')], 1440, 2, '1U', 12),
    ('GSM4248P', 'M4250-40G8F-PoE+', [rj(40, '1G', 'PoE+'), sfp(8, '1G SFP')], 480, 1, '1U', 12),
    ('GSM4248PX', 'M4250-40G8XF-PoE+', [rj(40, '1G', 'PoE+'), sfp(8, '10G SFP+')], 960, 2, '1U', 12),
    ('GSM4248UX', 'M4250-40G8XF-PoE++', [rj(40, '1G', 'PoE++'), sfp(8, '10G SFP+')], 2880, 3, '1U', 12),
    ('MSM4214X', 'M4250-12M2XF', [rj(12, '2.5G'), sfp(2, '10G SFP+')], 0, 1, '1U', 12),
    ('XSM4216F', 'M4250-16XF', [sfp(16, '10G SFP+')], 0, 1, '1U', 12)]
for sku, nm, ports, poe, psus, form, w in M4250:
    power = [R('in', 'Power', 'DC barrel', 1, 'DC In (external adapter)')] if form == 'desktop' else [R('in', 'Power', 'IEC C14', psus, 'AC In' if psus == 1 else 'AC In (PSU)')]
    add(sku, f'{nm} AV Line managed switch ({sku})', 'NETGEAR M4250', ports + CONSOLE[:2] + power,
        f'NETGEAR AV Line switch with the AV user interface and profiles for Dante, AES67, NDI, Q-SYS and AVB/Milan (AVB on selected models). '
        f'{"PoE budget " + format(poe, ",") + " W" + (" with all " + str(psus) + " internal supplies" if psus > 1 else "") + ". " if poe else "No PoE. "}'
        f'{"Desktop half-width unit, fanless; sits on a shelf or a rack tray. " if form == "desktop" else "1U rack mount. "}'
        'Check: console/USB ports and power inlets (typical for the series).', KB4250, verified=True, w=w,
        **({'boxMm': {'w': 216, 'h': 43}} if form == 'desktop' else {}))

# ---------------- M4350 (AV and IT) ----------------
M4350 = [
    ('GSM4328', 'M4350-24G4XF', [rj(24, '1G', 'PoE++'), sfp(4, '10G SFP+')], '648 W, up to 720 W'),
    ('GSM4352', 'M4350-48G4XF', [rj(48, '1G', 'PoE++'), sfp(4, '10G SFP+')], '236 W, up to 1,440 W'),
    ('MSM4352', 'M4350-44M4X4V', [rj(44, '2.5G', 'PoE++'), rj(4, '10G', 'PoE++'), sfp(4, '25G SFP28')], '194 W, up to 3,314 W'),
    ('XSM4316', 'M4350-8X8F', [rj(8, '10G'), sfp(8, '10G SFP+')], ''),
    ('XSM4324', 'M4350-12X12F', [rj(12, '10G'), sfp(12, '10G SFP+')], ''),
    ('XSM4328CV', 'M4350-24X4V', [rj(24, '10G', 'PoE+'), sfp(4, '25G SFP28')], '576 W, up to 720 W'),
    ('XSM4328FV', 'M4350-24F4V', [sfp(24, '10G SFP+'), sfp(4, '25G SFP28')], ''),
    ('XSM4340CV', 'M4350-36X4V', [rj(36, '10G', 'PoE++'), sfp(4, '25G SFP28')], '280 W, up to 1,760 W'),
    ('XSM4340V', 'M4350-24X8F8V', [rj(24, '10G', 'PoE++'), sfp(8, '10G SFP+'), sfp(8, '25G SFP28')], '290 W, up to 1,770 W'),
    ('XSM4340FV', 'M4350-32F8V', [sfp(32, '10G SFP+'), sfp(8, '25G SFP28')], ''),
    ('VSM4320C', 'M4350-16V4C', [sfp(16, '25G SFP28'), sfp(4, '100G QSFP28')], ''),
    ('XSM4344C', 'M4350-40X4C', [rj(40, '10G', 'PoE++'), sfp(4, '100G QSFP28')], '196 W, up to 1,676 W'),
    ('MSM4328F', 'M4350-24F4X', [sfp(24, '2.5G SFP'), rj(4, '10G (combo)'), sfp(4, '10G SFP+')], ''),
    ('MSM4310', 'M4350-8M2V', [rj(8, '2.5G', 'PoE++'), sfp(2, '25G SFP28')], '119 W, up to 551 W'),
    ('MSM4332', 'M4350-24M4X4V', [rj(24, '2.5G', 'PoE++'), rj(4, '10G', 'PoE++'), sfp(4, '25G SFP28')], '522 W, up to 1,972 W (110 V) or 2,520 W (220 V)'),
    ('XSM4344FC', 'M4350-40F4C', [sfp(40, '10G SFP+'), sfp(4, '100G QSFP28')], ''),
    ('MSM4320', 'M4350-16M4V', [rj(8, '2.5G', 'PoE++'), F('io', 'Ethernet', 'etherCON', 8, '2.5G PoE++ (etherCON)'), F('io', 'SFP', 'SFP28', 4, '25G SFP28 (APM414V card)')], '530 W, up to 1,130 W'),
    ('CSM4316', 'M4350-16C', [sfp(16, '100G QSFP28')], '')]
for sku, nm, ports, poe in M4350:
    add(sku, f'{nm} managed switch ({sku})', 'NETGEAR M4350', ports + CONSOLE + [OOB, R('in', 'Power', 'IEC C14', 2, 'AC In (modular PSU)')],
        f'NETGEAR M4350 AV and IT switch (AV user interface, Dante / AES67 / NDI / ST 2110 profiles{", SMPTE 2110 ready" if sku in ("VSM4320C", "XSM4344C", "MSM4328F", "MSM4310", "MSM4332", "XSM4344FC", "CSM4316") else ""}). '
        f'{"PoE budget " + poe + " (with extra power supplies). " if poe else "No PoE. "}1U rack mount, hot-swap modular power supplies and fans. '
        'Check: console/USB/management ports and number of PSU bays (typical for the series).', KB4350)

# ---------------- M4300 (previous generation, still widely installed) ----------------
M4300_URL = 'https://www.netgear.com/business/wired/switches/fully-managed/'
for sku, nm, ports, w, note in (
        ('XSM4316S', 'M4300-8X8F', [rj(8, '10G'), sfp(8, '10G SFP+')], 6, 'Half-width 1U; two fit side by side on one rack kit.'),
        ('XSM4324S', 'M4300-12X12F', [rj(12, '10G'), sfp(12, '10G SFP+')], 6, 'Half-width 1U; two fit side by side on one rack kit.'),
        ('XSM4348S', 'M4300-24X24F', [rj(24, '10G'), sfp(24, '10G SFP+')], 12, '1U.'),
        ('GSM4328S', 'M4300-28G', [rj(24, '1G'), rj(2, '10G'), sfp(2, '10G SFP+')], 12, '1U.'),
        ('GSM4352S', 'M4300-52G', [rj(48, '1G'), rj(2, '10G'), sfp(2, '10G SFP+')], 12, '1U.'),
        ('GSM4328PB', 'M4300-28G-PoE+', [rj(24, '1G', 'PoE+'), rj(2, '10G'), sfp(2, '10G SFP+')], 12, '1U, PoE+ (550 W PSU).'),
        ('GSM4352PB', 'M4300-52G-PoE+', [rj(48, '1G', 'PoE+'), rj(2, '10G'), sfp(2, '10G SFP+')], 12, '1U, PoE+ (550 W PSU).')):
    add(sku, f'{nm} managed switch ({sku})', 'NETGEAR M4300', ports + [F('io', 'RS-232', 'RJ45', 1, 'Console'), F('io', 'USB', 'USB-A', 1, 'USB storage'),
        OOB, R('in', 'Power', 'IEC C14', 2 if w == 12 else 1, 'AC In')],
        f'Previous-generation NETGEAR fully managed switch, stackable. {note} Check: ports and power inlets (from memory of the M4300 '
        'datasheet; the M4350 replaces it).', M4300_URL, verified=False, w=w)

ids = [m['id'] for m in MODELS]; assert len(ids) == len(set(ids))
json.dump(MODELS, open(os.path.join(CAT, 'netgear.json'), 'w'), indent=1)
print('netgear.json', len(MODELS), 'entries,', sum(m['verified'] for m in MODELS), 'verified')
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'netgear.json' not in idx: idx.append('netgear.json')
json.dump(idx, open(ip, 'w')); print(len(idx), 'files in index')
