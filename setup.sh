#!/bin/bash

echo "🎬 Setting up IMDB GraphQL CRUD Application..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama is not installed. Please install it from https://ollama.ai"
    echo "   For macOS: curl -fsSL https://ollama.ai/install.sh | sh"
    echo "   Then run: ollama pull llama2"
else
    echo "✅ Ollama found"
    
    # Check if llama2 model is available
    if ! ollama list | grep -q "llama2"; then
        echo "📥 Pulling llama2 model..."
        ollama pull llama2
    else
        echo "✅ llama2 model found"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating .env file..."
    echo "OLLAMA_URL=http://localhost:11434" > .env
    echo "✅ .env file created"
else
    echo "✅ .env file exists"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Start the backend: python3 app.py"
echo "3. Start the frontend: streamlit run frontend.py"
echo ""
echo "🌐 Access points:"
echo "- GraphQL API: http://localhost:5000/graphql"
echo "- Frontend UI: http://localhost:8501"
echo ""


