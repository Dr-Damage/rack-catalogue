"""Cameras as off-rack end points -> catalogue/cameras.json.

Studio / system cameras (SMPTE fibre or triax to a CCU), PTZ cameras, camcorders and box / studio cameras, each with the
connectors you cable to: CCU fibre or triax, SDI out and return in, genlock, timecode, intercom, mic inputs, tally, LAN / NDI,
remote control and power. Category 'camera' (tag CAM). They are not racked: leave them out of the racks and type where they
are (or add them as a Camera end point in Signal paths and pick the model there), so cables show their far end.

The fibre head port is called 'CCU' (type Fibre, LEMO 3K.93C) so it pairs with the CCU's 'Camera' port. Triax heads use
type 'Triax'. Also camera position boxes (category 'wallbox'): wall / floor boxes whose holes are preloaded with the usual
camera inserts (SMPTE 311, BNC, XLR, etherCON, triax) via thru.inserts; each insert can still be changed on the placed box.

Specs are from maker spec pages and memory: everything is verified=False with a 'Check:' note.
"""
import json, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'catalogue', 'cameras.json')
items = []
CHECK = 'Check: connectors from the maker spec page; confirm against the operating manual.'


def g(dir, type, conn, count, prefix, face='rear'):
    return {'face': face, 'dir': dir, 'type': type, 'connector': conn, 'count': count, 'prefix': prefix}


def cam(id, mfr, pn, name, family, ports, src='', url='', notes='', box=None):
    e = {'id': id, 'manufacturer': mfr, 'partNumber': pn, 'name': name, 'family': family, 'category': 'camera', 'ru': 1, 'widthCols': 12,
         'fullDepth': False, 'verified': False, 'source': src or f'{mfr} product page', 'productUrl': url,
         'notes': (notes + ' ' if notes else '') + 'Off-rack end point: leave it out of the racks and type where it is. ' + CHECK,
         'portGroups': [p for p in ports if p]}
    if box: e['boxMm'] = box
    items.append(e)


# ---- port sets ----
def fibre_head(sdi='3G-SDI', sdi_n=1, prompter=True, mics=2, ic=2, lan=True, extra=()):
    return [g('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'CCU'),
            g('out', sdi, 'BNC', sdi_n, 'SDI Out'),
            g('out', 'HD-SDI', 'BNC', 1, 'Prompter Out') if prompter else None,
            g('in', 'Analog audio', 'XLR3F', mics, 'Mic In') if mics else None,
            g('io', 'Intercom', 'XLR5F', ic, 'Intercom') if ic else None,
            g('io', 'Ethernet', 'RJ45', 1, 'Network') if lan else None,
            g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'),
            g('io', 'Other', 'Other', 1, 'Tracker'),
            g('in', 'Power', 'XLR4M', 1, 'DC In 12V'),
            g('out', 'Power', 'Other', 1, 'DC Out'), *extra]


def triax_head(sdi='HD-SDI', mics=2, ic=2, extra=()):
    return [g('io', 'Triax', 'Fischer triax', 1, 'CCU (triax)'),
            g('out', sdi, 'BNC', 1, 'SDI Out'),
            g('out', 'HD-SDI', 'BNC', 1, 'Prompter Out'),
            g('in', 'Analog audio', 'XLR3F', mics, 'Mic In'),
            g('io', 'Intercom', 'XLR5F', ic, 'Intercom'),
            g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'),
            g('in', 'Power', 'XLR4M', 1, 'DC In 12V'), *extra]


def ptz(sdi12=0, sdi3=1, hdmi=1, sfp=0, poe=True, genlock=True, rs422=True, rs232=False, tally=True, audio=1, dc='DC locking', extra=()):
    return [g('out', '12G-SDI', 'BNC', sdi12, 'SDI Out 12G') if sdi12 else None,
            g('out', '3G-SDI', 'BNC', sdi3, 'SDI Out') if sdi3 else None,
            g('out', 'HDMI', 'HDMI', hdmi, 'HDMI Out') if hdmi else None,
            g('io', 'SFP', 'SFP+', sfp, 'Optical (SFP)') if sfp else None,
            g('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE+)' if poe else 'LAN'),
            g('in', 'Reference', 'BNC', 1, 'Genlock In') if genlock else None,
            g('io', 'RS-422', 'RJ45', 1, 'RS-422 (VISCA/AW)') if rs422 else None,
            g('io', 'RS-232', 'Mini-DIN 8', 1, 'RS-232') if rs232 else None,
            g('in', 'GPI', 'Other', 1, 'Tally / GPIO') if tally else None,
            g('in', 'Analog audio', '3.5mm jack', audio, 'Audio In') if audio else None,
            g('in', 'Power', dc, 1, 'DC In 12V'), *extra]


def camcorder(sdi='12G-SDI', sdi_n=1, ret=False, hdmi=True, tc=True, genlock=True, xlr=2, mic5=False, lan=True, dc='XLR4M', extra=()):
    return [g('out', sdi, 'BNC', sdi_n, 'SDI Out'),
            g('in', '3G-SDI', 'BNC', 1, 'SDI Return In') if ret else None,
            g('out', 'HDMI', 'HDMI', 1, 'HDMI Out') if hdmi else None,
            g('in', 'Reference', 'BNC', 1, 'Genlock In') if genlock else None,
            g('io', 'Timecode', 'BNC', 1, 'TC In/Out') if tc else None,
            g('in', 'Analog audio', 'XLR3F', xlr, 'Audio In') if xlr else None,
            g('in', 'Analog audio', 'XLR5F', 1, 'Mic In (stereo)') if mic5 else None,
            g('io', 'Ethernet', 'RJ45', 1, 'LAN') if lan else None,
            g('io', 'Other', 'Other', 1, 'Remote'),
            g('in', 'Power', dc, 1, 'DC In 12V'), *extra]


# ---- generic templates (pick when the model isn't in the list) ----
cam('generic-camera-smpte-fibre', 'Generic', 'System camera (SMPTE fibre)', 'System camera head, SMPTE 311 fibre to CCU', 'Generic camera', fibre_head(),
    'Generic', notes='Video, returns, tally, intercom and power all travel on the hybrid fibre to the CCU.')
cam('generic-camera-triax', 'Generic', 'System camera (triax)', 'System camera head, triax to CCU', 'Generic camera', triax_head(), 'Generic')
cam('generic-camera-ptz', 'Generic', 'PTZ camera (SDI + IP)', 'PTZ camera with SDI, HDMI and IP (NDI / SRT) out', 'Generic camera', ptz(), 'Generic')
cam('generic-camera-ptz-ip', 'Generic', 'PTZ camera (IP / NDI only)', 'PTZ camera, single PoE cable (NDI or SRT)', 'Generic camera',
    ptz(sdi3=0, hdmi=0, genlock=False, rs422=False, tally=False, audio=0), 'Generic')
cam('generic-camcorder', 'Generic', 'Camcorder (SDI)', 'Shoulder or handheld camcorder with SDI out', 'Generic camera', camcorder(), 'Generic')
cam('generic-camera-box-sdi', 'Generic', 'Box / POV camera (SDI)', 'Box or POV camera, SDI out', 'Generic camera',
    [g('out', '3G-SDI', 'BNC', 1, 'SDI Out'), g('io', 'RS-485', 'Other', 1, 'Control'), g('in', 'Power', 'DC barrel', 1, 'DC In 12V')], 'Generic')
cam('generic-camera-wireless', 'Generic', 'Wireless camera (RF / bonded cellular)', 'Camera with an on-board wireless or bonded cellular transmitter', 'Generic camera',
    [g('out', 'RF', 'Other', 1, 'RF / cellular (to receiver)'), g('out', '3G-SDI', 'BNC', 1, 'SDI Out'), g('in', 'Power', 'Battery connector', 1, 'Battery')], 'Generic',
    notes='The link to the receiver is wireless: draw it as an RF cable to the receiver so it shows on the wiring.')

# ---- Sony ----
S = 'https://pro.sony/ue_US/products/'
cam('sony-hdc-3500', 'Sony', 'HDC-3500', 'HDC-3500 4K/HD system camera (2/3" 3-CMOS global shutter)', 'Sony system cameras', fibre_head('12G-SDI', 1), url=S + 'broadcast-cameras/hdc-3500',
    notes='Pairs with the HDCU-3500 / HDCU-5500.')
cam('sony-hdc-5500', 'Sony', 'HDC-5500', 'HDC-5500 4K/HD system camera, shoulder type', 'Sony system cameras', fibre_head('12G-SDI', 1), url=S + 'broadcast-cameras/hdc-5500')
cam('sony-hdc-5500v', 'Sony', 'HDC-5500V', 'HDC-5500V 4K/HD system camera with variable ND', 'Sony system cameras', fibre_head('12G-SDI', 1), url=S + 'broadcast-cameras/hdc-5500v')
cam('sony-hdc-f5500', 'Sony', 'HDC-F5500', 'HDC-F5500 Super 35 4K system camera', 'Sony system cameras', fibre_head('12G-SDI', 1, extra=[g('io', 'Other', 'Other', 1, 'PL lens / LEMO')]), url=S + 'broadcast-cameras/hdc-f5500')
cam('sony-hdc-3200', 'Sony', 'HDC-3200', 'HDC-3200 4K/HD system camera', 'Sony system cameras', fibre_head('12G-SDI', 1), url=S + 'broadcast-cameras/hdc-3200')
cam('sony-hdc-3100', 'Sony', 'HDC-3100', 'HDC-3100 HD system camera', 'Sony system cameras', fibre_head('3G-SDI', 1), url=S + 'broadcast-cameras/hdc-3100',
    notes='Pairs with the HDCU-3100.')
cam('sony-hdc-4800', 'Sony', 'HDC-4800', 'HDC-4800 4K/HD high frame rate system camera', 'Sony system cameras', fibre_head('12G-SDI', 1), url=S + 'broadcast-cameras/hdc-4800',
    notes='Pairs with the BPU-4800 and HDCU-4300.')
cam('sony-hdc-p50', 'Sony', 'HDC-P50', 'HDC-P50 4K/HD POV system camera (box, fibre)', 'Sony system cameras',
    [g('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'CCU'), g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'),
     g('io', 'Other', 'Other', 1, 'Remote'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')], url=S + 'broadcast-cameras/hdc-p50')
cam('sony-hxc-fz90', 'Sony', 'HXC-FZ90', 'HXC-FZ90 4K/HD studio camera (fibre or triax)', 'Sony system cameras', fibre_head('12G-SDI', 1, mics=1), url=S + 'broadcast-cameras/hxc-fz90',
    notes='Pairs with the HXCU-FZ90. The triax version (HXC-FB80 range) uses a triax CCU instead.')
cam('sony-hxc-fb80', 'Sony', 'HXC-FB80', 'HXC-FB80 HD studio camera, triax', 'Sony system cameras', triax_head('3G-SDI'), url=S + 'broadcast-cameras/hxc-fb80')
cam('sony-pxw-z750', 'Sony', 'PXW-Z750', 'PXW-Z750 4K 2/3" shoulder camcorder', 'Sony camcorders', camcorder('12G-SDI', 2, ret=True, mic5=True), url=S + 'camcorders/pxw-z750')
cam('sony-pxw-z280', 'Sony', 'PXW-Z280', 'PXW-Z280 4K handheld camcorder', 'Sony camcorders', camcorder('12G-SDI', 1, dc='DC barrel'), url=S + 'camcorders/pxw-z280')
cam('sony-pxw-fx9', 'Sony', 'PXW-FX9', 'PXW-FX9 full-frame camcorder', 'Sony camcorders', camcorder('12G-SDI', 1, genlock=True), url=S + 'camcorders/pxw-fx9')
cam('sony-ilme-fr7', 'Sony', 'ILME-FR7', 'ILME-FR7 full-frame PTZ cinema camera', 'Sony PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, dc='DC locking'), url=S + 'cinema-line-cameras/ilme-fr7')
cam('sony-brc-x1000', 'Sony', 'BRC-X1000', 'BRC-X1000 4K PTZ camera', 'Sony PTZ', ptz(sdi3=1, hdmi=1, rs232=True), url=S + 'ptz-network-cameras/brc-x1000')
cam('sony-brc-am7', 'Sony', 'BRC-AM7', 'BRC-AM7 4K compact PTZ camera', 'Sony PTZ', ptz(sdi12=1, sdi3=0, genlock=False), url=S + 'ptz-network-cameras/brc-am7')
cam('sony-srg-a40', 'Sony', 'SRG-A40', 'SRG-A40 4K PTZ camera with auto framing', 'Sony PTZ', ptz(sdi3=1, genlock=False, rs422=False), url=S + 'ptz-network-cameras/srg-a40')

# ---- Grass Valley ----
GV = 'https://www.grassvalley.com/products/cameras/'
for pn, desc in [('LDX 100', 'native UHD system camera'), ('LDX 110', 'UHD system camera'), ('LDX 135', 'HD system camera, 3X HFR'), ('LDX 150', 'UHD HFR system camera'), ('LDX 180', 'Super 35 system camera')]:
    cam('gv-' + pn.lower().replace(' ', '-'), 'Grass Valley', pn, f'{pn} {desc}', 'LDX cameras', fibre_head('12G-SDI' if pn != 'LDX 135' else '3G-SDI', 1), url=GV + pn.lower().replace(' ', '-') + '/',
        notes='Pairs with the XCU base station (fibre) or a triax XCU. Also an IP (XCU-less, SMPTE 2110) version.')
cam('gv-ldx-c135', 'Grass Valley', 'LDX C135', 'LDX C135 compact HD system camera', 'LDX cameras', fibre_head('3G-SDI', 1, prompter=False, mics=1), url=GV + 'ldx-c135/')
cam('gv-ldx-86n', 'Grass Valley', 'LDX 86N', 'LDX 86N HD/4K system camera', 'LDX cameras', fibre_head('3G-SDI', 1), url=GV + 'ldx-86n-series/')

# ---- Ikegami ----
IK = 'https://www.ikegami.co.uk/products/'
cam('ikegami-uhk-x700', 'Ikegami', 'UHK-X700', 'UHK-X700 4K/HD system camera, global shutter', 'Ikegami system cameras', fibre_head('12G-SDI', 1), url=IK + 'uhk-x700/', notes='Pairs with the BSX-100 base station.')
cam('ikegami-uhk-x600', 'Ikegami', 'UHK-X600', 'UHK-X600 4K/HD system camera', 'Ikegami system cameras', fibre_head('12G-SDI', 1), url=IK + 'uhk-x600/')
cam('ikegami-uhl-x40', 'Ikegami', 'UHL-X40', 'UHL-X40 compact 4K/HD box camera', 'Ikegami system cameras',
    [g('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'CCU'), g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('in', 'Reference', 'BNC', 1, 'Genlock In'),
     g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')], url=IK + 'uhl-x40/')
cam('ikegami-hdk-99', 'Ikegami', 'HDK-99', 'HDK-99 HD system camera', 'Ikegami system cameras', fibre_head('3G-SDI', 1), url=IK + 'hdk-99/')
cam('ikegami-hdk-73', 'Ikegami', 'HDK-73', 'HDK-73 HD studio camera (fibre or triax)', 'Ikegami system cameras', fibre_head('3G-SDI', 1, lan=False), url=IK + 'hdk-73/')

# ---- Hitachi ----
HI = 'https://www.hitachi-kokusai.co.jp/global/en/products/broadcast/'
cam('hitachi-sk-uhd7000', 'Hitachi', 'SK-UHD7000', 'SK-UHD7000 4K/HD system camera', 'Hitachi system cameras', fibre_head('12G-SDI', 1), url=HI, notes='Pairs with the CU-UHD7000.')
cam('hitachi-sk-hd1300', 'Hitachi', 'SK-HD1300', 'SK-HD1300 HD system camera (fibre or triax)', 'Hitachi system cameras', fibre_head('3G-SDI', 1), url=HI, notes='Pairs with the CU-HD1300.')
cam('hitachi-z-hd5500', 'Hitachi', 'Z-HD5500', 'Z-HD5500 HD studio camera (digital triax or fibre)', 'Hitachi system cameras', triax_head('3G-SDI'), url=HI)
cam('hitachi-dk-h200', 'Hitachi', 'DK-H200', 'DK-H200 HD box camera', 'Hitachi system cameras',
    [g('out', '3G-SDI', 'BNC', 1, 'SDI Out'), g('in', 'Reference', 'BNC', 1, 'Genlock In'), g('io', 'Other', 'Other', 1, 'Remote'), g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')], url=HI)

# ---- Panasonic ----
PA = 'https://pro-av.panasonic.net/en/products/'
cam('panasonic-ak-uc4000', 'Panasonic', 'AK-UC4000', 'AK-UC4000 4K studio camera', 'Panasonic studio cameras', fibre_head('12G-SDI', 1), url=PA + 'ak-uc4000/', notes='Pairs with the AK-UCU600.')
cam('panasonic-ak-uc3300', 'Panasonic', 'AK-UC3300', 'AK-UC3300 4K studio camera', 'Panasonic studio cameras', fibre_head('12G-SDI', 1), url=PA + 'ak-uc3300/', notes='Pairs with the AK-UCU600.')
cam('panasonic-ak-hc5000', 'Panasonic', 'AK-HC5000', 'AK-HC5000 HD studio camera', 'Panasonic studio cameras', fibre_head('3G-SDI', 1), url=PA + 'ak-hc5000/')
cam('panasonic-ak-plv100', 'Panasonic', 'AK-PLV100', 'AK-PLV100 Super 35 8K/4K studio camera', 'Panasonic studio cameras', fibre_head('12G-SDI', 1), url=PA + 'ak-plv100/')
cam('panasonic-aw-ue150', 'Panasonic', 'AW-UE150', 'AW-UE150 4K PTZ camera', 'Panasonic PTZ', ptz(sdi12=1, sdi3=1, hdmi=1, sfp=1, dc='XLR4M'), url=PA + 'aw-ue150/')
cam('panasonic-aw-ue160', 'Panasonic', 'AW-UE160', 'AW-UE160 4K PTZ camera (NDI, SRT, ST 2110 option)', 'Panasonic PTZ', ptz(sdi12=1, sdi3=1, hdmi=1, sfp=1, dc='XLR4M'), url=PA + 'aw-ue160/')
cam('panasonic-aw-ue100', 'Panasonic', 'AW-UE100', 'AW-UE100 4K PTZ camera (NDI)', 'Panasonic PTZ', ptz(sdi12=1, sdi3=0, hdmi=1), url=PA + 'aw-ue100/')
cam('panasonic-aw-ue80', 'Panasonic', 'AW-UE80', 'AW-UE80 4K PTZ camera (NDI)', 'Panasonic PTZ', ptz(sdi12=1, sdi3=0, hdmi=1), url=PA + 'aw-ue80/')
cam('panasonic-aw-ue50', 'Panasonic', 'AW-UE50', 'AW-UE50 4K PTZ camera', 'Panasonic PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url=PA + 'aw-ue50/')
cam('panasonic-aw-he40', 'Panasonic', 'AW-HE40', 'AW-HE40 HD PTZ camera', 'Panasonic PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url=PA + 'aw-he40/')
cam('panasonic-aj-cx4000', 'Panasonic', 'AJ-CX4000', 'AJ-CX4000 4K shoulder camcorder', 'Panasonic camcorders', camcorder('12G-SDI', 2, ret=True, mic5=True), url=PA + 'aj-cx4000/')
cam('panasonic-ag-cx350', 'Panasonic', 'AG-CX350', 'AG-CX350 4K handheld camcorder', 'Panasonic camcorders', camcorder('3G-SDI', 1, genlock=False, dc='DC barrel'), url=PA + 'ag-cx350/')

# ---- Blackmagic Design ----
BM = 'https://www.blackmagicdesign.com/products/'
cam('bmd-ursa-broadcast-g2', 'Blackmagic Design', 'URSA Broadcast G2', 'Blackmagic URSA Broadcast G2 (B4 mount)', 'Blackmagic cameras',
    camcorder('12G-SDI', 1, ret=True, hdmi=False, lan=False, extra=[g('in', 'Analog audio', '3.5mm jack', 1, 'Mic In (3.5mm)'), g('io', 'Other', 'Hirose 12-pin', 1, 'Lens'),
                                                                      g('io', 'USB', 'USB-C', 1, 'USB-C'), g('io', 'Other', '2.5mm jack', 1, 'LANC')]),
    url=BM + 'blackmagicursabroadcast/techspecs', notes='Add the Blackmagic Camera Fiber Converter for SMPTE fibre to a Studio Fiber Converter.')
cam('bmd-studio-camera-4k-plus-g2', 'Blackmagic Design', 'Studio Camera 4K Plus G2', 'Blackmagic Studio Camera 4K Plus G2', 'Blackmagic cameras',
    [g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('in', 'Analog audio', '3.5mm jack', 1, 'Mic In'),
     g('io', 'Intercom', 'Other', 1, 'Talkback (headset)'), g('io', 'Ethernet', 'RJ45', 1, 'Ethernet'), g('io', 'USB', 'USB-C', 1, 'USB-C'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')],
    url=BM + 'blackmagicstudiocamera/techspecs')
cam('bmd-studio-camera-4k-pro-g2', 'Blackmagic Design', 'Studio Camera 4K Pro G2', 'Blackmagic Studio Camera 4K Pro G2', 'Blackmagic cameras',
    [g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('in', '12G-SDI', 'BNC', 1, 'SDI Return In'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('in', 'Reference', 'BNC', 1, 'Ref In'),
     g('in', 'Analog audio', 'XLR3F', 2, 'Audio In'), g('io', 'Intercom', 'XLR5F', 1, 'Talkback'), g('io', 'Ethernet', 'RJ45', 1, '10G Ethernet (IP link)'),
     g('io', 'USB', 'USB-C', 1, 'USB-C'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')], url=BM + 'blackmagicstudiocamera/techspecs',
    notes='The 10G Ethernet carries video, return, talkback, tally and control to an ATEM or Studio Converter.')
cam('bmd-studio-camera-6k-pro', 'Blackmagic Design', 'Studio Camera 6K Pro', 'Blackmagic Studio Camera 6K Pro (EF mount)', 'Blackmagic cameras',
    [g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('in', '12G-SDI', 'BNC', 1, 'SDI Return In'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('in', 'Reference', 'BNC', 1, 'Ref In'),
     g('in', 'Analog audio', 'XLR3F', 2, 'Audio In'), g('io', 'Intercom', 'XLR5F', 1, 'Talkback'), g('io', 'Ethernet', 'RJ45', 1, '10G Ethernet (IP link)'),
     g('io', 'USB', 'USB-C', 1, 'USB-C'), g('in', 'Power', 'XLR4M', 1, 'DC In 12V')], url=BM + 'blackmagicstudiocamera/techspecs')
cam('bmd-micro-studio-camera-4k-g2', 'Blackmagic Design', 'Micro Studio Camera 4K G2', 'Blackmagic Micro Studio Camera 4K G2 (MFT)', 'Blackmagic cameras',
    [g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('in', '12G-SDI', 'BNC', 1, 'SDI Return In'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'),
     g('in', 'Analog audio', '3.5mm jack', 1, 'Mic In'), g('io', 'Other', 'HD15', 1, 'Expansion (power, PTZ, tally)'), g('io', 'USB', 'USB-C', 1, 'USB-C'),
     g('in', 'Power', 'DC barrel', 1, 'DC In 12V')], url=BM + 'blackmagicmicrostudiocamera/techspecs', box=[83, 66, 72])
cam('bmd-camera-fiber-converter', 'Blackmagic Design', 'Blackmagic Camera Fiber Converter', 'Blackmagic Camera Fiber Converter (fits on the camera)', 'Blackmagic cameras',
    [g('io', 'Fibre', 'LEMO 3K.93C (SMPTE 304)', 1, 'CCU'), g('in', '12G-SDI', 'BNC', 1, 'SDI In (from camera)'), g('out', '12G-SDI', 'BNC', 2, 'SDI Out (return to camera / monitor)'),
     g('in', 'Analog audio', 'XLR3F', 2, 'Audio In'), g('io', 'Intercom', 'XLR5F', 2, 'Talkback'), g('io', 'Ethernet', 'RJ45', 1, 'Ethernet'),
     g('out', 'Power', 'XLR4F', 1, '12V Out (to camera)'), g('in', 'Power', 'Battery connector', 1, 'V-mount battery')],
    url=BM + 'blackmagicstudiofiberconverter/techspecs', notes='Pairs with the Studio Fiber Converter at the other end of the SMPTE fibre; powers the camera from the studio end.')

# ---- Canon ----
CA = 'https://www.canon.com.au/business/products/cameras/'
cam('canon-cr-n700', 'Canon', 'CR-N700', 'CR-N700 4K PTZ camera', 'Canon PTZ', ptz(sdi12=1, sdi3=1, hdmi=1, dc='Terminal block'), url=CA)
cam('canon-cr-n500', 'Canon', 'CR-N500', 'CR-N500 4K PTZ camera', 'Canon PTZ', ptz(sdi3=1, hdmi=1, dc='Terminal block'), url=CA)
cam('canon-cr-n300', 'Canon', 'CR-N300', 'CR-N300 4K PTZ camera', 'Canon PTZ', ptz(sdi3=0, hdmi=1, genlock=False), url=CA)
cam('canon-cr-x300', 'Canon', 'CR-X300', 'CR-X300 4K outdoor PTZ camera', 'Canon PTZ', ptz(sdi3=1, hdmi=1, genlock=False, dc='Terminal block'), url=CA)
cam('canon-xf605', 'Canon', 'XF605', 'XF605 4K handheld camcorder', 'Canon camcorders', camcorder('12G-SDI', 1, genlock=True, dc='DC barrel'), url=CA)

# ---- JVC ----
cam('jvc-gy-hc900', 'JVC', 'GY-HC900', 'GY-HC900 HD connected shoulder camcorder', 'JVC camcorders', camcorder('3G-SDI', 1, ret=True, mic5=True), url='https://pro.jvc.com/')
cam('jvc-ky-pz510', 'JVC', 'KY-PZ510', 'KY-PZ510 HD PTZ camera (NDI|HX, SRT)', 'JVC PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url='https://pro.jvc.com/')

# ---- BirdDog, PTZOptics, AVer, Lumens (IP / PTZ) ----
cam('birddog-p400', 'BirdDog', 'P400', 'P400 4K PTZ camera (full NDI)', 'BirdDog PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, genlock=False, rs422=True), url='https://birddog.tv/')
cam('birddog-p240', 'BirdDog', 'P240', 'P240 HD PTZ camera (full NDI)', 'BirdDog PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url='https://birddog.tv/')
cam('birddog-maverick', 'BirdDog', 'MAKI Ultra', 'MAKI Ultra 4K PTZ camera (NDI)', 'BirdDog PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, genlock=False), url='https://birddog.tv/')
cam('ptzoptics-move-4k', 'PTZOptics', 'Move 4K', 'Move 4K PTZ camera (NDI|HX, SRT)', 'PTZOptics PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, genlock=False, rs232=True), url='https://ptzoptics.com/')
cam('ptzoptics-studio-pro', 'PTZOptics', 'Studio Pro', 'Studio Pro HD box/PTZ camera', 'PTZOptics PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url='https://ptzoptics.com/')
cam('aver-ptc320uv2', 'AVer', 'PTC320UV2', 'PTC320UV2 4K auto-tracking PTZ camera', 'AVer PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, genlock=False, extra=[g('io', 'USB', 'USB-C', 1, 'USB')]), url='https://www.aver.com/')
cam('lumens-vc-a71p', 'Lumens', 'VC-A71P', 'VC-A71P 4K PTZ camera', 'Lumens PTZ', ptz(sdi12=1, sdi3=0, hdmi=1, genlock=True), url='https://www.mylumens.com/')

# ---- Marshall POV / mini cameras ----
MA = 'https://marshall-usa.com/'
cam('marshall-cv568', 'Marshall', 'CV568', 'CV568 3G/HD-SDI miniature camera (genlock)', 'Marshall POV',
    [g('out', '3G-SDI', 'BNC', 1, 'SDI Out'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('in', 'Reference', 'BNC', 1, 'Genlock In'), g('io', 'RS-485', 'Other', 1, 'RS-485 (Visca / Pelco)'),
     g('in', 'Power', 'DC locking', 1, 'DC In 12V')], url=MA, box=[45, 45, 77])
cam('marshall-cv420-12g', 'Marshall', 'CV420-12G', 'CV420-12G 4K POV camera', 'Marshall POV',
    [g('out', '12G-SDI', 'BNC', 1, 'SDI Out'), g('out', 'HDMI', 'HDMI', 1, 'HDMI Out'), g('io', 'Ethernet', 'RJ45', 1, 'LAN (PoE)'), g('io', 'RS-485', 'Other', 1, 'RS-485'),
     g('in', 'Power', 'DC locking', 1, 'DC In 12V')], url=MA)
cam('marshall-cv605', 'Marshall', 'CV605', 'CV605 HD PTZ camera', 'Marshall PTZ', ptz(sdi3=1, hdmi=1, genlock=False), url=MA)

# ---- camera position boxes (wall / floor) with the usual inserts fitted ----
def campos(id, name, fam, ins, rows, notes=''):
    items.append({'id': id, 'manufacturer': 'Generic', 'partNumber': name, 'name': name, 'family': fam, 'category': 'wallbox', 'ru': 1, 'widthCols': 12,
                  'fullDepth': False, 'verified': False, 'source': 'Generic', 'productUrl': '',
                  'notes': (notes + ' ' if notes else '') + 'Camera end point: leave it out of the racks and type where it is (e.g. Studio 1 cam 3). Inserts come fitted and can be changed per hole. '
                           'Check: the inserts against the box you buy.',
                  'thru': {'holes': len(ins), 'rows': rows, 'prefix': 'D', 'insert': '', 'fixed': False, 'inserts': ins}, 'portGroups': []})

campos('campos-smpte-basic', 'Camera position box: SMPTE, 2 BNC, XLR, etherCON', 'Camera position box', ['smpte', 'bnc', 'bnc', 'xlr3f', 'ethercon', 'blank'], 2,
       'SMPTE fibre to the CCU, BNC for a programme return and a spare SDI, an XLR for a mic and an etherCON for data.')
campos('campos-smpte-full', 'Camera position box: SMPTE, 4 BNC, 2 XLR, 2 etherCON', 'Camera position box',
       ['smpte', 'bnc', 'bnc', 'bnc', 'bnc', 'xlr3f', 'xlr3f', 'ethercon', 'ethercon', 'blank'], 2,
       'BNC for camera out, return, prompter and tally / spare; XLR mic lines; etherCON for PTZ, data or Dante.')
campos('campos-smpte-dual', 'Camera position box: 2 SMPTE, 2 BNC, 2 XLR, etherCON', 'Camera position box',
       ['smpte', 'smpte', 'bnc', 'bnc', 'xlr3f', 'xlr3f', 'ethercon', 'blank'], 2, 'Two camera positions side by side, or a main and a spare fibre.')
campos('campos-triax', 'Camera position box: triax, 2 BNC, XLR', 'Camera position box', ['triax', 'bnc', 'bnc', 'xlr3f'], 1)
campos('campos-ptz', 'PTZ camera plate: 2 BNC, 2 etherCON', 'Camera position box', ['bnc', 'bnc', 'ethercon', 'ethercon'], 1,
       'SDI out and genlock on BNC; LAN / PoE and RS-422 control on etherCON.')
campos('campos-floor-smpte', 'Camera floor box: 2 SMPTE, 4 BNC, 4 XLR, 2 etherCON', 'Camera floor box',
       ['smpte', 'smpte', 'bnc', 'bnc', 'bnc', 'bnc', 'xlr3f', 'xlr3f', 'xlr3f', 'xlr3f', 'ethercon', 'ethercon'], 3)
campos('campos-ob-panel', 'OB / venue camera tie panel: 4 SMPTE, 4 BNC', 'Camera position box', ['smpte', 'smpte', 'smpte', 'smpte', 'bnc', 'bnc', 'bnc', 'bnc'], 2,
       'Venue or stadium camera point that ties back to the OB dock.')

json.dump(items, open(OUT, 'w'), indent=1)
print(len(items), 'entries ->', OUT)
