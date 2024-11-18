from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from apps.account.schemas import AccountSchema, AddAccountSchema
from apps.account.service import AccountService
from apps.transaction.enums import OpCodes

account_router = APIRouter(prefix="/account", tags=["account"])


@account_router.post("", description="Add account to tracking")
@inject
async def add_account(
    schema: AddAccountSchema,
    account_service: AccountService = Depends(Provide["account_service"]),
):
    result = await account_service.add_account(schema.address)
    return result


@account_router.get("", description="Add account accounts list", response_model=List[AccountSchema])
@inject
async def get_accounts(
    limit: int = 100,
    account_service: AccountService = Depends(Provide["account_service"]),
):
    return await account_service.get_accounts(limit)


@account_router.get(
    "/{address}", description="Add account accounts list", response_model=AccountSchema
)
@inject
async def get_account(
    address: str,
    account_service: AccountService = Depends(Provide["account_service"]),
):
    return await account_service.get_account(account_address=address)


@account_router.post(
    "/{address}", description="Add account accounts list", response_model=AccountSchema
)
@inject
async def make_event(
    address: str,
    op_code: OpCodes,
    account_service: AccountService = Depends(Provide["account_service"]),
):
    return await account_service.make_event(address=address, op_code=op_code)
