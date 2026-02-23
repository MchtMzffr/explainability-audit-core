# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Tests for explain() and Explanation (domain-agnostic)."""

from explainability_audit_core import explain, ReasonCode


def test_explain_allowed_no_guards() -> None:
    e = explain(allowed=True)
    assert ReasonCode.ALLOWED in e.reason_codes
    assert e.summary == "Decision allowed; no guard denied."


def test_explain_denied_fail_closed() -> None:
    e = explain(allowed=False, fail_closed=True)
    assert ReasonCode.FAIL_CLOSED in e.reason_codes
    assert "fail-closed" in e.summary.lower()


def test_explain_denied_guard_chain() -> None:
    e = explain(allowed=False, guard_chain=[("ops_health", "guard deny")])
    assert ReasonCode.GUARD_DENY in e.reason_codes
    assert len(e.triggered_guards) == 1
    assert e.triggered_guards[0].guard_name == "ops_health"


def test_explain_to_audit_dict() -> None:
    e = explain(allowed=False, fail_closed=True)
    d = e.to_audit_dict()
    assert "reason_codes" in d
    assert "FAIL_CLOSED" in d["reason_codes"]
    assert "summary" in d
