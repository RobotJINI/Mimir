from sensors.button_sensor import ButtonSensor
import math


class RainSensor(ButtonSensor):
    def __init__(self, sensor_volume=.2794, button=6, precision=4):
        ButtonSensor.__init__(self, button)

        self.rainfall = -1
        self.rain_rate = -1
        self._sensor_volume = sensor_volume
        self._precision = precision

    def update(self):
        rain_count, interval_sec = self._get_and_reset()
        self.rainfall = rain_count * self._sensor_volume #mm
        self.rain_rate = self.rainfall / interval_sec #mm/sec

        self.rainfall = round(self.rainfall, self._precision)
        self.rain_rate = round(self.rain_rate, self._precision)
