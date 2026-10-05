"""Check whether STATE.md was updated today."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path


def main() -> int:
    """Verify that .ai/STATE.md mentions today's date.

    Used as a pre-commit gate so state files are never left stale.

    Returns:
        0 if STATE.md exists and contains today's date, 1 otherwise.
    """
    state = Path(".ai/STATE.md")
    if not state.exists():
        print("GAGAL: .ai/STATE.md tidak ada")
        return 1

    content = state.read_text(encoding="utf-8")
    today = date.today().isoformat()

    if today not in content:
        print(f"GAGAL: .ai/STATE.md belum diupdate hari ini ({today})")
        print("       Update STATE.md dulu sebelum commit.")
        return 1

    print(f"OK: .ai/STATE.md sudah diupdate hari ini ({today})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
