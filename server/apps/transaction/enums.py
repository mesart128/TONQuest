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
    dedust_swap = 0x9C610DE3
    dedust_deposit = 0xB544F4A4

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
