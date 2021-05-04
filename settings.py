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

PROJECT_DIR = '~/streamer'  # The directory where this project lives
OBS_DIR = '~/obs'  # The directory where OBS expects its static files
USB_MOUNT_LOCATION = '/media/streamer'  # The location where USB devices get auto-mounted
