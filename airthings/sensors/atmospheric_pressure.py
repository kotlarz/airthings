from airthings.constants import (
    SENSOR_ATMOSPHERIC_PRESSURE_KEY,
    SENSOR_ATMOSPHERIC_PRESSURE_LABEL,
    SENSOR_ATMOSPHERIC_PRESSURE_UNIT,
)
from airthings.models import Sensor


class AtmosphericPressureSensor(Sensor):
    KEY = SENSOR_ATMOSPHERIC_PRESSURE_KEY
    LABEL = SENSOR_ATMOSPHERIC_PRESSURE_LABEL
    UNIT = SENSOR_ATMOSPHERIC_PRESSURE_UNIT
    ALARM_RULES = None

    def __init__(self, value):
        super(AtmosphericPressureSensor, self).__init__(value)
