FROM python:3.11-slim

WORKDIR /app

# Install git
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501


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


# ############################################################

ENV PYTHONPATH=.

# Run the application
CMD ["streamlit", "run", "service/app.py", "--server.address", "0.0.0.0"]
