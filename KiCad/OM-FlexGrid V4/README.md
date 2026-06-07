# OM-FlexGrid V4

> **Status: IN DESIGN (as of 2026-06-07).** Schematic and PCB are routed. DRC passes with zero unconnected nets. Production files generated via the `kicad-jlcpcb-tools` plugin and ready for upload to JLCPCB. Not yet fabricated, not yet brought up. Treat this revision as a paper design pending a fab cycle.
>
> Open items before pulling the trigger: final LDO part selection, double-check bottom-side / DNP exclusions in the generated BOM, final 3D / mechanical fit review against the bracelet form.

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

---

## Manufacturing (JLCPCB)

V4 was prepared for JLCPCB SMT assembly using the [`Bouni/kicad-jlcpcb-tools`](https://github.com/Bouni/kicad-jlcpcb-tools) KiCad plugin. The full workflow we use across revisions is captured at `docs/JLCPCB_WORKFLOW.md` in this repository.

### Generated output files (in `OM-FlexGrid-Rigid-PCB/jlcpcb/`)

```
jlcpcb/
|-- gerber/                                       individual Gerber + drill files
`-- production_files/
    |-- GERBER-OM-FlexGrid-Rigid-PCB.zip          upload this zip directly to JLCPCB
    |-- BOM-OM-FlexGrid-Rigid-PCB.csv             BOM with LCSC part numbers
    `-- CPL-OM-FlexGrid-Rigid-PCB.csv             component placement / pick-and-place
```

The BOM and CPL **only contain parts JLC will assemble**. Hand-soldered parts are excluded at the plugin level (BOM-OFF and POS-OFF), which keeps the manufacturer's view of the BOM clean and matches the physical reality of the assembled board they ship.

### Hand-soldered parts

These parts are physically present on the V4 board (footprints exist) but are intentionally excluded from the JLC assembly order. The user populates them after the assembled board arrives.

| Designator | Part | Why hand-soldered |
|---|---|---|
| microSD socket | Molex 5033981892 (LCSC C428492) | Single part, easy reflow, no setup fee, removes a stock-availability risk |
| Battery JST terminal | Through-hole | JLC standard SMT assembly does not include through-hole |
| Pin headers (programming, debug, OLED) | Through-hole | Same reason |
| Wurth FFC connector (rigid side) | Wurth 687120183722 from Mouser direct | Specific part not consistently at LCSC; user wants the genuine part |

The authoritative per-designator list lives in the schematic and the JLCPCB plugin's UI (any designator with BOM-toggle and POS-toggle OFF). The generated BOM and CPL CSVs reflect those exclusions.

---

## Open items before fab

- [ ] Final LDO part selection (TPS7A03 family; pick the LCSC variant with deepest stock at fab time)
- [ ] Review the generated `BOM-OM-FlexGrid-Rigid-PCB.csv` end to end for any "Type = Extended" rows with thin stock; substitute equivalent parts where possible
- [ ] Mechanical / 3D fit check against the bracelet enclosure (3D STEP at `OM-FlexGrid-Rigid-PCB.step`)
- [ ] Confirm IMU LCSC choice (ICM-42688-P or LSM6DSOX) shows **POP = green check** in the plugin (the V3 baseline hit a POP failure on Tokmas C54308212; pick a part JLC can actually place)
- [ ] V4 Flex PCB: bump the FFC tail width from 11.1 mm to **10.5 mm** per the Wurth 687120183722 datasheet; this fix has not yet landed in the V4 Flex folder

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
