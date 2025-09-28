#!/bin/bash

echo "🚀 Starting IMDB GraphQL CRUD Application (COMPLETE VERSION)"
echo "============================================================"

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
echo "🎯 Your application features (COMPLETE):"
echo "  ✅ Quick Actions at the top (4 buttons)"
echo "  ✅ Chat interface with natural language"
echo "  ✅ Example queries below chat (9 buttons)"
echo "  ✅ Working pagination for ALL queries"
echo "  ✅ Chat input ALWAYS visible"
echo "  ✅ Multiple queries in sequence"
echo "  ✅ Clear chat button"
echo "  ✅ NO duplicate widget errors"
echo "  ✅ All buttons have unique keys"
echo ""
echo "💡 Try these features:"
echo "  - Type multiple questions in chat input"
echo "  - Click example query buttons repeatedly"
echo "  - Use '🗑️ Clear Chat' to start fresh"
echo "  - Click '📋 Show All Movies' then '📥 Show More'"
echo "  - Click '🎭 Action Movies' then '📥 Show More Action Movies'"
echo "  - All pagination works correctly!"
echo "  - Continuous conversation flow!"
echo ""

python3 -m streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
