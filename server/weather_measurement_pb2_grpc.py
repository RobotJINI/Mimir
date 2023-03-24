# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import model.weather_measurement_pb2 as weather__measurement__pb2


class WeatherServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_measurements = channel.unary_unary(
                '/mimir.WeatherServer/get_measurements',
                request_serializer=weather__measurement__pb2.MeasurementRequest.SerializeToString,
                response_deserializer=weather__measurement__pb2.MeasurementResponse.FromString,
                )
        self.get_current_weather = channel.unary_unary(
                '/mimir.WeatherServer/get_current_weather',
                request_serializer=weather__measurement__pb2.CurrentWeatherRequest.SerializeToString,
                response_deserializer=weather__measurement__pb2.CurrentWeatherResponse.FromString,
                )


class WeatherServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_measurements(self, request, context):
        """Sends a greeting
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def get_current_weather(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WeatherServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_measurements': grpc.unary_unary_rpc_method_handler(
                    servicer.get_measurements,
                    request_deserializer=weather__measurement__pb2.MeasurementRequest.FromString,
                    response_serializer=weather__measurement__pb2.MeasurementResponse.SerializeToString,
            ),
            'get_current_weather': grpc.unary_unary_rpc_method_handler(
                    servicer.get_current_weather,
                    request_deserializer=weather__measurement__pb2.CurrentWeatherRequest.FromString,
                    response_serializer=weather__measurement__pb2.CurrentWeatherResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'mimir.WeatherServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class WeatherServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_measurements(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mimir.WeatherServer/get_measurements',
            weather__measurement__pb2.MeasurementRequest.SerializeToString,
            weather__measurement__pb2.MeasurementResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def get_current_weather(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/mimir.WeatherServer/get_current_weather',
            weather__measurement__pb2.CurrentWeatherRequest.SerializeToString,
            weather__measurement__pb2.CurrentWeatherResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
