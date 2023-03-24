from sensors.bme280_sensor import AirSensor
from sensors.ds18b20_therm import GroundSensor
from sensors.veml6070_uv import LightSensor
from sensors.wind import WindSensor
from sensors.rain import RainSensor
from sensors.wind_direction import WindDirectionSensor
from model.database import WeatherDatabase
from server.server import WeatherServer

import logging
import os
import time
from datetime import datetime
from threading import Thread


class Mimir:
    def __init__(self):
        self._running = True
        self._interval = 10000

        self._air_sensor = AirSensor()
        self._ground_sensor = GroundSensor()
        self._light_sensor = LightSensor()
        self._wind_sensor = WindSensor()
        self._rain_sensor = RainSensor()
        self._wind_direction_sensor = WindDirectionSensor()

        self._weather_database = WeatherDatabase()
        self._weather_server = WeatherServer()

        self._wind_thread = None
        self._rain_thread = None
        self._weather_server_thread = None
        self._last_recorded_time = None

    def run(self):
        logging.info('Running ....')

        self._start_sensors()

        while self._running:
            time_ms = self._get_time_ms()
            if self._last_recorded_time is None or (time_ms - self._last_recorded_time) >= self._interval:
                self._update()
                self._record(time_ms)
                self._last_recorded_time = time_ms

            time.sleep(.1)

    def stop(self):
        logging.info('Stopping ....')
        self._weather_server.stop()
        self._wind_sensor.stop()
        self._rain_sensor.stop()

        self._weather_server_thread.join()
        self._wind_thread.join()
        self._rain_thread.join()
        logging.info('Done!')

    def _start_sensors(self):
        self._wind_thread = Thread(target=self._wind_sensor.run)
        self._wind_thread.start()

        self._rain_thread = Thread(target=self._rain_sensor.run)
        self._rain_thread.start()

        self._weather_server_thread = Thread(target=self._weather_server.run)
        self._weather_server_thread.start()

    def _update(self):
        logging.debug('self._air_sensor.update()')
        self._air_sensor.update()

        logging.debug('self._ground_sensor.update()')
        self._ground_sensor.update()

        logging.debug('self._light_sensor.update()')
        self._light_sensor.update()

        logging.debug('self._wind_sensor.update()')
        self._wind_sensor.update()

        logging.debug('self._rain_sensor.update()')
        self._rain_sensor.update()

        logging.debug('self._wind_direction_sensor.update()')
        self._wind_direction_sensor.update()

    def _record(self, time_ms):
        self._weather_database.insert(time_ms, self._air_sensor.temperature, self._air_sensor.pressure, self._air_sensor.humidity,
                                      self._ground_sensor.temperature, self._light_sensor.uv, self._light_sensor.risk_level, self._wind_sensor.wind_speed,
                                      self._rain_sensor.rainfall, self._rain_sensor.rain_rate, self._wind_direction_sensor.wind_direction)

    def _get_time_ms(self):
        return int(time.time() * 1000)


def main():
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)
        
    log_filename = datetime.now().strftime(os.path.join('logs', 'mimir_%Y-%m-%d_%H-%M-%S.log'))
    logging.basicConfig(filename=log_filename, format='%(message)s', level=logging.DEBUG)
    
    mimir = Mimir()

    try:
        mimir.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    mimir.stop()

if __name__ == '__main__':
    main()
