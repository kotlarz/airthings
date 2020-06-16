class AirthingsModelNotImplementedException(Exception):
    def __init__(self, model_number):
        super(AirthingsModelNotImplementedException, self).__init__(
            "Airthings model number %s is not implemented" % model_number
        )


class OutOfScanRetriesException(Exception):
    def __init__(self, scan_timeout, scan_retries, scan_sleep):
        super(OutOfScanRetriesException, self).__init__(
            "Out of scan retries, try raising the scan_retries value (currently: %d), the scan_timeout value (currently: %d), or the scan_sleep value (currently: %d)"
            % (scan_retries, scan_timeout, scan_sleep)
        )


class OutOfConnectRetriesException(Exception):
    def __init__(self, connect_retries, connect_sleep):
        super(OutOfConnectRetriesException, self).__init__(
            "Out of connect retries, try raising the connect_retries value (currently: %d) or the connect_sleep value (currently: %d)"
            % (connect_retries, connect_sleep)
        )
