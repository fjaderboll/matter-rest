# Setup of IKEA Dirigera hub
Below are examples how to setup and control your lights.

## Commission node
In IKEA's app *Home smart", enter your *home*, select integrations -> Matter bridge -> create Matter bridge
-> get QR-kod and use that code below. (the code will stay the same even if you redo previous steps).

```shell
curl -X POST "http://localhost:8000/nodes/" -H "Content-Type: application/json" -d '{ "code": 1234-567-8910","network_only": true }'
```

## List node(s)
```shell
curl -s http://localhost:8000/nodes/ | jq
curl -s http://localhost:8000/nodes/4 | jq
```

## Read/write value
```shell
# read OnTime
curl -s -X POST http://localhost:8000/nodes/4/attributes/read  -H "Content-Type: application/json" -d '{ "attribute_path": "10/6/16385" }' | jq

# set OnTime = 5 minnutes
curl -s -X POST http://localhost:8000/nodes/4/attributes/write  -H "Content-Type: application/json" -d '{ "attribute_path": "10/6/16385", "value": 5 }' | jq
```

## Turn light on/off
```shell
# send On command
curl -s -X POST http://localhost:8000/nodes/4/command  -H "Content-Type: application/json" -d '{ "endpoint_id": 10, "cluster_id": 6, "command_name": "On" }'

# send Off command
curl -s -X POST http://localhost:8000/nodes/4/command  -H "Content-Type: application/json" -d '{ "endpoint_id": 10, "cluster_id": 6, "command_name": "Off" }'
```
