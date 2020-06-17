import logging
import struct

import bluepy.btle as btle

from .devices import DEVICE_MODELS
from .exceptions import AirthingsModelNotImplementedException

_LOGGER = logging.getLogger(__name__)


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
