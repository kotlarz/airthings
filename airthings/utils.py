import struct

import bluepy.btle as btle

from airthings.devices import DEVICE_MODELS


def fetch_characteristics(peripheral, uuid):
    characteristics = peripheral.getCharacteristics(uuid=uuid)
    if len(characteristics) != 1:
        raise ValueError(
            "fetch_characteristics did not return exactly 1 characteristic"
        )
    characteristic = characteristics[0]
    return characteristic.read()


def determine_device_model_from_mac_address(mac_address):
    peripheral = btle.Peripheral(mac_address)
    model_number = fetch_characteristics(
        peripheral, btle.AssignedNumbers.modelNumberString
    ).decode("utf-8")
    serial_number = fetch_characteristics(
        peripheral, btle.AssignedNumbers.serialNumberString
    ).decode("utf-8")
    model = determine_model_class(model_number)
    if not model:
        # TODO: Add warning about an unimplemented device
        return None
    return model(mac_address, serial_number, peripheral=peripheral)


def determine_model_class(model_number):
    for model in DEVICE_MODELS:
        if model_number == model.MODEL_NUMBER:
            return model
    else:
        return None


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
    if not model:
        # TODO: Add warning about an unimplemented device
        return None
    return model(mac_address, serial_number)


def parse_manufacturer_data(manufacturer_data):
    try:
        (idx, identifier, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:
        return None
    else:
        if idx == 0x0334:
            return identifier
