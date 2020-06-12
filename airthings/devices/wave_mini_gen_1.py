import bluepy.btle as btle

from airthings.constants import (
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
    WAVE_MINI_GEN_1_KEY,
    WAVE_MINI_GEN_1_LABEL,
    WAVE_MINI_GEN_1_MODEL_NUMBER,
    WAVE_MINI_GEN_1_RAW_DATA_FORMAT,
    WAVE_MINI_GEN_1_UUID_DATA,
)
from airthings.models import Device
from airthings.sensors import (
    AtmosphericPressureSensor,
    HumiditySensor,
    TemperatureSensor,
    VOCSensor,
)

from .utils import parse_radon_data


class WaveMiniGen1(Device):
    """
    Sensor values are updated every 5 minutes.
    """

    KEY = WAVE_MINI_GEN_1_KEY
    MODEL_NUMBER = WAVE_MINI_GEN_1_MODEL_NUMBER
    LABEL = WAVE_MINI_GEN_1_LABEL
    RAW_DATA_FORMAT = WAVE_MINI_GEN_1_RAW_DATA_FORMAT
    DATA_UUID = btle.UUID(WAVE_MINI_GEN_1_UUID_DATA)
    SENSOR_CAPABILITIES = {
        SENSOR_HUMIDITY_KEY: True,
        SENSOR_RADON_SHORT_TERM_AVG_KEY: False,
        SENSOR_RADON_LONG_TERM_AVG_KEY: False,
        SENSOR_TEMPERATURE_KEY: True,
        SENSOR_ATMOSPHERIC_PRESSURE_KEY: False,
        SENSOR_CO2_KEY: False,
        SENSOR_VOC_KEY: True,
    }

    def _parse_data(self, data):
        self._measurements[SENSOR_TEMPERATURE_KEY] = TemperatureSensor(
            round(data[1] / 100.0 - 273.15, 2)
        )
        self._measurements[SENSOR_HUMIDITY_KEY] = HumiditySensor(data[3] / 100.0)
        self._measurements[SENSOR_VOC_KEY] = VOCSensor(data[4])
