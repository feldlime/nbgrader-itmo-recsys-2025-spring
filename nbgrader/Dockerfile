FROM python:3.10-slim

RUN apt-get update \
    && apt-get install --yes \
        git \
        make \
        gcc \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir jupyter nbgrader

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ############################################################
## Setting up user

WORKDIR /app

ARG USER='dev'
ARG GROUP='dev'
ARG UID='1000'
ARG GID='100'

RUN groupadd --force --gid "${GID}" --non-unique "${GROUP}" \
    && adduser --uid "${UID}" --gid "${GID}" --disabled-password --gecos "" "${USER}" \
    && chown -R ${USER} /app

USER ${USER}

# ############################################################

ENV JUPYTER_CONFIG_DIR=/app

# Expose Jupyter port
EXPOSE 9999

# Default command to start Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=9999", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.base_url=/app"]
