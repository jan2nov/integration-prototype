#!/usr/bin/env bash

#
# Script to use docker-machine to create a Docker Swarm VM cluster
#
# Run with:
#   ./swarm.sh [mode]
#

NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW=$(tput setaf 3)
RED=$(tput setaf 1)

function error() {
    echo -e "${RED}ERROR: ${NORMAL}${*}"
}

function info() {
    echo -e "${GREEN}INFO: ${NORMAL}${*}"
}

function warn() {
    echo -e "${YELLOW}WARNING: ${NORMAL}${*}"
}

function create_node() {
    STATUS=$(docker-machine status "$1" 2> /dev/null)
    NODES+=("$1")
    if [ -z "$STATUS" ]; then
        info "Creating node: $1 ..."
        docker-machine create \
        --virtualbox-cpu-count "1" \
        --virtualbox-memory "1024" \
        "${1}"
    elif [ "$STATUS" == "Running" ]; then
        warn "> Node '$1' already running."
    elif [ "$STATUS" == "Stopped" ]; then
        info "Starting node: $1 ..."
        docker-machine start "$1"
    else
        warn "> Node '$1' already exists. Status = $STATUS."
    fi
}

function usage() {
    echo "Usage: $0 [mode == (up|rm|connect)]"
}

if [ $# -ne 1 ]; then
    usage
    exit 1
fi

mode="$1"
NUM_WORKERS=2

case $mode in
    start|up|s)
        info "Starting local swarm cluster."
        create_node manager
        eval "$(docker-machine env manager)"
        info "Running swarm init on manager"
        docker swarm init \
            --advertise-addr "$(docker-machine ip manager)" \
            2> /dev/null
        for i in $(seq 1 $NUM_WORKERS); do
            create_node "worker$i"
            info "Running swarm join on worker$1"
            docker-machine ssh "worker$i" \
                docker swarm join \
                --token "$(docker swarm join-token -q worker)" \
                "$(docker-machine ip manager)":2377 \
                2> /dev/null
        done
        info "Replacing the current shell to export the docker "\
             "daemon in node 'master'."
        info "Running: 'exit' will return to the orignal shell."
        exec "$SHELL" --init-file "${HOME}"/.bash_profile -i
        ;;
    connect|c)
        info "Replacing the current shell to export the docker "\
             "daemon in node 'master'."
        info "Running: 'exit' will return to the orignal shell."
        eval "$(docker-machine env manager)"
        exec "$SHELL" --init-file "${HOME}"/.bash_profile -i
        docker-machine ls
        ;;
    rm|clean|r)
        info "Removing local swarm cluster"
        docker-machine rm manager -f
        for i in $(seq 1 $NUM_WORKERS); do
            docker-machine rm "worker$i" -f
        done
        ;;
    *)
        error "unrecognised argument: $mode"
        usage
        ;;
esac
