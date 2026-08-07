FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ai-service/requirements.txt ./ai-reqs.txt
COPY dashboard/requirements.txt ./dash-reqs.txt

RUN pip install --no-cache-dir -r ai-reqs.txt
RUN pip install --no-cache-dir -r dash-reqs.txt

# Copy application code
COPY ai-service /app/ai-service
COPY dashboard /app/dashboard

# Environment variables
ENV PYTHONPATH=/app
ENV API_URL=http://localhost:8000/api/v1

# Script to start both services
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

EXPOSE 8000 8501

CMD ["/app/start.sh"]
