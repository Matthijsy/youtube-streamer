from time import sleep

import settings
from controllers import OBS

obs = OBS(settings.HOST, settings.PORT, settings.PASSWORD)

obs.connect()
print(obs.audio_fade_in('Desktop Audio'))


sleep(2)
print(obs.audio_fade_out('Desktop Audio'))