#!/bin/bash

PORT="9003"
TIMEOUT=600  # seconds of inactivity before stopping (10 min)

COMPOSE_YML="/opt/llm/docker-compose.yml"
IDLE_FILE="/opt/llm/timeout.txt"
PLACEHOLDER="/opt/llm/placeholder/server.py"

start_placeholder() {
    echo "Starting placeholder webserver..."
    $PLACEHOLDER
}

is_placeholder_running() {
    ss -tulpn | grep ":$PORT" | grep -q python3
}

# check if there are active connections
if ss -tn sport = :$PORT | grep -q ESTAB; then
    echo "Active connection on port $PORT"
    date +%s > "$IDLE_FILE"

# no active connections
else
    if is_placeholder_running; then
        echo "No active connections and placeholder running. Nothing to do..."
        exit
    fi

    LAST_SEEN=$(cat "$IDLE_FILE")
    NOW=$(date +%s)

    # check if container should be stopped
    if (( NOW - LAST_SEEN > TIMEOUT )); then
        echo "No connection for $TIMEOUT seconds. Stopping container..."
        docker compose -f "$COMPOSE_YML" down
        start_placeholder
    else
        echo "No active connection. Timeout in $(( TIMEOUT - NOW + LAST_SEEN )) seconds."
    fi
fi
