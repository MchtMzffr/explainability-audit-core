# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-EXPL-DET-1: Same PacketV2 → byte-stable same JSON explanation."""

import json

from decision_schema.packet_v2 import PacketV2

from explainability_audit_core import explain_from_packet


def test_inv_expl_det_1_same_packet_same_json() -> None:
    """Same packet twice must produce identical JSON (deterministic)."""
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
    a1 = explain_from_packet(packet)
    a2 = explain_from_packet(packet)
    d1 = a1.to_dict()
    d2 = a2.to_dict()
    assert json.dumps(d1, sort_keys=True) == json.dumps(d2, sort_keys=True)
    assert d1["primary_reason_code"] == "GUARD_DENY"
    assert d1["decision"] == "DENIED"
