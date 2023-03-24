from sensors.button_sensor import ButtonSensor
import math


class WindSensor(ButtonSensor):
    def __init__(self, radius_cm=9.0, button=5, precision=4):
        ButtonSensor.__init__(self, button)

        self.wind_speed = -1
        self._radius_cm = radius_cm
        self._precision = precision

    def update(self):
        wind_count, interval_sec = self._get_and_reset()
        self.wind_speed = self._get_speed(wind_count, interval_sec)

    def _get_speed(self, wind_count, interval_sec):
        circumference_cm = (2 * math.pi) * self._radius_cm
        rotations = wind_count / 2.0
        dist_meters = (circumference_cm * rotations) / 100
        speed = dist_meters / interval_sec

        return round(speed, self._precision)
    
