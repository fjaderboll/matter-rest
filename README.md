# Matter REST API

FastAPI-based REST facade for the [Matter Python Server](https://github.com/matter-js/python-matter-server), providing simple HTTP endpoints to connect to a Matter bridge, discover devices, and interact with them.

## Features
- Connect to an existing Matter bridge via WebSocket
- Discover available devices and fetch details
- Send cluster commands and read/write attributes
- Ready-to-run Docker setup with both the Matter server and this API

## Prerequisites
- Python 3.11+
- Docker (for containerized setup)

## Quickstart (local)
Start Matter server:
```shell
docker run -d \
  --name matter-server \
  --restart=unless-stopped \
  --security-opt apparmor=unconfined \
  -v matter-server-data:/data \
  --network=host \
  ghcr.io/matter-js/python-matter-server:stable
```

Start REST API:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MATTER_SERVER_WS_URL="ws://localhost:5580/ws"
uvicorn app.main:app --reload --port 8000
```
Visit http://localhost:8000/docs for the interactive OpenAPI UI.

## Run with Docker Compose
```bash
cd docker
docker compose up --build
```
- API: http://localhost:8000
- Matter server WebSocket: ws://localhost:5580

## Configuration
| Env var | Description | Default |
| --- | --- | --- |
| MATTER_APP_NAME | Display name for the API | Matter REST API |
| MATTER_SERVER_WS_URL | WebSocket endpoint for the Matter server | ws://matter-server:5580 |
| MATTER_REQUEST_TIMEOUT | Timeout in seconds for calls to the Matter server | 15 |
| MATTER_ALLOW_ORIGINS | Comma-separated list for CORS | * |

## API Overview (aligned to python-matter-server websocket API)
- `GET /health` — service status
- `POST /bridge/wifi` — `{ "ssid": "<ssid>", "credentials": "<password>" }`
- `POST /bridge/thread` — `{ "dataset": "<thread-dataset>" }`
- `POST /bridge/commission` — `{ "code": "MT:... or manual", "network_only": false }`
- `POST /bridge/commissioning-window` — `{ "node_id": 1 }`
- `POST /bridge/listen` — start streaming node events (returns initial response)
- `GET /devices/` — list commissioned nodes
- `GET /devices/{node_id}` — node details
- `POST /devices/{node_id}/commands` — `{ "endpoint_id": 1, "cluster_id": 6, "command_name": "On", "payload": { ... } }`
- `POST /devices/{node_id}/attributes/read` — `{ "attribute_path": "1/6/0" }` (endpoint/cluster/attribute)
- `POST /devices/{node_id}/attributes/write` — `{ "attribute_path": "1/6/16385", "value": 10 }`
