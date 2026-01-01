import asyncio
import json
import logging
from typing import Any, Dict, Optional

import websockets
from websockets.exceptions import (
    ConnectionClosedError,
    InvalidHandshake,
    InvalidURI,
    WebSocketException,
)

class MatterClientError(Exception):
    """Raised when the Matter server reports an error."""


class MatterClientConnectionError(Exception):
    """Raised when the Matter client cannot establish a websocket connection."""


class MatterClient:
    def __init__(self, websocket_url: str, timeout: int = 60):
        self.websocket_url = websocket_url
        self.timeout = timeout
        self.id = 0
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._send_lock = asyncio.Lock()
        self._connect_lock = asyncio.Lock()
        self._ready = False
    
    def _next_id(self) -> int:
        self.id = self.id + 1 if self.id < 2**31 - 1 else 1
        return self.id
    
    async def health_check(self) -> bool:
        await self._ensure_connection()

    async def _ensure_connection(self) -> websockets.WebSocketClientProtocol:
        if await self.is_connected():
            return self._ws

        async with self._connect_lock:
            if await self.is_connected():
                return self._ws

            try:
                self._reset_connection()
                ws = await websockets.connect(self.websocket_url)
                # The server sends a greeting/status message immediately; read and discard it.
                raw = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                logging.info("Matter server greeting: %s", raw)
            except (OSError, InvalidURI, InvalidHandshake, WebSocketException) as exc:
                self._reset_connection()
                raise MatterClientConnectionError("Cannot connect to Matter server: " + self.websocket_url) from exc
            except asyncio.TimeoutError as exc:
                self._reset_connection()
                raise TimeoutError("Matter server did not send greeting in time") from exc

            self._ws = ws
            self._ready = True
            return self._ws

    async def is_connected(self) -> bool:
        if self._ready and self._ws:
            return await self._ping()
        return False

    def _reset_connection(self) -> None:
        self._ws = None
        self._ready = False

    async def _ping(self) -> bool:
        """Ensure the websocket is alive by sending a ping."""
        try:
            pong = await self._ws.ping()
            await asyncio.wait_for(pong, timeout=self.timeout)
            return True
        except asyncio.TimeoutError as exc:
            return False
        except (ConnectionClosedError, WebSocketException, OSError) as exc:
            return False

    async def _rpc(self, command: str, args: Dict[str, Any] | None = None) -> Any:
        payload = {
            "message_id": str(self._next_id()),
            "command": command,
        }
        if args:
            payload["args"] = args

        ws = await self._ensure_connection()

        try:
            async with self._send_lock:
                data = json.dumps(payload)
                await ws.send(data)
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=self.timeout)
                except asyncio.TimeoutError as exc:
                    raise TimeoutError(
                        f"Matter server timed out waiting for {command}"
                    ) from exc
        except (ConnectionClosedError, WebSocketException) as exc:
            await self._reset_connection()
            raise MatterClientConnectionError("Cannot connect to Matter server") from exc

        response = json.loads(raw)
        if response.get("error_code"):
            raise MatterClientError(str(response.get("details", response.get("error_code"))))
        
        return response.get("result", response)

    async def set_wifi_credentials(self, ssid: str, credentials: str):
        await self._rpc(
            "set_wifi_credentials",
            {"ssid": ssid, "credentials": credentials},
        )

    async def set_thread_dataset(self, dataset: str):
        await self._rpc("set_thread_dataset", {"dataset": dataset})

    async def commission_node(self, code: str, network_only: Optional[bool] = None) -> Any:
        args: Dict[str, Any] = {"code": code}
        if network_only is not None:
            args["network_only"] = network_only
        return await self._rpc("commission_with_code", args)

    async def get_nodes(self) -> list[Dict[str, Any]]:
        result = await self._rpc("get_nodes")
        return result if isinstance(result, list) else []

    async def get_node(self, node_id: int) -> Optional[Dict[str, Any]]:
        result = await self._rpc("get_node", {"node_id": node_id})
        return result if isinstance(result, dict) else None

    async def server_info(self) -> Any:
        return await self._rpc("server_info")

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

    async def custom_command(self, command: str, args: Dict[str, Any] | None = None) -> Any:
        return await self._rpc(command, args or {})
