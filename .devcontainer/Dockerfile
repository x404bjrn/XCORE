# Basis-Image mit Python 3.11
FROM python:3.11-slim

# Node.js installieren (für Vite-React-Frontend)
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs git && \
    apt-get clean

# Arbeitsverzeichnis setzen
WORKDIR /workspace

# UTF-8, pip-Konfiguration
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1
