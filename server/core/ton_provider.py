import base64
import json
import logging
import typing
import uuid
from abc import ABC, abstractmethod

import aiohttp
from aiohttp import ContentTypeError
from pytoniq_core import Address, BlockIdExt, Cell, Transaction
from tonsdk.boc import Cell as tonsdk_Cell
from tonsdk.utils import Address as tonsdk_Address
from tonsdk.utils import bytes_to_b64str

from apps.account.schemas import JettonWalletData
from core.enums import GetMethodEnum, StrEnum
from core.schemas import (
    AccountStateEnum,
    BlockHeader,
    BlockIdExtDTO,
    FullAccountState,
    ShortTxId,
    SimpleAccountState,
    TransactionIdDTO,
    WalletState,
)
from core.utils import read_address


class TonProviderError(Exception):
    pass


class RunGetMethodError(TonProviderError):
    def __init__(self, exit_code: int, message: str):
        self.exit_code = exit_code
        self.message = message
        super().__init__(message)


class HandleResponseError(TonProviderError):
    pass


class LiteServerUnknownError(HandleResponseError):
    message = "LITE_SERVER_UNKNOWN: specified mc block is older than block's masterchain ref"
    counter = 0
    max_retries = 10

    @classmethod
    def increment_counter(cls):
        cls.counter += 1

    @classmethod
    def reset_counter(cls):
        cls.counter = 0

    @classmethod
    def should_raise(cls):
        return cls.counter >= cls.max_retries


class SmartContractIsNotJettonOrNFTError(HandleResponseError):
    message = "Smart contract is not Jetton or NFT"


class AccountUninitializedError(HandleResponseError):
    message = "Account has uninitialized state"


class IncorrectAddressError(HandleResponseError):
    message = "Incorrect address"


class MethodsEnum(StrEnum):
    GET = "GET"
    POST = "POST"


class TonClient(ABC):
    @abstractmethod
    async def raw_send_boc(self, boc: bytes) -> bool:
        pass

    @abstractmethod
    async def get_transactions(
        self,
        address: str,
        count: int,
        hash_: typing.Optional[str] = None,
        lt: typing.Optional[int] = None,
        to_lt: typing.Optional[int] = None,
        archival: typing.Optional[bool] = None,
    ) -> typing.List[Transaction]:
        pass

    @abstractmethod
    async def get_account_state(self, address: str) -> SimpleAccountState:
        pass

    @abstractmethod
    async def lookup_block(self, wc: int, shard: int, seqno: int):
        pass

    @abstractmethod
    async def get_all_shards_info(self, master_block: BlockIdExt) -> typing.List[BlockIdExt]:
        pass

    @abstractmethod
    async def get_block_header(self, block: BlockIdExt) -> BlockHeader:
        pass

    @abstractmethod
    async def raw_get_block_transactions(self, block: BlockIdExt) -> ShortTxId:
        pass

    @abstractmethod
    async def raw_get_block_transactions_ext(self, block: BlockIdExt) -> typing.List[Transaction]:
        pass

    @abstractmethod
    async def raw_get_shard_block_proof(self, block: BlockIdExt):
        pass

    @abstractmethod
    async def run_get_method(self, address: str, method: GetMethodEnum, stack: list):
        pass

    @abstractmethod
    async def get_jetton_wallet_address(
        self, jetton_master_address: str, owner_address: str
    ) -> Address:
        pass

    @abstractmethod
    async def get_jetton_wallet_data(self, jetton_wallet_address: str) -> JettonWalletData:
        pass

    @abstractmethod
    async def get_masterchain_info(self):
        pass

    @abstractmethod
    async def request_wrapper(self, method: MethodsEnum, url: str, params: dict) -> dict:
        pass

    @abstractmethod
    async def json_rpc_request(self, method: str, params: dict) -> dict:
        pass

    @abstractmethod
    async def handle_response(self, response: aiohttp.ClientResponse) -> dict:
        pass


class TONAPIClientAsync(TonClient):
    def __init__(self, base_url: typing.Optional[str] = None, key: typing.Optional[str] = None):
        if base_url is None:
            base_url = "https://go.getblock.io/95dfd73af9144e4e823cc81f2bed942a"
        self.base_url = base_url

        self.headers = {
            "Content-Type": "application/json",
        }
        if key:
            self.headers["X-API-Key"] = key

    async def raw_send_boc(self, boc: bytes) -> bool:
        url = self.base_url + "/sendBoc"
        boc_b64 = bytes_to_b64str(boc)
        params = {"boc": boc_b64}
        response = await self.request_wrapper(MethodsEnum.POST, url, params)
        return response["ok"]

    async def get_transactions(
        self,
        address: str,
        count: int,
        hash_: typing.Optional[str] = None,
        lt: typing.Optional[int] = None,
        to_lt: typing.Optional[int] = None,
        archival: typing.Optional[bool] = None,
    ) -> typing.List[Transaction]:
        url = self.base_url + "/getTransactions"
        params = {
            "address": address,
            "limit": count,
            "hash": hash_,
            "lt": lt,
            "toLt": to_lt,
            "archival": archival,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        transactions = response["result"]
        # transactions_list = []
        # for transaction in transactions:
        #     data_bytes = b64str_to_bytes(transaction["data"])
        #     tx_slice: Slice = Cell.one_from_boc(data_bytes).begin_parse()
        #     tx = Transaction.deserialize(tx_slice)
        #     transactions_list.append(tx)
        return transactions

    async def get_account_state(self, address: str) -> SimpleAccountState:
        account_state: FullAccountState = await self.get_address_information(address)
        balance = int(account_state.balance)
        state = account_state.state
        result = SimpleAccountState(
            balance=balance,
            address=Address(address),
            state=state,
        )
        return result

    def block_b64_data_to_bytes(self, block: dict) -> dict:
        root_hash_bytes = base64.b64decode(block["root_hash"])
        file_hash_bytes = base64.b64decode(block["file_hash"])
        block["root_hash"] = root_hash_bytes
        block["file_hash"] = file_hash_bytes
        return block

    async def lookup_block(self, wc: int, shard: int, seqno: int):
        url = self.base_url + "/lookupBlock"
        params = {"workchain": wc, "shard": shard, "seqno": seqno}
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        updated_block = self.block_b64_data_to_bytes(response["result"])
        block, _ = BlockIdExt.from_dict(updated_block), True
        return block, _

    async def get_all_shards_info(self, master_block: BlockIdExt) -> typing.List[BlockIdExt]:
        url = self.base_url + "/shards"
        params = {"seqno": master_block.seqno}
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        shards = response["result"]["shards"]
        shards_list = []
        for shard in shards:
            try:
                self.block_b64_data_to_bytes(shard)
                shards_list.append(BlockIdExt.from_dict(shard))
            except Exception:
                logging.error(f"Error while processing shard: {shard}")
        return shards_list

    async def get_block_header(self, block: BlockIdExt) -> BlockHeader:
        url = self.base_url + "/getBlockHeader"
        params = {
            "workchain": block.workchain,
            "shard": block.shard,
            "seqno": block.seqno,
            # "file_hash": block.file_hash.hex(),
            # "root_hash": block.root_hash.hex(),
        }
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        self.block_b64_data_to_bytes(response["result"]["id"])
        prev_blocks = response["result"]["prev_blocks"]
        for bl in prev_blocks:
            self.block_b64_data_to_bytes(bl)
        block_header = BlockHeader(**self.convert_keys(response["result"]))
        return block_header

    async def raw_get_block_transactions(self, block: BlockIdExt) -> ShortTxId:
        url = self.base_url + "/getBlockTransactions"
        params = {
            "workchain": block.workchain,
            "shard": block.shard,
            "seqno": block.seqno,
        }
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        result = response["result"]
        txs = [ShortTxId(**x) for x in self.convert_keys(result["transactions"])]
        return txs

    async def raw_get_block_transactions_ext(
        self, block: BlockIdExt, count: typing.Optional[int] = 40
    ) -> typing.List[Transaction]:
        url = self.base_url + "/getBlockTransactionsExt"
        params = {
            "workchain": block.workchain,
            "shard": block.shard,
            "seqno": block.seqno,
            "count": count,
        }
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        result = response["result"]
        transactions = []
        for tx in result["transactions"]:
            tx_data = base64.b64decode(tx["data"])
            tx_slice = Cell.one_from_boc(tx_data).begin_parse()
            tx = Transaction.deserialize(tx_slice)
            transactions.append(tx)
        return transactions

    def convert_keys(self, data):
        if isinstance(data, dict):
            return {
                (key[1:] + "_" if key.startswith("@") else key): self.convert_keys(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [self.convert_keys(item) for item in data]
        else:
            return data

    async def raw_get_shard_block_proof(self, block: BlockIdExt):
        url = self.base_url + "/getShardBlockProof"
        params = {
            "workchain": block.workchain,
            "shard": block.shard,
            "seqno": block.seqno,
            # "file_hash": block.file_hash.hex(),
            # "root_hash": block.root_hash.hex(),
        }
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        return response

    def _process_address(self, address: str | Address) -> Address:
        if isinstance(address, Address):
            return address
        return Address(address)

    async def run_get_method(self, address: str, method: GetMethodEnum, stack: list):
        url = self.base_url + "/runGetMethod"
        data = {"address": address, "method": method, "stack": stack}
        response = await self.request_wrapper(MethodsEnum.POST, url, data)
        if response["result"]["exit_code"] != 0:
            raise RunGetMethodError(
                exit_code=response["result"]["exit_code"],
                message=f'get method {method} for address'
                f' {self._process_address(address)} exit code is '
                f'{response["result"]["exit_code"]}',
            )
        return response["result"]["stack"]

    async def get_token_data(self, address: str) -> dict:
        url = self.base_url + "/getTokenData"
        params = {"address": address}
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        return response["result"]

    async def get_jetton_wallet_address(
        self, jetton_master_address: str, owner_address: str
    ) -> Address:
        cell = tonsdk_Cell()
        cell.bits.write_address(tonsdk_Address(owner_address))
        stack: dict = await self.run_get_method(
            address=jetton_master_address,
            method=GetMethodEnum.get_wallet_address,
            stack=[["tvm.Slice", bytes_to_b64str(cell.to_boc(False))]],
        )
        jetton_wallet_address: str = read_address(
            tonsdk_Cell.one_from_boc(base64.b64decode(stack[0][1]["bytes"]))
        ).to_string()
        return self._process_address(jetton_wallet_address)

    async def get_jetton_wallet_data(self, jetton_wallet_address: str) -> JettonWalletData:
        data = await self.run_get_method(
            address=jetton_wallet_address, method=GetMethodEnum.get_wallet_data, stack=[]
        )
        wallet = {
            "address": jetton_wallet_address,
            "balance": int(data[0][1], 16),
            "owner": self._process_address(
                read_address(
                    tonsdk_Cell.one_from_boc(base64.b64decode(data[1][1]["bytes"]))
                ).to_string(False)
            ),
            "jetton_master": self._process_address(
                read_address(
                    tonsdk_Cell.one_from_boc(base64.b64decode(data[2][1]["bytes"]))
                ).to_string(False)
            ),
            "jetton_wallet_code": base64.b64decode(data[3][1]["bytes"]),
        }
        return wallet

    async def get_masterchain_info(self):
        url = self.base_url + "/getMasterchainInfo"
        result = await self.request_wrapper(MethodsEnum.GET, url, {})
        response = result["result"]
        root_hash_bytes = base64.b64decode(response["last"]["root_hash"])
        file_hash_bytes = base64.b64decode(response["last"]["file_hash"])
        response["last"]["root_hash"] = root_hash_bytes
        response["last"]["file_hash"] = file_hash_bytes
        return response

    async def request_wrapper(self, method: MethodsEnum, url: str, params: dict) -> dict:
        match method:
            case MethodsEnum.GET:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url, params=params) as response:
                        return await self.handle_response(response)
            case MethodsEnum.POST:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.post(url, data=json.dumps(params)) as response:
                        return await self.handle_response(response)
            case _:
                raise ValueError(f"Unsupported method: {method}")

    async def json_rpc_request(self, method: str, params: dict) -> dict:
        url = self.base_url + "/jsonRPC"
        data = {"method": method, "params": params, "id": uuid.uuid4().hex, "jsonrpc": "2.0"}
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(url, data=json.dumps(data)) as response:
                return await self.handle_response(response)

    async def handle_response(self, response: aiohttp.ClientResponse) -> dict:
        try:
            result = await response.json()
        except ContentTypeError as e:
            logging.error(f"Error while handling response: {e}. {response=}")
            raise HandleResponseError(f"Error while handling response: {e}, {response=}") from e
        if result["ok"] is False:
            if "error" in result:
                match result["error"]:
                    case LiteServerUnknownError.message:
                        raise LiteServerUnknownError()
                    case SmartContractIsNotJettonOrNFTError.message:
                        raise SmartContractIsNotJettonOrNFTError()
                    case IncorrectAddressError.message:
                        raise IncorrectAddressError()
            if result.get("result") == "Ratelimit exceed":
                logging.error(f"Ratelimit exceed: {result}")
            logging.error(f"Response is not 'ok': {result}")
            raise HandleResponseError(f"{result=}")
        return result

    async def get_address_information(self, address: str) -> FullAccountState:
        method = "/getAddressInformation"
        params = {"address": address}
        url = self.base_url + method
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        response_data = response["result"]
        account_state = FullAccountState(
            extra=response_data.get("@extra"),
            type=response_data.get("@type"),
            balance=int(response_data.get("balance", 0)),
            block_id=BlockIdExtDTO(
                file_hash=response_data.get("block_id", {}).get("file_hash"),
                root_hash=response_data.get("block_id", {}).get("root_hash"),
                seqno=response_data.get("block_id", {}).get("seqno"),
                shard=response_data.get("block_id", {}).get("shard"),
                workchain=response_data.get("block_id", {}).get("workchain"),
            ),
            code=response_data.get("code"),
            data=response_data.get("data"),
            frozen_hash=response_data.get("frozen_hash"),
            last_transaction_id=TransactionIdDTO(
                hash=response_data.get("last_transaction_id", {}).get("hash"),
                lt=response_data.get("last_transaction_id", {}).get("lt"),
            ),
            state=response_data.get("state"),
            sync_utime=response_data.get("sync_utime"),
        )
        return account_state

    async def get_address_state(
        self, address
    ) -> typing.Literal["uninitialized", "frozen", "active"]:
        result = await self.get_address_information(address)
        return result.state

    async def get_wallet_information(self, address) -> WalletState:
        method = "/getWalletInformation"
        url = self.base_url + method
        params = {"address": address}
        response = await self.request_wrapper(MethodsEnum.GET, url, params)
        result = response["result"]
        if result["account_state"] == AccountStateEnum.uninitialized.value:
            result["seqno"] = None
            result["wallet_id"] = None
            result["wallet_type"] = None
        return WalletState(
            account_state=AccountStateEnum(result["account_state"]).value,
            balance=int(result["balance"]),
            last_transaction_id=TransactionIdDTO(
                hash=result["last_transaction_id"]["hash"], lt=result["last_transaction_id"]["lt"]
            ),
            seqno=result["seqno"],
            wallet=result["wallet"],
            wallet_id=result["wallet_id"],
            wallet_type=result["wallet_type"],
        )

    async def get_address_balance(self, address):
        method = "/getAddressBalance"
        params = {"address": address}
        url = self.base_url + method
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url, params=params) as response:
                return await response.json()
