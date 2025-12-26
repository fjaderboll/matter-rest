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


class CommissioningWindowRequest(BaseModel):
    node_id: int = Field(..., description="Existing node id to open window for")


class DeviceSummary(BaseModel):
    node_id: int = Field(..., description="Node identifier")
    label: Optional[str] = Field(None, description="Human friendly name")
    online: Optional[bool] = Field(None, description="Whether the node is reachable")


class DeviceDetail(DeviceSummary):
    vendor: Optional[str] = None
    product: Optional[str] = None
    endpoints: Optional[list[Dict[str, Any]]] = None


class DeviceCommandRequest(BaseModel):
    endpoint_id: int = Field(..., description="Endpoint id for the command")
    cluster_id: int = Field(..., description="Cluster id (numerical)")
    command_name: str = Field(..., description="Command name as defined by the cluster")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Command payload")


class AttributeReadRequest(BaseModel):
    attribute_path: str = Field(..., description="Path formatted as endpoint/cluster/attribute (e.g. 1/6/0)")


class AttributeWriteRequest(AttributeReadRequest):
    value: Any = Field(..., description="Value to write to the attribute")
