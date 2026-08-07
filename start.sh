#!/bin/bash

# Start FastAPI in the background
cd /app/ai-service
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 3

# Start Streamlit in the foreground
cd /app/dashboard
streamlit run app.py --server.port 8501 --server.address 0.0.0.0

# If Streamlit exits, kill FastAPI
kill $FASTAPI_PID
