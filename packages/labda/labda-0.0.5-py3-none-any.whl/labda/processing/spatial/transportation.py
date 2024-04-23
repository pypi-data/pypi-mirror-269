from typing import Any

import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from ...expanders.spatial import add_speed
from ...structure.validation.subject import Column
from ...utils import columns_exists, columns_not_exists, get_unique_column_name


def _trip_mode_from_activity(df: pd.DataFrame) -> None:
    df.loc[
        (df[Column.TRIP_MODE] == "vehicle")
        & (
            df[Column.ACTIVITY_INTENSITY].isin(
                ["moderate", "vigorous", "very_vigorous"]
            )
        ),
        Column.TRIP_MODE,
    ] = "bicycle"

    df.loc[
        (df[Column.TRIP_MODE].isin(["bicycle", "walk/run"]))
        & (df[Column.ACTIVITY_INTENSITY] == "sedentary"),
        Column.TRIP_MODE,
    ] = "vehicle"


def _fill_trip_mode_pauses(df: pd.DataFrame, fill: str) -> pd.DataFrame:
    if fill == "forward":
        df[Column.TRIP_MODE] = df[Column.TRIP_MODE].ffill()
    elif fill == "backward":
        df[Column.TRIP_MODE] = df[Column.TRIP_MODE].bfill()
    else:
        raise ValueError("fill must be either 'ffill' or 'bfill'")

    return df


def _set_trip_mode(df: pd.DataFrame, name: str):
    modes = df[name].value_counts()
    dominant_mode = modes.idxmax()
    df[name] = dominant_mode


def _get_partial_trips(df: pd.DataFrame) -> DataFrameGroupBy:
    helper_column = get_unique_column_name(df)
    df.loc[~df[Column.TRIP_STATUS].isin(["stationary", "pause"]), helper_column] = (
        df[Column.TRIP_STATUS] == "start"
    ).cumsum()

    return df.groupby([Column.TRIP_ID, helper_column])


def _detect_partial_transport(
    df: pd.DataFrame,
    on: Column | str,
    cut_points: dict[str, Any],
    window: int | None = None,
    activity: bool = False,
    name: str = Column.TRIP_MODE,
) -> pd.DataFrame:
    if window:
        df[on] = df[on].rolling(window=window, min_periods=1).mean()

    # Extract max values from cut_points
    bins = [-float("inf")]
    bins += [cp["max"] for cp in cut_points["cut_points"]]

    # Extract names from cut_points
    labels = [cp["name"] for cp in cut_points["cut_points"]]

    # Apply cut points
    df[name] = pd.cut(df[on], bins=bins, labels=labels)

    if activity:
        _trip_mode_from_activity(df)

    _set_trip_mode(df, name)

    return df


# FIXME: Fix custom column name, definitely does not work. It should be propably removed because then activity_intensity column name is also needed.
def detect_transportation(
    df: pd.DataFrame,
    crs: str,
    cut_points: dict[str, Any],
    *,
    window: int | None = None,
    pause_fill: str | None = None,
    activity: bool = False,
    name: str = Column.TRIP_MODE,
    overwrite: bool = False,
) -> pd.DataFrame:
    columns_not_exists(df, [name], overwrite=overwrite)

    required_column = cut_points["required_data"]
    columns_exists(df, [Column.TRIP_ID, Column.TRIP_STATUS, required_column])

    if activity:
        columns_exists(df, [Column.ACTIVITY_INTENSITY])

    temp_df = df.copy()

    if required_column == Column.SPEED:
        temp_df = add_speed(temp_df, crs=crs, overwrite=True)

    partials = _get_partial_trips(temp_df)
    partials = partials.apply(
        lambda x: _detect_partial_transport(
            x, required_column, cut_points, window, activity, name
        ),
        include_groups=False,
    ).reset_index(level=[0, 1])

    df = df.merge(partials[name], on=Column.DATETIME, how="left")

    if pause_fill:
        trips = df.groupby(Column.TRIP_ID)
        trips = trips.apply(
            lambda x: _fill_trip_mode_pauses(x, pause_fill), include_groups=False
        ).reset_index(level=0)
        df.drop(Column.TRIP_MODE, axis=1, inplace=True)
        df = df.merge(trips[name], on=Column.DATETIME, how="left")

    return df.astype({name: "category"})
