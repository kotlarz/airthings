import logging
import struct
import sys
import time

import bluepy.btle as btle

from .constants import (
    DEFAULT_CONNECT_RETRIES,
    DEFAULT_CONNECT_SLEEP,
    DEFAULT_SCAN_RETRIES,
    DEFAULT_SCAN_SLEEP,
    DEFAULT_SCAN_TIMEOUT,
)
from .exceptions import OutOfConnectRetriesException, OutOfScanRetriesException
from .models import Device
from .utils import determine_device_model, determine_device_model_from_mac_address

_LOGGER = logging.getLogger(__name__)


def discover_devices(
    mac_addresses=None,
    serial_numbers=None,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
):
    """
    Discover Airthings devices either automatically, by MAC addresses or by serial_number
    """
    _LOGGER.debug("Starting to scan and discover Airthings devices.")
    _LOGGER.debug(
        "Scan timeout = %d seconds, Scan retries = %d times, Scan sleep = %d seconds"
        % (scan_timeout, scan_retries, scan_sleep)
    )
    if mac_addresses:
        _LOGGER.debug(
            "We are only looking for Airthings devices with the following MAC addresses:"
        )
        _LOGGER.debug(mac_addresses)
    elif serial_numbers:
        _LOGGER.debug(
            "We are only looking for Airthings devices with the following serial numbers:"
        )
        _LOGGER.debug(serial_numbers)
    else:
        _LOGGER.debug("We are automatically discovering all nearby Airthings devices")

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
                        _LOGGER.debug(
                            "MAC address: %s is not in our mac_addresses list"
                            % device.mac_address
                        )
                        continue
                    elif serial_numbers and device.serial_number not in serial_numbers:
                        # Serial numbers are set, and the device serial number does not match
                        # any in the list.
                        _LOGGER.debug(
                            "Serial number: %s is not in our serial_numbers list"
                            % device.serial_number
                        )
                        continue

                    # Device is an Airthings device
                    airthings_devices.append(device)
            break
        except btle.BTLEException as e:
            if current_retries == scan_retries:
                raise OutOfScanRetriesException(scan_timeout, scan_retries, scan_sleep)

            current_retries += 1

            _LOGGER.debug(e)
            _LOGGER.debug(
                "discover_devices scan failed, retrying in %d seconds... Current retries = %d out of %d"
                % (scan_sleep, current_retries, scan_retries)
            )

            time.sleep(scan_sleep)

    _LOGGER.debug("discover_devices discovered the following Airthings devices:")
    _LOGGER.debug(airthings_devices)

    return airthings_devices


def find_devices_by_mac_addresses(
    mac_addresses,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
):
    """
    Find Airthings devices by using a list of MAC addresses.
    """
    return discover_devices(mac_addresses, scan_timeout, scan_retries, scan_sleep)


def find_device_by_mac_address(
    mac_address,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
):
    """
    Find a single Airthings device by searching for a MAC address.
    """
    devices = find_devices_by_mac_addresses(
        [mac_address], scan_timeout, scan_retries, scan_sleep
    )
    return devices[0] if devices else None


def find_devices_by_serial_numbers(
    serial_numbers,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
):
    """
    Find Airthings devices by using a list of serial numbers (6 digits).
    """
    return discover_devices(serial_numbers, scan_timeout, scan_retries, scan_sleep)


def find_device_by_serial_number(
    serial_number,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
):
    """
    Find a single Airthings device by using a serial number (6 digits).
    """
    devices = find_devices_by_serial_numbers(
        [serial_number], scan_timeout, scan_retries, scan_sleep
    )
    return devices[0] if devices else None


def fetch_measurements_from_devices(
    devices,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a list of Airthings devices.
    """
    for device in devices:
        current_retries = 0
        while True:
            try:
                device.fetch_and_set_measurements(connect_retries)
                break
            except btle.BTLEDisconnectError as e:
                if current_retries == connect_retries:
                    raise OutOfConnectRetriesException(connect_retries, connect_sleep)

                current_retries += 1

                _LOGGER.debug(e)
                _LOGGER.debug(
                    "fetch_measurements_from_devices scan failed, retrying connect in %d seconds... Current retries = %d out of %d"
                    % (connect_sleep, current_retries, connect_retries)
                )

                time.sleep(connect_sleep)

    return devices


def fetch_measurements(
    mac_addresses=None,
    serial_numbers=None,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from Airthings devices either automatically, by MAC addresses or by serial numbers
    """

    _LOGGER.debug("Starting to fetch measurements from Airthings devices")
    _LOGGER.debug(
        "Scan timeout = %d seconds, Scan retries = %d times, Scan sleep = %d seconds, Connect retries = %d times, Connect sleep = %d seconds"
        % (scan_timeout, scan_retries, scan_sleep, connect_retries, connect_sleep)
    )

    if mac_addresses:
        _LOGGER.debug(
            "We are only fetching measurements from Airthings devices with the following MAC addresses:"
        )
        _LOGGER.debug(mac_addresses)
    elif serial_numbers:
        _LOGGER.debug(
            "We are only fetching measurements from Airthings devices with the following serial numbers:"
        )
        _LOGGER.debug(serial_numbers)
    else:
        _LOGGER.debug(
            "We are automatically discovering all nearby Airthings devices and fetching measurements from them"
        )

    if mac_addresses:
        """
        We do not need to discover as we already have their MAC addresses.
        We do however need to identify which model, which is normally done on
        discovery.
        """
        _LOGGER.debug("Skipping discovering as MAC addresses are set")
        airthings_devices = []
        for mac_address in mac_addresses:
            current_retries = 0
            while True:
                try:
                    device = determine_device_model_from_mac_address(mac_address)
                except btle.BTLEDisconnectError as e:
                    if current_retries == connect_retries:
                        raise OutOfConnectRetriesException(
                            connect_retries, connect_sleep
                        )

                    current_retries += 1

                    _LOGGER.debug(e)
                    _LOGGER.debug(
                        "determine_device_model_from_mac_addres failed, retrying connect in %d seconds... Current retries = %d out of %d"
                        % (connect_sleep, current_retries, connect_retries)
                    )

                    time.sleep(connect_sleep)

            airthings_devices.append(device)

    else:
        # Discover the devices automatically
        airthings_devices = discover_devices(
            mac_addresses, serial_numbers, scan_timeout, scan_retries, scan_sleep,
        )

    return fetch_measurements_from_devices(
        airthings_devices, connect_retries, connect_sleep
    )


def fetch_measurements_from_serial_numbers(
    serial_numbers,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a list of Airthings device serial numbers.
    """

    return fetch_measurements(
        serial_numbers,
        scan_timeout,
        scan_retries,
        scan_sleep,
        connect_retries,
        connect_sleep,
    )


def fetch_measurements_from_serial_number(
    serial_number,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a specific Airthings device serial number.
    """
    devices = fetch_measurements_from_serial_numbers(
        [serial_number],
        scan_timeout,
        scan_retries,
        scan_sleep,
        connect_retries,
        connect_sleep,
    )
    return devices[0] if devices else None


def fetch_measurements_from_mac_addresses(
    mac_addresses,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a list of Airthings device MAC addresses.
    """

    return fetch_measurements(
        mac_addresses,
        scan_timeout,
        scan_retries,
        scan_sleep,
        connect_retries,
        connect_sleep,
    )


def fetch_measurements_from_mac_address(
    mac_address,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    scan_retries=DEFAULT_SCAN_RETRIES,
    scan_sleep=DEFAULT_SCAN_SLEEP,
    connect_retries=DEFAULT_CONNECT_RETRIES,
    connect_sleep=DEFAULT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a specific Airthings device MAC address.
    """
    devices = fetch_measurements(
        [mac_address],
        scan_timeout,
        scan_retries,
        scan_retries,
        connect_retries,
        connect_sleep,
    )
    return devices[0] if devices else None
