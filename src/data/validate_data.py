"""Validate fetched MT5 data and write a Markdown report.

The fetch step guarantees how data is *stored*; this module checks whether the
stored data is actually trustworthy before anything downstream builds features
or labels on it. Every check is a pure function over a DataFrame so the whole
thing can be tested without touching disk or the network.

Severity levels:
    ERROR  - the dataset is unsafe to use (duplicates, non-monotonic time)
    WARN   - suspicious but usable (wide gaps, extreme spread, odd break hour)
    INFO   - measured value, for the record
"""

# EXCEPTION: this file is over the 400 line soft limit. Re-audited 2026-10-05 and
# kept whole, with the owner's agreement, because splitting checks from rendering
# would move CheckResult and YearReport into a second module and create a circular
# import between the checks and the renderer. Growth since commit 74f155d is
# 444 -> 543 lines (+99): 22 code, 32 comments, 31 docstrings, 14 blank. Code is
# the smallest content bucket, and every public function still stays well under
# the 50 line limit, so the split is not needed yet. Measured 2026-10-05.
#
# HARD LIMITS, decided by the owner on 2026-10-05. This exception is only valid
# while all three hold; if any one breaks, split the file into checks vs render:
#   1. The file passes 600 lines (currently 543, so 57 lines of headroom).
#   2. A new public function is added to this module.
#   3. The end of Milestone 1 (Phase B data pipeline) is reached.
# This also honours the standing pipeline rule in STATE.md, which asks for the
# check-vs-render split; that split is deferred to end of Milestone 1.

from __future__ import annotations

import argparse
import logging
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.broker_time import wall_clock_series
from src.data.fetch_data import RAW_DIR, build_filename
from src.utils.config import load_config

logger = logging.getLogger(__name__)

# Bar-count bands measured 2026-10-05 from data/raw/M1/ (1,347,847 bars across
# 1,174 broker calendar dates), grouped by broker wall-clock date:
#     Saturday (weekend tail) : 118 - 180 bars      (200 days)
#     Monday  (week reopen)   : 1,167 - 1,260 bars  (194 days)
#     Tuesday .. Friday       : 1,341 - 1,433 bars  (774 days)
# Nothing lands between 180 and 1,167. A day inside that band means bars were
# lost.
#
# The broker trading day is 04:00 -> 03:00 broker time, so Monday is a 20 hour
# session (1,200 bars) because the week reopens at 04:00, while Tuesday through
# Friday carry 23 hours (1,380 bars) after the 03:00-04:00 break. That is why
# MIN_FULL_DAY_BARS stays at 1,100: raising it to the 1,300 the auditor
# suggested would flag all 194 legitimate Monday sessions as lost bars.
PARTIAL_DAY_MAX_BARS = 200
MIN_FULL_DAY_BARS = 1100
MAX_BARS_PER_DAY = 1440

# A session starts after any gap at least this long. The daily break is about
# 61 minutes and the weekend gap about 49 hours, so 55 minutes separates a real
# session boundary from the routine 8-9 minute holes around the break.
SESSION_BOUNDARY_MINUTES = 55

# Gap classes measured from the same dataset.
DAILY_BREAK_MINUTES = (55, 70)
WEEKEND_GAP_MINUTES = (2400, 3100)
# Small 9-13 minute gaps are routine around the break boundary. Only warn above
# this, otherwise every normal day produces noise.
ODD_GAP_MINUTES = 20

# Windows where the broker's break hour deviated from its usual value now live
# in configs/data.yaml under validation.anomaly_windows, so they can be
# corrected without touching this file (RULES.md §10).

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

    This groups by broker calendar date on purpose, unlike ``trading_days`` which
    counts sessions by gap. The two answer different questions, and only the
    calendar grouping detects a short session:

    - A broker date caps at 1,440 bars, so every band in this check is a fixed,
      verifiable limit. A session has no such cap: Jan-May 2023 had no daily
      break, so one session ran 7,160 bars across five days. Grouping sessions
      would push 24 of those past ``MAX_BARS_PER_DAY`` and report the healthy
      2023 dataset as an ERROR.
    - The roughly 180 bar Saturday tail is the end of Friday's session, because
      that session crosses broker midnight. Under session grouping the partial
      signal disappears entirely (0 partial sessions across all four years),
      losing the weekend detection this check relies on.

    Switching to session grouping is therefore rejected; see the owner's Q2
    decision of 2026-10-05.

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


def check_spread(frame: pd.DataFrame, config: dict[str, Any], year: str) -> CheckResult:
    """Check the year's spread tail against the configured spread for that year.

    The configuration has to be enforceable, otherwise setting a spread for a
    year is only a note in a file. The 99th percentile is compared against
    ``spread.by_year[year]`` scaled by the configured multipliers: above the
    warn multiplier it is a warning, above the error multiplier it is an error.

    Args:
        frame: One year of data with a ``spread_pips`` column.
        config: Parsed contents of configs/data.yaml.
        year: Year label used to look up the configured spread.

    Returns:
        A CheckResult carrying the measured distribution and the verdict.
    """
    spread_config = config["spread"]
    # YAML parses an unquoted `2023:` as an int key, so normalise to str before
    # looking up. Without this every year silently falls back to `default` and
    # the per-year spread never gets enforced.
    by_year = {str(key): float(value) for key, value in spread_config["by_year"].items()}
    configured = by_year.get(str(year), float(spread_config["default"]))
    warn_at = configured * float(spread_config["warn_multiplier"])
    error_at = configured * float(spread_config["error_multiplier"])

    pips = frame["spread_pips"]
    median = float(pips.median())
    p95 = float(pips.quantile(0.95))
    p99 = float(pips.quantile(0.99))

    if p99 > error_at:
        severity, passed = "ERROR", False
    elif p99 > warn_at:
        severity, passed = "WARN", False
    else:
        severity, passed = "INFO", True

    detail = (
        f"median {median:.2f} pip, p95 {p95:.2f}, p99 {p99:.2f}, maks {pips.max():.2f} "
        f"| config {configured:.2f} pip (warn > {warn_at:.2f}, error > {error_at:.2f})"
    )
    return CheckResult(f"Spread {year}", severity, passed, detail)


def check_break_hour(frame: pd.DataFrame) -> CheckResult:
    """Report the dominant hour trading resumes after the daily break.

    The hour reported is the wall-clock hour of the first bar *after* the gap,
    so the dominant value is 1 while the empty hour is 0: the broker stops
    quoting at 00:00 server time and reopens at 01:00, which matches the
    "Senin 01:00 sampai Jumat 00:00" session Finex publishes.

    The 80 percent share is a measurement threshold rather than a configured
    expectation, so this check reports drift instead of enforcing a fixed hour.
    An ``expected_break_hour`` in config would be the way to turn it into a
    hard assertion.

    Args:
        frame: One year of data with a ``broker_time`` column.

    Returns:
        A CheckResult with the dominant reopen hour and the share of breaks
        that used it.
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


def check_known_anomalies(
    frame: pd.DataFrame, anomaly_windows: list[dict[str, str]]
) -> CheckResult:
    """Flag data falling inside a previously identified anomaly window.

    Args:
        frame: One year of data with a ``broker_time`` column.
        anomaly_windows: Windows from ``validation.anomaly_windows`` in
            configs/data.yaml, each with ``start``, ``end`` and optional
            ``note`` keys.

    Returns:
        A CheckResult listing any overlapping known anomaly window.
    """
    if frame.empty:
        return CheckResult("Anomali diketahui", "WARN", True, "data kosong")

    first = frame["broker_time"].min().date()
    last = frame["broker_time"].max().date()
    hits = []
    for window in anomaly_windows:
        start_d = date.fromisoformat(str(window["start"]))
        end_d = date.fromisoformat(str(window["end"]))
        if first <= end_d and last >= start_d:
            note = window.get("note", "")
            hits.append(f"{start_d}..{end_d} ({note})" if note else f"{start_d}..{end_d}")
    detail = "tidak ada" if not hits else "; ".join(hits)
    return CheckResult("Anomali diketahui", "WARN", not hits, detail)


def prepare_frame(path: Path) -> pd.DataFrame:
    """Load one CSV and add the derived columns the checks need.

    Args:
        path: CSV written by fetch_data.

    Returns:
        DataFrame sorted by broker timestamp with ``broker_time`` attached.
    """
    frame = pd.read_csv(path)
    frame["broker_time"] = wall_clock_series(frame["broker_time_raw"])
    return frame.sort_values("broker_time_raw").reset_index(drop=True)


def validate_year(path: Path, config: dict[str, Any]) -> YearReport:
    """Run every check against one year file.

    Args:
        path: CSV written by fetch_data.
        broker_tz: Broker timezone.
        config: Parsed contents of configs/data.yaml.

    Returns:
        A YearReport holding the year and all check results.
    """
    frame = prepare_frame(path)
    year = path.stem[-4:]

    # A trading session starts after any gap long enough to be the daily break
    # or the weekend. Counting broker calendar dates instead would report the
    # same total here but would mislabel a session that spans midnight as two
    # days, which is the same class of bug as grouping by wall-clock date in
    # check_bar_count.
    gaps = frame["broker_time_raw"].diff() / 60.0
    trading_days = int(gaps.ge(SESSION_BOUNDARY_MINUTES).sum()) + int(not frame.empty)

    report = YearReport(
        year=year,
        bars=len(frame),
        trading_days=trading_days,
    )
    report.checks = [
        check_bar_count(frame),
        check_duplicates(frame),
        check_monotonic(frame),
        check_ohlc(frame),
        check_gaps(frame),
        check_spread(frame, config, year),
        check_break_hour(frame),
        check_known_anomalies(frame, config["validation"]["anomaly_windows"]),
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
        f"**Verdict: {verdict}** ({total_errors} error, {total_warnings} peringatan)",
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
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    config: dict[str, Any] = load_config("data")
    symbol = config["mt5"]["symbol"]
    timeframe = args.timeframe or config["mt5"]["timeframes"][0]
    pattern = config["data"]["filename_pattern"]

    data_dir = Path(args.data_dir) if args.data_dir else RAW_DIR / timeframe

    files = discover_files(symbol, timeframe, pattern, data_dir)
    if not files:
        message = f"GAGAL: tidak ada file data di {data_dir}"
        logger.error(message)
        print(message, file=sys.stderr)
        return 1

    reports = [validate_year(path, config) for path in files]
    document = render_markdown(reports)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORTS_DIR / f"data_validation_{date.today().isoformat()}.md"
    out.write_text(document, encoding="utf-8")

    for report in reports:
        mark = "LOLOS" if report.ok else "GAGAL"
        line = (
            f"{report.year}: {report.bars:,} bar, {len(report.errors)} error, "
            f"{len(report.warnings)} peringatan -> {mark}"
        )
        logger.info(line)
        print(line)

    logger.info("laporan ditulis ke %s", out)
    print(f"Laporan: {out}")
    return 0 if all(r.ok for r in reports) else 1


if __name__ == "__main__":
    sys.exit(main())
