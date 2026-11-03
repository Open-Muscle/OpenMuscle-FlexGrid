# 🧠 OpenMuscle-FlexGrid

![Current: V4 (validated)](https://img.shields.io/badge/current-V4%20%28validated%29-green)
![Previous: V3 (validated)](https://img.shields.io/badge/previous-V3%20%28validated%29-lightgrey)
![License: CERN-OHL-S-2.0](https://img.shields.io/badge/license-CERN--OHL--S--2.0-blue)
![MCU: ESP32-S3](https://img.shields.io/badge/MCU-ESP32--S3-blue)

OpenMuscle FlexGrid is a modular 60-sensor pressure-sensing platform designed for advanced forearm-based gesture tracking and biomechanical research.

This device is part of the [OpenMuscle](https://github.com/Open-Muscle) ecosystem and represents a leap forward from the original 12-sensor OM12 prototype by introducing high-density, flex-rigid PCBs and better sensor modularity.

### 📌 For documentation, firmware, and assembly guidance, visit the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub).

---

## 🚀 Current revisions

**V4 (current, validated).** Fabricated at JLCPCB in June 2026 (10-unit batch, single-side SMT), brought up 2026-06-23 and in use since. Two V4 bands were assembled, flashed with [FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware) v4.0.1 and shipped as the first OpenMuscle starter kit in October 2026. V4 is the best-performing FlexGrid revision to date and the one to build. It adds an on-device **microSD card socket** for local data logging, a **discrete RGB status LED** on three PWM channels, and a reoriented slimmer board profile that hugs the forearm. It carries forward the V3 power and interconnect architecture, with the FFC tail width corrected from 11.1 mm to **10.5 mm** per the Wurth 687120183722 datasheet, the ADC matrix-row caps reduced from 2.2 uF to **100 pF** (resolves V3's 22 ms RC bleed in silicon rather than via post-fab cap removal), all resistors normalized to 0603, and several footprint cleanups. Manufacturing strategy: **single-side SMT at JLCPCB plus hand-soldering of bottom-side parts and through-hole connectors**. The design files are now at board revision **V4-2** (2026-11-03): USB presence sensing for the firmware, vias moved out of the SMD pads, USB data lines re-routed as a pair. V4-2 has not been fabricated yet, and its BOM, placement and Gerber files are still the June 2026 as-ordered set. Full status, bring-up findings and the fab checklist are in the [V4 README](KiCad/OM-FlexGrid%20V4/README.md).

**V3 (previous, validated 2026-05-13).** First revision to use a 20-pin ZIF FFC connector for the flex-to-rigid interconnect (Wurth 687120183722). Two boards populated and tested end-to-end. Sensor matrix delivers **clean single-cell press detection across all 60 sensors** with ~22% carryover decaying to noise floor within 3 columns. **V3 is the first FlexGrid generation usable as a real ML training data source.** Firmware: [FlexGridV3-Firmware v0.1.7](https://github.com/Open-Muscle/FlexGridV3-Firmware).

→ For V4 hardware files, see [`KiCad/OM-FlexGrid V4/`](KiCad/OM-FlexGrid%20V4/) and the [V4 README](KiCad/OM-FlexGrid%20V4/README.md). For V3 see [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) and the [V3 README](KiCad/OM-FlexGrid%20V3/README.md). Firmware: V4 bands run [FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware); V3 boards run [FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware).

| Revision | Status | Notes |
|----------|--------|-------|
| **V4** | 🟢 Validated (current) | microSD + RGB LED + slimmer reorient; 10.5 mm FFC tail; 100 pF ADC caps; fabbed 2026-06, in starter kits since 2026-10; design files at V4-2 (USB sensing, vias out of pads, USB pair; not yet fabbed) |
| **V3** | 🟢 Validated (previous) | 20-pin FFC interconnect, integrated stiffened FFC tail, ~140 Hz raw scan |
| V2 | 🟢 Tested | FFC connector exploration, fabric harness testing |
| V1 | 🟢 Tested | First production revision |
| V0 | 🟢 Tested | Original prototype |

→ Full cross-version comparison: [`KiCad/REVISIONS.md`](KiCad/REVISIONS.md). Manufacturing process used across revisions: [`docs/JLCPCB_WORKFLOW.md`](docs/JLCPCB_WORKFLOW.md).

---

## 🧬 Overview

FlexGrid uses a flexible pressure sensor matrix with rigid breakout interfaces to detect volumetric muscle contractions in real time. It supports:

- 🧠 Biomechanical signal analysis  
- 🦾 Prosthetics and exosuit research  
- 🎛️ Machine learning data pipelines  

---

## 📁 Hardware Design Files

Design files are organized by board type and version:

### 🔌 KiCad Schematics & PCB Layout

📂 [`KiCad/`](KiCad/) — all design files, organized by revision.

| Revision | Path | Description |
|----------|------|-------------|
| **V4** (current) | [`KiCad/OM-FlexGrid V4/`](KiCad/OM-FlexGrid%20V4/) | Validated. microSD socket, RGB status LED, slimmer reorient, 10.5 mm FFC tail, 100 pF ADC caps. See [V4 README](KiCad/OM-FlexGrid%20V4/README.md). |
| **V3** (previous) | [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) | Validated. 20-pin ZIF FFC interconnect. See [V3 README](KiCad/OM-FlexGrid%20V3/README.md). |
| V2 | [`KiCad/OM-FlexGrid V2/`](KiCad/OM-FlexGrid%20V2/) | Tested. FFC exploration + fabric harness. See [V2 README](KiCad/OM-FlexGrid%20V2/README.md). |
| V1 | [`KiCad/OM-FlexGrid V1/`](KiCad/OM-FlexGrid%20V1/) | First production revision. |
| V0 | [`KiCad/OM-FlexGrid V0/`](KiCad/OM-FlexGrid%20V0/) | Original prototype. |

Each revision folder contains both the flex (`OM-FlexGrid-Flex/`) and rigid (`OM-FlexGrid-Rigid-PCB/`) board projects, plus their gerber bundles.

---

### 📦 Bill of Materials

BOMs live next to their KiCad project for each revision:

- **V4 Rigid (JLCPCB-ready):** [`KiCad/OM-FlexGrid V4/OM-FlexGrid-Rigid-PCB/jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv`](KiCad/OM-FlexGrid%20V4/OM-FlexGrid-Rigid-PCB/jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv) (LCSC part numbers, machine-readable, generated by the JLCPCB KiCad plugin). This is the June 2026 as-ordered V4 set; the V4-2 additions (R19, R20, R21) are not in it yet. The hand-soldered parts list (microSD socket, FFC connector, battery JST, pin headers, plus single-side-strategy BOT-side SMT) is documented prose-style in the [V4 README](KiCad/OM-FlexGrid%20V4/README.md#hand-soldered-parts-full-list).
- **V3 Rigid:** [`KiCad/OM-FlexGrid V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv`](KiCad/OM-FlexGrid%20V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv) (KiCad export).
- **Flex (V3 and V4):** no electronic-component BOM. The flex tail integrates the FFC connector pads directly; the only off-board parts are the Velostat sheet and the mating Wurth 687120183722 connector populated on the rigid board.

Older revision BOMs are kept under [`BOM/`](BOM/) for history.

---

### 🛠 Assembly & Testing

For V4: the [build video](https://youtu.be/2tb6GW4FNU0) covers hand-soldering the parts JLCPCB does not populate, [BRINGUP.md](https://github.com/Open-Muscle/FlexGridV4-Firmware/blob/main/BRINGUP.md) in the firmware repo covers flashing, and the [band reference](https://github.com/Open-Muscle/FlexGridV4-Firmware/blob/main/docs/device-reference.md) explains every button and light pattern. Recording, training and inference software lives in [OpenMuscle-Software](https://github.com/Open-Muscle/OpenMuscle-Software). For the wider picture see the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub) and the videos on [YouTube Open Muscle](https://youtube.com/@openmuscle) or [TURFPTAx Youtube](https://youtube.com/@turfptax).

---

## 🤝 Contributions

We welcome improvements to sensor design, firmware, or real-world testing. Please fork the repo and submit pull requests!

---
**Open Muscle** is an open-source prosthetic sensor initiative designed for accessibility, innovation, and community collaboration.
