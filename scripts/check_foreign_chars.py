"""Reject non-Latin characters sneaking into the repository.

This project is written in Indonesian and English. Neither uses CJK,
Cyrillic, Arabic, Hebrew or Hangul scripts. Those characters have appeared in
committed files by accident, so this check blocks them at the commit gate.

Usage:
    python scripts/check_foreign_chars.py [files...]

With no arguments it scans every file tracked by git.

Prints to stdout on purpose: this report is the product, the same reasoning
as verify_claims.py.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

# Directories whose content is archival and not subject to this check.
EXCLUDED_DIRS = ("checkpoints", "archive", ".ai/backup")

# Script blocks that have no legitimate use in this project.
SCRIPT_RANGES: dict[str, tuple[str, str]] = {
    "CJK punctuation": ("\u3000", "\u303f"),
    "Hiragana": ("\u3040", "\u309f"),
    "Katakana": ("\u30a0", "\u30ff"),
    "Han extension A": ("\u3400", "\u4dbf"),
    "Han": ("\u4e00", "\u9fff"),
    "Hangul": ("\uac00", "\ud7af"),
    "Cyrillic": ("\u0400", "\u04ff"),
    "Arabic": ("\u0600", "\u06ff"),
    "Hebrew": ("\u0590", "\u05ff"),
    "Fullwidth forms": ("\uff00", "\uffef"),
}

SCANNED_SUFFIXES = {".py", ".yaml", ".yml", ".md", ".ps1", ".toml", ".csv", ".txt"}


class Finding(NamedTuple):
    """One offending character located in one file."""

    path: str
    line: int
    block: str
    char: str


def is_excluded(path: Path) -> bool:
    """Report whether a path is exempt from the scan.

    Args:
        path: Path relative to the project root.

    Returns:
        True when the path lives under an excluded directory.
    """
    posix = path.as_posix()
    return any(posix.startswith(prefix) or f"/{prefix}" in posix for prefix in EXCLUDED_DIRS)


def list_tracked_files() -> list[Path]:
    """Return every file tracked by git.

    Returns:
        Paths relative to the project root. Empty when git is unavailable.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError):
        return []
    return [Path(p) for p in result.stdout.split("\0") if p]


def find_files(paths: list[str] | None) -> list[Path]:
    """Resolve the set of files to scan.

    Args:
        paths: Explicit paths from the command line. When empty, every file
            tracked by git is used.

    Returns:
        Unique, sorted paths that are worth scanning.
    """
    candidates = [Path(p) for p in paths] if paths else list_tracked_files()
    selected = {
        p
        for p in candidates
        if p.suffix.lower() in SCANNED_SUFFIXES and not is_excluded(p) and p.is_file()
    }
    return sorted(selected)


def scan_text(text: str) -> list[tuple[int, str, str]]:
    """Find non-Latin characters in a string.

    Args:
        text: Content to inspect.

    Returns:
        List of ``(line_number, block_name, character)`` tuples, one per
        offending character.
    """
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for char in line:
            for block, (low, high) in SCRIPT_RANGES.items():
                if low <= char <= high:
                    hits.append((lineno, block, char))
                    break
    return hits


def scan_file(path: Path) -> list[Finding]:
    """Scan one file for non-Latin characters.

    Args:
        path: File to read.

    Returns:
        One Finding per offending character. Unreadable or non-UTF-8 files
        yield no findings.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    return [Finding(path.as_posix(), line, block, char) for line, block, char in scan_text(text)]


def report(findings: list[Finding]) -> None:
    """Print findings grouped by file.

    Args:
        findings: Offending characters to display.
    """
    by_file: dict[str, list[Finding]] = {}
    for finding in findings:
        by_file.setdefault(finding.path, []).append(finding)

    for path in sorted(by_file):
        print(f"  {path}")
        for item in by_file[path]:
            print(f"    baris {item.line:5d}  [{item.block}] U+{ord(item.char):04X}")


def main(argv: list[str] | None = None) -> int:
    """Scan files and exit non-zero when anything is found.

    Args:
        argv: File list from the command line, defaults to ``sys.argv[1:]``.

    Returns:
        0 when clean, 1 when a forbidden character was found.
    """
    args = sys.argv[1:] if argv is None else argv
    files = find_files(args)

    if not files:
        print("OK: tidak ada file untuk discan.")
        return 0

    findings: list[Finding] = []
    for path in files:
        findings.extend(scan_file(path))

    if findings:
        print(f"GAGAL: {len(findings)} karakter asing di {len(files)} file discan.\n")
        report(findings)
        print("\nProyek ini memakai bahasa Indonesia dan Inggris.")
        return 1

    print(f"OK: {len(files)} file discan, tidak ada karakter asing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
