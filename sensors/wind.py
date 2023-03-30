from sensors.button_sensor import ButtonSensor
import math


class WindSensor(ButtonSensor):
    def __init__(self, button=5, precision=4):
        ButtonSensor.__init__(self, button)

        self.wind_speed = -1
        self._mph_per_tick_sec = 1.492
        self._precision = precision

    def update(self):
        wind_count, interval_sec = self._get_and_reset()
        self.wind_speed = (wind_count / interval_sec) * self._mph_per_tick_sec
    