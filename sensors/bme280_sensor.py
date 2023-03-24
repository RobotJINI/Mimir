import bme280
import smbus2

class AirSensor:
    def __init__(self, port=1, address=0x77, is_celsuis=False, precision=2):
        self._bus = smbus2.SMBus(port)
        self._address = address
        self._calibration_params = bme280.load_calibration_params(self._bus, address)
        self._is_celsuis = is_celsuis
        self._precision = precision

        self.humidity = 0
        self.pressure = 0
        self.temperature = 0

    def update(self):
        bme280_data = bme280.sample(self._bus, self._address, self._calibration_params)
        self.humidity  = round(bme280_data.humidity, self._precision)
        self.pressure  = round(bme280_data.pressure, self._precision)
        self.temperature = bme280_data.temperature if self._is_celsuis else self._convert_fahrenheit(bme280_data.temperature)
        self.temperature = round(self.temperature, self._precision)


    def _convert_fahrenheit(self, celsuis):
        return (celsuis * 9/5) + 32
