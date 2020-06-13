import struct

import bluepy.btle as btle

from .constants import (
    DEVICE_IDENTIFIER_LENGTH,
    DEVICE_MODEL_NUMBER_LENGTH,
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
)


class Sensor:
    KEY = None
    LABEL = None
    UNIT = None

    def __init__(self, value):
        self._value = value

    def __repr__(self):
        return repr("%s %s" % (self._value, self.unit))

    @property
    def key(self):
        return self.KEY

    @property
    def label(self):
        return self.LABEL

    @property
    def unit(self):
        return self.UNIT

    @property
    def value(self):
        return self._value


class Device:
    KEY = None
    MODEL_NUMBER = None
    LABEL = None
    RAW_DATA_FORMAT = None
    SENSOR_CAPABILITIES = {
        SENSOR_HUMIDITY_KEY: False,
        SENSOR_RADON_SHORT_TERM_AVG_KEY: False,
        SENSOR_RADON_LONG_TERM_AVG_KEY: False,
        SENSOR_TEMPERATURE_KEY: False,
        SENSOR_ATMOSPHERIC_PRESSURE_KEY: False,
        SENSOR_CO2_KEY: False,
        SENSOR_VOC_KEY: False,
    }

    def __init__(self, mac_address, serial_number):
        self._mac_address = mac_address
        self._serial_number = serial_number
        self._identifier = serial_number[-DEVICE_IDENTIFIER_LENGTH:]
        self._measurements = {}
        self._has_measurements = False

    def __repr__(self):
        return repr(
            "<Device mac_address=%s serial_number=%s model_number=%s model=%s>"
            % (self.mac_address, self.serial_number, self.model_number, self.LABEL,)
        )

    def _fetch_raw_data(self):
        periph = btle.Peripheral(self.mac_address)
        characteristics = periph.getCharacteristics(uuid=self.DATA_UUID)
        if len(characteristics) != 1:
            raise ValueError(
                "getCharacteristics did not return exactly 1 characteristic"
            )

        characteristic = characteristics[0]
        raw_data = characteristic.read()
        periph.disconnect()
        return raw_data

    def _parse_raw_data(self, raw_data):
        return struct.unpack(self.RAW_DATA_FORMAT, raw_data)

    def fetch_and_set_measurements(self):
        raw_data = self._fetch_raw_data()
        data = self._parse_raw_data(raw_data)
        # TODO: check sensor version
        self._parse_data(data)
        self._has_measurements = True

    @property
    def mac_address(self):
        return self._mac_address

    @mac_address.setter
    def mac_address(self, mac_address):
        self._mac_address = mac_address

    @property
    def serial_number(self):
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        self._serial_number = serial_number

    @property
    def identifier(self):
        return self._identifier

    @property
    def model_number(self):
        return self.MODEL_NUMBER

    @property
    def sensor_capabilities(self):
        return self.SENSOR_CAPABILITIES

    @property
    def has_measurements(self):
        return self._has_measurements

    @property
    def label(self):
        return self.LABEL

    @property
    def humidity(self):
        return self._measurements.get(SENSOR_HUMIDITY_KEY, None)

    @property
    def radon_short_term_avg(self):
        return self._measurements.get(SENSOR_RADON_SHORT_TERM_AVG_KEY, None)

    @property
    def radon_long_term_avg(self):
        return self._measurements.get(SENSOR_RADON_LONG_TERM_AVG_KEY, None)

    @property
    def temperature(self):
        return self._measurements.get(SENSOR_TEMPERATURE_KEY, None)

    @property
    def atmospheric_pressure(self):
        return self._measurements.get(SENSOR_ATMOSPHERIC_PRESSURE_KEY, None)

    @property
    def co2(self):
        return self._measurements.get(SENSOR_CO2_KEY, None)

    @property
    def voc(self):
        return self._measurements.get(SENSOR_VOC_KEY, None)
