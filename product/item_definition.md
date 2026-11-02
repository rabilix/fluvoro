# Fluvoro — item definition (ISO 26262-3, clause 5)

- Status: DRAFT 0.1 (2026-11-02), for maintainer review
- Inputs: `docs/product_brief.md`, `product/stakeholder_requirements.yaml`
- Next work product: `product/hara.yaml`

## 1. Item

**Fluvoro**: a battery-powered, solar-charged leaf shredder installed in the gutter
outlet (EN 612, NW 333, DN 87–100). It has two variants, V1 insert and V2
replacement outlet, and an optional BLE connectivity module. The HARA covers both
variants and the option; differences are named where they matter.

## 2. Functions of the item

| ID | Function | Description |
|---|---|---|
| F1 | Clog detection | Measure the water level in the outlet neck; decide whether a clog condition exists (FLV-STK-006/007), including quiet hours (FLV-STK-017). |
| F2 | Shred cycle | Drive the rotor through PWM with controlled speed and torque: soft start, run, current limit, jam detection, reverse, stop (FLV-STK-015). Verify the result (FLV-STK-010). |
| F3 | Energy management | Charge the battery from the PV cells (MPPT); protect the battery (over-voltage, under-voltage, over-current, short circuit, temperature, no charging below 0 °C); estimate the state of charge; keep a reserve (FLV-STK-033…043). |
| F4 | Access protection | Detect the cap being removed and the maintenance mode; inhibit the rotor in both cases (FLV-STK-071, -073). |
| F5 | Fault handling | Self-test, fault detection, safe state, latched faults, no restart without self-test (FLV-STK-016, -074, -080). |
| F6 | Signalling and logging | Status light, event log, service interface (FLV-STK-060…066). |
| F7 | Connectivity (option) | BLE status and notifications, signed firmware update; no actuation (FLV-STK-067, -101…103). |
| P1 | Passive drainage | Non-E/E: grate, liner and overflow bypass (FLV-STK-020/021). Inside the item boundary because its performance depends on what F2 and F5 do. |

## 3. Boundary and interfaces

```
            sunlight                      person (homeowner, roofer, passer-by)
               |                               |  removes cap, maintenance mode,
               v                               v  looks at status light, phone app
   +--------------------------- ITEM: Fluvoro -------------------------------+
   |  PV cells -> MPPT -> BMS <-> LiFePO4 pack (NTC)                          |
   |                       |                                                 |
   |  level sensor -> MCU (F1,F2,F4,F5,F6) -> gate driver -> BLDC -> rotor   |
   |  cap switch  ->   |        ^ current, speed feedback                     |
   |                   +-> status light, service port, [BLE option]          |
   |  grate / liner / overflow bypass (P1, passive)                           |
   +-------------------------------------------------------------------------+
        ^ water + debris in                    v water + mulch out
     gutter (EN 612, metal)                 downpipe (DN 87 / DN 100)
```

**Outside the item:** the gutter, the outlet (V1), the downpipe, the building, the
smartphone and its app, and the manufacturer's firmware signing infrastructure.

**Interfaces:** mechanical (outlet geometry, clips, bead), hydraulic (inflow,
discharge), energy (sunlight), human (cap, maintenance control, status light,
service port), radio (BLE option).

## 4. Operating modes

| Mode | Rotor | Charging | Entered by |
|---|---|---|---|
| Monitoring | off | allowed (temperature permitting) | default |
| Shredding | on, controlled | allowed | clog condition (F1) |
| Maintenance | inhibited | allowed | person, at the device |
| Cap removed | inhibited, drive de-energised | n/a | cap switch |
| Fault (latched) | inhibited | depends on the fault | F5 |
| Low energy | allowed for clearing only | allowed | state of charge ≤ reserve |
| Deep sleep / recovery | off | allowed | battery exhausted; leaves automatically (FLV-STK-035) |

## 5. Tailoring of ISO 26262 to a non-vehicle item

ISO 26262 is written for road vehicles. The customer requires it as the
development frame (FLV-STK-070), so its rating parameters are adapted here. The
**method** is unchanged: hazards are rated without considering the item's own
safety mechanisms, and the ASIL comes from Table 4 of ISO 26262-3.

**Severity (S).** As in ISO 26262-3 Annex B, by injury to persons (AIS):

| Class | Meaning |
|---|---|
| S0 | No injuries. |
| S1 | Light and moderate injuries. |
| S2 | Severe and life-threatening injuries, survival probable. |
| S3 | Life-threatening injuries, survival uncertain, or fatal injuries. |

Damage to property alone is **not** rated. It is handled by quality management
and the EN ISO 12100 risk assessment (FLV-STK-091).

**Exposure (E).** Rated by how often the operational situation occurs for **one
installed device**, because a household device has no "driving cycle":

| Class | Frequency |
|---|---|
| E1 | Less than once per year, or only under unusual conditions. |
| E2 | A few times per year. |
| E3 | About once a month or more often. |
| E4 | Daily, or permanently present. |

**Controllability (C).** Rated by the **person at risk**: a homeowner or roofer at
the device, or a passer-by below it. The question is whether that person can avoid
the harm once the malfunction occurs:

| Class | Meaning |
|---|---|
| C0 | Controllable in general. |
| C1 | Simply controllable: 99 % or more of persons avoid the harm. |
| C2 | Normally controllable: 90 % or more. |
| C3 | Difficult to control or uncontrollable. |

**Out of scope of the HARA** (but in the EN ISO 12100 risk assessment):

- Hazards with no E/E malfunction in their cause chain, for example a sharp edge or
  the device falling because of a broken clip.
- Cybersecurity causes of hazardous events, such as a malicious BLE command. These
  go to the ISO/SAE 21434 TARA (FLV-STK-100). The HARA rates the hazardous event
  once, whatever the cause.

## 6. Assumptions (to be confirmed)

| ID | Assumption |
|---|---|
| A1 | Nominal pack: 4 LiFePO4 cells in series, 12.8 V, ≤ 50 Wh. |
| A2 | Motor: BLDC, ≤ 60 W electrical, rotor ≤ 3 000 rpm, stall torque limited by the drive's current limit. |
| A3 | Installation height of the gutter: 2.5 m (garage, bungalow) to 10 m. |
| A4 | People walk below eaves near outlets (entrances, terraces). |
| A5 | The homeowner cleans the grate or removes objects a few times per season; a roofer opens the device about once a year. |
| A6 | Children can reach outlets on low buildings (garden sheds, carports); this is foreseeable misuse. |
