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

    def clear_line(self, line):
        # Move cursors and then backspace
        cursor = 0x14 if line == 0 else 0x3C
        self.execute_command(bytearray([0xFE, 0x45, cursor]))
        for _ in range(20):
            self.execute_command(bytearray([0xFE, 0x4E]))

    def print(self, string, line=None):
        if line:
            self._newline()
            self.execute_command(self._padded_string(string).encode())
            print(string)
        else:
            if len(string.split('\n')) > 1:
                parts = string.split('\n')
                self.print(parts[0], 0)
                self.print(parts[1], 1)
            elif len(string) > 20:
                self.print(string[:20], 0)
                self.print(string[20:], 1)
            else:
                self.execute_command(self._padded_string(string).encode())
                print(string)

    def _padded_string(self, string):
        # Make sure the string is exactly 20 characters, to fill the screen
        if len(string) > 20:
            return string[:17] + "..."
        elif len(string) == 20:
            return string
        else:
            return f"{string:20}"

    def _newline(self):
        self.execute_command(bytearray([0xFE, 0x45, 0x28]))  # Move to next line

    def execute_command(self, payload):
        self.connection.write(payload)
