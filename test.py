from obswebsocket import requests

import settings
from controllers import OBS

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)

obs.connect()
# obs._call(requests.SetStreamSettings(type="rtmp_common", settings={"key": settings.DEBUG_STREAM_KEY}, save=False))
print(obs._call(requests.StartStreaming(stream={"settings": {"key": settings.DEBUG_STREAM_KEY, "server": "x"}, "type": "rtmp_common"})))

# obs.start_stream()