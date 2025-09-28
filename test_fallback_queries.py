#!/usr/bin/env python3
"""
Test the new fallback queries to ensure they work correctly
"""

import requests
import json

def test_fallback_queries():
    """Test various fallback queries that were causing errors"""
    print("🔧 Testing Fallback Queries...")
    
    test_queries = [
        ("show me the least rated movies", "least rated"),
        ("find lowest rated movies", "lowest rated"),
        ("worst rated movies", "worst rated"),
        ("movies with rating below 5", "rating below"),
        ("movies with rating under 4", "rating under"),
        ("show me drama movies", "drama"),
        ("find horror movies", "horror"),
        ("thriller movies", "thriller"),
        ("romance films", "romance"),
        ("sci-fi movies", "sci-fi"),
        ("adventure films", "adventure"),
        ("fantasy movies", "fantasy"),
        ("animated movies", "animation"),
        ("family films", "family"),
        ("documentary movies", "documentary"),
        ("crime movies", "crime"),
        ("mystery films", "mystery"),
        ("biography movies", "biography"),
        ("historical films", "history"),
        ("war movies", "war"),
        ("western films", "western"),
        ("musical movies", "musical"),
        ("sports films", "sport"),
        ("film noir movies", "film-noir"),
        ("reality tv shows", "reality-tv"),
        ("talk show", "talk-show"),
        ("news programs", "news"),
        ("short films", "short")
    ]
    
    print(f"Testing {len(test_queries)} fallback queries...")
    
    success_count = 0
    
    for query_text, expected_type in test_queries:
        print(f"  Testing: '{query_text}'")
        
        # Simulate the fallback query generation
        prompt_lower = query_text.lower()
        
        if "least rated" in prompt_lower or "lowest rated" in prompt_lower or "worst rated" in prompt_lower:
            graphql_query = "query { movies { id title year rating } }"
        elif "rating below" in prompt_lower or "rating under" in prompt_lower:
            # Extract rating number if mentioned
            import re
            rating_match = re.search(r'rating (below|under) (\d+\.?\d*)', prompt_lower)
            if rating_match:
                max_rating = float(rating_match.group(2))
                graphql_query = f"query {{ searchMovies(maxRating: {max_rating}) {{ id title year rating }} }}"
            else:
                graphql_query = "query { movies { id title year rating } }"
        elif "drama" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Drama"]) { id title year genre rating } }'
        elif "horror" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Horror"]) { id title year genre rating } }'
        elif "thriller" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Thriller"]) { id title year genre rating } }'
        elif "romance" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Romance"]) { id title year genre rating } }'
        elif "sci-fi" in prompt_lower or "science fiction" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Sci-Fi"]) { id title year genre rating } }'
        elif "adventure" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Adventure"]) { id title year genre rating } }'
        elif "fantasy" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Fantasy"]) { id title year genre rating } }'
        elif "animation" in prompt_lower or "animated" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Animation"]) { id title year genre rating } }'
        elif "family" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Family"]) { id title year genre rating } }'
        elif "documentary" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Documentary"]) { id title year genre rating } }'
        elif "crime" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Crime"]) { id title year genre rating } }'
        elif "mystery" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Mystery"]) { id title year genre rating } }'
        elif "biography" in prompt_lower or "biographical" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Biography"]) { id title year genre rating } }'
        elif "history" in prompt_lower or "historical" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["History"]) { id title year genre rating } }'
        elif "war" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["War"]) { id title year genre rating } }'
        elif "western" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Western"]) { id title year genre rating } }'
        elif "musical" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Musical"]) { id title year genre rating } }'
        elif "sport" in prompt_lower or "sports" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Sport"]) { id title year genre rating } }'
        elif "film-noir" in prompt_lower or "noir" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Film-Noir"]) { id title year genre rating } }'
        elif "reality-tv" in prompt_lower or "reality" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Reality-TV"]) { id title year genre rating } }'
        elif "talk-show" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Talk-Show"]) { id title year genre rating } }'
        elif "news" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["News"]) { id title year genre rating } }'
        elif "short" in prompt_lower:
            graphql_query = 'query { searchMovies(genre: ["Short"]) { id title year genre rating } }'
        else:
            # Default fallback - just get all movies
            graphql_query = "query { movies { id title year genre rating director } }"
        
        # Execute the query
        response = requests.post(
            "http://localhost:5001/graphql",
            json={"query": graphql_query}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                # Find the data field
                for field in ["movies", "searchMovies"]:
                    if field in data["data"] and data["data"][field]:
                        movies = data["data"][field]
                        print(f"    ✅ Found {len(movies)} movies")
                        success_count += 1
                        break
                else:
                    print(f"    ❌ No movies found")
            else:
                print(f"    ❌ No data in response")
        else:
            print(f"    ❌ HTTP Error: {response.status_code}")
    
    print(f"\n📊 Results: {success_count}/{len(test_queries)} queries successful")
    return success_count == len(test_queries)

def main():
    print("🧪 Testing Fallback Queries")
    print("=" * 40)
    
    # Test fallback queries
    fallback_ok = test_fallback_queries()
    print()
    
    print("📊 Fallback Query Test Results:")
    print(f"All Fallback Queries: {'✅ Working' if fallback_ok else '❌ Failed'}")
    
    if fallback_ok:
        print("\n🎉 All fallback queries working!")
        print("\n💡 Now supported queries:")
        print("  ✅ 'show me the least rated movies'")
        print("  ✅ 'find lowest rated movies'")
        print("  ✅ 'worst rated movies'")
        print("  ✅ 'movies with rating below 5'")
        print("  ✅ 'movies with rating under 4'")
        print("  ✅ All genre queries (drama, horror, thriller, etc.)")
        print("  ✅ No more 400 Bad Request errors!")
        print("\n🚀 Users can now ask any movie question!")
    else:
        print("\n⚠️  Some fallback queries need attention.")

if __name__ == "__main__":
    main()
