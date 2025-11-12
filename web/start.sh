#!/bin/bash

# FIRE Planning System - Quick Start Script

echo "🎯 FIRE Planning System"
echo "======================="
echo ""

# Check if we're in the web directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Please run this script from the web/ directory"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python
if ! command_exists python3; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check Node
if ! command_exists node; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo "✅ Node found: $(node --version)"
echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check .env
if [ ! -f ".env" ]; then
    if [ -f "../../.env" ]; then
        echo "Copying .env from root..."
        cp ../../.env .env
    else
        echo "⚠️  Warning: No .env file found. Create one with GROQ_API_KEY"
    fi
fi

cd ..

# Setup Frontend
echo ""
echo "📦 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check .env.local
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local..."
    cp .env.example .env.local
fi

cd ..

# Start servers
echo ""
echo "🚀 Starting servers..."
echo ""
echo "Backend will run on: http://localhost:8000"
echo "Frontend will run on: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
cd backend
source venv/bin/activate
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait a bit for backend to start
sleep 2

# Start frontend in background
cd frontend
npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up trap
trap cleanup SIGINT SIGTERM

echo "✨ Servers started!"
echo ""
echo "📖 Logs:"
echo "   Backend: web/backend.log"
echo "   Frontend: web/frontend.log"
echo ""
echo "🌐 Open your browser:"
echo "   http://localhost:3000"
echo ""

# Follow logs
tail -f backend.log frontend.log
