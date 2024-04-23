#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Constants for the Salient SDK.

This module contains constants used throughout the Salient SDK.

"""

import datetime
import hashlib
import itertools
import urllib

import pandas as pd
import requests

# This is the base URL for the Salient API:
URL = "https://api.salientpredictions.com/"

API_VERSION = "v2"

MODEL_VERSION = "v8"
MODEL_VERSIONS = ["v7_1", "v8"]


def _build_url(endpoint: str, args: None | dict = None) -> tuple[str, str]:
    url = URL + API_VERSION + "/" + endpoint
    file_name = endpoint

    if args:
        # apikey will often be None when we're using a persistent session:
        args = {k: v for k, v in args.items() if v is not None}

        url += "?"
        url += urllib.parse.urlencode(args, safe=",")

        # apikey doesn't influence the file contents, so shouldn't be in the hash:
        if "apikey" in args:
            del args["apikey"]

        file_name += "_"
        file_name += hashlib.md5(str(args).encode()).hexdigest()

        if "format" in args:
            file_name += "." + args["format"]

    return (url, file_name)


def _build_urls(endpoint: str, args: None | dict = None) -> pd.DataFrame:
    url = URL + API_VERSION + "/" + endpoint
    file_name = endpoint

    if args:
        # apikey will often be None when we're using a persistent session:
        args = {k: v for k, v in args.items() if v is not None}

        scalar_args = {k: v for k, v in args.items() if not isinstance(v, (list, tuple))}
        vector_args = {k: v for k, v in args.items() if isinstance(v, (list, tuple))}

        if vector_args:
            expanded_args = list(itertools.product(*vector_args.values()))
            expanded_args = [dict(zip(vector_args.keys(), values)) for values in expanded_args]
            queries = [
                _build_urls(endpoint, {**arg, **scalar_args}).assign(**arg)
                for arg in expanded_args
            ]
            return pd.concat(queries, ignore_index=True)

        url += "?"
        url += urllib.parse.urlencode(scalar_args, safe=",")

        # apikey doesn't influence the file contents, so shouldn't be in the hash:
        if "apikey" in args:
            del args["apikey"]

        file_name += "_"
        file_name += hashlib.md5(str(args).encode()).hexdigest()

        if "format" in args:
            file_name += "." + args["format"]

    return pd.DataFrame([{"query": url, "file_name": file_name}])


def _validate_date(date: str | datetime.datetime) -> str:
    if isinstance(date, str) and date == "-today":
        date = datetime.datetime.today()

    if isinstance(date, datetime.datetime):
        date = date.strftime("%Y-%m-%d")

    # ENHANCEMENT: accept other date formats like numpy datetime64, pandas Timestamp, etc
    # ENHANCEMENT: make sure date is properly formatted

    return date


def get_model_version() -> str:
    """Get the current default model version.

    Returns:
        str: The current model version

    """
    return MODEL_VERSION


def set_model_version(version: str) -> None:
    """Set the default model version.

    Args:
        version (str): The model version to set

    """
    assert version in MODEL_VERSIONS
    global MODEL_VERSION
    MODEL_VERSION = version
