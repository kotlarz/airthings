import logging
import struct
import time

import bluepy.btle as btle

from .constants import (
    ALARM_SEVERITY_MAPPING,
    ALARM_SEVERITY_NONE,
    ALARM_SEVERITY_UNKNOWN,
    ALARM_SEVERITY_UNKNOWN_COLOR,
    ALARM_SEVERITY_UNKNOWN_LABEL,
    DEFAULT_BLUETOOTH_ADDRESS_TYPE,
    DEFAULT_BLUETOOTH_INTERFACE,
    DEFAULT_CONNECT_ATTEMPTS,
    DEFAULT_FETCH_ATTEMPTS,
    DEFAULT_RECONNECT_SLEEP,
    DEFAULT_REFETCH_SLEEP,
    DEVICE_MODEL_NUMBER_LENGTH,
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_CO2_KEY,
    SENSOR_HUMIDITY_KEY,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_SHORT_TERM_AVG_KEY,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_VOC_KEY,
)
from .exceptions import OutOfConnectAttemptsException, OutOfFetchAttemptsException

_LOGGER = logging.getLogger(__name__)


class Alarm:
    def __init__(self, severity, value, rules=None):
        self._severity = severity
        self._value = value
        self._rules = rules

        # Match the severity mapping and set color/label
        for alarm_severity, alarm_info in ALARM_SEVERITY_MAPPING.items():
            if alarm_severity == severity:
                self._label = alarm_info["label"]
                self._color = alarm_info["color"]
                break
        else:
            # TODO: raise exception?
            self._severity = ALARM_SEVERITY_UNKNOWN
            self._label = ALARM_SEVERITY_UNKNOWN_LABEL
            self._color = ALARM_SEVERITY_UNKNOWN_COLOR

    def __repr__(self):
        return repr("{} Alarm with value {}".format(self._label, self._value))

    @property
    def severity(self):
        return self._severity

    @property
    def value(self):
        return self._value

    @property
    def rules(self):
        return self._rules

    @property
    def label(self):
        return self._label

    @property
    def color(self):
        return self._color

    @property
    def is_important(self):
        return self.severity != ALARM_SEVERITY_NONE


class Sensor:
    KEY = None
    LABEL = None
    UNIT = None
    ALARM_RULES = None

    def __init__(self, value):
        from .utils import determine_alarm_severity

        self._value = value
        self._current_alarm = determine_alarm_severity(self.ALARM_RULES, value)

    def __repr__(self):
        return repr("{} {}".format(self._value, self.unit))

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
    def has_alarm_rules(self):
        return self.ALARM_RULES is not None

    @property
    def alarm_rules(self):
        return self.ALARM_RULES

    @property
    def has_alarm(self):
        return (
            self._current_alarm is not None
            and self._current_alarm.severity != ALARM_SEVERITY_NONE
        )

    @property
    def current_alarm(self):
        return self._current_alarm

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

    def __init__(
        self,
        mac_address,
        serial_number,
        peripheral=None,
        connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
        reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    ):
        self._mac_address = mac_address
        self._serial_number = serial_number
        self._identifier = serial_number[4:]
        self._measurements = {}
        self._has_measurements = False
        self._debug_information = None
        self._has_debug_information = False
        self._peripheral = peripheral
        self._connect_attempts = connect_attempts
        self._reconnect_sleep = reconnect_sleep

    def __repr__(self):
        return repr(
            "<Device mac_address={} serial_number={} model_number={} model={}>".format(
                self.mac_address, self.serial_number, self.model_number, self.LABEL
            )
        )

    def _connect(self):
        if self.is_connected:
            return
        current_retries = 0
        while True:
            try:
                if self._peripheral is not None:
                    # Try to disconnect from peripheral
                    try:
                        self._peripheral.disconnect()
                    except Exception as e:
                        _LOGGER.warning("Failed to disconnect from Peripheral")
                        _LOGGER.debug(e)

                self._peripheral = btle.Peripheral(
                    self.mac_address, iface=self._iface, addrType=self._address_type
                )
                break
            except btle.BTLEException as e:
                if current_retries == self._connect_attempts:
                    raise OutOfConnectAttemptsException(
                        self._connect_attempts, self._reconnect_sleep
                    )

                current_retries += 1

                _LOGGER.debug(type(e))
                _LOGGER.debug(e)
                _LOGGER.debug(
                    "device._connect failed, retrying connect in {} seconds... Current retries = {} out of {}".format(
                        self._reconnect_sleep, current_retries, self._connect_attempts
                    )
                )

                time.sleep(self._reconnect_sleep)

    def _disconnect(self):
        self._peripheral.disconnect()
        self._peripheral = None

    def _reconnect(self):
        try:
            self._disconnect()
        except Exception as e:
            _LOGGER.debug(e)
            _LOGGER.debug(
                "Failed to disconnect during device reconnect, ignoring and continuing..."
            )

        try:
            self._connect()
        except Exception as e:
            _LOGGER.debug(e)
            _LOGGER.debug("Failed to connect during device reconnect, ignoring...")

    def _fetch_characteristic(self, uuid):
        from .utils import fetch_characteristic

        current_retries = 0
        while True:
            try:
                return fetch_characteristic(self.connection, uuid)
            except btle.BTLEException as e:
                if current_retries == self._fetch_attempts:
                    raise OutOfFetchAttemptsException(
                        self._fetch_attempts, self._refetch_sleep
                    )

                current_retries += 1

                _LOGGER.debug(e)
                _LOGGER.debug(
                    "device._fetch_characteristic(uuid={}) failed, retrying connect in {} seconds... Current retries = {} out of {}".format(
                        uuid, self._refetch_sleep, current_retries, self._fetch_attempts
                    )
                )

                if isinstance(e, btle.BTLEDisconnectError):
                    _LOGGER.debug(
                        "Exception is a disconnect error, attempting a hard reconnect"
                    )
                    self._reconnect()

                time.sleep(self._refetch_sleep)

    def _fetch_and_set_debug_information(self):
        self._debug_information["firmware_revision"] = self._fetch_characteristic(
            btle.AssignedNumbers.firmwareRevisionString
        )
        self._debug_information["hardware_revision"] = self._fetch_characteristic(
            btle.AssignedNumbers.hardwareRevisionString
        )
        self._disconnect()

    def _fetch_raw_data(self):
        self._connect()
        raw_data = self._fetch_characteristic(self.DATA_UUID)
        self._disconnect()
        return raw_data

    def _parse_raw_data(self, raw_data):
        return struct.unpack(self.RAW_DATA_FORMAT, raw_data)

    def fetch_and_set_measurements(
        self,
        connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
        reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
        fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
        refetch_sleep=DEFAULT_REFETCH_SLEEP,
        iface=DEFAULT_BLUETOOTH_INTERFACE,
        address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
    ):
        _LOGGER.debug("Fetching measurements from device:")
        _LOGGER.debug(self)
        self._connect_attempts = connect_attempts
        self._reconnect_sleep = reconnect_sleep
        self._fetch_attempts = fetch_attempts
        self._refetch_sleep = refetch_sleep
        self._iface = iface
        self._address_type = address_type
        self._connect()
        raw_data = self._fetch_raw_data()
        data = self._parse_raw_data(raw_data)
        # TODO: check sensor version
        self._parse_data(data)
        self._has_measurements = True

        # Check for alarms
        for measurement, sensor in self.measurements.items():
            if not sensor.has_alarm_rules:
                _LOGGER.debug(
                    "Sensor {} does not have alarm rules, skipping".format(sensor.label)
                )
                continue
            elif not sensor.has_alarm:
                # No alarm triggering
                _LOGGER.debug(
                    "Sensor {} does not have any alarms triggering, skipping".format(
                        sensor.label
                    )
                )
                continue

            _LOGGER.debug(
                "Sensor {} has an alarm triggering: {}".format(
                    sensor.label, sensor.current_alarm
                )
            )

        _LOGGER.debug("Fetched measurements!")
        _LOGGER.debug(self._measurements)

    @property
    def is_connected(self):
        """
        function: getState()
        Returns a string indicating device state. Possible states are:
            "conn" - connected,
            "disc" - disconnected
            "scan" scanning
            "tryconn" - connecting
        """
        if not self._peripheral:
            return False

        try:
            return self._peripheral.getState() != "disc"
        except IOError as e:
            _LOGGER.warning(
                "IOError no {} whilst checking if the device is connected, assuming it's not connected".format(
                    e.errno
                )
            )
            _LOGGER.debug(e)
        except btle.BTLEException as e:
            _LOGGER.warning(
                "BTLE exception whilst checking if the device is connected, assuming it's not connected"
            )
            _LOGGER.debug(e)

        except Exception as e:
            _LOGGER.warning(
                "Generic exception whilst checking if the device is connected, assuming it's not connected"
            )
            _LOGGER.debug(e)

        return False

    @property
    def connection(self):
        if not self.is_connected:
            self._connect()
        return self._peripheral

    @property
    def debug_information(self):
        if not self._has_debug_information:
            self._fetch_and_set_debug_information()
            self._has_debug_information = True
        return self._debug_information

    @property
    def identifier(self):
        return self._identifier

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
    def measurements(self):
        return self._measurements

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
