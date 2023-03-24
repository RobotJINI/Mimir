from gpiozero import MCP3008


class WindDirectionSensor:
    def __init__(self):
        self._adc = MCP3008(channel=0)

        self.wind_direction = -1
        self._volts_to_degree = {0.82: 0.0,
                                 0.88: 22.5,
                                 0.72: 45.0,
                                 0.76: 67.5,
                                 0.39: 90.0,
                                 0.38: 90.0,
                                 0.41: 112.5,
                                 0.08: 135.0,
                                 0.07: 135.0,
                                 0.19: 157.5,
                                 0.13: 180.0,
                                 0.31: 202.5,
                                 0.23: 225.0,
                                 0.6: 247.5,
                                 0.55: 270.0,
                                 0.92: 292.5,
                                 0.91: 315.0,
                                 0.94: 337.5}
        self.values = []
        self.deg_values = []

    def update(self):

        dir_val = round(self._adc.value, 3)

        self.wind_direction = dir_val
        #todo: not working right, should do after grabbing from db
        #if dir_val in self._volts_to_degree:
        #    self.wind_direction = self._volts_to_degree[dir_val]
