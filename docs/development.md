# Development
If you're using *Visual Studio Code*, you can preferable use
the launch configurations to start it up.

## Start Matter server
This is self-sustained, and only needs to be running in the background.

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
Build and run a local image `matter-rest`.

```shell
./docker/build.sh
./docker/run.sh
curl http://localhost:8000/health
```
