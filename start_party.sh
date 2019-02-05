#!/usr/bin/env bash

xhost +local:party
docker start party
docker exec -it party /bin/bash