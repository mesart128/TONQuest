import logging
from typing import Optional, Union

from pytoniq_core import Address, MessageAny, Transaction

from apps.account.account_codes import (
    dedust_swap_pool_code_b64,
    evaa_main_address,
    tonstakers_main_address,
)
from apps.account.types import SystemAddress
from apps.ton_quest import manager as ton_quest_manager
from apps.ton_quest.enums import TaskTypeEnum
from apps.ton_quest.models import User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.ton_quest.schemas import DedustSwapEvent
from apps.transaction.enums import MessageTypeEnum, OpCodes
from apps.transaction.schemas import RawMessageDTO, RawTransactionDTO
from apps.transaction.service import TransactionService
from core.schemas import FullAccountState
from core.ton_provider import TONAPIClientAsync


class AccountService:
    def __init__(
        self,
        transaction_service: TransactionService,
        ton_rpc_client: TONAPIClientAsync,
        ton_quest_repository: TonQuestSQLAlchemyRepo,
    ):
        self.transaction_service = transaction_service
        self.ton_rpc_client = ton_rpc_client
        self.ton_quest_repository = ton_quest_repository

    async def get_account(self, account_address: Union[SystemAddress, Address, str]) -> User | None:
        if isinstance(account_address, str):
            account_address = Address(account_address)
        user_account = await self.ton_quest_repository.get_user_by(
            wallet_address=account_address.to_str(False)
        )
        return user_account

    async def handle_evaa_event_flow(self, out_msg: MessageAny) -> None:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        event_account_address = None
        if op == OpCodes.evaa_borrow:
            event_account_address = out_msg.info.dest
            event_type = TaskTypeEnum.evaa_borrow
            logging.debug(f"Detected $TON evaa borrow message for {event_account_address}")

        elif op == OpCodes.default_message:
            logging.debug(
                f"Detected default message from {out_msg.info.src.to_str()} in evaa contract"
            )
            if body.load_string() == "EVAA supply.":
                event_account_address = out_msg.info.dest
                event_type = TaskTypeEnum.evaa_supply
                logging.debug(f"Detected $TON evaa supply message for {event_account_address}")

        elif op == OpCodes.jetton_transfer:
            jetton_transfer_event = await self.transaction_service.parse_jetton_transfer_event(
                out_msg
            )
            if jetton_transfer_event.forward_payload:
                forward_payload = jetton_transfer_event.forward_payload.begin_parse()
                if forward_payload.load_uint(32) == OpCodes.evaa_borrow:
                    event_account_address = out_msg.info.dest
                    event_type = TaskTypeEnum.evaa_borrow
                    logging.debug(
                        f"Detected jetton evaa borrow message for {event_account_address}"
                    )

        if event_account_address:
            tracked_account: User = await self.get_account(account_address=event_account_address)
            if tracked_account:
                await ton_quest_manager.check_task(
                    user_account=tracked_account, event_type=event_type
                )
                logging.info(f"Detected {event_type} message from {tracked_account.wallet_address}")
            else:
                # user = User(
                #     telegram_id=randint(1, 1000),
                #     username=event_account_address.to_str(),
                #     first_name=event_account_address.to_str(True),
                #     last_name=event_account_address.to_str(False),
                #     image="web_app_init_data.user.photo_url",
                #     wallet_address=event_account_address.to_str(False),
                # )
                # tracked_account = await self.ton_quest_repository.create_user(user)
                # await ton_quest_manager.check_task(user_account=tracked_account,
                #                                    event_type=event_type)
                return

    async def handle_tonstakers_event_flow(self, out_msg: MessageAny) -> None:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        event_account_address = None
        if op == OpCodes.tonstakers_payout_mint_jettons:
            event_account_address = (
                await self.transaction_service.parse_tonstakers_payout_mint_jettons(out_msg)
            ).destination
            event_type = TaskTypeEnum.tonstakers_stake
            logging.debug(f"Detected tonstakers mint jetton for {event_account_address}")

        elif op == OpCodes.tonstakers_pool_withdraw:
            event_account_address = out_msg.info.dest
            event_type = TaskTypeEnum.tonstakers_unstake
            logging.debug(f"Detected tonstakers pool withdraw message for {event_account_address}")

        if event_account_address:
            tracked_account: User = await self.get_account(account_address=event_account_address)
            if tracked_account:
                await ton_quest_manager.check_task(
                    user_account=tracked_account, event_type=event_type
                )
                logging.info(f"Detected tonstakers message from {tracked_account.wallet_address}")
            else:
                # user = User(
                #     telegram_id=randint(1, 1000),
                #     username=event_account_address.to_str(),
                #     first_name=event_account_address.to_str(True),
                #     last_name=event_account_address.to_str(False),
                #     image="web_app_init_data.user.photo_url",
                #     wallet_address=event_account_address.to_str(False),
                # )
                # tracked_account = await self.ton_quest_repository.create_user(user)
                # await ton_quest_manager.check_task(user_account=tracked_account, event_type=event_type)
                return None

    async def handle_dedust_event_flow(self, out_msg: MessageAny) -> None:
        body = out_msg.body.to_slice()
        op = body.load_uint(32)
        if op == OpCodes.dedust_swap:
            message: DedustSwapEvent = await self.transaction_service.parse_dedust_swap_event(
                out_msg
            )
            logging.debug(f"Detected dedust message from {message.sender_address}")
        elif op == OpCodes.dedust_liquidity:
            message = await self.transaction_service.parse_dedust_liquidity_event(out_msg)
            logging.debug(f"Detected liquidity message from {out_msg.info.src.to_str()}")
        elif op == OpCodes.dedust_withdraw:
            message = await self.transaction_service.parse_dedust_withdraw_event(out_msg)
            logging.debug(f"Detected dedust_withdraw withdraw from {out_msg.info.src.to_str()}")
        else:
            logging.warning(
                f"Detected external message from {out_msg.info.src.to_str()} with code {op}"
            )
            return None
        tracked_account: User = await self.get_account(account_address=message.sender_address)
        if tracked_account:
            await ton_quest_manager.check_task(
                user_account=tracked_account, event_type=message.event_type
            )
            logging.info(f"Detected OUR USER dedust message from {tracked_account.wallet_address}")
        else:
            # user = User(
            #     telegram_id=randint(1, 1000),
            #     username=message.sender_address.to_str(),
            #     first_name=message.sender_address.to_str(True),
            #     last_name=message.sender_address.to_str(False),
            #     image="web_app_init_data.user.photo_url",
            #     wallet_address=message.sender_address.to_str(False),
            # )
            # tracked_account = await self.ton_quest_repository.create_user(user)
            # await ton_quest_manager.check_task(user_account=tracked_account, event_type=message)
            return None

    async def handle_out_msg(self, tx: Transaction, out_msg: MessageAny) -> None:
        if out_msg.info.dest is None:
            # account: FullAccountState = await self.ton_rpc_client.get_address_information(
            #     out_msg.info.src.to_str()
            # )
            try:
                await self.handle_dedust_event_flow(out_msg=out_msg)
                logging.debug(f"Detected dedust message {tx.cell.hash.hex()}")
            except Exception:
                pass
        if out_msg.info.src.to_str(is_user_friendly=False) == tonstakers_main_address:
            logging.debug(f"Detected tonstakers message {tx.cell.hash.hex()}")
            await self.handle_tonstakers_event_flow(out_msg=out_msg)
        elif out_msg.info.src.to_str(is_user_friendly=False) == evaa_main_address:
            logging.debug(
                f"Detected evaa message {tx.cell.hash.hex()}. {out_msg.info.src.to_str()}"
            )
            await self.handle_evaa_event_flow(out_msg=out_msg)

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
                    logging.warning(
                        f"Detected internal message with op code {in_msg['op_code']}. "
                        f"Account {account_address.to_non_bounceable()}"
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
            await self.handle_transaction_event(parsed_transaction)
            logging.info(f"Transaction {parsed_transaction['hash']} scanned to db. ")
        except Exception as e:
            logging.error(
                f"Error while processing detected account {e}. \n" f"Info {parsed_transaction=}",
                exc_info=True,
            )
