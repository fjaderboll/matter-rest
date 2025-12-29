from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class WifiCredentials(BaseModel):
    ssid: str = Field(..., description="WiFi SSID")
    credentials: str = Field(..., description="WiFi password or credentials")


class ThreadDataset(BaseModel):
    dataset: str = Field(..., description="Thread dataset blob")


class CommissionRequest(BaseModel):
    code: str = Field(..., description="Matter QR or manual pairing code")
    network_only: Optional[bool] = Field(
        None,
        description="Set true when using manual code and device is already on the network",
    )


class AttributeInfo(BaseModel):
    id: int = Field(..., description="Attribute identifier")
    path: str = Field(..., description="Attribute path")
    value: Any = Field(None, description="Current value of the attribute")


class ClusterInfo(BaseModel):
    id: int = Field(..., description="Cluster identifier")
    attributes: dict[int, AttributeInfo] = Field(default_factory=dict, description="Attributes under this cluster")


class EndpointInfo(BaseModel):
    id: int = Field(..., description="Endpoint identifier")
    clusters: dict[int, ClusterInfo] = Field(default_factory=dict, description="Clusters associated with the endpoint")


class NodeSummary(BaseModel):
    node_id: int = Field(..., description="Node identifier")
    available: bool = Field(None, description="Online or not")
    is_bridge: bool = Field(None, description="Whether the node is a bridge")


class NodeInfo(NodeSummary):
    date_commissioned: str = None
    last_interview: str = None
    interview_version: int = None
    endpoints: dict[int, EndpointInfo] = Field(default_factory=dict, description="Endpoints associated with the node")


class CommandArgsRequest(BaseModel):
    args: Optional[Dict[str, Any]] = Field(default=None, description="Optional command arguments")


class AttributeWriteRequest(BaseModel):
    value: Any = Field(..., description="Value to write to the attribute")
