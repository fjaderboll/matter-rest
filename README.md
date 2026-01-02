# Matter REST API
A REST API facade to the [Open Home Foundation Matter Server](https://github.com/matter-js/python-matter-server), providing simple HTTP endpoints to interact with your Matter devices.

## Under the hood
This simply relays commands via a websocket to the Matter server and returns the result
somewhat formatted. If you're doing something serious, you probably want to interface
the server directly.

## Examples
```shell
# list nodes
curl http://localhost:8000/nodes/
# get node details
curl http://localhost:8000/nodes/4
# read attribute
curl http://localhost:8000/nodes/4/endpoints/10/clusters/6/attributes/16385
# toggle light
curl -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Toggle
```

See more details and examples in [examples.md](docs/examples.md).

## Quick start
If you've cloned this repo you can simply run:
```shell
docker stack deploy -c docker/docker-compose.yaml mr
```
else see below.

### Start Matter server
```shell
docker run -d \
  --name matter-server \
  --restart=unless-stopped \
  --security-opt apparmor=unconfined \
  -v matter-server-data:/data \
  --network=host \
  ghcr.io/matter-js/python-matter-server:stable
```

### Start Matter REST
```shell
docker run -d \
  --name matter-rest \
  --restart=unless-stopped \
  -p 8000:80 \
  --add-host host.docker.internal:host-gateway \
  -e "MATTER_SERVER_WS_URL=ws://host.docker.internal:5580/ws" \
  ghcr.io/fjaderboll/matter-rest:latest

# test
curl http://localhost:8000/health
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger documentation.

## Development
See details in [development.md](docs/development.md)

## TODO
Next upcoming planned stuff:
* Add more examples in [examples.md](docs/examples.md)
* Include `name` in attributes for easier readability (eg id `16385` -> name `OnTime`)
