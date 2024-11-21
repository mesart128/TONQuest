from enum import Enum, IntEnum


class OpCodes(IntEnum):
    # JETTON messages
    # transfer = 0xF8A7EA5
    # internal_transfer = 0x178D4519
    # transfer_notification = 0x7362D09C
    # excesses = 0xD53276DB
    # burn = 0x595F07BC
    # burn_notification = 0x7BDD97DE

    # TON messages
    default_message = 0x00000000

    # TonCrypto
    dedust_swap = 0x9c610de3
    dedust_liquidity = 0xb544f4a4
    dedust_withdraw = 0x3aa870a6

    # TonStakers
    tonstakers_payout_mint_jettons = 0x1674b0a0
    tonstakers_pool_withdraw = 0x319b0cdc

    @classmethod
    def dedust_code_list(cls):
        return [cls.dedust_swap, cls.dedust_liquidity, cls.dedust_withdraw]

    @classmethod
    def get_by_code(cls, code):
        for opcode in cls:
            if opcode.value == code:
                return opcode.name
        return cls.default_message.name

    @classmethod
    def item_list(cls):
        return [opcode.value for opcode in cls]


class MessageTypeEnum(Enum):
    internal = "internal"
    external = "external"
    external_out = "external_out"


class Web2TxTypeEnum(Enum):
    deposit = "deposit"
    withdrawal = "withdrawal"
    transfer = "transfer"
    outer = "outer"
    refill = "refill"
