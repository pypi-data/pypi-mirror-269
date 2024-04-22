from enum import Enum


class RPCMessageType(str, Enum):
    STATUS = 'status'
    WARNING = 'warning'
    EXCEPTION = 'exception'
    STARTUP = 'startup'
    CHAT = 'chat'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value
    

NO_ECHO_MESSAGES = ()