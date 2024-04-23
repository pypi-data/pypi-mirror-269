#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Salient Predictions Software Development Kit."""

import os
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import toml

from .constants import get_model_version, set_model_version
from .data_timeseries_api import data_timeseries, load_multihistory
from .downscale_api import downscale
from .forecast_timeseries_api import forecast_timeseries
from .hindcast_summary_api import hindcast_summary, transpose_hindcast_summary
from .location import Location
from .login_api import (
    get_current_session,
    get_verify_ssl,
    login,
    set_current_session,
    set_verify_ssl,
)
from .upload_file_api import upload_bounding_box, upload_file, upload_location_file


def _get_version(pkgname):
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    if pyproject_path.exists():
        pyproject_content = toml.load(pyproject_path)
        return pyproject_content["tool"]["poetry"]["version"]
    else:
        # Try to import the version from installed package metadata
        # Only works for python v3.9 or later.
        try:
            return version(pkgname)
        except PackageNotFoundError:
            return "unknown"  # Development fallback


__version__ = _get_version("salientsdk")
__author__ = "Salient Predictions"
__all__ = [
    "login",
    "data_timeseries",
    "downscale",
    "forecast_timeseries",
    "get_current_session",
    "get_model_version",
    "get_verify_ssl",
    "hindcast_summary",
    "transpose_hindcast_summary",
    "load_multihistory",
    "Location",
    "set_model_version",
    "set_verify_ssl",
    "set_current_session",
    "upload_file",
    "upload_bounding_box",
    "upload_location_file",
]

if __name__ == "__main__":
    print(f"ver: {__version__} by: {__author__}")
