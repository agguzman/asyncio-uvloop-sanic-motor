#!/usr/bin/env bash


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
