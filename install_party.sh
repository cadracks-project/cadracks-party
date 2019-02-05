#!/usr/bin/env bash

# username="$USER"
# user="$(id -u)"
home="${1:-$HOME}"

imageName="guillaume-florent/cadracks_party:latest"
containerName="cadracks_party"
displayVar="$DISPLAY"

docker build --file Dockerfile.py3 --tag ${imageName} .

docker run  -it -d --name ${containerName}                  \
    -e DISPLAY=${displayVar}                                \
    --workdir="${home}"                                     \
    --volume="${home}:${home}"                              \
     -v=/tmp/.X11-unix:/tmp/.X11-unix ${imageName}          \
     /bin/bash
