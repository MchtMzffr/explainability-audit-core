# explainability-audit-core — Integration Guide

## Dependency

```toml
# pyproject.toml
[project]
dependencies = ["decision-schema>=0.2.2,<0.3"]
```

## API

```python
from explainability_audit_core import explain_from_packet, ExplanationArtifact
from decision_schema.packet_v2 import PacketV2

packet = PacketV2(
    run_id="r1",
    step=1,
    input={},
    external={},
    mdm={},
    final_action={"allowed": False, "action": "HOLD"},
    latency_ms=10,
    mismatch={"reason_codes": ["GUARD_DENY"], "flags": []},
)
artifact: ExplanationArtifact = explain_from_packet(packet)
print(artifact.decision)           # DENIED
print(artifact.primary_reason_code) # GUARD_DENY
print(artifact.to_dict())           # byte-stable JSON for logs
```

## Optional harness step

In **decision-ecosystem-integration-harness**, after building `PacketV2` for a step:

```python
try:
    from explainability_audit_core import explain_from_packet
    explanation = explain_from_packet(packet)
    report["explanation"] = explanation.to_dict()
except ImportError:
    report["explanation"] = None  # optional dependency
```

Attach `report["explanation"]` to the eval report or write to a separate JSONL (one line per step).

## Namespaced reason codes (example domain)

Domain-specific codes that are not in `REASON_TEMPLATES` should use the namespaced prefix so that INV-EXPL-RC-1 is satisfied (e.g. `example_domain:custom_rule`). Core does not resolve these to human text; the domain layer can map them.

## Invariant tests

Run the full invariant suite:

```bash
pytest tests/test_inv_expl_*.py -v
```

- **INV-EXPL-DET-1:** `test_inv_expl_det_1.py`
- **INV-EXPL-MIN-1:** `test_inv_expl_min_1.py`
- **INV-EXPL-RC-1:** `test_inv_expl_rc_1.py`
- **INV-EXPL-SEC-1:** `test_inv_expl_sec_1.py`
- **INV-EXPL-COV-1:** `test_inv_expl_cov_1.py`
