#!/bin/bash
# Quick start script for Smart Patient Health Assistant
# Single command to start both Flask API and Streamlit app

echo "🏥 Smart Patient Health Assistant - Quick Start"
echo "================================================"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Run: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Kill any existing processes on ports 5001 and 8501
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:8501 | xargs kill -9 2>/dev/null
sleep 1

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    jobs -p | xargs kill 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo "🚀 Starting services..."
echo ""

# Start both services in background and redirect output
python -m src.api.app > /tmp/flask_api.log 2>&1 & 
sleep 2
streamlit run app.py > /tmp/streamlit.log 2>&1 &

# Wait a moment for services to start
sleep 3

echo "✅ Both services are running!"
echo ""
echo "📍 Access the application at: http://localhost:8501"
echo "📍 API endpoint: http://127.0.0.1:5001"
echo ""
echo "📋 Logs:"
echo "   Flask API: tail -f /tmp/flask_api.log"
echo "   Streamlit: tail -f /tmp/streamlit.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"

# Keep script running and wait for all background jobs
wait
