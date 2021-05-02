import serial


class LCD(object):
    PREFIX = 0xFE

    def __init__(self, device):
        self.device = device
        self.connection = None

    def configure(self):
        self.connection = serial.Serial(self.device, 9600, timeout=5)
        self.clear()

    def clear(self):
        self.execute_command(bytearray([0xFE, 0x51]))
        self.execute_command(bytearray([0xFE, 0x46]))

    def print(self, string):
        print(string)
        self.clear()

        if (len(string.split('\n')) > 1):
            parts = string.split('\n')
            self._print(parts[0])
            self._newline()
            self._print(parts[1])
        else:
            self._print(string)

    def _print(self, part):
        if len(part) > 20:  # Length of 1 line
            self.execute_command(part[0:20].encode())
            self._newline()
            part = part[20:]

        if len(part) > 20:  # Length still longer than 20
            part = part[:17] + '...'

        self.execute_command(part.encode())

    def _newline(self):
        self.execute_command(bytearray([0xFE, 0x45, 0x28]))  # Move to next line

    def execute_command(self, payload):
        self.connection.write(payload)
