# rack-catalogue

Equipment catalogue for **BroadcastRackElevations**, the rack elevation, wiring and cable schedule tool for broadcast engineers.

This repository holds data only: one JSON file per manufacturer describing each rack-mount product's size and connectors. It has no app code and no manufacturer images. The desktop app downloads these files at startup, so new equipment appears without reinstalling.

## What's here

| Path | Contents |
|---|---|
| `catalogue/index.json` | Plain array of the file names to load, in order |
| `catalogue/<brand>.json` | Array of models for one manufacturer (format in [`catalogue/README.md`](catalogue/README.md)) |
| `catalogue/FRAMES.md` | Extra fields for card frames (openGear, Evertz, Densité) and their cards |
| `catalogue/manifest.json` | `version` stamp plus the SHA-256, entry count and size of every listed file |
| `tools/*.py` | Generators that write the brand files (`python3 tools/<brand>.py`) |
| `tools/manifest.py` | Rebuilds `manifest.json`; run it after any generator |

## How the app uses it

1. Fetch `catalogue/manifest.json` from
   `https://raw.githubusercontent.com/Dr-Damage/rack-catalogue/main/catalogue/manifest.json`.
2. If `version` differs from the cached copy, download every file whose `sha256` changed.
3. Merge in this order: catalogue bundled with the app, then downloaded files, then the user's own edits (which always win).
4. If the network is unavailable, keep using the last cached or bundled copy.

## Data notes

- Port and connector data comes from manufacturers' published specification sheets and manuals. Each entry names its `source`.
- `verified: false` means some details are estimates. The entry's `notes` start the doubt with "Check:". Confirm these against the hardware before issuing drawings.
- Product names and part numbers belong to their manufacturers. This catalogue is not affiliated with or endorsed by any of them.

## Adding equipment

Edit or add a generator in `tools/`, run it, run `python3 tools/manifest.py`, and commit both the JSON and the manifest. Generators append new file names to `index.json` and never rewrite it.
