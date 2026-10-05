"""Convert between the Finex MT5 server clock and UTC.

MT5 does not return Unix instants. It returns its server wall clock encoded as
if it were UTC, so reading the raw value as a UTC timestamp reproduces the
broker's clock reading rather than a real instant.

Finex's server clock is not fixed. It runs GMT+2 (EET) in winter and GMT+3
(EEST) in summer, switching on the second Sunday of March and the first Sunday
of November to follow US DST. Stated on finex.co.id/trading/instruments and
confirmed by Finex support on 2026-10-05 with the exact dates for 2023-2026.

Every transition lands on a Sunday while forex is closed. That was verified
against the data rather than assumed: all seven transitions in 2023-2026 have
zero bars, and the first bar after each one is a Monday. No trading day is ever
split across two offsets, so the offset resolves from the bar's own date.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from typing import Any

import numpy as np
import pandas as pd

SECONDS_PER_HOUR = 3600
EPOCH_DATE = date(1970, 1, 1)


def _days_since_epoch(value: date) -> int:
    """Days between the Unix epoch and ``value``.

    Args:
        value: Date to convert.

    Returns:
        Whole days since 1970-01-01, matching NumPy's ``datetime64[D]``.
    """
    return (value - EPOCH_DATE).days


@dataclass(frozen=True)
class BrokerSchedule:
    """Resolves the broker's UTC offset from its own wall-clock date.

    Attributes:
        standard_offset: Offset in seconds during winter, e.g. 7200 for GMT+2.
        daylight_offset: Offset in seconds during summer, e.g. 10800 for GMT+3.
        daylight_windows: Half-open (start, end) date ranges covering summer.
            The intraday transition hour is deliberately not modelled because
            every transition falls on a Sunday that carries no bars.
    """

    standard_offset: int
    daylight_offset: int
    daylight_windows: tuple[tuple[date, date], ...]

    @classmethod
    def from_config(cls, mt5_config: Mapping[str, Any]) -> BrokerSchedule:
        """Build a schedule from the ``mt5`` block of configs/data.yaml.

        Args:
            mt5_config: The ``mt5`` mapping loaded from the data config.

        Returns:
            A schedule ready for offset lookups.

        Raises:
            KeyError: If the config block is missing the offset or schedule.
            ValueError: If a schedule entry is not a valid date.
        """
        offsets = mt5_config["broker_utc_offset_hours"]
        windows: list[tuple[date, date]] = []
        for window in mt5_config["broker_dst_schedule"]:
            start, end = window["start"], window["end"]
            windows.append((_as_date(start), _as_date(end)))
        windows.sort()
        return cls(
            standard_offset=int(offsets["standard"]) * SECONDS_PER_HOUR,
            daylight_offset=int(offsets["daylight"]) * SECONDS_PER_HOUR,
            daylight_windows=tuple(windows),
        )

    def offset_seconds(self, broker_date: date) -> int:
        """Return the broker's UTC offset in seconds for a wall-clock date.

        Dates past the end of the last known daylight window raise instead of
        quietly returning the standard offset. Every date after that window is
        technically winter, so the fallback would look right right up to the
        next spring, then silently mislabel an entire summer by an hour.

        Args:
            broker_date: Date read from the broker's own wall clock.

        Returns:
            Offset in seconds to subtract from the wall clock to reach UTC.

        Raises:
            ValueError: If the date is beyond the configured schedule.
        """
        if self.daylight_windows and broker_date >= self.daylight_windows[-1][1]:
            raise ValueError(
                f"{broker_date} di luar jadwal DST yang diketahui "
                f"(terakhir {self.daylight_windows[-1][1]}). Perbarui "
                "broker_dst_schedule di configs/data.yaml, jangan tebak offset."
            )
        for start, end in self.daylight_windows:
            if start <= broker_date < end:
                return self.daylight_offset
        return self.standard_offset


def _as_date(value: Any) -> date:
    """Coerce a YAML scalar into a date.

    Args:
        value: A date, or an ISO-8601 string as PyYAML may return.

    Returns:
        The parsed date.

    Raises:
        ValueError: If the value cannot be read as a date.
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"Tanggal DST tidak valid: {value!r}") from exc


def broker_wall_clock(epoch: int) -> datetime:
    """Read a raw MT5 epoch as a naive broker wall-clock datetime.

    The raw digits already are the broker's clock reading. No offset is
    applied, because the goal here is the broker's own frame rather than UTC.

    Args:
        epoch: Raw epoch seconds as returned by MT5.

    Returns:
        Naive datetime holding the broker's wall-clock reading.
    """
    return datetime.fromtimestamp(epoch, tz=UTC).replace(tzinfo=None)


def broker_epoch_to_utc(epoch: int, schedule: BrokerSchedule) -> datetime:
    """Convert a raw MT5 epoch to the real UTC instant.

    Args:
        epoch: Raw epoch seconds holding the broker's wall clock.
        schedule: Broker schedule supplying the seasonal offset.

    Returns:
        Timezone-aware datetime in UTC.
    """
    wall = broker_wall_clock(epoch)
    return wall.replace(tzinfo=UTC) - timedelta(seconds=schedule.offset_seconds(wall.date()))


def wall_clock_series(raw: pd.Series) -> pd.Series:
    """Vectorised broker wall clock for a Series of raw MT5 epochs.

    Args:
        raw: Integer Series of raw epochs, typically ``broker_time_raw``.

    Returns:
        Naive datetime Series holding the broker's wall-clock reading.
    """
    return pd.to_datetime(raw, unit="s")


def utc_series(raw: pd.Series, schedule: BrokerSchedule) -> pd.Series:
    """Vectorised UTC conversion for a Series of raw MT5 epochs.

    Args:
        raw: Integer Series of raw epochs, typically ``broker_time_raw``.
        schedule: Broker schedule supplying the seasonal offset.

    Returns:
        Datetime Series in UTC with tzinfo attached, so the ``%z`` directive
        of ``TIME_FORMAT`` still renders an offset.
    """
    wall = wall_clock_series(raw)
    days = wall.values.astype("datetime64[D]").astype("int64")
    offsets = np.full(len(days), schedule.standard_offset, dtype="int64")
    for start, end in schedule.daylight_windows:
        start_day = _days_since_epoch(start)
        end_day = _days_since_epoch(end)
        offsets[(days >= start_day) & (days < end_day)] = schedule.daylight_offset
    return (wall - pd.to_timedelta(offsets, unit="s")).dt.tz_localize("UTC")
