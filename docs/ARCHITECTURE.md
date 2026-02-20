# explainability-audit-core — Architecture

## Purpose

**explainability-audit-core** is the “trace explainer” core of the Decision Ecosystem. It turns a `PacketV2` (single-step decision trace) into a human-readable, audit-ready **explanation**: why a decision was ALLOWED or DENIED, which guard failed first, and what evidence was used.

## Pipeline

```
PacketV2 (decision-schema)
    → explain_from_packet(packet)
    → ExplanationArtifact (run_id, step, decision, primary_reason_code, reason_codes, evidence_refs, coverage, redaction_ok)
    → to_dict() → byte-stable JSON (INV-EXPL-DET-1)
```

- **Input:** `PacketV2` with `final_action`, `mismatch`, `mdm` (and optionally `input`/`external`; we do not re-emit them to avoid PII).
- **Output:** `ExplanationArtifact` with deterministic fields; serialized for logs or integration reports.

## Dependencies

- **decision-schema** only (`PacketV2`); no domain engines. INV-CORE-DEP-1 compliant.
- Domain-specific reason texts are **namespaced** (`example_domain:*`); core uses only domain-agnostic codes and templates.

## Components

| Component        | Role |
|-----------------|------|
| `model.py`      | `ExplanationArtifact`, `Explanation`, `ReasonCode`, `GuardTrigger` |
| `explainer.py`  | `explain_from_packet(packet)`, `explain(allowed, guard_chain, fail_closed)` |
| `reason_templates.py` | `REASON_TEMPLATES`, `NAMESPACED_PREFIX` for INV-EXPL-RC-1 |

## Invariants (summary)

- **INV-EXPL-DET-1:** Same PacketV2 → same JSON.
- **INV-EXPL-MIN-1:** `allowed=False` ⇒ `primary_reason_code` set (first failing guard or FAIL_CLOSED).
- **INV-EXPL-RC-1:** Reason codes resolved via template or namespaced.
- **INV-EXPL-SEC-1:** No secret/PII in explanation output; `redaction_ok=True`.
- **INV-EXPL-COV-1:** Core packets: coverage ≥ 0.8 (evidence_used / evidence_available).

## Integration

Optional step in **decision-ecosystem-integration-harness**: after building `PacketV2`, call `explain_from_packet(packet)` and attach the artifact to the eval report or a separate explanation output.
