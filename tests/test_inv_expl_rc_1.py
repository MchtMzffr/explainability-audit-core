# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""INV-EXPL-RC-1: reason_codes must be template-resolved or namespaced."""

from explainability_audit_core.reason_templates import NAMESPACED_PREFIX, REASON_TEMPLATES


def test_inv_expl_rc_1_all_core_codes_have_template() -> None:
    """Every key in REASON_TEMPLATES must be a non-empty string."""
    for code, template in REASON_TEMPLATES.items():
        assert isinstance(template, str), f"{code}: template must be str"
        assert len(template) > 0, f"{code}: template must be non-empty"


def test_inv_expl_rc_1_namespaced_prefix_defined() -> None:
    """Namespaced codes (example_domain:*) are allowed when template unknown."""
    assert NAMESPACED_PREFIX == "example_domain:"
    assert "example_domain:custom" not in REASON_TEMPLATES  # namespaced, no template required
