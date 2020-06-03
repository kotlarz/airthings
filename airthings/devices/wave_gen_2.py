import bluepy.btle as btle

from airthings.constants import (
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
    WAVE_GEN_2_KEY,
    WAVE_GEN_2_LABEL,
    WAVE_GEN_2_MODEL_NUMBER,
    WAVE_GEN_2_RAW_DATA_FORMAT,
    WAVE_GEN_2_UUID_DATA,
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


class WaveGen2(Device):
    """
    On 2nd Gen Wave, temperature and humidity are updated every 5 minutes.
    Radon measurements are updated once every hour.
    """

    KEY = WAVE_GEN_2_KEY
    MODEL_NUMBER = WAVE_GEN_2_MODEL_NUMBER
    LABEL = WAVE_GEN_2_LABEL
    RAW_DATA_FORMAT = WAVE_GEN_2_RAW_DATA_FORMAT
    DATA_UUID = btle.UUID(WAVE_GEN_2_UUID_DATA)
    SENSOR_CAPABILITIES = {
        SENSOR_HUMIDITY_KEY: True,
        SENSOR_RADON_SHORT_TERM_AVG_KEY: True,
        SENSOR_RADON_LONG_TERM_AVG_KEY: True,
        SENSOR_TEMPERATURE_KEY: True,
        SENSOR_ATMOSPHERIC_PRESSURE_KEY: False,
        SENSOR_CO2_KEY: False,
        SENSOR_VOC_KEY: False,
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
