#!/usr/bin/env bash
# The single-user demo ([mbse-basis/proposals/PRIORITIES.md, single-user demo](../../mbse-basis/proposals/PRIORITIES.md#single-user-demo-with-schema-driven-index-site-for-any-mbse-app)): the WorkTracker served by mbse-rest, persisted in memory or in
# DynamoDB Local (FEA-006, CAP-013), and browsed with mbse-react (FEA-004, FEA-005).
#
#   scripts/demo.sh [memory|dynamodb] [--check]
#
# memory (the default) keeps the store in the service's memory, so it starts fresh each run; dynamodb keeps it in
# DynamoDB Local, run in Docker, so that a write survives a restart of the service (the container, run without a
# volume, forgets it when stopped). --check starts everything, checks that each part answers, and stops it all.
#
# It needs the sibling checkouts beside this repository (mbse-schemas, mbse-rest, mbse-react, and mbse-dynamodb for
# dynamodb), uv, npm, curl, and Docker for dynamodb. Ports: the service on 8000, DynamoDB Local on 8001, the UI on 5173.

set -euo pipefail
set -m  # each background job in a process group of its own, so that stopping it stops what it started

mode=memory
check=0
for arg in "$@"; do
  case "$arg" in
    memory|dynamodb) mode=$arg ;;
    --check) check=1 ;;
    *) echo "usage: $0 [memory|dynamodb] [--check]" >&2; exit 2 ;;
  esac
done

workspace=$(cd "$(dirname "$0")/../.." && pwd)
api_port=${MBSE_REST_PORT:-8000}
db_port=8001
ui_port=5173
container=mbse-demo-dynamodb
pids=()

for sibling in mbse-schemas mbse-rest mbse-react $([ "$mode" = dynamodb ] && echo mbse-dynamodb); do
  [ -d "$workspace/$sibling" ] || { echo "missing sibling checkout: $workspace/$sibling" >&2; exit 1; }
done

stop() {
  for pid in "${pids[@]:-}"; do [ -n "$pid" ] && kill -TERM -- "-$pid" 2>/dev/null || true; done
  if [ "$mode" = dynamodb ]; then docker stop "$container" >/dev/null 2>&1 || true; fi
}
trap stop EXIT INT TERM

wait_for() {  # wait_for <url> <what>: until the URL answers, 60 seconds at most
  for _ in $(seq 1 120); do curl -sf -o /dev/null "$1" && return 0; sleep 0.5; done
  echo "$2 did not answer at $1" >&2
  exit 1
}

if [ "$mode" = dynamodb ]; then
  echo "== DynamoDB Local on $db_port"
  docker run -d --rm --name "$container" -p "$db_port:8000" amazon/dynamodb-local >/dev/null
  service_env="$workspace/mbse-dynamodb/python3"  # mbse-rest, the plugin and the WorkTracker
  export MBSE_REST_PLUGIN=mbse.Persistence.DynamoDB.Plugin:Plugin
  export MBSE_DYNAMODB_ENDPOINT_URL="http://localhost:$db_port" MBSE_DYNAMODB_TABLE=mbse-demo
  export AWS_REGION=us-east-1 AWS_ACCESS_KEY_ID=local AWS_SECRET_ACCESS_KEY=local  # DynamoDB Local takes any
  sleep 2
else
  service_env="$workspace/mbse-rest/python3"  # mbse-rest and the WorkTracker, a development dependency
  export MBSE_REST_PLUGIN=memory
fi

echo "== mbse-rest on $api_port ($mode)"
(cd "$service_env" && uv sync -q)
(cd "$service_env" && MBSE_REST_PORT="$api_port" uv run python -m mbse.Services.Rest) &
pids+=($!)
wait_for "http://localhost:$api_port/views" "mbse-rest"

echo "== mbse-react on $ui_port"
(cd "$workspace/mbse-react/typescript5" && npm install --silent)
(cd "$workspace/mbse-react/typescript5" &&
  MBSE_REST_URL="http://localhost:$api_port" npx vite --port "$ui_port" --strictPort) &
pids+=($!)
wait_for "http://localhost:$ui_port/" "mbse-react"

if [ "$check" = 1 ]; then
  echo "== checking"
  curl -sf "http://localhost:$api_port/schemas" | grep -q "work.Project" || { echo "no WorkTracker schemas" >&2; exit 1; }
  curl -sf "http://localhost:$ui_port/rest/views" | grep -q '"chip"' || { echo "the UI cannot reach the service" >&2; exit 1; }
  echo "demo is up: service, UI, and the UI's way to the service all answer"
  exit 0
fi

echo
echo "The demo is running: open http://localhost:$ui_port/ (Ctrl-C stops everything)."
wait
