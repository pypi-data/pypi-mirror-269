from typing import Any, Dict, Optional
import abc

from phound.events import EventType
from phound.event_listener import EventListener
from phound.logging import logger


class BaseHandler(metaclass=abc.ABCMeta):
    def __init__(self, channel_id, conn, client):
        self._channel_id = channel_id
        self._event_listener = EventListener(conn.file)
        self._client = client
        self._is_active = True

    def start(self, start_event):
        handler = self._get_event_handler(start_event)
        if handler is not None:
            handler(start_event.body)

        while self._is_active:
            self._client.request_next_event(self._channel_id)
            event = self._event_listener.wait_event(accept_any=True)

            logger.info(f"Got new event in channel with id {self._channel_id}: {event}")
            if event.type == EventType.CLOSE_CHANNEL:
                self._is_active = False
            else:
                handler = self._get_event_handler(event)
                if handler is not None:
                    handler(event.body)
        logger.info(f"Channel with id {self._channel_id} closed")

    @abc.abstractmethod
    def _get_event_handler(self, event):
        pass


class BaseChatHandler(BaseHandler):
    _SYSTEM_MESSAGE_FROM_UID = "0"

    def __init__(self, chat_id, persona_uid, chat_type, channel_id, conn, client):
        self.persona_uid = persona_uid
        self.chat_type = chat_type
        self._chat_id = chat_id
        super().__init__(channel_id, conn, client)

    def on_message(self, message):
        pass

    def show_typing(self, timeout: int = 60):
        self._client.show_typing(self.persona_uid, self._chat_id, timeout, self._channel_id)

    def send_message(self, text: str, app_meta: Optional[Dict[str, Any]] = None):
        self._client.send_message(
            self.persona_uid, self._chat_id, text, app_meta=app_meta, channel_id=self._channel_id)
        return self._event_listener.wait_event(EventType.CHAT_MESSAGE_SENT).body

    def get_history(self, depth: int = 10, start_message_id: str = "0"):
        self._client.request_chat_history(self.persona_uid, self._chat_id, start_message_id, self._channel_id, depth)
        return self._event_listener.wait_event(EventType.CHAT_HISTORY).body

    def _get_event_handler(self, event):
        if event.type == EventType.CHAT_MESSAGE:
            message = event.body
            if message.from_uid in (self.persona_uid, self._SYSTEM_MESSAGE_FROM_UID):
                return None
            return self.on_message
        return None


class BaseCallHandler(BaseHandler):
    def __init__(self, call_id, channel_id, conn, client):
        self._call_id = call_id
        super().__init__(channel_id, conn, client)

    def on_incoming_call(self, call):
        pass

    def on_call_answer(self, answer):
        pass

    def on_playback(self, playback):
        pass

    def answer(self):
        self._client.answer_call(self._call_id)

    def play(self, file_path):
        self._client.play_file(self._call_id, file_path)

    def hangup(self):
        self._client.hangup(self._call_id)

    def _get_event_handler(self, event):
        if event.type == EventType.CALL_INCOMING:
            return self.on_incoming_call
        if event.type == EventType.CALL_ANSWER:
            return self.on_call_answer
        if event.type == EventType.PLAYBACK_STATUS:
            return self.on_playback
        return None
