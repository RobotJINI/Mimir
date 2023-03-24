import MySQLdb, datetime, http.client, json, os
import io
import math
import logging
import threading


class MysqlDatabase:
    def __init__(self, credentials):
        self._credentials = credentials

    def execute(self, query, params=[]):
        try:
            connection = MySQLdb.connect(user=self._credentials["USERNAME"], password=self._credentials["PASSWORD"], database=self._credentials["DATABASE"])
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            connection.close()
        except Exception as e:
            connection.rollback()
            connection.close()
            logging.error(f'Failed to execute query: {query} with params {params}. Error: {e}')
            raise

    def query(self, query, params=[]):
        try:
            connection = MySQLdb.connect(user=self._credentials["USERNAME"], password=self._credentials["PASSWORD"], database=self._credentials["DATABASE"])
            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query, params)
            result = cursor.fetchall()
            connection.close()
            return result
        except Exception as e:
            connection.close()
            logging.error(f'Failed to execute query: {query} with params {params}. Error: {e}')
            raise


class WeatherDatabase:
    def __init__(self):
        self._insert_template = 'INSERT INTO weather_measurement (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, ' + \
                                'rain_rate, wind_dir) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'

        self._historical_weather_template = 'SELECT time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir ' + \
                                            'FROM weather_measurement ' + \
                                            'WHERE time BETWEEN %s AND %s LIMIT %s;'
                                          
        self._limit = 2000
        credentials_file = os.path.join(os.path.dirname(__file__), "../config/credentials.mysql")                                  
        self._credentials = self._load_credentials(credentials_file)
        self._db = MysqlDatabase(self._credentials)
                                          
    def _load_credentials(self, credentials_file):
        try:
            with open(credentials_file, 'r') as f:
                credentials = json.load(f)
            for key, value in credentials.items():
                credentials[key] = value.strip()  # remove leading/trailing whitespace
            return credentials
        except FileNotFoundError:
            logging.error(f'Credentials file \'{credentials_file}\' does not exist. Creating a new one, please modify password...')
            with open(credentials_file, 'w') as f:
                credentials = {'USERNAME': 'mimir', 'PASSWORD': '*******', 'DATABASE': 'weather'}
                json.dump(credentials, f)
            sys.exit(1)

    def insert(self, time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir):
        params = (time, air_temp, pressure, humidity, ground_temp, uv, uv_risk_lv, wind_speed, rainfall, rain_rate, wind_dir)
        logging.debug(self._insert_template % params)
        self._db.execute(self._insert_template, params)

    def get_historical_weather(self, start_time, end_time):
        params = (start_time, end_time, self._limit)
        logging.debug(self._historical_weather_template % params)
        return self._db.query(self._historical_weather_template, params)
