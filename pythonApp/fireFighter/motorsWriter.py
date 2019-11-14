import communicationHandler
import errors


class MotorsWriter:
    def __init__(self, comm_handler: communicationHandler.CommunicationHandler):
        self._comm_handler = comm_handler

    """Turns on a motor."""

    def write_motor(self, motor, direction, speed):
        # Construct the request.
        motors_data = motor + "," + direction + "," + str(speed)

        message = self._comm_handler.encode_message(self._comm_handler.motor, motors_data)

        # Send request and wait for response.
        response = self._comm_handler.write_message(message)

        # If the response is valid, return true.
        if response == message:
            return True
        # Invalid response.
        else:
            raise errors.InvalidMessageException
