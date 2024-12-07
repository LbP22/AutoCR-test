cd "$(dirname "$0")"


function doIt {
  COMPOSE_DOCKER_CLI_BUILD=0 docker compose -p autocr -f inventory.yml up -d --build
}
doIt