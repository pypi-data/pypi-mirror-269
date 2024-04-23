
# Intended Use

The Salient SDK is a python convenience wrapper around Salient Predictions' customer-facing  
[web API](https://api.salientpredictions.com/v2/documentation/api/).  It also contains utility functions for manipulating and analyzing the data delivered from the API.

# Setting up the SDK

## Prerequisites 

The Salient SDK requires Python 3.11 to use.   If you have Python installed, you can check your version with:

```bash
python3 --version
```

To get version 3.11:

```bash
# Ubuntu:
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
```

```bash
# macOS:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew update
brew install python@3.11
```

## Installing the SDK

The easiest way to get the Salient SDK is to install it like any other package:

```bash
pip install salientsdk --upgrade
# to verify version with
pip show salientsdk
```

# Usage

## Command Line

The Salient SDK contains a full command line interface that can access each of the primary
API functions without even opening python.  You can get help for all options or specific commands:

```bash
python3 -m salientsdk --help
python3 -m salientsdk forecast_timeseries --help
```

To verify that you are set up to execute the sdk, ask for its version number:

```bash
python3 -m salientsdk version
```

To verify that you can access Salient's API, use the limited universal credentials `testusr` and `testpwd` to log in:

```bash
python3 -m salientsdk login -u testusr -p testpwd
```

To verify that you can download data from Salient, try the `testusr/testpwd` credentials to download historical data with the `data_timeseries` function.  This will download a NetCDF file to your current directory and display its contents.

```bash
python3 -m salientsdk data_timeseries -lat 42 -lon -73 -fld all --start 2020-01-01 --end 2020-12-31 -u testusr -p testpwd
```

To test that your specific Salient-issued credentials are functioning properly, try them with the `forecast_timeseries` function.  Replace `username` and `password` in the example below with your credentials.  Note that you may need to change the location (North America) and timescale (seasonal) if your license does not include them.

```bash
python3 -m salientsdk forecast_timeseries -lat 42 -lon -73 --variable precip --timescale seasonal --date 2020-01-01 -u username -p password
```



## Via Python

In a python 3.11 script, this example code will login and request a historical ERA5 data timeseries.

```python
import salientsdk as sk
import xarray as xr
import netcdf4

session = sk.login("testusr","testpwd")
history = sk.data_timeseries(loc = Location(lat=42, lon=-73), field="all", variable="temp", session=session)
print(xr.open_file(history))
```

Note that this example uses the limited credentials `testusr` and `testpwd`.  To access the full capabilities of your license, use your Salient-provided credentials.

See all available functions in the [API Reference](api.md).

The [examples](https://github.com/Salient-Predictions/salientsdk/tree/main/examples) directory contains `ipynb` notebooks to help you get started with common operations. 

# License

This SDK is licensed for use by Salient customers [details](https://salient-predictions.github.io/salientsdk/LICENSE/).


Copyright 2024 [Salient Predictions](https://www.salientpredictions.com/)
