# OM-FlexGrid Revision History

Quick cross-version comparison for anyone walking up to the repo cold. For per-revision detail, follow the link in each row to that revision's README.

| Revision | Status | Year | Headline change | Detail |
|---|---|---|---|---|
| **V4** | Current, validated (fabbed 2026-06, in starter kits since 2026-10; design files at V4-2) | 2026 | microSD + RGB status LED + slimmer reorientation; V4-2 adds USB presence sensing | [`OM-FlexGrid V4/README.md`](OM-FlexGrid%20V4/README.md) |
| **V3** | Previous, validated | 2026 | Wurth FFC interconnect; matrix usable as ML training source | [`OM-FlexGrid V3/README.md`](OM-FlexGrid%20V3/README.md) |
| **V2** | Deprecated | 2025 | Pre-FFC, used hand-soldered pin headers between flex and rigid | [`OM-FlexGrid V2/README.md`](OM-FlexGrid%20V2/README.md) |
| **V1** | Archived | 2025 | Early prototype | [`OM-FlexGrid V1/`](OM-FlexGrid%20V1/) |
| **V0** | Archived | 2024 | Initial proof-of-concept | [`OM-FlexGrid V0/`](OM-FlexGrid%20V0/) |

---

## V4 (current, 2026)

**Headline:** Wearable-ready upgrade. On-device data logging via microSD, glance-tells via RGB status LED, slimmer board geometry for a bracelet fit. Builds on the V3 production baseline. Fabricated June 2026 (10 units, JLCPCB single-side SMT), brought up 2026-06-23, validated in use; two bands shipped as the first OpenMuscle starter kit in October 2026 running FlexGridV4-Firmware v4.0.1. Design files are at revision V4-2 (2026-11-03), not yet fabricated.

**Key adds vs V3:**
- microSD card socket (Molex 5033981892, LCSC C428492) wired in SPI mode
- Discrete common-cathode 0603 RGB LED on GPIO 40/41/42 (zero quiescent, no setup fee)
- Board re-rotated so the long axis runs along the forearm, lower-profile against the skin
- Footprint cleanup: 1N5819 and 1N4007 standardized on SOD-123 (was SOD-123F), resistors forced to 0603
- V4-2 (design files only): VBUS sense divider on IO39 so firmware can detect USB, vias moved out of SMD pads, USB D+/D- routed as a pair

**Found in bring-up:** USBLC6 pinout reversed in the schematic (fixed; June boards need the chip rotated 180 degrees), IMU shipped as the TOKMAS rebrand (firmware auto-probes both). **Open before the next fab:** final VBUS-STAT divider values, regenerate BOM/CPL/Gerbers for V4-2, swap the IMU back to genuine InvenSense.

**Hand-soldered after JLC assembly:** all bottom-side SMT (ESP32-S3 module, CD74HC4067 mux, a few passives), microSD socket, Wurth FFC connector, USB-C, battery JST, pin headers.

**Firmware:** [Open-Muscle/FlexGridV4-Firmware](https://github.com/Open-Muscle/FlexGridV4-Firmware) v4.0.1.

[Full V4 README](OM-FlexGrid%20V4/README.md)

---

## V3 (production-quality matrix, May 2026)

**Headline:** First revision with a usable sensor matrix. Validated end-to-end on two physical boards. UDP telemetry over Wi-Fi confirmed reaching the desktop visualizer; matrix declared **usable as a real ML training data source** for the first time in the project's history.

**Key wins:**
- 60-cell matrix delivers clean single-cell press detection across all 60 sensors
- Peak ~1100 ADC counts on direct press, 22% carryover to next column, decays to noise floor within 3 columns, idle baseline exactly 0
- 59 Hz scan rate
- Wurth 687120183722 FFC interconnect mates cleanly with the integrated stiffened flex tail

**Known issues that V4 addresses:**
- Mixed diode footprints (SOD-123F vs SOD-123) caused LCSC mismatch pain during ordering
- Some resistors mid-design ended up on 0402 from the JLCPCB plugin's "auto-select alike"; cleaner to standardize on 0603
- No on-device storage or status indicator
- Original layout not optimized for bracelet form factor

**Firmware that makes V3 work:** [Open-Muscle/FlexGridV3-Firmware](https://github.com/Open-Muscle/FlexGridV3-Firmware) v0.1.7.

[Full V3 README](OM-FlexGrid%20V3/README.md)

---

## Pattern across revisions

The repo treats each revision as a frozen sibling directory under `KiCad/`. New revisions:

1. Start as a clean copy of the previous one (fab outputs and backups stripped)
2. Get committed as a baseline before any V(N) work begins, so subsequent commits show up as clean diffs
3. Are documented per-revision in their own README, with the status line at the top
4. Land into this cross-revision table once committed

Older revisions stay accessible in their original form; we never rewrite their history. Field-deployed V3 boards continue to function and continue to be supported by their firmware.

For the operating workflow that turns a routed KiCad project into a JLCPCB order, see [`../docs/JLCPCB_WORKFLOW.md`](../docs/JLCPCB_WORKFLOW.md).
