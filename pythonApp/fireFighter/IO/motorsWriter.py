from IO import communicationInterface
import errors


class MotorsWriter:
    def __init__(self, comm_interface: communicationInterface.CommunicationInterface):
        self._comm_interface = comm_interface

    """Turns on a motor."""

    def write_motor(self, motor, direction, speed):
        # Construct the request.
        motors_data = motor + "," + direction + "," + str(speed)

        message = self._comm_interface.encode_message(self._comm_interface.motor, motors_data)

        # Send request and wait for response.
        response = self._comm_interface.write_message(message)

        # If the response is valid, return true.
        if response == message:
            return True
        # Invalid response.
        else:
            raise errors.InvalidMessageException

    def brake(self):
        message = self._comm_interface.encode_message(self._comm_interface.motors_brake)

        response = self._comm_interface.write_message(message)

        if response == message:
            return True
        else:
            raise errors.InvalidMessageException
