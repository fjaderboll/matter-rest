from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routes import bridge, health, nodes
from app.core.config import get_settings
from app.services.matter_client import (
    MatterClient,
    MatterClientConnectionError,
    MatterClientError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.matter_client = MatterClient(
        websocket_url=str(settings.matter_server_ws_url),
        timeout=settings.request_timeout,
    )
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s | %(levelname)-8s | "
                           "%(module)s:%(funcName)s:%(lineno)d - %(message)s")

    @app.exception_handler(MatterClientConnectionError)
    async def matter_connection_error_handler(request: Request, exc: MatterClientConnectionError) -> JSONResponse:
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    @app.exception_handler(MatterClientError)
    async def matter_client_error_handler(request: Request, exc: MatterClientError) -> JSONResponse:
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(bridge.router)
    app.include_router(nodes.router)

    return app


app = create_app()
