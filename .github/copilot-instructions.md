# Copilot Instructions - Repository Outline

## Purpose
An easy to use REST API for your Matter devices.

It will be based on the officially certified [Open Home Foundation Matter Server](https://github.com/matter-js/python-matter-server) SDK
and act as a controller for your Matter devices.

## Technical Stack
- Primary Language: Python
- Web Framework: FastAPI

## Setup
The Docker image `ghcr.io/matter-js/python-matter-server` will run the Matter server, 
and this app will interact with the server over the websocket.

## Repository Structure
- `app/`: Main application source code.
- `docs/`: Documentation files.
- `docker/`: Dockerfile, Docker compose and such.
- `tests/`: Unit and integration tests.
- `requirements.txt`: Python dependencies.
