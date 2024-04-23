#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Forecast data timeseries.

This module is an interface to the Salient `forecast_timeseries` API, which returns
probabilistic weather forecasts in subseasonal-to-seasonal timescales.

Command line usage example:

```
cd ~/salientsdk
# this will get a single variable in a single file:
python -m salientsdk forecast_timeseries -lat 42 -lon -73 --timescale seasonal -u username -p password
# this will get multiple variables in separate files:
python -m salientsdk forecast_timeseries -lat 42 -lon -73 -var temp,precip --timescale seasonal
```

"""

import os
from datetime import datetime

import requests
import xarray as xr

from . import login_api
from .constants import _build_url, get_model_version
from .location import Location
from .login_api import get_api_key, get_current_session, get_verify_ssl


def forecast_timeseries(
    loc: Location,
    date: str = "-today",
    debias: bool = False,
    field: str = "anom",
    format: str = "nc",
    model: str = "blend",
    reference_clim: str = "30_yr",
    timescale="all",
    variable: str = "temp",
    version: str = get_model_version(),
    force: bool = False,
    session: requests.Session = get_current_session(),
    apikey: str | None = get_api_key(),
    verify: bool = get_verify_ssl(),
    verbose: bool = False,
    **kwargs,
) -> str | dict[str, str]:
    """Get time series of S2S meteorological forecasts.

    This function is a convenience wrapper to the Salient
    [API](https://api.salientpredictions.com/v2/documentation/api/#/Forecasts/forecast_timeseries).

    Args:
        loc (Location): The location to query
        date (str): The date the forecast was generated.  Defaults to `-today`, which will find the
            most recent forecast.  Can also be a specific date in the format `YYYY-MM-DD`.
        debias (bool): If True, debias the data to local observations.
            Disabled for `shapefile` locations.
            [detail](https://salientpredictions.notion.site/Debiasing-2888d5759eef4fe89a5ba3e40cd72c8f)
        field (str): The field to query, defaults to `anom` which is an anomaly value from climatology.
            Also available: `vals`, which will return absolute values without regard to climatology.
        format (str): The file format of the response.
            Defaults to `nc` which returns a multivariate NetCDF file.
            Also available: `csv` which returns a CSV file.
        model (str): The model to query.  Defaults to `blend`, which is the Salient blended forecast.
        reference_clim (str):  Reference climatology for calculating anomalies.
            Ignored when `field=vals` since there are no anomalies to calculate.
            Defaults to `30_yr`, which is the 30-year climatology.
        timescale (str): Forecast look-ahead.
            - `sub-seasonal` is 1-5 weeks.  Will return a coordinate `forecast_date_weekly` and
                a data variable `anom_weekly` or `vals_weekly`.
            - `seasonal` is 1-3 months.  Will return a coordinate `forecast_date_monthly` and a
                data variable `anom_monthly` or `vals_monthly`.
            - `long-range` is 1-4 quarters.  Will return a coordinate `forecast_date_quarterly` and a
                data variable `anom_quarterly` or `vals_quarterly`.
            - `all` (default) will include `sub-seasonal`, `seasonal`, and `long-range` timescales
        variable (str): The variable to query, defaults to `temp`
            To request multiple variables, separate them with a comma `temp,precip`
            This will download one file per variable
            See the
            [Data Fields](https://salientpredictions.notion.site/Variables-d88463032846402e80c9c0972412fe60)
            documentation for a full list of available historical variables.
        version (str): The model version of the Salient `blend` forecast.
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
        str | dict: the file name of the downloaded data.
            File names are a hash of the query parameters.
            When `force=False` and the file already exists, the function will return the file name
            almost instantaneously without querying the API.
            If multiple variables are requested, returns a `dict` of `{variable:file_name}`
    """
    assert field in [
        "anom",
        "vals",
        "vals_ens",
    ], f"Invalid field {field}"
    assert format in ["nc", "csv"], f"Invalid format {format}"

    if date == "-today":
        date = datetime.today().strftime("%Y-%m-%d")

    # if there is a comma in variable, vectorize:
    if isinstance(variable, str) and "," in variable:
        variable = variable.split(",")

    if isinstance(variable, list):
        file_names = {
            var: forecast_timeseries(
                loc=loc,
                date=date,
                debias=debias,
                field=field,
                format=format,
                model=model,
                reference_clim=reference_clim,
                timescale=timescale,
                variable=var,
                version=version,
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

    endpoint = "forecast_timeseries"
    args = loc.asdict(
        date=date,
        debias=debias,
        field=field,
        format=format,
        model=model,
        reference_clim=reference_clim,
        timescale=timescale,
        variable=variable,
        version=version,
        apikey=apikey,
        **kwargs,
    )

    (query, file_name) = _build_url(endpoint, args)

    if force or not os.path.exists(file_name):
        if verbose:
            print(f"Downloading {query} to {file_name}")
        with open(file_name, "wb" if format == "nc" else "w") as f:
            result = session.get(query, verify=verify)
            result.raise_for_status()
            if format == "nc":
                f.write(result.content)
            else:
                f.write(result.text)
    elif verbose:
        print(f"File {file_name} already exists")

    return file_name
