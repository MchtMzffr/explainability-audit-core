# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Domain-agnostic models for explanation and audit."""

from dataclasses import dataclass, field
from enum import Enum


class ReasonCode(str, Enum):
    """Domain-agnostic reason codes for audit/compliance."""

    ALLOWED = "ALLOWED"
    GUARD_DENY = "GUARD_DENY"
    KILL_SWITCH = "KILL_SWITCH"
    THRESHOLD_EXCEEDED = "THRESHOLD_EXCEEDED"
    FAIL_CLOSED = "FAIL_CLOSED"
    UNKNOWN = "UNKNOWN"


@dataclass
class GuardTrigger:
    """Single guard that fired (name + reason)."""

    guard_name: str
    reason_code: ReasonCode
    detail: str = ""


@dataclass
class Explanation:
    """Audit-ready explanation for a decision."""

    reason_codes: list[ReasonCode] = field(default_factory=list)
    triggered_guards: list[GuardTrigger] = field(default_factory=list)
    summary: str = ""

    def to_audit_dict(self) -> dict:
        """Serializable dict for logs/audit trails."""
        return {
            "reason_codes": [c.value for c in self.reason_codes],
            "triggered_guards": [
                {"guard_name": g.guard_name, "reason_code": g.reason_code.value, "detail": g.detail}
                for g in self.triggered_guards
            ],
            "summary": self.summary,
        }


@dataclass
class ExplanationArtifact:
    """
    Trace-derived explanation artifact (PacketV2 → audit output).
    INV-EXPL-*: deterministic, primary_reason_code for denied, coverage, redaction_ok.
    """

    run_id: str
    step: int
    decision: str  # ALLOWED | DENIED
    primary_reason_code: str
    reason_codes: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    coverage: float = 0.0
    redaction_ok: bool = True
    version: str = "0.1.0"

    def to_dict(self) -> dict:
        """Byte-stable JSON-serializable dict (INV-EXPL-DET-1)."""
        return {
            "run_id": self.run_id,
            "step": self.step,
            "decision": self.decision,
            "primary_reason_code": self.primary_reason_code,
            "reason_codes": list(self.reason_codes),
            "evidence_refs": list(self.evidence_refs),
            "coverage": self.coverage,
            "redaction_ok": self.redaction_ok,
            "version": self.version,
        }
