# Use Python base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        curl \
        ca-certificates \
        build-essential \
        && rm -rf /var/lib/apt/lists/*

# Set environment variable for SSL certs
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt


# Set working directory
WORKDIR /workspace

# Copy requirements early to cache pip install step
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

CMD /bin/sh -c "while sleep 1000; do :; done"
