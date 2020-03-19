from IO import communicationInterface


class EncodersInterface:
    def __init__(self, comm_interface: communicationInterface.CommunicationInterface):
        self._comm_interface = comm_interface

    def get_encoders_data(self):
        message = self._comm_interface.encode_message(self._comm_interface.encoders)
        response = self._comm_interface.write_message(message)

        return self._comm_interface.decode_message(response)

    def reset_encoders(self):
        message = self._comm_interface.encode_message(self._comm_interface.encoders, "R")
        response = self._comm_interface.write_message(message)

        if message == response:
            return True
        else:
            return False
