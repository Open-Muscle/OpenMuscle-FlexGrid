# JLCPCB Assembly Workflow (KiCad + Bouni Plugin)

How OpenMuscle hardware revisions get from a routed KiCad project to a JLCPCB order. The procedure is the same for every board (Flex, Rigid, future revisions); only the specific LCSC parts change.

This document captures the workflow we use today. It is generic enough to apply to any V4+ revision of the FlexGrid or other Open Muscle boards.

---

## Toolchain

| Component | What it does |
|---|---|
| **KiCad 8.x** | Schematic capture + PCB layout (you already have this) |
| **`kicad-jlcpcb-tools` plugin** | LCSC part search, LCSC-number tagging on components, BOM + CPL + Gerber generation in JLCPCB-friendly format |
| **JLCPCB web ordering page** | https://jlcpcb.com/ (where the generated files actually get uploaded) |

### Plugin install (one-time per machine)

The plugin is **not** in KiCad's official Plugin and Content Manager repository, so two install paths:

**Option A: Install from a release zip (recommended)**

1. Download the latest release from https://github.com/Bouni/kicad-jlcpcb-tools/releases (looks like `KiCadJLCPCBTools.zip` or similar)
2. KiCad main window → **Tools → Plugin and Content Manager**
3. Click **Install from File...** at the bottom
4. Pick the downloaded zip
5. Apply Pending Changes, restart KiCad

**Option B: Add Bouni's PCM repository for auto-updates**

1. PCM dialog → **Manage...** (top right)
2. Add a new repository:
   - Name: `Bouni's repo`
   - URL: `https://raw.githubusercontent.com/Bouni/bouni-kicad-repository/main/repository.json`
3. Switch the repository dropdown to "Bouni's repo"
4. Search `jlcpcb`, install the plugin, restart KiCad

After install: the plugin appears as a button in the **PCB Editor toolbar** (not the schematic editor). Also accessible at **Tools → External Plugins → JLCPCB Tools**.

---

## Per-revision workflow

The 5 phases below run in order for every new revision. Each phase is a checkpoint; don't skip ahead.

### Phase 1: tag LCSC parts on every component

Open the PCB editor for the board you are about to fab. Click the JLCPCB Tools button. A side panel opens listing every component on the board, color-coded:

- **Green** = LCSC part is assigned, BOM and POS toggled on
- **Red** = no LCSC part yet, needs attention
- **Yellow / partial** = mixed state (some flags off)

For each red row:

1. Click the row in the panel
2. Click **Assign LCSC number**
3. The plugin opens a search dialog into LCSC's catalog
4. Search by part value (e.g. `100nF 0603` for a cap, or by exact MFR name like `BSS84`)
5. **Check all three tier boxes**: Basic, Preferred, Extended
6. Also check **Only show parts in stock**
7. Look at the **Package** column to verify it matches your KiCad footprint
8. Pick the row with the best stock + tier
9. Click **Select part**

The LCSC number is now associated with that component.

### Phase 2: handle hand-soldered parts

Any part you intend to hand-solder after JLC assembly (microSD socket, FFC connector, pin headers, battery JST, through-hole anything) should be **excluded from both BOM and POS** so JLC neither sources nor places it.

1. Select the row in the plugin panel
2. Click **Toggle BOM POS** (or Toggle BOM + Toggle POS individually)
3. The BOM and POS columns should flip to red X marks
4. Leave the LCSC field empty or as-is; the exclusion is what matters

A separate column called **POP** (Place On PCB) shows whether JLC's machines can actually assemble the part. POP = X means the part is sourceable but not assembleable; fix by picking a different LCSC part or accept the part as hand-soldered.

### Phase 3: tier and stock sanity pass

Before generating, scan the panel for risk patterns:

- Count rows with **Type = Extended**. Each one adds **$3 setup fee** to your order. Worth checking if a Basic-tier equivalent exists.
- Look for rows with **Stock < 1000**. Those parts can go out of stock between now and when JLC places the order. Substitute if possible.
- Spot-check **value vs LCSC Params**. The schematic value (e.g. "10k") should match the LCSC part description (e.g. "10kΩ ±1% 0603"). Mismatches are silent assembly bugs.

### Phase 4: save and export

1. **Save mappings** (button on the right side of the plugin panel). This writes your LCSC choices into the plugin's database for re-use across projects.
2. **Export to schematic**. This writes the LCSC field into each component's symbol in the schematic file.
3. Open the **Schematic Editor** and press **Ctrl+S** to actually save the schematic file (this is the step people miss; the export-to-schematic only marks the file as modified)

### Phase 5: generate fab files

Back in the PCB editor JLCPCB plugin panel:

1. Click **Generate fabrication files for JLCPCB** (top-left button)
2. The plugin creates a `jlcpcb/` directory next to your `.kicad_pcb` file containing:

```
jlcpcb/
|-- gerber/                                       individual Gerber + drill files
`-- production_files/
    |-- GERBER-<projectname>.zip                  what you upload
    |-- BOM-<projectname>.csv                     BOM with LCSC numbers
    `-- CPL-<projectname>.csv                     pick-and-place coordinates
```

3. **Open and verify** the BOM and CPL CSVs:
   - BOM: every row should have a non-empty LCSC column (Cxxxxx format)
   - BOM: hand-soldered parts should be **absent** from the list
   - CPL: same set of designators as the BOM
   - Spot-check one or two rotation values against the part's datasheet pin-1 orientation (the plugin applies JLC's known rotation corrections automatically; this is a sanity check, not a fix)

---

## Uploading to JLCPCB

Order page: https://jlcpcb.com/quote

1. Drag the `GERBER-<projectname>.zip` into the gerber upload field
2. JLCPCB reads the gerbers and shows a board preview. Verify board outline, layer count, dimensions, drill positions.
3. Choose your PCB options (layers, thickness, color, surface finish, etc.)
4. Toggle on **PCB Assembly**. Pick:
   - **Assembly Side**: single-side (TOP) by default. Choose double-side only if you have BOT components that need SMT placement.
   - **Tooling holes**: per JLCPCB's recommendation
   - **Confirm parts placement**: yes (gives you a final visual review)
5. Upload the **BOM** CSV when prompted
6. Upload the **CPL** CSV when prompted
7. JLC processes the files. Within ~30 minutes you receive a **parts placement preview** email asking you to confirm rotations and positions before they cut metal.

**Always review the placement preview.** This is where rotation errors are caught (e.g., a SOT-23 placed 180 degrees rotated would short power to ground). If anything looks wrong, the plugin's rotation correction is the most common cause; adjust in KiCad, regenerate, re-upload.

---

## BOM presentation in a public repo

A common ask for an open-hardware project: the repo's BOM should be readable by people who are not going to fab the board, while the BOM JLC actually uses needs to be machine-readable and accurate.

Two-file pattern:

| File | Audience | Source of truth? |
|---|---|---|
| `jlcpcb/production_files/BOM-<projectname>.csv` | JLCPCB | **Yes**, this is what they assemble from. Do not hand-edit; regenerate from the plugin. |
| Optional `BOM/Hand-Solder-Notes.md` or repo README section | Humans browsing the repo | Human-friendly notes about what is hand-soldered and why |

The plugin-generated BOM **only includes parts JLC will assemble**, which is what you want for the manufacturer. Hand-soldered parts get documented separately as prose, with the canonical list living in the revision's README (e.g. `KiCad/OM-FlexGrid V4/README.md` → "Hand-soldered parts").

---

## Tips earned the hard way

- **Avoid "Auto-select alike"** as a bulk action. It groups parts by footprint, not value, and will happily tag every 0603 resistor with the same LCSC number regardless of resistance. Tag manually one value at a time.
- **Check the Package column on every search result.** Same MFR number can come in different packages; SOT-23 vs SOT-323 vs TSOT-23 look similar in name but have different pad geometry.
- **TSOT-23-6 is pad-compatible with SOT-23-6**, same pitch + same pad layout, just thinner profile. A common gotcha when a part is only available in TSOT.
- **SOD-123FL is NOT pad-compatible with SOD-123**, different pad geometry. Check before assuming.
- **Basic and Preferred tiers have no setup fee**, Extended has $3 per unique part. A board with 5 Extended-tier parts costs $15 more in setup than a board with 5 Basic equivalents. Worth optimizing for.
- **The "Save mappings" plugin database** remembers your choices across projects. After you have tagged a bunch of common values once, future projects auto-suggest the same LCSC parts.
- **POP = X in the plugin** means JLC can source the part but cannot auto-place it. Pick a different LCSC part; do not just ignore the warning, the assembly will not happen.
- **For double-side assembly**, JLC charges meaningfully more than single-side. If your BOT side has only one or two SMD parts, consider moving them to TOP in the next revision.

---

## Workflow checklist (copy this into the revision's commit message)

```
[ ] Every component tagged with an LCSC part number (or explicitly excluded)
[ ] All hand-soldered parts have BOM and POS toggled OFF
[ ] No POP = X warnings remaining (or accepted as hand-soldered)
[ ] Tier mix is acceptable (counted Extended-tier parts, weighed setup cost)
[ ] Stock levels checked (no parts at < 1000 in stock)
[ ] Mappings saved + exported to schematic + schematic saved
[ ] Fab files regenerated AFTER schematic save
[ ] BOM CSV manually inspected (LCSC values present, hand-solder parts absent)
[ ] CPL CSV manually inspected (designators match BOM, rotations sane)
[ ] 3D STEP exported for mechanical fit check (if board lives in an enclosure)
```
