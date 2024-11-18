from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.scanner.service import BlockScanner

scanner_router = APIRouter(prefix="/scanner", tags=["scanner"])


@scanner_router.get("")
@inject
async def manual_get_raw_tx_for_get_data(
    hash_: str, lt: int, address: str, scanner: BlockScanner = Depends(Provide["scanner_service"])
):
    params = {
        "address": address,
        "limit": 1,
        "hash": hash_,
        "lt": lt,
        "toLt": None,
        "archival": True,
    }
    params = {k: v for k, v in params.items() if v is not None}
    txs = await scanner.ton_rpc_client.get_transactions(
        hash_=hash_, lt=lt, address=address, count=1
    )
    return txs


#
#
# @scanner_router.get(
#     "/is_connected", dependencies=[Depends(access(Permissions.SCANNER_IS_CONNECTED))]
# )
# @inject
# async def is_connected(
#     scanner_service: BlockScanner = Depends(Provide["scanner_service"]),
# ):
#     result = await scanner_service.is_node_connected()
#     return {"node_connect_status": result}
#
#
# @scanner_router.post(
#     "/sync/block/one", dependencies=[Depends(access(Permissions.SCANNER_SYNC_BLOCK_ONE))]
# )
# @inject
# async def sync_block(
#     shard_block_id: int = Query(
#         default=-9223372036854775808,
#         description="Shard block id, default -9223372036854775808 is masterchain",
#     ),
#     workchain: int = Query(default=-1, description="Workchain. Default -1 is masterchain"),
#     masterchain_seqno: int = Query(..., description="Masterchain seqno"),
#     scanner_service: BlockScanner = Depends(Provide["scanner_service"]),
# ):
#     await scanner_service.manual_scan(
#         seqno=masterchain_seqno, shard=shard_block_id, workchain=workchain
#     )
#     return {"manual_scanned_block": masterchain_seqno, "status": "complete"}
#
#
# @scanner_router.get(
#     "/last_scanned_block_id",
#     dependencies=[Depends(access(Permissions.SCANNER_LAST_SCANNED_BLOCK_ID))],
# )
# @inject
# async def last_scanned_block(
#     scanner_service: BlockScanner = Depends(Provide["scanner_service"]),
# ):
#     result = await scanner_service.get_last_scanned_block()
#     return {"last_scanned_block": result}
#
#
# @scanner_router.get(
#     "/last_block_id", dependencies=[Depends(access(Permissions.SCANNER_LAST_BLOCK_ID))]
# )
# @inject
# async def last_masterchain_block(
#     scanner_service: BlockScanner = Depends(Provide["scanner_service"]),
# ) -> dict:
#     result = await scanner_service.get_seqno_last_masterchain_block()
#     return {"last_node_block": result}
#
#
# @scanner_router.get(
#     "/scanner_state", dependencies=[Depends(access(Permissions.SCANNER_SCANNER_STATE))]
# )
# @inject
# async def get_scanner_state(
#     scanner_service: BlockScanner = Depends(Provide["scanner_service"]),
# ) -> dict:
#     result = await scanner_service.get_scanner_state()
#     return result
