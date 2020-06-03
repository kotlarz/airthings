#!/usr/bin/env python3
from airthings import find_device_by_mac_address, find_devices_by_mac_addresses

if __name__ == "__main__":
    # With a single MAC address
    device = find_device_by_mac_address("00:81:f9:f8:19:92")
    print("Found Airthings device")
    print("=" * 36)
    print("\tMAC address:", device.mac_address)
    print("\tIdentifier:", device.identifier)
    print("\tModel:", device.label)
    print("\tModel number:", device.model_number)

    # Or with a list of MAC addresses
    mac_addresses = ["00:81:f9:f8:19:92"]
    airthings_devices = find_devices_by_mac_addresses(mac_addresses)
    print("Found %s Airthings devices:" % len(airthings_devices))
    for device in airthings_devices:
        print("=" * 36)
        print("\tMAC address:", device.mac_address)
        print("\tIdentifier:", device.identifier)
        print("\tModel:", device.label)
        print("\tModel number:", device.model_number)
