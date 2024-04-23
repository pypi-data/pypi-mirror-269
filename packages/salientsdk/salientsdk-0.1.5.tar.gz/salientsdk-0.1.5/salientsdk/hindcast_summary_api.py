#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Hindcast Summary statistics.

This module is an interface to the Salient `hindcast_summmary` API, which returns
summary statistics for historical weather forecast quality.

Command line usage example:

```
cd ~/salientsdk
# this will get a single variable in a single file:
python -m salientsdk hindcast_summary -lat 42 -lon -73 -u username -p password --force
# to request multiple variables, separate them with a comma:
python -m salientsdk hindcast_summary -lat 42 -lon -73 --variable temp,precip
# to request variables AND multiple seasons:
python -m salientsdk hindcast_summary -lat 42 -lon -73 --variable temp,precip --season DJF,MAM

```

"""

import hashlib
import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import xarray as xr

from . import login_api
from .constants import _build_urls, get_model_version
from .location import Location
from .login_api import (
    download_queries,
    get_api_key,
    get_current_session,
    get_verify_ssl,
)

REFERENCE_VALUES = ["-auto", "ai", "clim", "gfs", "ecmwf", "blend", "norm_5yr", "norm_10yr"]
METRIC_VALUES = ["rps", "mae", "crps", "rps_skill_score", "mae_skill_score", "crps_skill_score"]
SEASON_VALUES = ["all", "DJF", "MAM", "JJA", "SON"]

COL_FILE = "file_name"
ENDPOINT = "hindcast_summary"


def hindcast_summary(
    loc: Location,
    metric: str = "crps",
    reference: str = "-auto",
    season: str | list[str] = "all",
    split_set: str = "all",
    timescale="all",
    variable: str | list[str] = "temp",
    version: str | list[str] = get_model_version(),
    force: bool = False,
    session: requests.Session = get_current_session(),
    apikey: str | None = get_api_key(),
    verify: bool = get_verify_ssl(),
    verbose: bool = False,
    **kwargs,
) -> str:
    """Get summary of accuracy metrics.

    This function is a convenience wrapper to the Salient
    [API](https://api.salientpredictions.com/v2/documentation/api/#/Validation/hindcast_summary).

    Args:
        loc (Location): The location to query
        metric (str): The accuracy metric to calculate. Defaults to "crps".
        reference (str): The reference dataset to compare against. Defaults to "-auto".
        season (str | list[str]): Meteorological season to consider.
            Defaults to "all".
            May also be a list of strings or a comma-separated string to vectorize the query.
            Also valid: DJF, MAM, JJA, SON.
        split_set (str): The split set to use. Defaults to "all".
        timescale (str): Forecast look-ahead.
            - `sub-seasonal` is 1-5 weeks.  Will return a coordinate `forecast_date_weekly` and
                a data variable `anom_weekly` or `vals_weekly`.
            - `seasonal` is 1-3 months.  Will return a coordinate `forecast_date_monthly` and a
                data variable `anom_monthly` or `vals_monthly`.
            - `long-range` is 1-4 quarters.  Will return a coordinate `forecast_date_quarterly` and a
                data variable `anom_quarterly` or `vals_quarterly`.
            - `all` (default) will include `sub-seasonal`, `seasonal`, and `long-range` timescales
        variable (str | list[str]): The variable to query, defaults to `temp`
            To request multiple variables, separate them with a comma `temp,precip` or use a list.
            This will download one file per variable
            See the
            [Data Fields](https://salientpredictions.notion.site/Variables-d88463032846402e80c9c0972412fe60)
            documentation for a full list of available historical variables.
        version (str | list[str]): The model version of the Salient `blend` forecast.
            To compare multiple versions, provide a list or comma-separated string.
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The `Session` object to use for the request.
            Defaults to use get_current_session(), typically set during `login()`.
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided
            and `get_api_key()` returns `None`.
        verify (bool): Verify the SSL certificate.
            Defaults to use get_verify_ssl(), typically set during `login()`.
        verbose (bool): If True (default False) print status messages.
        **kwargs: Additional arguments to pass to the API

    Keyword Arguments:
        units (str): `SI` or `US`

    Returns:
        str: the file name of the downloaded data.
            File names are a hash of the query parameters.
            When `force=False` and the file already exists, the function will return the file name
            almost instantaneously without querying the API.
            If multiple files are requested, they will be concatenated into a single table.
    """
    model = "blend"  # hardcode, not supporting "ai" in the sdk
    format = "csv"  # hardcode, not supporting "table" in the sdk

    # These args aren't natively vectorized in the API, so we'll do it here
    variable = _expand_comma(variable)
    season = _expand_comma(season, SEASON_VALUES, "season")

    assert reference in REFERENCE_VALUES, f"reference must be one of {REFERENCE_VALUES}"
    # We can't expand_comma on "metric" since it changes the column headers
    # and messes up the multi-file concatenation.
    assert metric in METRIC_VALUES, f"metric must be one of {METRIC_VALUES}"

    if reference == "-auto":
        reference = "gfs"

    args = loc.asdict(
        metric=metric,
        reference=reference,
        season=season,
        split_set=split_set,
        timescale=timescale,
        variable=variable,
        version=version,
        format=format,
        model=model,
        apikey=apikey,
        **kwargs,
    )

    queries = _build_urls(ENDPOINT, args)

    download_queries(
        query=queries["query"].values,
        file_name=queries[COL_FILE].values,
        force=force,
        session=session,
        verify=verify,
        verbose=verbose,
        format=format,
    )

    file_name = _concatenate_hindcast_summary(queries, format)

    if verbose:
        print(f"Saving combined table to {file_name}")

    return file_name


def _concatenate_hindcast_summary(queries: pd.DataFrame, format: str) -> str:
    file_names = queries[COL_FILE].values
    if len(file_names) == 1:
        # Most of the time, we'll only have downloaded a single file.
        # No need to concatenate.
        return file_names[0]

    scores = pd.concat(
        [
            pd.read_csv(row[COL_FILE]).assign(
                **{col: row[col] for col in queries.columns if col not in ["query", COL_FILE]}
            )
            for index, row in queries.iterrows()
        ],
        ignore_index=True,
    )

    # Now let's generate a filename for the combined table
    hash = hashlib.md5(str(file_names).encode()).hexdigest()
    file_name = f"{ENDPOINT}_{hash}.{format}"

    scores.to_csv(file_name, index=False)

    return file_name


def _expand_comma(
    val: str | list[str], valid: list[str] | None = None, name="value"
) -> list[str] | str:
    """Expand a comma-separated string into a list of strings.

    Args:
        val (str | list[str]): A single string that may contain commas.
            If a list of strings, convert to a single string if length == 1
        valid (list[str] | None): A list of valid values for the string.
            If None (default) no validation is performed.
            If provided, asserts
        name (str): The name of the value to use in error messages.

    Returns:
        list[str] | str: A list of strings if commas are present,
            otherwise the original string or list of strings.
    """
    if isinstance(val, str) and "," in val:
        val = val.split(",")

    # Check to see if val is a list of strings
    if isinstance(val, list):
        if len(val) == 1:
            val = val[0]

    if valid:
        if isinstance(val, list):
            for v in val:
                assert v in valid, f"{name} {v} not in {valid}"
        else:
            assert val in valid, f"{name} {val} not in {valid}"

    return val


def transpose_hindcast_summary(scores: str | pd.DataFrame, min_score: float = 0.0) -> pd.DataFrame:
    """Transpose hindcast_summary long to wide, preserving groups.

    Transposes the hindcast summary data from a long format to a wide format
    where each 'Lead' row becomes a column.

    Parameters:
        scores (str | pd.DataFrame): The hindcast scores data.
            This can be either a file path as a string or a pre-loaded DataFrame
            of the type returned by `hindcast_summary()`
        min_score (float): Render any scores below this threshold as NA

    Returns:
        pd.DataFrame: The transposed DataFrame with 'Lead' categories as columns.
    """
    if isinstance(scores, str):
        scores = pd.read_csv(scores)

    # The first 5 columns are standard columns that are always present
    # Any additional columns represent the vectorized arguments
    # (and may not exist if arguments were not vectorized)

    # set the table index to be columns 6 to end:
    unstack_by = "Lead"
    vector_cols = scores.columns[5:].tolist()
    index_cols = vector_cols + [unstack_by]
    extract_col = 4  # This should be the relative skill score
    if isinstance(extract_col, int):
        extract_col = scores.columns[extract_col]

    scores.set_index(index_cols, inplace=True)
    scores = scores[[extract_col]]

    # Adds new rows with Lead="mean"
    scores = _add_mean(scores)

    if len(index_cols) == 1:
        # If there is no vector expansion we don't need an unstack.
        # A simple transpose will do.
        scores = scores.T
    else:
        # Preserve the order of the original table rows
        unstack_row = scores.index.get_level_values(unstack_by).unique()
        scores = scores.unstack(unstack_by)
        # restore the original order of the rows, now in column form
        scores = scores[extract_col][unstack_row]

    # make any scores below min_score NA
    scores = scores.where(scores >= min_score)

    return scores


def _add_mean(scores: pd.DataFrame, weeks=1.0, months=0.5, quarters=0.25) -> pd.DataFrame:
    """Add a row with the mean of the scores.

    This adds a set of rows to the DataFrame with the mean of the scores
    weighted by the number of weeks, months, or quarters in the forecast lead.

    Args:
        scores (pd.DataFrame): The DataFrame of scores as returned by `hindcast_summary()`
        weeks (int): Weight for weeks 3-5
        months (float): Weight for months 2-3
        quarters (float): Weight for quarters 2-4

    Returns:
        pd.DataFrame: The DataFrame with the mean rows added.
    """
    # get the names of the index columns of scores
    unstack_by = "Lead"
    index_cols = scores.index.names
    vector_cols = index_cols.copy()
    vector_cols.remove(unstack_by)

    WGT = "Weight"
    weights = {
        "Week 1": 0,
        "Week 2": 0,
        "Week 3": weeks,
        "Week 4": weeks,
        "Week 5": weeks,
        "Month 1": 0,
        "Month 2": months,
        "Month 3": months,
        "Months 1-3": 0,
        "Months 4-6": quarters,
        "Months 7-9": quarters,
        "Months 10-12": quarters,
    }
    extract_col = scores.columns[0]

    weights = pd.DataFrame.from_dict(weights, orient="index", columns=[WGT])
    weights.index.name = unstack_by
    scores = scores.merge(weights, how="left", left_index=True, right_index=True)

    def _weighted_mean(group):
        if WGT in group.columns and extract_col in group.columns:
            # Ensure there are no NaN values in weights or the extract_col
            group = group.dropna(subset=[WGT, extract_col])
            if not group.empty:
                return np.average(group[extract_col], weights=group[WGT]).round(2)

    if len(vector_cols) == 0:
        avg = pd.DataFrame({extract_col: [_weighted_mean(scores)], unstack_by: ["mean"]})
    else:
        avg = (
            scores.groupby(level=vector_cols)  # don't include "Lead" in the groupby
            .apply(_weighted_mean)
            .reset_index(name=extract_col)
        )
        avg[unstack_by] = "mean"
    avg.set_index(index_cols, inplace=True)

    scores.drop(columns=WGT, inplace=True)  # don't need this anymore
    scores = pd.concat([scores, avg], ignore_index=False, axis=0)
    return scores
