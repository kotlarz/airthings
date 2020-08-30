import logging
import struct

import bluepy.btle as btle

from .constants import (
    ALARM_OPERATOR_EQUAL,
    ALARM_OPERATOR_GREATER_THAN,
    ALARM_OPERATOR_GREATER_THAN_OR_EQUAL,
    ALARM_OPERATOR_LESS_THAN,
    ALARM_OPERATOR_LESS_THAN_OR_EQUAL,
    ALARM_OPERATOR_NOT_EQUAL,
    ALARM_SEVERITY_UNKNOWN,
    DEFAULT_BLUETOOTH_ADDRESS_TYPE,
    DEFAULT_BLUETOOTH_INTERFACE,
)
from .devices import DEVICE_MODELS
from .exceptions import (
    AirthingsModelNotImplementedException,
    CouldNotDetermineAlarmSeverityException,
)

_LOGGER = logging.getLogger(__name__)


def determine_alarm_severity(alarm_rules, value):
    from .models import Alarm

    if alarm_rules is None:
        # TODO: exception?
        return None

    for alarm_rule in alarm_rules:
        severity = alarm_rule["severity"]
        rules = alarm_rule["rules"]
        required_matches = len(rules)

        matches = 0
        for rule in rules:
            matched_rule = None
            rule_operator = rule["operator"]
            rule_value = rule["value"]
            if rule_operator == ALARM_OPERATOR_EQUAL:
                if value == rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_NOT_EQUAL:
                if value != rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_GREATER_THAN:
                if value > rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_LESS_THAN:
                if value < rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_GREATER_THAN_OR_EQUAL:
                if value >= rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_LESS_THAN_OR_EQUAL:
                if value <= rule_value:
                    matched_rule = rule

            if matched_rule:
                matches += 1

        if matches >= required_matches:
            return Alarm(severity=severity, value=value, rules=rules)
    else:
        # TODO:?
        """
        if matched_rule is None:
            raise CouldNotDetermineAlarmSeverityException(severity, value, rules)

        """
        _LOGGER.warning(
            "Setting severity to unknown. Could not determine alarm severity for value: {}, and alarm_rules: {}".format(
                value, alarm_rules
            )
        )
        return Alarm(severity=ALARM_SEVERITY_UNKNOWN, value=value)


def fetch_characteristic(peripheral, uuid):
    if peripheral is None:
        raise ValueError("Peripheral cannot be None")
    characteristics = peripheral.getCharacteristics(uuid=uuid)
    if len(characteristics) != 1:
        raise ValueError("fetch_characteristic did not return exactly 1 characteristic")
    characteristic = characteristics[0]
    return characteristic.read()


def determine_device_from_mac_address(
    mac_address,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    _LOGGER.debug(
        "Attempting to determine device model class from MAC address: {}".format(
            mac_address
        )
    )

    peripheral = btle.Peripheral(mac_address, iface=iface, addrType=address_type)
    # First 4 digits of the serial number
    model_number = fetch_characteristic(
        peripheral, btle.AssignedNumbers.modelNumberString
    ).decode("utf-8")
    # Last 6 digits of the serial number
    identifier = fetch_characteristic(
        peripheral, btle.AssignedNumbers.serialNumberString
    ).decode("utf-8")

    # 10 digits
    serial_number = model_number + identifier

    device_class = determine_device_class_from_serial_number(serial_number)

    return device_class(mac_address, serial_number, peripheral=peripheral)


def determine_device_class_from_serial_number(serial_number):
    _LOGGER.debug(
        "Attempting to determine device model class from serial number: {}".format(
            serial_number
        )
    )

    model_number = serial_number[:4]

    return determine_device_class_from_model_number(model_number)


def determine_device_class_from_model_number(model_number):
    _LOGGER.debug(
        "Attempting to determine device model class from model number: {}".format(
            model_number
        )
    )

    for device_class in DEVICE_MODELS:
        if model_number == device_class.MODEL_NUMBER:
            return device_class
    else:
        _LOGGER.warning(
            "Could not determine Airthings model from model number: {}. Most likely an unimplemented model, or not an Airthings device.".format(
                model_number
            )
        )
        raise AirthingsModelNotImplementedException(model_number)


def determine_device(dev):
    mac_address = dev.addr
    manufacturer_data = dev.getValue(btle.ScanEntry.MANUFACTURER)
    serial_number = parse_manufacturer_data(manufacturer_data)
    if serial_number is None:
        # Not a Airthings device
        return None
    serial_number = str(serial_number)
    device_class = determine_device_class_from_serial_number(serial_number)
    return device_class(mac_address, serial_number)


def parse_manufacturer_data(manufacturer_data):
    try:
        (idx, serial_number, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:
        return None
    else:
        if idx == 0x0334:
            return serial_number
