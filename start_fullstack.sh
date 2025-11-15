#!/bin/bash
# One-command startup for Smart Patient Health Assistant

echo "🏥 Smart Patient Health Assistant - Full Stack Launcher"
echo "========================================================"

# Navigate to project root
cd "$(dirname "$0")"

# Check if venv exists for backend
if [ ! -d "venv" ]; then
    echo "⚠️  Backend virtual environment not found."
    echo "Creating virtual environment and installing dependencies..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    pip install streamlit -q
fi

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Cleanup existing processes
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null
lsof -ti:3000 | xargs kill -9 2>/dev/null
sleep 1

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down all services..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    jobs -p | xargs kill -9 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo ""
echo "🚀 Starting all services..."
echo ""

# Start Flask API
echo "🔌 Starting Flask API on port 5001..."
source venv/bin/activate
python -m src.api.app > /tmp/flask_api.log 2>&1 &
FLASK_PID=$!

# Wait a bit for Flask to start
sleep 3

# Check if Flask started successfully
if ps -p $FLASK_PID > /dev/null 2>&1; then
    echo "✅ Flask API running (PID: $FLASK_PID)"
else
    echo "❌ Failed to start Flask API. Check /tmp/flask_api.log for details"
    tail -20 /tmp/flask_api.log
    exit 1
fi

# Start Next.js frontend
echo "🌐 Starting Next.js Frontend on port 3000..."
cd frontend
npm run dev > /tmp/nextjs.log 2>&1 &
NEXT_PID=$!
cd ..

# Wait for Next.js to start
sleep 5

# Check if Next.js started successfully
if ps -p $NEXT_PID > /dev/null 2>&1; then
    echo "✅ Next.js Frontend running (PID: $NEXT_PID)"
else
    echo "⚠️  Next.js may still be starting..."
fi

echo ""
echo "✅ All services started!"
echo ""
echo "📍 Access your application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5001"
echo ""
echo "📋 View logs:"
echo "   Flask API: tail -f /tmp/flask_api.log"
echo "   Next.js: tail -f /tmp/nextjs.log"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================================"
echo ""

# Keep script running
while true; do
    # Check if processes are still running
    if ! ps -p $FLASK_PID > /dev/null 2>&1; then
        echo "⚠️  Flask API stopped unexpectedly"
        break
    fi
    if ! ps -p $NEXT_PID > /dev/null 2>&1; then
        echo "⚠️  Next.js stopped unexpectedly"
        break
    fi
    sleep 5
done

cleanup
