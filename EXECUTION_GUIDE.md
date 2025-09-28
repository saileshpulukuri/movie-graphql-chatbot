# CS5200 Programming Assignment 1 - Execution Guide

## 📋 Assignment Requirements Fulfilled

This application implements all required CRUD operations using GraphQL APIs with LLM integration:

### ✅ 5 Main Functions Implemented:
1. **Create Function**: Insert new movies with all required fields
2. **Update Function**: Update movie information and display results
3. **Delete Function**: Delete movie documents using title (as specified)
4. **Retrieve Function**: Retrieve movie documents by various criteria
5. **Search Function**: Advanced search with multiple filters

### ✅ Technologies Used:
- **Backend**: Python Flask + GraphQL (Graphene) - Apollo Server equivalent
- **Frontend**: Streamlit web interface
- **LLM Integration**: Ollama (open-source LLM) for natural language processing
- **Data Source**: Converted IMDB CSV to JSON format
- **API**: GraphQL with full CRUD operations

## 🚀 How to Execute the Application

### Prerequisites:
1. **Python 3.7+** installed
2. **Ollama** installed and running
3. **Internet connection** for initial setup

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd CS5200-Assignment

# Install Python packages
pip3 install -r requirements.txt
```

### Step 2: Setup Ollama (Open Source LLM)
```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the llama2 model
ollama pull llama2

# Start Ollama service (run this in a separate terminal)
ollama serve
```

### Step 3: Convert CSV Data (Already Done)
```bash
# The CSV has been converted to JSON format
python3 csv_to_json_converter.py
```

### Step 4: Start the GraphQL Backend
```bash
# Start the Flask GraphQL server
python3 app.py
```
**Access Point**: http://localhost:5000/graphql

### Step 5: Start the Frontend Interface
```bash
# In a new terminal, start Streamlit
streamlit run frontend.py
```
**Access Point**: http://localhost:8501

## 🎯 How to Use the Application

### Natural Language Chat Interface:
1. Open http://localhost:8501 in your browser
2. Type natural language queries in the chat box:
   - "Show me all movies"
   - "Find movies by Christopher Nolan"
   - "What are the highest rated movies?"
   - "Display action movies from 2008"
   - "Show me movies with rating above 8.0"

### Manual GraphQL Operations:
Use the sidebar for direct GraphQL queries:

**Example Queries:**
```graphql
# Get all movies
query {
  movies {
    id
    title
    year
    genre
    rating
    director
  }
}

# Search movies
query {
  searchMovies(year: 2008, minRating: 8.0) {
    title
    rating
    director
  }
}
```

**Example Mutations:**
```graphql
# Create a new movie
mutation {
  createMovie(movieData: {
    title: "New Movie"
    year: 2024
    genre: ["Action", "Drama"]
    description: "A great movie"
    director: "John Doe"
    actors: ["Actor1", "Actor2"]
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

# Delete movie by title (as required)
mutation {
  deleteMovie(title: "Movie Title") {
    success
    message
  }
}
```

## 🔧 LLM Integration Details

### Ollama Configuration:
- **Model Used**: llama2 (open-source)
- **Purpose**: Translate natural language to GraphQL queries
- **Integration**: Real-time processing of user queries
- **No Proprietary LLMs**: Only open-source Ollama used

### Natural Language Processing:
The LLM processes user input and generates appropriate GraphQL queries based on:
- Query intent (search, create, update, delete)
- Entity recognition (movies, directors, genres)
- Filter parameters (year, rating, etc.)

## 📊 Data Structure

The application works with 1000 movies from the IMDB dataset with fields:
- **id**: Unique identifier
- **title**: Movie title
- **year**: Release year
- **genre**: Array of genres
- **description**: Movie plot description
- **director**: Director name
- **actors**: Array of actor names
- **runtime**: Duration in minutes
- **rating**: IMDb rating
- **votes**: Number of votes
- **revenue**: Box office revenue in millions

## 🧪 Testing the Application

### Test Cases:
1. **Create**: Add a new movie through chat or manual mutation
2. **Read**: Query movies by various criteria
3. **Update**: Modify existing movie information
4. **Delete**: Remove movies by title
5. **Search**: Find movies with complex filters

### Quick Test Commands:
```bash
# Test GraphQL endpoint directly
curl -X POST http://localhost:5000/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "query { movies { title rating } }"}'
```

## 🐛 Troubleshooting

### Common Issues:
1. **Ollama not responding**: Ensure `ollama serve` is running
2. **Port conflicts**: Change ports in app.py (5000) or Streamlit (8501)
3. **Import errors**: Reinstall requirements.txt
4. **Data not loading**: Run csv_to_json_converter.py again

### Error Messages:
- "Error connecting to Ollama": Check if Ollama service is running
- "GraphQL endpoint not accessible": Ensure Flask app is running
- "Movie not found": Verify movie exists in database

## 📁 Project Files

```
CS5200-Assignment/
├── app.py                    # Flask GraphQL backend
├── models.py                 # Data models and CRUD operations
├── schema.py                 # GraphQL schema definition
├── frontend.py               # Streamlit web interface
├── csv_to_json_converter.py  # CSV to JSON conversion utility
├── imdb.json                # Movie database (1000 movies)
├── IMDB-Movie-Data.csv      # Original CSV data
├── requirements.txt          # Python dependencies
├── setup.sh                 # Automated setup script
├── README.md                # Project documentation
└── EXECUTION_GUIDE.md       # This execution guide
```

## ✅ Assignment Compliance

This application fully satisfies all assignment requirements:
- ✅ GraphQL APIs with CRUD operations
- ✅ Backend using Python Flask (Apollo Server equivalent)
- ✅ Frontend web interface using Streamlit
- ✅ Open-source LLM integration (Ollama)
- ✅ Natural language to GraphQL translation
- ✅ JSON file data storage
- ✅ All 5 required functions implemented
- ✅ Delete by title functionality
- ✅ Real-time query execution and display

## 🎓 LLM Usage Declaration

**LLMs Used in Development:**
- **Claude AI (Anthropic)**: Used for code generation, debugging, and project structuring
- **Ollama (llama2)**: Integrated into the application for natural language processing

This assignment demonstrates the effective use of LLMs in developing a complete full-stack application with advanced natural language processing capabilities.

