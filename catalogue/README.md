# Equipment catalogue data

One JSON file per manufacturer, listed in `index.json` (a plain array of file names).
The app loads every listed file at startup and merges the entries into its built-in
catalogue. Entries a user edits in the app are saved to the database and override these.

Each file is an array of models:

| field | meaning |
|---|---|
| `id` | unique, prefixed by brand (`ross-`, `gv-`, `sony-` ...). Never reuse `bmd-`, `gen-`, `linkpi-`, `tvu-`. |
| `manufacturer`, `partNumber`, `name`, `family` | as printed by the maker; `family` groups the catalogue |
| `category` | router, switcher, recorder, converter, monitor, network, power, patch, shelf, blank, audio, computer, control, other |
| `ru`, `widthCols` | height in RU, width in twelfths of a 19" rack (12 = full width) |
| `fullDepth` | true if the unit blocks the rear of the rack |
| `verified` | true only when ports come from the maker's spec sheet or manual; false shows "check specs" |
| `source`, `productUrl`, `notes` | where the data came from; notes start any doubt with "Check:" |
| `portGroups` | `[{face: front/rear, dir: in/out/io, type, connector, count, prefix}]`; `type` is one of the app's signal types (12G-SDI, 3G-SDI, HD-SDI, HDMI, DisplayPort, Ethernet, Fibre, SFP, Reference, RS-422, USB, Power, Analog audio, AES/EBU, Dante/AES67, Other) or a descriptive one such as Timecode or MADI audio |
| optional | `frontImg`/`rearImg` (`panels/<id>-F.jpg`), `frontAR`/`rearAR` (width/height), `screens {count,sizeIn,aspect}`, `boxMm {w,h}` |

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
