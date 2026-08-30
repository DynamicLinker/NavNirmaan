#!/bin/bash
# Start backend in the background
cd /app/Backend
uvicorn server:app --host 0.0.0.0 --port 8000 &

# Start Frontend in the foreground
cd /app/Frontend
python3 -m http.server 8080
