import errors
from IO.commiface import CommInterface, MessageType


class EncodersInterface:
    def __init__(self, comm_interface: CommInterface):
        self._comm_interface = comm_interface
        self._reset_command = 'R'

    def get_encoders_data(self):
        message = self._comm_interface.encode_message(MessageType.ENCODERS)
        response = self._comm_interface.write_message(message)

        return self._comm_interface.decode_message(response)

    def reset_encoders(self):
        message = self._comm_interface.encode_message(MessageType.ENCODERS, self._reset_command)
        response = self._comm_interface.write_message(message)

        if message == response:
            return True
        else:
            raise errors.InvalidMessageException
