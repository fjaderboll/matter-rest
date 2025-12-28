from fastapi import APIRouter, Depends

from app.deps import get_matter_client
from app.models.schemas import (
    CommissioningWindowRequest,
    ThreadDataset,
    WifiCredentials,
)
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/bridge", tags=["bridge"])


@router.post("/wifi-credentials")
async def set_wifi_credentials(
    payload: WifiCredentials, client: MatterClient = Depends(get_matter_client)
):
    return await client.set_wifi_credentials(payload.ssid, payload.credentials)


@router.post("/thread-dataset")
async def set_thread_dataset(
    payload: ThreadDataset, client: MatterClient = Depends(get_matter_client)
):
    return await client.set_thread_dataset(payload.dataset)


@router.post("/commissioning-window")
async def open_commissioning_window(
    payload: CommissioningWindowRequest, client: MatterClient = Depends(get_matter_client)
):
    return await client.open_commissioning_window(payload.node_id)


@router.post("/listen")
async def start_listening(client: MatterClient = Depends(get_matter_client)):
    return await client.start_listening()
