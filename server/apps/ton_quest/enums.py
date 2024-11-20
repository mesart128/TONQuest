from enum import Enum


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    __repr__ = __str__


class TaskTypeEnum(StrEnum):
    dedust_swap = "dedust_swap"
    dedust_liquidity = "dedust_liquidity"
    dedust_withdraw = "dedust_withdraw"