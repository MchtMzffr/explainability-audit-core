# explainability-audit-core

Domain-agnostic explainability and audit for the Decision Ecosystem: reason codes and guard-chain explanation for decision transparency and compliance.

**Status:** Minimal core; active development deferred. CI runs on push/PR/tag.

## Install

```bash
pip install "explainability-audit-core>=0.1,<0.2"
```

Requires `decision-schema>=0.2.2,<0.3`.

## Usage

```python
from explainability_audit_core import explain, ReasonCode

# Decision was allowed
e = explain(allowed=True)
# e.reason_codes -> [ReasonCode.ALLOWED], e.summary -> "Decision allowed; no guard denied."

# Decision denied (e.g. fail-closed)
e = explain(allowed=False, fail_closed=True)
# e.reason_codes -> [ReasonCode.FAIL_CLOSED], e.to_audit_dict() for logs
```

## Scope (future)

- Proposal explanation, guard trigger chain, domain-agnostic reason codes.
- See [NEXT_STEPS_ROADMAP.md](https://github.com/MchtMzffr/decision-ecosystem-docs/blob/main/NEXT_STEPS_ROADMAP.md) in the docs repo.

## License

MIT. See [LICENSE](LICENSE).
