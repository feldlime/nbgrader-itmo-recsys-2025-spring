build:
    docker build \
        --rm \
        --build-arg UID="$(id -u)" \
        --build-arg GID="$(id -g)" \
        -f Dockerfile \
        -t emiliy_nbgrader \
        .


run *flags:
    docker run {{ flags }} \
        --rm \
        -it \
        --network host \
        -v "${PWD}/nbgrader:/app/nbgrader" \
        --name emiliy-nbgrader \
        emiliy_nbgrader \
        /bin/bash


run-jupyter:
    docker run -d \
        --rm \
        -it \
        -p 11234:11234 \
        -v "${PWD}/nbgrader:/app" \
        -v "${PWD}/exchange:/usr/local/share/nbgrader/exchange" \
        --name emiliy-nbgrader \
        emiliy_nbgrader \
        jupyter notebook \
            --allow-root \
            --ip=0.0.0.0 \
            --no-browser \
            --port=11234 \
            --port-retries=0 \
            --NotebookApp.token="ms" \
            --NotebookApp.password="ms"


stop:
    docker rm --force emiliy-nbgrader
