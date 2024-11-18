from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    __repr__ = __str__


class GetMethodEnum(StrEnum):
    get_wallet_data = "get_wallet_data"
    get_jetton_data = "get_jetton_data"
    get_wallet_address = "get_wallet_address"


class CustomLoggingLevels(int, Enum):
    ADMIN = 60

    def __int__(self):
        return self.value

    __repr__ = __int__
