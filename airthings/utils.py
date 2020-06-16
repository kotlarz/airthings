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


def determine_device_model_from_mac_address(mac_address):
    peripheral = btle.Peripheral(mac_address)
    model_number = fetch_characteristic(
        peripheral, btle.AssignedNumbers.modelNumberString
    ).decode("utf-8")
    serial_number = fetch_characteristic(
        peripheral, btle.AssignedNumbers.serialNumberString
    ).decode("utf-8")
    model = determine_model_class(model_number)

    if not model:
        try:
            _LOGGER.warning(
                "Could not determine Airthings model from MAC address: %s. serial_number = %s"
                % (mac_address, serial_number)
            )
        except AirthingsModelNotImplementedException as e:
            raise e

    return model(mac_address, serial_number, peripheral=peripheral)


def determine_model_class(model_number):
    for model in DEVICE_MODELS:
        if model_number == model.MODEL_NUMBER:
            return model
    else:
        _LOGGER.warning(
            "Could not determine Airthings model from model number: %s. Most likely an unimplemented model, or not an Airthings device."
        )
        raise AirthingsModelNotImplementedException(model_number)


def determine_device_model(dev):
    mac_address = dev.addr
    manufacturer_data = dev.getValue(btle.ScanEntry.MANUFACTURER)
    identifier = parse_manufacturer_data(manufacturer_data)
    if identifier is None:
        # Not a Airthings device
        return None
    identifier = str(identifier)
    model_number = identifier[:4]
    serial_number = identifier[4:]
    model = determine_model_class(model_number)
    return model(mac_address, serial_number)


def parse_manufacturer_data(manufacturer_data):
    try:
        (idx, identifier, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:
        return None
    else:
        if idx == 0x0334:
            return identifier
