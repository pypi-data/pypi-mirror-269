import time
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pandas as pd

from ..logging import success_parsing_log
from ..structure.subject import Metadata, Sensor, Subject, Vendor
from ..structure.validation.subject import SCHEMA, Column
from ..utils import (
    align_datetimes,
    filter_datetime,
    get_sampling_frequency,
)
from .utils import set_timezone


def _parse_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        engine="pyarrow",
        dtype={
            " general/nodata/time": "boolean",
            " activity/lying_sitting_rest/time": "boolean",
            " activity/lying_sitting_movement/time": "boolean",
            " activity/upright_stand/time": "boolean",
            " activity/upright_sporadic_walk/time": "boolean",
            " activity/upright_walk/time": "boolean",
            " activity/upright_moderate/time": "boolean",
            " activity/upright_run/time": "boolean",
            " activity/cycling/time": "boolean",
        },
    )

    df[Column.DATETIME] = pd.to_datetime(
        df[" unixts"], unit="ms", origin="unix", utc=True
    )
    df[Column.WEAR] = ~df[" general/nodata/time"]
    df.drop(columns=["utc", " local", " unixts", " general/nodata/time"], inplace=True)
    df.set_index(Column.DATETIME, inplace=True)

    df.rename(
        columns={" activity/intensity/count": Column.ACTIVITY_VALUE}, inplace=True
    )

    return df


def _infer_position(df: pd.DataFrame) -> None:
    df.loc[
        df[" activity/lying_sitting_rest/time"]
        | df[" activity/lying_sitting_movement/time"],
        Column.POSITION,
    ] = "sitting-lying"

    df.loc[
        df[" activity/upright_stand/time"]
        | df[" activity/upright_sporadic_walk/time"]
        | df[" activity/upright_walk/time"]
        | df[" activity/upright_moderate/time"]
        | df[" activity/upright_run/time"],
        Column.POSITION,
    ] = "standing"

    df.loc[df[" activity/cycling/time"], Column.POSITION] = "sitting"


def _infer_activity_intensity(df: pd.DataFrame) -> None:
    labels = ["sedentary", "light", "moderate", "vigorous", "very_vigorous"]
    cuts = [0, 2, 50, 75, 100, float("inf")]

    df[Column.ACTIVITY_INTENSITY] = pd.cut(
        df[Column.ACTIVITY_VALUE],
        bins=cuts,
        labels=labels,
        right=False,
        include_lowest=True,
    )


def _infer_steps(df: pd.DataFrame) -> None:
    df[Column.STEPS] = (
        df[" activity/steps/count"]
        + df[" activity/steps2/count"]
        + df[" activity/steps3/count"]
    )
    df[Column.STEPS] = df[Column.STEPS].round().astype("Int16")


def _infer_activity(df: pd.DataFrame) -> None:
    df.loc[df[" activity/cycling/time"], Column.ACTIVITY] = "bicycling"
    df.loc[df[" activity/lying_sitting_rest/time"], Column.ACTIVITY] = "resting"
    df.loc[df[" activity/upright_sporadic_walk/time"], Column.ACTIVITY] = (
        "sporadic_walking"
    )
    df.loc[df[" activity/upright_walk/time"], Column.ACTIVITY] = "walking"
    df.loc[df[" activity/upright_moderate/time"], Column.ACTIVITY] = "jogging"
    df.loc[df[" activity/upright_run/time"], Column.ACTIVITY] = "running"


def from_csv(
    path: str | Path,
    *,
    subject_id: str | None = None,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    vendor: Vendor = Vendor.SENS,
    firmware_version: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    sampling_frequency: float | None = None,
    timezone: str | None | Tuple[str, str] = None,
) -> Subject:
    # https://support.sens.dk/hc/en-us/articles/15580259064093-Description-of-activity-categories

    if isinstance(path, str):
        path = Path(path)

    if not path.is_file():
        raise ValueError(f"Invalid file path: {path}")

    if path.suffix != ".csv":
        raise ValueError(f"Invalid file extension: {path.suffix}")

    df = _parse_csv(path)
    df, timezone = set_timezone(df, timezone)

    if not timezone:
        timezone = time.tzname[0]

    df.index = df.index.tz_convert(timezone).tz_localize(None)  # type: ignore

    df = filter_datetime(df, start, end)

    if not sampling_frequency:
        sampling_frequency = get_sampling_frequency(df)

    df = align_datetimes(df, sampling_frequency)

    _infer_position(df)
    _infer_activity_intensity(df)
    _infer_steps(df)
    _infer_activity(df)

    # Order columns as defined in Column, remove extra columns
    columns = [col.value for col in Column]
    ordered_columns = [col for col in columns if col in df.columns]
    df = df[ordered_columns]

    df = SCHEMA.validate(df)

    subject_id = subject_id or path.stem
    sensor_id = sensor_id or path.stem

    sensor = Sensor(
        id=sensor_id,
        serial_number=serial_number,
        model=model,
        vendor=vendor,
        firmware_version=firmware_version,
    )

    metadata = Metadata(
        id=subject_id,
        sensor=[sensor],
        sampling_frequency=sampling_frequency,
        timezone=timezone,
    )

    subject = Subject(metadata=metadata, df=df)

    func = f"{__name__}:from_csv"
    success_parsing_log(subject, path, func)

    return subject
