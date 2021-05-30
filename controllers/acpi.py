import socket

import settings


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
        if settings.DEBUG_MODE:
            self._wait_enter()
        else:
            self._wait_button(timeout)

    def _wait_button(self, timeout):
        self.s.settimeout(timeout)
        while True:
            event = self.s.recv(4096).decode('utf-8').split(' ')

            if event[0] == 'button/power' and event[1] == 'PBTN':
                return True

    def _wait_enter(self):
        input("Press enter to continue..")
