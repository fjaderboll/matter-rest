# Development

## Prerequisites
- Python 3.11+

## Start Matter server
```shell
docker run -d \
  --name matter-server \
  --restart=unless-stopped \
  --security-opt apparmor=unconfined \
  -v matter-server-data:/data \
  --network=host \
  ghcr.io/matter-js/python-matter-server:stable
```

## Start REST API
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export MATTER_SERVER_WS_URL="ws://localhost:5580/ws"
uvicorn app.main:app --reload --port 8000

# test
curl http://localhost:8000/health
```

Visit http://localhost:8000/docs for Swagger documentation.

## Docker build
```shell
docker build -t matter-rest -f docker/Dockerfile .
docker run -d \
  --name matter-rest \
  --restart=unless-stopped \
  -p 8000:80 \
  -e "MATTER_SERVER_WS_URL=ws://192.168.1.3:5580/ws" \
  matter-rest
curl http://localhost:8000/health
```
