from typing import Optional, Any
from moss_cappa import messages

class ServiceException(Exception):

    default_message = None

    def __init__(
        self,
        message: Optional[str] = None,
        details: Optional[Any] = None
    ):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)

class ParsingOutputException(ServiceException):

    default_message = messages.MSG_1

class ConnectionException(ServiceException):

    default_message = messages.MSG_2

class SendingException(ServiceException):

    default_message = messages.MSG_3

class URLException(ServiceException):

    default_message = messages.MSG_4