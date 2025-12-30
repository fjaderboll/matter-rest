# Raw Matter commands
All endpoints can be accomplised by sending a raw matter command instead.

## List node(s)
```shell
curl -s http://localhost:8000/nodes/ | jq
curl -s http://localhost:8000/nodes/4 | jq

# corresponding Matter commands
curl -s -X POST http://localhost:8000/controller/command/get_nodes | jq
curl -s -X POST http://localhost:8000/controller/command/get_node -H "Content-Type: application/json" -d '{ "args": { "node_id": 4 }}' | jq
```

## Turn light on
```shell
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/On

# corresponding Matter command
curl -s -X POST http://localhost:8000/controller/command/device_command -H "Content-Type: application/json" -d '{ "args": {
                "node_id": 4,
                "endpoint_id": 10,
                "cluster_id": 6,
                "command_name": "On",
                "payload": {}
            }}'
```
