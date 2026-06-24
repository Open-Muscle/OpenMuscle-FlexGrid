# OM-FlexGrid V4

> **Status: BROUGHT UP 2026-06-23.** Boards arrived from JLCPCB; two units flashed with V4 MicroPython firmware and running end-to-end on the OpenMuscle discovery + subscribe protocol. Two hardware bugs surfaced during bring-up: USBLC6 ESD chip pinout reversed in the schematic (schematic fix landed; existing boards work with a 180-degree chip rotation), and the as-ordered IMU is a TOKMAS rebrand rather than genuine InvenSense as planned (driver auto-probes both variants; see [Bring-up findings](#bring-up-findings-2026-06-23) below). Total landed cost $341.84 for 10 units (~$35 per board for the JLC half; see [Cost breakdown](#cost-breakdown-10-unit-batch-june-2026) for per-unit details).

## 📄 Design documents (PDFs)

For people who want to review the design without opening KiCad:

### Rigid PCB

- 📐 [`FlexGridV4-Rigid-Schematic.pdf`](OM-FlexGrid-Rigid-PCB/FlexGridV4-Rigid-Schematic.pdf): full schematic, all sheets, all nets named
- 🟦 [`FlexGridV4-Rigid-PCB.pdf`](OM-FlexGrid-Rigid-PCB/FlexGridV4-Rigid-PCB.pdf): board layout

### Flex PCB

- 📐 [`FlexGridV4-Flex-Schematic.pdf`](OM-FlexGrid-Flex/FlexGridV4-Flex-Schematic.pdf): sensor matrix schematic
- 🟦 [`FlexGridV4-Flex-PCB.pdf`](OM-FlexGrid-Flex/FlexGridV4-Flex-PCB.pdf): flex layout including the stiffened FFC tail
- 🟧 [`FrontCopper_SolderMask.pdf`](OM-FlexGrid-Flex/FrontCopper_SolderMask.pdf): front-side copper + soldermask overlay (useful for sanity-checking the Velostat sensor cell exposures)

### What gets populated and what doesn't

The split between "JLCPCB assembles this" and "I hand-solder this after the boards arrive" is documented in [Hand-soldered parts (full list)](#hand-soldered-parts-full-list) below. tl;dr:

- **JLCPCB assembles all TOP-side SMT parts** (passives, regulators, charger, MUX-driver MOSFETs, MAX16054, USBLC6, IMU, CHRG LED, RGB LED, etc.)
- **You hand-solder everything else**: all BOT-side SMT (including U1 CD74HC4067 mux and U2 ESP32-S3 module), the microSD socket, the Wurth FFC connector, USB-C, and every through-hole pin header / JST. The per-designator table further down has each part listed by reference designator with solder-difficulty notes.

Fourth major revision of the Open Muscle FlexGrid wearable sensor platform. V4 builds on the V3 production baseline (which validated the FFC interconnect and proved the 60-cell matrix as a usable ML training data source) and adds on-device storage, a status indicator, and a slimmer board profile.

---

## Bring-up findings (2026-06-23)

Two boards from the 10-unit fab batch were flashed with V4 MicroPython firmware ([Open-Muscle/FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware), see its `BRINGUP.md` for step-by-step flashing instructions). Both ran the OpenMuscle discovery + subscribe protocol end-to-end against the PC `openmuscle web` app and the Android Connect client. Two hardware bugs surfaced during bring-up; both are documented here so future builders do not re-discover them.

### 1. USBLC6-2SC6 pinout reversed in schematic (FIXED)

The V4 KiCad schematic wired the USBLC6 with pin 2 on VBUS and pin 5 on GND. The actual chip pinout is the other way around (pin 2 = GND, pin 5 = VCC). With the silkscreen-correct placement, USB enumerates VBUS only (Windows reports "Device Descriptor Request Failed"), no COM port appears.

- **Workaround for the existing 10-unit batch:** rotate the USBLC6 chip 180 degrees from the silkscreen orientation during placement. The SOT-23-6 footprint is symmetric so the I/O pin pairs still route correctly, and VCC and GND land where they belong.
- **Schematic fix landed** in this repo. The next fab order will be correct without rotation.

### 2. IMU is a TOKMAS rebrand, not genuine InvenSense (DRIVER WORKAROUND)

The pre-fab checklist documented the IMU choice as genuine InvenSense ICM-42688-P (LCSC C1850418). The as-ordered BOM ended up with the cheaper TOKMAS rebrand (LCSC C54308212) instead. TOKMAS has the same general silicon spec but a different I2C address (0x36 / 0x37 instead of 0x68 / 0x69) and a different register map (data at 0x00-0x0D instead of 0x1F-0x2A).

- **Workaround:** [`lib/imu.py`](https://github.com/Open-Muscle/FlexGridV4-Firmware/blob/main/lib/imu.py) in the V4 firmware auto-probes both variants. Verified working on board #1: live accel + gyro at the expected rates.
- **Recommendation for the next fab order:** switch back to genuine InvenSense (C1850418) and retire the TOKMAS code path. The ~$11 per-chip savings cost a custom driver branch and ongoing maintenance.

### Firmware repo and bring-up guide

- Firmware: [Open-Muscle/FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware)
- Step-by-step flashing instructions: [`BRINGUP.md`](https://github.com/Open-Muscle/FlexGridV4-Firmware/blob/main/BRINGUP.md)
- One-shot flash script: `flash.py COM<port>` after pip-installing esptool 5.x + mpremote and downloading the MicroPython binary

---

## What is new in V4 vs V3

| Area | V3 | V4 | Why |
|---|---|---|---|
| **On-device storage** | None | **microSD socket** (SPI mode) | Local data logging and on-device model storage; lets the band run untethered for a session and offload later |
| **Status indication** | OLED only | **RGB status LED** (3-channel PWM) | Glance-tells "what is the band doing" without looking at the OLED; survives an OLED-off power state |
| **Power-on indicator** | None | Provided by the RGB LED's idle color | One fewer LED in the BOM; cleaner board |
| **Board orientation** | Original V3 layout | **Reoriented for slimmer bracelet fit** | Long axis aligned with the forearm; lower profile against the skin |
| **Diode footprints** | Mixed (D-SOD-123F seen on 1N5819 and 1N4007) | **Standardized on SOD-123** (1N4007W style) | Matches what LCSC actually stocks; avoids the V3 mid-design footprint mismatch we hit |
| **Resistor packages** | Mixed 0402 / 0603 | **All 0603** | Easier hand rework, broader LCSC stock, more forgiving for the prototype-quantity user |

What stays the same as V3: 60-sensor 15x4 Velostat matrix on the flex PCB, ESP32-S3-WROOM-1-N16R8 controller, CD74HC4067 mux, Wurth 687120183722 FFC interconnect, MAX16054 soft power, LTC4054-class charger, TPS7A03 LDO family (specific part TBD this revision), USB-C power and data, BAT54C diode-OR for VBUS-or-VBAT, ICM-42688-P IMU (genuine TDK or pin-compatible part, awaiting final LCSC stock decision).

---

## microSD card socket (NEW IN V4)

Wired in 1-bit SPI mode for simplicity and ESP32-S3 compatibility. SDIO 4-bit mode is not used; SPI is sufficient for logging sensor frames at the band's scan rates with margin.

| Pin name on socket | Wired to | Role in SPI mode |
|---|---|---|
| DATA0 (DAT0) | ESP32-S3 SPI MISO | data out of card |
| CMD | ESP32-S3 SPI MOSI | data in to card |
| CLK | ESP32-S3 SPI SCK | clock |
| DATA3 / CD | ESP32-S3 GPIO (CS) | chip select |
| VCC | 3V3 | power |
| GND, shield, mounting tabs | GND | return + mechanical |

### Connector

| Field | Value |
|---|---|
| Manufacturer P/N | Molex 5033981892 |
| LCSC P/N | **C428492** |
| Mount | Surface-mount, push-push, top side of rigid board |
| Hand-solder | **Yes, explicitly excluded from JLCPCB assembly** (see [Hand-soldered parts](#hand-soldered-parts) below) |

The microSD socket is intentionally hand-soldered after JLC assembly rather than included in the SMT run. Rationale: only one part, easy to solder, avoids a setup fee, and removes a parts-availability risk from the assembly order.

---

## RGB status LED (NEW IN V4)

Discrete common-cathode RGB LED in a 1.6 x 1.6 mm (0603-style) package, driven by three PWM-capable GPIOs through current-limiting resistors. Chosen over an addressable smart LED (WS2812 family) specifically for **zero quiescent current** when the LED is dark, which protects the 500 mAh battery's standby time.

### Wiring

| Channel | GPIO | Series resistor | Notes |
|---|---|---|---|
| Red | GPIO 40 | 330 ohm | adjust if too bright |
| Green | GPIO 41 | 330 ohm | |
| Blue | GPIO 42 | 330 ohm | |
| Common cathode | GND | n/a | shared return |

LCSC examples: C2827305-class 0603 common-cathode RGB. Final LCSC part number is recorded in the generated BOM at `jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv`.

### Status palette (firmware target)

The exact palette is firmware-defined; the V4 hardware just provides the channels. Suggested defaults:

| State | Color | Pattern |
|---|---|---|
| Booting / Wi-Fi connecting | blue | slow breathe (1 Hz) |
| Idle, no peer | white | dim solid |
| Streaming sensor data | green | solid |
| Recording (paired with PC) | yellow | slow breathe |
| Sending predictions to hand | purple | solid |
| Sleeping / deep idle | off | n/a |
| Wi-Fi disconnected | orange | fast blink (3 Hz) |
| Error / sensor fault | red | fast blink |

---

## Layout reorientation

V4 rotates the long axis of the rigid board so it hugs the forearm rather than crossing it. The component placement was reworked around the new aspect ratio: power management clustered at one end, ESP32 and OLED at the other, microSD socket on the side that faces away from the skin so the user can pop a card in or out without removing the band.

---

## Footprint cleanup applied

Issues we hit during V3 design / V4 LCSC selection that are now fixed in V4:

- **1N5819 and 1N4007** previously used the `D_SOD-123F` footprint. LCSC primarily stocks the `1N5819W` and `1N4007W` variants in **SOD-123** (no `F` suffix). V4 swaps both diode footprints to plain SOD-123 to match what is actually available at the manufacturer.
- **Resistors** that the JLCPCB plugin's "auto-select alike" feature had silently downgraded to 0402 are all forced back to **0603**. This matches the LCSC Basic-tier inventory the design draws from and keeps hand rework feasible.
- **C9 (100 uF)** previously sat on an 0603 footprint that cannot physically host a 100 uF cap. Footprint upsized to match the chosen part.
- **MAX1 (MAX16054 soft-power controller)** footprint changed from SOT-23-6 to **TSOT-23-6** to match the LCSC part C79401 (MAX16054AZT+T ships in TSOT-23-6). The two packages share the same pad pitch and outline (the TSOT variant is just thinner), so a SOT-23-6 footprint would have accepted the part, but matching the footprint to the actual package is cleaner for downstream KiCad consumers. The schematic value also got cleaned up from `~` to `MAX16054` so the BOM and silkscreen identify it correctly.

---

## Known carry-forward concerns from V3

These items are present on the V4 board, were either copied from V3 unchanged or built in speculatively, and have **NOT been validated in the V4 configuration**. Documented here so future bring-up does not get blindsided.

### Haptic feedback circuit (built but untested)

V4 carries forward the haptic motor driver from V3 (IRLML2060 N-channel MOSFET on a haptic GPIO line, driving a small DC vibration motor through a header). The driver was placed on V3 and has been retained in V4 as a "just in case" feature for future user-feedback work, **but it has not been bench-tested in this configuration on any V3 board, and will arrive on V4 unvalidated**.

Treat haptic as an **optional / experimental feature** for now. If V4 bring-up needs haptic for a demo, expect a debug pass: gate-level on the MOSFET, motor selection, current draw at startup, and any required flyback protection.

The firmware should default the haptic GPIO to "off" and only enable it behind an explicit opt-in setting, so users running a standard recording or inference session do not get unexpected vibration.

### ADC matrix-row capacitors (C12, C13, C14, C15): RESOLVED

**Final decision: 100 pF (LCSC C14858, 0603, Basic tier).** Option 3 from the original analysis below.

The 100 pF value drops the RC time constant with each row's 10 kΩ pulldown from ~22 ms (V3 with 2.2 uF) to ~1 microsecond, well below the per-column ADC dwell time. Resolves the column-to-column bleed that V3 had to fix by removing the caps entirely, while preserving the high-frequency noise filtering at the ADC input. **No mid-bring-up rework needed on V4 if the math holds.**

For posterity, the original options considered were:

1. Leave the 2.2 uF parts in the JLC BOM, then physically remove them during V4 bring-up the same way V3 did. Wastes the per-board part cost; lowest cognitive risk.
2. Toggle C12 through C15 to BOM-OFF and POS-OFF in the JLCPCB plugin so JLC does not populate them. Hand-solder only if matrix bench-testing on a bare board shows they are needed for noise filtering. Matches V3 empirical outcome.
3. **Change the V4 value to 100 pF** (same 0603 footprint, new LCSC). Most engineering-correct; adds a small amount of rework. **Selected.**

V3's bring-up README documents the original symptom (22 ms RC bleed at 2.2 uF, ~9x signal improvement after physical removal).

---

## Manufacturing (JLCPCB)

V4 was prepared for JLCPCB SMT assembly using the [`Bouni/kicad-jlcpcb-tools`](https://github.com/Bouni/kicad-jlcpcb-tools) KiCad plugin. The full workflow we use across revisions is captured at `docs/JLCPCB_WORKFLOW.md` in this repository.

### Strategy: single-side SMT + hand assembly

The first V4 batch is 10 units. We chose **single-side SMT assembly** at JLCPCB (top side only) over double-side assembly. Tradeoff:

- **Saves money** on JLC's double-side setup fee, roughly $25 to $50 per order at this quantity
- **Costs time** at the hand-solder bench: every bottom-side SMT part has to be reflowed at home, including the ESP32-S3-WROOM-1 module
- Acceptable for a prototyping batch of 10 because the time investment is one-off; future production runs can revisit this when component placement is stable enough to justify the double-side setup

Required hand-assembly equipment for this strategy:
- Hot air rework station or solder paste + stencil + reflow plate, specifically for the ESP32-S3-WROOM-1 module's thermal pad
- Fine-tipped iron, liquid flux, solder wick, 10x or better magnification, for the TSSOP-24 mux and 0402 / 0603 BOT-side passives
- Standard through-hole iron technique for the pin headers, battery JST, OLED connector, USB-C, and Wurth FFC

### Generated output files (in `OM-FlexGrid-Rigid-PCB/jlcpcb/`)

```
jlcpcb/
|-- gerber/                                       individual Gerber + drill files
`-- production_files/
    |-- GERBER-OM-FlexGrid-Rigid-PCB.zip          upload this zip directly to JLCPCB
    |-- BOM-OM-FlexGrid-Rigid-PCB.csv             BOM with LCSC part numbers
    `-- CPL-OM-FlexGrid-Rigid-PCB.csv             component placement / pick-and-place
```

The BOM and CPL **only contain parts JLC will assemble**. Everything we hand-solder is excluded at the plugin level (BOM-OFF and POS-OFF), which keeps the manufacturer's view of the BOM clean and matches the physical reality of the assembled board they ship.

### Hand-soldered parts (full list)

All bottom-side SMT plus every through-hole part. Excluded from the JLC BOM and CPL by toggling BOM-OFF and POS-OFF in the plugin. Buy these separately and populate them after the JLC-assembled boards arrive.

**Bottom-side SMT (excluded for single-side cost saving):**

| Designator | Part | Footprint | Solder difficulty |
|---|---|---|---|
| **U2** | ESP32-S3-WROOM-1-N16R8 | Module, castellated edges + thermal pad | **Hard**: hot air rework or stencil reflow only |
| **U1** | CD74HC4067M | TSSOP-24, 0.65 mm pitch | Medium: fine iron + flux + wick |
| C9 | 100 uF cap | 0603 (or larger if footprint was upsized) | Easy |
| D4 | 1N4007W | SOD-123 | Easy |
| Q1 | IRLML2060 | SOT-23 | Easy |
| R10, R11 | 10 kΩ | 0603 | Easy |
| J9 | microSD socket (Molex 5033981892, LCSC C428492) | Push-push SMT | Easy with patience |

**Through-hole connectors (JLC standard SMT assembly does not cover these regardless of side):**

| Designator | Part | Notes |
|---|---|---|
| J1 | Programming / debug pin header | 6-pin 1x06 vertical |
| J2 | Battery JST terminal | 2-pin through-hole |
| J3 | Wurth 687120183722 FFC connector (rigid side) | Sourced direct from Mouser (P/N 710-687120183722). Würth not consistently available at LCSC |
| J4 | USB-C receptacle (HRO PE-C-31-M-12 or equivalent) | SMT but explicitly hand-soldered for this batch |
| J5, J6, J7 | Pin headers / sockets | Various, all through-hole |
| SCRN1 | OLED interface (4-pin pin header) | Through-hole |

**Mounting holes (H1 through H4) are virtual** in the BOM sense; they have BOM-OFF and POS-OFF set because there is no component to source or place. They exist on the PCB as physical M2 mounting positions only.

The authoritative per-designator list lives in the schematic and the JLCPCB plugin's UI (any designator with BOM-toggle and POS-toggle OFF). The generated BOM and CPL CSVs reflect those exclusions.

### Cost breakdown (10-unit batch, June 2026)

Real numbers from the V4 fab order placed on 2026-06-12. Use these as a starting estimate for budgeting your own build; LCSC prices and JLC fees move month to month.

**JLCPCB landed cost (rigid + flex, both boards together):**

| Line item | Total | Per board (10 units) |
|---|---|---|
| Merchandise (4-layer rigid PCB + flex PCB + single-side SMT assembly) | $204.72 | $20.47 |
| Shipping (DHL to Texas) | $47.20 | $4.72 |
| Customs duties + taxes | $71.66 | $7.17 |
| Sales tax | $18.26 | $1.83 |
| **Grand total at checkout** | **$341.84** | **~$35** |

So the JLC half of the build lands at **~$35 per assembled board**: top-side SMT populated, ready for the hand-solder add-ons.

**Hand-solder add-on parts (rough qty-10 prices, source noted):**

| Part | Source | Per-unit (qty 10-20) |
|---|---|---|
| ESP32-S3-WROOM-1-N16R8 module (U2) | LCSC | ~$5.00 |
| Wurth 687120183722 FFC connector (J3, rigid side) | Mouser (P/N 710-687120183722) | ~$2.50 |
| microSD push-push socket (J9) | LCSC C428492 | ~$1.00 |
| USB-C receptacle (J4) | LCSC | ~$1.00 |
| CD74HC4067M 16-channel mux (U1) | LCSC | ~$0.70 |
| Pin headers, JST battery terminal, OLED interface (J1, J2, J5, J6, J7, SCRN1) | LCSC | ~$1.00 combined |
| BOT-side passives (C9, D4, Q1, R10, R11) | LCSC | ~$0.50 combined |
| **Hand-solder add-on subtotal** | | **~$12** |

**External parts not on either BOM (per band):**

| Part | Per-unit |
|---|---|
| SSD1306 128 x 32 OLED display module | ~$3 |
| 500 mAh LiPo battery | ~$6 |
| Cloth bracelet housing (Velcro, fabric, elastic, anti-slip tape) | varies, ~$2 to $5 |

**Estimated total per complete wearable: ~$55 to $60.** That's the JLC landed cost, plus the hand-solder add-ons, plus the display and battery. Cost drops meaningfully above ~50 units because JLC's setup fees amortize and LCSC reel pricing kicks in.

What this does NOT include: the build labor (~30 minutes per board of hand-soldering once the workflow is dialed in), the tooling cost (hot-air station, microscope, stencil), or the dev iterations that got us to a working V4.

---

## Pre-fab checklist

### Resolved this pass

- [x] **IMU footprint fixed.** IC1 (ICM-42688-P) was swapped from a custom `IIM42352` named footprint to KiCad's standard `Package_LGA:LGA-14_3x2.5mm_P0.5mm_LayoutBorder3x4y`. POP now shows green; JLC can place the part with the chosen LCSC.
- [x] **Manufacturing strategy locked.** Single-side SMT at JLCPCB for the first 10 units, plus hand assembly of every BOT-side part and every through-hole part. See [Manufacturing](#manufacturing-jlcpcb) above.
- [x] **TPS7A03 LDO chosen.** C2873330 (Texas Instruments TPS7A0333DBVR, 3.3 V output, SOT-23-5, ~3000 stock at LCSC).
- [x] **STC4054GR charger chosen.** C262930 (ST Microelectronics, pin-compatible with the original LTC4054).
- [x] **CHRG LED swap.** Replaced the original Extended-tier C72043 (stock = 1) with C2297 (Basic tier, > 3M stock).
- [x] **Footprint cleanup applied:** 1N5819 and 1N4007 standardized on SOD-123, all resistors forced to 0603, C9 footprint upsized to fit the chosen 100 uF cap, MAX1 (MAX16054) footprint moved to TSOT-23-6.
- [x] **ADC matrix-row caps C12-C15 changed to 100 pF.** Resolves the V3 column-bleed risk in silicon; no mid-bring-up rework needed. New LCSC: C14858 (Basic tier).

### Done before fab submission

- [x] **V4 Flex PCB FFC tail width fixed.** Bumped from 11.1 mm to 10.5 mm per the Wurth 687120183722 datasheet; the +67.6 deg horizontal-banana rotation was applied via `scripts/prep_flex_svgs.py` and re-imported into the V4 Flex Edge.Cuts layer.
- [x] **Final BOM scan completed.** RGB LED swapped to ASMB-UTF2-0E20B (C7077610, Avago PLCC-6 RGB, 100 in stock, $0.56) replacing the original 1615 part. IMU was specified as genuine InvenSense ICM-42688-P (C1850418, $14.19, 3358 in stock); however, **the as-ordered BOM ended up with the TOKMAS rebrand (C54308212)** rather than the genuine part. Documented in [Bring-up findings](#bring-up-findings-2026-06-23). Next fab should re-select C1850418.
- [x] **JLCPCB order submitted 2026-06-12.** $341.84 total landed cost. "Confirm Production file" toggled ON; PCB Remark field carries explicit stiffener-side instructions (FR-4 0.2 mm on B.Cu side, 10.5 x 8 mm under the FFC contact pads per User.1 layer).
- [x] **Responded to JLC's production-file confirmation email.** Order proceeded; boards arrived 2026-06-23.
- [x] **Parts for hand assembly ordered and received.** ESP32-S3-WROOM-1, CD74HC4067M, USB-C, Wurth FFC, microSD socket, headers all in inventory; two boards built end-to-end.
- [x] **Boards brought up.** See [Bring-up findings](#bring-up-findings-2026-06-23). Two HW bugs surfaced (USBLC6 schematic-fixed; TOKMAS IMU driver workaround).
- [x] **Flag haptic as experimental in firmware.** Firmware defaults `haptic_enabled` to false in `lib/settings_manager.py`; explicit opt-in only.

### Still open

- [ ] **Mechanical / 3D fit check** against the bracelet enclosure (3D STEP at `OM-FlexGrid-Rigid-PCB.step`). Two bring-up boards are loose; first complete wearable assembly still pending.
- [ ] **Next-fab BOM changes** to land before the second batch:
    - Swap TOKMAS IMU back to genuine InvenSense (C1850418).
    - Verify the USBLC6 schematic fix produces a correct CPL on the next fab.
    - Reconfirm RGB LED, LDO, charger LCSC parts are still in stock at the same tier.
- [ ] **Distribute remaining boards** to collaborators (8 boards spare; Christopher gets 2+ for prosthetics socket integration work).

---

## File layout

```
OM-FlexGrid V4/
|-- OM-FlexGrid-Flex/                        Flex PCB (15x4 sensor matrix + FFC tail)
|   |-- OM-FlexGrid-Flex.kicad_pro           KiCad project
|   |-- OM-FlexGrid-Flex.kicad_sch           Schematic
|   |-- OM-FlexGrid-Flex.kicad_pcb           PCB layout (flex + integrated FFC tail)
|   |-- FlexGridV4-Flex-Schematic.pdf        Reviewable schematic PDF
|   |-- FlexGridV4-Flex-PCB.pdf              Reviewable layout PDF
|   |-- FrontCopper_SolderMask.pdf           Sensor cell overlay PDF
|   |-- V4CurveCutout.svg                    Fusion 360 source: flex body outline
|   |-- FFC-Stiffener.svg                    Fusion 360 source: FFC tail stiffener
|   |-- V4-EdgeCuts-for-KiCad.svg            Processed: import to Edge.Cuts
|   `-- V4-Stiffener-for-KiCad.svg           Processed: import to Stiffener user layer
`-- OM-FlexGrid-Rigid-PCB/                   Rigid controller board
    |-- OM-FlexGrid-Rigid-PCB.kicad_pro      KiCad project
    |-- OM-FlexGrid-Rigid-PCB.kicad_sch      Schematic (24K lines)
    |-- OM-FlexGrid-Rigid-PCB.kicad_pcb      PCB layout
    |-- FlexGridV4-Rigid-Schematic.pdf       Reviewable schematic PDF
    |-- FlexGridV4-Rigid-PCB.pdf             Reviewable layout PDF
    |-- OM-FlexGrid-Rigid-PCB.csv            BOM (KiCad-exported)
    |-- OM-FlexGrid-Rigid-PCB.step           3D model
    |-- OM-FlexGrid-Rigid-V4-Gerber/         Standalone Gerber export
    |-- OM-FlexGrid-Rigid-V4-Gerber.zip      Standalone Gerber zip
    |-- OmFlexGridArtV4.svg                  Front silkscreen artwork
    |-- jlcpcb/                              JLCPCB plugin output (use these for ordering)
    |   |-- gerber/
    |   `-- production_files/
    |       |-- GERBER-OM-FlexGrid-Rigid-PCB.zip
    |       |-- BOM-OM-FlexGrid-Rigid-PCB.csv
    |       `-- CPL-OM-FlexGrid-Rigid-PCB.csv
    `-- OM-FlexGrid-Rigid-PCB-backups/       KiCad auto-rotated backups from this design session
```

---

## Related work

- **V3 status and bring-up findings:** `../OM-FlexGrid V3/README.md`
- **JLCPCB plugin workflow (generic, applies to all revisions):** `../../docs/JLCPCB_WORKFLOW.md`
- **Cross-revision comparison table:** `../REVISIONS.md`
- **V4 Firmware:** [Open-Muscle/FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware) (active; includes TOKMAS IMU support, ssd1306 driver vendored, `flash.py` one-shot bring-up, BRINGUP.md guide)
- **V3 Firmware:** [Open-Muscle/FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware) (shipping V3 reference; V4 firmware was forked from this)
- **Cross-device protocol spec:** [`PROTOCOL.md`](https://github.com/Open-Muscle/OpenMuscle-Hub/blob/main/PROTOCOL.md) in OpenMuscle-Hub (wire format, discovery, subscribe semantics, multi-device data model)
