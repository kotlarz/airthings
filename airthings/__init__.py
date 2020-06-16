import struct
import sys
import time

import bluepy.btle as btle

from .models import Device
from .utils import determine_device_model, determine_device_model_from_mac_address

# General
SCAN_TIMEOUT = 3  # Seconds
SCAN_RETRIES = 3  # Times
CONNECT_RETRIES = 3  # Times


def discover_devices(
    mac_addresses=None,
    serial_numbers=None,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
):
    """
    Discover Airthings devices either automatically, by MAC addresses or by serial_number
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
                    elif serial_numbers and device.serial_number not in serial_numbers:
                        # Serial numbers are set, and the device serial number does not match
                        # any in the list.
                        continue

                    # Device is an Airthings device
                    airthings_devices.append(device)
            break
        except btle.BTLEException as e:
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


def find_devices_by_serial_numbers(
    serial_numbers, scan_timeout=SCAN_TIMEOUT, scan_retries=SCAN_RETRIES
):
    """
    Find Airthings devices by using a list of serial numbers (6 digits).
    """
    return discover_devices(
        serial_numbers=serial_numbers,
        scan_timeout=SCAN_TIMEOUT,
        scan_retries=SCAN_RETRIES,
    )


def find_device_by_serial_number(serial_number, timeout=SCAN_TIMEOUT):
    """
    Find a single Airthings device by using a serial number (6 digits).
    """
    devices = find_devices_by_serial_numbers([serial_number])
    return devices[0] if devices else None


def fetch_measurements_from_devices(devices, connect_retries=CONNECT_RETRIES):
    """
    Fetch measurements from a list of Airthings devices.
    """
    for device in devices:
        current_retries = 0
        while True:
            try:
                device.fetch_and_set_measurements(connect_retries)
                break
            except btle.BTLEDisconnectError:
                # TODO: better error handling
                if current_retries == connect_retries:
                    break
                current_retries += 1

    return devices


def fetch_measurements(
    mac_addresses=None,
    serial_numbers=None,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connect_retries=CONNECT_RETRIES,
):
    """
    Fetch measurements from Airthings devices either automatically, by MAC addresses or by serial numbers
    """
    if mac_addresses:
        """
        We do not need to discover as we already have their MAC addresses.
        We do however need to identify which model, which is normally done on
        discovery.
        """
        airthings_devices = []
        for mac_address in mac_addresses:
            current_retries = 0
            device = None
            while True:
                try:
                    device = determine_device_model_from_mac_address(mac_address)
                except btle.BTLEDisconnectError:
                    # TODO: better error handling
                    if current_retries == connect_retries:
                        break
                    current_retries += 1
            if device is None:
                # Could not determine device model/class
                # TODO: raise error?
                continue
            airthings_devices.append(device)

    else:
        # Discover the devices automatically
        airthings_devices = discover_devices(
            mac_addresses=mac_addresses,
            serial_numbers=serial_numbers,
            scan_timeout=scan_timeout,
            scan_retries=scan_retries,
        )

    return fetch_measurements_from_devices(
        devices=airthings_devices, connect_retries=connect_retries
    )


def fetch_measurements_from_serial_numbers(
    serial_numbers,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connect_retries=CONNECT_RETRIES,
):
    """
    Fetch measurements from a list of Airthings device serial numbers.
    """

    return fetch_measurements(
        serial_numbers=serial_numbers,
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connect_retries=connect_retries,
    )


def fetch_measurements_from_serial_number(
    serial_number,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connect_retries=CONNECT_RETRIES,
):
    """
    Fetch measurements from a specific Airthings device serial number.
    """
    devices = fetch_measurements_from_serial_numbers(
        serial_numbers=[serial_number],
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connect_retries=connect_retries,
    )
    return devices[0] if devices else None


def fetch_measurements_from_mac_addresses(
    mac_addresses,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connect_retries=CONNECT_RETRIES,
):
    """
    Fetch measurements from a list of Airthings device MAC addresses.
    """

    return fetch_measurements(
        mac_addresses=mac_addresses,
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connect_retries=connect_retries,
    )


def fetch_measurements_from_mac_address(
    mac_address,
    scan_timeout=SCAN_TIMEOUT,
    scan_retries=SCAN_RETRIES,
    connect_retries=CONNECT_RETRIES,
):
    """
    Fetch measurements from a specific Airthings device MAC address.
    """
    devices = fetch_measurements(
        mac_addresses=[mac_address],
        scan_timeout=scan_timeout,
        scan_retries=scan_retries,
        connect_retries=connect_retries,
    )
    return devices[0] if devices else None
