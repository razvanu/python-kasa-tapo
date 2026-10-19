#!/usr/bin/env python3
"""Build isolated python-kasa TPAP namespace for the HACS integration.

Input: a checked-out, SHA-pinned python-kasa PR #1592 tree.
Output: custom_components/tapo_tpap/_vendor/kasa

Never import or install the input package as globally named 'kasa' in HA.
Original python-kasa code is GPL-3.0-or-later; retain LICENSE and notices.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path
import re
import shutil
import sys

NAMESPACE = "custom_components.tapo_tpap._vendor.kasa"
FROM_RE = re.compile(r"(?m)^(\s*from\s+)kasa(?=(?:\.[A-Za-z_][\w.]*)?\s+import\b)")
IMPORT_RE = re.compile(r"(?m)^(\s*import\s+)kasa\s*(?=(?:#.*)?$)")
IMPORT_OTHER_RE = re.compile(r"(?m)^\s*import\s+kasa(?:\.|,)")
VENDOR_MARKER = "0.10.2+tpap-vendored"


def rewrite(content: str, source: Path) -> str:
    if IMPORT_OTHER_RE.search(content):
        raise ValueError(f"Unsupported complex kasa import in {source}")
    content = FROM_RE.sub(r"\1" + NAMESPACE, content)
    content = IMPORT_RE.sub(r"\1" + NAMESPACE + " as kasa", content)
    if source.as_posix() == "kasa/__init__.py":
        content = content.replace(
            '__version__ = version("python-kasa")',
            f'__version__ = "{VENDOR_MARKER}"',
        )
    ast.parse(content, filename=str(source))
    # Avoid leaving top-level imported 'kasa' references.
    tree = ast.parse(content, filename=str(source))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and (
            node.module == "kasa" or
            (node.module or "").startswith("kasa.")
        ):
            raise AssertionError(f"Non-isolated kasa import: {source}")
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "kasa" or alias.name.startswith("kasa."):
                    raise AssertionError(f"Non-isolated kasa import: {source}")
    return content


def build(source: Path, dest: Path) -> int:
    src = source / "kasa"
    if not (src / "__init__.py").exists():
        raise FileNotFoundError(f"Missing python-kasa source: {src}")
    if dest.exists():
        shutil.rmtree(dest)
    count = 0
    for file in src.rglob("*"):
        if not file.is_file() or "__pycache__" in file.parts:
            continue
        relative = file.relative_to(src)
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if file.suffix == ".py":
            target.write_text(rewrite(file.read_text(encoding="utf-8"),
                                      Path("kasa") / relative), encoding="utf-8")
            count += 1
        else:
            shutil.copy2(file, target)
    license_src = source / "LICENSE"
    if license_src.exists():
        shutil.copy2(license_src, dest / "LICENSE")
    (dest.parent / "__init__.py").write_text(
        '"""Isolated vendored python-kasa TPAP package."""\n',
        encoding="utf-8",
    )
    print(f"Vendored {count} Python modules to {dest}; namespace {NAMESPACE}")
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument(
        "--dest", type=Path,
        default=Path("custom_components/tapo_tpap/_vendor/kasa"))
    options = parser.parse_args()
    count = build(options.source.resolve(), options.dest.resolve())
    sys.exit(0 if count > 0 else 1)
