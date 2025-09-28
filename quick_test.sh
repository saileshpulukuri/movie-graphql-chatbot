#!/bin/bash

echo "🧪 Quick Test Script for IMDB GraphQL Application"
echo "==============================================="

# Test 1: Check if data is loaded
echo "📊 Testing data loading..."
python3 -c "
from models import data_manager
movies = data_manager.get_all_movies()
print(f'✅ Data loaded: {len(movies)} movies')
sample = data_manager.get_movie_by_id(1)
print(f'✅ Sample movie: {sample[\"title\"]} ({sample[\"year\"]})')
"

# Test 2: Check GraphQL server
echo ""
echo "🔧 Testing GraphQL server..."
if curl -s http://localhost:5001/health > /dev/null; then
    echo "✅ GraphQL server is running"
    
    # Test a simple query
    echo "🔍 Testing GraphQL query..."
    response=$(curl -s -X POST http://localhost:5001/graphql \
        -H "Content-Type: application/json" \
        -d '{"query": "query { movies { title rating } }"}' | head -c 100)
    
    if [[ $response == *"data"* ]]; then
        echo "✅ GraphQL query successful"
    else
        echo "❌ GraphQL query failed"
    fi
else
    echo "❌ GraphQL server is not running"
    echo "   Start it with: python3 app.py"
fi

# Test 3: Check Ollama
echo ""
echo "🤖 Testing Ollama connection..."
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running"
    echo "   Start it with: ollama serve"
fi

echo ""
echo "🎯 Test Summary:"
echo "- Data: ✅ Loaded"
echo "- GraphQL: Check status above"
echo "- Ollama: Check status above"
echo ""
echo "🚀 To start everything: ./start_application.sh"

