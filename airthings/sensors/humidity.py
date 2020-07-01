from airthings.constants import (
    SENSOR_HUMIDITY_KEY,
    SENSOR_HUMIDITY_LABEL,
    SENSOR_HUMIDITY_UNIT,
)
from airthings.models import Sensor


class HumiditySensor(Sensor):
    KEY = SENSOR_HUMIDITY_KEY
    LABEL = SENSOR_HUMIDITY_LABEL
    UNIT = SENSOR_HUMIDITY_UNIT
    ALARM_RULES = None

    def __init__(self, value):
        super(HumiditySensor, self).__init__(value)
