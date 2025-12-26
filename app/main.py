from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import bridge, devices, health
from app.core.config import get_settings
from app.services.matter_client import MatterClient


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

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(bridge.router)
    app.include_router(devices.router)

    return app


app = create_app()
