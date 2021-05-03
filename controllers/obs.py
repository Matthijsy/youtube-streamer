from time import sleep

from obswebsocket import obsws, requests


class OBS:
    def __init__(self, host, port, password):
        self.ws = obsws(host, port, password)

    def connect(self):
        self.ws.connect()

    def disconnect(self):
        self.ws.disconnect()

    def start_stream(self):
        if self.is_streaming():
            return True

        res = self._call(requests.StartStreaming())
        return res.status

    def stop_stream(self):
        if not self.is_streaming():
            return True

        res = self._call(requests.StopStreaming())
        return res.status

    def get_stream_time(self):
        res = self._call(requests.GetStreamingStatus())

        if res.getStreaming():
            return res.getStreamTimecode().split('.')[0]

        return '00:00:00'

    def get_stream_frame_drop(self):
        res = self._call(requests.GetOutputInfo('simple_stream'))

        return res.getOutputInfo().get('droppedFrames')

    def get_stream_reconnecting(self):
        res = self._call(requests.GetOutputInfo('simple_stream'))

        return res.getOutputInfo().get('reconnecting')

    def is_streaming(self):
        res = self._call(requests.GetStreamingStatus())

        return res.getStreaming()

    def set_scene(self, name):
        res = self._call(requests.SetCurrentScene(name))

        return res.status

    def get_audio_volume(self, name):
        res = self._call(requests.GetVolume(name))

        return res.getVolume()

    def audio_fade_out(self, name, transition_time=2):
        volume = self.get_audio_volume(name)
        if transition_time > 0:
            steps = volume / transition_time / 10
        else:
            steps = volume

        for i in range((transition_time * 10) + 1):
            res_volume = volume - ((i + 1) * steps)
            self._call(requests.SetVolume(name, res_volume, False))
            sleep(0.1)

        return self.audio_mute(name) and self.get_audio_volume(name) == 0

    def audio_fade_in(self, name, transition_time=2):
        if not self.audio_unmute(name):
            return False

        volume = self.get_audio_volume(name)
        if transition_time > 0:
            steps = (1 - volume) / transition_time / 10
        else:
            steps = volume

        for i in range((transition_time * 10) + 1):
            res_volume = volume + ((i + 1) * steps)
            self._call(requests.SetVolume(name, res_volume, False))
            sleep(0.1)

        return self.get_audio_volume(name) == 1

    def audio_mute(self, name):
        res = self._call(requests.SetMute(name, True))

        return res.status

    def audio_unmute(self, name):
        res = self._call(requests.SetMute(name, False))

        return res.status

    def _call(self, req):
        return self.ws.call(req)
