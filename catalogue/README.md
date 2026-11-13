# Equipment catalogue data

One JSON file per manufacturer, listed in `index.json` (a plain array of file names).
The app loads every listed file at startup and merges the entries into its built-in
catalogue. Entries a user edits in the app are saved to the database and override these.

Each file is an array of models:

| field | meaning |
|---|---|
| `id` | unique, prefixed by brand (`ross-`, `gv-`, `sony-` ...). Never reuse `bmd-`, `gen-`, `linkpi-`, `tvu-`. |
| `manufacturer`, `partNumber`, `name`, `family` | as printed by the maker; `family` groups the catalogue |
| `category` | router, switcher, recorder, converter, monitor, network, power, pdu, patch, shelf, blank, audio, computer, control, other |
| `ru`, `widthCols` | height in RU, width in twelfths of a 19" rack (12 = full width) |
| `fullDepth` | true if the unit blocks the rear of the rack |
| `verified` | true only when ports come from the maker's spec sheet or manual; false shows "check specs" |
| `source`, `productUrl`, `notes` | where the data came from; notes start any doubt with "Check:" |
| `portGroups` | `[{face: front/rear, dir: in/out/io, type, connector, count, prefix}]`; `type` is one of the app's signal types (12G-SDI, 3G-SDI, HD-SDI, HDMI, DisplayPort, Ethernet, Fibre, SFP, Reference, RS-422, USB, Power, Analog audio, AES/EBU, Dante/AES67, Other) or a descriptive one such as Timecode or MADI audio |
| optional | `frontImg`/`rearImg` (`panels/<id>-F.jpg`), `frontAR`/`rearAR` (width/height), `screens {count,sizeIn,aspect}`, `boxMm {w,h}` |
| desktop units | `boxMm {w,h}` draws a desktop box (Mac mini, NUC) at real size on its shelf space; `formFactor` names its body shape (`Mac mini (2024+)`, `Mac mini (2018-2023)`, `Mac Studio`, `NUC 4x4 tall`, `NUC 4x4 slim`, `NUC Pro+ slim`) |
| rack kits | a shelf or enclosure (category `shelf`) that holds desktop units has `carrier {bays, fits}`: how many it holds and the `formFactor`s it takes (Sonnet RackMac, Penn Elcom R1498, MyElectronics NUC mounts; `tools/computers.py`) |

Card-based frames (Ultrix, openGear) list only the fixed frame ports; card I/O is added per device.
Generator scripts live in `../tools/` (e.g. `tools/ross.py`).

## Panel layout (optional)

`layout` places port groups where they really sit on the panel, so the app draws the true arrangement (its own drawing, no manufacturer image). Groups with no block keep the automatic grid.

```json
"layout": {
  "rear": [
    {"g": 1, "start": 1, "count": 72, "x0": 0.05, "y0": 0.40, "x1": 0.95, "y1": 0.60, "rows": 1, "cols": 72, "order": "row", "from": "tl", "size": 0.12}
  ],
  "front": [],
  "fixtures": [{"face": "rear", "kind": "psu", "x0": 0.88, "y0": 0.1, "x1": 0.99, "y1": 0.9, "text": "PSU 1"}]
}
```

| key | meaning |
|---|---|
| `g` | index into `portGroups` (0-based). Several blocks may share one `g` |
| `start`, `count` | optional slice of that group (1-based first port, number of ports); default is the whole group |
| `x0,y0,x1,y1` | block rectangle as fractions of the panel, origin top-left. Rear is as seen from behind the rack (no mirroring). The panel is the full 19-inch width with ears; for a part-width unit (`widthCols` < 12) it is that unit's own share of the width |
| `rows`, `cols` | grid inside the block |
| `order` | `row` fills across then down, `col` fills down then across |
| `from` | start corner: `tl`, `tr`, `bl`, `br` |
| `size` | optional connector pitch as a fraction of panel height; otherwise sized to the cell |
| `fixtures` | non-port features: `kind` psu, fan, slot or label, with `face`, a rectangle and optional `text` |

Layouts are traced from the maker's published rear-panel drawings or photos; `layoutSource` names the source.

## Power strips (PDUs)

A power strip is an entry (category `pdu`) with a `pdu` block. The app makes its ports from it: `Mains In` plus `Outlet 1` to `Outlet N`, numbered in the order of `outlets`. Leave power groups out of `portGroups` (other connectors, such as a network port, stay there). A 0U vertical strip still gives `ru: 1, widthCols: 12`; those are ignored.

```json
"pdu": {
  "mount": "v", "lengthMm": 1800, "widthMm": 56, "cordEnd": "bottom",
  "phase": 3, "volts": 400, "amps": 32, "plug": "au3p32", "cordM": 3, "metering": "metered",
  "main": {"type": "none"},
  "circuits": [{"id": "A", "phase": "L1", "type": "mcb", "amps": 16}, {"id": "B", "phase": "L2", "type": "rcbo", "amps": 16, "mA": 30}],
  "outlets": [{"type": "c13", "count": 6, "circuit": "A"}, {"type": "c19", "count": 1, "circuit": "A", "switched": false}]
}
```

| key | meaning |
|---|---|
| `mount` | `h` sits in RU positions, `v` is a 0U strip down the side of the rack (`lengthMm`, `widthMm`, `cordEnd` top/bottom) |
| `phase`, `volts`, `amps` | 1 or 3. Volts is line to neutral for single phase (230) and line to line for 3 phase (400). Amps is per phase |
| `plug` | au10, au15, au20, au32, au3p20, au3p32, au3p40, au3p50, c14, c20, cee16, cee32, cee3p16, cee3p32, schuko, uk, n515, l530, l630, l2130, hard (hardwired), other (with `plugText`) |
| `metering` | none, meter, metered, switched, outlet, switched-outlet |
| `main` | whole-strip protection before the circuits: `type`, `amps`, `mA` |
| `circuits` | the protected circuits inside the strip. `type`: none, switch, fuse, resettable (thermal / resettable fuse), mcb, rcd, rcbo. `amps` is the rating, `mA` the RCD trip current. `phase` L1/L2/L3 on 3 phase strips |
| `outlets` | groups in order: `type` au10, au15, c13, c19, c15, c13l, c19l, schuko, uk, n515, n520, other; `count`; `circuit` id; `switched` true when each outlet has its own switch |
