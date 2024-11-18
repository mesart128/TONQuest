import enum


class AccountEventEnum(enum.Enum):
    # TonCrypto
    dedust_swap = "dedust_swap"
    dedust_deposit = "dedust_deposit"

    # ton transfer
    default_ton_transfer = "default_ton_transfer"
