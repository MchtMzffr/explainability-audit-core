# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-EXPL-SEC-1: Explanation output must not contain secret/PII patterns."""

import re

from decision_schema.packet_v2 import PacketV2

from explainability_audit_core import explain_from_packet

# Denylist patterns (simple; extend as needed)
SECRET_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.I),
    re.compile(r"api[_-]?key\s*[:=]\s*[\w-]+", re.I),
    re.compile(r"password\s*[:=]\s*\S+", re.I),
]


def test_inv_expl_sec_1_artifact_redaction_ok() -> None:
    """ExplanationArtifact.redaction_ok must be True (we do not emit raw input)."""
    packet = PacketV2(
        run_id="r1",
        step=1,
        input={"key": "value"},
        external={},
        mdm={},
        final_action={"allowed": True},
        latency_ms=0,
    )
    art = explain_from_packet(packet)
    assert art.redaction_ok is True


def test_inv_expl_sec_1_to_dict_no_secret_patterns() -> None:
    """Serialized to_dict() must not contain denylist patterns."""
    packet = PacketV2(
        run_id="r1",
        step=1,
        input={},
        external={},
        mdm={},
        final_action={"allowed": True},
        latency_ms=0,
    )
    art = explain_from_packet(packet)
    text = str(art.to_dict())
    for pat in SECRET_PATTERNS:
        assert not pat.search(text), f"INV-EXPL-SEC-1: secret pattern found: {pat.pattern}"
