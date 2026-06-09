# 🧠 OpenMuscle-FlexGrid

![Latest stable: V3 (validated)](https://img.shields.io/badge/stable-V3%20%28validated%29-green)
![In development: V4](https://img.shields.io/badge/in--development-V4-yellow)
![License: CERN-OHL-S-2.0](https://img.shields.io/badge/license-CERN--OHL--S--2.0-blue)
![MCU: ESP32-S3](https://img.shields.io/badge/MCU-ESP32--S3-blue)

OpenMuscle FlexGrid is a modular 60-sensor pressure-sensing platform designed for advanced forearm-based gesture tracking and biomechanical research.

This device is part of the [OpenMuscle](https://github.com/Open-Muscle) ecosystem and represents a leap forward from the original 12-sensor OM12 prototype by introducing high-density, flex-rigid PCBs and better sensor modularity.

### 📌 For documentation, firmware, and assembly guidance, visit the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub).

---

## 🚀 Current revisions

**V4 (in development, 2026-06).** Ready for fab. Adds an on-device **microSD card socket** for local data logging, a **discrete RGB status LED** on three PWM channels, and a reoriented slimmer board profile that hugs the forearm. Carries forward the V3 power and interconnect architecture, but with the FFC tail width corrected from 11.1 mm to **10.5 mm** per the Wurth 687120183722 datasheet, the ADC matrix-row caps reduced from 2.2 uF to **100 pF** (resolves V3's 22 ms RC bleed in silicon rather than via post-fab cap removal), all resistors normalized to 0603, and several footprint cleanups. Manufacturing strategy: **single-side SMT at JLCPCB for an initial batch of 10 units, plus hand-soldering of bottom-side parts and through-hole connectors at home**. Not yet ordered, not yet brought up. Full status and pre-fab checklist in the [V4 README](KiCad/OM-FlexGrid%20V4/README.md).

**V3 (stable, 2026-05-13).** First revision to use a 20-pin ZIF FFC connector for the flex-to-rigid interconnect (Wurth 687120183722). Two boards populated and tested end-to-end. Sensor matrix delivers **clean single-cell press detection across all 60 sensors** with ~22% carryover decaying to noise floor within 3 columns. **V3 is the first FlexGrid generation usable as a real ML training data source.** Firmware: [FlexGridV3-Firmware v0.1.7](https://github.com/Open-Muscle/FlexGridV3-Firmware).

→ For V4 hardware files, see [`KiCad/OM-FlexGrid V4/`](KiCad/OM-FlexGrid%20V4/) and the [V4 README](KiCad/OM-FlexGrid%20V4/README.md). For V3 see [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) and the [V3 README](KiCad/OM-FlexGrid%20V3/README.md). The MicroPython firmware that runs on V3 (and will be ported to V4) lives at [FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware).

| Revision | Status | Notes |
|----------|--------|-------|
| **V4** | 🟡 In development | microSD + RGB LED + slimmer reorient; 10.5 mm FFC tail; 100 pF ADC caps; not yet fabbed |
| **V3** | 🟢 Validated | 20-pin FFC interconnect, integrated stiffened FFC tail, ~140 Hz raw scan |
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
| **V4** (in dev) | [`KiCad/OM-FlexGrid V4/`](KiCad/OM-FlexGrid%20V4/) | microSD socket, RGB status LED, slimmer reorient, 10.5 mm FFC tail, 100 pF ADC caps. See [V4 README](KiCad/OM-FlexGrid%20V4/README.md). |
| **V3** (stable) | [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) | Validated. 20-pin ZIF FFC interconnect. See [V3 README](KiCad/OM-FlexGrid%20V3/README.md). |
| V2 | [`KiCad/OM-FlexGrid V2/`](KiCad/OM-FlexGrid%20V2/) | Tested. FFC exploration + fabric harness. See [V2 README](KiCad/OM-FlexGrid%20V2/README.md). |
| V1 | [`KiCad/OM-FlexGrid V1/`](KiCad/OM-FlexGrid%20V1/) | First production revision. |
| V0 | [`KiCad/OM-FlexGrid V0/`](KiCad/OM-FlexGrid%20V0/) | Original prototype. |

Each revision folder contains both the flex (`OM-FlexGrid-Flex/`) and rigid (`OM-FlexGrid-Rigid-PCB/`) board projects, plus their gerber bundles.

---

### 📦 Bill of Materials

BOMs live next to their KiCad project for each revision:

- **V4 Rigid (JLCPCB-ready):** [`KiCad/OM-FlexGrid V4/OM-FlexGrid-Rigid-PCB/jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv`](KiCad/OM-FlexGrid%20V4/OM-FlexGrid-Rigid-PCB/jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv) (LCSC part numbers, machine-readable, generated by the JLCPCB KiCad plugin). The hand-soldered parts list (microSD socket, FFC connector, battery JST, pin headers, plus single-side-strategy BOT-side SMT) is documented prose-style in the [V4 README](KiCad/OM-FlexGrid%20V4/README.md#hand-soldered-parts-full-list).
- **V3 Rigid:** [`KiCad/OM-FlexGrid V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv`](KiCad/OM-FlexGrid%20V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv) (KiCad export).
- **Flex (V3 and V4):** no electronic-component BOM. The flex tail integrates the FFC connector pads directly; the only off-board parts are the Velostat sheet and the mating Wurth 687120183722 connector populated on the rigid board.

Older revision BOMs are kept under [`BOM/`](BOM/) for history.

---

### 🛠 Assembly & Testing

Instructions for soldering, testing, and integrating the FlexGrid with ESP32-S3 firmware are in development. For now, please refer to the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub) and follow updates on [YouTube Open Muscle](https://youtube.com/@openmuscle) or [TURFPTAx Youtube](https://youtube.com/@turfptax).

---

## 🤝 Contributions

We welcome improvements to sensor design, firmware, or real-world testing. Please fork the repo and submit pull requests!

---
**Open Muscle** is an open-source prosthetic sensor initiative designed for accessibility, innovation, and community collaboration.
