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
| [`KiCad/OM-FlexGrid V0/OM-60-Flex/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/OM-FlexGrid%20V0/OM-60-Flex) | Flexible PCB sensor matrix (wraps around forearm) |
| [`KiCad/OM-FlexGrid V0/OM-60-Rigid-PCB/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/OM-FlexGrid%20V0/OM-60-Rigid-PCB) | Rigid microcontroller and connector breakout PCB |
| [`KiCad/OM-FlexGrid V0/OM-60-Flex/V1 Gerber/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/OM-FlexGrid%20V0/OM-60-Flex/V1%20Gerber) | Fabrication files for the flexible PCB |
| [`KiCad/OM-FlexGrid V0/OM-60-Rigid-PCB/OM-60-Rigid-Gerber/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/KiCad/OM-FlexGrid%20V0/OM-60-Rigid-PCB/OM-60-Rigid-Gerber) | Fabrication files for the rigid PCB |

> Current version: **v0 (prototype)**  
> Next planned version: **v1.0 – improved sensor headers and trace layout**

---

### 📦 Bill of Materials

📂 [`BOM/`](https://github.com/Open-Muscle/OpenMuscle-FlexGrid/tree/main/BOM)

Each subfolder contains BOM spreadsheets for its respective board.  
Format: CSV or XLSX, with part numbers and source links.

---

### 🛠 Assembly & Testing

Instructions for soldering, testing, and integrating the FlexGrid with ESP32-S3 firmware are in development. For now, please refer to the [OpenMuscle Hub](https://github.com/Open-Muscle/OpenMuscle-Hub) and follow updates on [YouTube Open Muscle](https://youtube.com/@openmuscle) or [TURFPTAx Youtube](https://youtube.com/@turfptax).

---

## 🤝 Contributions

We welcome improvements to sensor design, firmware, or real-world testing. Please fork the repo and submit pull requests!

---
**Open Muscle** is an open-source prosthetic sensor initiative designed for accessibility, innovation, and community collaboration.
