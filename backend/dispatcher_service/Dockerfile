FROM python:3.10-slim

# Install curl and netcat BEFORE switching user
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Create user AFTER packages are installed
RUN useradd --create-home appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x wait-for-kafka.sh

# Now switch to non-root user
USER appuser

ENV PYTHONUNBUFFERED=1

CMD ["./wait-for-kafka.sh"]
