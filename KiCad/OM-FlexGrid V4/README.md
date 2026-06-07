# OM-FlexGrid V4

> **Status: READY FOR FAB (as of 2026-06-07).** Schematic and PCB are routed. DRC passes with zero unconnected nets. Production files generated via the `kicad-jlcpcb-tools` plugin. Manufacturing strategy decided (see [Manufacturing](#manufacturing-jlcpcb) below): **single-side SMT assembly at JLCPCB for 10 units, plus hand-soldering of all bottom-side parts and through-hole connectors at home.** Not yet ordered. Not yet brought up.

Fourth major revision of the Open Muscle FlexGrid wearable sensor platform. V4 builds on the V3 production baseline (which validated the FFC interconnect and proved the 60-cell matrix as a usable ML training data source) and adds on-device storage, a status indicator, and a slimmer board profile.

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

### Still open

- [ ] **Mechanical / 3D fit check** against the bracelet enclosure (3D STEP at `OM-FlexGrid-Rigid-PCB.step`)
- [ ] **V4 Flex PCB**: bump the FFC tail width from 11.1 mm to **10.5 mm** per the Wurth 687120183722 datasheet. This fix has not yet landed in the V4 Flex folder; do it before ordering the matching flex.
- [ ] **Flag haptic as experimental in firmware.** The haptic driver hardware (IRLML2060 on the haptic GPIO) ships unvalidated. Firmware should default the haptic GPIO low and only drive it behind an explicit opt-in.
- [ ] **Final BOM scan**: open `jlcpcb/production_files/BOM-OM-FlexGrid-Rigid-PCB.csv` and confirm no surprise Extended-tier parts with thin stock slipped in. The plugin's auto-suggestions occasionally rotate inventory between sessions.
- [ ] **Order parts for hand assembly** (need physical inventory before boards arrive):
    - microSD socket: LCSC C428492 or Mouser equivalent (10 + spares)
    - Wurth 687120183722 FFC connector: Mouser 710-687120183722 (10 + spares)
    - All through-hole pin headers, JSTs, OLED interface as in the hand-solder list
    - The full BOT-side SMT list (ESP32 module, mux, passives) ordered loose from LCSC
- [ ] **Submit the JLCPCB order** with **"Confirm parts placement"** toggled ON so the assembly preview email catches any rotation surprises before they cut metal.

---

## File layout

```
OM-FlexGrid V4/
|-- OM-FlexGrid-Flex/                        Flex PCB (15x4 sensor matrix + FFC tail)
`-- OM-FlexGrid-Rigid-PCB/                   Rigid controller board
    |-- OM-FlexGrid-Rigid-PCB.kicad_pro      KiCad project
    |-- OM-FlexGrid-Rigid-PCB.kicad_sch      Schematic (24K lines)
    |-- OM-FlexGrid-Rigid-PCB.kicad_pcb      PCB layout
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
- **Firmware:** [Open-Muscle/FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware) (V4 will likely fork this when fabbed)
