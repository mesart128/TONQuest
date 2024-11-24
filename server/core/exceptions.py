import json
from abc import ABC

from starlette.responses import JSONResponse


class JsonException(ABC, Exception):
    status_code: int = None  # This field is need to be set as class attribute
    error_name: str = None  # This field is need to be set as class attribute
    error_description: str = (
        None  # This field can be set as class attribute or as argument in __init__
    )

    def __init__(
        self,
        status_code: int | None = None,
        error_name: str | None = None,
        error_description: str | None = None,
        error_meta: dict | None = None,
        headers: dict | None = None,
    ) -> None:
        if not (self.__class__.status_code or status_code):
            raise AttributeError(
                "status_code is not set, you can set it as a class attribute or as argument"
                " in __init__"
            )

        if not (self.__class__.error_name or error_name):
            raise AttributeError(
                "error_name is not set, you can set it as a class attribute or as argument"
                " in __init__"
            )

        # NOR
        if not (self.__class__.error_description or error_description):
            raise AttributeError(
                "error_description is not set, you can set it as a class attribute or as argument"
                " in __init__"
            )

        self.status_code = self.__class__.status_code or status_code
        self.error_name = self.__class__.error_name or error_name
        self.error_description = self.__class__.error_description or error_description
        self.headers = headers or {}
        self.error_meta = error_meta

        if self.__class__.status_code == 401 and self.headers.get("WWW-Authenticate") is None:
            self.headers["WWW-Authenticate"] = "Bearer"

    def _render_response_body(self) -> dict:
        return {
            "error": {
                "name": self.error_name,
                "code": self.status_code,
                "description": self.error_description,
                "meta": self.error_meta or {},
            }
        }

    def response(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.status_code,
            content=self._render_response_body(),
            headers=self.headers,
        )

    def raw_response(self) -> dict:
        return self._render_response_body()

    def json_raw_response(self) -> str:
        return json.dumps(self._render_response_body())

    def __str__(self) -> str:
        return str(self._render_response_body())
