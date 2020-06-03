import struct

import bluepy.btle as btle

from airthings.devices import DEVICE_MODELS


def determine_device_model(dev):
    mac_address = dev.addr
    manufacturer_data = dev.getValue(btle.ScanEntry.MANUFACTURER)
    for model in DEVICE_MODELS:
        serial_number = parse_manufacturer_data(manufacturer_data)
        if serial_number is None:
            # Not a Airthings device
            continue
        serial_number = str(serial_number)
        model_number = serial_number[:4]
        if model_number == model.MODEL_NUMBER:
            return model(mac_address, serial_number)
    else:
        return None


def parse_manufacturer_data(manufacturer_data):
    try:
        (idx, serial_number, _) = struct.unpack("<HLH", manufacturer_data)
    except Exception:
        return None
    else:
        if idx == 0x0334:
            return serial_number
