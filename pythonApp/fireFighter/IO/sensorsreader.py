from IO.commiface import CommInterface, MessageType


class SensorsReader:
    def __init__(self, comm_interface: CommInterface):
        self._comm_interface = comm_interface

    """Reads data from all sensors at once."""
    def get_sensors_data(self):
        message = self._comm_interface.encode_message(MessageType.SENSORS_DATA)
        response = self._comm_interface.write_message(message)

        sensors_data = response.split('\t')

        sensors_data_decoded = []
        for sensor_data in sensors_data:
            sensors_data_decoded.append(self._comm_interface.decode_message(sensor_data))

        return sensors_data_decoded
