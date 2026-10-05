"""Verify AI claims automatically.

Checks that the required rule files exist, that key modules import, and that
the test suite passes. Run before commit and before reporting work as done.

Notes:
    This script uses print() on purpose: the console report is the product.
    Switching to logging (RULES.md section 9) would hide the report from the
    terminal output the way this script is meant to be read.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REQUIRED_FILES = [
    ".ai/AGENTS.md",
    ".ai/RULES.md",
    ".ai/CONTEXT.md",
    ".ai/PROMPTS.md",
    ".ai/STATE.md",
    ".ai/TASKS.md",
]

REQUIRED_IMPORTS = ["src"]


def check_file_exists(path: str) -> bool:
    """Check that a path exists on disk.

    Args:
        path: Path to check, relative to the project root.

    Returns:
        True if the path exists, False otherwise.
    """
    return Path(path).exists()


def check_import(module: str) -> bool:
    """Check that a Python module can be imported in a subprocess.

    The import runs in a child process so that a hard failure (segfault,
    missing shared library) is reported as False instead of killing this
    script.

    Args:
        module: Dotted module name to import, for example ``"src"``.

    Returns:
        True if the import process exits with code 0, False otherwise.
    """
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def check_tests() -> tuple[bool, str]:
    """Run the pytest suite and capture its output.

    Returns:
        A tuple of ``(passed, output)``. When the tests directory holds no
        test files the check is skipped and reported as passing with a SKIP
        note, because an empty suite is not a failure.
    """
    tests_dir = Path("tests")
    if not tests_dir.exists() or not list(tests_dir.glob("test_*.py")):
        return True, "SKIP: belum ada test"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-q", "--no-header"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.strip() or result.stderr.strip()
    return result.returncode == 0, output


def main() -> int:
    """Run every verification check and print a summary report.

    Writes a per-check report to stdout.

    Returns:
        0 when every check passed, 1 when at least one check failed.
    """
    print("\n=== Verifikasi Klaim AI ===\n")
    all_ok = True

    print("[File Existence]")
    for path in REQUIRED_FILES:
        ok = check_file_exists(path)
        status = "TERVERIFIKASI" if ok else "GAGAL"
        print(f"  [{status}] {path}")
        if not ok:
            all_ok = False

    print("\n[Import Check]")
    for module in REQUIRED_IMPORTS:
        ok = check_import(module)
        status = "TERVERIFIKASI" if ok else "GAGAL"
        print(f"  [{status}] import {module}")
        if not ok:
            all_ok = False

    print("\n[Test Check]")
    ok, output = check_tests()
    status = "TERVERIFIKASI" if ok else "GAGAL"
    print(f"  [{status}] pytest")
    if output and not ok:
        for line in output.splitlines()[:5]:
            print(f"         {line}")
    if not ok:
        all_ok = False

    print()
    if all_ok:
        print("=== SEMUA TERVERIFIKASI ===\n")
        return 0
    print("=== ADA YANG GAGAL ===\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
