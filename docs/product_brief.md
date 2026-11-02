# Fluvoro — product brief

- Status: DRAFT 0.1 (2026-11-02), for maintainer review
- Owner: product maintainer
- Companion: `product/stakeholder_requirements.yaml` (the clean reference specification)

## 1. The problem

Leaves, needles and small twigs collect at the gutter outlet, the conical sheet-metal
piece where the gutter drains into the downpipe. Once the outlet is blocked, water
overflows the gutter edge. It runs down the façade, soaks the base of the wall, and
in winter freezes into ice on paths. Today's remedies are passive: a leaf strainer
basket in the outlet, which itself clogs, or a leaf guard over the gutter. Both
still need someone on a ladder.

## 2. The product

Fluvoro is a self-powered shredder that sits in the gutter outlet. When water
starts to back up, it shreds the debris blocking the outlet into mulch small enough
to flow down the downpipe, then goes back to sleep.

```
        clip            ▒▒▒▒▒ SOLAR CAP (oval) ▒▒▒▒▒          clip
         _|_           /  [MCU][BMS][cells][motor] \           _|_
   _____|   |_________/____________||_______________\_________|   |_____
        \   ~~> water + leaves  slotted liner  <~~             /
         \                          ||   overflow bypass ->   /
          \                 [====( rotor )====]              /
           '.                 |<|> grind <|>|              .'
             |                |   [LEVEL]   |             |   neck -> downpipe
             |________________|______v______|_____________|
```

| Element | Function |
|---|---|
| Solar cap | PV cells on top; sealed compartment below holds the controller, battery management, battery and motor. Removing the cap disables the motor. |
| Slotted liner and grate | Follows the outlet funnel; lets water in, holds back large debris, and has an overflow bypass so water still drains when everything else is blocked. |
| Rotor and grind ring | Disposal principle: swivel impellers fling debris against a fixed serrated ring at the funnel-to-neck transition. |
| Level sensor | Detects water backing up in the neck: the clog signal. |
| PWM-driven BLDC motor | Speed and torque controlled by software: soft start, current limit, jam detection, reverse to clear. |
| LiFePO4 battery with BMS and MPPT | Stores solar energy; protected against over- and under-voltage, over-current and temperature; no charging below 0 °C. |
| Status LED | Visible from the ground: OK, low battery, service needed, fault. |

## 3. Variants

| | **V1 Insert** (primary) | **V2 Replacement outlet** |
|---|---|---|
| Buyer | Homeowner (DIY, hardware store) | Roofer / plumber for a homeowner |
| Installation | Dropped into an existing outlet, no tools, no change to the gutter | Replaces the standard outlet (clipped or soldered like an EN 612 outlet) |
| First sizes | Gutter NW 333, downpipe DN 87–100 | Gutter NW 333, downpipe DN 87 and DN 100 |
| Strength | Retrofit to millions of existing gutters | More room, better sealing, matching gutter metal |
| Main constraint | Cap must stay below the gutter rim; very little PV area | Must match titanium zinc, copper and aluminium gutters without galvanic corrosion |
| Option | Bluetooth Low Energy app (status, history, firmware update) | same |

## 4. Who it is for

- **Homeowners** with trees near the house who clean gutters several times each autumn.
- **Property managers** with many downpipes and expensive cleaning visits.
- **Roofers**, who can offer V2 as an upgrade when installing new gutters.

## 5. What success looks like

- The outlet does not block during a normal autumn, with no ladder visit.
- No visible water overflow at the outlet during design rainfall with typical leaf fall.
- The device runs on solar energy alone from September to December in Central Europe.
- No hazard to a person who opens or services it.

## 6. Development frame

- **Functional safety:** the customer requires ISO 26262:2018, tailored to this item, with ASILs determined by hazard analysis and risk assessment. It is a contractual development frame chosen by the customer.
- **Process:** Automotive SPICE 4.0 (SYS.1–SYS.5, SWE.1–SWE.6, MAN.3, SUP.1, SUP.8–SUP.10), target capability level 2.
- **Legal product compliance (EU):**
  - Machinery Regulation (EU) 2023/1230, EMC Directive 2014/30/EU, RoHS 2011/65/EU, WEEE 2012/19/EU, Battery Regulation (EU) 2023/1542 and the General Product Safety Regulation (EU) 2023/988.
  - With the BLE option, also the Radio Equipment Directive 2014/53/EU (including EN 18031-1) and the Cyber Resilience Act (EU) 2024/2847.

## 7. Open points (not researched yet)

1. Trademark clearance for "Fluvoro" (DPMA, EUIPO).
2. Prior art and freedom to operate for gutter shredders and self-cleaning outlets.
3. The real hydraulic capacity of NW 333 / DN 87–100 outlets with the device installed (needs a flow test).
4. The real PV yield of a cap-sized panel inside a gutter in November (needs a field measurement).
5. Cost targets and volumes, confirmed by a market check.
