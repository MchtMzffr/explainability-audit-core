# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Domain-agnostic reason code templates (INV-EXPL-RC-1)."""

REASON_TEMPLATES: dict[str, str] = {
    "ALLOWED": "Decision allowed; no guard denied.",
    "GUARD_DENY": "Decision denied: one or more guards denied.",
    "KILL_SWITCH": "Decision denied: kill-switch or cooldown active.",
    "THRESHOLD_EXCEEDED": "Decision denied: threshold exceeded.",
    "FAIL_CLOSED": "Decision denied: fail-closed (exception or error).",
    "UNKNOWN": "Decision denied: reason not resolved (namespaced or unknown).",
}

# Namespaced prefix: domain-specific codes must start with this to pass INV-EXPL-RC-1
NAMESPACED_PREFIX = "example_domain:"
