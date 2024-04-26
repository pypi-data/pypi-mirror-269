import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from phound.logging import logger
from phound import exceptions


class EventType(str, Enum):
    CONNECTED = "Connected"
    NEW_CHANNEL = "NewChannel"
    CLOSE_CHANNEL = "CloseChannel"
    ERROR = "Error"

    CHAT_MESSAGE = "ChatMessage"
    CHAT_MESSAGE_SENT = "ChatMessageSent"
    CHAT_HISTORY = "ChatHistoryBulk"
    INVALID_CHAT = "InvalidChat"

    CALL_INCOMING = "CallIncoming"
    CALL_ANSWER = "CallAnswer"
    PLAYBACK_STATUS = "PlaybackStatus"
    CALL_HANGUP = "CallHangup"


class PlaybackStatus(str, Enum):
    IN_PROGRESS = "inprogress"
    COMPLETE = "complete"


class ChatType(str, Enum):
    PRIVATE = "private"
    GROUP = "group"


@dataclass(frozen=True)
class NewChannel:
    id: str

@dataclass(frozen=True)
class Message:
    id: str
    text: str
    from_uid: str
    tagged: bool
    persona_uid: str
    chat_id: str
    chat_type: ChatType


@dataclass(frozen=True)
class Call:
    id: str


@dataclass(frozen=True)
class CallAnswer:
    attendie_id: str


@dataclass(frozen=True)
class Playback:
    status: str


@dataclass(frozen=True)
class Event:
    type: EventType
    body: Any


def parse(string: str) -> Optional[Event]:
    try:
        raw_event = json.loads(string)
    except json.decoder.JSONDecodeError:
        # string is not an event, skipping
        return None

    logger.debug(f"Raw event: {raw_event}")
    headers, body = raw_event.get("headers") or {}, raw_event.get("body")
    event_body = None
    event_type = headers["Event"]
    try:
        if event_type == EventType.NEW_CHANNEL:
            event_body = _build_new_channel(headers)
        elif event_type == EventType.ERROR:
            event_body = _build_error_message(headers)
        elif event_type in (EventType.CHAT_MESSAGE, EventType.CHAT_MESSAGE_SENT):
            event_body = _build_message(headers, body)
        elif event_type == EventType.CHAT_HISTORY:
            event_body = _build_chat_history(body)
        elif event_type == EventType.INVALID_CHAT:
            event_body = _build_invalid_chat_message(headers)
        elif event_type == EventType.CALL_INCOMING:
            event_body = _build_call(headers)
        elif event_type == EventType.CALL_ANSWER:
            event_body = _build_call_answer(headers)
        elif event_type == EventType.PLAYBACK_STATUS:
            event_body = _build_playback(headers)
    except exceptions.EventParseError as e:
        logger.error(f"Failed to parse raw event {raw_event}: {e}")
        raise

    return Event(type=event_type, body=event_body)


def _build_new_channel(headers):
    return NewChannel(id=headers["ChanID"])


def _build_error_message(headers: Dict[str, Any]) -> str:
    return headers["ErrInfo"]


def _build_message(headers, body):
    return Message(
        id=str(headers["MsgID"]),
        from_uid=str(headers["FromUID"]),
        persona_uid=str(headers["PersonaUID"]),
        tagged=headers.get("Tagged", False),
        chat_id=headers["ChatID"],
        chat_type=_get_valid_chat_type(headers["ChatType"]),
        text=body,
    )


def _get_valid_chat_type(chat_type_int: int) -> ChatType:
    _chat_type_int_to_enum = {
        1: ChatType.PRIVATE,
        2: ChatType.GROUP,
        3: ChatType.GROUP,
        4: ChatType.GROUP,
    }
    chat_type = _chat_type_int_to_enum.get(chat_type_int)
    if not chat_type:
        raise exceptions.EventParseError(f"Invalid chat type: {chat_type_int}")
    return chat_type


def _build_chat_history(body: str) -> List[Message]:
    return [_build_message(m["headers"], m["body"]) for m in json.loads(body)]


def _build_invalid_chat_message(headers: Dict[str, Any]) -> str:
    return f"invalid chat id: {headers['ChatID']}"


def _build_call(headers):
    return Call(
        id=headers["CallID"],
    )


def _build_call_answer(headers):
    return CallAnswer(
        attendie_id=headers["AttendieID"],
    )


def _build_playback(headers):
    return Playback(
        status=headers["Status"],
    )
