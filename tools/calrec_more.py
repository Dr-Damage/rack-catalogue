#!/usr/bin/env python3
"""More Calrec (added 2026-11-15) -> catalogue/calrec-more.json. calrec.json stays with tools/audio2.py (cores, ImPulse, Apex M6, H2-IP,
and the 3U modular I/O rack, now a card frame with system 'Calrec modular I/O').
  Hydra2 fixed-format I/O boxes: analog XLR (AD5782/5781/5780, AD5603/5608), analog EDAC (AE5743/5991/5992), AES BNC (JB5606/5783/5962/5607),
  MADI (JM5736/5890/5831), GPIO (SW5739), Fieldbox AD6217-2, RP1 remote production core.
  Modular I/O cards for the 3U rack: analog in/out (D-type and XLR), mic splits, AES (BNC, XLR, D-type), Dante, SDI embed/de-embed, GPIO,
  and the Hydra2 interface card.
Every box has two Hydra2 SFP ports (primary/secondary; copper RJ45 or LC fibre SFPs) and two AC inlets. Rear RJ45 sockets on fixed boxes are
not used. Codes, I/O counts and connector types are from the Hydra2 installation manual (manualslib 904743) and Calrec's fixed-format launch
note; rack heights are estimated from connector counts unless stated, so those entries carry "Check:"."""
import json, os
CAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'catalogue')
def g(face, d, t, c, n, p): return dict(face=face, dir=d, type=t, connector=c, count=n, prefix=p)
def R(*a): return g('rear', *a)
AA, AES = 'Analog audio', 'AES/EBU'; OUT = []
MAN = ('Calrec Hydra2 installation manual (manualslib)', 'https://www.manualslib.com/manual/904743/Calrec-Hydra2.html')
NEW = ('Calrec fixed-format I/O launch (TV Technology)', 'https://tvtechnology.com/equipment/calrec-launches-new-fixedformat-io-boxes')
H2 = lambda: R('io', 'SFP', 'SFP', 2, 'Hydra2 SFP (Pri/Sec)')
PSU = lambda n=2: R('in', 'Power', 'IEC C14', n, 'PSU' if n > 1 else 'AC In')
def box(code, name, ru, ports, notes, src=MAN, verified=False, w=12, **kw):
    m = dict(id='calrec-' + code.lower(), manufacturer='Calrec', partNumber=code, name=name, family='Hydra2 fixed I/O', category='audio', ru=ru,
             widthCols=w, fullDepth=False, verified=verified, source=src[0], productUrl=src[1], notes=notes, portGroups=ports + [H2(), PSU()])
    m.update(kw); OUT.append(m)
CHK = ' Check: rack height (estimated from the connector count).'
# ---- analog XLR ----
for code, i, o, ru, src, ok in (('AD5782', 12, 4, 1, MAN, False), ('AD5781', 24, 8, 2, MAN, False), ('AD5780', 48, 16, 4, MAN, False),
                                ('AD5608', 12, 4, 2, NEW, True), ('AD5603', 24, 8, 2, NEW, True)):
    box(code, f'{code} Hydra2 analog I/O, {i} mic/line in, {o} line out, XLR, {ru}U', ru,
        [R('in', AA, 'XLR3F', i, 'Mic/Line In'), R('out', AA, 'XLR3M', o, 'Line Out')],
        f'Fixed-format Hydra2 I/O box: {i} mic/line inputs on female XLR, {o} line outputs on male XLR, 100-240 V AC.'
        + (' From the newer fixed-format range (2U to 4U).' if src is NEW else CHK), src=src, verified=ok)
# ---- analog EDAC ----
for code, style, ins, outs in (('AE5743', 'standard pin-out', (3, 12), (3, 12)), ('AE5991', 'Style 1 pin-out (8 in or 16 out per connector)', (4, 8), (2, 16)),
                               ('AE5992', 'Style 2 pin-out (12 in / 12 out per connector)', (3, 12), (3, 12))):
    box(code, f'{code} Hydra2 analog I/O, 32 mic/line in, 32 out, EDAC 38-pin', 1,
        [R('in', AA, f'EDAC 38-pin ({ins[1]} ch)', ins[0], 'Mic/Line In'), R('out', AA, f'EDAC 38-pin ({outs[1]} ch)', outs[0], 'Line Out')],
        f'Fixed-format Hydra2 I/O box: 32 mic/line inputs and 32 line outputs on 38-pin EDAC multipins, {style}.'
        + (' Check: EDAC count per direction for the standard pin-out.' if code == 'AE5743' else '') + CHK)
# ---- AES ----
for code, n, ru, src, ok, extra in (('JB5606', 16, 1, MAN, False, ''), ('JB5783', 32, 2, MAN, False, ''), ('JB5962', 32, 2, MAN, False, ' Later version of the JB5783.'),
                                    ('JB5607', 32, 3, NEW, True, ' A 4U version with 110 ohm XLRs is also made.')):
    box(code, f'{code} Hydra2 AES3 I/O, {n} in, {n} out, BNC, {ru}U', ru,
        [R('in', AES, 'BNC', n, 'AES In'), R('out', AES, 'BNC', n, 'AES Out')],
        f'Fixed-format Hydra2 I/O box: {n} AES3 inputs and {n} outputs on 75 ohm BNC (stereo pairs).{extra}' + ('' if ok else CHK), src=src, verified=ok)
# ---- MADI ----
for code, desc, ports in (('JM5736', 'multimode, SC', [R('io', 'MADI', 'SC duplex', 2, 'MADI (MM)')]),
                          ('JM5890', 'multimode ST plus BNC', [R('io', 'MADI', 'ST', 2, 'MADI fibre (MM)'), R('in', 'MADI', 'BNC', 2, 'MADI In'), R('out', 'MADI', 'BNC', 2, 'MADI Out')]),
                          ('JM5831', 'single-mode, SC (no fans)', [R('io', 'MADI', 'SC duplex', 2, 'MADI (SM)')])):
    box(code, f'{code} Hydra2 MADI I/O, 2 streams, {desc}', 1, ports,
        f'Fixed-format Hydra2 MADI box: two MADI streams, up to 128 channels in and 128 out. {desc[0].upper() + desc[1:]}. Check: rack height and connector counts.')
box('SW5739', 'SW5739 Hydra2 GPIO box', 1, [R('out', 'GPIO', 'Other', 1, 'GP outputs (relays)'), R('in', 'GPIO', 'Other', 1, 'GP inputs (opto)')],
    'Fixed-format Hydra2 GPIO unit: relay outputs and opto-isolated inputs on Calrec GPIO connectors. Check: counts, connector type and rack height.')
box('AD6217-2', 'Fieldbox AD6217-2 compact Hydra2 I/O, 8 mic/line in, 8 out', 1,
    [R('in', AA, 'XLR3F', 8, 'Mic/Line In'), R('out', AA, 'DB25 (8 ch)', 1, 'Line Out (Tascam)'), R('in', 'Power', 'DC', 1, 'DC In 10-30 V')],
    'Less than 1U high (40 mm), 220 mm wide, 384 mm deep: sits on a shelf or in a half-rack tray. 8 mic/line inputs on XLR, 8 line outputs on a '
    'Tascam-pinout D-type, two Hydra2 SFPs, IEC mains plus 10-30 V DC for battery or external PSU. One internal slot for a future AoIP card.',
    src=('Calrec Hydra2 I/O product guide (Fieldbox)', 'https://manualedistruzioni.it/calrec/i-o-system/hydra2/user-manual/1sowt'), verified=True, w=6, boxMm={'w': 220, 'h': 40})
OUT[-1]['portGroups'][-1] = PSU(1)
OUT.append(dict(id='calrec-rp1', manufacturer='Calrec', partNumber='RP1', name='RP1 remote production core, 2U', family='Hydra2', category='audio', ru=2,
                widthCols=12, fullDepth=True, verified=False, source='Calrec RP1 launch coverage (Fast and Wide)',
                productUrl='https://www.fast-and-wide.com/equipment-releases/location-recording/8132-calrec-audio-rp1',
                notes='2U core with on-board DSP for remote production: the console surface stays at base and the RP1 at the venue mixes IFBs and '
                      'monitors locally with low latency, over Hydra2 or AoIP. Check: I/O and network ports.',
                portGroups=[R('io', 'SFP', 'SFP', 4, 'Hydra2 / AoIP SFP'), R('io', 'Ethernet', 'RJ45', 2, 'Control'), PSU()]))

# ---- modular I/O cards (3U rack) ----
def mcard(code, name, width, ports, notes, color=None):
    c = dict(fits=['Calrec modular I/O'], slotWidth=width)
    if color: c['color'] = color
    OUT.append(dict(id='calrec-' + code.lower(), manufacturer='Calrec', partNumber=code, name=name, family='Hydra2 modular I/O cards', category='card', ru=0,
                    widthCols=0, fullDepth=False, verified=False, source=MAN[0], productUrl=MAN[1], notes=notes + ' Check: rear panel layout.', portGroups=[],
                    card=c, rearModules=[dict(partNumber=code, name='Connector panel', width=width, cardsPerModule=1, cardOffset=0, default=True,
                                              included=True, portGroups=ports)]))
mcard('HY-IF', 'Hydra2 interface card (modular I/O)', 1, [H2()], 'Links the modular I/O rack to the Hydra2 network; goes in the central slot. Part code not published.', '#3a6ea5')
mcard('AD5838', 'AD5838 8 line inputs, 37-pin D-type', 1, [R('in', AA, 'DB37 (8 ch)', 1, 'Line In')], '8 balanced line-level analog inputs.')
mcard('AD6057', 'AD6057 mic/line inputs, 37-pin D-type', 1, [R('in', AA, 'DB37 (8 ch)', 1, 'Mic/Line In')], 'Balanced mic/line analog inputs on one 37-pin D-type. Check: input count (8 shown).')
mcard('AD5840', 'AD5840 4 mic/line inputs, XLR (2 slots)', 2, [R('in', AA, 'XLR3F', 4, 'Mic/Line In')], '4 balanced mic/line inputs on female XLR.')
mcard('AL5870', 'AL5870 mic/line inputs with split outputs, XLR (2 slots)', 2, [R('in', AA, 'XLR3F', 2, 'Mic/Line In'), R('out', AA, 'XLR3M', 2, 'Split Out')],
      'Mic/line inputs, each with a pre-gain split output. Check: channel count (2 shown).')
mcard('AL5875', 'AL5875 mic/line input with 3 split outputs, XLR (2 slots)', 2, [R('in', AA, 'XLR3F', 1, 'Mic/Line In'), R('out', AA, 'XLR3M', 3, 'Split Out')],
      'Mic/line input with three pre-gain split outputs. Check: channel count.')
mcard('DA5839', 'DA5839 8 line outputs, 37-pin D-type', 1, [R('out', AA, 'DB37 (8 ch)', 1, 'Line Out')], '8 balanced line-level analog outputs.')
mcard('DA5867', 'DA5867 4 line outputs, XLR (2 slots)', 2, [R('out', AA, 'XLR3M', 4, 'Line Out')], '4 balanced line-level analog outputs on male XLR.')
mcard('JB5860', 'JB5860 4 AES3 inputs, BNC', 1, [R('in', AES, 'BNC', 4, 'AES In')], '4 unbalanced (75 ohm) AES3 inputs.')
mcard('JB5837', 'JB5837 4 AES3 outputs, BNC', 1, [R('out', AES, 'BNC', 4, 'AES Out')], '4 unbalanced (75 ohm) AES3 outputs.')
mcard('JX5869', 'JX5869 4 AES3 inputs, XLR (2 slots)', 2, [R('in', AES, 'XLR3F', 4, 'AES In')], '4 balanced (110 ohm) AES3 inputs on female XLR.')
mcard('JB5868', 'JB5868 4 AES3 outputs, XLR', 2, [R('out', AES, 'XLR3M', 4, 'AES Out')], '4 balanced (110 ohm) AES3 outputs on male XLR. Check: slot width (manual says 1).')
mcard('JD5842', 'JD5842 8 AES3 in and 8 out, 25-pin D-type', 1, [R('in', AES, 'DB25 (8 ch)', 1, 'AES In'), R('out', AES, 'DB25 (8 ch)', 1, 'AES Out')],
      '8 AES3 inputs (male 25-pin D-type) and 8 outputs (female 25-pin D-type).')
mcard('BI6192', 'BI6192 Dante card, redundant', 1, [R('io', 'Dante/AES67', 'RJ45', 2, 'Dante Pri/Sec')], 'Dante integration with network redundancy.', '#c8102e')
mcard('VI5872', 'VI5872 SDI embedder', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Out')], 'Embeds Hydra2 audio into SDI. Check: BNC count.')
mcard('VO5841', 'VO5841 SDI de-embedder', 1, [R('in', '3G-SDI', 'BNC', 1, 'SDI In'), R('out', '3G-SDI', 'BNC', 1, 'SDI Loop')], 'De-embeds SDI audio onto the Hydra2 network. Check: BNC count.')
mcard('WY5858', 'WY5858 GPIO card, 8 in / 8 changeover out', 1, [R('io', 'GPIO', 'DB50', 1, 'GPIO')], '8 opto inputs and 8 full-changeover relay outputs on a 50-pin D-type.')
mcard('WY5859', 'WY5859 GPIO card, 8 in / 16 out', 1, [R('io', 'GPIO', 'DB50', 1, 'GPIO')], '8 opto inputs and 16 outputs on a 50-pin D-type.')

ids = [m['id'] for m in OUT]; assert len(ids) == len(set(ids))
json.dump(OUT, open(os.path.join(CAT, 'calrec-more.json'), 'w'), indent=1, ensure_ascii=False)
ip = os.path.join(CAT, 'index.json'); idx = json.load(open(ip))
if 'calrec-more.json' not in idx: idx.append('calrec-more.json')
json.dump(idx, open(ip, 'w')); print('calrec-more.json', len(OUT), 'entries,', sum(m['verified'] for m in OUT), 'verified;', len(idx), 'files')
