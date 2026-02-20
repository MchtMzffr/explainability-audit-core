# explainability-audit-core — Formulas

## Evidence set (from PacketV2)

\[
\mathcal{E}(\tau) = \{\ \text{final\_action},\ \text{mismatch.reason\_codes},\ \text{mismatch.flags},\ \text{mdm.reasons}\ \}
\]

(We treat “proposal / features_summary” as reflected in `mdm.reasons` and mismatch fields.)

## Minimal explanation (fail-closed)

For denied decisions, the **minimal** explanation is the first failing guard (deterministic order):

\[
\text{Expl}_{\min}(\tau) = \{\ \text{primary\_reason\_code} = \text{first\_failing\_guard}\ \}
\]

If no `reason_codes` are present, \(\text{primary\_reason\_code} = \texttt{FAIL\_CLOSED}\).

## Coverage (auditability)

\[
\text{coverage} = \frac{|\text{evidence\_used}|}{|\text{evidence\_available}|}
\]

- **evidence_available:** fixed set of keys we consider (e.g. `final_action`, `mismatch`, `mdm.reasons`).
- **evidence_used:** subset actually present and used in this packet.

**INV-EXPL-COV-1:** For core-coded packets, \(\text{coverage} \geq 0.8\).

## Determinism (INV-EXPL-DET-1)

Same \(\tau\) (PacketV2) must yield the same \(\text{ExplanationArtifact}\) and thus the same JSON under `to_dict()\). No randomness; no timestamp in the artifact.

## Redaction (INV-EXPL-SEC-1)

Explanation output must not introduce PII or secrets. We do not copy raw `input`/`external` into the artifact; only references and codes. \(\text{redaction\_ok} = \texttt{True}\) when the pipeline does not emit sensitive data.
