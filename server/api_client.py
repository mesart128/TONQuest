import json
import logging
import os
import typing
from enum import Enum
from dotenv import load_dotenv
import aiohttp

load_dotenv()

scanner_url = os.getenv("SCANNER_URL")


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    __repr__ = __str__


class MethodsEnum(StrEnum):
    GET = "GET"
    POST = "POST"


class HttpProducer:
    def __init__(self, base_url: typing.Optional[str] = None, key: typing.Optional[str] = None):
        if base_url is None:
            base_url = "http://localhost:2024"
        self.base_url = base_url

        self.headers = {
            "Content-Type": "application/json",
        }
        if key:
            self.headers["X-API-Key"] = key

    async def handle_response(self, response: aiohttp.ClientResponse) -> dict:
        try:
            result = await response.json()
        except Exception as e:
            logging.error(f"Error while handling response: {e}. {response=}")
            raise
        return result

    async def request_wrapper(self, method: MethodsEnum, url: str, params: typing.Optional[dict] = None, data: typing.Optional[dict] = None) -> dict:
        match method:
            case MethodsEnum.GET:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.get(url, params=params) as response:
                        return await self.handle_response(response)
            case MethodsEnum.POST:
                async with aiohttp.ClientSession(headers=self.headers) as session:
                    async with session.post(url, data=json.dumps(data) if data is not None else None, params=params) as response:
                        return await self.handle_response(response)
            case _:
                raise ValueError(f"Unsupported method: {method}")

    async def add_user_to_track(self, address: str) -> None:
        event_url = f"{self.base_url}/account"
        response = await self.request_wrapper(
            method=MethodsEnum.POST,
            url=event_url,
            data={"address": address},
        )
        logging.debug(f"Send request to add user to track {address}. {response=}")
        return response


scanner_producer = HttpProducer(
    base_url=scanner_url,
)