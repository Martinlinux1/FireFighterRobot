class MockEncodersIface:
    def __init__(self):
        self._encoders_values = []
        self._is_reset = False

    def get_encoders_data(self):
        return self._encoders_values

    def reset(self):
        self._is_reset = True

    def set_encoders_data(self, values):
        self._encoders_values = values

    def is_reset(self):
        if self._is_reset:
            self._is_reset = False
            return True
        else:
            return False
