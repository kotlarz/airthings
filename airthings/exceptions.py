class AirthingsModelNotImplementedException(Exception):
    def __init__(self, model_number):
        super(AirthingsModelNotImplementedException, self).__init__(
            "Airthings model number {} is not implemented".format(model_number)
        )


class CouldNotDetermineAlarmSeverityException(Exception):
    def __init__(self, severity, value, rules):
        super(CouldNotDetermineAlarmSeverityException, self).__init__(
            "Could not determine severity: {}, with value: {}, and rules: {}. It's most likely not implemented".format(
                severity, value, rules
            )
        )


class OutOfScanAttemptsException(Exception):
    def __init__(self, scan_attempts, scan_timeout, rescan_sleep):
        super(OutOfScanAttemptsException, self).__init__(
            "Out of scan attempts, try raising the scan_attempts value (currently: {} times), scan_timeout value (currently: {} seconds), or the rescan_sleep value (currently: {} seconds)".format(
                scan_attempts, scan_timeout, rescan_sleep
            )
        )


class OutOfConnectAttemptsException(Exception):
    def __init__(self, connect_attempts, reconnect_sleep, next_connect_sleep=None):
        super(OutOfConnectAttemptsException, self).__init__(
            (
                "Out out connect attempts, try raising the connect_attempts value (currently: {} times), the reconnect_sleep value (currently: {} seconds)".format(
                    connect_attempts, reconnect_sleep
                )
            )
            + (
                ""
                if not next_connect_sleep
                else " or the next_connect_sleep value (currently: {} seconds)".format(
                    next_connect_sleep
                )
            )
        )


class OutOfFetchAttemptsException(Exception):
    def __init__(self, fetch_attempts, refetch_sleep):
        super(OutOfFetchAttemptsException, self).__init__(
            "Out of fetch attempts, try raising the fetch_attempts value (currently: {} times), or the refetch_sleep value (currently: {} seconds)".format(
                fetch_attempts, refetch_sleep
            )
        )
