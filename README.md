# Matter REST API
A REST API facade to the [Open Home Foundation Matter Server](https://github.com/matter-js/python-matter-server), providing simple HTTP endpoints to interact with your Matter devices.

## Under the hood
This simply relays commands via a websocket to the Matter server and returns the result
somewhat formatted. If you're doing something serious, you probably want to interface
the server directly.

## Examples
```shell
# list nodes
curl -s http://localhost:8000/nodes/ | jq
# get node details
curl -s http://localhost:8000/nodes/4 | jq
# read attribute
curl -s http://localhost:8000/nodes/4/endpoints/10/clusters/6/attributes/16385 | jq
# toggle light
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Toggle
```

See more examples in [IKEA Dirigera setup](docs/ikea-dirigera-setup.md)
and [command examples](docs/raw-commands-examples.md).

## Quick start
```shell
TODO
```

## Development
See details in [development.md](docs/development.md)
