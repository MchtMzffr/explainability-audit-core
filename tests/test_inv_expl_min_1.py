# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-EXPL-MIN-1: allowed=False ⇒ explanation contains primary_reason_code."""

from decision_schema.packet_v2 import PacketV2

from explainability_audit_core import explain_from_packet


def test_inv_expl_min_1_denied_has_primary_reason() -> None:
    """When decision is DENIED, primary_reason_code must be set (first failing guard)."""
    packet = PacketV2(
        run_id="r1",
        step=1,
        input={},
        external={},
        mdm={},
        final_action={"allowed": False, "action": "HOLD"},
        latency_ms=0,
        mismatch={"reason_codes": ["KILL_SWITCH"], "flags": []},
    )
    art = explain_from_packet(packet)
    assert art.decision == "DENIED"
    assert art.primary_reason_code == "KILL_SWITCH"
    assert art.primary_reason_code in art.reason_codes


def test_inv_expl_min_1_denied_no_mismatch_uses_fail_closed() -> None:
    """When allowed=False but no reason_codes, primary_reason_code = FAIL_CLOSED."""
    packet = PacketV2(
        run_id="r2",
        step=1,
        input={},
        external={},
        mdm={},
        final_action={"allowed": False},
        latency_ms=0,
        mismatch=None,
    )
    art = explain_from_packet(packet)
    assert art.decision == "DENIED"
    assert art.primary_reason_code == "FAIL_CLOSED"
