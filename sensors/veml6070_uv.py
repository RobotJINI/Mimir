import board
import adafruit_veml6070


class LightSensor:
    def __init__(self):
        self._veml = adafruit_veml6070.VEML6070(board.I2C())
        
        self.uv = 0
        self.risk_level = 0
    
    def update(self):
        self.uv = self._veml.uv_raw
        self.risk_level = self._veml.get_index(self.uv)
