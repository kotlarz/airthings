import logging
import struct
import sys
import time

import bluepy.btle as btle

from .constants import (
    DEFAULT_BEFORE_FETCH_SLEEP,
    DEFAULT_BLUETOOTH_ADDRESS_TYPE,
    DEFAULT_BLUETOOTH_INTERFACE,
    DEFAULT_CONNECT_ATTEMPTS,
    DEFAULT_FETCH_ATTEMPTS,
    DEFAULT_NEXT_CONNECT_SLEEP,
    DEFAULT_RECONNECT_SLEEP,
    DEFAULT_REFETCH_SLEEP,
    DEFAULT_RESCAN_SLEEP,
    DEFAULT_SCAN_ATTEMPTS,
    DEFAULT_SCAN_TIMEOUT,
)
from .exceptions import OutOfConnectAttemptsException, OutOfScanAttemptsException
from .models import Device
from .utils import (
    determine_device,
    determine_device_class_from_serial_number,
    determine_device_from_mac_address,
)

_LOGGER = logging.getLogger(__name__)


def discover_devices(
    mac_addresses=None,
    serial_numbers=None,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Discover Airthings devices either automatically, by MAC addresses or by serial_number
    """
    _LOGGER.debug("Starting to scan and discover Airthings devices.")
    _LOGGER.debug(
        "Scan attempts = {} times, Scan timeout = {} seconds, Rescan sleep = {} seconds, Iface= {}".format(
            scan_attempts, scan_timeout, rescan_sleep, iface
        )
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
            scanner = btle.Scanner(iface=iface)
            devices = scanner.scan(scan_timeout)
            for dev in devices:
                device = determine_device(dev)
                if device:
                    if mac_addresses and device.mac_address not in mac_addresses:
                        # MAC addresses are set, and the device MAC address does not
                        # match any in the list.
                        _LOGGER.debug(
                            "MAC address: {} is not in our mac_addresses list, ignoring it".format(
                                device.mac_address
                            )
                        )
                        continue
                    elif serial_numbers and device.serial_number not in serial_numbers:
                        # Serial numbers are set, and the device serial number does not match
                        # any in the list.
                        _LOGGER.debug(
                            "Serial number: {} is not in our serial_numbers list, ignoring it".format(
                                device.serial_number
                            )
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
                "discover_devices scan failed, retrying in {} seconds... Current retries = {} out of {}".format(
                    rescan_sleep, current_retries, scan_attempts
                )
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Find Airthings devices by using a list of MAC addresses.
    """
    return discover_devices(
        mac_addresses=mac_addresses,
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        iface=iface,
        address_type=address_type,
    )


def find_device_by_mac_address(
    mac_address,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Find a single Airthings device by searching for a MAC address.
    """
    devices = find_devices_by_mac_addresses(
        mac_addresses=[mac_address],
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        iface=iface,
        address_type=address_type,
    )
    return devices[0] if devices else None


def find_devices_by_serial_numbers(
    serial_numbers,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
):
    """
    Find Airthings devices by using a list of serial numbers (6 digits).
    """
    return discover_devices(
        serial_numbers=serial_numbers,
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        iface=iface,
    )


def find_device_by_serial_number(
    serial_number,
    scan_attempts=DEFAULT_SCAN_ATTEMPTS,
    scan_timeout=DEFAULT_SCAN_TIMEOUT,
    rescan_sleep=DEFAULT_RESCAN_SLEEP,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
):
    """
    Find a single Airthings device by using a serial number (6 digits).
    """
    devices = find_devices_by_serial_numbers(
        serial_numbers=[serial_number],
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        iface=iface,
    )
    return devices[0] if devices else None


def fetch_measurements_from_devices(
    devices,
    connect_attempts=DEFAULT_CONNECT_ATTEMPTS,
    reconnect_sleep=DEFAULT_RECONNECT_SLEEP,
    next_connect_sleep=DEFAULT_NEXT_CONNECT_SLEEP,
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from a list of Airthings devices.
    """
    for device in devices:
        current_retries = 0
        while True:
            try:
                device.fetch_and_set_measurements(
                    connect_attempts=connect_attempts,
                    reconnect_sleep=reconnect_sleep,
                    iface=iface,
                    fetch_attempts=fetch_attempts,
                    refetch_sleep=refetch_sleep,
                    address_type=address_type,
                )
                break
            except btle.BTLEDisconnectError as e:
                if current_retries == connect_attempts:
                    raise OutOfConnectAttemptsException(
                        connect_attempts, reconnect_sleep, next_connect_sleep
                    )

                current_retries += 1

                _LOGGER.debug(e)
                _LOGGER.debug(
                    "fetch_measurements_from_devices scan failed, retrying connect in {} seconds... Current retries = {} out of {}".format(
                        reconnect_sleep, current_retries, connect_attempts
                    )
                )

                time.sleep(reconnect_sleep)

        _LOGGER.debug(
            "Sleeping {} seconds before fetching and settings measurements from the next Airthings device".format(
                next_connect_sleep
            )
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from Airthings devices either automatically, by MAC addresses or by serial numbers
    """

    _LOGGER.debug("Starting to fetch measurements from Airthings devices")
    _LOGGER.debug(
        "Scan attempts = {} times, Scan timeout = {} seconds, Rescan sleep = {} seconds, Connect attempts = {} times, Reconnect sleep = {} seconds, Next connect sleep = {} seconds, Before fetch sleep = {} seconds. iface = {}, Fetch attempts = {} times, Refetch sleep = {} seconds, Address type = {}".format(
            scan_attempts,
            scan_timeout,
            rescan_sleep,
            connect_attempts,
            reconnect_sleep,
            next_connect_sleep,
            before_fetch_sleep,
            iface,
            fetch_attempts,
            refetch_sleep,
            address_type,
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

        _LOGGER.debug(
            "Checking if the serial numbers are valid Airthings serial numbers"
        )
        for serial_number in serial_numbers:
            device_class = determine_device_class_from_serial_number(serial_number)
            _LOGGER.debug(
                "Matched serial number {} with Airthings device model: {}".format(
                    serial_number, device_class.LABEL
                )
            )

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
                    device = determine_device_from_mac_address(
                        mac_address, iface=iface, address_type=address_type
                    )
                except btle.BTLEDisconnectError as e:
                    if current_retries == connect_attempts:
                        raise OutOfConnectAttemptsException(
                            connect_attempts, reconnect_sleep, next_connect_sleep
                        )

                    current_retries += 1

                    _LOGGER.debug(e)
                    _LOGGER.debug(
                        "determine_device_from_mac_address failed, retrying connect in {} seconds... Current retries = {} out of {}".format(
                            reconnect_sleep, current_retries, connect_attempts
                        )
                    )

                    time.sleep(reconnect_sleep)

            airthings_devices.append(device)
    else:
        # Discover the devices automatically
        _LOGGER.debug(
            "MAC addresses are not set, automatically discovering nearby Airthings devices"
        )
        airthings_devices = discover_devices(
            mac_addresses=mac_addresses,
            serial_numbers=serial_numbers,
            scan_timeout=scan_timeout,
            scan_attempts=scan_attempts,
            rescan_sleep=rescan_sleep,
            iface=iface,
            address_type=address_type,
        )

    _LOGGER.debug(
        "Sleeping {} seconds before fetching measurements from Airthings devices".format(
            before_fetch_sleep
        )
    )
    time.sleep(before_fetch_sleep)

    return fetch_measurements_from_devices(
        devices=airthings_devices,
        connect_attempts=connect_attempts,
        reconnect_sleep=reconnect_sleep,
        iface=iface,
        fetch_attempts=fetch_attempts,
        refetch_sleep=refetch_sleep,
        address_type=address_type,
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from a list of Airthings device serial numbers.
    """

    return fetch_measurements(
        serial_numbers=serial_numbers,
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        connect_attempts=connect_attempts,
        reconnect_sleep=reconnect_sleep,
        next_connect_sleep=next_connect_sleep,
        before_fetch_sleep=before_fetch_sleep,
        iface=iface,
        fetch_attempts=fetch_attempts,
        refetch_sleep=refetch_sleep,
        address_type=address_type,
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from a specific Airthings device serial number.
    """
    devices = fetch_measurements_from_serial_numbers(
        serial_numbers=[serial_number],
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        connect_attempts=connect_attempts,
        reconnect_sleep=reconnect_sleep,
        next_connect_sleep=next_connect_sleep,
        before_fetch_sleep=before_fetch_sleep,
        iface=iface,
        fetch_attempts=fetch_attempts,
        refetch_sleep=refetch_sleep,
        address_type=address_type,
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from a list of Airthings device MAC addresses.
    """
    return fetch_measurements(
        mac_addresses=mac_addresses,
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        connect_attempts=connect_attempts,
        reconnect_sleep=reconnect_sleep,
        next_connect_sleep=next_connect_sleep,
        before_fetch_sleep=before_fetch_sleep,
        iface=iface,
        fetch_attempts=fetch_attempts,
        refetch_sleep=refetch_sleep,
        address_type=address_type,
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
    iface=DEFAULT_BLUETOOTH_INTERFACE,
    fetch_attempts=DEFAULT_FETCH_ATTEMPTS,
    refetch_sleep=DEFAULT_REFETCH_SLEEP,
    address_type=DEFAULT_BLUETOOTH_ADDRESS_TYPE,
):
    """
    Fetch measurements from a specific Airthings device MAC address.
    """
    devices = fetch_measurements(
        mac_addresses=[mac_address],
        scan_attempts=scan_attempts,
        scan_timeout=scan_timeout,
        rescan_sleep=rescan_sleep,
        connect_attempts=connect_attempts,
        reconnect_sleep=reconnect_sleep,
        next_connect_sleep=next_connect_sleep,
        before_fetch_sleep=before_fetch_sleep,
        iface=iface,
        fetch_attempts=fetch_attempts,
        refetch_sleep=refetch_sleep,
        address_type=address_type,
    )
    return devices[0] if devices else None
