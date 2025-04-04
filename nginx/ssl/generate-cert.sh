#!/bin/bash

# Generate SSL certificate and private key
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout nginx.key \
    -out nginx.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set proper permissions
chmod 644 nginx.crt
chmod 600 nginx.key
