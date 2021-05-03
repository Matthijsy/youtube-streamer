import serial

PREFIX = 0xFE
LINE_START = [0x0, 0x28]
LINE_END = [0x14, 0x32]


class LCD(object):

    def __init__(self, device):
        self.device = device
        self.connection = None

    def configure(self):
        self.connection = serial.Serial(self.device, 9600, timeout=5)
        self.clear()

    def clear(self):
        self.print("")

    def print(self, string, line=None):
        if line:
            self._set_cursor_start(line)
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
                self._set_cursor_start(0)
                self.execute_command(self._padded_string(string).encode())
                self.print(self._padded_string(""), 1)
                print(string)

    def _padded_string(self, string):
        # Make sure the string is exactly 20 characters, to fill the screen
        if len(string) > 20:
            return string[:17] + "..."
        elif len(string) == 20:
            return string
        else:
            return f"{string:20}"

    def _set_cursor_start(self, line):
        self.execute_command(bytearray([0xFE, 0x45, LINE_START[line]]))  # Move to next line

    def execute_command(self, payload):
        self.connection.write(payload)
