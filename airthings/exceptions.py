class AirthingsModelNotImplementedException(Exception):
    def __init__(self, model_number):
        super(AirthingsModelNotImplementedException, self).__init__(
            "Airthings model number %s is not implemented" % model_number
        )


class OutOfScanAttemptsException(Exception):
    def __init__(self, scan_attempts, scan_timeout, rescan_sleep):
        super(OutOfScanAttemptsException, self).__init__(
            "Out of scan attempts, try raising the scan_attempts value (currently: %d times), scan_timeout value (currently: %d seconds), or the rescan_sleep value (currently: %d seconds)"
            % (scan_attempts, scan_timeout, rescan_sleep)
        )


class OutOfConnectAttemptsException(Exception):
    def __init__(self, connect_attempts, reconnect_sleep, next_connect_sleep=None):
        super(OutOfConnectAttemptsException, self).__init__(
            (
                "Out out connect attempts, try raising the connect_attempts value (currently: %d times), the reconnect_sleep value (currently: %d seconds)"
                % (connect_attempts, reconnect_sleep)
            )
            + (
                ""
                if not next_connect_sleep
                else " or the next_connect_sleep value (currently: %d seconds)"
                % next_connect_sleep
            )
        )
