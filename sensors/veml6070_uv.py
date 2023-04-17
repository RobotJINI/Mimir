import board
import adafruit_veml6070


class LightSensor:
    def __init__(self):
        try:
            self._veml = adafruit_veml6070.VEML6070(board.I2C())
        except Exception as error:
            print("Error initializing VEML6070 sensor: ", error)
            self._veml = None
        
        self.uv = 0
        self.risk_level = 0
    
    def update(self):
        try:
            self.uv = self._veml.uv_raw
            self.risk_level = self._veml.get_index(self.uv)
        except Exception as error:
            print("Error updating VEML6070 sensor: ", error)
