# from graphene import ObjectType, String, Int, Float, List, Field, InputObjectType
# import json
# import os

# class Movie(ObjectType):
#     id = Int()
#     title = String()
#     year = Int()
#     genre = List(String)
#     description = String()
#     director = String()
#     actors = List(String)
#     runtime = Int()
#     rating = Float()
#     votes = Int()
#     revenue = Float()

# class MovieInput(InputObjectType):
#     title = String(required=True)
#     year = Int(required=True)
#     genre = List(String, required=True)
#     description = String(required=True)
#     director = String(required=True)
#     actors = List(String, required=True)
#     runtime = Int(required=True)
#     rating = Float(required=True)
#     votes = Int(required=True)
#     revenue = Float(required=True)

# class MovieUpdateInput(InputObjectType):
#     title = String()
#     year = Int()
#     genre = List(String)
#     description = String()
#     director = String()
#     actors = List(String)
#     runtime = Int()
#     rating = Float()
#     votes = Int()
#     revenue = Float()

# class DataManager:
#     def __init__(self, json_file='imdb.json'):
#         self.json_file = json_file
#         self.data = self.load_data()
    
#     def load_data(self):
#         """Load data from JSON file and normalize genres into lists"""
#         try:
#             with open(self.json_file, 'r') as f:
#                 data = json.load(f)

#             for movie in data:
#                 g = movie.get("genre")
#                 if isinstance(g, str):
#                     movie["genre"] = [x.strip() for x in g.split(",") if x.strip()]
#                 elif g is None:
#                     movie["genre"] = []

#                 a = movie.get("actors")
#                 if isinstance(a, str):
#                     movie["actors"] = [x.strip() for x in a.split(",") if x.strip()]
#                 elif a is None:
#                     movie["actors"] = []
#             return data

#         except FileNotFoundError:
#             return []
#         except json.JSONDecodeError:
#             return []

#     def save_data(self):
#         """Save data to JSON file"""
#         with open(self.json_file, 'w') as f:
#             json.dump(self.data, f, indent=2)
    
#     def get_next_id(self):
#         """Get the next available ID"""
#         if not self.data:
#             return 1
#         return max(movie['id'] for movie in self.data) + 1
    
#     def get_all_movies(self):
#         """Get all movies"""
#         print("DEBUG total movies:", len(self.data))  # helpful for debugging
#         return self.data
    
#     def get_movie_by_id(self, movie_id):
#         """Get movie by ID"""
#         for movie in self.data:
#             if movie['id'] == movie_id:
#                 return movie
#         return None
    
#     def get_movie_by_title(self, title):
#         """Get movie by title"""
#         for movie in self.data:
#             if movie['title'].lower() == title.lower():
#                 return movie
#         return None
    
#     def create_movie(self, movie_data):
#         """Create a new movie"""
#         movie_data['id'] = self.get_next_id()
#         self.data.append(movie_data)
#         self.save_data()
#         return movie_data
    
#     def update_movie(self, movie_id, update_data):
#         """Update an existing movie"""
#         for i, movie in enumerate(self.data):
#             if movie['id'] == movie_id:
#                 self.data[i].update(update_data)
#                 self.save_data()
#                 return self.data[i]
#         return None
    
#     def delete_movie(self, movie_id):
#         """Delete a movie by ID"""
#         for i, movie in enumerate(self.data):
#             if movie['id'] == movie_id:
#                 deleted_movie = self.data.pop(i)
#                 self.save_data()
#                 return deleted_movie
#         return None
    
#     def delete_movie_by_title(self, title):
#         """Delete a movie by title"""
#         for i, movie in enumerate(self.data):
#             if movie['title'].lower() == title.lower():
#                 deleted_movie = self.data.pop(i)
#                 self.save_data()
#                 return deleted_movie
#         return None
    
#     def search_movies(self, title=None, genre=None, year=None, director=None, min_rating=None, max_rating=None):
#         """Search movies by various criteria"""
#         results = self.data
        
#         if title:
#             results = [m for m in results if title.lower() in m.get('title', '').lower()]
        
#         if genre:
#             genre_lower = [g.lower() for g in genre]
#             results = [
#                 m for m in results
#                 if any(g in [gg.lower() for gg in m.get('genre', [])] for g in genre_lower)
#             ]

#         if year:
#             results = [m for m in results if m.get('year') == year]

#         if director:
#             results = [m for m in results if director.lower() in m.get('director', '').lower()]

#         if min_rating is not None:
#             results = [m for m in results if m.get('rating') is not None and m['rating'] >= min_rating]

#         if max_rating is not None:
#             results = [m for m in results if m.get('rating') is not None and m['rating'] <= max_rating]
        
#         return results

# # Global data manager instance
# data_manager = DataManager()









from graphene import ObjectType, String, Int, Float, List, Field, InputObjectType
import json
import os

class Movie(ObjectType):
    id = Int()
    title = String()
    year = Int()
    genre = List(String)
    description = String()
    director = String()
    actors = List(String)
    runtime = Int()
    rating = Float()
    votes = Int()
    revenue = Float()

class MovieInput(InputObjectType):
    title = String(required=True)
    year = Int(required=True)
    genre = List(String, required=True)
    description = String(required=True)
    director = String(required=True)
    actors = List(String, required=True)
    runtime = Int(required=True)
    rating = Float(required=True)
    votes = Int(required=True)
    revenue = Float(required=True)

class MovieUpdateInput(InputObjectType):
    title = String()
    year = Int()
    genre = List(String)
    description = String()
    director = String()
    actors = List(String)
    runtime = Int()
    rating = Float()
    votes = Int()
    revenue = Float()

class DataManager:
    def __init__(self, json_file='imdb.json'):
        self.json_file = json_file
        self.data = self.load_data()
    
    def load_data(self):
        """Load data from JSON file and normalize genres/actors into lists"""
        try:
            with open(self.json_file, 'r') as f:
                data = json.load(f)

            for movie in data:
                g = movie.get("genre")
                if isinstance(g, str):
                    movie["genre"] = [x.strip() for x in g.split(",") if x.strip()]
                elif g is None:
                    movie["genre"] = []

                a = movie.get("actors")
                if isinstance(a, str):
                    movie["actors"] = [x.strip() for x in a.split(",") if x.strip()]
                elif a is None:
                    movie["actors"] = []
            return data

        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        with open(self.json_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def get_next_id(self):
        if not self.data:
            return 1
        return max(movie['id'] for movie in self.data) + 1
    
    def get_all_movies(self):
        return self.data
    
    def get_movie_by_id(self, movie_id):
        return next((m for m in self.data if m['id'] == movie_id), None)
    
    def get_movie_by_title(self, title):
        return next((m for m in self.data if m['title'].lower() == title.lower()), None)
    
    def create_movie(self, movie_data):
        movie_data['id'] = self.get_next_id()
        self.data.append(movie_data)
        self.save_data()
        return movie_data
    
    def update_movie(self, movie_id, update_data):
        for i, movie in enumerate(self.data):
            if movie['id'] == movie_id:
                self.data[i].update(update_data)
                self.save_data()
                return self.data[i]
        return None
    
    def delete_movie(self, movie_id):
        for i, movie in enumerate(self.data):
            if movie['id'] == movie_id:
                deleted_movie = self.data.pop(i)
                self.save_data()
                return deleted_movie
        return None
    
    def delete_movie_by_title(self, title):
        for i, movie in enumerate(self.data):
            if movie['title'].lower() == title.lower():
                deleted_movie = self.data.pop(i)
                self.save_data()
                return deleted_movie
        return None
    
    # ---------------------------
    # Extended Queries
    # ---------------------------
    def search_movies(self, title=None, genre=None, year=None, director=None, actor=None,
                      min_rating=None, max_rating=None):
        results = self.data
        
        if title:
            results = [m for m in results if title.lower() in m.get('title', '').lower()]
        
        if genre:
            genre_lower = [g.lower() for g in genre]
            results = [
                m for m in results
                if any(g in [gg.lower() for gg in m.get('genre', [])] for g in genre_lower)
            ]

        if year:
            results = [m for m in results if m.get('year') == year]

        if director:
            results = [m for m in results if director.lower() in m.get('director', '').lower()]

        if actor:
            results = [m for m in results if any(actor.lower() in a.lower() for a in m.get('actors', []))]

        if min_rating is not None:
            results = [m for m in results if m.get('rating') is not None and m['rating'] >= min_rating]

        if max_rating is not None:
            results = [m for m in results if m.get('rating') is not None and m['rating'] <= max_rating]
        
        return results

    def top_rated(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('rating') or 0, reverse=True)[:limit]

    def top_revenue(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('revenue') or 0, reverse=True)[:limit]

    def movies_by_director(self, director):
        return [m for m in self.data if director.lower() in m.get('director', '').lower()]

    def movies_by_actor(self, actor):
        return [m for m in self.data if any(actor.lower() in a.lower() for a in m.get('actors', []))]

    def movies_by_year(self, year):
        return [m for m in self.data if m.get('year') == year]

    def movies_by_genre(self, genre):
        return [m for m in self.data if genre.lower() in [g.lower() for g in m.get('genre', [])]]

    def average_rating_by_genre(self, genre):
        genre_movies = self.movies_by_genre(genre)
        if not genre_movies:
            return 0.0
        return sum(m.get('rating') or 0 for m in genre_movies) / len(genre_movies)

    def count_movies_by_director(self, director):
        return len(self.movies_by_director(director))

    def revenue_by_year(self, year):
        return sum(m.get('revenue') or 0 for m in self.movies_by_year(year))

    def latest_movies(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('year') or 0, reverse=True)[:limit]

    def earliest_movies(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('year') or 9999)[:limit]

    def longest_movies(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('runtime') or 0, reverse=True)[:limit]

    def most_voted_movies(self, limit=10):
        return sorted(self.data, key=lambda m: m.get('votes') or 0, reverse=True)[:limit]


# Global data manager instance
data_manager = DataManager()
