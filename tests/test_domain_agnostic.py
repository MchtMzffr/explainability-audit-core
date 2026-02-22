# Decision Ecosystem — explainability-audit-core
# Copyright (c) 2026 Mücahit Muzaffer Karafil (MchtMzffr)
# SPDX-License-Identifier: MIT
"""Domain-agnosticism: no domain-specific imports or types from other cores."""

import ast
from pathlib import Path


def test_no_cross_core_imports() -> None:
    """Package must not import from other ecosystem cores (only decision_schema)."""
    pkg_root = Path(__file__).resolve().parent.parent / "explainability_audit_core"
    allowed = {"__future__", "decision_schema", "explainability_audit_core", "dataclasses", "enum", "typing"}
    for path in pkg_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    assert top in allowed, f"{path}: forbidden import {alias.name}"
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    top = node.module.split(".")[0]
                    assert top in allowed, f"{path}: forbidden import from {node.module}"
