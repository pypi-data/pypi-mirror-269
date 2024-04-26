from phound import Phound
from phound.events import PlaybackStatus
from phound.handlers import BaseCallHandler



class CallHandler(BaseCallHandler):
    def on_incoming_call(self, call):
        self.answer()

    def on_call_answer(self, answer):
        # make sure the file could be found
        self.play("./service_data/guitar.g722")

    def on_playback(self, playback):
        if playback.status == PlaybackStatus.COMPLETE:
            self.record("./service_data/rec/recording.mp3")


if __name__ == "__main__":
    with Phound() as phound:
        phound.register_call_handler(CallHandler)
        phound.start_listen_events()
