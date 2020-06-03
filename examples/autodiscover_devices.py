#!/usr/bin/env python3
from airthings import discover_devices

if __name__ == "__main__":
    airthings_devices = discover_devices()
    print("Found %s Airthings devices:" % len(airthings_devices))
    for device in airthings_devices:
        print("=" * 36)
        print("\tMAC address:", device.mac_address)
        print("\tIdentifier:", device.identifier)
        print("\tModel:", device.label)
        print("\tModel number:", device.model_number)
        print("\tHas measurements:", device.has_measurements)
        print("\tHumidity:", device.humidity)
        print("\tSensor capabilities:")
        for sensor, supported in device.sensor_capabilities.items():
            print("\t", sensor, "=", "YES" if supported else "NO")
