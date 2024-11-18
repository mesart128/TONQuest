import json
import logging
import typing

import aiohttp

from core.ton_provider import MethodsEnum


class HttpProducer:
    def __init__(self, base_url: typing.Optional[str] = None, key: typing.Optional[str] = None):
        if base_url is None:
            base_url = "https://go.getblock.io/95dfd73af9144e4e823cc81f2bed942a"
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

    async def publish_task_event(self, data: dict) -> None:
        logging.debug(f"Publishing task event with data: {data}")
        event_url = f"{self.base_url}/tasks/complete"

        response = await self.request_wrapper(
            method=MethodsEnum.POST,
            url=event_url,
            params=data,
        )
        logging.debug(f"Data for task {data} published. {response=}")
        return response
