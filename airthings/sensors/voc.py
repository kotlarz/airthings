from airthings.constants import (
    SENSOR_VOC_ALARM_RULES,
    SENSOR_VOC_KEY,
    SENSOR_VOC_LABEL,
    SENSOR_VOC_UNIT,
)
from airthings.models import Sensor


class VOCSensor(Sensor):
    KEY = SENSOR_VOC_KEY
    LABEL = SENSOR_VOC_LABEL
    UNIT = SENSOR_VOC_UNIT
    ALARM_RULES = SENSOR_VOC_ALARM_RULES

    def __init__(self, value):
        super(VOCSensor, self).__init__(value)
