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

See more examples in [IKEA Dirigera setup](docs/ikea-dirigera-setup.md)
and [command examples](docs/raw-commands-examples.md).

## Quick start
```shell
# start
docker stack deploy -c docker/docker-compose.yaml mr
# test
curl http://localhost:8000/health
# debug
docker service ls
docker service logs -f mr_matter-rest
# stop
docker stack rm mr
```

Visit [http://localhost:8000/docs](http://localhost:8000/docs) to see the Swagger documentation.

## Development
See details in [development.md](docs/development.md)

## TODO
Next upcoming planned features:
* Figure out how dimming lights works (`MoveToLevel`)
* Include `name` in attributes for easier readability (eg id `16385` -> name `OnTime`)
