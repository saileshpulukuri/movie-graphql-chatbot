#!/bin/bash

echo "🎬 Starting IMDB GraphQL CRUD Application"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the CS5200-Assignment directory"
    exit 1
fi

# Kill any existing processes on our ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:8501 | xargs kill -9 2>/dev/null || true
lsof -ti:11434 | xargs kill -9 2>/dev/null || true

# Check if Python dependencies are installed
echo "📦 Checking Python dependencies..."
if ! python3 -c "import flask, graphene, streamlit" 2>/dev/null; then
    echo "⚠️  Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Check if Ollama is installed
echo "🤖 Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it from https://ollama.ai"
    echo "   For macOS: curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check if llama2 model is available
echo "🧠 Checking Ollama model..."
if ! ollama list | grep -q "llama2"; then
    echo "📥 Pulling llama2 model (this may take a few minutes)..."
    ollama pull llama2
fi

# Start Ollama service in background
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!
sleep 5

# Start GraphQL backend in background
echo "🔧 Starting GraphQL backend on port 5001..."
python3 app.py &
BACKEND_PID=$!
sleep 3

# Check if backend is running
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ GraphQL backend is running"
else
    echo "❌ Failed to start GraphQL backend"
    kill $OLLAMA_PID 2>/dev/null
    exit 1
fi

# Start Streamlit frontend
echo "🌐 Starting Streamlit frontend on port 8501..."
echo ""
echo "🎉 Application is starting up!"
echo "========================================"
echo "🔗 GraphQL API: http://localhost:5001/graphql"
echo "🌐 Web Interface: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"
echo "========================================"

# Start Streamlit (this will block)
streamlit run frontend.py

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $BACKEND_PID 2>/dev/null
    kill $OLLAMA_PID 2>/dev/null
    lsof -ti:5001 | xargs kill -9 2>/dev/null || true
    lsof -ti:8501 | xargs kill -9 2>/dev/null || true
    lsof -ti:11434 | xargs kill -9 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handling
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait

