import os
import socket
from time import sleep

from obswebsocket.exceptions import ConnectionFailure

import settings
from controllers import OBS, LCD, ACPI
from controllers.stream_status import StreamStatus

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)
acpi = ACPI()
lcd = LCD('/dev/ttyUSB0')
lcd.configure()
should_record = False


def connect_obs():
    lcd.print("Connecting to OBS...")
    for i in range(6):
        try:
            obs.connect()
            obs.audio_fade_out(settings.SERVICE_AUDIO, 0)
            lcd.print("OBS started..\n Press to go live")
            return True
        except ConnectionFailure as e:
            sleep(5)
            lcd.print(f"Connecting to OBS...\n Retry {i}")
    else:
        lcd.print("Can't connect to OBS\n ")
        exit(0)


def start_stream():
    lcd.print("Starting stream...\n ")
    if obs.set_scene(settings.PRE_SERVICE_SCENE) and \
            obs.audio_fade_in(settings.PRE_SERVICE_AUDIO) and \
            obs.start_stream():
        lcd.print("Pre service image")
    else:
        lcd.print("Failed to start OBS")
        exit(1)


def start_record():
    lcd.print("Starting recording...\n ")
    if not obs.start_record():
        lcd.print("Failed to start recoring")
        exit(1)


def start_live_video():
    lcd.print("Starting live video")
    if obs.audio_fade_out(settings.PRE_SERVICE_AUDIO) and \
            obs.set_scene(settings.SERVICE_SCENE) and \
            obs.audio_fade_in(settings.SERVICE_AUDIO):
        lcd.print("Streaming live video")
    else:
        lcd.print("Failed to change scene")
        exit(0)


# Start OBS
connect_obs()

# Wait for click, then go live with pre-service image
acpi.wait_power_button()
start_stream()

# Check for recording
if os.system(f'lsusb | grep "{settings.USB_DEVICE}"') == 0:
    should_record = True
    start_record()

# Start monitoring the stream
StreamStatus(obs, lcd).start()

# Wait for click then go live with live video
acpi.wait_power_button()
start_live_video()

# Wait for two clicks before stopping the stream
while True:
    acpi.wait_power_button()
    try:
        lcd.print("Press to confirm")
        acpi.wait_power_button(timeout=10)
        break
    except socket.timeout:
        lcd.print("Streaming live video")

if not obs.stop_stream():
    lcd.print("Failed to stop stream")
    exit(0)

if should_record and not obs.stop_record():
    lcd.print("Failed to stop recording")
    exit(0)

lcd.print("Shutdown..")
sleep(2)
obs.disconnect()
lcd.clear()
# os.system("sudo shutdown now")
