from threading import Thread
from time import sleep

from obswebsocket import requests

import settings
from controllers import OBS
from controllers.stream_status import StreamStatus

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)

obs.connect()
res = obs.get_stream_time()

# def show_stream_status():
#     while obs.is_streaming():
#         stream_time = obs.get_stream_time()
#         df = obs.get_stream_frame_drop()
#         reconnecting = obs.get_stream_reconnecting()
#         print(stream_time, df, reconnecting)
#         sleep(1)
#
# thread = Thread(target=show_stream_status)
# thread.start()
#

st = StreamStatus(obs, None)
st.run()

