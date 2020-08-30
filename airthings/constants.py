# General
DEVICE_MODEL_NUMBER_LENGTH = 4

DEFAULT_BLUETOOTH_INTERFACE = 0  # 0 is hci0, 1 is hci1, etc.
BLUETOOTH_ADDRESS_TYPE_PUBLIC = "public"  # Same as bluepy.btle.ADDR_TYPE_PUBLIC
BLUETOOTH_ADDRESS_TYPE_RANDOM = "random"  # Same as bluepy.btle.ADDR_TYPE_RANDOM
DEFAULT_BLUETOOTH_ADDRESS_TYPE = BLUETOOTH_ADDRESS_TYPE_PUBLIC
DEFAULT_BEFORE_FETCH_SLEEP = 3  # seconds

# Connect
DEFAULT_CONNECT_ATTEMPTS = 6  # Times
DEFAULT_RECONNECT_SLEEP = 5  # Seconds
DEFAULT_NEXT_CONNECT_SLEEP = 0.5  # Seconds

# Fetch
DEFAULT_FETCH_ATTEMPTS = 3  # Times
DEFAULT_REFETCH_SLEEP = 5  # Seconds
DEFAULT_NEXT_CONNECT_SLEEP = 0.5  # Seconds

# Scan
DEFAULT_SCAN_ATTEMPTS = 5  # Times
DEFAULT_SCAN_TIMEOUT = 3  # Seconds
DEFAULT_RESCAN_SLEEP = 1  # Seconds

# Alarm rules
ALARM_OPERATOR_EQUAL = "equal"
ALARM_OPERATOR_NOT_EQUAL = "not_equal"
ALARM_OPERATOR_GREATER_THAN = "greater_than"
ALARM_OPERATOR_LESS_THAN = "less_than"
ALARM_OPERATOR_GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
ALARM_OPERATOR_LESS_THAN_OR_EQUAL = "less_than_or_equal"

# Alarm severity levels
ALARM_SEVERITY_HIGH = "high"
ALARM_SEVERITY_HIGH_LABEL = "HIGH"
ALARM_SEVERITY_HIGH_COLOR = "red"
ALARM_SEVERITY_MEDIUM = "medium"
ALARM_SEVERITY_MEDIUM_LABEL = "MEDIUM"
ALARM_SEVERITY_MEDIUM_COLOR = "orange"
ALARM_SEVERITY_LOW = "low"
ALARM_SEVERITY_LOW_LABEL = "LOW"
ALARM_SEVERITY_LOW_COLOR = "yellow"
ALARM_SEVERITY_CAUTION = "caution"
ALARM_SEVERITY_CAUTION_LABEL = "CAUTION"
ALARM_SEVERITY_CAUTION_COLOR = "blue"
ALARM_SEVERITY_NONE = "none"
ALARM_SEVERITY_NONE_LABEL = "NONE"
ALARM_SEVERITY_NONE_COLOR = None
ALARM_SEVERITY_UNKNOWN = "unknown"
ALARM_SEVERITY_UNKNOWN_LABEL = "UNKNOWN"
ALARM_SEVERITY_UNKNOWN_COLOR = "gray"
ALARM_SEVERITY_MAPPING = {
    ALARM_SEVERITY_HIGH: {
        "label": ALARM_SEVERITY_HIGH_LABEL,
        "color": ALARM_SEVERITY_HIGH_COLOR,
    },
    ALARM_SEVERITY_MEDIUM: {
        "label": ALARM_SEVERITY_MEDIUM_LABEL,
        "color": ALARM_SEVERITY_MEDIUM_COLOR,
    },
    ALARM_SEVERITY_LOW: {
        "label": ALARM_SEVERITY_LOW_LABEL,
        "color": ALARM_SEVERITY_LOW_COLOR,
    },
    ALARM_SEVERITY_CAUTION: {
        "label": ALARM_SEVERITY_CAUTION_LABEL,
        "color": ALARM_SEVERITY_CAUTION_COLOR,
    },
    ALARM_SEVERITY_NONE: {
        "label": ALARM_SEVERITY_NONE_LABEL,
        "color": ALARM_SEVERITY_NONE_COLOR,
    },
    ALARM_SEVERITY_UNKNOWN: {
        "label": ALARM_SEVERITY_UNKNOWN_LABEL,
        "color": ALARM_SEVERITY_UNKNOWN_COLOR,
    },
}

# Sensors
## Humidity
SENSOR_HUMIDITY_KEY = "humidity"
SENSOR_HUMIDITY_LABEL = "Humidity"
SENSOR_HUMIDITY_UNIT = "%rH"
SENSOR_HUMIDITY_ALARM_RULES = [
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 70}],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 60},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 70},
        ],
    },
    {
        "severity": ALARM_SEVERITY_NONE,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 30},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 60},
        ],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 25},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 30},
        ],
    },
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_LESS_THAN, "value": 25}],
    },
]
## Radon
SENSOR_RADON_UNIT = "Bq/m3"
SENSOR_RADON_ALARM_RULES = [
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 150}],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 100},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 150},
        ],
    },
    {
        "severity": ALARM_SEVERITY_NONE,
        "rules": [{"operator": ALARM_OPERATOR_LESS_THAN, "value": 100}],
    },
]

### Radon short term avg
SENSOR_RADON_SHORT_TERM_AVG_KEY = "radon_short_term_avg"
SENSOR_RADON_SHORT_TERM_AVG_LABEL = "Radon Short Term Average"

### Radon long term avg
SENSOR_RADON_LONG_TERM_AVG_KEY = "radon_long_term_avg"
SENSOR_RADON_LONG_TERM_AVG_LABEL = "Radon Long Term Average"

## Temperature
SENSOR_TEMPERATURE_KEY = "temperature"
SENSOR_TEMPERATURE_LABEL = "Temperature"
SENSOR_TEMPERATURE_UNIT = "°C"
SENSOR_TEMPERATURE_ALARM_RULES = [
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 25}],
    },
    {
        "severity": ALARM_SEVERITY_NONE,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN, "value": 18},
            {"operator": ALARM_OPERATOR_LESS_THAN_OR_EQUAL, "value": 25},
        ],
    },
    {
        "severity": ALARM_SEVERITY_CAUTION,
        "rules": [{"operator": ALARM_OPERATOR_LESS_THAN, "value": 18}],
    },
]

## Atmospheric pressure
SENSOR_ATMOSPHERIC_PRESSURE_KEY = "atmospheric_pressure"
SENSOR_ATMOSPHERIC_PRESSURE_LABEL = "Atmospheric pressure"
SENSOR_ATMOSPHERIC_PRESSURE_UNIT = "hPa"

## CO2
SENSOR_CO2_KEY = "co2"
SENSOR_CO2_LABEL = "CO2"
SENSOR_CO2_UNIT = "ppm"
SENSOR_CO2_ALARM_RULES = [
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 1000}],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN, "value": 800},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 1000},
        ],
    },
    {
        "severity": ALARM_SEVERITY_NONE,
        "rules": [{"operator": ALARM_OPERATOR_LESS_THAN, "value": 800}],
    },
]

## VOC
SENSOR_VOC_KEY = "voc"
SENSOR_VOC_LABEL = "VOC"
SENSOR_VOC_UNIT = "ppb"
SENSOR_VOC_ALARM_RULES = [
    {
        "severity": ALARM_SEVERITY_HIGH,
        "rules": [{"operator": ALARM_OPERATOR_GREATER_THAN_OR_EQUAL, "value": 2000}],
    },
    {
        "severity": ALARM_SEVERITY_MEDIUM,
        "rules": [
            {"operator": ALARM_OPERATOR_GREATER_THAN, "value": 250},
            {"operator": ALARM_OPERATOR_LESS_THAN, "value": 2000},
        ],
    },
    {
        "severity": ALARM_SEVERITY_NONE,
        "rules": [{"operator": ALARM_OPERATOR_LESS_THAN, "value": 250}],
    },
]

# Devices

## Wave Gen 1
WAVE_GEN_1_KEY = "wave_gen_1"
WAVE_GEN_1_LABEL = "Wave Gen 1"
WAVE_GEN_1_MODEL_NUMBER = "2900"
WAVE_GEN_1_RAW_DATA_FORMAT = "<H5B4H"
WAVE_GEN_1_UUID_DATETIME = 0x2A08
WAVE_GEN_1_UUID_HUMIDITY = 0x2A6F
WAVE_GEN_1_UUID_TEMPERATURE = 0x2A6E
WAVE_GEN_1_UUID_RADON_SHORT_TERM_AVERAGE = "b42e01aa-ade7-11e4-89d3-123b93f75cba"
WAVE_GEN_1_UUID_RADON_LONG_TERM_AVERAGE = "b42e0a4c-ade7-11e4-89d3-123b93f75cba"

## Wave Mini Gen 1
WAVE_MINI_GEN_1_KEY = "wave_mini_gen_1"
WAVE_MINI_GEN_1_LABEL = "Wave Mini Gen 1"
WAVE_MINI_GEN_1_MODEL_NUMBER = "2920"
WAVE_MINI_GEN_1_RAW_DATA_FORMAT = "<HHHHHHLL"
WAVE_MINI_GEN_1_UUID_DATA = "b42e3b98-ade7-11e4-89d3-123b93f75cba"

## Wave Plus Gen 1
WAVE_PLUS_GEN_1_KEY = "wave_plus_gen_1"
WAVE_PLUS_GEN_1_LABEL = "Wave Plus Gen 1"
WAVE_PLUS_GEN_1_MODEL_NUMBER = "2930"
WAVE_PLUS_GEN_1_RAW_DATA_FORMAT = "BBBBHHHHHHHH"
WAVE_PLUS_GEN_1_UUID_DATA = "b42e2a68-ade7-11e4-89d3-123b93f75cba"

## Wave Gen 2
WAVE_GEN_2_KEY = "wave_gen_2"
WAVE_GEN_2_LABEL = "Wave Gen 2"
WAVE_GEN_2_MODEL_NUMBER = "2950"
WAVE_GEN_2_RAW_DATA_FORMAT = "<4B8H"
WAVE_GEN_2_UUID_DATA = "b42e4dcc-ade7-11e4-89d3-123b93f75cba"
