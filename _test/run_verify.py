#!/usr/bin/env python3
"""
VSteach Project Verify Script
=============================
Run: python _test/run_verify.py

Checks:
1. Python syntax -- scan all .py files
2. Module import -- verify key modules load
3. File integrity -- critical files exist and non-empty
"""

import ast
import importlib
import os
import sys
from pathlib import Path, PureWindowsPath

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

OK = "[PASS]"
WARN = "[WARN]"
FAIL = "[FAIL]"

KEY_MODULES = []  # add modules like "_CHRIS.bangongyong_md2pdf" when needed

KEY_FILES = [
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/skills/chris-daily-plan/SKILL.md",
]

EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules", ".venv", ".agents"}


def check_python_syntax():
    results = []
    for f in sorted(ROOT.rglob("*.py")):
        rel = f.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        try:
            source = f.read_text(encoding="utf-8")
            ast.parse(source)
        except SyntaxError as e:
            results.append({"file": str(rel), "status": "FAIL",
                            "detail": "SyntaxError: {} (line {})".format(e.msg, e.lineno)})
        except Exception as e:
            results.append({"file": str(rel), "status": "ERROR",
                            "detail": str(e)})
    return results


def check_module_import(name):
    try:
        importlib.import_module(name)
        return {"module": name, "status": "PASS", "detail": ""}
    except Exception as e:
        return {"module": name, "status": "FAIL", "detail": str(e)}


def check_file_exists(fp):
    p = ROOT / fp
    if p.exists():
        sz = p.stat().st_size
        return {"file": fp, "status": "PASS" if sz > 0 else "WARN",
                "detail": "{} bytes".format(sz) if sz > 0 else "empty"}
    return {"file": fp, "status": "FAIL", "detail": "not found"}


def report(title, items):
    if not items:
        print("  {} {} -- 0 items".format(OK, title))
        return 0

    print("\n" + "=" * 60)
    print("  " + title)
    print("=" * 60)

    fails = [i for i in items if i.get("status") in ("FAIL", "ERROR")]
    passes = [i for i in items if i.get("status") == "PASS"]
    warns = [i for i in items if i.get("status") == "WARN"]

    if passes:
        print("  {} Pass: {}".format(OK, len(passes)))
    if warns:
        print("  {} Warn: {}".format(WARN, len(warns)))
    if fails:
        print("  {} Fail: {}".format(FAIL, len(fails)))
        for f in fails:
            name = f.get("file") or f.get("module") or "?"
            print("    - {}: {}".format(name, f.get("detail", "")))
    return len(fails)


def main():
    title = "VSteach Project Verify"
    print("#" * 60)
    print("  " + title)
    print("  " + __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M"))
    print("  " + str(ROOT))
    print("#" * 60)

    total = 0
    total += report("Python Syntax", check_python_syntax())
    total += report("Module Import", [check_module_import(m) for m in KEY_MODULES])
    total += report("File Integrity", [r for r in (check_file_exists(f) for f in KEY_FILES) if r])

    print("\n" + "=" * 60)
    if total == 0:
        print("  {} All checks passed!".format(OK))
    else:
        print("  {} {} check(s) failed, please fix".format(FAIL, total))
    print("=" * 60 + "\n")
    return 1 if total > 0 else 0


if __name__ == "__main__":
    sys.exit(main())