# airthings

`airthings` is a simple python package that contains methods to communicate with [Airthings](https://airthings.com/) devices. The package utilizies [bluepy](https://github.com/IanHarvey/bluepy) for the communication between python and the devices. The package features can be found below.

_Note: Some features are currently undocumented, and parts are untested/not yet implemented._

## Features

- Autodiscover Airthings devices
- Find and search for Airthings devices by using MAC addresses and/or identifiers
- Fetch sensor measurements from various Airthings models, see sensor capability list below

## Requirements

The package has currently only been tested on Linux with the `Wave Plus Gen 1 (2930)`, other operating systems and device models should in theory work fine, but is untested.

### System requirements:

- libglib2.0-dev

## Supported devices

| Model number\* | Device label    | Sensor capabilites                                                                                                                                                                                                | Notes                                                                                                                                                    |
| -------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2900           | Wave Gen 1      | <ul><li>Humidity (%rH)</li><li>Radon short term average (Bp/m3)</li><li>Radon long term average (Bq/m3)</li><li>Temperature (°C)</li></ul>                                                                        | On 1st Gen Wave, temperature and humidity are updated every time we read the wave.                                                                       |
| 2920           | Wave Mini Gen 1 | <ul><li>Humidity (%rH)</li><li>Temperature (°C)</li><li>Atmospheric pressure (hPa)</li><li>VOC (ppb)</li></ul>                                                                                                    | Sensor values are updated every 5 minutes.                                                                                                               |
| 2930           | Wave Plus Gen 1 | <ul><li>Humidity (%rH)</li><li>Radon short term average (Bp/m3)</li><li>Radon long term average (Bq/m3)</li><li>Temperature (°C)</li><li>Atmospheric pressure (hPa)</li><li>CO2 (ppm)</li><li>VOC (ppb)</li></ul> | Except for the radon measurements, the Wave Plus updates its current sensor values once every 5 minutes. Radon measurements are updated once every hour. |
| 2940           | Wave Gen 2      | <ul><li>Humidity (%rH)</li><li>Radon short term average (Bp/m3)</li><li>Radon long term average (Bq/m3)</li><li>Temperature (°C)</li></ul>                                                                        | On 2nd Gen Wave, temperature and humidity are updated every 5 minutes. On both devices, radon measurements are updated once every hour.                  |

_\* Model number is the first 4 digits of the Airthings device_

## Installation

The current stable version of infrastructure-daigrams is available on pypi and can be installed by running:

`pip install airthings`

Other sources:

- pypi: http://pypi.python.org/pypi/airthings/
- github: https://github.com/kotlarz/airthings/

## Usage

Examples can be found in the [examples](./examples) directory.
