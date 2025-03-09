default:
  @just --list --justfile {{justfile()}}

# ############################################################

nbgrader-build:
    docker build \
        --rm \
        --build-arg UID="$(id -u)" \
        --build-arg GID="$(id -g)" \
        -f nbgrader/Dockerfile \
        -t nbgrader \
        nbgrader


nbgrader-start:
    docker run -d \
        --rm \
        -it \
        -p 9999:9999 \
        -v "${PWD}/nbgrader/app:/app" \
        -v "${PWD}/exchange:/usr/local/share/nbgrader/exchange" \
        --name nbgrader \
        nbgrader


nbgrader-stop:
    docker rm --force nbgrader

# ############################################################

puller-build:
    docker build \
        --rm \
        --build-arg UID="$(id -u)" \
        --build-arg GID="$(id -g)" \
        -f puller/Dockerfile \
        -t puller \
        puller


puller-start:
    docker run \
        --rm \
        -it \
        -p 8501:8501 \
        -v "${PWD}/puller:/app" \
        -v "${PWD}/exchange:/exchange" \
        --env-file "${PWD}/puller/.env" \
        --name puller \
        puller

puller-stop:
    docker rm --force puller


# ############################################################

# Production commands
prod-build:
    docker compose build --build-arg UID="$(id -u)" --build-arg GID="$(id -g)"

prod-up:
    docker compose up --no-build

prod-down:
    docker compose down

# Development commands
dev-build:
    NGINX_HTTP_PORT=8080 NGINX_HTTPS_PORT=8443 docker compose -f docker-compose.yml -f docker-compose.dev.yml build

dev-up:
    NGINX_HTTP_PORT=8080 NGINX_HTTPS_PORT=8443 docker compose -f docker-compose.yml -f docker-compose.dev.yml up --no-build

dev-down:
    docker compose -f docker-compose.yml -f docker-compose.dev.yml down

# ############################################################

run-ansible:
    ansible-playbook -i ansible/inventory.ini ansible/setup_remote.yml -vv  # --start-at-task="Copy .env"
