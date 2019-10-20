class FakeSerial:
    def __init__(self):
        self._messageReceived = ""
        self._messageToSend = ""

    def write(self, message):
        self._messageReceived = message

    def readline(self):
        return self._messageToSend

    def get_received_message(self):
        return self._messageReceived

    def set_message_to_send(self, message_to_send):
        self._messageToSend = message_to_send