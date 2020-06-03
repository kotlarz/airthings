#!/usr/bin/env python3
from airthings import (
    fetch_measurements_from_identifier,
    fetch_measurements_from_identifiers,
)

if __name__ == "__main__":
    # With a single identifier
    device = fetch_measurements_from_identifier("xxxxxx")
    print("Found Airthings device")
    print("=" * 36)
    print("\tMAC address:", device.mac_address)
    print("\tIdentifier:", device.identifier)
    print("\tModel:", device.label)
    print("\tModel number:", device.model_number)
    print("\tHas measurements:", device.has_measurements)
    print("+" * 11, "Measurements", "+" * 11)
    print("\t", device.humidity)
    print("\t", device.radon_short_term_avg)
    print("\t", device.radon_long_term_avg)
    print("\t", device.temperature)
    print("\t", device.atmospheric_pressure)
    print("\t", device.co2)
    print("\t", device.voc)

    # Or with a list of identifiers
    identifiers = ["xxxxxx"]
    airthings_devices = fetch_measurements_from_identifiers(identifiers)
    print("Found %s Airthings devices:" % len(airthings_devices))
    for device in airthings_devices:
        print("=" * 36)
        print("\tMAC address:", device.mac_address)
        print("\tIdentifier:", device.identifier)
        print("\tModel:", device.label)
        print("\tModel number:", device.model_number)
        print("\tHas measurements:", device.has_measurements)
        print("+" * 11, "Measurements", "+" * 11)
        print("\t", device.humidity)
        print("\t", device.radon_short_term_avg)
        print("\t", device.radon_long_term_avg)
        print("\t", device.temperature)
        print("\t", device.atmospheric_pressure)
        print("\t", device.co2)
        print("\t", device.voc)
