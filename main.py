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


def init():
    # Pull the git repo, to have new changes
    if os.system(f'cd {settings.PROJECT_DIR} && git pull') > 0:
        print("Git pull failed...")

    # Copy the needed OBS files
    if os.system(f'cp {settings.PROJECT_DIR}/obs_files/* {settings.OBS_DIR}') > 0:
        print("Updating OBS files failed")

    # If there are OBS files on the plugged in USB devices, overwrite the files
    if os.system(f'cp {settings.USB_MOUNT_LOCATION}/**/obs_studio/* {settings.OBS_DIR}'):
        print('Copying from USB device failed')


def connect_obs():
    lcd.print("Connecting to OBS...")
    for i in range(6):
        try:
            obs.connect()
            obs.audio_fade_out(settings.SERVICE_AUDIO, 0)
            obs.studio_mode()
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
    if not obs.set_scene(settings.PRE_SERVICE_SCENE):
        lcd.print("Failed change scene")
        exit(0)
    if not obs.audio_fade_in(settings.PRE_SERVICE_AUDIO, 0):
        lcd.print("Failed fade in audio")
        exit(0)
    if not obs.start_stream():
        lcd.print("Failed start stream")
        exit(0)

    lcd.print("Pre service image")


def start_record():
    lcd.print("Starting recording...\n ")
    if not obs.start_record():
        lcd.print("Failed to start recording")
        exit(1)


def start_live_video():
    lcd.print("Starting live video")
    if not obs.audio_fade_out(settings.PRE_SERVICE_AUDIO):
        lcd.print("Failed fade out audio")
        exit(0)
    if not obs.set_preview_scene(settings.SERVICE_SCENE):
        lcd.print("Failed change scene")
        exit(0)
    if not obs.transition_to_program(transition_name="Fade", transition_duration=settings.TRANSITION_DURATION):
        lcd.print("Failed to transition")
        exit(0)
    if not obs.audio_fade_in(settings.SERVICE_AUDIO):
        lcd.print("Failed fade in audio")
        exit(0)

    lcd.print("Streaming live video")


# Wait for network connetion
lcd.print("Waiting for network")
while os.system('ping  -w 1 8.8.8.8') > 0:
    sleep(1)

# Init some files
init()

# Start OBS
connect_obs()

# Wait for click, then go live with pre-service image
acpi.wait_power_button()
start_stream()

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

# TODO create fade to black
# if not obs.transition_to_program(transition_name="Fade to black", transition_duration=settings.TRANSITION_DURATION):
#     lcd.print("Failed fade black")
#     exit(0)

if not obs.stop_stream():
    lcd.print("Failed to stop stream")
    exit(0)

lcd.print("Shutdown..")
sleep(2)
obs.disconnect()
lcd.clear()

if not settings.DEBUG_MODE:
    os.system("sudo shutdown now")
