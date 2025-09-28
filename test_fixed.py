#!/usr/bin/env python3
"""
Quick test to verify the fixed application
"""

import requests
import json

def test_graphql():
    """Test GraphQL endpoint"""
    print("🧪 Testing GraphQL endpoint...")
    
    # Test basic query
    query = "query { movies { title rating year } }"
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["movies"]:
            print(f"✅ GraphQL working - Found {len(data['data']['movies'])} movies")
            print(f"Sample movie: {data['data']['movies'][0]['title']}")
            return True
        else:
            print("❌ No data returned")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_ollama():
    """Test Ollama connection"""
    print("🤖 Testing Ollama connection...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("❌ Ollama not responding")
            return False
    except:
        print("❌ Cannot connect to Ollama")
        return False

def main():
    print("🔧 Testing Fixed Application")
    print("=" * 40)
    
    # Test GraphQL
    graphql_ok = test_graphql()
    
    # Test Ollama
    ollama_ok = test_ollama()
    
    print("\n📊 Test Results:")
    print(f"GraphQL: {'✅ Working' if graphql_ok else '❌ Failed'}")
    print(f"Ollama: {'✅ Working' if ollama_ok else '❌ Failed'}")
    
    if graphql_ok and ollama_ok:
        print("\n🎉 All systems working! You can now:")
        print("1. Start the frontend: python3 -m streamlit run frontend.py")
        print("2. Open http://localhost:8501 in your browser")
        print("3. Try asking: 'Show me all movies'")
    else:
        print("\n⚠️  Some issues detected. Please check the services.")

if __name__ == "__main__":
    main()
