# OM-FlexGrid V1 - Rigid PCB

Welcome to the repository for **OM-FlexGrid V1**, the first revision of the rigid portion of Open Muscle's flexible sensor interface. This KiCad project represents a crucial part of Open Muscle's modular architecture for wearable, open-source prosthetic sensor systems.

---

## 🔧 Overview
This board is a rigid PCB designed to interface with a flexible sensor grid. It includes:

- An **ESP32-S3-WROOM-1-N16R8** module with Wi-Fi/BLE support
- Support for **I2C devices**: SSD1306 OLED and ICM-42688-P IMU
- **Multiplexer (MUX)** interface for up to 60 sensor lines
- **Battery charging and power management** circuits
- **Pushbutton-based low-power on/off** control
- **USB-C interface** for charging, programming, and serial communication
- **User interface buttons** and **haptic feedback motor**

---

## 📦 Hardware Block Summary

### 🧠 MCU
- **ESP32-S3-WROOM-1-N16R8**
  - 16MB Flash / 8MB PSRAM
  - Native USB, Wi-Fi, BLE
  - ADC-connected to 4 ROW lines
  - Boot/Reset accessible via tactile switches

### 🖥️ Display
- **SSD1306 OLED (I2C)**
  - Connected to `SCL` / `SDA`
  - Provides user interface feedback

### 📐 IMU
- **ICM-42688-P** (I2C)
  - 6-DOF (gyro + accel)
  - For orientation and gesture sensing

### 🔢 Flex Sensor Array
- **CD74HC4067 16-channel Multiplexer**
  - Connected to 15 COL lines
  - SIG line connected to 4 ADC-row lines
  - Enables scanning a 15x4 grid of passive sensors (typically in the flex PCB)

### ⚡ Power Management
- **TPS7A0333 LDO** (3.3V output)
  - Powered by either USB or battery
  - Controlled via EN pin from the smart pushbutton
- **LTC4054ES5**
  - Single-cell LiPo charging from USB
  - Status LED pin for visual charge indicator
- **MAX16054**
  - Smart pushbutton controller with power latch circuit

### 🔘 Buttons
- `MENU`, `SELECT`, `BOOT`, `RESET`
- `BOOT` and `RESET` used for flashing and recovery

### 📳 Haptic Feedback
- MOSFET-driven vibration motor
- GPIO-controlled with flyback diode for safety

### 🔌 USB-C Interface
- Provides:
  - Power (VBUS)
  - USB Data
  - LiPo charging input
  - Debugging and firmware flashing

---

## 📁 File Structure
```
/KiCad/OM-FlexGrid V1/
├── OM-FlexGrid-Rigid-PCB.kicad_sch     # KiCad Schematic
├── OM-FlexGrid-Rigid-PCB.kicad_pcb     # PCB Layout
├── symbols/                            # Custom symbols (if any)
├── footprints/                         # Custom footprints (if any)
└── exports/                            # Exported fabrication files (optional)
```

---

## 💡 Usage Notes
- The rigid PCB is designed to pair with a **flexible sensor grid**.
- The MUX enables **high-density analog signal acquisition** using only 4 ADCs.
- Power control via MAX16054 allows **ultra-low-power standby**.
- OLED and IMU allow for rich feedback and motion awareness in prosthetic or wearable contexts.

---

## 📜 License
This hardware is released under the **CERN Open Hardware License v2.0**.

> Open Muscle is committed to making prosthetic technologies accessible to all. You are encouraged to fork, remix, and contribute to this project.

---

## 🧠 Learn More
- 🌐 https://openmuscle.org
- 🤝 Community: [Discord Invite Link](https://discord.gg/WstCaqUG63))
- 🛠️ Firmware Repo: https://github.com/Open-Muscle/OpenMuscle-Firmware

---

Let us know if you use this board or build on it—we'd love to feature your work!
