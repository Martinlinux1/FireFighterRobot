import communicationHandler


class Encoders:
    def __init__(self, comm_handler: communicationHandler.CommunicationHandler):
        self._comm_handler = comm_handler

    def get_encoders_data(self):
        message = self._comm_handler.encode_message(self._comm_handler.encoders)
        response = self._comm_handler.write_message(message)

        return self._comm_handler.decode_message(response)

    def reset_encoders(self):
        message = self._comm_handler.encode_message(self._comm_handler.encoders, "R")
        response = self._comm_handler.write_message(message)

        if message == response:
            return True
        else:
            return False
