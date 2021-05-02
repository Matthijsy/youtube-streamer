import os
import socket
from time import sleep

from obswebsocket.exceptions import ConnectionFailure

import settings
from controllers import OBS, LCD, ACPI

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)
acpi = ACPI()
lcd = LCD('/dev/ttyUSB0')
lcd.configure()


def connect_obs():
    lcd.print("Connecting to OBS...")
    for i in range(3):
        try:
            obs.connect()
            obs.audio_fade_out(settings.SERVICE_AUDIO, 0)
            lcd.print("OBS started..\n Press to go live")
            return True
        except ConnectionFailure as e:
            sleep(10)
            lcd.print(f"Connecting to OBS...\n Retry {i}")
    else:
        lcd.print("Can't connect to OBS")
        exit(0)


def start_stream():
    lcd.print("Starting stream...")
    if obs.set_scene(settings.PRE_SERVICE_SCENE) and \
            obs.audio_fade_in(settings.PRE_SERVICE_AUDIO) and \
            obs.start_stream():
        lcd.print("Current->Pre-service \n Next->Live video")
    else:
        lcd.print("Failed to start OBS")
        exit(1)


def start_live_video():
    lcd.print("Starting live video")
    if obs.audio_fade_out(settings.PRE_SERVICE_AUDIO) and \
            obs.set_scene(settings.SERVICE_SCENE) and \
            obs.audio_fade_in(settings.SERVICE_AUDIO):
        lcd.print("Current->Live video\n Next->End ")
    else:
        lcd.print("Failed to change scene")
        exit(0)


# Start OBS
connect_obs()

# Wait for click, then go live with pre-service image
acpi.wait_power_button()
start_stream()

# Wait for click then go live with live video
acpi.wait_power_button()
start_live_video()

# Wait for two clicks before stopping the stream
while True:
    acpi.wait_power_button()
    try:
        lcd.print("Want to stop stream?\nPress to confirm")
        acpi.wait_power_button(timeout=10)
        break
    except socket.timeout:
        lcd.print("Current->Live video\n Next->End ")

if not obs.stop_stream():
    lcd.print("Failed to stop stream")
    exit(0)

obs.disconnect()
lcd.clear()
os.system("sudo shutdown now")
