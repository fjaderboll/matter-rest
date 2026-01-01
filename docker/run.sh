#!/bin/bash -e

docker rm -f matter-rest
docker run -d \
  --name matter-rest \
  --restart=unless-stopped \
  -p 8000:80 \
  --add-host host.docker.internal:host-gateway \
  -e "MATTER_SERVER_WS_URL=ws://host.docker.internal:5580/ws" \
  matter-rest
