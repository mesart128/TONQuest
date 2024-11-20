import logging
from typing import Optional, Union

from pytoniq_core import Address, MessageAny

from apps.account.account_codes import dedust_swap_pool_code_b64
from apps.account.schemas import AccountSchema
from apps.account.types import SystemAddress
from apps.ton_quest import manager as ton_quest_manager
from apps.ton_quest.models import User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import DedustEvent
from apps.transaction.enums import MessageTypeEnum, OpCodes
from apps.transaction.schemas import RawMessageDTO, RawTransactionDTO
from apps.transaction.service import TransactionService
from core.producer import HttpProducer
from core.schemas import FullAccountState
from core.ton_provider import TONAPIClientAsync


class AccountService:
    def __init__(
        self,
        transaction_service: TransactionService,
        ton_rpc_client: TONAPIClientAsync,
        producer: HttpProducer,
        ton_quest_repository: TonQuestSQLAlchemyRepo,
    ):
        self.transaction_service = transaction_service
        self.ton_rpc_client = ton_rpc_client
        self.producer = producer
        self.ton_quest_repository = ton_quest_repository

    # async def add_account(self, account_address: str) -> AccountSchema:
    #     existed_account = await self.get_account(account_address)
    #     if existed_account:
    #         return existed_account
    #     account_address_system = SystemAddress(account_address).to_raw()
    #     return await self._create_account(account_address_system, is_trackable=True)
    #
    # async def _create_account(
    #     self, account_address: SystemAddress | str, is_trackable: bool
    # ) -> AccountSchema:
    #     if isinstance(account_address, str):
    #         account_address = SystemAddress(account_address)
    #     if await self.get_account(account_address):
    #         raise ValueError("Account already exists")
    #     account_id = await self.repository.add_one(
    #         {
    #             "account_address": account_address.to_raw(),
    #             "is_trackable": is_trackable,
    #         }
    #     )
    #     result = await self.repository.find_one(account_id)
    #     return AccountSchema(**result)

    async def get_accounts(self, limit: int) -> list[AccountSchema]:
        result = await self.repository.find_all()
        return [AccountSchema(**item) for item in result[:limit]]

    async def get_account(self, account_address: Union[SystemAddress, Address, str]) -> User | None:
        if isinstance(account_address, str):
            account_address = Address(account_address)
        user_account = await self.ton_quest_repository.get_user_by(
            wallet_address=account_address.to_raw()
        )
        return user_account

    async def handle_external_out_msg(self, out_msg: MessageAny) -> None:
        account: FullAccountState = await self.ton_rpc_client.get_address_information(
            out_msg.info.src.to_str()
        )
        if account.code == dedust_swap_pool_code_b64:
            try:
                message: DedustEvent = (
                    await self.transaction_service.parse_external_dedust_messages(out_msg)
                )
            except Exception as e:
                logging.error(f"Error while parsing dedust message {e}", exc_info=True)
                return
            logging.debug(f"Detected dedust message {message}")
            tracked_account: User = await self.get_account(
                account_address=message["sender_address"]
            )
            if tracked_account:
                await ton_quest_manager.check_task(user_account=tracked_account, event=message)
                # TODO update tasks here
                logging.info(f"Detected dedust message from {tracked_account.wallet_address}")
        else:
            logging.warning(
                f"Detected external message from "
                f"{out_msg.info.src.to_str()} with code another acc code"
            )

    async def handle_transaction_event(self, raw_transaction: RawTransactionDTO) -> None:
        try:
            in_msg: RawMessageDTO = raw_transaction["in_msg"]
            message_type = in_msg["message_type"]
            logging.debug(f"Detected message type {message_type}")
            if message_type == MessageTypeEnum.internal.value:
                # case TON deposit to wallet
                account_address = SystemAddress(in_msg["dest"])
                assert account_address == SystemAddress(raw_transaction["account_address"])
                logging.debug(f"Detected external message to {account_address.to_non_bounceable()}")
                if in_msg["op_code"] in OpCodes.item_list():
                    await self.producer.publish_task_event(
                        data={
                            "address": account_address.to_raw(),
                            "op_code": str(in_msg["op_code"]),
                        }
                    )
                logging.info(f"handle_account_in_out_msg {raw_transaction['account_address']=}")
        except Exception as e:
            logging.error(
                f"Error while processing transaction event {e}. \n" f"Info {raw_transaction=}",
                exc_info=True,
            )

    async def insert_parsed_raw_tx_dto_to_db_object(
        self, parsed_transaction: RawTransactionDTO, account_id: str | None
    ) -> dict:
        parsed_transaction["account_id"] = account_id
        tx_to_insert = {
            "account_id": parsed_transaction["account_id"],
            "account_address": parsed_transaction["account_address"],
            "hash": parsed_transaction["hash"],
            "total_fee": parsed_transaction["total_fee"],
            "lt": parsed_transaction["lt"],
            "now": parsed_transaction["now"],
            "compute_phase_code": parsed_transaction["compute_phase_code"],
            "action_phase_code": parsed_transaction["action_phase_code"],
            "bag_of_cell": parsed_transaction["bag_of_cell"],
            "masterchain_seqno": parsed_transaction["masterchain_seqno"],
            "workchain": parsed_transaction["workchain"],
            "shard": parsed_transaction["shard"],
            "shard_seqno": parsed_transaction["shard_seqno"],
        }
        in_msg_src = (
            parsed_transaction["in_msg"]["src"] if parsed_transaction["in_msg"]["src"] else None
        )
        tx_to_insert["in_msg"] = {
            "message_type": MessageTypeEnum(parsed_transaction["in_msg"]["message_type"]).value,
            "src": in_msg_src,
            "dest": parsed_transaction["in_msg"]["dest"],
            "op_code": parsed_transaction["in_msg"]["op_code"],
            "created_lt": parsed_transaction["in_msg"]["created_lt"],
            "init": parsed_transaction["in_msg"]["init"],
            "body": parsed_transaction["in_msg"]["body"],
            "value": parsed_transaction["in_msg"]["value"],
        }
        tx_to_insert["out_msgs"] = []

        for msg in parsed_transaction["out_msgs"]:
            dict_to_insert = {
                "message_type": MessageTypeEnum(msg["message_type"]).value,
                "src": msg["src"],
                "dest": msg["dest"],
                "op_code": msg["op_code"],
                "created_lt": msg["created_lt"],
                "init": msg["init"],
                "body": msg["body"],
                "value": msg["value"],
            }
            tx_to_insert["out_msgs"].append(dict_to_insert)
        # await self.repository.add_one(tx_to_insert)
        # full_transaction = await self.transaction_service.get_transaction_by_hash(
        #     hash_=parsed_transaction["hash"]
        # )
        return parsed_transaction

    async def handle_transaction_on_account(self, parsed_transaction: RawTransactionDTO) -> None:
        try:
            account: Optional[User] = await self.get_account(
                Address(parsed_transaction["account_address"])
            )
            if not account:
                return
            logging.debug(f"Detected account {account.wallet_address}")
            return
            existed_transaction = await self.transaction_service.get_transaction_by_hash(
                hash_=parsed_transaction["hash"]
            )
            if existed_transaction:
                logging.info(f"Transaction {parsed_transaction['hash']} already exists")
                await self.handle_transaction_event(parsed_transaction)
                return existed_transaction
            inserted_tx = await self.insert_parsed_raw_tx_dto_to_db_object(
                parsed_transaction, account_id=account.id
            )
            full_transaction = await self.transaction_service.get_transaction_by_hash(
                parsed_transaction["hash"]
            )
            await self.handle_transaction_event(parsed_transaction)
            logging.info(f"Transaction {inserted_tx['hash']} added to db. {full_transaction=}")
        except Exception as e:
            logging.error(
                f"Error while processing detected account {e}. \n" f"Info {parsed_transaction=}",
                exc_info=True,
            )
