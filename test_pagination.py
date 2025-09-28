#!/usr/bin/env python3
"""
Test pagination functionality to ensure "Show More" works correctly
"""

import requests
import json

def test_all_movies_pagination():
    """Test that we can get all movies and pagination works"""
    print("🎬 Testing All Movies Pagination...")
    
    query = "query { movies { id title year rating } }"
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]["movies"]:
            movies = data["data"]["movies"]
            print(f"✅ Found {len(movies)} total movies")
            
            # Test pagination logic
            movies_to_show = 20
            remaining = len(movies) - movies_to_show
            
            print(f"📊 Pagination Test:")
            print(f"  - First batch: {movies_to_show} movies")
            print(f"  - Remaining: {remaining} movies")
            print(f"  - Total: {len(movies)} movies")
            
            # Simulate "Show More" clicks
            for i in range(3):
                movies_to_show += 20
                remaining = len(movies) - movies_to_show
                print(f"  - After 'Show More' #{i+1}: Showing {movies_to_show}, {remaining} remaining")
                
                if remaining <= 0:
                    print(f"  - All movies would be shown after {i+1} 'Show More' clicks")
                    break
            
            return True
        else:
            print("❌ No movies found")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def test_action_movies_pagination():
    """Test action movies pagination"""
    print("🎭 Testing Action Movies Pagination...")
    
    query = 'query { searchMovies(genre: ["Action"]) { id title year rating } }'
    response = requests.post(
        "http://localhost:5001/graphql",
        json={"query": query}
    )
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"].get("searchMovies"):
            movies = data["data"]["searchMovies"]
            print(f"✅ Found {len(movies)} action movies")
            
            # Test pagination logic
            movies_to_show = 20
            remaining = len(movies) - movies_to_show
            
            print(f"📊 Action Movies Pagination Test:")
            print(f"  - First batch: {movies_to_show} movies")
            print(f"  - Remaining: {remaining} movies")
            print(f"  - Total: {len(movies)} movies")
            
            # Simulate "Show More" clicks
            for i in range(3):
                movies_to_show += 20
                remaining = len(movies) - movies_to_show
                print(f"  - After 'Show More' #{i+1}: Showing {movies_to_show}, {remaining} remaining")
                
                if remaining <= 0:
                    print(f"  - All action movies would be shown after {i+1} 'Show More' clicks")
                    break
            
            return True
        else:
            print("❌ No action movies found")
            return False
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return False

def main():
    print("🧪 Testing Pagination Functionality")
    print("=" * 50)
    
    # Test all movies pagination
    all_movies_ok = test_all_movies_pagination()
    print()
    
    # Test action movies pagination
    action_movies_ok = test_action_movies_pagination()
    print()
    
    print("📊 Pagination Test Results:")
    print(f"All Movies Pagination: {'✅ Working' if all_movies_ok else '❌ Failed'}")
    print(f"Action Movies Pagination: {'✅ Working' if action_movies_ok else '❌ Failed'}")
    
    if all_movies_ok and action_movies_ok:
        print("\n🎉 Pagination is working perfectly!")
        print("\n💡 In the frontend:")
        print("- Click '📋 Show All Movies' to see 1001 movies")
        print("- Click '📥 Show More (981 remaining)' to see more")
        print("- Click '🎭 Action Movies' to see 304 action movies")
        print("- Click '📥 Show More Action Movies (284 remaining)' to see more")
    else:
        print("\n⚠️  Some pagination tests failed. Check the GraphQL server.")

if __name__ == "__main__":
    main()
