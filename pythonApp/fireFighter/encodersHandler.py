from hardwarehandler import HardwareHandler


class EncodersHandler(HardwareHandler):
    def __init__(self, encoders_reader):
        super().__init__(encoders_reader, True)

    def update(self):
        if self._update.poll():
            if self._update.recv() == 'R':
                self._hardware.reset_encoders()

        if self._event.is_set():
            self._event.clear()
            encoders_data = self._hardware.get_encoders_data()[1]

            self._update.send(encoders_data)

    def reset(self):
        super().set('R')
        super().write()

