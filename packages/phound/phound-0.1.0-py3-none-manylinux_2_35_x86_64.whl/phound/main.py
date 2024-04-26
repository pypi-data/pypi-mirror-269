from typing import Any, Dict, Optional
import threading
from uuid import uuid4

from phound.events import EventType, ChatType
from phound.event_listener import EventListener
from phound.server import Server
from phound.client import Client
from phound.logging import logger


class Phound:
    def __init__(self):
        self._server = Server()
        self._client = Client()
        self._chat_handlers = []
        self._call_handlers = []
        self._channel_threads = set()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop()

    def send_message(self, persona_uid: str, chat_id: str, text: str, app_meta: Optional[Dict[str, Any]] = None):
        self._client.send_message(persona_uid, chat_id, text, app_meta=app_meta)

    def register_chat_handler(self, handler, chat_types=(ChatType.PRIVATE,)):
        self._chat_handlers.append((handler, [ChatType(chat_type) for chat_type in chat_types]))

    def register_call_handler(self, handler):
        self._call_handlers.append(handler)

    def stop(self):
        logger.info("Gracefully stopping phound")
        self._client.shutdown()
        for t in self._channel_threads:
            t.join()
        self._client.stop()

    def start_listen_events(self):
        self._client.enable_channels()
        try:
            while True:
                # updating alive threads here is not ideal but seems optimal for now
                self._channel_threads = {t for t in self._channel_threads if t.is_alive()}
                conn = self._server.get_new_connection()
                logger.info(f"Got new connection: {conn}")
                thread = threading.Thread(target=self._start_listen_connection, args=(conn,), name=str(uuid4()))
                self._channel_threads.add(thread)
                thread.start()
        except KeyboardInterrupt:
            logger.info("Ctrl+C pressed, stopping listen events")

    def _start_listen_connection(self, conn):
        event_listener = EventListener(conn.file)
        channel = event_listener.wait_event(EventType.NEW_CHANNEL).body
        logger.info(f"Channel: {channel}")

        self._client.request_next_event(channel.id)
        start_event = event_listener.wait_event(accept_any=True)
        logger.info(f"Start event: {start_event}")
        if start_event.type == EventType.CHAT_MESSAGE:
            cls_handler = next((h[0] for h in self._chat_handlers if start_event.body.chat_type in h[1]), None)
            if cls_handler:
                try:
                    chat = cls_handler(start_event.body.chat_id,
                                       start_event.body.persona_uid,
                                       start_event.body.chat_type,
                                       channel.id,
                                       conn,
                                       self._client)
                    chat.start(start_event)
                except Exception as e:
                    logger.error(e, exc_info=True)
        elif start_event.type == EventType.CALL_INCOMING:
            cls_handler = next((h for h in self._call_handlers), None)
            if cls_handler:
                try:
                    call = cls_handler(start_event.body.id, channel.id, conn, self._client)
                    call.start(start_event)
                except Exception as e:
                    logger.error(e, exc_info=True)

        conn.close()
