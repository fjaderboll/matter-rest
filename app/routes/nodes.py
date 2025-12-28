from fastapi import APIRouter, Depends, HTTPException
import logging
import json
from app.deps import get_matter_client
from app.models.schemas import (
    AttributeReadRequest,
    AttributeWriteRequest,
    CommissionRequest,
    NodeCommandRequest,
    NodeDetail,
    NodeSummary,
)
from app.services.matter_client import MatterClient

router = APIRouter(prefix="/nodes", tags=["nodes"])

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
            label=node.get("label") or node.get("name"),
            online=node.get("online"),
        )
        for node in nodes
        if node.get("node_id") is not None
    ]


@router.get("/{node_id}", response_model=NodeDetail)
async def node_details(node_id: int, client: MatterClient = Depends(get_matter_client)):
    node = await client.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    #logging.debug(json.dumps(node, indent=4))
    return NodeDetail(
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
    payload: NodeCommandRequest,
    client: MatterClient = Depends(get_matter_client),
):
    result = await client.node_command(
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
