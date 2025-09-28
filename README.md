# IMDB GraphQL CRUD Application with LLM Integration

This project implements a complete CRUD (Create, Read, Update, Delete) application using GraphQL APIs with natural language processing through Large Language Models (LLMs).

## 🏗️ Architecture

- **Backend**: Flask + GraphQL (Graphene) for API endpoints
- **Frontend**: Streamlit for user interface
- **LLM Integration**: Ollama (open-source LLM) for natural language to GraphQL translation
- **Data Storage**: JSON file (imdb.json) for movie data

## 🚀 Features

### GraphQL CRUD Operations
- **Create**: Add new movies to the database
- **Read**: Query movies with various filters
- **Update**: Modify existing movie information
- **Delete**: Remove movies from the database

### Natural Language Interface
- Chat-based interface for querying movies
- Automatic translation of natural language to GraphQL queries
- Support for complex queries like "Show me all action movies from 2008"

### Manual GraphQL Operations
- Direct GraphQL query/mutation interface
- Real-time query execution
- Error handling and validation

## 📋 Prerequisites

1. **Python 3.7+**
2. **Ollama** - Install from [https://ollama.ai](https://ollama.ai)
3. **Required Python packages** (install via requirements.txt)

## 🛠️ Installation & Setup

1. **Clone/Download the project files**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama:**
   ```bash
   # Install Ollama (macOS)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull a model (e.g., llama2)
   ollama pull llama2
   
   # Start Ollama service
   ollama serve
   ```

4. **Verify setup:**
   - Ollama should be running on `http://localhost:11434`
   - Check that `imdb.json` contains sample movie data

## 🎬 Usage

### 1. Start the GraphQL Backend
```bash
python app.py
```
The GraphQL API will be available at `http://localhost:5000/graphql`

### 2. Start the Frontend Interface
```bash
streamlit run frontend.py
```
The web interface will open in your browser at `http://localhost:8501`

### 3. Using the Application

#### Chat Interface
- Type natural language queries like:
  - "Show me all movies"
  - "Find movies by Christopher Nolan"
  - "What are the top-rated action movies?"
  - "Display movies from 1994"

#### Manual GraphQL Operations
Use the sidebar to execute direct GraphQL queries:

**Query Examples:**
```graphql
# Get all movies
query {
  movies {
    id
    title
    year
    rating
  }
}

# Search movies by title
query {
  searchMovies(title: "Dark") {
    id
    title
    year
    genre
    rating
  }
}

# Get movie by ID
query {
  movie(id: 1) {
    title
    director
    actors
    plot
  }
}
```

**Mutation Examples:**
```graphql
# Create a new movie
mutation {
  createMovie(movieData: {
    title: "Inception"
    year: 2010
    genre: ["Action", "Sci-Fi"]
    rating: 8.8
    director: "Christopher Nolan"
    actors: ["Leonardo DiCaprio", "Marion Cotillard"]
    plot: "A thief who steals corporate secrets..."
  }) {
    success
    message
    movie {
      id
      title
    }
  }
}

# Update a movie
mutation {
  updateMovie(id: 1, movieData: {
    rating: 9.5
  }) {
    success
    message
    movie {
      id
      title
      rating
    }
  }
}

# Delete a movie
mutation {
  deleteMovie(id: 5) {
    success
    message
    movie {
      id
      title
    }
  }
}
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file (optional):
```
OLLAMA_URL=http://localhost:11434
```

### Customizing Ollama Model
In `frontend.py`, change the model parameter:
```python
ollama_client.generate_response(prompt, model="your-preferred-model")
```

## 📁 Project Structure

```
CS5200-Assignment/
├── app.py              # Flask GraphQL backend
├── models.py           # Data models and management
├── schema.py           # GraphQL schema definition
├── frontend.py         # Streamlit frontend interface
├── imdb.json          # Movie database (JSON)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🧪 Testing

### Test the GraphQL API directly:
Visit `http://localhost:5000/graphql` in your browser to access the GraphQL playground.

### Test the Frontend:
1. Start both backend and frontend
2. Try natural language queries in the chat
3. Use manual GraphQL operations in the sidebar
4. Test the quick action buttons

## 🐛 Troubleshooting

### Common Issues:

1. **Ollama connection error:**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is installed: `ollama list`
   - Verify the URL in the frontend matches your Ollama setup

2. **GraphQL endpoint not accessible:**
   - Ensure Flask app is running on port 5000
   - Check for port conflicts
   - Verify CORS settings in app.py

3. **Import errors:**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility

## 🔮 Future Enhancements

- Add user authentication
- Implement real-time notifications
- Add more sophisticated search capabilities
- Support for batch operations
- Add data validation and sanitization
- Implement caching for better performance
- Add unit and integration tests

## 📝 Technologies Used

- **Backend**: Flask, Graphene (GraphQL), Python
- **Frontend**: Streamlit, HTML/CSS
- **LLM**: Ollama (open-source)
- **Data**: JSON file storage
- **HTTP Client**: Requests library
- **Environment**: Python-dotenv



