#!/usr/bin/env python3
from airthings import find_device_by_identifier, find_devices_by_identifiers

if __name__ == "__main__":
    # With a single identifier
    device = find_device_by_identifier("xxxxxx")
    print("Found Airthings device")
    print("=" * 36)
    print("\tMAC address:", device.mac_address)
    print("\tIdentifier:", device.identifier)
    print("\tModel:", device.label)
    print("\tModel number:", device.model_number)

    # Or with a list of identifiers
    identifiers = ["xxxxxx"]
    airthings_devices = find_devices_by_identifiers(identifiers)
    print("Found %s Airthings devices:" % len(airthings_devices))
    for device in airthings_devices:
        print("=" * 36)
        print("\tMAC address:", device.mac_address)
        print("\tIdentifier:", device.identifier)
        print("\tModel:", device.label)
        print("\tModel number:", device.model_number)
