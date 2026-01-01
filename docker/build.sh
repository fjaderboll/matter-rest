#!/bin/bash -e

cd "$(dirname "$0")"
docker build -t matter-rest -f Dockerfile ..
