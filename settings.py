import os

from dotenv import load_dotenv

load_dotenv()

HOST = "localhost"
PORT = 4444
PASSWORD = os.environ.get('OBS_PASSWORD')

PRE_SERVICE_SCENE = 'Pre-Service'
SERVICE_SCENE = 'Live'

PRE_SERVICE_AUDIO = 'Intro media'
SERVICE_AUDIO = 'Audio Input'

USB_DEVICE = 'Bus 002 Device 011'  # The name in the lsusb command
