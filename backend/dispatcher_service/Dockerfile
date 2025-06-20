# Use official slim Python base
FROM python:3.10-slim

# Create non-root user and home directory
RUN useradd --create-home appuser

# Install netcat for our wait-for-kafka script
RUN apt-get update \
 && apt-get install -y --no-install-recommends netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service code
COPY . .

# Ensure schema and scripts are accessible
RUN chmod +x wait-for-kafka.sh

# Switch to non-root user
USER appuser

# Expose any ports if needed (none for pure consumer)
# EXPOSE 8000

# Optional healthcheck to verify Kafka connectivity
HEALTHCHECK --interval=30s --timeout=5s \
  CMD nc -z localhost 9092 || exit 1

# Unbuffered output
ENV PYTHONUNBUFFERED=1

# Entrypoint: wait for Kafka, then run app.py
CMD ["./wait-for-kafka.sh"]
