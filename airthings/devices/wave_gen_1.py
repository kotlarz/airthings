import bluepy.btle as btle

from airthings.constants import (
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
    WAVE_GEN_1_KEY,
    WAVE_GEN_1_LABEL,
    WAVE_GEN_1_MODEL_NUMBER,
    WAVE_GEN_1_RAW_DATA_FORMAT,
    WAVE_GEN_1_UUID_DATETIME,
    WAVE_GEN_1_UUID_HUMIDITY,
    WAVE_GEN_1_UUID_RADON_LONG_TERM_AVERAGE,
    WAVE_GEN_1_UUID_RADON_SHORT_TERM_AVERAGE,
    WAVE_GEN_1_UUID_TEMPERATURE,
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


class WaveGen1(Device):
    """
    On 1st Gen Wave, temperature and humidity are updated every time we read the wave.
    Radon measurements are updated once every hour.
    """

    KEY = WAVE_GEN_1_KEY
    MODEL_NUMBER = WAVE_GEN_1_MODEL_NUMBER
    LABEL = WAVE_GEN_1_LABEL
    RAW_DATA_FORMAT = WAVE_GEN_1_RAW_DATA_FORMAT
    UUID_DATETIME = btle.UUID(WAVE_GEN_1_UUID_DATETIME)
    UUID_HUMIDITY = btle.UUID(WAVE_GEN_1_UUID_HUMIDITY)
    UUID_TEMPERATURE = btle.UUID(WAVE_GEN_1_UUID_TEMPERATURE)
    UUID_RADON_STA = btle.UUID(WAVE_GEN_1_UUID_RADON_SHORT_TERM_AVERAGE)
    UUID_RADON_LTA = btle.UUID(WAVE_GEN_1_UUID_RADON_LONG_TERM_AVERAGE)
    SENSOR_CAPABILITIES = {
        SENSOR_HUMIDITY_KEY: True,
        SENSOR_RADON_SHORT_TERM_AVG_KEY: True,
        SENSOR_RADON_LONG_TERM_AVG_KEY: True,
        SENSOR_TEMPERATURE_KEY: True,
        SENSOR_ATMOSPHERIC_PRESSURE_KEY: False,
        SENSOR_CO2_KEY: False,
        SENSOR_VOC_KEY: False,
    }

    def _fetch_raw_data(self, connect_retries=3):
        self._connect(connect_retries)
        raw_data = self._fetch_characteristic(self.UUID_DATETIME)
        raw_data += self._fetch_characteristic(self.UUID_HUMIDITY)
        raw_data += self._fetch_characteristic(self.UUID_TEMPERATURE)
        raw_data += self._fetch_characteristic(self.UUID_RADON_STA)
        raw_data += self._fetch_characteristic(self.UUID_RADON_LTA)
        self._disconnect()
        return raw_data

    def _parse_data(self, data):
        self._measurements[SENSOR_HUMIDITY_KEY] = HumiditySensor(data[6] / 100.0)
        self._measurements[SENSOR_TEMPERATURE_KEY] = TemperatureSensor(data[7] / 100.0)
        self._measurements[
            SENSOR_RADON_SHORT_TERM_AVG_KEY
        ] = RadonShortTermAverageSensor(parse_radon_data(data[8]))
        self._measurements[SENSOR_RADON_LONG_TERM_AVG_KEY] = RadonLongTermAverageSensor(
            parse_radon_data(data[9])
        )
