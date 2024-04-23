#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Historical data timeseries.

This module is an interface to the Salient `data_timeseries` API, which returns historical
observed data.  It also includes utility functions for operating on the returned data.

Command line usage example:

```
cd ~/salientsdk
# this will get a single variable in a single file:
python -m salientsdk data_timeseries -lat 42 -lon -73 -fld all --start 2020-01-01 --end 2020-12-31 --force
# this will get multiple variables in separate files:
python -m salientsdk data_timeseries -lat 42 -lon -73 -fld all -var temp,precip
```

"""

import os

import requests
import xarray as xr

from .constants import _build_url
from .location import Location
from .login_api import download_query, get_api_key, get_current_session, get_verify_ssl


def data_timeseries(
    loc: Location,
    variable: str = "temp",
    field: str = "anom",
    debias: bool = False,
    start: str = "1950-01-01",
    end: str = "-today",
    format: str = "nc",
    frequency: str = "daily",
    force: bool = False,
    session: requests.Session = get_current_session(),
    apikey: str | None = get_api_key(),
    verify: bool = get_verify_ssl(),
    verbose: bool = False,
    **kwargs,
) -> str | dict[str, str]:
    """Get a historical time series of ERA5 data.

    This function is a convenience wrapper to the Salient
    [API](https://api.salientpredictions.com/v2/documentation/api/#/Historical/get_data_timeseries).

    Args:
        loc (Location): The location to query
        variable (str): The variable to query, defaults to `temp`
            To request multiple variables, separate them with a comma `temp,precip`
            This will download one file per variable
            See the
            [Data Fields](https://salientpredictions.notion.site/Variables-d88463032846402e80c9c0972412fe60)
            documentation for a full list of available historical variables.
        field (str): The field to query, defaults to "anom"
        debias (bool): If True, debias the data to local observations.  Disabled for `shapefile` locations.  [detail](https://salientpredictions.notion.site/Debiasing-2888d5759eef4fe89a5ba3e40cd72c8f)
        start (str): The start date of the time series
        end (str): The end date of the time series
        format (str): The format of the response
        frequency (str): The frequency of the time series
        force (bool): If False (default), don't download the data if it already exists
        session (requests.Session): The session object to use for the request
        apikey (str | None): The API key to use for the request.
            In most cases, this is not needed if a `session` is provided
            and `get_api_key()` returns `None`.
        verify (bool): If True (default), verify the SSL certificate
        verbose (bool): If True (default False) print status messages
        **kwargs: Additional arguments to pass to the API

    Keyword Arguments:
        units (str): `SI` or `US`

    Returns:
        str | dict: the file name of the downloaded data.  File names are a hash of the query parameters.
            When `force=False` and the file already exists, the function will return the file name
            almost instantaneously without querying the API.
            If multiple variables are requested, returns a `dict` of `{variable:file_name}`
    """
    assert field in [
        "anom",
        "anom_d",
        "anom_ds",
        "anom_qnt",
        "anom_s",
        "clim",
        "stdv",
        "trend",
        "vals",
        "all",
    ], f"Invalid field {field}"
    assert format in ["nc", "csv"], f"Invalid format {format}"
    assert frequency in [
        "daily",
        "weekly",
        "monthly",
        "3-monthly",
    ], f"Invalid frequency {frequency}"

    # if there is a comma in variable, vectorize:
    if isinstance(variable, str) and "," in variable:
        variable = variable.split(",")

    if isinstance(variable, list):
        file_names = {
            var: data_timeseries(
                loc=loc,
                variable=var,
                field=field,
                debias=debias,
                start=start,
                end=end,
                format=format,
                frequency=frequency,
                force=force,
                session=session,
                verify=verify,
                verbose=verbose,
                apikey=apikey,
                **kwargs,
            )
            for var in variable
        }
        if verbose:
            print(file_names)
        return file_names

    endpoint = "data_timeseries"
    args = loc.asdict(
        start=start,
        end=end,
        debias=debias,
        field=field,
        format=format,
        frequency=frequency,
        variable=variable,
        apikey=apikey,
        **kwargs,
    )

    (query, file_name) = _build_url(endpoint, args)

    download_query(
        query=query,
        file_name=file_name,
        force=force,
        session=session,
        verify=verify,
        verbose=verbose,
        format=format,
    )

    return file_name


def load_multihistory(files: dict, fields: list[str] = ["vals"]) -> xr.Dataset:
    """Load multiple history files and merge them into a single dataset.

    Args:
        files (dict): Dictionary of `{variable:file_name}` of the type returned by
                      `data_timeseries` when multiple `variable`s are requested
                      e.g. `data_timeseries(..., variable = "temp,precip")`
        fields (list[str]): List of fields to extract from the history files

    Returns:
        xr.Dataset: The merged dataset, where each field and variable is renamed
        to `<variable>_<field>` or simply `variable` if field = "vals".
    """

    def __extract_history_fields(file: str, variable: str, fields: str) -> xr.Dataset:
        hst = xr.load_dataset(file)
        hst = hst[fields]
        fields_new = [variable if field == "vals" else variable + "_" + field for field in fields]
        hst = hst.rename({field: field_new for field, field_new in zip(fields, fields_new)})
        for fld in fields_new:
            hst[fld].attrs = hst.attrs
        hst.attrs = {}
        hst.close()

        return hst

    # Would prefer to use xr.open_mfdataset, but we need to pass in the variable name
    # Can convert when history files have a short_name attribute
    # https://salientpredictions.atlassian.net/browse/RD-1184
    hst = xr.merge(
        [__extract_history_fields(files[variable], variable, fields) for variable in files.keys()]
    )
    return hst
