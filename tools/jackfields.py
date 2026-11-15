"""Video and audio jackfields (patchbays with normals) for the rack designer -> catalogue/jackfields.json.

Each entry has a `jack` block that the app turns into ports: rear A1..An (in, from the source), rear B1..Bn (out, to the
destination) and front jacks "A n jack" (top row) / "B n jack" (bottom row). normal: full | half | none.
Configurations come from maker part-number listings at resellers (Markertek, Full Compass, B&H, Pacific Radio) and maker pages;
everything is verified=false until checked against the maker's spec sheet. Canare patchbays live in canare.json and are read as
jackfields by the app. Krone is handled elsewhere.
"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'jackfields.json')
items = []

def jf(id, mfr, pn, name, family, ru, points, normal, sig, front, rear, src, url='', notes='', per=0):
    j = {'points': points, 'normal': normal, 'type': sig, 'front': front, 'rear': rear}
    if per: j['perRow'] = per
    items.append({'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': 'patch',
                  'ru': ru, 'widthCols': 12, 'fullDepth': False, 'verified': False, 'source': src, 'productUrl': url,
                  'notes': (notes + ' ' if notes else '') + 'Check: configuration from the part number listing; confirm normals, termination and rear connector on the maker spec sheet.',
                  'jack': j,
                  'portGroups': [{'face': 'front', 'dir': 'io', 'type': sig, 'connector': front, 'count': points * 2, 'prefix': 'Jack'},
                                 {'face': 'rear', 'dir': 'in', 'type': sig, 'connector': rear, 'count': points, 'prefix': 'A'},
                                 {'face': 'rear', 'dir': 'out', 'type': sig, 'connector': rear, 'count': points, 'prefix': 'B'}]})

N = {'full': 'full normal', 'half': 'half normal', 'none': 'not normalled'}
# ---- generic (for when the maker isn't decided yet) ----
for nm, sig, front, rear in [('full', '12G-SDI', 'Midsize video jack', 'BNC'), ('none', '12G-SDI', 'Midsize video jack', 'BNC')]:
    jf(f'jf-generic-sdi-2x32-{nm}', 'Generic', f'SDI jackfield 2x32 ({N[nm]})', f'SDI video jackfield, 2x32, 1RU, {N[nm]}', 'Video jackfield', 1, 32, nm, sig, front, rear, 'Generic', notes='Use until the maker is chosen.')
for nm in ['full', 'half', 'none']:
    jf(f'jf-generic-tt-2x48-{nm}', 'Generic', f'TT audio jackfield 2x48 ({N[nm]})', f'Bantam/TT audio jackfield, 2x48, 1RU, {N[nm]}, DB25 rear', 'Audio jackfield', 1, 48, nm, 'Analog audio', 'Bantam (TT)', 'DB25 (8 ch)', 'Generic', notes='Use until the maker is chosen.')

# ---- ADC / CommScope ProPatch video ----
MK = 'Markertek part listing'
jf('adc-ppe1232-mvj-bk', 'ADC (CommScope)', 'PPE1232-MVJ-BK', 'ProPatch 2x32 midsize HD video jackfield, normalled, non-terminating, 1RU', 'ProPatch video jackfield', 1, 32, 'full', 'HD-SDI', 'Midsize video jack', 'BNC', MK, 'https://m.markertek.com/product/ppe1232-mvj-bk/adc-commscope-ppe1232-mvj-bk-1-ru-2x32-mid-size-hd-normalled-video-jackfield-non-terminating-black')
jf('adc-ppe2232-mvjt-bk', 'ADC (CommScope)', 'PPE2232-MVJT-BK', 'ProPatch 2x32 midsize HD video jackfield, normalled, terminating, 2RU', 'ProPatch video jackfield', 2, 32, 'full', 'HD-SDI', 'Midsize video jack', 'BNC', MK, 'https://markertek.com/product/ppe2232-mvjt-bk/adc-commscope-ppe2232-mvjt-bk-2ru2x32-mid-size-hd-normalled-video-jackfield-terminating-black')
jf('adc-ppe1232-cjm-bk', 'ADC (CommScope)', 'PPE1232-CJM-BK', 'ProPatch 2x32 midsize HD video jackfield, straight-through (not normalled), 1RU', 'ProPatch video jackfield', 1, 32, 'none', 'HD-SDI', 'Midsize video jack', 'BNC', MK, 'https://www.markertek.com/product/ppe1232-cjm-bk/adc-commscope-ppe1232-cjm-bk-1ru-2x32-mid-size-hd-straight-thru-video-jackfield-non-terminating-black')
jf('adc-ppi2232-cjm-bk', 'ADC (CommScope)', 'PPI2232-CJM-BK', 'ProPatch Integrated 2x32 midsize video jackfield, straight-through (not normalled), 2RU', 'ProPatch video jackfield', 2, 32, 'none', 'HD-SDI', 'Midsize video jack', 'BNC', MK, 'https://www.markertek.com/product/ppi2232-cjm-bk/adc-commscope-ppi2232-cjm-2ru-2x32-straight-thru-non-terminating-video-patchbay')
# ---- ADC / CommScope audio ----
jf('adc-ppp1248-e3-hn-s', 'ADC (CommScope)', 'PPP1248-E3-HN-S', 'ProPatch 2x48 bantam audio patchbay, half normal, EDAC 90-pin rear, 1RU', 'ProPatch audio', 1, 48, 'half', 'Analog audio', 'Bantam (TT)', 'EDAC 90-pin', MK, 'https://www.markertek.com/product/ppp1248-e3-hn-s/adc-commscope-ppp1248-e3-hn-s-1ru-2x48-bantam-patchbay-half-normal-with-edac-3-pin')
jf('adc-ppb3-14mkivhn', 'ADC (CommScope)', 'PPB3-14MKIVHN', 'ProPatch QCP IV 2x48 bantam audio patchbay, half normal, punch-down rear, 2RU', 'ProPatch audio', 2, 48, 'half', 'Analog audio', 'Bantam (TT)', 'QCP punch-down', MK, 'https://www.markertek.com/product/ppb3-14mkivhn/adc-commscope-ppb3-14mkivhn-propatch-qcp-iv-2ru-2x48-bantam-tt-audio-patchbay-half-normals')

# ---- Bittree video ----
jf('bittree-s64s-1mwnbk', 'Bittree', 'S64S-1MWNBK', '2x32 12G Mini-WECO midsize video patchbay, 1RU', '12G midsize video', 1, 32, 'full', '12G-SDI', 'Mini-WECO jack', 'BNC', MK, 'https://www.markertek.com/product/bit-s64s-1mwnbk/bittree-s64s-1mwnbk-64-point-12ghz-4k-8k-mini-weco-mid-size-video-patchbay-2x32-1ru', 'Check: normalling assumed from the N in the part number.')
jf('bittree-s64t-1mwnbk', 'Bittree', 'S64T-1MWNBK', '2x32 12G Mini-WECO midsize video patchbay, 2RU', '12G midsize video', 2, 32, 'full', '12G-SDI', 'Mini-WECO jack', 'BNC', MK, 'https://www.markertek.com/product/bit-s64t-1mwnbk/bittree-s64t-1mwnbk-2x32-2ru-64-point-12ghz-4k-8k-mini-weco-mid-size-video-patchbay', 'Check: normalling assumed from the N in the part number.')
jf('bittree-s64s-2mvtbk', 'Bittree', 'S64S-2MVTBK', '2x32 12G+ micro-video patchbay, full normal and terminated, BNC rear, 1RU', '12G+ micro video', 1, 32, 'full', '12G-SDI', 'Micro video jack', 'BNC', MK, 'https://www.markertek.com/product/bit-s64s-2mvtbk/bittree-s64s-2mvtbk-1-ru-stylized-2x32-12gplus-micro-video-patchbay-full-normal-terminated-full-size-bnc-on-rear')
# ---- Bittree audio ----
jf('bittree-b96dc-hnibs-d25', 'Bittree', 'B96DC-HNIBS/D25 M2OU7B', '2x48 TT patchbay, half normal, bussed ground, DB25 rear, 1RU', 'TT audio 969', 1, 48, 'half', 'Analog audio', 'Bantam (TT)', 'DB25 (8 ch)', MK, 'https://markertek.com/product/bit-b96dchnibsd/bittree-b96dc-hnibs-d25-m2ou7b-2x48-1ru-db25-half-norm-buss-ground-tt-patchbay-7-inch', 'Front programmable normals.')
jf('bittree-b96dc-fnibs-e90', 'Bittree', 'B96DC-FNIBS/E90 M2OU7B', '2x48 TT patchbay, full normal, bussed ground, EDAC 90-pin rear, 1RU', 'TT audio 969', 1, 48, 'full', 'Analog audio', 'Bantam (TT)', 'EDAC 90-pin', MK, 'https://www.markertek.com/product/b96dc-fnibs-e90/bittree-b96dc-fnibs-e90-m2ou7b-2x48-1ru-e90-full-norm-bussed-ground-tt-patchbay-7-inch', 'Front programmable normals.')
jf('bittree-b96dc-fnait-e3', 'Bittree', 'B96DC-FNAIT/E3 M2OU12B', '2x48 TT patchbay, full normal, isolated grounds, E3 rear, 2RU', 'TT audio 969', 2, 48, 'full', 'Analog audio', 'Bantam (TT)', 'EDAC 90-pin (E3)', MK, 'https://www.markertek.com/product/bit-969a018/bittree-969a018-audio-tt-bantam-full-normal-isolated-front-programmable-969-a-series-2x48-2-ru-e3-rear-interface', 'Front programmable normals.')
jf('bittree-b96dc-nnait-e3', 'Bittree', 'B96DC-NNAIT/E3 M2OU12B', '2x48 TT patchbay, not normalled, E3 rear, 2RU', 'TT audio 969', 2, 48, 'none', 'Analog audio', 'Bantam (TT)', 'EDAC 90-pin (E3)', MK, 'https://www.markertek.com/product/bit-b96dcnnaite3/bittree-b96dc-nnait-e3-m2ou12b-2-ru-black-2x48-mono-spaced-front-programable-bantam-patchbay', 'Front programmable normals.')

# ---- Switchcraft video ----
jf('switchcraft-mmvpb32k175t', 'Switchcraft', 'MMVPB32K175T', '2x32 12G micro video patchbay, full normal, terminated, BNC rear, 1RU', 'Ultra VideoPatch', 1, 32, 'full', '12G-SDI', 'Micro video jack', 'BNC', 'Switchcraft product page', 'https://www.switchcraft.com/1ru-2x32-midsize-12g-4k-8k-video-patchbay-full-normal-no-looping-plug-micro-video-plug-to-uhd-bnc/mmvpb32k175t/')
jf('switchcraft-mvp32k1uhd', 'Switchcraft', 'MVP32K1UHD', 'Ultra VideoPatch 2x32 12G midsize video patchbay, not normalled, 1RU', 'Ultra VideoPatch', 1, 32, 'none', '12G-SDI', 'Midsize video jack', 'BNC', MK, 'https://markertek.com/product/sw-mvp32k1uhd/switchcraft-mvp32k1uhd-ultra-videopatch-midsize-12g-video-patchbay-2x32-x-1ru')
jf('switchcraft-mvp32k3nt', 'Switchcraft', 'MVP32K3NT', '2x32 midsize video patchbay, normalled, non-terminated, 2RU', 'VideoPatch', 2, 32, 'full', 'HD-SDI', 'Midsize video jack', 'BNC', MK, 'https://markertek.com/product/sw-mvp32k3nt/switchcraft-mvp32k3nt-2ru-2x32-midsize-video-patchbay-normalled-non-terminated')
# ---- Switchcraft audio ----
jf('switchcraft-9625', 'Switchcraft', '9625', 'StudioPatch 9625 2x48 TT patchbay, DB25 rear, front-programmable normals, 1RU', 'StudioPatch', 1, 48, 'half', 'Analog audio', 'Bantam (TT)', 'DB25 (8 ch)', 'Switchcraft StudioPatch manual', 'https://www.switchcraft.com/Product.aspx?ID=3151', 'Normals set per channel from the front (full, half or none); half shown as set.')

# ---- Neutrik audio ----
jf('neutrik-nys-spp-l1', 'Neutrik', 'NYS-SPP-L1', '2x24 1/4-inch TRS patchbay, switchable normals, 1RU', 'Patchbay', 1, 24, 'half', 'Analog audio', '1/4" TRS jack', '1/4" TRS jack', 'Neutrik product listing', '', 'Normals set per channel by turning the jack card round (full, half or through). Neutrik makes no SDI jackfield.')

json.dump(items, open(OUT, 'w'), indent=1)
print(len(items), 'entries ->', OUT)
