import asyncio
import logging
import typing
from datetime import datetime

from pytoniq_core import Address, MessageAny, Transaction
from pytoniq_core.tl import BlockIdExt

from apps.account.service import AccountService
from core.enums import CustomLoggingLevels
from core.exceptions import JsonException
from core.schemas import BlockHeader, BlockIdTypedDict
from core.ton_provider import HandleResponseError, LiteServerUnknownError, TONAPIClientAsync
from database.local_storage import LocalStorage


class BlockScanner:
    def __init__(
        self,
        ton_rpc_client: TONAPIClientAsync,
        local_storage: LocalStorage,
        account_service: AccountService,
        # producer: BaseProducer,
    ):
        self.ton_rpc_client = ton_rpc_client
        self.local_storage = local_storage
        self.account_service = account_service
        # self.producer = producer
        self.shards_storage = {}
        self.blks_queue = asyncio.Queue()

    async def is_node_connected(self) -> bool:
        last_mc_block = await self.get_seqno_last_masterchain_block()
        if last_mc_block:
            return True
        return False

    async def get_last_scanned_block(self) -> int | None:
        return await self.local_storage.get_last_scanned_block()

    async def get_seqno_last_masterchain_block(self) -> int:
        master_blk: BlockIdExt = self.mc_info_to_tl_blk(
            await self.ton_rpc_client.get_masterchain_info()
        )
        return master_blk.seqno

    async def get_scanner_state(self):
        last_scanned_block = await self.get_last_scanned_block()
        last_masterchain_block = await self.get_seqno_last_masterchain_block()
        is_connected = await self.is_node_connected()
        scanner_lags = last_masterchain_block - last_scanned_block
        return {
            "last_scanned_block": last_scanned_block,
            "last_masterchain_block": last_masterchain_block,
            "is_connected": is_connected,
            "scanner_lags": scanner_lags,
        }

    async def get_master_seqno_for_scan(self) -> int:
        last_scanned_block = await self.get_last_scanned_block()
        master_blk_seqno = await self.get_seqno_last_masterchain_block()
        if last_scanned_block is None:
            return master_blk_seqno - 1
        if last_scanned_block < master_blk_seqno:
            return last_scanned_block + 1
        else:
            raise ValueError("No new blocks to scan")

    async def manual_scan(self, seqno: int, shard: int, workchain: int):
        logging.info(f"Manual scanning masterchain block {seqno}")
        try:
            master_blk, _ = await self.ton_rpc_client.lookup_block(
                wc=workchain, shard=shard, seqno=seqno
            )
        except HandleResponseError as e:
            raise JsonException(
                status_code=400,
                error_description=f"Failed to lookup block {seqno} {shard} {workchain}: {e}",
                error_name="LITE_SERVER_ERROR",
            ) from e
        if master_blk.workchain == -1:
            shards = await self.ton_rpc_client.get_all_shards_info(master_blk)
            for shard in shards:
                await self.handle_block(shard, manual_scan=True)
        else:
            await self.handle_block(master_blk, manual_scan=True)

    async def get_not_seen_shards(self, shard: BlockIdExt):
        if self.shards_storage.get(self.get_shard_id(shard)) == shard.seqno:
            return
        block_header: BlockHeader = await self.ton_rpc_client.get_block_header(shard)
        if not block_header.after_merge:
            prev: BlockIdTypedDict = block_header.prev_blocks[0]
            prev_shard = (
                self.get_parent_shard(shard.shard) if block_header.after_split else shard.shard
            )
            await self.get_not_seen_shards(
                BlockIdExt(
                    workchain=shard.workchain,
                    seqno=prev["seqno"],
                    shard=prev_shard,
                    root_hash=prev["root_hash"],
                    file_hash=prev["file_hash"],
                )
            )
        else:
            prev1: BlockIdTypedDict = block_header.prev_blocks[0]
            prev2: BlockIdTypedDict = block_header.prev_blocks[1]
            await self.get_not_seen_shards(
                BlockIdExt(
                    workchain=shard.workchain,
                    seqno=prev1["seqno"],
                    shard=self.get_child_shard(int(shard.shard), left=True),
                    root_hash=prev1["root_hash"],
                    file_hash=prev1["file_hash"],
                )
            )
            await self.get_not_seen_shards(
                BlockIdExt(
                    workchain=shard.workchain,
                    seqno=prev2["seqno"],
                    shard=self.get_child_shard(int(shard.shard), left=False),
                    root_hash=prev2["root_hash"],
                    file_hash=prev2["file_hash"],
                )
            )

        await self.blks_queue.put(shard)

    def get_child_shard(self, shard: int, left: bool) -> int:
        if not isinstance(shard, int):
            shard = int(shard)
        x = self.lower_bit64(shard) >> 1
        if left:
            return self.simulate_overflow(shard - x)
        return self.simulate_overflow(shard + x)

    def get_parent_shard(self, shard: int) -> int:
        if not isinstance(shard, int):
            shard = int(shard)
        x = self.lower_bit64(shard)
        return self.simulate_overflow((shard - x) | (x << 1))

    @staticmethod
    def simulate_overflow(x) -> int:
        return (x + 2**63) % 2**64 - 2**63

    @staticmethod
    def lower_bit64(num: int) -> int:
        return num & (~num + 1)

    async def run(self):
        mc_seqno = await self.get_master_seqno_for_scan()
        logging.info("Starting scanner")
        master_blk, _ = await self.ton_rpc_client.lookup_block(
            wc=-1, shard=-9223372036854775808, seqno=mc_seqno
        )
        master_blk_prev, _ = await self.ton_rpc_client.lookup_block(
            wc=-1, shard=-9223372036854775808, seqno=master_blk.seqno - 1
        )
        shards_prev = await self.ton_rpc_client.get_all_shards_info(master_blk_prev)
        for shard in shards_prev:
            self.shards_storage[self.get_shard_id(shard)] = shard.seqno
        while True:
            try:
                logging.debug(f"Scanning masterchain block {master_blk.seqno}")
                await self.blks_queue.put(master_blk)
                shards = await self.ton_rpc_client.get_all_shards_info(master_blk)
                shard_tasks = [self.get_not_seen_shards(shard) for shard in shards]
                await asyncio.gather(*shard_tasks)
                for shard in shards:
                    self.shards_storage[self.get_shard_id(shard)] = shard.seqno
                while not self.blks_queue.empty():
                    block_to_handle = self.blks_queue.get_nowait()
                    number_tries = 50
                    for i in range(number_tries):
                        try:
                            await self.handle_block(block_to_handle)
                            break
                        except LiteServerUnknownError:
                            logging.warning(
                                f"Failed to handle shard block: "
                                f"{block_to_handle.seqno=} "
                                f"{block_to_handle.shard=}"
                            )
                        except HandleResponseError as e:
                            logging.warning(
                                f"Failed to handle block. \n"
                                f"Retry {i} for block {block_to_handle.seqno}. \n"
                                f"Error: {e}",
                                exc_info=True,
                            )
                        await asyncio.sleep(0.1)
                        if i == number_tries - 1:
                            logging.log(
                                CustomLoggingLevels.ADMIN,
                                f"Failed to handle block {block_to_handle.seqno} "
                                f"after {number_tries} retries",
                                exc_info=True,
                            )

                while True:
                    last_mc_block: BlockIdExt = self.mc_info_to_tl_blk(
                        await self.ton_rpc_client.get_masterchain_info()
                    )
                    if master_blk.seqno + 1 == last_mc_block.seqno:
                        master_blk = last_mc_block
                        break
                    elif master_blk.seqno + 1 < last_mc_block.seqno:
                        master_blk, _ = await self.ton_rpc_client.lookup_block(
                            wc=-1, shard=-9223372036854775808, seqno=master_blk.seqno + 1
                        )
                        break
                    await asyncio.sleep(0.3)
            except HandleResponseError as e:
                if isinstance(e, LiteServerUnknownError):
                    LiteServerUnknownError.increment_counter()
                    if LiteServerUnknownError.should_raise():
                        logging.warning(f"Encountered predictable error: {e}")
                        LiteServerUnknownError.reset_counter()
                    continue
                logging.error(f"Failed to scan block: {e}", exc_info=True)
            except Exception as e:
                logging.log(
                    CustomLoggingLevels.ADMIN,
                    f"Failed to scan master block {master_blk.seqno=}, {master_blk.shard}: {e}.",
                    exc_info=True,
                )

    @staticmethod
    def get_shard_id(blk: BlockIdExt):
        return f"{blk.workchain}:{blk.shard}"

    @staticmethod
    def mc_info_to_tl_blk(info: dict):
        return BlockIdExt.from_dict(info["last"])

    async def mc_seqno_by_shard(self, shard: BlockIdExt):
        full_blk: BlockHeader = await self.ton_rpc_client.get_block_header(shard)
        mc_seqno = full_blk.min_ref_mc_seqno
        return mc_seqno

    async def blockchain_tx_to_raw_transaction(
        self, tx: Transaction, block: BlockIdExt, mc_seqno: typing.Optional[int] = None
    ):
        if mc_seqno is None:
            mc_seqno = await self.mc_seqno_by_shard(block)
        parsed_transaction = (
            await self.account_service.transaction_service.chain_transaction_to_dto(
                tx, block, masterchain_seqno=mc_seqno
            )
        )
        logging.debug(f"Scanning transaction: {parsed_transaction=}")
        return parsed_transaction

    async def handle_out_msgs(self, out_msgs: typing.List[MessageAny]) -> None:
        for out_msg in out_msgs:
            if out_msg.info.dest is None:
                # case External out message: swap logs
                await self.account_service.handle_external_out_msg(out_msg)

    async def scan_transaction(self, tx: Transaction, block: BlockIdExt):
        system_account = await self.account_service.get_account(Address(f"0:{tx.account_addr_hex}"))
        if system_account is not None:
            raw_transaction_dto = await self.blockchain_tx_to_raw_transaction(tx, block)
            logging.debug(f"Transaction {raw_transaction_dto} is system account")
            await self.account_service.handle_transaction_on_account(raw_transaction_dto)
        await self.handle_out_msgs(out_msgs=tx.out_msgs)

    async def handle_block(self, block: BlockIdExt, manual_scan: bool = False):
        if block.workchain == -1:  # skip masterchain blocks
            logging.debug(f"Skip masterchain block in handle block: {block.seqno}")
            if manual_scan is False:
                await self.local_storage.set_last_scanned_block(block.seqno)
            return
        time_start = datetime.now()
        transactions = await self.ton_rpc_client.raw_get_block_transactions_ext(block, 1028)
        transactions.sort(key=lambda x: x.lt)
        for tx in transactions:
            tx: Transaction
            await self.scan_transaction(tx, block)

        logging.debug(
            f"Scanned shard block {block.shard} {block.seqno} with {len(transactions)=}"
            f" in {(datetime.now() - time_start).microseconds} microseconds"
        )
