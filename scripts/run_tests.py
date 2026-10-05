"""Run the pytest suite for the pre-commit gate.

pytest returns exit code 5 when it collects no tests at all. That is not a
failure, it means the suite is empty, so this wrapper reports it as success.
Every other non-zero exit code is passed through unchanged, so real test
failures still block the commit.

Cross-platform on purpose: no shell syntax, so the same entry works from
PowerShell, cmd, and Git Bash.
"""

from __future__ import annotations

import subprocess
import sys

PYTEST_NO_TESTS_COLLECTED = 5
TESTS_DIR = "tests"


def run_tests(tests_dir: str = TESTS_DIR) -> int:
    """Run pytest and normalise the "no tests collected" exit code.

    Args:
        tests_dir: Directory passed to pytest.

    Returns:
        0 when pytest passed or collected nothing, otherwise pytest's own
        exit code.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", tests_dir, "-q", "--no-header"],
        capture_output=True,
        text=True,
    )

    output = (result.stdout or "") + (result.stderr or "")
    output = output.strip()

    if result.returncode == PYTEST_NO_TESTS_COLLECTED:
        print(f"OK: tidak ada test di {tests_dir}/ (pytest exit {PYTEST_NO_TESTS_COLLECTED})")
        print("     Lolos, tapi ini bukan verifikasi apa pun.")
        return 0

    if output:
        print(output)

    if result.returncode == 0:
        print("OK: semua test lulus.")

    return result.returncode


def main() -> int:
    """Run the test suite and forward the result to the shell.

    Returns:
        Process exit code: 0 when acceptable, non-zero otherwise.
    """
    return run_tests()


if __name__ == "__main__":
    sys.exit(main())
