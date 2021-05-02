from obswebsocket import obsws, requests


class OBS:
    def __init__(self, host, port, password):
        self.ws = obsws(host, port, password)

    def connect(self):
        self.ws.connect()

    def disconnect(self):
        self.ws.disconnect()

    def start_stream(self):
        if self._is_streaming():
            return True

        res = self._call(requests.StartStreaming())
        return res.status

    def stop_stream(self):
        if not self._is_streaming():
            return True

        res = self._call(requests.StopStreaming())
        return res.status

    def set_scene(self, name):
        res = self._call(requests.SetCurrentScene(name))

        return res.status

    def _is_streaming(self):
        res = self._call(requests.GetStreamingStatus())

        return res.getStreaming()

    def _call(self, req):
        return self.ws.call(req)
