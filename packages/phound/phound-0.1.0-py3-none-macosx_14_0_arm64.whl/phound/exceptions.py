class PhoundError(Exception):
    pass


class EventParseError(PhoundError):
    pass


class UnexpectedEventError(PhoundError):
    pass


class InvalidChatError(PhoundError):
    pass


class InputError(PhoundError):
    pass
