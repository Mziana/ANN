"""Cek apakah STATE.md diupdate hari ini."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path


def main() -> int:
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
