import struct

import bluepy.btle as btle

from airthings.constants import (
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
    WAVE_PLUS_GEN_1_KEY,
    WAVE_PLUS_GEN_1_LABEL,
    WAVE_PLUS_GEN_1_MODEL_NUMBER,
    WAVE_PLUS_GEN_1_RAW_DATA_FORMAT,
    WAVE_PLUS_GEN_1_UUID_DATA,
)
from airthings.models import Device
from airthings.sensors import (
    AtmosphericPressureSensor,
    CO2Sensor,
    HumiditySensor,
    RadonLongTermAverageSensor,
    RadonShortTermAverageSensor,
    TemperatureSensor,
    VOCSensor,
)

from .utils import parse_radon_data


class WavePlusGen1(Device):
    """
    Except for the radon measurements, the Wave Plus updates its current sensor values once every 5 minutes. Radon measurements are updated once every hour.
    """

    KEY = WAVE_PLUS_GEN_1_KEY
    MODEL_NUMBER = WAVE_PLUS_GEN_1_MODEL_NUMBER
    LABEL = WAVE_PLUS_GEN_1_LABEL
    RAW_DATA_FORMAT = WAVE_PLUS_GEN_1_RAW_DATA_FORMAT
    DATA_UUID = btle.UUID(WAVE_PLUS_GEN_1_UUID_DATA)
    SENSOR_CAPABILITIES = {
        SENSOR_HUMIDITY_KEY: True,
        SENSOR_RADON_SHORT_TERM_AVG_KEY: True,
        SENSOR_RADON_LONG_TERM_AVG_KEY: True,
        SENSOR_TEMPERATURE_KEY: True,
        SENSOR_ATMOSPHERIC_PRESSURE_KEY: True,
        SENSOR_CO2_KEY: True,
        SENSOR_VOC_KEY: True,
    }

    def _parse_data(self, data):
        self._measurements[SENSOR_HUMIDITY_KEY] = HumiditySensor(data[1] / 2.0)
        self._measurements[
            SENSOR_RADON_SHORT_TERM_AVG_KEY
        ] = RadonShortTermAverageSensor(parse_radon_data(data[4]))
        self._measurements[SENSOR_RADON_LONG_TERM_AVG_KEY] = RadonLongTermAverageSensor(
            parse_radon_data(data[5])
        )
        self._measurements[SENSOR_TEMPERATURE_KEY] = TemperatureSensor(data[6] / 100.0)
        self._measurements[SENSOR_ATMOSPHERIC_PRESSURE_KEY] = AtmosphericPressureSensor(
            data[7] / 50.0
        )
        self._measurements[SENSOR_CO2_KEY] = CO2Sensor(data[8] * 1.0)
        self._measurements[SENSOR_VOC_KEY] = VOCSensor(data[9] * 1.0)
