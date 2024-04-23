from enum import Enum

class GrantType(Enum):
    CLIENT_CREDENTIALS = 'client_credentials'
    CLIENT_SIGNATURE = 'client_signature'
    REFRESH_TOKEN = 'refresh_token'

class RetCode(Enum):
    OK = 'ok'
    ERROR = 'error'

class SubType(Enum):
    TICKER = 'TICKER'
    BOOK = 'BOOK'
    USER_TRADES = 'USER_TRADES'

class TimeInForce(Enum):
    GUC = 'good_til_cancelled'
    GUD = 'good_til_day'
    FOK = 'fill_or_kill'
    IOC = 'immediate_or_cancel'