# explainability-audit-core v0.1.0 — Release Notes

**Tag:** v0.1.0  
**Date:** 2026-02

---

## Summary

First release of **explainability-audit-core** (v0.1.0). Domain-agnostic trace explainer: turns `PacketV2` into an audit-ready `ExplanationArtifact` (primary_reason_code, coverage, redaction_ok). Single dependency: `decision-schema>=0.2.2,<0.3`.

## Compatibility

- Depends only on `decision-schema` (INV-CORE-DEP-1). Pin: `decision-schema>=0.2.2,<0.3`.
- Python >=3.11.

## Security

- No secrets in explanation output (INV-EXPL-SEC-1); `redaction_ok=True`. No PII/secret patterns in serialized artifact.

## Changes

- **Added:** `explain_from_packet(packet: PacketV2) -> ExplanationArtifact`; byte-stable JSON via `to_dict()` (INV-EXPL-DET-1).
- **Added:** `ExplanationArtifact`, `ReasonCode`, `REASON_TEMPLATES`, `NAMESPACED_PREFIX` for domain-agnostic and namespaced reason codes.
- **Added:** INV-EXPL test suite (DET-1, MIN-1, RC-1, SEC-1, COV-1).
- **Added:** Doc trio: ARCHITECTURE.md, FORMULAS.md, INTEGRATION_GUIDE.md.

## Verification

- Tests: `pytest tests/ -v` (INV-EXPL + domain-agnostic).
- Contract gate: decision-schema minor 2.

## Links

- Repository: https://github.com/MchtMzffr/explainability-audit-core
- Tags: https://github.com/MchtMzffr/explainability-audit-core/tags
- Integration: see docs/INTEGRATION_GUIDE.md
