from typing import Any, Dict, Optional
import os
import subprocess
import json
import threading
from pathlib import Path

from phound import exceptions
from phound.events import EventType, Message
from phound.event_listener import EventListener
from phound.logging import logger, get_logging_parameters


_HEALTH_CHECK_INTERVAL_SECONDS = 5
lock = threading.Lock()


class Client:
    def __init__(self):
        self._sbc = os.environ.get("SBC")
        self._uid = os.environ.get("UID")
        self._token = os.environ.get("TOKEN")

        self._process = self._create_process()
        self._event_listener = EventListener(self._process.stdout)

        self._connect(self._sbc, self._uid, self._token)

        self._health_check_thread = _HealthCheckThread(target=self._restart_not_running_process)
        self._health_check_thread.start()
        self._channels_enabled = False

    def stop(self):
        self._health_check_thread.stop()
        self._health_check_thread.join()
        self._destroy_process()

    def send_message(self,
                     persona_uid: str,
                     chat_id: str,
                     text: str,
                     app_meta: Optional[Dict[str, Any]] = None,
                     channel_id: int = 0,
                     wait_sent: bool = True) -> Optional[Message]:
        message_json = {
            "text": text,
            "chan": channel_id,
            "wait": wait_sent,
        }
        if app_meta:
            message_json["app_meta"] = json.dumps(app_meta)

        self._write(f"send-message-json {persona_uid} {chat_id} {channel_id} <<JSON\n{json.dumps(message_json)}")
        if wait_sent and channel_id == 0:
            chat_event = self._event_listener.wait_event(EventType.CHAT_MESSAGE_SENT, EventType.INVALID_CHAT)
            if chat_event.type == EventType.INVALID_CHAT:
                raise exceptions.InvalidChatError(chat_event.body)
            return chat_event.body
        return None

    def answer_call(self, call_id):
        self._write(f"answer {call_id}")

    def play_file(self, call_id, file_path):
        self._write(f"play {call_id} {file_path}")

    def hangup(self, call_id):
        self._write(f"hangup {call_id}")

    def show_typing(self, persona_uid, chat_id, timeout=10, channel_id=0):
        self._write(f"typing-indicator {persona_uid} {chat_id} {timeout} {channel_id}")

    def request_chat_history(self, persona_uid, chat_id, start_message_id, channel_id=0, depth=10):
        self._write(f"get-history-bulk {persona_uid} {chat_id} {start_message_id} {channel_id} {depth}")

    def request_next_event(self, channel_id):
        self._write(f"pump-queue {channel_id}")

    def shutdown(self):
        self._write("shutdown")

    def enable_channels(self):
        self._channels_enabled = True
        self._write("set-handler channel 127.0.0.1:24000")

    def _connect(self, sbc, uid, token):
        self._write(f"connect {sbc} {uid} {token}", log=False)
        self._event_listener.wait_event(EventType.CONNECTED)

    def _create_process(self):
        cmd = [f"{Path(__file__).parent.resolve()}/bin/uccrobot", "-e", "-q"]

        is_logging_enabled, log_file_dir = get_logging_parameters()
        if not is_logging_enabled:
            cmd.append("-q")
        elif log_file_dir:
            cmd.extend(["-l", log_file_dir])
        cmd.append("-")

        # pylint: disable=W1509
        return subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # this is required in order not to receive parent's signals eg SIGINT
            preexec_fn=os.setpgrp,
            encoding="utf-8",
            bufsize=0
        )

    def _destroy_process(self):
        self._process.stdin.close()
        self._process.stdout.close()
        self._process.wait()
        logger.info("UCC client process destroyed")

    def _write(self, cmd, log=True):
        if log:
            logger.info(f"Sending cmd '{cmd}' to ucc")
        with lock:
            self._process.stdin.write(cmd + os.linesep)

    def _restart_not_running_process(self):
        while not self._health_check_thread.stopped():
            if self._process.poll() is not None:
                logger.error("Found UCC client process died, restarting")
                self._process = self._create_process()
                self._connect(self._sbc, self._uid, self._token)
                if self._channels_enabled:
                    self.enable_channels()
            self._health_check_thread.wait(_HEALTH_CHECK_INTERVAL_SECONDS)


class _HealthCheckThread(threading.Thread):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def wait(self, timeout):
        self._event.wait(timeout)

    def stopped(self):
        return self._event.is_set()
