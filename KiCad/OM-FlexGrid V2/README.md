# OM-FlexGrid V2

The second major revision of Open Muscle's FlexGrid wearable sensor platform. V2 includes improvements to both the flexible sensor matrix and rigid controller board.

---

## Overview

V2 consists of two paired PCBs:

| Board | Description |
|-------|-------------|
| **OM-FlexGrid-Flex** | Flexible PCB with 15×4 Velostat sensor matrix (60 sensors) |
| **OM-FlexGrid-Rigid-PCB** | Rigid controller with ESP32-S3, power management, display, and interfaces |

---

## Flex PCB (OM-FlexGrid-Flex)

The flexible sensor matrix wraps around the forearm to capture muscle pressure.

### Specifications
- **Sensor Grid:** 15 columns × 4 rows (60 total sensors)
- **Sensor Type:** Velostat pressure-sensitive pads
- **Output:** 21-pin header connecting to rigid PCB
- **Profile:** Thin, wearable design (~3mm depth with sensors)

### Files
```
OM-FlexGrid-Flex/
├── OM-FlexGrid-Flex.kicad_sch      # Schematic
├── OM-FlexGrid-Flex.kicad_pcb      # PCB layout
├── OM-FlexGrid-Flex.kicad_pro      # Project file
├── V2-1 Gerber/                    # Latest fabrication files
├── V2-1 Gerber.zip                 # Ready for manufacturing
├── FlexStiff.stl                   # 3D model for stiffener
└── *.svg                           # Outline drawings
```

---

## Rigid PCB (OM-FlexGrid-Rigid-PCB)

The main controller board handles sensor scanning, processing, display, and communication.

### MCU
- **ESP32-S3-WROOM-1-N16R8**
  - 16MB Flash / 8MB PSRAM
  - Native USB, Wi-Fi, BLE
  - 4 ADC inputs for row sensing
  - Boot/Reset via tactile switches

### Sensor Interface
- **CD74HC4067** 16-channel multiplexer
  - 15 columns active
  - Sequential scanning with 4 simultaneous row reads
  - 60 readings per scan frame

### Display & IMU
- **SSD1306** OLED 128×32 (I2C)
- **ICM-42688-P** 6-DOF IMU (I2C, optional)

### Power Management
| Component | Function |
|-----------|----------|
| TPS7A0333 | 3.3V LDO regulator |
| LTC4054ES5 | Single-cell LiPo charger |
| MAX16054 | Smart pushbutton power latch |

### User Interface
- **Buttons:** MENU, SELECT, BOOT, RESET
- **Haptic:** MOSFET-driven vibration motor (IRLML2060)
- **USB-C:** Charging, programming, serial debug

### Files
```
OM-FlexGrid-Rigid-PCB/
├── OM-FlexGrid-Rigid-PCB.kicad_sch         # Schematic
├── OM-FlexGrid-Rigid-PCB.kicad_pcb         # PCB layout
├── OM-FlexGrid-Rigid-PCB.kicad_pro         # Project file
├── OM-FlexGrid-Rigid-PCB.step              # 3D model
├── OM-FlexGrid-Rigid-PCB-Gerber-V2-1/      # Latest fabrication files
├── OM-FlexGrid-Rigid-PCB-Gerber-V2-1.zip   # Ready for manufacturing
└── OmFlexGridArtV2.svg                     # Silkscreen artwork
```

---

## V2 Development Goals

### FFC/FPC Connection Improvement
The primary focus of V2 is strengthening the FFC/FPC connection between the flex and rigid PCBs. The V1 connection was not robust enough for reliable wearable use. V2 explores connector options and mechanical reinforcement to ensure the connection holds up during daily wear and movement.

### Fabric Enclosure & Harness Testing
V2 is being tested with a custom fabric enclosure that houses both PCBs. This tests:
- Mechanical stress on board-to-board connections
- Overall harness durability
- Ergonomics and comfort during extended wear
- Real-world wearability on different forearm sizes

## Changes from V1

- Improved trace routing and signal integrity
- Updated silkscreen artwork
- Refined board outlines
- Additional Gerber iterations (V2, V2-1)
- FFC/FPC connector exploration for improved reliability

---

## Manufacturing

Use the latest Gerber ZIP files for fabrication:
- **Flex:** `V2-1 Gerber.zip` or `Gerber_OM-FlexGrid-Flex_2025-11-14.zip`
- **Rigid:** `OM-FlexGrid-Rigid-PCB-Gerber-V2-1.zip`

Recommended: Order flex PCB with stiffener using `FlexStiff.stl` dimensions.

---

## Related Resources

- **Firmware:** https://github.com/Open-Muscle/OpenMuscle-Firmware
- **Documentation Hub:** https://github.com/Open-Muscle/OpenMuscle-Hub
- **Project Site:** https://openmuscle.org
- **Discord:** https://discord.gg/WstCaqUG63

---

## License

Hardware released under **CERN Open Hardware License v2.0**
