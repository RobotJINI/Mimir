from concurrent import futures
import logging

import grpc
import time
import model.weather_measurement_pb2 as weather_measurement_pb2
import server.weather_measurement_pb2_grpc as weather_measurement_pb2_grpc
from model.database import WeatherDatabase


class WeatherServer(weather_measurement_pb2_grpc.WeatherServer):
    def __init__(self, port='50051'):
        self._port = port
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        weather_measurement_pb2_grpc.add_WeatherServerServicer_to_server(self.WeatherGrpcServer(), self._server)
        self._server.add_insecure_port('[::]:' + self._port)
        self._running = False

    def run(self):
        self._server.start()
        self._running = True
        while self._running:
            time.sleep(.1)

    def stop(self):
        self._running = False
        self._server.stop(None)


    class WeatherGrpcServer(weather_measurement_pb2_grpc.WeatherServer):
        def __init__(self):
            weather_measurement_pb2_grpc.WeatherServer.__init__(self)
            self._weather_db = WeatherDatabase()
            self._executor = futures.ThreadPoolExecutor(max_workers=10)
            

        def get_measurements(self, request, context):
            try:
                logging.debug('get_measurements')
                query_response = self._weather_db.get_historical_weather(request.start_time, request.end_time)
                logging.debug(f'query_response:{len(query_response)}')
                return self._query_to_measurement_response(query_response)
            except Exception as e:
                logging.error(f'Error get_measurements failed!\n{e}')
                return weather_measurement_pb2.MeasurementResponse()

        def _query_to_measurement_response(self, query_response):
            measurement_response = weather_measurement_pb2.MeasurementResponse()
            for db_measurement in query_response:
                proto_measurement = weather_measurement_pb2.Measurement(
                                        time=int(db_measurement['time']),
                                        air_temp=str(db_measurement['air_temp']),
                                        pressure=str(db_measurement['pressure']),
                                        humidity=str(db_measurement['humidity']),
                                        ground_temp=str(db_measurement['ground_temp']),
                                        uv=str(db_measurement['uv']),
                                        uv_risk_lv=str(db_measurement['uv_risk_lv']),
                                        wind_speed=str(db_measurement['wind_speed']),
                                        rainfall=str(db_measurement['rainfall']),
                                        rain_rate=str(db_measurement['rain_rate']),
                                        wind_dir=str(db_measurement['wind_dir'])
                                    )
                measurement_response.measurements.append(proto_measurement)

            return measurement_response
