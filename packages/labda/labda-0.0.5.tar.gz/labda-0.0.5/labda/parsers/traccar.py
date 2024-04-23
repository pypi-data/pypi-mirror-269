from datetime import datetime
from typing import Any, Tuple
from urllib.parse import urljoin

import pandas as pd
import requests
from pytz import UTC
from requests.auth import HTTPBasicAuth

from ..logging import success_parsing_log
from ..structure.subject import SCHEMA, Column, Metadata, Sensor, Subject, Vendor
from ..utils import (
    align_datetimes,
    get_sampling_frequency,
)
from .utils import set_crs, set_timezone


def _get_device(
    url: str,
    username: str,
    password: str,
    subject_id: str,
) -> dict[str, Any]:
    url = urljoin(url, "api/devices")

    params = {"uniqueId": subject_id}

    headers = {
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
    )

    response_json = response.json()

    if not response_json:
        raise ValueError(f"Device with subject_id {subject_id} not found")

    device = response_json[0]
    phone = device["phone"]
    model = device["model"]

    if phone and model:
        model = f"{phone} ({model})"
    elif phone:
        model = phone
    elif model:
        model = model

    return {
        "id": device["id"],
        "model": model,
    }


def _get_records(
    url: str,
    username: str,
    password: str,
    id: int,
    start: datetime | None = None,
    end: datetime | None = None,
) -> dict[str, Any]:
    url = urljoin(url, "api/reports/route")

    params = {
        "deviceId": id,
        "from": start,
        "to": end,
    }

    headers = {
        "Accept": "application/json",
    }

    response = requests.get(
        url,
        params,
        auth=HTTPBasicAuth(username, password),
        headers=headers,
    )

    response_json = response.json()

    if not response_json:
        raise ValueError(f"No records found for device with id {id}")

    return response_json


def _parse_records(response_json: dict[str, Any]) -> pd.DataFrame:
    df = pd.DataFrame(response_json)
    attributes = pd.json_normalize(df["attributes"]).add_prefix("attributes_")  # type: ignore
    df = pd.concat([df, attributes], axis=1).drop(columns=["attributes"])

    df = df[df["valid"] == True]
    df.rename(
        columns={
            "fixTime": Column.DATETIME,
            "altitude": Column.ELEVATION,
            "attributes_distance": Column.DISTANCE,
            "accuracy": Column.GNSS_ACCURACY,
            "attributes_motion": Column.MOTION,
        },
        inplace=True,
    )

    df = df[
        [
            Column.DATETIME,
            Column.LATITUDE,
            Column.LONGITUDE,
            Column.ELEVATION,
            Column.SPEED,
            Column.DISTANCE,
            Column.GNSS_ACCURACY,
            Column.MOTION,
        ]
    ]

    df[Column.DATETIME] = pd.to_datetime(df[Column.DATETIME], utc=True)
    df.set_index(Column.DATETIME, inplace=True)

    return df


def from_server(
    url: str,
    username: str,
    password: str,
    subject_id: str,
    sensor_id: str | None = None,
    serial_number: str | None = None,
    model: str | None = None,
    vendor: Vendor = Vendor.TRACCAR,
    firmware_version: str | None = None,
    start: datetime | None = None,
    end: datetime | None = None,
    sampling_frequency: float | None = None,
    crs: str | None | Tuple[str, str] = None,
    timezone: str | None | Tuple[str, str] = None,
) -> Subject:
    if not start:
        start = datetime.fromtimestamp(0)

    if not end:
        end = datetime.now()

    start = start.astimezone(UTC).isoformat()  # type: ignore
    end = end.astimezone(UTC).isoformat()  # type: ignore

    device = _get_device(url, username, password, subject_id)
    records = _get_records(url, username, password, device["id"], start, end)
    df = _parse_records(records)

    df, timezone = set_timezone(df, timezone)
    df.index = df.index.tz_convert(timezone).tz_localize(None)  # type: ignore

    df, crs = set_crs(df, crs)

    if not sampling_frequency:
        sampling_frequency = get_sampling_frequency(df)

    df = align_datetimes(df, sampling_frequency)

    # Order columns as defined in Column, remove extra columns
    records_columns = [col.value for col in Column]
    ordered_columns = [col for col in records_columns if col in df.columns]
    df = df[ordered_columns]

    df = SCHEMA.validate(df)

    sensor_id = sensor_id or device["id"]
    model = model or device["model"]

    sensor = Sensor(
        id=sensor_id,  # type: ignore
        serial_number=serial_number,
        model=model,
        vendor=vendor,
        firmware_version=firmware_version,
    )

    metadata = Metadata(
        id=subject_id,
        sensor=[sensor],
        sampling_frequency=sampling_frequency,
        crs=crs,
        timezone=timezone,
    )

    subject = Subject(metadata=metadata, df=df)

    func = f"{__name__}:from_server"
    success_parsing_log(subject, url, func)

    return subject
