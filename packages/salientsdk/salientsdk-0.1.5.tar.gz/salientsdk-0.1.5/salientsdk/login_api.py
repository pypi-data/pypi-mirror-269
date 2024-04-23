#!/usr/bin/env python
# Copyright Salient Predictions 2024

"""Login to the Salient API.

Command line usage:
```
cd ~/salientsdk
python -m salientsdk login -u testusr -p testpwd
# or, to use api keys:
python -m salientsdk login --apikey testkey

```

"""

import argparse
import os
from concurrent.futures import ThreadPoolExecutor

import requests

from .constants import _build_url

try:
    from google.cloud import secretmanager
except ImportError as ie:
    # secretmanager is a convenience for internal Salient users.
    # Not needed for customer use.
    pass


VERFY_SSL = True

CURRENT_SESSION = None

API_KEY = None


def get_api_key() -> str | None:
    """Get the current API key.

    All calls to the Salient API have an `api_key` argument
    that defaults to call this function. In most cases, users
    will never need to call it explicitly.

    Returns:
        str: The current API key, or `None` if one is not set.

    """
    return API_KEY


def set_api_key(apikey: str | None) -> str | None:
    """Set the current API key.

    Sets the default value to be used when calling
    `apikey = get_api_key()`.

    Args:
        apikey (str | None): The API key that will be returned by `get_api_key()`.
            Special value `testkey` will use a universal key with limited permissions.
            Value `None` will clear the stored API key.

    Returns:
        str | None: The API key that was set
    """
    if apikey == "apikey":
        apikey_path = "projects/forecast-161702/secrets/API_TEST_USER_KEY/versions/1"
        try:
            apikey = (
                secretmanager.SecretManagerServiceClient()
                .access_secret_version(request={"name": apikey_path})
                .payload.data.decode("UTF-8")
            )
        except Exception as e:
            raise ValueError("Supply your Salient api key")

    elif apikey == "testkey":
        # https://api.salientpredictions.com/accounts/testing
        apikey = "950d43ac7571d8a8"

    global API_KEY
    API_KEY = apikey

    return apikey


def get_current_session() -> None | requests.Session:
    """Get the current session.

    All calls to the Salient API have a `session` argument
    that defaults to call this function. In most cases, users
    will never need to call it explicitly since it will be
    set during `login()`.

    Returns:
        requests.Session: The current session, or a temporary
            one for use with `apikey`.
    """
    return requests.Session() if CURRENT_SESSION is None else CURRENT_SESSION


def set_current_session(session: requests.Session | None) -> None:
    """Set the current session.

    This function is called internally as a side effect of
    `login()`. In most cases, users will never need
    to call it explicitly.

    Args:
        session (requests.Session | None): The session that will be
              returned by `get_current_session()`.  Set `None` to
              clear the session.

    """
    assert session is None or isinstance(session, requests.Session)

    global CURRENT_SESSION
    CURRENT_SESSION = session


def get_verify_ssl() -> bool:
    """Get the current SSL verification setting.

    All functions that call the Salient API have a
    `verify` argument that controls whether or not to use
    SSL verification when making the call.  That argument
    will default to use this function, so in most cases
    users will never need to call it.

    Returns:
        bool: The current SSL verification setting

    """
    return VERFY_SSL


def set_verify_ssl(verify: bool) -> None:
    """Set the SSL verification setting.

    Sets the default value to be used when calling
    `verify = get_verify_ssl()` in most API calls.
    This is usually set automatically as a side
    effect of `login(..., verify=None)` so in most
    cases users will never need to call it.

    Args:
        verify (bool): The SSL verification setting
           that will be returned by `get_verify_ssl()`.

    """
    global VERFY_SSL
    VERFY_SSL = verify


def login(
    username: str = "username",
    password: str = "password",
    apikey: str | None = None,
    verify: bool | None = None,
    verbose=False,
) -> requests.Session | None:
    """Login to the Salient API.

    This function is a local convenience wrapper around the Salient API
    [login](https://api.salientpredictions.com/v2/documentation/api/#/Authentication/login)
    endpoint.  It will use your credentials to create a persistent session you
    can use to execute API calls.

    Args:
        username (str): The username to login with
        password (str): The password to login with
        apikey (str | None): The API key to use instead of a login.
            If `None` (default) uses `username` and `password` to create a `Session`.
            If specified, sets the default key to use with `set_api_key()`, ignores
            `username` and `password`, does not create a `Session`.
        verify (bool): Whether to verify the SSL certificate.
            If `None` (default) will try `True` and then `False`, remembering the
            last successful setting and preserving it for future calls in `get_verify_ssl()`.
        verbose (bool): Whether to print the response status

    Returns:
        Session | None: Session object to pass to other API calls.
            As a side effect, will also set the default session for
            use with `get_current_session()`
            Returns `None` if called with `apikey`
    """
    if apikey is not None:
        set_api_key(apikey)
        set_current_session(None)  # clear out existing session, if there is one
        session = get_current_session()  # temporary
        if verbose:
            print(f"Using API key {apikey} with a temporary Session {session}.")
        return session

    if username == "username" and password == "password":
        password_path = "projects/forecast-161702/secrets/API_TEST_USER_PWD/versions/1"
        try:
            password = (
                secretmanager.SecretManagerServiceClient()
                .access_secret_version(request={"name": password_path})
                .payload.data.decode("UTF-8")
            )
        except Exception as e:
            raise ValueError("Supply your Salient username and password")
        username = "testuser@salientpredictions.com"

    elif username == "testusr" and password == "testpwd":
        # https://api.salientpredictions.com/accounts/testing
        username = "help+test@salientpredictions.com"
        password = "salty!"

    if verify is None:
        try:
            session = login(username, password, verify=True, verbose=verbose)
            set_verify_ssl(True)
        except requests.exceptions.SSLError:
            session = login(username, password, verify=False, verbose=verbose)
            set_verify_ssl(False)
        return session

    auth = (username, password)
    (url, file_name) = _build_url("login")

    session = requests.Session()
    login_ok = session.get(url, auth=auth, verify=verify)
    login_ok.raise_for_status()

    if verbose:
        print(login_ok.text)

    set_current_session(session)
    # Now that we have successfully created a session, make sure we don't preempt it:
    set_api_key(None)

    return session


def download_queries(
    query: list[str],
    file_name: list[str],
    format: str = "-auto",
    force: bool = False,
    session: requests.Session = get_current_session(),
    verify: bool = get_verify_ssl(),
    verbose: bool = False,
) -> None:
    """Downloads multiple queries saves them to a file.

    This function handles the downloading of data based on the provided query URLs.
    It saves the data to the specified file names.
    If the file already exists and `force` is not set to True, the download is skipped.
    Download will happen in parallel.

    Parameters:
        query (list[str]): The URLs from which to download the data.
        file_name (list[str]): The paths where the data will be saved.
        format (str, optional): The format of the file.
            Defaults to '-auto', which will infer the format from the file extension.
        force (bool, optional): If True, the file will be downloaded even if it already exists.
            Defaults to False.
        session (requests.Session, optional): The session to use for the download.
            Defaults to the current session via `get_current_session()`.
        verify (bool, optional): Whether to verify the server's TLS certificate.
            Defaults to the current verification setting via `get_verify_ssl()`.
        verbose (bool, optional): If True, prints additional output about the download process.
            Defaults to False.


    Raises:
        requests.HTTPError: If the server returns an error status code.
    """
    assert len(query) == len(file_name)

    if len(query) == 0:
        return None
    elif len(query) == 1:
        # Much of the time we won't have vectorized queries.  Keep it simple.
        download_query(query[0], file_name[0], format, force, session, verify, verbose)
        return None

    # max_workers defaults to os.cpu_count() * 5
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(download_query, qry, fil, format, force, session, verify, verbose)
            for qry, fil in zip(query, file_name)
        ]
        for future in futures:
            future.result()  # raises exceptions

    return None


def download_query(
    query: str,
    file_name: str,
    format: str = "-auto",
    force: bool = False,
    session: requests.Session = get_current_session(),
    verify: bool = get_verify_ssl(),
    verbose: bool = False,
) -> [requests.Response | None]:
    """Downloads the query result and saves it to a file.

    This function handles the downloading of data based on the provided query URL.
    It saves the data to the specified file name.
    If the file already exists and `force` is not set to True, the download is skipped.

    Parameters:
        query (str): The URL from which to download the data.
        file_name (str): The path where the data will be saved.
        format (str, optional): The format of the file.
            Defaults to '-auto', which will infer the format from the file extension.
        force (bool, optional): If True, the file will be downloaded even if it already exists.
            Defaults to False.
        session (requests.Session, optional): The session to use for the download.
            Defaults to the current session via `get_current_session()`.
        verify (bool, optional): Whether to verify the server's TLS certificate.
            Defaults to the current verification setting via `get_verify_ssl()`.
        verbose (bool, optional): If True, prints additional output about the download process.
            Defaults to False.

    Returns:
        requests.Response | None: The response object from the server after attempting the download,
            or None if the file was already cached and not re-downloaded.

    Raises:
        requests.HTTPError: If the server returns an error status code.
    """
    if format == "-auto":
        # extract the file extension from the file name
        format = file_name.split(".")[-1]

    result = None
    if force or not os.path.exists(file_name):
        if verbose:
            print(f"Downloading\n  {query}\n to {file_name}\n with {session}")
        result = session.get(query, verify=verify)
        result.raise_for_status()
        with open(file_name, "wb" if format == "nc" else "w") as f:
            if format == "nc":
                f.write(result.content)
            else:
                f.write(result.text)
    elif verbose:
        print(f"File {file_name} already exists")

    return result
