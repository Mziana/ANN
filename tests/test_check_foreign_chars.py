"""Unit tests for scripts.check_foreign_chars.

The scanner exists to catch characters that slipped into source files, so
the tests include a deliberate positive control: a file that really does
contain a forbidden character must be reported.
"""

from __future__ import annotations

from pathlib import Path

from scripts.check_foreign_chars import (
    Finding,
    find_files,
    is_excluded,
    main,
    scan_file,
    scan_text,
)

CLEAN_TEXT = "# Judul\n# Isi dalam bahasa Indonesia dan English.\nvalue = 42\n"

# Forbidden characters are written as escape sequences on purpose: a literal
# one would make this test file fail the very check it is testing.
HAN = "\u9a8c"  # U+9A8C, Han
CYRILLIC = "\u0435"  # U+0435, Cyrillic

DIRTY_TEXT = f"# Judul\n# ini punya karakter asing: {HAN}\nvalue = 42\n"


class TestScanText:
    def test_clean_text_has_no_findings(self):
        assert scan_text(CLEAN_TEXT) == []

    def test_detects_han_character(self):
        hits = scan_text(DIRTY_TEXT)
        assert len(hits) == 1
        line, block, char = hits[0]
        assert line == 2
        assert block == "Han"
        assert char == HAN

    def test_reports_correct_line_number(self):
        text = f"a\nb\nc\nd\n{CYRILLIC}"
        hits = scan_text(text)
        assert hits[0][0] == 5
        assert hits[0][1] == "Cyrillic"

    def test_ignores_ordinary_punctuation(self):
        assert scan_text("-> ,.:;()[]{}#/*-+=%$@!") == []

    def test_ignores_emoji_and_symbols(self):
        """Emoji live outside the blocked ranges and must not be flagged."""
        assert scan_text("status: OK | arrow -> | 100%") == []


class TestIsExcluded:
    def test_checkpoints_is_excluded(self):
        assert is_excluded(Path("checkpoints/checkpoint_01.ps1"))

    def test_archive_is_excluded(self):
        assert is_excluded(Path("archive/old_notes.md"))

    def test_normal_path_is_not_excluded(self):
        assert not is_excluded(Path("src/data/fetch_data.py"))


class TestFindFiles:
    def test_filters_by_suffix(self, tmp_path):
        target = tmp_path / "notes.txt"
        target.write_text("hi", encoding="utf-8")
        (tmp_path / "image.png").write_bytes(b"\x89PNG")
        found = find_files([str(target), str(tmp_path / "image.png")])
        assert found == [target]

    def test_skips_missing_files(self, tmp_path):
        assert find_files([str(tmp_path / "nope.py")]) == []


class TestScanFile:
    def test_returns_findings_for_dirty_file(self, tmp_path):
        target = tmp_path / "dirty.py"
        target.write_text(DIRTY_TEXT, encoding="utf-8")
        findings = scan_file(target)
        assert len(findings) == 1
        assert isinstance(findings[0], Finding)
        assert findings[0].block == "Han"

    def test_returns_empty_for_clean_file(self, tmp_path):
        target = tmp_path / "clean.py"
        target.write_text(CLEAN_TEXT, encoding="utf-8")
        assert scan_file(target) == []

    def test_ignores_binary_content(self, tmp_path):
        target = tmp_path / "blob.md"
        target.write_bytes(b"\xff\xfe\x00\x01binary")
        assert scan_file(target) == []


class TestMain:
    def test_exit_zero_when_clean(self, tmp_path, capsys):
        target = tmp_path / "clean.md"
        target.write_text(CLEAN_TEXT, encoding="utf-8")
        assert main([str(target)]) == 0
        assert "tidak ada karakter asing" in capsys.readouterr().out

    def test_exit_one_when_dirty(self, tmp_path, capsys):
        target = tmp_path / "dirty.md"
        target.write_text(DIRTY_TEXT, encoding="utf-8")
        assert main([str(target)]) == 1
        assert "GAGAL" in capsys.readouterr().out

    def test_exit_zero_when_no_files(self, capsys):
        assert main([""]) == 0
        assert "tidak ada file untuk discan" in capsys.readouterr().out
