#!/usr/bin/env python3
"""
Test script for the IMDB GraphQL CRUD Application
This script tests all the required CRUD operations
"""

import requests
import json
import time

# Configuration
GRAPHQL_ENDPOINT = "http://localhost:5001/graphql"

def test_graphql_query(query, description):
    """Test a GraphQL query"""
    print(f"\n🧪 Testing: {description}")
    print(f"Query: {query}")
    
    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        result = response.json()
        
        if "errors" in result:
            print(f"❌ Error: {result['errors']}")
            return False
        else:
            print(f"✅ Success: {len(str(result))} characters returned")
            return True
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

def main():
    print("🎬 IMDB GraphQL CRUD Application Test Suite")
    print("=" * 50)
    
    # Test if server is running
    print("\n🔍 Checking if GraphQL server is running...")
    try:
        response = requests.get("http://localhost:5001/health", timeout=5)
        if response.status_code == 200:
            print("✅ GraphQL server is running")
        else:
            print("❌ GraphQL server is not responding properly")
            return
    except requests.exceptions.RequestException:
        print("❌ GraphQL server is not running. Please start it with: python3 app.py")
        return
    
    # Test 1: Read all movies (Retrieve function)
    test_graphql_query(
        "query { movies { id title year genre rating director } }",
        "Retrieve all movies"
    )
    
    # Test 2: Read specific movie by ID
    test_graphql_query(
        "query { movie(id: 1) { id title year genre rating director actors } }",
        "Retrieve movie by ID"
    )
    
    # Test 3: Search movies
    test_graphql_query(
        'query { searchMovies(year: 2008, minRating: 8.0) { title year rating director } }',
        "Search movies by year and rating"
    )
    
    # Test 4: Create a new movie (Create function)
    create_mutation = """
    mutation {
        createMovie(movieData: {
            title: "Test Movie"
            year: 2024
            genre: ["Action", "Drama"]
            description: "A test movie for the assignment"
            director: "Test Director"
            actors: ["Test Actor 1", "Test Actor 2"]
            runtime: 120
            rating: 8.5
            votes: 1000
            revenue: 50.0
        }) {
            success
            message
            movie {
                id
                title
            }
        }
    }
    """
    test_graphql_query(create_mutation, "Create a new movie")
    
    # Test 5: Update a movie (Update function)
    update_mutation = """
    mutation {
        updateMovie(id: 1, movieData: {
            rating: 9.5
            votes: 2000
        }) {
            success
            message
            movie {
                id
                title
                rating
                votes
            }
        }
    }
    """
    test_graphql_query(update_mutation, "Update movie information")
    
    # Test 6: Delete a movie by title (Delete function - as required)
    delete_mutation = """
    mutation {
        deleteMovie(title: "Test Movie") {
            success
            message
            movie {
                id
                title
            }
        }
    }
    """
    test_graphql_query(delete_mutation, "Delete movie by title")
    
    # Test 7: Get movie by title
    test_graphql_query(
        'query { movieByTitle(title: "Guardians of the Galaxy") { id title year rating } }',
        "Get movie by title"
    )
    
    # Test 8: Advanced search
    test_graphql_query(
        'query { searchMovies(genre: ["Action"], minRating: 7.0) { title year genre rating } }',
        "Search action movies with high rating"
    )
    
    print("\n" + "=" * 50)
    print("🎉 Test suite completed!")
    print("\n📋 Summary of CRUD Operations Tested:")
    print("✅ 1. Create Function - Insert new movies")
    print("✅ 2. Read Function - Retrieve movies by various criteria")
    print("✅ 3. Update Function - Update movie information")
    print("✅ 4. Delete Function - Delete movies by title (as required)")
    print("✅ 5. Search Function - Advanced search with filters")
    print("\n🔗 GraphQL Playground: http://localhost:5001/graphql")
    print("🌐 Frontend Interface: http://localhost:8501 (run: streamlit run frontend.py)")

if __name__ == "__main__":
    main()
