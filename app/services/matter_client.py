import asyncio
import json
import time
from typing import Any, Dict, Optional

import websockets


class MatterClientError(Exception):
    """Raised when the Matter server reports an error."""


class MatterClient:
    def __init__(self, websocket_url: str, timeout: int = 15):
        self.websocket_url = websocket_url
        self.timeout = timeout

    async def _rpc(self, command: str, args: Dict[str, Any] | None = None) -> Any:
        payload = {
            "message_id": str(int(time.time() * 1000)),
            "command": command,
        }
        if args:
            payload["args"] = args

        # Open a short-lived connection for each call to keep things simple.
        async with websockets.connect(self.websocket_url) as ws:
            await ws.send(json.dumps(payload))
            try:
                raw = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
            except asyncio.TimeoutError as exc:
                raise TimeoutError(f"Matter server timed out waiting for {command}") from exc

        response = json.loads(raw)
        if error := response.get("error"):
            raise MatterClientError(str(error))
        return response.get("result", response.get("message", response))

    async def set_wifi_credentials(self, ssid: str, credentials: str) -> Any:
        return await self._rpc(
            "set_wifi_credentials",
            {"ssid": ssid, "credentials": credentials},
        )

    async def set_thread_dataset(self, dataset: str) -> Any:
        return await self._rpc("set_thread_dataset", {"dataset": dataset})

    async def commission_with_code(self, code: str, network_only: Optional[bool] = None) -> Any:
        args: Dict[str, Any] = {"code": code}
        if network_only is not None:
            args["network_only"] = network_only
        return await self._rpc("commission_with_code", args)

    async def open_commissioning_window(self, node_id: int) -> Any:
        return await self._rpc("open_commissioning_window", {"node_id": node_id})

    async def get_nodes(self) -> list[Dict[str, Any]]:
        result = await self._rpc("get_nodes")
        return result if isinstance(result, list) else []

    async def get_node(self, node_id: int) -> Optional[Dict[str, Any]]:
        result = await self._rpc("get_node", {"node_id": node_id})
        return result if isinstance(result, dict) else None

    async def start_listening(self) -> Any:
        return await self._rpc("start_listening")

    async def read_attribute(self, node_id: int, attribute_path: str) -> Any:
        return await self._rpc(
            "read_attribute",
            {"node_id": node_id, "attribute_path": attribute_path},
        )

    async def write_attribute(self, node_id: int, attribute_path: str, value: Any) -> Any:
        return await self._rpc(
            "write_attribute",
            {"node_id": node_id, "attribute_path": attribute_path, "value": value},
        )

    async def device_command(
        self,
        node_id: int,
        endpoint_id: int,
        cluster_id: int,
        command_name: str,
        payload: Dict[str, Any] | None = None,
    ) -> Any:
        return await self._rpc(
            "device_command",
            {
                "node_id": node_id,
                "endpoint_id": endpoint_id,
                "cluster_id": cluster_id,
                "command_name": command_name,
                "payload": payload or {},
            },
        )
