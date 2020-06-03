import struct
import sys
import time
from pprint import pprint

import bluepy.btle as btle

from .utils import determine_device_model

# General
SCAN_TIMEOUT = 3  # Seconds
SCAN_RETRIES = 3  # Times
CONNECTION_RETRIES = 3  # Times


def discover_devices(
    mac_addresses=None,
    identifiers=None,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
):
    """
    Discover Airthings devices either automatically, by MAC addresses or by identifiers
    """
    airthings_devices = []
    current_retries = 0
    while True:
        try:
            scanner = btle.Scanner()
            devices = scanner.scan(scan_timeout)
            for dev in devices:
                device = determine_device_model(dev)
                if device:
                    if mac_addresses and device.mac_address not in mac_addresses:
                        # MAC addresses are set, and the device MAC address does not
                        # match any in the list.
                        continue
                    elif identifiers and device.identifier not in identifiers:
                        # Identifiers are set, and the device identifier does not match
                        # any in the list.
                        continue

                    # Device is an Airthings device
                    airthings_devices.append(device)
            break
        except Exception as _:  # noqa: F841
            # TODO: better error handling
            if current_retries == scan_retries:
                break
            current_retries += 1

    return airthings_devices


def find_devices_by_mac_addresses(
    mac_addresses, scan_timeout=SCAN_TIMEOUT, scan_retries=SCAN_RETRIES
):
    """
    Find Airthings devices by using a list of MAC addresses.
    """
    return discover_devices(
        mac_addresses=mac_addresses,
        scan_timeout=SCAN_TIMEOUT,
        scan_retries=SCAN_RETRIES,
    )


def find_device_by_mac_address(
    mac_address, scan_timeout=SCAN_TIMEOUT, scan_retries=SCAN_RETRIES
):
    """
    Find a single Airthings device by searching for a MAC address.
    """
    devices = find_devices_by_mac_addresses(
        mac_addresses=[mac_address],
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
    )
    return devices[0] if devices else None


def find_devices_by_identifiers(
    identifiers, scan_timeout=SCAN_TIMEOUT, scan_retries=SCAN_RETRIES
):
    """
    Find Airthings devices by using a list of identifiers (the last 6 digits of a serial number).
    """
    return discover_devices(
        identifiers=identifiers, scan_timeout=SCAN_TIMEOUT, scan_retries=SCAN_RETRIES
    )


def find_device_by_identifier(identifier, timeout=SCAN_TIMEOUT):
    """
    Find a single Airthings device by using an identifier (the last 6 digits of aserial number).
    """
    devices = find_devices_by_identifiers([identifier])
    return devices[0] if devices else None


def fetch_measurements_from_devices(devices, connection_retries=CONNECTION_RETRIES):
    """
    Fetch measurements from a list of Airthings devices.
    """
    current_retries = 0
    for device in devices:
        while True:
            try:
                device.fetch_and_set_measurements()
                break
            except btle.BTLEDisconnectError as _:  # noqa: F841
                # TODO: better error handling
                if current_retries == connection_retries:
                    break
                current_retries += 1

    return devices


def fetch_measurements(
    mac_addresses=None,
    identifiers=None,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connection_retries=CONNECTION_RETRIES,
):
    """
    Fetch measurements from Airthings devices either automatically, by MAC addresses or by identifiers
    """

    airthings_devices = discover_devices(
        mac_addresses=mac_addresses,
        identifiers=identifiers,
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
    )

    return fetch_measurements_from_devices(
        devices=airthings_devices, connection_retries=connection_retries
    )


def fetch_measurements_from_identifiers(
    identifiers,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connection_retries=CONNECTION_RETRIES,
):
    """
    Fetch measurements from a list of Airthings device identifiers.
    """

    return fetch_measurements(
        identifiers=identifiers,
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connection_retries=connection_retries,
    )


def fetch_measurements_from_identifier(
    identifier,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connection_retries=CONNECTION_RETRIES,
):
    """
    Fetch measurements from a specific Airthings device identifier.
    """
    devices = fetch_measurements_from_identifiers(
        identifiers=[identifier],
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connection_retries=connection_retries,
    )
    return devices[0] if devices else None


def fetch_measurements_from_mac_addresses(
    mac_addresses,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connection_retries=CONNECTION_RETRIES,
):
    """
    Fetch measurements from a list of Airthings device MAC addresses.
    """

    return fetch_measurements(
        mac_addresses=mac_addresses,
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connection_retries=connection_retries,
    )


def fetch_measurements_from_mac_address(
    mac_address,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connection_retries=CONNECTION_RETRIES,
):
    """
    Fetch measurements from a specific Airthings device MAC address.
    """
    devices = fetch_measurements(
        mac_addresses=[mac_address],
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connection_retries=connection_retries,
    )
    return devices[0] if devices else None
