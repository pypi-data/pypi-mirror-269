#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Interface to the Salient `upload_file` API.

Command line usage example:
```
cd ~/salientsdk
python -m salientsdk.upload_file
```
"""

import json
import os

import pandas as pd
import requests

from .constants import _build_url
from .login_api import get_current_session, login


def upload_file(
    file: str, verbose: bool = True, session: requests.Session = get_current_session()
) -> None:
    """Uploads a geography file to the Salient API.

    An interface to to the Salient
    [upload_file](https://api.salientpredictions.com/v2/documentation/api/#/General/upload_file)
    API endpoint.

    Args:
        file (str): the file to upload (e.g. a shapefile or CSV).
        verbose (bool): whether to print status messages.
        session (requests.Session): the session to use for the upload.

    """
    if verbose:
        print(f"Uploading {file}")

    (url, loc_file) = _build_url("upload_file")

    # do we need to open .zipped shapefiles in 'rb' binary mode?
    req = session.post(url, files={"file": open(file, "r")})
    req.raise_for_status()
    if verbose:
        print(req.text)

    return None


def upload_bounding_box(
    north: float,
    south: float,
    east: float,
    west: float,
    geoname: str,
    force: bool = False,
    verbose: bool = True,
    session: requests.Session = get_current_session(),
) -> str:
    """Upload a bounding box.

    Create and upload a GeoJSON shapefile with a rectangular bounding box
    for later use with the `shapefile` location argument.

    Args:
        north (float): Northern extent decimal latitude
        south (float): Southern extent decimal latitude
        east (float): Eastern extent decimal longitude
        west (float): Western extent decimal longitude
        geoname (str): Name of the GeoJSON file and object to create
        force (bool): If the file already exists, don't upload it
        verbose (bool): Whether to print status messages
        session (requests.Session): The session object to use for the request

    Returns:
        str: File name of the GeoJSON file
    """
    geofile = geoname + ".geojson"
    if not force and os.path.exists(geofile):
        if verbose:
            print(f"File {geofile} already exists")
        return geofile

    assert west < east, "West must be less than East"
    assert south < north, "South must be less than North"
    assert session is not None, "login to create a session"

    geoshape = {
        "type": "Feature",
        "properties": {"name": geoname},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [[west, north], [east, north], [east, south], [west, south], [west, north]]
            ],
        },
    }
    with open(geofile, "w") as f:
        json.dump(geoshape, f)

    upload_file(geofile, verbose, session)

    return geofile


def upload_location_file(
    lats: list[float],
    lons: list[float],
    names: list[str],
    geoname: str,
    force: bool = False,
    verbose: bool = False,
    session: requests.Session = get_current_session(),
    **kwargs,
) -> str:
    """Upload a vector of locations.

    Create and upload a CSV file with a list of locations for
    later use with the `location_file` location argument.

    Args:
        lats (list[float]): List of decimal latitudes
        lons (list[float]): List of decimal longitudes
        names (list[str]): List of names for the locations
        geoname (str): Name of the CSV file and object to create
        force (bool): When False, if the file already exists don't upload it
        verbose (bool): If True, print status messages
        session (requests.Session): The session object to use for the request
        **kwargs: Additional columns to include in the CSV file

    Returns:
        str: File name of the CSV file
    """
    geofile = geoname + ".csv"
    if not force and os.path.exists(geofile):
        if verbose:
            print(f"File {geofile} already exists")
        return geofile

    loc_table = pd.DataFrame({"lat": lats, "lon": lons, "name": names, **kwargs})
    loc_table.to_csv(geofile, index=False)

    upload_file(geofile, verbose, session)

    return geofile


if __name__ == "__main__":
    session = login()

    geofile = upload_bounding_box(
        west=-109.1, east=-102.0, south=37.8, north=41.0, geoname="Colorado", session=session
    )

    # read the JSON geofile
    with open(geofile, "r") as f:
        print(json.load(f))
