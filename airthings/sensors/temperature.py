from airthings.constants import (
    SENSOR_TEMPERATURE_ALARM_RULES,
    SENSOR_TEMPERATURE_KEY,
    SENSOR_TEMPERATURE_LABEL,
    SENSOR_TEMPERATURE_UNIT,
)
from airthings.models import Sensor


class TemperatureSensor(Sensor):
    KEY = SENSOR_TEMPERATURE_KEY
    LABEL = SENSOR_TEMPERATURE_LABEL
    UNIT = SENSOR_TEMPERATURE_UNIT
    ALARM_RULES = SENSOR_TEMPERATURE_ALARM_RULES

    def __init__(self, value):
        super(TemperatureSensor, self).__init__(value)
