## Blind quote estimate: Fluvoro (RFQ-FLV-2026-01)

**Finished:** 2 November 2026, 22:07 CET (UTC+01:00)  
**Basis:** `rfq.md` and `fluvoro_crs_v1.reqif` only  
**Estimate type:** Independent rough-order-of-magnitude engineering estimate  
**Unit:** Person-day (PD), assumed as 8 productive hours

### 1. Assumptions

#### Open points from RFQ §5

- **Volume split V1/V2:** 70% V1 insert and 30% V2 replacement outlet during the first two years. The software baseline is common to both variants. Variant-specific effort is mainly in system requirements, system architecture, interfaces, calibration, integration, and qualification. Production volume does not materially change development effort, except for cost engineering, traceability, and end-of-line considerations.
- **Connectivity timing:** BLE is assumed to be available from start of production in September 2028. It is developed as an independent option and does not control or start the rotor. The quote includes only device-side BLE, pairing, diagnostic/event data, notifications, and the secure firmware-update path. Smartphone application development is excluded.
- **Hardware partner:** A customer-nominated hardware/mechanical partner provides schematics, PCB, motor stage, sensing, battery/charging design, mechanics, prototypes, and hardware verification. This estimate covers system/software definition, hardware-software interface, safety requirements allocated to hardware, technical reviews, and support of hardware integration. Detailed electronics design, PCB layout, mechanical design, tooling, and manufacturing industrialisation are excluded.

#### Other effort-significant assumptions

- One common electronic control platform and one common firmware baseline serve V1 and V2, with configuration/calibration differences only.
- First release covers NW 333 and DN 87/DN 100 only. The three V2 gutter materials do not create separate firmware variants.
- Customer provides timely access to representative V1/V2 mechanical prototypes, electronics, motor/rotor assemblies, batteries, solar elements, gutters/outlets, and test fixtures.
- The CRS is the contractual baseline. Up to 15% requirements clarification/refinement and normal controlled change are included. Major changes to product concept, safety architecture, MCU, sensors, motor, battery, or schedule require re-estimation.
- Development follows Automotive SPICE 4.0 capability-level-2 intent for the processes named in FLV-STK-140. The estimate includes work products and assurance activities, but not a formal external ASPICE assessment.
- ISO 26262:2018 is applied as contractually requested and tailored to this non-automotive item. The estimate assumes that the HARA does not produce requirements above ASIL B. An ASIL C/D outcome, freedom-from-interference partitioning, redundant sensing, or a safety-certified MCU would require re-estimation.
- Machinery risk assessment to EN ISO 12100 and IEC 60730-1 Annex H Class B engineering are included where they affect system/software. Full legal conformity assessment, certification-body fees, laboratory fees, CE declaration ownership, and product certification are excluded.
- Qualification effort includes test specification, execution support, analysis, reporting, and regression on representative samples. Accredited external laboratory execution, destructive hardware tests, long-duration UV/lifetime campaigns, hydraulic rig construction, EMC chamber fees, and certification fees are excluded. Supplier analyses and available partner/lab reports are incorporated as evidence.
- Test automation uses standard embedded unit-test and host/HIL tooling already available to the supplier. Purchase or development of a major custom HIL platform is excluded.
- Software is bare-metal or RTOS-based embedded C on one MCU. Reuse of qualified vendor drivers, MCU libraries, BLE stack, bootloader primitives, and cryptographic libraries is permitted. No custom radio stack or cryptographic algorithm is developed.
- Secure firmware update is local/device-side. A cloud backend, update campaign service, app distribution, PKI operation, and long-term vulnerability-monitoring service are excluded.
- The estimate includes one B-sample and one C-sample release baseline, plus normal internal integration drops. One major re-spin of the electronics after initial integration is assumed.
- Customer and partner reviews/decisions are returned within five working days. Delays in hardware maturity or safety decisions shift milestones without reducing effort.
- Project calendar assumes kick-off in February 2027, B-sample in October 2027, and C-sample in April 2028. The quoted effort is engineering effort, not elapsed staffing duration.
- A contingency reserve is included explicitly because hardware characteristics, HARA outcome, environmental test findings, and the feasibility of the 2 mW standby target are not yet demonstrated.

### 2. Effort per work package

| Work package | Systems engineering | Software | Functional safety | Test / verification | Project / QA | Total PD |
|---|---:|---:|---:|---:|---:|---:|
| WP1 Project setup, planning, ASPICE/QA infrastructure, configuration and change management | 4 | 3 | 2 | 2 | 24 | 35 |
| WP2 Stakeholder requirements analysis and bidirectional traceability | 32 | 8 | 8 | 8 | 6 | 62 |
| WP3 System requirements and system architecture, including V1/V2, energy, hydraulics, HW/SW interface and compliance allocation | 50 | 18 | 16 | 12 | 6 | 102 |
| WP4 Functional safety and machinery-safety engineering: item definition, HARA, FSC/TSC, safety analyses, safety plan and safety case | 12 | 8 | 72 | 12 | 8 | 112 |
| WP5 Software requirements and architecture | 12 | 52 | 14 | 8 | 6 | 92 |
| WP6 Base software, drivers and platform services: MCU, sensors, motor/PWM, battery/solar, RTC, NVM, diagnostics and service interface | 6 | 90 | 8 | 20 | 5 | 129 |
| WP7 Application software: clog detection, shred/jam control, energy management, self-test, state machine, signalling, event log and variant handling | 8 | 112 | 12 | 26 | 6 | 164 |
| WP8 Software detailed design, unit verification, static analysis and code reviews | 2 | 68 | 6 | 42 | 6 | 124 |
| WP9 Software integration and verification on target | 6 | 48 | 8 | 55 | 7 | 124 |
| WP10 System integration and B-sample feature-complete validation | 26 | 32 | 10 | 65 | 10 | 143 |
| WP11 C-sample qualification, regression, compliance evidence and release | 24 | 24 | 16 | 78 | 12 | 154 |
| WP12 Deliverable consolidation, traceability report, safety-case completion and final release package | 10 | 12 | 24 | 16 | 14 | 76 |
| WP13 Explicit technical contingency, approximately 12% | 23 | 57 | 24 | 41 | 13 | 158 |
| **Total, base scope without BLE option** | **215** | **532** | **220** | **385** | **127** | **1,479** |
| **Connectivity option, BLE, separate** | **18** | **115** | **12** | **65** | **15** | **225** |
| **Total if BLE is ordered for SOP** | **233** | **647** | **232** | **450** | **142** | **1,704** |

#### BLE option composition

The 225 PD option includes device-side BLE requirements and architecture, GATT/interface definition, physical-presence pairing, read-only operational data, event-log transfer, notification support, authenticated firmware and fail-safe update behavior, cybersecurity TARA and requirements, ISO/SAE 21434 work products for the radio/update path, RED/EN 18031-1 evidence support, integration, security tests, robustness tests, qualification, traceability, and option-specific management. It excludes the smartphone app, backend services, hosted update infrastructure, certification fees, and long-term product cybersecurity operations.

#### Estimate interpretation

- **Recommended quotation basis:** 1,479 PD for the base scope, plus 225 PD for BLE.
- **Expected accuracy at RFQ stage:** approximately -15% / +25% for the base scope. BLE uncertainty is approximately -15% / +30%, mainly due to the update architecture and regulatory/cybersecurity evidence.
- **Primary cost drivers:** full SYS.1-SYS.5 and SWE.1-SWE.6 lifecycle, traceability to code/tests, motor and jam control, very-low-power operation, safety activities, two physical variants, broad qualification evidence, and compliance-related verification.

### 3. Milestones and work-package mapping

| Milestone / period | Planned content | Work packages | Exit criteria |
|---|---|---|---|
| Kick-off and planning, Feb-Mar 2027 | Plans, lifecycle, repositories/tools, configuration/change process, initial CRS analysis, partner interfaces | WP1, WP2 start | Approved development, quality, configuration, verification and safety plans; requirements issues logged; traceability framework operational |
| System and safety concept, Mar-May 2027 | System requirements/architecture, HW/SW interface, variant concept, item definition, HARA, safety goals, FSC and preliminary TSC | WP2, WP3, WP4 | Reviewed system baseline; safety concept accepted; hardware allocations and prototype needs agreed |
| Software definition, Apr-Jun 2027 | Software requirements/architecture, interfaces, diagnostics, energy strategy, control concept, test strategy | WP5, early WP6-WP8 | SWE.1/SWE.2 baselines reviewed; unit/integration test framework operational |
| Incremental implementation and bench integration, May-Sep 2027 | Drivers, platform, state machine, motor/jam control, battery/solar functions, signalling, log, service/update path and variant configuration | WP6, WP7, WP8, WP9 | Feature increments integrated on target; unit and integration evidence available; no unresolved blocker to B-sample |
| **B-sample software, October 2027** | Feature-complete base software for V1/V2; BLE feature complete if option ordered; preliminary safety mechanisms integrated | WP1-WP10 substantially complete; WP11 started | All planned product features implemented; target integration passed; representative V1/V2 demonstration completed; known limitations documented; preliminary traceability and safety evidence available |
| Qualification preparation and corrective loop, Nov 2027-Jan 2028 | System qualification procedures, compliance evidence collection, fault injection, environmental/EMC/lab support, defect correction | WP9, WP10, WP11; remaining WP4 | Qualification baseline frozen; major B-sample defects resolved; safety analyses updated with test evidence |
| C-sample qualification, Feb-Mar 2028 | Full regression, system/software qualification, variant coverage, safety validation, release-candidate testing | WP11, WP12 | Qualification reports complete; residual anomalies accepted; complete bidirectional traceability; release candidate approved |
| **C-sample software, April 2028** | Qualified software and completed safety case/release package | WP4, WP11, WP12 complete | Qualified base and optional BLE software released; safety case complete; required deliverables accepted |
| SOP support, May-Sep 2028 | Limited defect correction, production/EOL support and release maintenance | Small residual allowance within WP11-WP13 | Production software baseline and EOL interfaces stable before September 2028 SOP |

### 4. Deliverables cross-check against FLV-STK-142

| FLV-STK-142 requested deliverable | Planned deliverable / evidence | Main work package |
|---|---|---|
| System requirements | Reviewed system-requirements specification, including V1/V2 allocations, interface requirements and verification criteria | WP2, WP3 |
| System architecture | System architecture description, interfaces, HW/SW allocation, variant concept, safety mechanisms and architecture views | WP3, WP4 |
| Software requirements | Software-requirements specification with safety classification, verification criteria and trace links | WP5 |
| Software architecture | Software architecture description, component/interface design, runtime behavior, memory/NVM concept and variant handling | WP5 |
| Safety work products from FLV-STK-070 | Safety plan, item definition, HARA/ASIL determination, safety goals, FSC, TSC, applicable analyses, verification evidence and safety case | WP4, WP11, WP12 |
| Source code | Embedded C source, configuration, build scripts, generated configuration where applicable, and release tags/baselines | WP6-WP9, WP12 |
| Test specifications | Unit, software integration, software qualification, system integration and system qualification specifications/procedures | WP8-WP11 |
| Test reports | Unit/static-analysis reports, software integration/qualification reports, system integration/qualification reports and regression summary | WP8-WP11 |
| Traceability report | Bidirectional stakeholder-to-system-to-software-to-architecture-to-code-to-test traceability report, including coverage and gaps | WP2-WP12 |

### 5. Exclusions and quotation qualifications

The estimate excludes industrial design, detailed electronics and mechanics, tooling, series production, smartphone app development, cloud/backend services, certification and accredited-laboratory fees, test-specimen costs, production equipment, translations, and post-SOP maintenance. Hardware/mechanical partner deliverables remain dependencies for system integration, safety evidence, and qualification. Any quotation should therefore contain a formal change-control mechanism and milestone assumptions tied to prototype and hardware availability.
