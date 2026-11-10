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
