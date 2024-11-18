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

from apps.account.enums import AccountEventEnum
from apps.currency.common.asset import Asset
from apps.transaction.enums import MessageTypeEnum, OpCodes
from apps.transaction.repositories import TransactionMongoRepository
from apps.transaction.schemas import (
    ParsedTransactionDTO,
    RawMessageDTO,
    RawTransactionDTO,
)
from core.ton_provider import TONAPIClientAsync


class TransactionService:
    def __init__(
        self,
        repository: TransactionMongoRepository,
        ton_rpc_client: TONAPIClientAsync,
    ):
        self.ton_rpc_client = ton_rpc_client
        self.repository = repository

    async def try_find_tx_by_out_msg(self, out_msg: RawMessageDTO) -> RawTransactionDTO | None:
        transaction: RawTransactionDTO = await self.repository.find_one_by(
            in_msg_dest=out_msg["dest"],
            in_msg_created_lt=out_msg["created_lt"],
        )
        return transaction

    async def get_transaction_by_hash(self, hash_: str) -> RawTransactionDTO | None:
        transaction: RawTransactionDTO = await self.repository.find_one_by(hash=hash_)
        return transaction

    async def get_transaction_by(self, **kwargs) -> RawTransactionDTO | None:
        transaction: RawTransactionDTO = await self.repository.find_one_by(**kwargs)
        return transaction

    async def get_transaction_with_messages(self, id_: str) -> RawTransactionDTO | None:
        transaction: RawTransactionDTO = await self.repository.find_one_by(id_)
        return transaction

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
    async def parse_external_dedust_messages(out_msg: MessageAny):
        body = out_msg.body.to_slice()
        op = body.load_uint(32)

        if op == OpCodes.dedust_swap.value:
            event = {
                "event_type": AccountEventEnum.dedust_swap.value,
                "asset_in": Asset.from_slice(body).address,
                "asset_out": Asset.from_slice(body).address,
                "amount_out": body.load_coins(),
                "amount_in": body.load_coins(),
                "sender_address": body.load_ref().begin_parse().load_address(),
                "op_code": op,
            }
            logging.info(event)
            return event
        elif op == OpCodes.dedust_deposit.value:
            event = {
                "event_type": AccountEventEnum.dedust_deposit.value,
                "asset_in": Asset.from_slice(body).address.to_str(),
                "asset_out": Asset.from_slice(body).address.to_str(),
                "amount_out": body.load_coins(),
                "amount_in": body.load_coins(),
                "sender_address": body.load_ref().begin_parse().load_address().to_str(),
                "op_code": op,
            }

            logging.info(event)
            return event
