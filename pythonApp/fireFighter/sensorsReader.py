import communicationHandler


class SensorsReader:
    def __init__(self, comm_handler: communicationHandler.CommunicationHandler):
        self._comm_handler = comm_handler

    """Reads data from all sensors at once."""
    def get_sensors_data(self):
        message = self._comm_handler.encode_message(self._comm_handler.sensors_data)
        print(message)
        response = self._comm_handler.write_message(message)
        print(response)

        sensors_data = response.split('\t')

        sensors_data_decoded = []
        for sensor_data in sensors_data:
            sensors_data_decoded.append(self._comm_handler.decode_message(sensor_data))

        return sensors_data_decoded
