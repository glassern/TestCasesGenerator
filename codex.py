#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codex-friendly command wrapper.

This file intentionally does not implement or modify test-case generation
logic. It only calls the existing project scripts so the project can be used
without Amp installed.
"""

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

from config import Config


PROJECT_ROOT = Path(__file__).resolve().parent


def run_python(*args: str) -> int:
    cmd = [sys.executable, *args]
    return subprocess.call(cmd, cwd=PROJECT_ROOT)


def check(_: argparse.Namespace) -> int:
    return run_python(".agents/skills/checking-dependencies/scripts/check_deps.py", "--check")


def check_local(_: argparse.Namespace) -> int:
    missing = []
    for package in ("requests", "openpyxl", "pandas", "cryptography"):
        ok = importlib.util.find_spec(package) is not None
        print(f"{'OK' if ok else 'MISSING'} {package}")
        if not ok:
            missing.append(package)

    pandoc = shutil.which("pandoc")
    print(f"{'OK' if pandoc else 'MISSING'} pandoc" + (f" ({pandoc})" if pandoc else ""))

    if missing:
        print("\nInstall missing Python packages with:")
        print("python3 -m pip install -r requirements.txt")

    if not pandoc:
        print("\nInstall Pandoc before converting .docx files.")

    return 0 if not missing and pandoc else 1


def convert(_: argparse.Namespace) -> int:
    Config.ensure_directories()
    return run_python("script/convert_docx_to_markdown.py")


def excel(_: argparse.Namespace) -> int:
    Config.ensure_directories()
    return run_python("script/generate_final_excel.py")


def status(_: argparse.Namespace) -> int:
    return run_python("tools/project_manager.py", "status")


def reset(args: argparse.Namespace) -> int:
    cmd = [".agents/skills/resetting-workspace/scripts/reset.py"]
    if args.force:
        cmd.append("--force")
    return run_python(*cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Codex-friendly wrapper for the test case project")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="Check dependencies without installing anything")
    check_parser.set_defaults(func=check)

    check_local_parser = subparsers.add_parser("check-local", help="Check local document dependencies only")
    check_local_parser.set_defaults(func=check_local)

    convert_parser = subparsers.add_parser("convert", help="Convert product/*.docx to product/markdown/*.md")
    convert_parser.set_defaults(func=convert)

    excel_parser = subparsers.add_parser("excel", help="Merge output/module_*.json into the final Excel file")
    excel_parser.set_defaults(func=excel)

    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.set_defaults(func=status)

    reset_parser = subparsers.add_parser("reset", help="Preview or execute workspace reset")
    reset_parser.add_argument("--force", action="store_true", help="Delete generated files")
    reset_parser.set_defaults(func=reset)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
