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

    def print(self, string, line=None):
        print(string)
        self.clear()

        if line:
            self._print(string, line)

        if len(string.split('\n')) > 1:
            parts = string.split('\n')
            self._print(parts[0], 0)
            self._print(parts[1], 1)
        else:
            if len(string) > 20:
                string = string[:20] + "\n" + string[20:]
                self.print(string)
            else:
                self._print(string)

    def _print(self, part, line=0):
        if line == 1:
            self._newline()

        self.execute_command(part.encode())

    def _newline(self):
        self.execute_command(bytearray([0xFE, 0x45, 0x28]))  # Move to next line

    def execute_command(self, payload):
        self.connection.write(payload)
