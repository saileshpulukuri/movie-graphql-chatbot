#!/bin/bash

echo "🚀 Starting IMDB GraphQL CRUD Application (Final Version)"
echo "=================================================="

# Check if Ollama is running
echo "🤖 Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running. Starting Ollama..."
    brew services start ollama
    sleep 3
fi

# Start GraphQL backend
echo "🔧 Starting GraphQL backend..."
python3 app.py &
BACKEND_PID=$!
sleep 3

# Check if backend is running
echo "🧪 Testing GraphQL backend..."
if curl -s http://localhost:5001/graphql -X POST -H "Content-Type: application/json" -d '{"query":"query { movies { id title } }"}' > /dev/null 2>&1; then
    echo "✅ GraphQL backend is running on port 5001"
else
    echo "❌ GraphQL backend failed to start"
    exit 1
fi

# Start Streamlit frontend
echo "🎬 Starting Streamlit frontend..."
echo "📱 Frontend will open at: http://localhost:8501"
echo ""
echo "🎯 Your application features:"
echo "  ✅ Quick Actions at the top"
echo "  ✅ Chat interface with natural language"
echo "  ✅ Example queries below chat"
echo "  ✅ Working pagination for all movies"
echo "  ✅ Working pagination for action movies"
echo "  ✅ 9 example query buttons"
echo ""
echo "💡 Try these features:"
echo "  - Click '📋 Show All Movies' then '📥 Show More'"
echo "  - Click '🎭 Action Movies' then '📥 Show More Action Movies'"
echo "  - Use the chat: 'Show me all movies'"
echo "  - Click example query buttons"
echo ""

python3 -m streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
