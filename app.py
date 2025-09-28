from flask import Flask, request, jsonify
from flask_graphql import GraphQLView
from schema import schema
import json

app = Flask(__name__)

# Add GraphQL endpoint
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

# Enable CORS for frontend integration
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return """
    <h1>IMDB GraphQL API</h1>
    <p>Visit <a href="/graphql">/graphql</a> for the GraphQL interface</p>
    <h2>Available Queries:</h2>
    <ul>
        <li>movies - Get all movies</li>
        <li>movie(id: Int) - Get movie by ID</li>
        <li>searchMovies(title, genre, year, director) - Search movies</li>
    </ul>
    <h2>Available Mutations:</h2>
    <ul>
        <li>createMovie - Create a new movie</li>
        <li>updateMovie - Update an existing movie</li>
        <li>deleteMovie - Delete a movie</li>
    </ul>
    """

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "IMDB GraphQL API"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

