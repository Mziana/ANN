"""Unit tests for src.data.validate_data.

Each check is a pure function over a DataFrame, so every test builds its own
synthetic year. No test touches disk, the network, or the real dataset.
"""

from __future__ import annotations

import pandas as pd

from src.data.broker_time import wall_clock_series
from src.data.validate_data import (
    CheckResult,
    YearReport,
    check_bar_count,
    check_break_hour,
    check_duplicates,
    check_gaps,
    check_known_anomalies,
    check_monotonic,
    check_ohlc,
    check_spread,
    classify_gaps,
    discover_files,
    prepare_frame,
    render_markdown,
    validate_year,
)
from src.utils.config import load_config

START_EPOCH = 1_700_000_000

DATA_CONFIG = load_config("data")
ANOMALY_WINDOWS = DATA_CONFIG["validation"]["anomaly_windows"]


def make_frame(
    rows: list[tuple[int, float, float, float, float, float]] | None = None,
) -> pd.DataFrame:
    """Build a minimal one-year DataFrame.

    Args:
        rows: Optional tuples of (epoch, open, high, low, close, spread_pips).
            When omitted, 1300 consecutive minutes are generated.

    Returns:
        DataFrame with the columns every check expects.
    """
    if rows is None:
        rows = [(START_EPOCH + i * 60, 1.0, 1.1, 0.9, 1.0, 0.6) for i in range(1300)]
    return pd.DataFrame(
        rows, columns=["broker_time_raw", "open", "high", "low", "close", "spread_pips"]
    )


def frame_with_tail(tail_pips: float, rows: int = 200, wide: int = 5) -> pd.DataFrame:
    """Build a frame whose p99 sits on a wide tail.

    pandas interpolates the quantile, so a single outlier in a short frame never
    reaches p99. Five wide rows out of 200 puts the 99th percentile on the tail.

    Args:
        tail_pips: Spread value used by the final rows.
        rows: Total number of rows.
        wide: How many final rows carry the wide spread.

    Returns:
        Frame with a predictable p99 equal to ``tail_pips``.
    """
    pips = [0.6] * (rows - wide) + [tail_pips] * wide
    return make_frame([(START_EPOCH + i * 60, 1, 2, 0.5, 1, pips[i]) for i in range(rows)])


def make_sessions(count: int, bars: int = 600, gap_minutes: int = 61) -> pd.DataFrame:
    """Build ``count`` trading sessions separated by a single gap.

    Args:
        count: How many sessions to emit.
        bars: Bars inside each session.
        gap_minutes: Gap between one session and the next.

    Returns:
        Frame whose session count is exactly ``count``.
    """
    rows: list[tuple[int, float, float, float, float, float]] = []
    cursor = START_EPOCH
    for _ in range(count):
        for i in range(bars):
            rows.append((cursor + i * 60, 1.0, 2.0, 0.5, 1.0, 0.6))
        cursor += (bars - 1) * 60 + gap_minutes * 60
    return attach_broker_time(
        pd.DataFrame(
            rows,
            columns=["broker_time_raw", "open", "high", "low", "close", "spread_pips"],
        )
    )


def make_frame_with_tail(tail_pips: float, rows: int = 200, wide: int = 5) -> pd.DataFrame:
    """Build a frame whose p99 sits on a wide tail.

    Args:
        tail_pips: Spread value used by the final rows.
        rows: Total number of rows.
        wide: How many final rows carry the wide spread.

    Returns:
        Frame with a predictable p99 equal to ``tail_pips``.
    """
    pips = [0.6] * (rows - wide) + [tail_pips] * wide
    return make_frame([(START_EPOCH + i * 60, 1, 2, 0.5, 1, pips[i]) for i in range(rows)])


def attach_broker_time(frame: pd.DataFrame) -> pd.DataFrame:
    """Add the broker wall-clock column the time-based checks need."""
    frame = frame.copy()
    frame["broker_time"] = wall_clock_series(frame["broker_time_raw"])
    return frame


# The raw epoch digits are the broker's wall clock, so a fixture reading
# 2026-01-05 00:00 server time needs the epoch whose UTC rendering is that.
SESSION_START = int(pd.Timestamp("2026-01-05").tz_localize("UTC").timestamp())
SESSION_BARS_BEFORE_BREAK = 1000
SESSION_BREAK_MINUTES = 61
SESSION_TOTAL_BARS = 1440 - SESSION_BREAK_MINUTES


def make_trading_year(days: int = 4) -> pd.DataFrame:
    """Build data with the cadence the real broker feed actually shows.

    One trading session spans 24 hours of broker wall clock and carries
    exactly one break, so a full calendar day holds 1,379 bars. Sessions are
    aligned to broker midnight, which is how the real data behaves.

    Args:
        days: How many full trading sessions to emit.

    Returns:
        Frame with broker timestamps and the broker wall-clock column.
    """
    rows: list[tuple[int, float, float, float, float, float]] = []
    for day in range(days):
        base = SESSION_START + day * 86_400
        for i in range(SESSION_BARS_BEFORE_BREAK):
            rows.append((base + i * 60, 1.0, 1.1, 0.9, 1.0, 0.6))
        resume = base + (SESSION_BARS_BEFORE_BREAK + SESSION_BREAK_MINUTES) * 60
        for i in range(SESSION_TOTAL_BARS - SESSION_BARS_BEFORE_BREAK):
            rows.append((resume + i * 60, 1.0, 1.1, 0.9, 1.0, 0.6))
    return attach_broker_time(
        pd.DataFrame(
            rows,
            columns=["broker_time_raw", "open", "high", "low", "close", "spread_pips"],
        )
    )


def make_partial_day(offset_days: int = 30, bars: int = 120) -> pd.DataFrame:
    """Build a short weekend-style session of the kind seen in real data.

    Args:
        offset_days: How many days after the trading year to place it.
        bars: How many bars the short session holds.

    Returns:
        Frame with broker timestamps and the broker wall-clock column.
    """
    base = SESSION_START + offset_days * 86_400
    return attach_broker_time(
        pd.DataFrame(
            {
                "broker_time_raw": [base + i * 60 for i in range(bars)],
                "open": 1.0,
                "high": 1.1,
                "low": 0.9,
                "close": 1.0,
                "spread_pips": 0.6,
            }
        )
    )


class TestCheckBarCount:
    def test_realistic_year_passes(self):
        result = check_bar_count(make_trading_year())
        assert result.passed

    def test_partial_weekend_day_is_not_an_error(self):
        """The real feed has 200 days of 118-180 bars; those are legitimate."""
        combined = pd.concat([make_trading_year(days=2), make_partial_day()], ignore_index=True)
        result = check_bar_count(combined)
        assert result.passed
        assert "parsial" in result.detail

    def test_day_in_the_empty_band_fails(self):
        """Nothing lands between 180 and 1100 bars in healthy data."""
        damaged = attach_broker_time(
            pd.DataFrame(
                {
                    "broker_time_raw": [SESSION_START + 30 * 86_400 + i * 60 for i in range(600)],
                    "open": 1.0,
                    "high": 1.1,
                    "low": 0.9,
                    "close": 1.0,
                    "spread_pips": 0.6,
                }
            )
        )
        combined = pd.concat([make_trading_year(days=2), damaged], ignore_index=True)
        result = check_bar_count(combined)
        assert not result.passed
        assert "BAR HILANG" in result.detail

    def test_more_than_1440_bars_is_impossible(self):
        too_many = attach_broker_time(
            pd.DataFrame(
                {
                    "broker_time_raw": [SESSION_START + 30 * 86_400 + i * 30 for i in range(1500)],
                    "open": 1.0,
                    "high": 1.1,
                    "low": 0.9,
                    "close": 1.0,
                    "spread_pips": 0.6,
                }
            )
        )
        combined = pd.concat([make_trading_year(days=2), too_many], ignore_index=True)
        assert "tidak mungkin" in check_bar_count(combined).detail


class TestCheckDuplicates:
    def test_clean_frame_passes(self):
        assert check_duplicates(make_frame()).passed

    def test_duplicate_timestamp_fails(self):
        frame = make_frame()
        frame.loc[5, "broker_time_raw"] = frame.loc[4, "broker_time_raw"]
        result = check_duplicates(frame)
        assert not result.passed
        assert result.severity == "ERROR"
        assert "1 duplikat" in result.detail


class TestCheckMonotonic:
    def test_sorted_frame_passes(self):
        assert check_monotonic(make_frame()).passed

    def test_backwards_timestamp_fails(self):
        frame = make_frame()
        frame.loc[10, "broker_time_raw"] = frame.loc[9, "broker_time_raw"] - 60
        result = check_monotonic(frame)
        assert not result.passed
        assert "monoton" in result.detail


class TestCheckOhlc:
    def test_valid_ohlc_passes(self):
        assert check_ohlc(make_frame()).passed

    def test_high_below_low_fails(self):
        frame = make_frame()
        frame.loc[3, "high"] = 0.5
        result = check_ohlc(frame)
        assert not result.passed
        assert "OHLC" in result.detail

    def test_close_outside_range_fails(self):
        frame = make_frame()
        frame.loc[7, "close"] = 5.0
        assert not check_ohlc(frame).passed


class TestClassifyGaps:
    def test_daily_break_and_weekend_are_separated(self):
        frame = make_trading_year(days=4)
        daily, weekend, odd, _ = classify_gaps(frame)
        assert daily == 4
        assert odd == 0

    def test_weekend_gap_is_classified(self):
        frame = make_trading_year(days=3)
        cursor = SESSION_START + 5 * 86_400
        tail = attach_broker_time(
            pd.DataFrame(
                {
                    "broker_time_raw": [cursor + i * 60 for i in range(300)],
                    "open": 1.0,
                    "high": 1.1,
                    "low": 0.9,
                    "close": 1.0,
                    "spread_pips": 0.6,
                }
            )
        )
        combined = pd.concat([frame, tail], ignore_index=True).sort_values("broker_time_raw")
        _, weekend, odd, _ = classify_gaps(combined)
        assert weekend == 1
        assert odd == 0

    def test_returns_series_for_odd_gaps(self):
        frame = pd.DataFrame({"broker_time_raw": [START_EPOCH, START_EPOCH + 1800]})
        _, _, odd, series = classify_gaps(frame)
        assert odd == 1
        assert len(series) == 1


class TestCheckGaps:
    def test_clean_gaps_pass(self):
        result = check_gaps(make_trading_year(days=4))
        assert result.severity == "WARN"
        assert result.passed

    def test_routine_small_gaps_are_ignored(self):
        """9-13 minute gaps are normal around the break boundary."""
        frame = make_trading_year(days=2)
        noisy = frame.drop(index=range(100, 111)).reset_index(drop=True)
        result = check_gaps(noisy)
        assert result.passed

    def test_odd_gap_is_warned(self):
        frame = make_trading_year(days=2)
        broken = frame.drop(index=range(100, 132)).reset_index(drop=True)
        assert not check_gaps(broken).passed


class TestCheckSpread:
    def test_reports_distribution(self):
        result = check_spread(make_frame(), DATA_CONFIG, "2023")
        assert "median" in result.detail

    def test_uses_year_in_name(self):
        assert "2023" in check_spread(make_frame(), DATA_CONFIG, "2023").name

    def test_quiet_year_passes(self):
        frame = make_frame([(START_EPOCH + i * 60, 1, 2, 0.5, 1, 0.6) for i in range(100)])
        result = check_spread(frame, DATA_CONFIG, "2025")
        assert result.passed
        assert result.severity == "INFO"

    def test_wide_tail_warns(self):
        """p99 between warn and error multiplier must warn, not pass silently."""
        result = check_spread(frame_with_tail(9.0), DATA_CONFIG, "2023")
        assert result.severity == "WARN"
        assert not result.passed

    def test_worst_tail_is_an_error(self):
        result = check_spread(frame_with_tail(90.0), DATA_CONFIG, "2023")
        assert result.severity == "ERROR"
        assert not result.passed

    def test_detail_shows_the_thresholds_used(self):
        result = check_spread(make_frame(), DATA_CONFIG, "2023")
        assert "config 3.00 pip" in result.detail


class TestCheckBreakHour:
    def test_reports_dominant_hour(self):
        result = check_break_hour(make_trading_year(days=4))
        assert result.severity == "WARN"
        assert "jam dinding dominan" in result.detail

    def test_no_daily_break_is_info(self):
        frame = attach_broker_time(
            pd.DataFrame({"broker_time_raw": [START_EPOCH, START_EPOCH + 60]})
        )
        result = check_break_hour(frame)
        assert result.severity == "INFO"
        assert "tanpa break" in result.detail


class TestCheckKnownAnomalies:
    def test_frame_before_all_windows_passes(self):
        frame = attach_broker_time(make_frame())
        assert check_known_anomalies(frame, ANOMALY_WINDOWS).passed

    def test_frame_inside_window_warns(self):
        window = next(w for w in ANOMALY_WINDOWS if w["start"] == "2026-03-10")
        start = pd.Timestamp(window["start"], tz="UTC").timestamp()
        frame = attach_broker_time(
            make_frame([(int(start) + i * 60, 1, 2, 0.5, 1, 0.6) for i in range(100)])
        )
        result = check_known_anomalies(frame, ANOMALY_WINDOWS)
        assert not result.passed
        assert f"{window['start']}..{window['end']}" in result.detail
        assert "BELUM TERVERIFIKASI" in result.detail

    def test_every_window_carries_the_unverified_warning(self):
        """Each anomaly window must say its offset is unverified (Klenz 2026-10-05)."""
        for window in ANOMALY_WINDOWS:
            assert "BELUM TERVERIFIKASI" in window["note"], window["start"]

    def test_the_two_known_windows_are_registered(self):
        """Self-audit SA-02 found three windows, but Klenz re-verification
        (2026-10-05) showed the 2023-03-17..24 entry is SA-03 regime, not
        an anomaly. The Architect deleted it. Lock the remaining two so a
        silent re-addition of 2023 fails."""
        starts = {w["start"] for w in ANOMALY_WINDOWS}
        assert len(ANOMALY_WINDOWS) == 2
        assert starts == {"2024-10-28", "2026-03-10"}

    def test_windows_are_well_formed(self):
        for window in ANOMALY_WINDOWS:
            assert window["start"] < window["end"]
            assert window["note"]

    def test_empty_window_list_passes(self):
        frame = attach_broker_time(make_frame())
        assert check_known_anomalies(frame, []).passed


class TestValidateYearSessions:
    """trading_days must count sessions by gap, not by broker calendar date."""

    def _write(self, tmp_path, frame):
        path = tmp_path / "usdjpy_m1_2026.csv"
        frame.assign(time="2026-01-01T00:00:00+0000").to_csv(path, index=False)
        return path

    def test_counts_one_session_per_break(self, tmp_path):
        path = self._write(tmp_path, make_sessions(count=3))
        report = validate_year(path, DATA_CONFIG)
        assert report.trading_days == 3

    def test_weekend_gap_starts_a_session(self, tmp_path):
        path = self._write(tmp_path, make_sessions(count=2, gap_minutes=2900))
        report = validate_year(path, DATA_CONFIG)
        assert report.trading_days == 2

    def test_broken_session_counts_as_one_session(self, tmp_path):
        """A 10 minute hole must not start a new session."""
        path = self._write(tmp_path, make_sessions(count=2, gap_minutes=10))
        report = validate_year(path, DATA_CONFIG)
        assert report.trading_days == 1

    def test_session_spanning_many_dates_is_still_one_session(self, tmp_path):
        """2023 Jan-Mei had no daily break, so one session ran for days."""
        start = int(pd.Timestamp("2023-01-02 01:00", tz="UTC").timestamp())
        rows = [(start + i * 60, 1.0, 2.0, 0.5, 1.0, 0.6) for i in range(5 * 1440)]
        frame = attach_broker_time(
            pd.DataFrame(
                rows,
                columns=["broker_time_raw", "open", "high", "low", "close", "spread_pips"],
            )
        )
        path = self._write(tmp_path, frame)
        report = validate_year(path, DATA_CONFIG)
        distinct_dates = prepare_frame(path)["broker_time"].dt.date.nunique()
        assert report.trading_days == 1
        assert distinct_dates > report.trading_days

    def test_run_on_report_uses_configured_spread(self, tmp_path):
        path = self._write(tmp_path, make_frame_with_tail(90.0))
        report = validate_year(path, DATA_CONFIG)
        spread = next(c for c in report.checks if c.name.startswith("Spread"))
        assert spread.severity == "ERROR"

    def test_uses_configured_anomaly_windows(self, tmp_path):
        start = pd.Timestamp("2026-03-15", tz="UTC").timestamp()
        frame = attach_broker_time(
            make_frame([(int(start) + i * 60, 1, 2, 0.5, 1, 0.6) for i in range(100)])
        )
        path = self._write(tmp_path, frame)
        report = validate_year(path, DATA_CONFIG)
        anomaly = next(c for c in report.checks if c.name == "Anomali diketahui")
        assert not anomaly.passed


class TestPrepareFrame:
    def test_adds_broker_time_column(self, tmp_path):
        path = tmp_path / "usdjpy_m1_2026.csv"
        make_frame().assign(time="2026-01-01T00:00:00+0000").to_csv(path, index=False)
        frame = prepare_frame(path)
        assert "broker_time" in frame.columns

    def test_sorts_by_raw_timestamp(self, tmp_path):
        path = tmp_path / "usdjpy_m1_2026.csv"
        rows = [(START_EPOCH + 60, 1, 2, 0.5, 1, 0.6), (START_EPOCH, 1, 2, 0.5, 1, 0.6)]
        frame = pd.DataFrame(
            rows, columns=["broker_time_raw", "open", "high", "low", "close", "spread_pips"]
        )
        frame.assign(time="2026-01-01T00:00:00+0000").to_csv(path, index=False)
        assert prepare_frame(path)["broker_time_raw"].is_monotonic_increasing


class TestRenderMarkdown:
    def test_contains_verdict_and_table(self):
        report = YearReport(year="2026", bars=100, trading_days=5)
        report.checks = [CheckResult("Duplikat", "ERROR", True, "bersih")]
        text = render_markdown([report])
        assert "Verdict: LOLOS" in text
        assert "| 2026 |" in text

    def test_error_flips_verdict(self):
        report = YearReport(year="2026", bars=100, trading_days=5)
        report.checks = [CheckResult("Duplikat", "ERROR", False, "ada duplikat")]
        assert "Verdict: GAGAL" in render_markdown([report])

    def test_warning_does_not_flip_verdict(self):
        report = YearReport(year="2026", bars=100, trading_days=5)
        report.checks = [CheckResult("Gap", "WARN", False, "ada gap aneh")]
        assert "Verdict: LOLOS" in render_markdown([report])


class TestDiscoverFiles:
    def test_returns_only_existing(self, tmp_path):
        for year in (2023, 2024):
            (tmp_path / f"usdjpy_m1_{year}.csv").write_text(
                "broker_time_raw\n1\n", encoding="utf-8"
            )
        found = discover_files("USDJPY", "M1", "{symbol}_{tf}_{year}.{format}", tmp_path)
        assert [p.name for p in found] == ["usdjpy_m1_2023.csv", "usdjpy_m1_2024.csv"]

    def test_empty_dir_returns_empty(self, tmp_path):
        assert discover_files("USDJPY", "M1", "{symbol}_{tf}_{year}.{format}", tmp_path) == []


class TestYearReport:
    def test_ok_false_when_error_present(self):
        report = YearReport(year="2026", bars=1, trading_days=1)
        report.checks = [CheckResult("x", "ERROR", False, "bad")]
        assert not report.ok

    def test_ok_true_with_warning_only(self):
        report = YearReport(year="2026", bars=1, trading_days=1)
        report.checks = [CheckResult("x", "WARN", False, "meh")]
        assert report.ok
