# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-EXPL-COV-1: coverage >= 0.8 for core-coded packets (evidence used/available)."""

from decision_schema.packet_v2 import PacketV2

from explainability_audit_core import explain_from_packet


def test_inv_expl_cov_1_full_evidence_coverage() -> None:
    """Packet with final_action + mismatch + mdm.reasons gives high coverage."""
    packet = PacketV2(
        run_id="r1",
        step=1,
        input={},
        external={},
        mdm={"reasons": ["proposal_reason"]},
        final_action={"allowed": False, "action": "HOLD"},
        latency_ms=5,
        mismatch={"reason_codes": ["GUARD_DENY"], "flags": ["guard_fail"]},
    )
    art = explain_from_packet(packet)
    assert art.coverage >= 0.8, f"INV-EXPL-COV-1: coverage {art.coverage} < 0.8"
    assert len(art.evidence_refs) >= 2
    assert "final_action" in art.evidence_refs
    assert "mismatch.reason_codes" in art.evidence_refs
