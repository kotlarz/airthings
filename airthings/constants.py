# General
DEVICE_MODEL_NUMBER_LENGTH = 4

DEFAULT_BEFORE_FETCH_SLEEP = 3  # seconds

# Connect
DEFAULT_CONNECT_ATTEMPTS = 6  # Times
DEFAULT_RECONNECT_SLEEP = 10  # Seconds
DEFAULT_NEXT_CONNECT_SLEEP = 0.1  # Seconds

# Scan
DEFAULT_SCAN_ATTEMPTS = 5  # Times
DEFAULT_SCAN_TIMEOUT = 3  # Seconds
DEFAULT_RESCAN_SLEEP = 1  # Seconds


# Sensors
## Humidity
SENSOR_HUMIDITY_KEY = "humidity"
SENSOR_HUMIDITY_LABEL = "Humidity"
SENSOR_HUMIDITY_UNIT = "%rH"
## Radon short term avg
SENSOR_RADON_SHORT_TERM_AVG_KEY = "radon_short_term_avg"
SENSOR_RADON_SHORT_TERM_AVG_LABEL = "Radon Short Term Average"
SENSOR_RADON_SHORT_TERM_AVG_UNIT = "Bq/m3"
## Radon long term avg
SENSOR_RADON_LONG_TERM_AVG_KEY = "radon_long_term_avg"
SENSOR_RADON_LONG_TERM_AVG_LABEL = "Radon Long Term Average"
SENSOR_RADON_LONG_TERM_AVG_UNIT = "Bq/m3"
## Temperature
SENSOR_TEMPERATURE_KEY = "temperature"
SENSOR_TEMPERATURE_LABEL = "Temperature"
SENSOR_TEMPERATURE_UNIT = "°C"
## Atmospheric pressure
SENSOR_ATMOSPHERIC_PRESSURE_KEY = "atmospheric_pressure"
SENSOR_ATMOSPHERIC_PRESSURE_LABEL = "Atmospheric pressure"
SENSOR_ATMOSPHERIC_PRESSURE_UNIT = "hPa"
## CO2
SENSOR_CO2_KEY = "co2"
SENSOR_CO2_LABEL = "CO2"
SENSOR_CO2_UNIT = "ppm"
## VOC
SENSOR_VOC_KEY = "voc"
SENSOR_VOC_LABEL = "VOC"
SENSOR_VOC_UNIT = "ppb"

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
