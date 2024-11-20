import unittest
from unittest.mock import AsyncMock, MagicMock

import pytest
from pytoniq_core import Slice, Transaction
from tonsdk.utils import b64str_to_bytes

from apps.account.account_codes import dedust_swap_pool_code_b64
from apps.account.schemas import AccountSchema
from apps.account.service import AccountService
from apps.scanner.service import BlockScanner
from apps.ton_quest.repository import TonQuestSQLAlchemyRepo
from apps.transaction.enums import OpCodes
from apps.transaction.schemas import ParsedTransactionDTO, RawTransactionDTO
from apps.transaction.service import TransactionService
from tests.datasets.transactions import TestCases


@pytest.mark.asyncio
async def test_add_parse_dedust_message(setup_database, ton_quest_repo):
    raw_transaction_b64 = TestCases.DEDUST_SWAP_EVENT
    raw_tx_bytes = b64str_to_bytes(raw_transaction_b64)
    transaction = Transaction.deserialize(Slice.one_from_boc(raw_tx_bytes))

    ton_rpc_client = AsyncMock()
    transaction_service = TransactionService(
        ton_rpc_client
    )
    account_service = AccountService(
        transaction_service=transaction_service,
        ton_rpc_client=ton_rpc_client,
        producer=AsyncMock(),
        ton_quest_repository=ton_quest_repo
    )
    raw_parsed_transaction: ParsedTransactionDTO = await transaction_service.chain_transaction_to_dto(
        transaction, block=MagicMock(shard=1), masterchain_seqno=0
    )
    await account_service.handle_transaction_on_account(transaction)

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


