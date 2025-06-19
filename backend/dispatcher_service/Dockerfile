FROM python:3.10-slim

WORKDIR /app

# Install netcat for wait-for-kafka.sh to work
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

COPY wait-for-kafka.sh /app/wait-for-kafka.sh
RUN chmod +x /app/wait-for-kafka.sh
CMD ["/app/wait-for-kafka.sh"]