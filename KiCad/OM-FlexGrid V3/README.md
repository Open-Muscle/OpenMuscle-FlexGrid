# OM-FlexGrid V3

> **Status: VALIDATED (as of 2026-05-13).** Two boards populated and brought up end-to-end. The Wurth 687120183722 FFC interconnect mates cleanly with the integrated stiffened flex tail (0.20 mm FR4 stiffener, bottom-side, total ~0.31 mm — on Wurth's 0.30 ±0.05 mm spec). Sensor matrix scans at ~75 Hz with no row-sneak crosstalk, no scan-direction bleed, and isolated single-cell response under a single-column Velostat strip press test. UDP telemetry over Wi-Fi confirmed reaching the desktop visualizer (`openmuscle web` and `openmuscle receive`). **V3 is the first revision where the flex↔rigid interconnect is no longer the project's main signal-quality problem** — the original goal of the revision is met.
>
> Firmware that makes this work lives at [Open-Muscle/FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware) (v0.1.6, MIT). Five non-obvious scan techniques were needed; they're documented in that repo's `README` under "Sensor scan techniques".
>
> Open items: characterizing one occasionally-glitchy sensor on board #1; diagnosing IO2 (= ROW_1) GPIO-output anomaly on board #1 (suspect R13 or its trace); ICM-42688-P IMU driver still TODO.

Third major revision of the Open Muscle FlexGrid wearable sensor platform. V3 standardizes the flex-to-rigid interconnect on a 20-pin 0.5 mm-pitch ZIF FFC connector, eliminating the hand-soldered pin-header link used through V2.

---

## Overview

V3 is two paired PCBs, mated by a single FFC ribbon formed by the flex PCB's own tail.

| Board | Role | Layers | Mating |
|-------|------|--------|--------|
| **OM-FlexGrid-Flex** | 15×4 Velostat sensor matrix on a flex PCB. The PCB tail itself is the male FFC. | 2L flex | Inserts into J3 on rigid |
| **OM-FlexGrid-Rigid-PCB** | ESP32-S3 controller, mux, power, display, IMU. | 4L rigid (1.6 mm) | Hosts J3 = Wurth 687120183722 |

---

## Flex-to-Rigid Interconnect (NEW IN V3)

The flex PCB tail is fabricated with 20 exposed gold pads on the top copper layer (F.Cu) and a stiffener on the bottom. It plugs directly into the Wurth ZIF connector on the rigid board — no separate FFC cable.

### Connector (rigid side, J3)

| Field | Value |
|-------|-------|
| Manufacturer P/N | **Wurth 687120183722** |
| Mouser P/N | 710-687120183722 |
| Series | WR-FPC SMT ZIF Horizontal Low Profile |
| Pin count | 20 |
| Pitch | 0.50 mm |
| Contact orientation | **Bottom Contact** |
| Actuator | Flip-lock ZIF (top) |
| Operating temp | -25 °C to +85 °C |
| Datasheet | https://www.we-online.com/components/products/datasheet/687120183722.pdf |

"Bottom Contact" means the connector's contacts are on the underside of the housing, so **the FFC's contact pads must face the rigid PCB when inserted.**

### FFC tail (flex side, J1) — design spec

The tail is integral to the flex PCB; there is no separate FFC cable.

| Parameter | Value | Source |
|-----------|-------|--------|
| Pin count | 20 | matches J3 |
| Pitch | 0.50 mm | Wurth datasheet |
| Contact pad width | 0.30 mm | Wurth datasheet |
| Exposed contact length | 1.45 mm (min) | Wurth datasheet |
| Pin-to-pin span (centre of pin 1 → pin 20) | 9.50 mm | 19 × 0.5 mm |
| Tail width across pads | ≥ 11.10 mm | Pl + 2× 0.80 mm end margin |
| Insertion depth into housing | ~3.8 mm | Wurth datasheet |
| **Total FFC tail thickness** (flex + stiffener) | **0.30 mm ±0.05 mm** | Wurth datasheet |
| Contacts on layer | **F.Cu** (top) — must face down on insertion | KiCad project |
| Stiffener side | **B side** (opposite contacts) | required by Wurth |
| Plating | ENIG (gold) recommended | reliable mating |

### Orientation gotcha

Because the rigid connector is bottom-contact and the FFC pads are on F.Cu (top side of flex):

- During use the flex tail must enter J3 with **F.Cu facing the rigid board**.
- In the wearable, the sensor matrix sits on top of the forearm with sensor pads up; the tail folds 180° beneath the matrix and its contacts naturally end up facing down — which is what we want. Verify in the 3D view before sending to fab.

---

## Flex PCB Fabrication (JLCPCB)

These are the order parameters for JLCPCB's flex PCB service. Cross-check against `OM-FlexGrid-Flex/V2-1 Gerber.zip` (current latest) before submitting.

| Parameter | Value |
|-----------|-------|
| Layers | 2 |
| Material | Polyimide flex |
| Base thickness | 0.11 mm (JLCPCB default 2L) |
| Coverlay | Yellow polyimide (default) |
| Surface finish | **ENIG** (required for reliable FFC mating; HASL will not work) |
| Copper weight | 1 oz (0.5 oz also fine) |
| **Stiffener material** | **FR4** |
| **Stiffener thickness** | **0.20 mm** |
| **Stiffener side** | **Bottom** (opposite the FFC contacts) |
| Stiffener placement | Drawn on `User.1 (Stiffener)` layer in KiCad |
| EMI shielding | None |
| 3M tape backing | Optional (none required for FFC) |

**Total FFC tail thickness = 0.11 mm flex + 0.20 mm stiffener ≈ 0.31 mm** ✓ within Wurth's 0.30 ±0.05 mm window.

### Stiffener outline rules

The stiffener is a rectangular FR4 backer bonded to the bottom side of the flex tail. JLCPCB needs an outline drawn on a dedicated layer so they know where to glue it.

- Layer: `User.1` (already named "Stiffener" in `OM-FlexGrid-Flex.kicad_pcb`).
- Shape: rectangle covering the **full width of the FFC tail** and extending from the **board edge** at least **5 mm past the last contact pad** (≈ 7 mm total length is typical). This puts the entire ZIF clamp area on stiffener.
- Do not let the stiffener cross the bend region of the flex — keep it confined to the tail.
- When uploading to JLCPCB, in the order form select stiffener side = **Bottom side**, material = **FR4**, thickness = **0.2 mm**.

### Notes on the current J1 footprint

`OpenMuscleDevKit:20Pin-FFC` (used as J1) has 20 pads at 0.5 mm pitch, 0.30 × 2.60 mm each, on F.Cu — geometry matches Wurth's recommended FFC pattern. Two items to confirm before fab:

1. **Soldermask opening** on the contact area should match or exceed the 1.45 mm exposed-contact length (KiCad's mask expansion typically handles this; verify in F.Mask).
2. **Stiffener layer is currently empty** — there is no shape drawn on `User.1`. You need to add a rectangle there before generating new gerbers, otherwise JLCPCB has no stiffener outline to follow. The previous V2-1 gerber already includes `OM-FlexGrid-Flex-Stiffener.gbr`, so the stiffener was authored as a separate file last round; either re-import it onto User.1 or redraw it.

---

## Rigid PCB

4-layer, 1.6 mm, ESP32-S3 host. No architectural changes from V2. See `OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv` for the full BOM.

### Key components

| Ref | Component | Function |
|-----|-----------|----------|
| U? | ESP32-S3-WROOM-1-N16R8 | MCU (16 MB Flash, 8 MB PSRAM) |
| MUX | CD74HC4067 | 16:1 analog mux (15 columns used) |
| OLED | SSD1306 128×32 | I²C status display |
| IC1 | ICM-42688-P | 6-DOF IMU (I²C, optional) |
| MAX1 | MAX16054 | Soft power latch |
| — | TPS7A0333 | 3.3 V LDO |
| — | LTC4054ES5 | Single-cell LiPo charger |
| Q1, Q3 | IRLML2060 | Haptic motor / aux MOSFET |
| **J3** | **Wurth 687120183722** | **20-pin ZIF, FFC to flex matrix** |
| J4 | USB-C (HRO TYPE-C-31-M-12) | Charge / programming |

### Sensor matrix scan

CD74HC4067 walks 15 columns to 3.3 V one at a time; four row lines with 10 kΩ pulldowns are sampled on ESP32 ADC1. 60 readings per scan frame.

---

## Bring-up findings (2026-05-13)

Five firmware-side issues had to be solved before the matrix produced clean data. They're all documented in detail in the [firmware repo's README](https://github.com/Open-Muscle/FlexGridV3-Firmware#sensor-scan-techniques), but the hardware-relevant takeaways are:

| Issue | Root cause | Where the fix lives |
|---|---|---|
| Row sneak path — press lights up whole row | CD74HC4067 unselected channels are high-Z; press on one cell forms a sneak path through other pressed cells via the floating columns | Firmware: drive non-target rows to OUTPUT LOW while reading the target row |
| Mux address glitches kick energy into pressed column | MicroPython `Pin.value()` is ~1 µs and S0–S3 update non-atomically; HC4067 settles in 80 ns and routes intermediate addresses | Firmware: raise mux `E` (disable) before changing address, lower it after |
| Scan-direction bleed (right of pressed cell) | ADC sample-and-hold cap holds the previous cell's voltage; first read after `Pin.init()` mode change returns a stale sample | Firmware: 30 µs row discharge + discard-first-read |
| Slow Wi-Fi join → permanent UDP silence | `connect()` blocked for 20 s, then `RuntimeError` skipped socket creation | Firmware: create UDP socket in `__init__` |
| `openmuscle receive` heatmap silently dropped V3 packets | Viz hardcoded 16-column matrix; V3 sends 15 | Host: shape auto-detection in [OpenMuscle-Software](https://github.com/Open-Muscle/OpenMuscle-Software) |

**One open hardware finding** worth chasing on the next revision or as a follow-up on board #1: **GPIO 2 (ROW_1) does not drive HIGH cleanly.** When the firmware sets the pin to `Pin.OUT(value=1)`, the ADC reads back ~55 (≈ 0 V) instead of the expected ~3100. Other rows on the same board behave normally. Suspect a bad solder joint on R13 (the 10 kΩ pulldown for ROW_1) or a local trace short. Doesn't break the scan (the pin still works as an ADC input and reaches GND well enough for the ground-other-rows trick), but worth probing with a multimeter.

## Design suggestions for V4

Captured here so they don't get lost. None of these are *needed* — V3 works — but they'd make the next revision easier to bring up and more robust:

- **Per-row series resistor (~100 Ω–1 kΩ)** between each ROW_N net and the ESP32 ADC pin. Limits short-circuit current if a row is accidentally driven high while a column is also high, and dampens RC oscillations on long traces. Cheap insurance.
- **Pick row GPIOs from outside ADC1 if possible**, OR accept the ADC-sharing quirks documented above. ESP32-S3 GPIO1–10 are ADC1-shared and have the SAH-stale-sample behavior. If you only need 4 row ADCs, IO11–IO20 (ADC2) work too, with the caveat that ADC2 conflicts with Wi-Fi RF — so only sample when Wi-Fi is idle, or stay on ADC1 and use the discard-first-read trick from V3 firmware.
- **Move the BOOT button further from the FFC connector** so accidental flex pressure or a stray tool tip can't depress it during assembly. The "stuck in download mode at boot" failure mode bit us on V3 bring-up.
- **Consider per-cell Velostat patches** instead of one continuous sheet, or a thin spacer mask with cell-sized holes, to reduce mechanical bleed between adjacent cells. The firmware fixes only kill electrical bleed; Velostat compression spreads laterally as a material property.
- **Label the FFC pin 1 marker on the silkscreen for both flex and rigid.** Both V3 footprints turned out to be internally consistent, but the schematic-only review process couldn't easily confirm that — silkscreen markers make the inspection trivial.
- **Add test pads** on the four row nets (ROW_0–ROW_3), the four mux address lines (S0–S3), and the mux `E`. Makes scope/multimeter probing during bring-up much easier than soldering wires to 0603s.

## V3 release files (sent to fab 2026-04-25)

| Board | Source | Gerber bundle | BOM |
|-------|--------|---------------|-----|
| Flex | `OM-FlexGrid-Flex/OM-FlexGrid-Flex.kicad_*` | `OM-FlexGrid-Flex/V3 Flex PCB Gerber.zip` | n/a (no electronic components — integrated FFC tail only) |
| Rigid | `OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.kicad_*` | `OM-FlexGrid-Rigid-PCB/V3 Rigid PCB Gerber.zip` | `OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv` |

Schematic PDFs (export instructions below) live in `Schematics/` at the repo root.

### Repository layout (V3)

```
OM-FlexGrid V3/
├── README.md                              # this file
├── OM-FlexGrid-Flex/
│   ├── OM-FlexGrid-Flex.kicad_sch
│   ├── OM-FlexGrid-Flex.kicad_pcb
│   ├── OM-FlexGrid-Flex.kicad_pro
│   ├── V3 Flex PCB Gerber.zip             # ← V3 release gerbers
│   ├── V3 Flex PCB Gerber/                # ← unzipped gerbers (incl. Stiffener.gbr)
│   ├── FlexStiff.stl                      # 3D model of stiffener (reference)
│   └── (older V1/V2 Gerber folders kept for history)
└── OM-FlexGrid-Rigid-PCB/
    ├── OM-FlexGrid-Rigid-PCB.kicad_sch
    ├── OM-FlexGrid-Rigid-PCB.kicad_pcb
    ├── OM-FlexGrid-Rigid-PCB.kicad_pro
    ├── OM-FlexGrid-Rigid-PCB.step
    ├── OM-FlexGrid-Rigid-PCB.csv          # BOM (KiCad export)
    ├── V3 Rigid PCB Gerber.zip            # ← V3 release gerbers
    └── V3 Rigid PCB Gerber/               # ← unzipped gerbers
```

### How to regenerate the schematic PDFs

In KiCad's Schematic Editor (`OM-FlexGrid-*.kicad_sch`):

1. *File → Plot…*
2. Output format: **PDF**
3. Output directory: `../../Schematics/` (or the repo's top-level `Schematics/` folder)
4. Filename auto-generated from project name; rename to `OM-FlexGrid-Rigid-V3.pdf` and `OM-FlexGrid-Flex-V3.pdf` after export.
5. Click **Plot All Pages** (multi-sheet) or **Plot Current Page**.

Repeat for both projects so both schematics are checked into `Schematics/` for non-KiCad readers.

---

## Pre-fab checklist

Before sending V3 to JLCPCB:

**Flex PCB**
- [ ] Stiffener rectangle drawn on `User.1` covering the full FFC tail
- [ ] J1 pads on F.Cu, F.Mask opening covers contact area
- [ ] FFC tail edge cut clean and flush at pin-1 / pin-20 datum
- [ ] Surface finish set to **ENIG** in JLCPCB order form
- [ ] Stiffener: **FR4, 0.2 mm, Bottom side**
- [ ] Verify in 3D / fold model that F.Cu of tail faces J3 host PCB

**Rigid PCB**
- [ ] J3 footprint = `OpenMuscleDevKit:687120183722-20P-Bottom` ✓ already in design
- [ ] J3 pin-to-net assignment matches J1 on flex (run ERC across boards)
- [ ] BOM line for J3 = `Wurth 687120183722` (Mouser 710-687120183722)

---

## Related Resources

- **Firmware:** https://github.com/Open-Muscle/OpenMuscle-Firmware
- **Documentation Hub:** https://github.com/Open-Muscle/OpenMuscle-Hub
- **Project Site:** https://openmuscle.org
- **Discord:** https://discord.gg/WstCaqUG63

---

## License

Hardware released under **CERN Open Hardware License v2.0 (CERN-OHL-S-2.0)**.
