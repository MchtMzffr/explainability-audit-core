# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Build explanations from decision outcome and guard chain (domain-agnostic)."""

from explainability_audit_core.model import Explanation, GuardTrigger, ReasonCode


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
