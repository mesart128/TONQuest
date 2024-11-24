from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware
from core.config import LoggerSettings
from core.dependencies import CoreContainer, initialize_container
from core.logger import setup_logging
from core.middlewares import log_body, setup_middlewares
from core.router import v1_router

# pyproject_data = toml.load("pyproject.toml")
# poetry_config = pyproject_data.get("tool", {}).get("poetry", {})

FASTAPI_CONFIG = {
    "title": "TON Service",
    "version": "0.1.0",
    "description": "Default Description",
}


def app_factory():
    logger_config = LoggerSettings()
    setup_logging(logger_settings=logger_config)
    fastapi_app = FastAPI(
        **FASTAPI_CONFIG,
        dependencies=[
            Depends(
                log_body(
                    sensitive_fields={"password"},
                )
            )
        ],
    )
    fastapi_app.include_router(v1_router)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    setup_middlewares(fastapi_app)
    core_container = CoreContainer()
    fastapi_app.container = core_container
    return fastapi_app


app = app_factory()


@app.on_event("startup")
async def startup():
    await initialize_container(app.container)


@app.on_event("shutdown")
async def shutdown():
    pass
