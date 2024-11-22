from enum import Enum, IntEnum


class OpCodes(IntEnum):
    # JETTON messages
    jetton_transfer = 0xF8A7EA5
    # internal_transfer = 0x178D4519
    # transfer_notification = 0x7362D09C
    # excesses = 0xD53276DB
    # burn = 0x595F07BC
    # burn_notification = 0x7BDD97DE

    # TON messages
    default_message = 0x00000000

    # TonCrypto
    dedust_swap = 0x9C610DE3
    dedust_liquidity = 0xB544F4A4
    dedust_withdraw = 0x3AA870A6

    # TonStakers
    tonstakers_payout_mint_jettons = 0x1674B0A0
    tonstakers_pool_withdraw = 0x0A77535C  # Tonstake Pool Withdrawal

    # Evaa
    evaa_borrow = 0x0000211A
    evaa_supply = 0x0000011A

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
