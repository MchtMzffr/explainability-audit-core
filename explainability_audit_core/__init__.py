# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Explainability and Audit Core: domain-agnostic reason codes and guard-chain explanation."""

from explainability_audit_core.version import __version__
from explainability_audit_core.model import Explanation, ExplanationArtifact, GuardTrigger, ReasonCode
from explainability_audit_core.explainer import explain, explain_from_packet

__all__ = [
    "__version__",
    "Explanation",
    "ExplanationArtifact",
    "GuardTrigger",
    "ReasonCode",
    "explain",
    "explain_from_packet",
]
