from fastapi import APIRouter, Depends, HTTPException

from app.routes.deps import get_matter_client
from app.models.schemas import (
    AttributeReadRequest,
    AttributeWriteRequest,
    DeviceCommandRequest,
    DeviceDetail,
    DeviceSummary,
)
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/", response_model=list[DeviceSummary])
async def list_devices(client: MatterClient = Depends(get_matter_client)):
    nodes = await client.get_nodes()
    return [
        DeviceSummary(
            node_id=int(node.get("node_id")),
            label=node.get("label") or node.get("name"),
            online=node.get("online"),
        )
        for node in nodes
        if node.get("node_id") is not None
    ]


@router.get("/{node_id}", response_model=DeviceDetail)
async def device_detail(node_id: int, client: MatterClient = Depends(get_matter_client)):
    node = await client.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Device not found")
    return DeviceDetail(
        node_id=int(node.get("node_id")),
        label=node.get("label") or node.get("name"),
        online=node.get("online"),
        vendor=node.get("vendor"),
        product=node.get("product"),
        endpoints=node.get("endpoints"),
    )


@router.post("/{node_id}/commands")
async def send_command(
    node_id: int,
    payload: DeviceCommandRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.device_command(
        node_id=node_id,
        endpoint_id=payload.endpoint_id,
        cluster_id=payload.cluster_id,
        command_name=payload.command_name,
        payload=payload.payload,
    )
    return {"result": result}


@router.post("/{node_id}/attributes/read")
async def read_attribute(
    node_id: int,
    payload: AttributeReadRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.read_attribute(node_id=node_id, attribute_path=payload.attribute_path)
    return {"result": result}


@router.post("/{node_id}/attributes/write")
async def write_attribute(
    node_id: int,
    payload: AttributeWriteRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.write_attribute(
        node_id=node_id,
        attribute_path=payload.attribute_path,
        value=payload.value,
    )
    return {"result": result}
