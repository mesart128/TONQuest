from fastapi.security import APIKeyHeader
from fastapi import Request, HTTPException
from typing import Optional
from aiogram.utils.web_app import safe_parse_webapp_init_data, parse_webapp_init_data, WebAppInitData


class WebAppAuthHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> Optional[WebAppInitData]:
        init_data = request.headers.get(self.model.name)
        if not init_data:
            if self.auto_error:
                raise HTTPException(
                    status_code='401', detail="Unauthorized"
                )
            else:
                return None
            
        parsed_init_data = parse_webapp_init_data(init_data)
        return parsed_init_data