import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GRAPHQL_ENDPOINT = "http://localhost:5001/graphql"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

class GraphQLClient:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def execute_query(self, query, variables=None):
        """Execute a GraphQL query"""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        try:
            response = requests.post(self.endpoint, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"errors": [{"message": f"Request failed: {str(e)}"}]}

class OllamaClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def generate_response(self, prompt, model="llama2"):
        """Generate response using Ollama"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False}
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"

def main():
    st.set_page_config(
        page_title="IMDB GraphQL Chatbot",
        page_icon="🎬",
        layout="wide"
    )
    
    st.title("🎬 IMDB GraphQL Chatbot")
    st.markdown("**Ask questions about movies in natural language!**")
    
    # Initialize clients
    graphql_client = GraphQLClient(GRAPHQL_ENDPOINT)
    ollama_client = OllamaClient(OLLAMA_URL)
    
    # Sidebar for manual GraphQL operations
    with st.sidebar:
        st.header("🔧 Manual GraphQL Operations")
        
        operation = st.selectbox(
            "Choose Operation",
            ["Query", "Mutation"]
        )
        
        if operation == "Query":
            st.subheader("Available Queries:")
            st.markdown("""
            - `movies` - Get all movies
            - `movie(id: 1)` - Get movie by ID
            - `movieByTitle(title: "The Dark Knight")` - Get movie by title
            - `searchMovies(title: "Dark", year: 2008)` - Search movies
            """)
            
            query_text = st.text_area("Enter GraphQL Query:", height=100)
            
            if st.button("Execute Query"):
                if query_text.strip():
                    result = graphql_client.execute_query(query_text)
                    st.json(result)
        
        elif operation == "Mutation":
            st.subheader("Available Mutations:")
            st.markdown("""
            - `createMovie` - Create new movie
            - `updateMovie` - Update existing movie  
            - `deleteMovie` - Delete movie (by ID or title)
            """)
            
            mutation_text = st.text_area("Enter GraphQL Mutation:", height=100)
            
            if st.button("Execute Mutation"):
                if mutation_text.strip():
                    result = graphql_client.execute_query(mutation_text)
                    st.json(result)
    
    # Initialize session state for pagination
    if "all_movies" not in st.session_state:
        st.session_state.all_movies = []
    if "movies_to_show" not in st.session_state:
        st.session_state.movies_to_show = 20
    if "action_movies" not in st.session_state:
        st.session_state.action_movies = []
    if "action_movies_to_show" not in st.session_state:
        st.session_state.action_movies_to_show = 20

    # Quick action buttons at the top
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show All Movies"):
            query = "query { movies { id title year genre description director actors runtime rating votes revenue } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                st.session_state.all_movies = result["data"]["movies"]
                st.session_state.movies_to_show = 20
                st.success(f"✅ Loaded {len(st.session_state.all_movies)} movies!")
            else:
                st.error("No movies found or error occurred")
    
    with col2:
        if st.button("🔍 Top Rated Movies"):
            query = "query { movies { id title year rating } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = sorted(result["data"]["movies"], key=lambda x: x["rating"], reverse=True)[:5]
                st.write("**🏆 Top 5 Rated Movies:**")
                for i, movie in enumerate(movies):
                    st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
            else:
                st.error("No movies found")
    
    with col3:
        if st.button("🎭 Action Movies"):
            query = 'query { searchMovies(genre: ["Action"]) { id title year genre rating } }'
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"].get("searchMovies"):
                st.session_state.action_movies = result["data"]["searchMovies"]
                st.session_state.action_movies_to_show = 20
                st.success(f"✅ Found {len(st.session_state.action_movies)} action movies!")
            else:
                st.error("No action movies found")
    
    with col4:
        if st.button("📊 Movie Statistics"):
            query = "query { movies { id year rating revenue } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = result["data"]["movies"]
                avg_rating = sum(movie["rating"] for movie in movies) / len(movies)
                years = [movie["year"] for movie in movies]
                total_revenue = sum(movie["revenue"] for movie in movies if movie["revenue"])
                st.write(f"📊 **Database Statistics:**")
                st.write(f"🎬 **Total Movies:** {len(movies)}")
                st.write(f"⭐ **Average Rating:** {avg_rating:.2f}")
                st.write(f"📅 **Year Range:** {min(years)} - {max(years)}")
                st.write(f"💰 **Total Revenue:** ${total_revenue:.2f}M")
            else:
                st.error("No data available")

    # Display all movies with pagination
    if st.session_state.all_movies:
        st.subheader("🎬 All Movies")
        movies_to_display = st.session_state.all_movies[:st.session_state.movies_to_show]
        
        for i, movie in enumerate(movies_to_display):
            st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
        
        if len(st.session_state.all_movies) > st.session_state.movies_to_show:
            remaining = len(st.session_state.all_movies) - st.session_state.movies_to_show
            if st.button(f"📥 Show More ({remaining} remaining)", key="show_more_all"):
                st.session_state.movies_to_show += 20
                st.rerun()

    # Display action movies with pagination
    if st.session_state.action_movies:
        st.subheader("🎭 Action Movies")
        action_movies_to_display = st.session_state.action_movies[:st.session_state.action_movies_to_show]
        
        st.write(f"**Found {len(st.session_state.action_movies)} action movies:**")
        for i, movie in enumerate(action_movies_to_display):
            st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
        
        if len(st.session_state.action_movies) > st.session_state.action_movies_to_show:
            remaining = len(st.session_state.action_movies) - st.session_state.action_movies_to_show
            if st.button(f"📥 Show More Action Movies ({remaining} remaining)", key="show_more_action"):
                st.session_state.action_movies_to_show += 20
                st.rerun()

    # Main chat interface
    st.header("💬 Chat with IMDB Database")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle example query
    if hasattr(st.session_state, 'example_query'):
        prompt = st.session_state.example_query
        delattr(st.session_state, 'example_query')
    else:
        prompt = st.chat_input("Ask about movies (e.g., 'Show me all movies', 'Find movies by Christopher Nolan')")
    
    if prompt:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Create a prompt for Ollama to translate natural language to GraphQL
                system_prompt = f"""
You are a helpful assistant that translates natural language queries about movies into GraphQL queries.

Available operations:
1. Get all movies: query {{ movies {{ id title year genre description director actors runtime rating votes revenue }} }}
2. Get movie by ID: query {{ movie(id: 1) {{ id title year genre description director actors runtime rating votes revenue }} }}
3. Get movie by title: query {{ movieByTitle(title: "Movie Title") {{ id title year genre description director actors runtime rating votes revenue }} }}
4. Search movies: query {{ searchMovies(title: "keyword", year: 2008, director: "Director Name", minRating: 7.0) {{ id title year genre description director actors runtime rating votes revenue }} }}

Common query patterns:
- "Show me all movies" → query {{ movies {{ id title year genre rating director }} }}
- "Find movies by Christopher Nolan" → query {{ searchMovies(director: "Christopher Nolan") {{ id title year genre rating director }} }}
- "What are the highest rated movies?" → query {{ movies {{ id title year rating }} }}
- "Show me action movies" → query {{ searchMovies(genre: ["Action"]) {{ id title year genre rating }} }}
- "Movies from 2008" → query {{ searchMovies(year: 2008) {{ id title year rating }} }}
- "Movies with rating above 8" → query {{ searchMovies(minRating: 8.0) {{ id title year rating }} }}

The user asked: "{prompt}"

Generate ONLY the GraphQL query. No explanations, no markdown, just the query.
"""
                
                # Get GraphQL query from Ollama
                graphql_query = ollama_client.generate_response(system_prompt)
                
                # Clean up the query (remove any extra text)
                if "query" in graphql_query:
                    # Extract just the query part
                    start = graphql_query.find("query")
                    end = graphql_query.rfind("}") + 1
                    graphql_query = graphql_query[start:end]
                
                # Fallback queries for common requests
                prompt_lower = prompt.lower()
                if "all movies" in prompt_lower or "show me movies" in prompt_lower:
                    graphql_query = "query { movies { id title year genre rating director } }"
                elif "christopher nolan" in prompt_lower or "nolan" in prompt_lower:
                    graphql_query = 'query { searchMovies(director: "Christopher Nolan") { id title year genre rating director } }'
                elif "highest rated" in prompt_lower or "top rated" in prompt_lower:
                    graphql_query = "query { movies { id title year rating } }"
                elif "action" in prompt_lower:
                    graphql_query = 'query { searchMovies(genre: ["Action"]) { id title year genre rating } }'
                elif "2008" in prompt_lower:
                    graphql_query = "query { searchMovies(year: 2008) { id title year rating } }"
                elif "rating above 8" in prompt_lower or "rating above 8.0" in prompt_lower:
                    graphql_query = "query { searchMovies(minRating: 8.0) { id title year rating } }"
                elif "steven spielberg" in prompt_lower or "spielberg" in prompt_lower:
                    graphql_query = 'query { searchMovies(director: "Steven Spielberg") { id title year genre rating director } }'
                elif "comedy" in prompt_lower:
                    graphql_query = 'query { searchMovies(genre: ["Comedy"]) { id title year genre rating } }'
                elif "statistics" in prompt_lower or "stats" in prompt_lower:
                    graphql_query = "query { movies { id year rating revenue } }"
                
                # Execute the GraphQL query
                result = graphql_client.execute_query(graphql_query)
                
                # Format the response in natural language
                if "errors" in result:
                    response_text = f"❌ **Sorry, I encountered an error:** {result['errors'][0]['message']}"
                else:
                    data = result.get("data", {})
                    if not data or all(not v for v in data.values()):
                        response_text = f"🤔 **I couldn't find any movies matching your request.**\n\nTry asking something like:\n- 'Show me all movies'\n- 'Find movies by Christopher Nolan'\n- 'What are the highest rated movies?'"
                    else:
                        # Format response in natural language
                        response_text = ""
                        
                        # Handle different query types
                        if "movies" in data and data["movies"]:
                            movies = data["movies"]
                            if len(movies) > 0:
                                response_text = f"🎬 **I found {len(movies)} movies for you!**\n\n"
                                for i, movie in enumerate(movies[:10]):  # Show first 10
                                    response_text += f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}\n"
                                if len(movies) > 10:
                                    response_text += f"\n... and {len(movies) - 10} more movies!"
                        
                        elif "movie" in data and data["movie"]:
                            movie = data["movie"]
                            response_text = f"🎬 **{movie['title']}** ({movie['year']})\n"
                            response_text += f"⭐ Rating: {movie['rating']} | 🎭 Genre: {', '.join(movie['genre'])}\n"
                            response_text += f"🎬 Director: {movie['director']}\n"
                            response_text += f"📖 {movie['description']}"
                        
                        elif "searchMovies" in data and data["searchMovies"]:
                            movies = data["searchMovies"]
                            response_text = f"🔍 **I found {len(movies)} movies matching your search:**\n\n"
                            for i, movie in enumerate(movies[:10]):
                                response_text += f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}\n"
                            if len(movies) > 10:
                                response_text += f"\n... and {len(movies) - 10} more movies!"
                        
                        else:
                            response_text = "🤔 I found some data, but I'm not sure how to display it properly."
                
                st.markdown(response_text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Initialize session state for pagination
    if "all_movies" not in st.session_state:
        st.session_state.all_movies = []
    if "movies_to_show" not in st.session_state:
        st.session_state.movies_to_show = 20
    if "action_movies" not in st.session_state:
        st.session_state.action_movies = []
    if "action_movies_to_show" not in st.session_state:
        st.session_state.action_movies_to_show = 20

    # Quick action buttons
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show All Movies"):
            query = "query { movies { id title year genre description director actors runtime rating votes revenue } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                st.session_state.all_movies = result["data"]["movies"]
                st.session_state.movies_to_show = 20
                st.success(f"✅ Loaded {len(st.session_state.all_movies)} movies!")
            else:
                st.error("No movies found or error occurred")
    
    with col2:
        if st.button("🔍 Top Rated Movies"):
            query = "query { movies { id title year rating } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = sorted(result["data"]["movies"], key=lambda x: x["rating"], reverse=True)[:5]
                st.write("**🏆 Top 5 Rated Movies:**")
                for i, movie in enumerate(movies):
                    st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
            else:
                st.error("No movies found")
    
    with col3:
        if st.button("🎭 Action Movies"):
            query = 'query { searchMovies(genre: ["Action"]) { id title year genre rating } }'
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"].get("searchMovies"):
                st.session_state.action_movies = result["data"]["searchMovies"]
                st.session_state.action_movies_to_show = 20
                st.success(f"✅ Found {len(st.session_state.action_movies)} action movies!")
            else:
                st.error("No action movies found")
    
    with col4:
        if st.button("📊 Movie Statistics"):
            query = "query { movies { id year rating revenue } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = result["data"]["movies"]
                avg_rating = sum(movie["rating"] for movie in movies) / len(movies)
                years = [movie["year"] for movie in movies]
                total_revenue = sum(movie["revenue"] for movie in movies if movie["revenue"])
                st.write(f"📊 **Database Statistics:**")
                st.write(f"🎬 **Total Movies:** {len(movies)}")
                st.write(f"⭐ **Average Rating:** {avg_rating:.2f}")
                st.write(f"📅 **Year Range:** {min(years)} - {max(years)}")
                st.write(f"💰 **Total Revenue:** ${total_revenue:.2f}M")
            else:
                st.error("No data available")

    # Display all movies with pagination
    if st.session_state.all_movies:
        st.subheader("🎬 All Movies")
        movies_to_display = st.session_state.all_movies[:st.session_state.movies_to_show]
        
        for i, movie in enumerate(movies_to_display):
            st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
        
        if len(st.session_state.all_movies) > st.session_state.movies_to_show:
            remaining = len(st.session_state.all_movies) - st.session_state.movies_to_show
            if st.button(f"📥 Show More ({remaining} remaining)", key="show_more_all"):
                st.session_state.movies_to_show += 20
                st.rerun()

    # Display action movies with pagination
    if st.session_state.action_movies:
        st.subheader("🎭 Action Movies")
        action_movies_to_display = st.session_state.action_movies[:st.session_state.action_movies_to_show]
        
        st.write(f"**Found {len(st.session_state.action_movies)} action movies:**")
        for i, movie in enumerate(action_movies_to_display):
            st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - ⭐ {movie['rating']}")
        
        if len(st.session_state.action_movies) > st.session_state.action_movies_to_show:
            remaining = len(st.session_state.action_movies) - st.session_state.action_movies_to_show
            if st.button(f"📥 Show More Action Movies ({remaining} remaining)", key="show_more_action"):
                st.session_state.action_movies_to_show += 20
                st.rerun()

if __name__ == "__main__":
    main()
