from fastapi import APIRouter, Depends

from app.routes.deps import get_matter_client
from app.models.schemas import (
    CommissioningWindowRequest,
    CommissionRequest,
    ThreadDataset,
    WifiCredentials,
)
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/bridge", tags=["bridge"])


@router.post("/wifi")
async def set_wifi_credentials(
    payload: WifiCredentials, client: MatterClient = Depends(get_matter_client)
):
    return await client.set_wifi_credentials(payload.ssid, payload.credentials)


@router.post("/thread")
async def set_thread_dataset(
    payload: ThreadDataset, client: MatterClient = Depends(get_matter_client)
):
    return await client.set_thread_dataset(payload.dataset)


@router.post("/commission")
async def commission_with_code(
    payload: CommissionRequest, client: MatterClient = Depends(get_matter_client)
):
    return await client.commission_with_code(payload.code, payload.network_only)


@router.post("/commissioning-window")
async def open_commissioning_window(
    payload: CommissioningWindowRequest, client: MatterClient = Depends(get_matter_client)
):
    return await client.open_commissioning_window(payload.node_id)


@router.post("/listen")
async def start_listening(client: MatterClient = Depends(get_matter_client)):
    return await client.start_listening()
