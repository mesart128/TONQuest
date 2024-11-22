import logging

from pytoniq_core import (
    Address,
    BlockIdExt,
    ExternalMsgInfo,
    ExternalOutMsgInfo,
    InternalMsgInfo,
    MessageAny,
    Slice,
    Transaction,
)
from tonsdk.utils import b64str_to_bytes, bytes_to_b64str

from apps.currency.common.asset import Asset
from apps.ton_quest.enums import TaskTypeEnum
from apps.ton_quest.schemas import (
    DedustDepositEvent,
    DedustSwapEvent,
    DedustWithdrawEvent,
    TonstakersPayoutMintJettonsEvent,
    JettonTransferEvent,
)
from apps.transaction.enums import MessageTypeEnum, OpCodes
from apps.transaction.schemas import (
    ParsedTransactionDTO,
    RawMessageDTO,
    RawTransactionDTO,
)
from core.ton_provider import TONAPIClientAsync


class TransactionService:
    def __init__(
        self,
        # repository: TransactionMongoRepository,
        ton_rpc_client: TONAPIClientAsync,
    ):
        self.ton_rpc_client = ton_rpc_client
        # self.repository = repository

    # async def try_find_tx_by_out_msg(self, out_msg: RawMessageDTO) -> RawTransactionDTO | None:
    #     transaction: RawTransactionDTO = await self.repository.find_one_by(
    #         in_msg_dest=out_msg["dest"],
    #         in_msg_created_lt=out_msg["created_lt"],
    #     )
    #     return transaction

    # async def get_transaction_by_hash(self, hash_: str) -> RawTransactionDTO | None:
    #     transaction: RawTransactionDTO = await self.repository.find_one_by(hash=hash_)
    #     return transaction
    #
    # async def get_transaction_by(self, **kwargs) -> RawTransactionDTO | None:
    #     transaction: RawTransactionDTO = await self.repository.find_one_by(**kwargs)
    #     return transaction
    #
    # async def get_transaction_with_messages(self, id_: str) -> RawTransactionDTO | None:
    #     transaction: RawTransactionDTO = await self.repository.find_one_by(id_)
    #     return transaction

    @classmethod
    async def chain_transaction_to_dto(
        self, transaction: Transaction, block: BlockIdExt, masterchain_seqno: int
    ) -> RawTransactionDTO:
        parsed_transaction = await self.parse_transaction(transaction)
        result = RawTransactionDTO(
            **parsed_transaction,
            masterchain_seqno=masterchain_seqno,
            workchain=block.workchain,
            shard=int(block.shard),
            shard_seqno=block.seqno,
            id=None,
        )
        return result

    @classmethod
    def calculate_tx_hash_by_b64(cls, b64_str: str) -> str:
        bag_of_cell: bytes = b64str_to_bytes(b64_str)
        blockchain_tx = Transaction.deserialize(Slice.one_from_boc(bag_of_cell))
        in_msg_cell = blockchain_tx.in_msg.serialize()
        in_msg_hash = in_msg_cell.hash.hex()
        return in_msg_hash

    @classmethod
    async def parse_b64_transaction(cls, b64_str: str) -> ParsedTransactionDTO:
        raw_tx_bytes = b64str_to_bytes(b64_str)
        transaction = Transaction.deserialize(Slice.one_from_boc(raw_tx_bytes))
        parsed_transaction: ParsedTransactionDTO = await TransactionService.parse_transaction(
            transaction
        )
        return parsed_transaction

    @classmethod
    async def parse_transaction(cls, transaction: Transaction) -> ParsedTransactionDTO:
        computation_exit_code = None
        action_exit_code = None
        try:
            hash_ = transaction.cell.get_hash(0).hex()
            account_address = Address(f"0:{transaction.account_addr_hex}")
            total_fee = transaction.total_fees.grams
            lt = transaction.lt
            now = transaction.now
            bag_of_cell = bytes_to_b64str(transaction.cell.to_boc())
            computation_ph = transaction.description.compute_ph
            # check if transaction was not skipped compute phase
            match computation_ph.type_:
                case "vm":
                    # logging.debug(f"VM phase exit code: {computation_ph.exit_code}")
                    computation_exit_code = computation_ph.exit_code
                case "skipped":
                    pass
                case _:
                    logging.error(f"Unknown computation phase type: {computation_ph.type_}")

            action_ph = transaction.description.action
            # check if transaction was not skipped action phase, else None
            if action_ph is not None:
                action_exit_code = action_ph.result_code

            in_msg = await cls._parse_message(transaction.in_msg)
            out_msgs = [await cls._parse_message(msg) for msg in transaction.out_msgs]
            result = {
                "account_address": account_address.to_str(False),
                "hash": hash_,
                "compute_phase_code": computation_exit_code,
                "action_phase_code": action_exit_code,
                "total_fee": total_fee,
                "lt": lt,
                "now": now,
                "bag_of_cell": bag_of_cell,
                "in_msg": in_msg,
                "out_msgs": out_msgs,
            }
        except Exception as e:
            logging.error(f"Error while parsing transaction in _parsed_transaction {e}")
            raise e
        return result

    @classmethod
    async def _parse_message(cls, msg: MessageAny) -> RawMessageDTO:
        created_lt = 0
        fwd_fee = 0
        if isinstance(msg.info, InternalMsgInfo):
            message_type = MessageTypeEnum.internal.value
            created_lt = msg.info.created_lt
            value = msg.info.value_coins
            fwd_fee = msg.info.fwd_fee
        elif isinstance(msg.info, ExternalMsgInfo):
            message_type = MessageTypeEnum.external.value
            value = msg.info.import_fee
        elif isinstance(msg.info, ExternalOutMsgInfo):
            # case external out message. Wallets and jettons dont use this
            message_type = MessageTypeEnum.external_out.value
            value = 0
        else:
            logging.error(f"Unknown message type: {msg.info}. \n {msg=}")
            raise ValueError(f"Unknown message type: {msg.info}")
        src = msg.info.src
        dest = msg.info.dest
        msg_body = msg.body
        msg_body_str = bytes_to_b64str(msg_body.to_boc())
        msg_init = msg.init
        msg_init_str = (
            bytes_to_b64str(msg_init.serialize().to_boc()) if msg_init is not None else None
        )
        cell_body = msg_body.begin_parse()
        if cell_body.remaining_bits == 0:
            # case empty body.
            logging.debug(f"Empty message body. {msg.body=}")
            op_code = OpCodes.default_message.value
        else:
            try:
                op_code = cell_body.load_uint(32)
            except Exception as e:
                logging.error(f"Problem while parsing message op code {e=}. " f"Message: {msg=}")
                op_code = OpCodes.default_message.value
        result = {
            "id": None,
            "message_type": message_type,
            "src": src.to_str(False) if src is not None else None,  # case external msg
            "dest": dest.to_str(False)
            if dest is not None
            else None,  # None case internal external msg
            "op_code": op_code,
            "created_lt": created_lt,
            "init": msg_init_str,
            "body": msg_body_str,
            "value": value,
            "fwd_fee": fwd_fee,
        }
        return result
    
    @staticmethod
    async def parse_jetton_transfer_event(out_msg: MessageAny) -> JettonTransferEvent:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        if op != OpCodes.jetton_transfer:
            raise ValueError(f"Wrong op code. Expected {OpCodes.jetton_transfer}. Got {op}")
        event = {
            "event_type": "jetton_transfer",
            "op_code": op,
            "query_id": body.load_uint(64),
            "amount": body.load_coins(),
            "destination": body.load_address(),
            "response_destination": body.load_address(),
            "custom_payload": body.load_ref() if body.load_bit() else None,
            "forward_ton_amount": body.load_coins(),
            "forward_payload": body.load_ref() if body.load_bit() else None,
        }
        logging.info(event)
        result = JettonTransferEvent(**event)
        return result        

    @staticmethod
    async def parse_dedust_swap_event(out_msg: MessageAny) -> DedustSwapEvent:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        event = {
            "event_type": TaskTypeEnum.dedust_swap.value,
            "asset_in": Asset.from_slice(body).address,
            "asset_out": Asset.from_slice(body).address,
            "amount_out": body.load_coins(),
            "amount_in": body.load_coins(),
            "sender_address": body.load_ref().begin_parse().load_address(),
            "op_code": op,
        }
        logging.info(event)
        result = DedustSwapEvent(**event)
        return result

    @staticmethod
    async def parse_dedust_liquidity_event(out_msg: MessageAny) -> DedustDepositEvent:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        event = {
            "event_type": TaskTypeEnum.dedust_liquidity.value,
            "sender_address": body.load_address(),
            "amount0": body.load_coins(),
            "amount1": body.load_coins(),
            "reserve1": body.load_coins(),
            "liquidity": body.load_coins(),
            "op_code": op,
        }
        logging.info(event)
        result = DedustDepositEvent(**event)
        return result

    @staticmethod
    async def parse_dedust_withdraw_event(out_msg: MessageAny) -> DedustWithdrawEvent:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        event = {
            "event_type": TaskTypeEnum.dedust_withdraw.value,
            "sender_address": body.load_address(),
            "liquidity": body.load_coins(),
            "amount0": body.load_coins(),
            "amount1": body.load_coins(),
            "reserve0": body.load_coins(),
            "reserve1": body.load_coins(),
            "op_code": op,
        }
        logging.info(event)
        result = DedustWithdrawEvent(**event)
        return result


    @staticmethod
    async def parse_tonstakers_payout_mint_jettons(out_msg: MessageAny) -> TonstakersPayoutMintJettonsEvent:
        body = out_msg.body.to_slice()
        event = {
            "op_code": body.load_uint(32),
            "query_id": body.load_uint(64),
            "destination": body.load_address(),
            "amount": body.load_coins(),
            "event_type": TaskTypeEnum.tonstakers_stake.value,
        }
        logging.info(event)
        result = TonstakersPayoutMintJettonsEvent(**event)
        return result
