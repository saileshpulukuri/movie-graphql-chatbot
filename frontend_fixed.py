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
    
    # Main chat interface
    st.header("💬 Chat with IMDB Database")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about movies (e.g., 'Show me all movies', 'Find movies by Christopher Nolan')"):
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

Available operations and fields:
1. Get all movies: query {{ movies {{ id title year genre description director actors runtime rating votes revenue }} }}
2. Get movie by ID: query {{ movie(id: 1) {{ id title year genre description director actors runtime rating votes revenue }} }}
3. Get movie by title: query {{ movieByTitle(title: "Movie Title") {{ id title year genre description director actors runtime rating votes revenue }} }}
4. Search movies: query {{ searchMovies(title: "keyword", year: 2008, director: "Director Name", minRating: 7.0) {{ id title year genre description director actors runtime rating votes revenue }} }}

Available fields: id, title, year, genre, description, director, actors, runtime, rating, votes, revenue

The user asked: "{prompt}"

Please provide ONLY the GraphQL query that answers their question. Do not include any explanations or markdown formatting.
"""
                
                # Get GraphQL query from Ollama
                graphql_query = ollama_client.generate_response(system_prompt)
                
                # Execute the GraphQL query
                result = graphql_client.execute_query(graphql_query)
                
                # Format the response
                if "errors" in result:
                    response_text = f"❌ **Error executing query:**\n```\n{graphql_query}\n```\n\n**Error:** {result['errors'][0]['message']}"
                else:
                    response_text = f"✅ **Query executed successfully:**\n```graphql\n{graphql_query}\n```\n\n**Result:**\n```json\n{json.dumps(result['data'], indent=2)}\n```"
                
                st.markdown(response_text)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    # Quick action buttons
    st.subheader("🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📋 Show All Movies"):
            query = "query { movies { id title year genre description director actors runtime rating votes revenue } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = result["data"]["movies"]
                st.write(f"**Found {len(movies)} movies:**")
                for i, movie in enumerate(movies[:10]):  # Show first 10
                    st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - Rating: {movie['rating']}")
                if len(movies) > 10:
                    st.write(f"... and {len(movies) - 10} more movies")
            else:
                st.error("No movies found or error occurred")
    
    with col2:
        if st.button("🔍 Top Rated Movies"):
            query = "query { movies { id title year rating } }"
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"]["movies"]:
                movies = sorted(result["data"]["movies"], key=lambda x: x["rating"], reverse=True)[:5]
                st.write("**Top 5 Rated Movies:**")
                for movie in movies:
                    st.write(f"**{movie['title']}** ({movie['year']}) - Rating: {movie['rating']}")
            else:
                st.error("No movies found")
    
    with col3:
        if st.button("🎭 Action Movies"):
            query = 'query { searchMovies(genre: ["Action"]) { id title year genre rating } }'
            result = graphql_client.execute_query(query)
            if "data" in result and result["data"].get("searchMovies"):
                movies = result["data"]["searchMovies"]
                st.write(f"**Found {len(movies)} Action Movies:**")
                for i, movie in enumerate(movies[:10]):  # Show first 10
                    st.write(f"{i+1}. **{movie['title']}** ({movie['year']}) - Rating: {movie['rating']}")
                if len(movies) > 10:
                    st.write(f"... and {len(movies) - 10} more action movies")
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
                st.write(f"**Total Movies:** {len(movies)}")
                st.write(f"**Average Rating:** {avg_rating:.2f}")
                st.write(f"**Year Range:** {min(years)} - {max(years)}")
                st.write(f"**Total Revenue:** ${total_revenue:.2f}M")
            else:
                st.error("No data available")

if __name__ == "__main__":
    main()
