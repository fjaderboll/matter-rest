from fastapi import APIRouter, Depends

from app.deps import get_matter_client
from app.models.schemas import (
    CommissioningWindowRequest,
    ControllerCommandRequest,
    ThreadDataset,
    WifiCredentials,
)
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/controller", tags=["controller"])


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


@router.post("/command")
async def send_custom_command(
    payload: ControllerCommandRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.custom_command(command=payload.command, args=payload.args)
    return result
