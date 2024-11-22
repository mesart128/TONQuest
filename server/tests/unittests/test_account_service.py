from unittest.mock import AsyncMock, MagicMock

import pytest
from pytoniq_core import Slice, Transaction
from sqlalchemy.ext.asyncio import async_sessionmaker
from tonsdk.utils import b64str_to_bytes

from apps.account.account_codes import dedust_swap_pool_code_b64
from apps.account.service import AccountService
from apps.ton_quest.models import User
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.transaction.enums import OpCodes
from apps.transaction.schemas import RawTransactionDTO
from apps.transaction.service import TransactionService
from tests.datasets.transactions import TestCases


@pytest.mark.asyncio
async def test_opcodes():
    chain_view_codes = [0x9C610DE3, 0x9C610DE3]
    dedust_op_list = OpCodes.dedust_code_list()
    for i in chain_view_codes:
        assert i in dedust_op_list


@pytest.mark.asyncio
async def test_add_parse_dedust_message(database_engine, mocker):
    SessionFactory = async_sessionmaker(database_engine)
    ton_quest_repo = TonQuestSQLAlchemyRepo(SessionFactory)
    test_user = User(
        wallet_address="0:1",
        telegram_id=1,
        username="test",
        first_name="test",
        last_name="test",
        image="test",
    )
    user = await ton_quest_repo.create_user(test_user)
    print(user)
    raw_transaction_b64 = TestCases.DEDUST_SWAP_EVENT
    raw_tx_bytes = b64str_to_bytes(raw_transaction_b64)
    transaction = Transaction.deserialize(Slice.one_from_boc(raw_tx_bytes))
    ton_rpc_client = AsyncMock()
    transaction_service = TransactionService(ton_rpc_client)
    ton_quest_repo_mock = AsyncMock()
    account_service = AccountService(
        transaction_service=transaction_service,
        ton_rpc_client=ton_rpc_client,
        ton_quest_repository=ton_quest_repo,
    )
    ton_rpc_client.get_address_information = AsyncMock(
        return_value=MagicMock(code=dedust_swap_pool_code_b64)
    )
    account_service.get_account = AsyncMock(return_value=user)
    raw_parsed_transaction: RawTransactionDTO = await transaction_service.chain_transaction_to_dto(
        transaction, block=MagicMock(shard=1), masterchain_seqno=0
    )

    for msg in transaction.out_msgs:
        await account_service.handle_out_msg(msg)

    # await account_service.handle_external_out_msg(raw_parsed_transaction)


# async def test_add_parse_dedust_message_not_found_account(self):
#     raw_transaction_b64 = TestCases.DEDUST_SWAP_EVENT
#     raw_tx_bytes = b64str_to_bytes(raw_transaction_b64)
#     transaction = Transaction.deserialize(Slice.one_from_boc(raw_tx_bytes))
#     full_acc_state_mock = MagicMock()
#     full_acc_state_mock.code = dedust_swap_pool_code_b64
#     self.mock_rpc_client.get_address_information = AsyncMock(return_value=full_acc_state_mock)
#     self.account_service.get_account = AsyncMock(return_value=None)
#     self.producer.publish_task_event = AsyncMock()
#     for out_msg in transaction.out_msgs:
#         await self.account_service.handle_external_out_msg(out_msg)
#     self.producer.publish_task_event.assert_not_called()
#
