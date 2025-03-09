FROM quay.io/oauth2-proxy/oauth2-proxy:v7.5.1

# Copy configuration
COPY oauth2-proxy.cfg /etc/oauth2-proxy/oauth2-proxy.cfg

EXPOSE 4180

ENTRYPOINT ["/bin/oauth2-proxy", "--config=/etc/oauth2-proxy/oauth2-proxy.cfg"]
