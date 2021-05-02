import socket


class ACPI:
    """
      Class to interact with the ACPI socket
      The ACPID services relays all the ACPI messages onto a socket which can then be listened to
      This is used to detect power button actions
    """

    def __init__(self):
        self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.s.connect('/var/run/acpid.socket')

    def wait_power_button(self, timeout=None):
        input('enter...')
        return
        self.s.settimeout(timeout)
        while True:
            event = self.s.recv(4096).decode('utf-8').split(' ')

            if event[0] == 'button/power' and event[1] == 'PBTN':
                return True
