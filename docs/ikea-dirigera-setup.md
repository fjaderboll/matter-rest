# Setup of IKEA Dirigera hub

## Commission node
In IKEA's app *Home smart", enter your *home*, select integrations -> Matter bridge -> create Matter bridge
-> get QR-kod and use that code below. (the code will stay the same even if you redo previous steps).

```shell
curl -X POST "http://localhost:8000/nodes/" -H "Content-Type: application/json" -d '{ "code": 1234-567-8910","network_only": true }'
```

## List node(s)
```shell
curl http://localhost:8000/nodes/
curl http://localhost:8000/nodes/4
```
