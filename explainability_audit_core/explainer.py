# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Build explanations from decision outcome and guard chain (domain-agnostic)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from explainability_audit_core.model import Explanation, ExplanationArtifact, GuardTrigger, ReasonCode
from explainability_audit_core.reason_templates import REASON_TEMPLATES

if TYPE_CHECKING:
    from decision_schema.packet_v2 import PacketV2


def explain(
    allowed: bool,
    guard_chain: list[tuple[str, str]] | None = None,
    fail_closed: bool = False,
) -> Explanation:
    """
    Produce an audit-ready explanation for a decision.

    Args:
        allowed: Whether the final decision was allowed (ACT) or denied (HOLD).
        guard_chain: Optional list of (guard_name, reason) that contributed.
        fail_closed: True if decision was deny due to exception/fail-closed.

    Returns:
        Explanation with reason_codes, triggered_guards, and summary.
    """
    reason_codes: list[ReasonCode] = []
    triggered_guards: list[GuardTrigger] = []
    if fail_closed:
        reason_codes.append(ReasonCode.FAIL_CLOSED)
        triggered_guards.append(
            GuardTrigger(guard_name="system", reason_code=ReasonCode.FAIL_CLOSED, detail="exception")
        )
    if guard_chain:
        for name, reason in guard_chain:
            code = _reason_to_code(reason)
            reason_codes.append(code)
            triggered_guards.append(GuardTrigger(guard_name=name, reason_code=code, detail=reason))
    if allowed and not reason_codes:
        reason_codes.append(ReasonCode.ALLOWED)
    elif not allowed and not any(
        c in reason_codes
        for c in (ReasonCode.FAIL_CLOSED, ReasonCode.GUARD_DENY, ReasonCode.KILL_SWITCH)
    ):
        reason_codes.append(ReasonCode.THRESHOLD_EXCEEDED)

    summary = _build_summary(allowed, reason_codes)
    return Explanation(
        reason_codes=reason_codes,
        triggered_guards=triggered_guards,
        summary=summary,
    )


def _reason_to_code(reason: str) -> ReasonCode:
    r = reason.upper()
    if "KILL" in r or "COOLDOWN" in r:
        return ReasonCode.KILL_SWITCH
    if "DENY" in r or "HOLD" in r or "GUARD" in r:
        return ReasonCode.GUARD_DENY
    if "THRESHOLD" in r or "EXCEED" in r:
        return ReasonCode.THRESHOLD_EXCEEDED
    if "FAIL" in r or "CLOSED" in r:
        return ReasonCode.FAIL_CLOSED
    return ReasonCode.UNKNOWN


def _build_summary(allowed: bool, reason_codes: list[ReasonCode]) -> str:
    if allowed:
        return "Decision allowed; no guard denied."
    if ReasonCode.FAIL_CLOSED in reason_codes:
        return "Decision denied: fail-closed (exception or error)."
    if ReasonCode.KILL_SWITCH in reason_codes:
        return "Decision denied: kill-switch or cooldown active."
    if ReasonCode.GUARD_DENY in reason_codes:
        return "Decision denied: one or more guards denied."
    if ReasonCode.THRESHOLD_EXCEEDED in reason_codes:
        return "Decision denied: threshold exceeded."
    return "Decision denied."


def explain_from_packet(packet: "PacketV2") -> ExplanationArtifact:
    """
    Build ExplanationArtifact from PacketV2 trace (INV-EXPL-MIN-1, INV-EXPL-DET-1).

    Expected packet shape (dict-like or PacketV2): run_id, step, final_action (dict with
    "allowed", "action"), mismatch (dict with "reason_codes", "flags"), mdm (dict with
    "reasons"). primary_reason_code = first failing reason when allowed=False.

    Reason code mapping: known codes (e.g. ops_deny_actions, guard names) map to ReasonCode
    enum; unknown or namespaced reason_codes map to ReasonCode.UNKNOWN (INV-EXPL-RC-1).
    """
    from explainability_audit_core.version import __version__

    run_id = getattr(packet, "run_id", "") or ""
    step = getattr(packet, "step", 0) or 0
    final = getattr(packet, "final_action", None) or {}
    mismatch = getattr(packet, "mismatch", None) or {}
    mdm = getattr(packet, "mdm", None) or {}

    allowed = final.get("allowed", True)
    reason_codes = list(mismatch.get("reason_codes") or [])
    flags = list(mismatch.get("flags") or [])
    proposal_reasons = list(mdm.get("reasons") or [])

    evidence_available = ["final_action", "mismatch", "mdm.reasons"]
    evidence_used: list[str] = ["final_action"]
    if reason_codes:
        evidence_used.append("mismatch.reason_codes")
    if flags:
        evidence_used.append("mismatch.flags")
    if proposal_reasons:
        evidence_used.append("mdm.reasons")
    coverage = len(evidence_used) / len(evidence_available) if evidence_available else 0.0

    if allowed:
        decision = "ALLOWED"
        primary_reason_code = "ALLOWED"
        if not reason_codes:
            reason_codes = ["ALLOWED"]
    else:
        decision = "DENIED"
        primary_reason_code = reason_codes[0] if reason_codes else "FAIL_CLOSED"
        if not reason_codes:
            reason_codes = [primary_reason_code]

    return ExplanationArtifact(
        run_id=run_id,
        step=step,
        decision=decision,
        primary_reason_code=primary_reason_code,
        reason_codes=reason_codes,
        evidence_refs=evidence_used,
        coverage=round(coverage, 2),
        redaction_ok=True,
        version=__version__,
    )
