# Examples

Various examples on how to use the framework.

## Discovery

### Autodiscover all Airthings devices ([autodiscover_devices.py](./examples/autodiscover_devices.py))

`$ python examples/autodiscover_devices.py`

```bash
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: False
	Humidity: None
	Sensor capabilities:
	 humidity = YES
	 radon_short_term_avg = YES
	 radon_long_term_avg = YES
	 temperature = YES
	 atmospheric_pressure = YES
	 co2 = YES
	 voc = YES
```

### Finding Airthings devices by MAC addresses ([find_devices_by_mac_addresses.py](./examples/find_devices_by_mac_addresses.py))

`$ python examples/find_devices_by_mac_addresses.py`

```bash
Found Airthings device
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
```

### Finding Airthings devices by identifiers ([find_devices_by_identifiers.py](./examples/find_devices_by_identifiers.py))

_Identifiers are the last 6 digits of the serial number_

`$ python examples/find_devices_by_identifiers.py`

```bash
Found Airthings device
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
```

## Measurements

### Autodiscover and fetch measurements of all nearby Airthings devices ([fetch_measurements.py](./examples/fetch_measurements.py))

`$ python examples/fetch_measurements.py`

```bash
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Measurements +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.45 °C
	 1002.3 hPa
	 485.0 ppm
	 65.0 ppb
```

### Fetch measurement of Airthings devices specified by MAC addresses ([fetch_measurements_from_mac_addresses.py](./examples/fetch_measurements_from_mac_addresses.py))

_Identifiers are the last 6 digits of the serial number_

`$ python examples/fetch_measurements_from_identifiers.py`

```bash
Found Airthings device
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Measurements +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.45 °C
	 1002.3 hPa
	 485.0 ppm
	 65.0 ppb
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Measurements +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.45 °C
	 1002.3 hPa
	 485.0 ppm
	 65.0 ppb
```

### Fetch measurement of Airthings devices specified by identifiers ([fetch_measurements_from_identifiers.py](./examples/fetch_measurements_from_identifiers.py))

_Identifiers are the last 6 digits of the serial number_

`$ python examples/fetch_measurements_from_identifiers.py`

```bash
Found Airthings device
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Measurements +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.45 °C
	 1002.3 hPa
	 485.0 ppm
	 65.0 ppb
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Measurements +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.45 °C
	 1002.3 hPa
	 485.0 ppm
	 65.0 ppb
```

## Miscellaneous

### Using sensor measurement variables ([sensor_variables.py](./examples/sensor_variables.py))

`$ python examples/sensor_variables.py`

```bash
Found 1 Airthings devices:
====================================
	MAC address: 00:81:f9:ff:ff:ff
	Identifier: xxxxxx
	Model: Wave Plus Gen 1
	Model number: 2930
	Has measurements: True
+++++++++++ Default +++++++++++
	 31.0 %rH
	 6 Bq/m3
	 5 Bq/m3
	 24.49 °C
	 1002.2 hPa
	 486.0 ppm
	 67.0 ppb
+++++++++++ Manual +++++++++++
	 Humidity : 31.0 %rH
	 Radon Short Term Average : 6 Bq/m3
	 Radon Long Term Average : 5 Bq/m3
	 Temperature : 24.49 °C
	 Atmospheric pressure : 1002.2 hPa
	 CO2 : 486.0 ppm
	 VOC : 67.0 ppb
```
