import logging
import struct

import bluepy.btle as btle

from .devices import DEVICE_MODELS
from .exceptions import (
    AirthingsModelNotImplementedException,
    CouldNotDetermineAlarmSeverityException,
)
from .constants import (
    ALARM_SEVERITY_UNKNOWN,
    ALARM_SEVERITY_UNKNOWN,
    ALARM_OPERATOR_EQUAL,
    ALARM_OPERATOR_NOT_EQUAL,
    ALARM_OPERATOR_GREATER_THAN,
    ALARM_OPERATOR_LESS_THAN,
    ALARM_OPERATOR_GREATER_THAN_OR_EQUAL,
    ALARM_OPERATOR_LESS_THAN_OR_EQUAL,
)

_LOGGER = logging.getLogger(__name__)


def determine_alarm_severity(alarm_rules, value):
    from .models import Alarm

    if alarm_rules is None:
        # TODO: exception?
        return None

    print("=" * 32)
    print("ALARM RULES:", alarm_rules)

    for alarm_rule in alarm_rules:
        print("*" * 48)
        severity = alarm_rule["severity"]
        rules = alarm_rule["rules"]
        required_matches = len(rules)

        print(severity, rules)

        matches = 0
        for rule in rules:
            matched_rule = None
            rule_operator = rule["operator"]
            rule_value = rule["value"]
            print(value, rule_operator, rule_value)
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
                if value > rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_GREATER_THAN_OR_EQUAL:
                if value >= rule_value:
                    matched_rule = rule
            elif rule_operator == ALARM_OPERATOR_LESS_THAN_OR_EQUAL:
                if value <= rule_value:
                    matched_rule = rule

            if matched_rule:
                matches += 1

            print("MATCHES", matches, required_matches)

        if matches == required_matches:
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


"""

    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{ALARM_RULE_GREATER_THAN_OR_EQUAL: 70,}],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [{ALARM_RULE_GREATER_THAN_OR_EQUAL: 60,}, {ALARM_RULE_LESS_THAN: 70,}],
    },

# Alarm rules
ALARM_RULE_EQUAL = "equal"
ALARM_RULE_NOT_EQUAL = "not_equal"
ALARM_RULE_GREATER_THAN = "greater_than"
ALARM_RULE_LESS_THAN = "less_than"
ALARM_RULE_GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
ALARM_RULE_LESS_THAN_OR_EQUAL = "less_than_or_equal"

    # Alarm severity levels
    ALARM_SEVERITY_HIGH = "high"
    ALARM_SEVERITY_HIGH_COLOR = "red"
    ALARM_SEVERITY_MEDIUM = "medium"
    ALARM_SEVERITY_MEDIUM_COLOR = "orange"
    ALARM_SEVERITY_LOW = "low"
    ALARM_SEVERITY_LOW_COLOR = "yellow"
    ALARM_SEVERITY_CAUTION = "low"
    ALARM_SEVERITY_CAUTION_COLOR = "blue"
    ALARM_SEVERITY_NONE = "none"
    ALARM_SEVERITY_NONE_COLOR = None
"""


def fetch_characteristic(peripheral, uuid):
    if peripheral is None:
        raise ValueError("Peripheral cannot be None")
    characteristics = peripheral.getCharacteristics(uuid=uuid)
    if len(characteristics) != 1:
        raise ValueError("fetch_characteristic did not return exactly 1 characteristic")
    characteristic = characteristics[0]
    return characteristic.read()


def determine_device_from_mac_address(mac_address):
    _LOGGER.debug(
        "Attempting to determine device model class from MAC address: {}".format(
            mac_address
        )
    )

    peripheral = btle.Peripheral(mac_address)
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
