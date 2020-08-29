from airthings.constants import (
    SENSOR_RADON_ALARM_RULES,
    SENSOR_RADON_LONG_TERM_AVG_KEY,
    SENSOR_RADON_LONG_TERM_AVG_LABEL,
    SENSOR_RADON_UNIT,
)
from airthings.models import Sensor


class RadonLongTermAverageSensor(Sensor):
    KEY = SENSOR_RADON_LONG_TERM_AVG_KEY
    LABEL = SENSOR_RADON_LONG_TERM_AVG_LABEL
    UNIT = SENSOR_RADON_UNIT
    ALARM_RULES = SENSOR_RADON_ALARM_RULES

    def __init__(self, value):
        super(RadonLongTermAverageSensor, self).__init__(value)
