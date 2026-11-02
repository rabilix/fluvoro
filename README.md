# Fluvoro

A battery-powered, solar-charged leaf shredder that sits in a gutter outlet
(German: *Rinnenstutzen*) and keeps it from clogging.

This repository holds two things that must never be mixed:

| Path | What | Who may see it |
|---|---|---|
| `product/` | The **clean reference specification**: the real product specification if Fluvoro goes ahead | Engineering; never a simulation run |
| `kit/shown/` | What a simulated customer hands to the system under test (RFQ, customer requirements specification, change request) | The system under test |
| `kit/hidden/` | Answer key, seeded-defect list, customer answer book, blind estimate | The judge only |
| `kit/plant/` | Plant model and scenarios (host-side C) for qualification | The judge only |
| `kit/variants/` | Negative-control variants per phase | The judge only |
| `docs/` | Product brief, provenance | Engineering |

**Isolation rule.** Only `kit/shown/` may ever be ingested into a knowledge
collection a simulation run can reach. `product/` and `kit/hidden/` may be ingested
only into a separate collection that no simulation key is scoped to.

The simulation framework that uses this kit is described in FlexForge
`docs/superpowers/specs/2026-11-01-user-simulation-gutter-shredder-concept.md`.

Everything here is a DRAFT until the maintainer reviews it. Every number marked
`basis: engineering_assumption` must be confirmed before it is used for a real product.
