# Examples
Examples are given with `curl` and responses formatted with `jq`.

Below is tested on a IKEA Dirigera hub, but should hopefully work
with any matter device.

## Commission node
In IKEA's app *Home smart":
enter your *home*
-> select integrations
-> Matter bridge
-> create Matter bridge
-> get QR-kod and use that code below.

```shell
curl -X POST "http://localhost:8000/nodes/" -H "Content-Type: application/json" -d '{ "code": 1234-567-8910","network_only": true }'
```

## List node(s)
```shell
curl -s http://localhost:8000/nodes/ | jq
curl -s http://localhost:8000/nodes/4 | jq
```

## Cluster OnOff (id = 6)
### Read/write attribute value
```shell
# read current OnOff value
curl -s http://localhost:8000/nodes/4/endpoints/14/clusters/6/attributes/0 | jq

# read OnTime (attribute id = 16385)
curl -s http://localhost:8000/nodes/4/endpoints/14/clusters/6/attributes/16385 | jq

# set OnTime = 5 minutes
curl -s -X PUT http://localhost:8000/nodes/4/endpoints/14/clusters/6/attributes/16385 -H "Content-Type: application/json" -d '{ "value": 5 }' | jq
```

### Turn light on/off
```shell
# send On command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/On

# send Off command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Off

# send Toggle command
curl -s -X POST http://localhost:8000/nodes/4/endpoints/10/clusters/6/command/Toggle
```

## Cluster LevelControl (id = 8)
```shell
# read current level
curl -s http://localhost:8000/nodes/4/endpoints/14/clusters/8/attributes/0 | jq

# set brightness (0-254)
curl -s -X POST http://localhost:8000/nodes/4/endpoints/14/clusters/8/command/MoveToLevel -H "Content-Type: application/json" -d '{ "args": { "level": 254, "transitionTime": 0 } }'
```

## Further reading
It's also possible to use the same endpoint for everything and send
raw commands to the *Matter server*, see [raw-commands-examples.md](raw-commands-examples.md).

To find all possible commands and arguments, have a look [here](https://github.com/project-chip/connectedhomeip/tree/master/data_model/1.5/clusters).
