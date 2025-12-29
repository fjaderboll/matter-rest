from fastapi import APIRouter, Depends, Response, status

from app.deps import get_matter_client
from app.models.schemas import ControllerCommandRequest, ThreadDataset, WifiCredentials
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/controller", tags=["controller"])


@router.get("/")
async def get_controller_info(client: MatterClient = Depends(get_matter_client)):
    return await client.server_info()


@router.put("/wifi-credentials", status_code=status.HTTP_204_NO_CONTENT)
async def set_wifi_credentials(
    payload: WifiCredentials, client: MatterClient = Depends(get_matter_client)
):
    await client.set_wifi_credentials(payload.ssid, payload.credentials)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/thread-credentials", status_code=status.HTTP_204_NO_CONTENT)
async def set_thread_credentials(
    payload: ThreadDataset, client: MatterClient = Depends(get_matter_client)
):
    await client.set_thread_dataset(payload.dataset)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/command")
async def send_custom_command(
    payload: ControllerCommandRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.custom_command(command=payload.command, args=payload.args)
    return result
