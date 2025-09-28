import csv
import json
import os

def convert_csv_to_json(csv_file='IMDB-Movie-Data.csv', json_file='imdb.json'):
    """
    Convert CSV file to JSON format matching our GraphQL schema
    """
    movies = []
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                # Clean and process the data
                movie = {
                    'id': int(row['Ids']) if row['Ids'] else None,
                    'title': row['Title'].strip() if row['Title'] else '',
                    'genre': [genre.strip() for genre in row['Genre'].split(',')] if row['Genre'] else [],
                    'description': row['Description'].strip() if row['Description'] else '',
                    'director': row['Director'].strip() if row['Director'] else '',
                    'actors': [actor.strip() for actor in row['Actors'].split(',')] if row['Actors'] else [],
                    'year': int(row['Year']) if row['Year'] else None,
                    'runtime': int(row['Runtime']) if row['Runtime'] else None,
                    'rating': float(row['Rating']) if row['Rating'] else 0.0,
                    'votes': int(row['Votes']) if row['Votes'] else 0,
                    'revenue': float(row['Revenue']) if row['Revenue'] else 0.0
                }
                
                # Only add movies with valid IDs
                if movie['id'] is not None:
                    movies.append(movie)
        
        # Sort by ID to maintain consistency
        movies.sort(key=lambda x: x['id'])
        
        # Save to JSON file
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(movies, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully converted {len(movies)} movies from {csv_file} to {json_file}")
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: {csv_file} not found")
        return False
    except Exception as e:
        print(f"❌ Error converting CSV to JSON: {str(e)}")
        return False

def get_movie_statistics():
    """
    Get basic statistics about the movie database
    """
    try:
        with open('imdb.json', 'r', encoding='utf-8') as file:
            movies = json.load(file)
        
        if not movies:
            return {"total_movies": 0}
        
        # Calculate statistics
        ratings = [movie['rating'] for movie in movies if movie['rating'] > 0]
        years = [movie['year'] for movie in movies if movie['year']]
        revenues = [movie['revenue'] for movie in movies if movie['revenue'] > 0]
        
        stats = {
            "total_movies": len(movies),
            "average_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
            "highest_rated": max(movies, key=lambda x: x['rating'])['title'] if movies else None,
            "year_range": f"{min(years)} - {max(years)}" if years else "N/A",
            "total_revenue": round(sum(revenues), 2) if revenues else 0,
            "genres": len(set(genre for movie in movies for genre in movie['genre']))
        }
        
        return stats
        
    except Exception as e:
        print(f"Error getting statistics: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    print("🎬 Converting IMDB CSV to JSON...")
    success = convert_csv_to_json()
    
    if success:
        print("\n📊 Movie Database Statistics:")
        stats = get_movie_statistics()
        for key, value in stats.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

