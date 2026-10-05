"""Verifikasi klaim AI secara otomatis."""
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
    return Path(path).exists()


def check_import(module: str) -> bool:
    result = subprocess.run(
        [sys.executable, "-c", f"import {module}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def check_tests() -> tuple[bool, str]:
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
