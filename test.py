from threading import Thread
from time import sleep

from obswebsocket import requests

import settings
from controllers import OBS
from controllers.stream_status import StreamStatus

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)

obs.connect()

print(obs._call(requests.GetTransitionList()))

res = obs.transition_to_program(transition_name="Cut", transition_duration=500)



