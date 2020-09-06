class MockSerial:
    def __init__(self):
        self._sent_messages = []
        self._responses = []
        self.is_open = False

    def write(self, message):
        self._sent_messages.append(message.decode("ascii"))

    def readline(self):
        message = self._responses[0]
        self._responses.pop(0)
        return message

    def open(self):
        self.is_open = True
        pass

    def close(self):
        self.is_open = False
        pass

    def flush(self):
        pass

    def get_sent_message(self):
        message = self._sent_messages[0]
        self._sent_messages.pop(0)
        return message

    def add_response(self, response):
        self._responses.append(bytes(response, 'ascii'))
