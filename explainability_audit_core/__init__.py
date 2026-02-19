# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Explainability and Audit Core: domain-agnostic reason codes and guard-chain explanation."""

from explainability_audit_core.version import __version__
from explainability_audit_core.model import Explanation, GuardTrigger, ReasonCode
from explainability_audit_core.explainer import explain

__all__ = [
    "__version__",
    "Explanation",
    "GuardTrigger",
    "ReasonCode",
    "explain",
]
