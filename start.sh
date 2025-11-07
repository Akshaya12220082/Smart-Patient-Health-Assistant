#!/bin/bash
# Quick start script for Smart Patient Health Assistant
# This script starts both the Flask API and Streamlit app

echo "🏥 Smart Patient Health Assistant - Quick Start"
echo "================================================"

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not detected."
    echo "   Consider running: source venv/bin/activate"
    echo ""
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $API_PID 2>/dev/null
    kill $STREAMLIT_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start Flask API in background
echo "🔌 Starting Flask API..."
python -m src.api.app &
API_PID=$!

# Wait for API to start
sleep 3

# Check if API started successfully
if ! ps -p $API_PID > /dev/null; then
    echo "❌ Failed to start Flask API"
    exit 1
fi

echo "✅ Flask API running (PID: $API_PID)"
echo ""

# Start Streamlit
echo "🌐 Starting Streamlit UI..."
streamlit run app.py &
STREAMLIT_PID=$!

echo ""
echo "✅ Both services are running!"
echo ""
echo "📍 Access the application at: http://localhost:8501"
echo "📍 API endpoint: http://127.0.0.1:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================================"

# Wait for both processes
wait
