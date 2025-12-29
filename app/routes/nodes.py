from fastapi import APIRouter, Depends, HTTPException
import logging
import json
from app.deps import get_matter_client
from app.models.schemas import (
    AttributeWriteRequest,
    CommandArgsRequest,
    CommissionRequest,
    AttributeInfo,
    CommandArgsRequest,
    NodeInfo,
    NodeSummary,
)
from app.services.matter_client import MatterClient
from app.services.transform import create_attribute_info, create_attribute_path, map_attributes_to_objects

router = APIRouter(prefix="/nodes", tags=["nodes"])


async def _get_node_or_404(node_id: int, client: MatterClient) -> dict:
    node = await client.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node

@router.post("/")
async def commission_node(
    payload: CommissionRequest, client: MatterClient = Depends(get_matter_client)
):
    return await client.commission_node(payload.code, payload.network_only)

@router.get("/", response_model=list[NodeSummary])
async def list_nodes(client: MatterClient = Depends(get_matter_client)):
    nodes = await client.get_nodes()
    
    return [
        NodeSummary(
            node_id=int(node.get("node_id")),
            available=node.get("available"),
            is_bridge=node.get("is_bridge"),
        )
        for node in nodes
        if node.get("node_id") is not None
    ]


@router.get("/{node_id}", response_model=NodeInfo)
async def node_details(node_id: int, client: MatterClient = Depends(get_matter_client)) -> NodeInfo:
    node = await _get_node_or_404(node_id, client)
    
    return NodeInfo(
        node_id=int(node.get("node_id")),
        available=node.get("available"),
        is_bridge=node.get("is_bridge"),
        date_commissioned=node.get("date_commissioned"),
        last_interview=node.get("last_interview"),
        interview_version=node.get("interview_version"),
        endpoints=map_attributes_to_objects(node),
    )


@router.get(
    "/{node_id}/endpoints/{endpoint_id}/clusters/{cluster_id}/attributes/{attribute_id}",
    response_model=AttributeInfo,
)
async def read_attribute(
    node_id: int,
    endpoint_id: int,
    cluster_id: int,
    attribute_id: int,
    client: MatterClient = Depends(get_matter_client),
):
    attribute_path = create_attribute_path(endpoint_id, cluster_id, attribute_id)
    result = await client.read_attribute(node_id=node_id, attribute_path=attribute_path)
    return create_attribute_info(endpoint_id, cluster_id, attribute_id, result[attribute_path])

@router.put(
    "/{node_id}/endpoints/{endpoint_id}/clusters/{cluster_id}/attributes/{attribute_id}",
    response_model=AttributeInfo,
)
async def write_attribute(
    node_id: int,
    endpoint_id: int,
    cluster_id: int,
    attribute_id: int,
    payload: AttributeWriteRequest,
    client: MatterClient = Depends(get_matter_client),
):
    attribute_path = create_attribute_path(endpoint_id, cluster_id, attribute_id)
    result = await client.write_attribute(node_id=node_id, attribute_path=attribute_path, value=payload.value)
    status = result[0]['Status'] if len(result) == 1 and 'Status' in result[0] else -1
    if status == 0:
        return await read_attribute(node_id, endpoint_id, cluster_id, attribute_id, client)
    
    raise HTTPException(status_code=500, detail=f"Failed to write attribute: {status}")

@router.post("/{node_id}/endpoints/{endpoint_id}/clusters/{cluster_id}/command/{command}")
async def send_custom_device_command(
    node_id: int,
    endpoint_id: int,
    cluster_id: int,
    command: str,
    payload: CommandArgsRequest | None = None,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.device_command(
        node_id=node_id,
        endpoint_id=endpoint_id,
        cluster_id=cluster_id,
        command_name=command,
        payload=payload.args if payload else None
    )
    return result
