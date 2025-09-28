#!/usr/bin/env python3
"""
Test specific queries to verify the application works correctly
"""

import requests
import json

def test_action_movies():
    """Test action movies query"""
    print("🎭 Testing Action Movies Query...")
    
    query = 'query { searchMovies(genre: ["Action"]) { id title year genre rating } }'
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["searchMovies"]:
            movies = data["data"]["searchMovies"]
            print(f"✅ Found {len(movies)} action movies")
            print("Sample action movies:")
            for i, movie in enumerate(movies[:5]):
                print(f"  {i+1}. {movie['title']} ({movie['year']}) - {movie['rating']}")
            return True
        else:
            print("❌ No action movies found")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_christopher_nolan():
    """Test Christopher Nolan query"""
    print("🎬 Testing Christopher Nolan Query...")
    
    query = 'query { searchMovies(director: "Christopher Nolan") { id title year genre rating director } }'
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["searchMovies"]:
            movies = data["data"]["searchMovies"]
            print(f"✅ Found {len(movies)} movies by Christopher Nolan")
            for movie in movies:
                print(f"  - {movie['title']} ({movie['year']}) - {movie['rating']}")
            return True
        else:
            print("❌ No movies by Christopher Nolan found")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_high_rated_movies():
    """Test high rated movies query"""
    print("⭐ Testing High Rated Movies Query...")
    
    query = "query { searchMovies(minRating: 8.0) { id title year rating } }"
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["searchMovies"]:
            movies = data["data"]["searchMovies"]
            print(f"✅ Found {len(movies)} movies with rating 8.0+")
            print("Sample high-rated movies:")
            for i, movie in enumerate(movies[:5]):
                print(f"  {i+1}. {movie['title']} ({movie['year']}) - {movie['rating']}")
            return True
        else:
            print("❌ No high-rated movies found")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def main():
    print("🧪 Testing Specific Queries")
    print("=" * 40)
    
    # Test action movies
    action_ok = test_action_movies()
    print()
    
    # Test Christopher Nolan
    nolan_ok = test_christopher_nolan()
    print()
    
    # Test high rated movies
    high_rated_ok = test_high_rated_movies()
    print()
    
    print("📊 Test Results:")
    print(f"Action Movies: {'✅ Working' if action_ok else '❌ Failed'}")
    print(f"Christopher Nolan: {'✅ Working' if nolan_ok else '❌ Failed'}")
    print(f"High Rated Movies: {'✅ Working' if high_rated_ok else '❌ Failed'}")
    
    if action_ok and nolan_ok and high_rated_ok:
        print("\n🎉 All queries working! Your application should work perfectly now.")
        print("\n💡 Try these in the chat:")
        print("- 'Show me action movies'")
        print("- 'Find movies by Christopher Nolan'")
        print("- 'What are the highest rated movies?'")
    else:
        print("\n⚠️  Some queries failed. Check the GraphQL server.")

if __name__ == "__main__":
    main()
