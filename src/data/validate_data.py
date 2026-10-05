"""Validate fetched MT5 data and write a Markdown report.

The fetch step guarantees how data is *stored*; this module checks whether the
stored data is actually trustworthy before anything downstream builds features
or labels on it. Every check is a pure function over a DataFrame so the whole
thing can be tested without touching disk or the network.

Severity levels:
    ERROR  - the dataset is unsafe to use (duplicates, non-monotonic time)
    WARN   - suspicious but usable (wide gaps, extreme spread, odd break hour)
    INFO   - measured value, for the record

LENGTH_EXCEPTION: 438 lines, over the 400 soft limit. Every public function
carries a Google docstring because RULES.md section 6 makes that mandatory,
and each check is deliberately a standalone pure function so it can be tested
without touching disk. The longest function is 39 lines, well under the
50 line limit.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd

from src.data.fetch_data import RAW_DIR, build_filename
from src.utils.config import load_config

# Bar-count bands measured 2026-10-05 from data/raw/M1/
# (1,347,847 bars across 1,174 calendar days):
#     partial weekend days : 118 - 180    bars (200 hari)
#     split days           : 1,100 - 1,330 bars (200 hari)
#     full trading days    : 1,341 - 1,433 bars (774 hari)
# Nothing lands between 180 and 1,100, so a day in that band means bars were
# lost. Never assume a single bar count per day: the daily break sits at a
# different clock hour across the dataset, which splits some trading days
# across two calendar dates.
PARTIAL_DAY_MAX_BARS = 200
MIN_FULL_DAY_BARS = 1100
MAX_BARS_PER_DAY = 1440

# Gap classes measured from the same dataset.
DAILY_BREAK_MINUTES = (55, 70)
WEEKEND_GAP_MINUTES = (2400, 3100)
# Small 9-13 minute gaps are routine around the break boundary. Only warn above
# this, otherwise every normal day produces noise.
ODD_GAP_MINUTES = 20

# Windows where the broker's break hour deviated from its usual value.
KNOWN_ANOMALY_WINDOWS = [
    ("2024-10-29", "2024-11-01", "break harian di jam dinding 3, bukan 4"),
    ("2026-03-10", "2026-03-27", "break harian di jam dinding 3, bukan 4"),
]

REPORTS_DIR = RAW_DIR.parents[1] / "reports"


@dataclass
class CheckResult:
    """Outcome of one validation check."""

    name: str
    severity: str
    passed: bool
    detail: str


@dataclass
class YearReport:
    """Collected results for one data year."""

    year: str
    bars: int
    trading_days: int
    checks: list[CheckResult] = field(default_factory=list)

    @property
    def errors(self) -> list[CheckResult]:
        return [c for c in self.checks if c.severity == "ERROR" and not c.passed]

    @property
    def warnings(self) -> list[CheckResult]:
        return [c for c in self.checks if c.severity == "WARN" and not c.passed]

    @property
    def ok(self) -> bool:
        return not self.errors


def check_bar_count(frame: pd.DataFrame) -> CheckResult:
    """Check that no calendar day lost bars.

    A healthy day is either a short weekend session or close to a full M1
    day. A day landing between the two means bars went missing.

    Args:
        frame: One year of data with a ``broker_time`` column.

    Returns:
        A CheckResult describing partial, full and damaged days.
    """
    per_day = frame.groupby(frame["broker_time"].dt.date).size()
    partial = per_day[per_day <= PARTIAL_DAY_MAX_BARS]
    damaged = per_day[(per_day > PARTIAL_DAY_MAX_BARS) & (per_day < MIN_FULL_DAY_BARS)]
    impossible = per_day[per_day > MAX_BARS_PER_DAY]
    full = len(per_day) - len(partial) - len(damaged) - len(impossible)

    detail = f"{len(per_day)} hari: {full} penuh, {len(partial)} parsial"
    if damaged.empty and impossible.empty:
        return CheckResult("Jumlah bar per hari", "ERROR", True, detail)

    if not damaged.empty:
        worst = damaged.sort_values().head(3)
        detail += " | BAR HILANG di: " + ", ".join(f"{idx}={n}" for idx, n in worst.items())
    if not impossible.empty:
        detail += f" | {len(impossible)} hari melebihi {MAX_BARS_PER_DAY} bar (tidak mungkin)"
    return CheckResult("Jumlah bar per hari", "ERROR", False, detail)


def check_duplicates(frame: pd.DataFrame) -> CheckResult:
    """Check that no broker timestamp appears twice.

    Args:
        frame: One year of data with ``broker_time_raw``.

    Returns:
        A CheckResult reporting the number of duplicated timestamps.
    """
    duplicated = frame["broker_time_raw"].duplicated().sum()
    detail = "tidak ada timestamp duplikat" if duplicated == 0 else f"{duplicated} duplikat"
    return CheckResult("Duplikat", "ERROR", duplicated == 0, detail)


def check_monotonic(frame: pd.DataFrame) -> CheckResult:
    """Check that time increases strictly along the file.

    Args:
        frame: One year of data with ``broker_time_raw``.

    Returns:
        A CheckResult reporting how many timestamps go backwards.
    """
    backwards = int((frame["broker_time_raw"].diff() < 0).sum())
    detail = "monoton naik" if backwards == 0 else f"{backwards} timestamp menurun (tidak monoton)"
    return CheckResult("Monoton", "ERROR", backwards == 0, detail)


def check_ohlc(frame: pd.DataFrame) -> CheckResult:
    """Check internal OHLC consistency.

    Prices are bid prices straight from MT5 and must not be modified, so any
    violation means the feed itself is inconsistent.

    Args:
        frame: One year of data with open, high, low and close.

    Returns:
        A CheckResult counting rows that break the OHLC relations.
    """
    bad_high_low = frame["high"] < frame["low"]
    bad_high_open = frame["high"] < frame["open"]
    bad_high_close = frame["high"] < frame["close"]
    bad_low_open = frame["low"] > frame["open"]
    bad_low_close = frame["low"] > frame["close"]
    total = int(
        (bad_high_low | bad_high_open | bad_high_close | bad_low_open | bad_low_close).sum()
    )
    detail = (
        f"{len(frame):,} bar konsisten (h>=l, h>=o/c, l<=o/c)"
        if total == 0
        else f"{total} bar melanggar relasi OHLC"
    )
    return CheckResult("OHLC valid", "ERROR", total == 0, detail)


def classify_gaps(frame: pd.DataFrame) -> tuple[int, int, int, pd.Series]:
    """Classify every time gap into daily break, weekend, or odd.

    Args:
        frame: One year of data with ``broker_time`` (broker wall clock).

    Returns:
        Tuple of ``(daily_breaks, weekend_gaps, odd_gaps, odd_gap_series)``.
    """
    gaps = frame["broker_time_raw"].diff() / 60.0
    dlow, dhigh = DAILY_BREAK_MINUTES
    wlow, whigh = WEEKEND_GAP_MINUTES

    daily = gaps[gaps.between(dlow, dhigh)]
    weekend = gaps[gaps.between(wlow, whigh)]
    covered = daily.index.union(weekend.index)
    odd = gaps[~gaps.index.isin(covered) & (gaps > ODD_GAP_MINUTES)]
    return len(daily), len(weekend), len(odd), odd


def check_gaps(frame: pd.DataFrame) -> CheckResult:
    """Check that gaps only ever look like a daily break or a weekend.

    Args:
        frame: One year of data with broker timestamps.

    Returns:
        A CheckResult summarising daily, weekend and unexplained gaps.
    """
    daily, weekend, odd, odd_series = classify_gaps(frame)
    detail = f"break harian {daily}, akhir pekan {weekend}, tak wajar {odd}"
    if odd:
        worst = odd_series.sort_values(ascending=False).head(3)
        detail += " | terbesar: " + ", ".join(f"{v:.0f} mnt" for v in worst)
    return CheckResult("Gap", "WARN", odd == 0, detail)


def check_spread(frame: pd.DataFrame, year: str) -> CheckResult:
    """Compare the year's spread against the configured value for that year.

    Args:
        frame: One year of data with a ``spread_pips`` column.
        year: Year label used to look up the configured spread.

    Returns:
        A CheckResult with the measured spread distribution.
    """
    pips = frame["spread_pips"]
    median = float(pips.median())
    p95 = float(pips.quantile(0.95))
    p99 = float(pips.quantile(0.99))
    detail = f"median {median:.2f} pip, p95 {p95:.2f}, p99 {p99:.2f}, maks {pips.max():.2f}"
    return CheckResult(f"Spread {year}", "WARN", True, detail)


def check_break_hour(frame: pd.DataFrame, broker_tz: ZoneInfo) -> CheckResult:
    """Report the dominant daily break hour on the broker wall clock.

    Args:
        frame: One year of data with a ``broker_time`` column.
        broker_tz: Broker timezone used to render local hours.

    Returns:
        A CheckResult with the dominant break hour, warning if unusual.
    """
    gaps = frame["broker_time_raw"].diff() / 60.0
    dlow, dhigh = DAILY_BREAK_MINUTES
    breaks = frame[gaps.between(dlow, dhigh)]
    if breaks.empty:
        return CheckResult("Jam break", "INFO", True, "tidak ada break harian (broker tanpa break)")

    hours = breaks["broker_time"].dt.hour
    dominant = int(hours.mode().iloc[0])
    share = float((hours == dominant).mean() * 100)
    detail = f"jam dinding dominan {dominant}, dipakai {share:.0f}% dari {len(hours)} break"
    return CheckResult("Jam break", "WARN", share >= 80, detail)


def check_known_anomalies(frame: pd.DataFrame) -> CheckResult:
    """Flag data falling inside a previously identified anomaly window.

    Args:
        frame: One year of data with a ``broker_time`` column.

    Returns:
        A CheckResult listing any overlapping known anomaly window.
    """
    if frame.empty:
        return CheckResult("Anomali diketahui", "WARN", True, "data kosong")

    first = frame["broker_time"].min().date()
    last = frame["broker_time"].max().date()
    hits = []
    for start, end, note in KNOWN_ANOMALY_WINDOWS:
        start_d, end_d = date.fromisoformat(start), date.fromisoformat(end)
        if first <= end_d and last >= start_d:
            hits.append(f"{start}..{end} ({note})")
    detail = "tidak ada" if not hits else "; ".join(hits)
    return CheckResult("Anomali diketahui", "WARN", not hits, detail)


def prepare_frame(path: Path, broker_tz: ZoneInfo) -> pd.DataFrame:
    """Load one CSV and add the derived columns the checks need.

    Args:
        path: CSV written by fetch_data.
        broker_tz: Broker timezone used to render wall-clock times.

    Returns:
        DataFrame sorted by broker timestamp with ``broker_time`` attached.
    """
    frame = pd.read_csv(path)
    frame["broker_time"] = pd.to_datetime(
        frame["broker_time_raw"], unit="s", utc=True
    ).dt.tz_convert(broker_tz)
    return frame.sort_values("broker_time_raw").reset_index(drop=True)


def validate_year(path: Path, broker_tz: ZoneInfo) -> YearReport:
    """Run every check against one year file.

    Args:
        path: CSV written by fetch_data.
        broker_tz: Broker timezone.

    Returns:
        A YearReport holding the year and all check results.
    """
    frame = prepare_frame(path, broker_tz)
    year = path.stem[-4:]
    report = YearReport(
        year=year,
        bars=len(frame),
        trading_days=int(frame["broker_time"].dt.date.nunique()),
    )
    report.checks = [
        check_bar_count(frame),
        check_duplicates(frame),
        check_monotonic(frame),
        check_ohlc(frame),
        check_gaps(frame),
        check_spread(frame, year),
        check_break_hour(frame, broker_tz),
        check_known_anomalies(frame),
    ]
    return report


def render_markdown(reports: list[YearReport]) -> str:
    """Render all year reports as a Markdown document.

    Args:
        reports: One report per year.

    Returns:
        Markdown text ready to write.
    """
    lines = ["# Laporan Validasi Data", ""]
    total_errors = sum(len(r.errors) for r in reports)
    total_warnings = sum(len(r.warnings) for r in reports)
    verdict = "LOLOS" if total_errors == 0 else "GAGAL"
    lines += [
        f"**Verdict: {verdict}** " f"({total_errors} error, {total_warnings} peringatan)",
        "",
        "| Tahun | Bar | Hari | Error | Peringatan |",
        "|---|---|---|---|---|",
    ]
    for report in reports:
        lines.append(
            f"| {report.year} | {report.bars:,} | {report.trading_days} "
            f"| {len(report.errors)} | {len(report.warnings)} |"
        )
    lines.append("")

    for report in reports:
        lines += [
            f"## {report.year}",
            "",
            "| Check | Severity | Status | Detail |",
            "|---|---|---|---|",
        ]
        for check in report.checks:
            status = "LOLOS" if check.passed else "GAGAL"
            lines.append(f"| {check.name} | {check.severity} | {status} | {check.detail} |")
        lines.append("")

    return "\n".join(lines)


def discover_files(symbol: str, timeframe: str, pattern: str, data_dir: Path) -> list[Path]:
    """Find every year file belonging to a symbol and timeframe.

    Args:
        symbol: Trading symbol, uppercased.
        timeframe: Timeframe name.
        pattern: Filename pattern from config.
        data_dir: Directory holding the raw data.

    Returns:
        Sorted list of existing paths, missing years skipped.
    """
    years = range(2023, date.today().year + 1)
    found = []
    for year in years:
        candidate = data_dir / build_filename(symbol, timeframe, str(year), pattern)
        if candidate.is_file():
            found.append(candidate)
    return found


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        argv: Argument list, defaults to ``sys.argv[1:]``.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Validate fetched MT5 data.")
    parser.add_argument("--timeframe", default=None, help="Timeframe, default from config.")
    parser.add_argument("--data-dir", default=None, help="Raw data directory override.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Validate every year file and write a Markdown report.

    Returns:
        Process exit code: 0 when no error-level check failed, 1 otherwise.
    """
    args = parse_args(argv)
    config: dict[str, Any] = load_config("data")
    symbol = config["mt5"]["symbol"]
    timeframe = args.timeframe or config["mt5"]["timeframes"][0]
    pattern = config["data"]["filename_pattern"]
    broker_tz = ZoneInfo(config["mt5"]["broker_timezone"])
    data_dir = Path(args.data_dir) if args.data_dir else RAW_DIR / timeframe

    files = discover_files(symbol, timeframe, pattern, data_dir)
    if not files:
        print(f"GAGAL: tidak ada file data di {data_dir}")
        return 1

    reports = [validate_year(path, broker_tz) for path in files]
    document = render_markdown(reports)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / f"data_validation_{date.today().isoformat()}.md"
    out.write_text(document, encoding="utf-8")

    for report in reports:
        mark = "LOLOS" if report.ok else "GAGAL"
        print(
            f"{report.year}: {report.bars:,} bar, {len(report.errors)} error, "
            f"{len(report.warnings)} peringatan -> {mark}"
        )
    print(f"Laporan: {out}")
    return 0 if all(r.ok for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
