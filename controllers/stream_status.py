import os
from threading import Thread
from time import sleep


class StreamStatus(Thread):

    def __init__(self, obs, lcd):
        super().__init__()
        self.obs = obs
        self.lcd = lcd
        self._dropped_frames = []  # Array to list the amount of dropped frames in the last minute
        self._last_df_value = 0

    def run(self):
        while self.obs.is_streaming():
            stream_time = self.obs.get_stream_time()
            dropped_frames = self.obs.get_stream_frame_drop()
            reconnecting = self.obs.get_stream_reconnecting()

            if not self._check_status(dropped_frames, reconnecting):
                os.system("sudo env -i beep")

            if not reconnecting:
                status_str = f"{stream_time:<8} {dropped_frames:>11}"
            else:
                status_str = "Reconnecting..."
            self.lcd.print(status_str, line=1)
            sleep(1)

    def _check_status(self, dropped_frames, reconnecting):
        if reconnecting:
            return False

        df_total = self._calculate_df(dropped_frames)  # Total dropped frames of last 30 seconds
        return df_total < 30 * 10  # If we dropped at least 10 seconds

    def _calculate_df(self, dropped_frames):
        df_size = len(self._dropped_frames)
        # If we have more than a half a minute of information
        if df_size > 30:
            self._dropped_frames.pop(0)  # Pop the oldest item

        # Write the diff to the end of the list
        self._dropped_frames.append(dropped_frames - self._last_df_value)
        self._last_df_value = dropped_frames

        return sum(self._dropped_frames)
