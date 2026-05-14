# 🧠 OpenMuscle-FlexGrid

![Latest: V3 (validated)](https://img.shields.io/badge/latest-V3%20%E2%80%94%20validated-green)
![License: CERN-OHL-S-2.0](https://img.shields.io/badge/license-CERN--OHL--S--2.0-blue)
![MCU: ESP32-S3](https://img.shields.io/badge/MCU-ESP32--S3-blue)

OpenMuscle FlexGrid is a modular 60-sensor pressure-sensing platform designed for advanced forearm-based gesture tracking and biomechanical research.

This device is part of the [OpenMuscle](https://github.com/Open-Muscle) ecosystem and represents a leap forward from the original 12-sensor OM12 prototype by introducing high-density, flex-rigid PCBs and better sensor modularity.

### 📌 For documentation, firmware, and assembly guidance, visit the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub).

---

## 🚀 Latest revision

**V3 — production-quality matrix as of 2026-05-13.** First revision to use a 20-pin ZIF FFC connector for the flex-to-rigid interconnect (Wurth 687120183722). Two boards populated and tested end-to-end. Sensor matrix delivers **clean single-cell press detection across all 60 sensors** with ~22% carryover decaying to noise floor within 3 columns. **V3 is the first FlexGrid generation usable as a real ML training data source.** Firmware: [FlexGridV3-Firmware v0.1.7](https://github.com/Open-Muscle/FlexGridV3-Firmware).

→ See [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) for hardware files, the [V3 hardware README](KiCad/OM-FlexGrid%20V3/README.md) for build notes, and the [FlexGridV3-Firmware repo](https://github.com/Open-Muscle/FlexGridV3-Firmware) for the MicroPython firmware that runs on it.

| Revision | Status | Notes |
|----------|--------|-------|
| **V3** | 🟢 Validated | 20-pin FFC interconnect, integrated stiffened FFC tail, ~140 Hz raw scan |
| V2 | 🟢 Tested | FFC connector exploration, fabric harness testing |
| V1 | 🟢 Tested | First production revision |
| V0 | 🟢 Tested | Original prototype |

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
| **V3** (latest) | [`KiCad/OM-FlexGrid V3/`](KiCad/OM-FlexGrid%20V3/) | Current design — 20-pin ZIF FFC interconnect. See [V3 README](KiCad/OM-FlexGrid%20V3/README.md). |
| V2 | [`KiCad/OM-FlexGrid V2/`](KiCad/OM-FlexGrid%20V2/) | Tested. FFC exploration + fabric harness. See [V2 README](KiCad/OM-FlexGrid%20V2/README.md). |
| V1 | [`KiCad/OM-FlexGrid V1/`](KiCad/OM-FlexGrid%20V1/) | First production revision. |
| V0 | [`KiCad/OM-FlexGrid V0/`](KiCad/OM-FlexGrid%20V0/) | Original prototype. |

Each revision folder contains both the flex (`OM-FlexGrid-Flex/`) and rigid (`OM-FlexGrid-Rigid-PCB/`) board projects, plus their gerber bundles.

---

### 📦 Bill of Materials

The current BOM lives next to its KiCad project for each revision:

- **V3 Rigid:** [`KiCad/OM-FlexGrid V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv`](KiCad/OM-FlexGrid%20V3/OM-FlexGrid-Rigid-PCB/OM-FlexGrid-Rigid-PCB.csv) (KiCad export)
- **V3 Flex:** no electronic-component BOM — the flex tail integrates the FFC connector pads directly; the only off-board parts are the Velostat sheet and the mating Wurth 687120183722 connector populated on the rigid board.

Older revision BOMs are kept under [`BOM/`](BOM/) for history.

---

### 🛠 Assembly & Testing

Instructions for soldering, testing, and integrating the FlexGrid with ESP32-S3 firmware are in development. For now, please refer to the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub) and follow updates on [YouTube Open Muscle](https://youtube.com/@openmuscle) or [TURFPTAx Youtube](https://youtube.com/@turfptax).

---

## 🤝 Contributions

We welcome improvements to sensor design, firmware, or real-world testing. Please fork the repo and submit pull requests!

---
**Open Muscle** is an open-source prosthetic sensor initiative designed for accessibility, innovation, and community collaboration.
