from airthings.constants import SENSOR_CO2_KEY, SENSOR_CO2_LABEL, SENSOR_CO2_UNIT
from airthings.models import Sensor


class CO2Sensor(Sensor):
    KEY = SENSOR_CO2_KEY
    LABEL = SENSOR_CO2_LABEL
    UNIT = SENSOR_CO2_UNIT

    def __init__(self, value):
        super(CO2Sensor, self).__init__(value)
