import logging
import struct
import sys
import time

import bluepy.btle as btle

from .constants import (
    DEFAULT_BEFORE_FETCH_SLEEP,
    DEFAULT_CONNECT_ATTEMPTS,
    DEFAULT_NEXT_CONNECT_SLEEP,
    DEFAULT_RECONNECT_SLEEP,
    DEFAULT_RESCAN_SLEEP,
    DEFAULT_SCAN_ATTEMPTS,
    DEFAULT_SCAN_TIMEOUT,
)
from .exceptions import OutOfConnectAttemptsException, OutOfScanAttemptsException
from .models import Device
from .utils import determine_device_model, determine_device_model_from_mac_address

_LOGGER = logging.getLogger(__name__)


def discover_devices(
    mac_addresses=None,
    serial_numbers=None,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
):
    """
    Discover Airthings devices either automatically, by MAC addresses or by serial_number
    """
    _LOGGER.debug("Starting to scan and discover Airthings devices.")
    _LOGGER.debug(
        "Scan attempts = %d times, Scan timeout = %d seconds, Rescan sleep = %d seconds"
        % (scan_attempts, scan_timeout, rescan_sleep)
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
            if current_retries == scan_attempts:
                raise OutOfScanAttemptsException(
                    scan_attempts, scan_timeout, rescan_sleep
                )

            current_retries += 1

            _LOGGER.debug(e)
            _LOGGER.debug(
                "discover_devices scan failed, retrying in %d seconds... Current retries = %d out of %d"
                % (rescan_sleep, current_retries, scan_attempts)
            )

            time.sleep(rescan_sleep)

    _LOGGER.debug("discover_devices discovered the following Airthings devices:")
    _LOGGER.debug(airthings_devices)

    return airthings_devices


def find_devices_by_mac_addresses(
    mac_addresses,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
):
    """
    Find Airthings devices by using a list of MAC addresses.
    """
    return discover_devices(mac_addresses, scan_attempts, scan_timeout, rescan_sleep)


def find_device_by_mac_address(
    mac_address,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
):
    """
    Find a single Airthings device by searching for a MAC address.
    """
    devices = find_devices_by_mac_addresses(
        [mac_address], scan_attempts, scan_timeout, rescan_sleep
    )
    return devices[0] if devices else None


def find_devices_by_serial_numbers(
    serial_numbers,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
):
    """
    Find Airthings devices by using a list of serial numbers (6 digits).
    """
    return discover_devices(serial_numbers, scan_attempts, scan_timeout, rescan_sleep)


def find_device_by_serial_number(
    serial_number,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
):
    """
    Find a single Airthings device by using a serial number (6 digits).
    """
    devices = find_devices_by_serial_numbers(
        [serial_number], scan_attempts, scan_timeout, rescan_sleep
    )
    return devices[0] if devices else None


def fetch_measurements_from_devices(
    devices,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
):
    """
    Fetch measurements from a list of Airthings devices.
    """
    for device in devices:
        current_retries = 0
        while True:
            try:
                device.fetch_and_set_measurements(connect_attempts)
                break
            except btle.BTLEDisconnectError as e:
                if current_retries == connect_attempts:
                    raise OutOfConnectAttemptsException(
                        connect_attempts, reconnect_sleep, next_connect_sleep
                    )

                current_retries += 1

                _LOGGER.debug(e)
                _LOGGER.debug(
                    "fetch_measurements_from_devices scan failed, retrying connect in %d seconds... Current retries = %d out of %d"
                    % (reconnect_sleep, current_retries, connect_attempts)
                )

                time.sleep(reconnect_sleep)

        _LOGGER.debug(
            "Sleeping %d seconds before fetching and settings measurements from the next Airthings device"
            % next_connect_sleep
        )
        time.sleep(next_connect_sleep)

    return devices


def fetch_measurements(
    mac_addresses=None,
    serial_numbers=None,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    before_fetch_sleep=DEFAULT_BEFORE_FETCH_SLEEP,
):
    """
    Fetch measurements from Airthings devices either automatically, by MAC addresses or by serial numbers
    """

    _LOGGER.debug("Starting to fetch measurements from Airthings devices")
    _LOGGER.debug(
        "Scan attempts = %d times, Scan timeout = %d seconds, Rescan sleep = %d seconds, Connect attempts = %d times, Reconnect sleep = %d seconds, Next connect sleep = %d seconds, Before fetch sleep = %d seconds"
        % (
            scan_attempts,
            scan_timeout,
            rescan_sleep,
            connect_attempts,
            reconnect_sleep,
            next_connect_sleep,
            before_fetch_sleep,
        )
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
                    if current_retries == connect_attempts:
                        raise OutOfConnectAttemptsException(
                            connect_attempts, reconnect_sleep, next_connect_sleep
                        )

                    current_retries += 1

                    _LOGGER.debug(e)
                    _LOGGER.debug(
                        "determine_device_model_from_mac_addres failed, retrying connect in %d seconds... Current retries = %d out of %d"
                        % (reconnect_sleep, current_retries, connect_attempts)
                    )

                    time.sleep(reconnect_sleep)

            airthings_devices.append(device)

    else:
        # Discover the devices automatically
        _LOGGER.debug(
            "MAC addresses are not set, automatically discovering nearby Airthings devices"
        )
        airthings_devices = discover_devices(
            mac_addresses, serial_numbers, scan_timeout, scan_attempts, rescan_sleep,
        )

    _LOGGER.debug(
        "Sleeping %d seconds before fetching measurements from devices"
        % before_fetch_sleep
    )
    time.sleep(before_fetch_sleep)

    return fetch_measurements_from_devices(
        airthings_devices, connect_attempts, reconnect_sleep
    )


def fetch_measurements_from_serial_numbers(
    serial_numbers,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    before_fetch_sleep=DEFAULT_BEFORE_FETCH_SLEEP,
):
    """
    Fetch measurements from a list of Airthings device serial numbers.
    """

    return fetch_measurements(
        serial_numbers,
        scan_attempts,
        scan_timeout,
        rescan_sleep,
        connect_attempts,
        reconnect_sleep,
        next_connect_sleep,
        before_fetch_sleep,
    )


def fetch_measurements_from_serial_number(
    serial_number,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    before_fetch_sleep=DEFAULT_BEFORE_FETCH_SLEEP,
):
    """
    Fetch measurements from a specific Airthings device serial number.
    """
    devices = fetch_measurements_from_serial_numbers(
        [serial_number],
        scan_attempts,
        scan_timeout,
        rescan_sleep,
        connect_attempts,
        reconnect_sleep,
        next_connect_sleep,
        before_fetch_sleep,
    )
    return devices[0] if devices else None


def fetch_measurements_from_mac_addresses(
    mac_addresses,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    before_fetch_sleep=DEFAULT_BEFORE_FETCH_SLEEP,
):
    """
    Fetch measurements from a list of Airthings device MAC addresses.
    """

    return fetch_measurements(
        mac_addresses,
        scan_attempts,
        scan_timeout,
        rescan_sleep,
        connect_attempts,
        reconnect_sleep,
        next_connect_sleep,
        before_fetch_sleep,
    )


def fetch_measurements_from_mac_address(
    mac_address,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    before_fetch_sleep=DEFAULT_BEFORE_FETCH_SLEEP,
):
    """
    Fetch measurements from a specific Airthings device MAC address.
    """
    devices = fetch_measurements(
        [mac_address],
        scan_attempts,
        scan_timeout,
        rescan_sleep,
        connect_attempts,
        reconnect_sleep,
        next_connect_sleep,
        before_fetch_sleep,
    )
    return devices[0] if devices else None
