# airthings

`airthings` is a simple python package that contains methods to communicate with Airthings[1] devices. The package utilizies bluepy[2] for the communication between python and the devices. The package features can be found below.

- [1] https://airthings.com/
- [2] https://github.com/IanHarvey/bluepy

_Note: Some features are currently undocumented, and parts are untested/not yet implemented._

## Features

- Autodiscover Airthings devices
- Find and search for Airthings devices by using MAC addresses and/or identifiers
- Fetch sensor measurements from various Airthings models, see sensor capability list below

## Requirements

The package has currently only been tested on Linux with the `Wave Plus Gen 1 (2930)`, other operating systems and device models should in theory work fine, but is untested.

### System requirements:

- libglib2.0-dev

## Installation

The current stable version of infrastructure-daigrams is available on pypi and can be installed by running:

`pip install airthings`

Other sources:

- pypi: http://pypi.python.org/pypi/airthings/
- github: https://github.com/kotlarz/airthings/

## Usage

Examples can be found in the [examples](./examples) directory.

## Supported devices

_Note: "Model number" are the first 4 digits of the Airthings device_

### Wave Gen 1 (Model number: 2900)

On 1st Gen Wave, temperature and humidity are updated every time we read the wave.

#### Sensor capabilities

- Humidity (%rH)
- Radon short term average (Bp/m3)
- Radon long term average (Bq/m3)
- Temperature (°C)

### Wave Mini Gen 1 (Model number: 2920)

Sensor values are updated every 5 minutes.

#### Sensor capabilities

- Humidity (%rH)
- Temperature (°C)
- Atmospheric pressure (hPa)
- VOC (ppb)

### Wave Plus Gen 1 (Model number: 2930)

Except for the radon measurements, the Wave Plus updates its current sensor values once every 5 minutes. Radon measurements are updated once every hour.

#### Sensor capabilities

- Humidity (%rH)
- Radon short term average (Bp/m3)
- Radon long term average (Bq/m3)
- Temperature (°C)
- Atmospheric pressure (hPa)
- CO2 (ppm)
- VOC (ppb)

### Wave Gen 2 (Model number: 2950)

On 2nd Gen Wave, temperature and humidity are updated every 5 minutes. On both devices, radon measurements are updated once every hour.

#### Sensor capabilities

- Humidity (%rH)
- Radon short term average (Bp/m3)
- Radon long term average (Bq/m3)
- Temperature (°C)
