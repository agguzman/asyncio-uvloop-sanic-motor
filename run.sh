#!/usr/bin/env bash


# Run dev environment with mongo instance
function dev {
    docker-compose \
    --file docker-compose-dev.yml \
    up --build
}

# Run sanic server with no backend DB
function run_now {
    docker container run \
        --interactive \
        --tty \
        --rm \
        --name sanic-motor \
        --volume "$PWD":/usr/src/myapp \
        --workdir /usr/src/myapp \
        python:3 \
        python src/app.py
}

function build {
    docker image build \
        --tag my-python-app \
        --file Dockerfile-python .
}

function run {
    docker container run \
        --publish 127.0.0.1:8000:8000 \
        --rm \
        my-python-app
}
