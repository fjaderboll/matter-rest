# Setup of IKEA Dirigera hub
Below is tested on a IKEA Dirigera hub, but has likely a lot in common
with other solutions.

Examples are given with `curl` and responses formatted with `jq`.

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

## Read/write attribute value
```shell
# read OnTime
curl -s http://localhost:8000/nodes/4/endpoints/10/clusters/6/attributes/16385 | jq

# set OnTime = 5 minutes
curl -s -X PUT http://localhost:8000/nodes/4/endpoints/10/clusters/6/attributes/16385 -H "Content-Type: application/json" -d '{ "value": 5 }' | jq
```

## Turn light on/off
```shell
# send On command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/On

# send Off command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Off

# send Toggle command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Toggle
```
