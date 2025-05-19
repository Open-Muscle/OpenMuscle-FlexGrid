# 🧠 OpenMuscle-FlexGrid

![Status: Prototype](https://img.shields.io/badge/status-prototype-orange)
![License: CERN-OHL-S-2.0](https://img.shields.io/badge/license-CERN--OHL--S--2.0-blue)
![MCU: ESP32-S3](https://img.shields.io/badge/MCU-ESP32--S3-blue)

OpenMuscle FlexGrid is a modular 60-sensor pressure-sensing platform designed for advanced forearm-based gesture tracking and biomechanical research.

This device is part of the [OpenMuscle](https://github.com/Open-Muscle) ecosystem and represents a leap forward from the original 12-sensor OM12 prototype by introducing high-density, flex-rigid PCBs and better sensor modularity.


### 📌 For documentation, firmware, and assembly guidance, visit the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub).


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

📂 [`KiCad/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad)

| Subfolder | Description |
|-----------|-------------|
| [`KiCad/flex/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/flex) | Flexible PCB with sensor traces (wraps around the forearm) |
| [`KiCad/rigid/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/rigid) | Rigid controller PCB with MCU, power, and connectors |

> Current version: **v0.0 (prototype)**  
> Next planned version: **v1.0 – integrated headers, optimized traces**

---

### 📦 Bill of Materials

📂 [`BOM/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/BOM)

Each subfolder contains BOM spreadsheets for its respective board.  
Format: CSV or
