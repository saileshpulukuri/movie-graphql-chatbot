# from graphene import ObjectType, String, Int, Float, List, Field, Mutation, Argument
# from models import Movie, MovieInput, MovieUpdateInput, data_manager


# class Query(ObjectType):
#     # Get all movies (with optional limit/offset for pagination)
#     movies = List(Movie, limit=Int(), offset=Int())

#     # Get movie by ID
#     movie = Field(Movie, id=Int(required=True))

#     # Get movie by title
#     movie_by_title = Field(Movie, title=String(required=True))

#     # Search movies with various criteria
#     search_movies = List(
#         Movie,
#         title=String(),
#         genre=List(String),
#         year=Int(),
#         director=String(),
#         actor=String(),
#         min_rating=Float(),
#         max_rating=Float(),
#         limit=Int(),
#     )

#     # Top N rated movies
#     top_rated_movies = List(Movie, limit=Int(default_value=10))

#     # Top N revenue movies
#     top_revenue_movies = List(Movie, limit=Int(default_value=10))

#     # Movies by director
#     movies_by_director = List(Movie, director=String(required=True))

#     # Movies by actor
#     movies_by_actor = List(Movie, actor=String(required=True))

#     # Movies by year
#     movies_by_year = List(Movie, year=Int(required=True))

#     # Movies by genre
#     movies_by_genre = List(Movie, genre=String(required=True))

#     # Average rating by genre
#     average_rating_by_genre = Float(genre=String(required=True))

#     # Count movies by director
#     count_movies_by_director = Int(director=String(required=True))

#     # Total revenue by year
#     revenue_by_year = Float(year=Int(required=True))

#     # Latest movies (newest releases)
#     latest_movies = List(Movie, limit=Int(default_value=10))

#     # Earliest movies (oldest releases)
#     earliest_movies = List(Movie, limit=Int(default_value=10))

#     # Longest runtime movies
#     longest_movies = List(Movie, limit=Int(default_value=10))

#     # Most voted movies
#     most_voted_movies = List(Movie, limit=Int(default_value=10))

#     # --- RESOLVERS ---

#     def resolve_movies(self, info, limit=None, offset=None):
#         movies = data_manager.get_all_movies()
#         if offset:
#             movies = movies[offset:]
#         if limit:
#             movies = movies[:limit]
#         return movies

#     def resolve_movie(self, info, id):
#         return data_manager.get_movie_by_id(id)

#     def resolve_movie_by_title(self, info, title):
#         return data_manager.get_movie_by_title(title)

#     def resolve_search_movies(self, info, title=None, genre=None, year=None,
#                               director=None, actor=None, min_rating=None,
#                               max_rating=None, limit=None):
#         results = data_manager.search_movies(
#             title=title, genre=genre, year=year,
#             director=director, actor=actor,
#             min_rating=min_rating, max_rating=max_rating
#         )
#         if limit:
#             results = results[:limit]
#         return results

#     def resolve_top_rated_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.rating or 0, reverse=True)
#         return movies[:limit]

#     def resolve_top_revenue_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.revenue or 0, reverse=True)
#         return movies[:limit]

#     def resolve_movies_by_director(self, info, director):
#         return data_manager.search_movies(director=director)

#     def resolve_movies_by_actor(self, info, actor):
#         return data_manager.search_movies(actor=actor)

#     def resolve_movies_by_year(self, info, year):
#         return data_manager.search_movies(year=year)

#     def resolve_movies_by_genre(self, info, genre):
#         return data_manager.search_movies(genre=[genre])

#     def resolve_average_rating_by_genre(self, info, genre):
#         movies = data_manager.search_movies(genre=[genre])
#         if not movies:
#             return 0.0
#         return sum(m.rating or 0 for m in movies) / len(movies)

#     def resolve_count_movies_by_director(self, info, director):
#         movies = data_manager.search_movies(director=director)
#         return len(movies)

#     def resolve_revenue_by_year(self, info, year):
#         movies = data_manager.search_movies(year=year)
#         return sum(m.revenue or 0 for m in movies)

#     def resolve_latest_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.year or 0, reverse=True)
#         return movies[:limit]

#     def resolve_earliest_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.year or 9999)
#         return movies[:limit]

#     def resolve_longest_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.runtime or 0, reverse=True)
#         return movies[:limit]

#     def resolve_most_voted_movies(self, info, limit=10):
#         movies = sorted(data_manager.get_all_movies(), key=lambda m: m.votes or 0, reverse=True)
#         return movies[:limit]


# # --- MUTATIONS (same as your code) ---
# class CreateMovie(Mutation):
#     class Arguments:
#         movie_data = MovieInput(required=True)

#     movie = Field(Movie)
#     success = String()
#     message = String()

#     def mutate(self, info, movie_data):
#         try:
#             movie = data_manager.create_movie(dict(movie_data))
#             return CreateMovie(movie=movie, success="true", message="Movie created successfully")
#         except Exception as e:
#             return CreateMovie(movie=None, success="false", message=f"Error creating movie: {str(e)}")


# class UpdateMovie(Mutation):
#     class Arguments:
#         id = Int(required=True)
#         movie_data = MovieUpdateInput(required=True)

#     movie = Field(Movie)
#     success = String()
#     message = String()

#     def mutate(self, info, id, movie_data):
#         try:
#             update_data = {k: v for k, v in dict(movie_data).items() if v is not None}
#             movie = data_manager.update_movie(id, update_data)
#             if movie:
#                 return UpdateMovie(movie=movie, success="true", message="Movie updated successfully")
#             else:
#                 return UpdateMovie(movie=None, success="false", message="Movie not found")
#         except Exception as e:
#             return UpdateMovie(movie=None, success="false", message=f"Error updating movie: {str(e)}")


# class DeleteMovie(Mutation):
#     class Arguments:
#         id = Int()
#         title = String()

#     movie = Field(Movie)
#     success = String()
#     message = String()

#     def mutate(self, info, id=None, title=None):
#         try:
#             if title:
#                 movie = data_manager.delete_movie_by_title(title)
#             elif id:
#                 movie = data_manager.delete_movie(id)
#             else:
#                 return DeleteMovie(movie=None, success="false", message="Either id or title must be provided")

#             if movie:
#                 return DeleteMovie(movie=movie, success="true", message="Movie deleted successfully")
#             else:
#                 return DeleteMovie(movie=None, success="false", message="Movie not found")
#         except Exception as e:
#             return DeleteMovie(movie=None, success="false", message=f"Error deleting movie: {str(e)}")


# class Mutation(ObjectType):
#     create_movie = CreateMovie.Field()
#     update_movie = UpdateMovie.Field()
#     delete_movie = DeleteMovie.Field()


# from graphene import Schema
# schema = Schema(query=Query, mutation=Mutation)







from graphene import ObjectType, String, Int, Float, List, Field, Mutation
from models import Movie, MovieInput, MovieUpdateInput, data_manager


class Query(ObjectType):
    # Get all movies (with optional limit/offset for pagination)
    movies = List(Movie, limit=Int(), offset=Int())

    # Get movie by ID
    movie = Field(Movie, id=Int(required=True))

    # Get movie by title
    movie_by_title = Field(Movie, title=String(required=True))

    # Search movies
    search_movies = List(
        Movie,
        title=String(),
        genre=List(String),
        year=Int(),
        director=String(),
        actor=String(),
        min_rating=Float(),
        max_rating=Float(),
        limit=Int(),
    )

    # Extended queries
    top_rated_movies = List(Movie, limit=Int(default_value=10))
    top_revenue_movies = List(Movie, limit=Int(default_value=10))
    movies_by_director = List(Movie, director=String(required=True))
    movies_by_actor = List(Movie, actor=String(required=True))
    movies_by_year = List(Movie, year=Int(required=True))
    movies_by_genre = List(Movie, genre=String(required=True))
    average_rating_by_genre = Float(genre=String(required=True))
    count_movies_by_director = Int(director=String(required=True))
    revenue_by_year = Float(year=Int(required=True))
    latest_movies = List(Movie, limit=Int(default_value=10))
    earliest_movies = List(Movie, limit=Int(default_value=10))
    longest_movies = List(Movie, limit=Int(default_value=10))
    most_voted_movies = List(Movie, limit=Int(default_value=10))

    # --- RESOLVERS ---
    def resolve_movies(self, info, limit=None, offset=None):
        movies = data_manager.get_all_movies()
        if offset:
            movies = movies[offset:]
        if limit:
            movies = movies[:limit]
        return movies

    def resolve_movie(self, info, id):
        return data_manager.get_movie_by_id(id)

    def resolve_movie_by_title(self, info, title):
        return data_manager.get_movie_by_title(title)

    def resolve_search_movies(self, info, title=None, genre=None, year=None,
                              director=None, actor=None, min_rating=None,
                              max_rating=None, limit=None):
        results = data_manager.search_movies(
            title=title, genre=genre, year=year,
            director=director, actor=actor,
            min_rating=min_rating, max_rating=max_rating
        )
        if limit:
            results = results[:limit]
        return results

    def resolve_top_rated_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("rating") or 0, reverse=True)
        return movies[:limit]

    def resolve_top_revenue_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("revenue") or 0, reverse=True)
        return movies[:limit]

    def resolve_movies_by_director(self, info, director):
        return data_manager.search_movies(director=director)

    def resolve_movies_by_actor(self, info, actor):
        return data_manager.search_movies(actor=actor)

    def resolve_movies_by_year(self, info, year):
        return data_manager.search_movies(year=year)

    def resolve_movies_by_genre(self, info, genre):
        return data_manager.search_movies(genre=[genre])

    def resolve_average_rating_by_genre(self, info, genre):
        movies = data_manager.search_movies(genre=[genre])
        if not movies:
            return 0.0
        return sum(m.get("rating") or 0 for m in movies) / len(movies)

    def resolve_count_movies_by_director(self, info, director):
        movies = data_manager.search_movies(director=director)
        return len(movies)

    def resolve_revenue_by_year(self, info, year):
        movies = data_manager.search_movies(year=year)
        return sum(m.get("revenue") or 0 for m in movies)

    def resolve_latest_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("year") or 0, reverse=True)
        return movies[:limit]

    def resolve_earliest_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("year") or 9999)
        return movies[:limit]

    def resolve_longest_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("runtime") or 0, reverse=True)
        return movies[:limit]

    def resolve_most_voted_movies(self, info, limit=10):
        movies = sorted(data_manager.get_all_movies(), key=lambda m: m.get("votes") or 0, reverse=True)
        return movies[:limit]


# --- MUTATIONS ---
class CreateMovie(Mutation):
    class Arguments:
        movie_data = MovieInput(required=True)

    movie = Field(Movie)
    success = String()
    message = String()

    def mutate(self, info, movie_data):
        try:
            movie = data_manager.create_movie(dict(movie_data))
            return CreateMovie(movie=movie, success="true", message="Movie created successfully")
        except Exception as e:
            return CreateMovie(movie=None, success="false", message=f"Error creating movie: {str(e)}")


class UpdateMovie(Mutation):
    class Arguments:
        id = Int(required=True)
        movie_data = MovieUpdateInput(required=True)

    movie = Field(Movie)
    success = String()
    message = String()

    def mutate(self, info, id, movie_data):
        try:
            update_data = {k: v for k, v in dict(movie_data).items() if v is not None}
            movie = data_manager.update_movie(id, update_data)
            if movie:
                return UpdateMovie(movie=movie, success="true", message="Movie updated successfully")
            else:
                return UpdateMovie(movie=None, success="false", message="Movie not found")
        except Exception as e:
            return UpdateMovie(movie=None, success="false", message=f"Error updating movie: {str(e)}")


class DeleteMovie(Mutation):
    class Arguments:
        id = Int()
        title = String()

    movie = Field(Movie)
    success = String()
    message = String()

    def mutate(self, info, id=None, title=None):
        try:
            if title:
                movie = data_manager.delete_movie_by_title(title)
            elif id:
                movie = data_manager.delete_movie(id)
            else:
                return DeleteMovie(movie=None, success="false", message="Either id or title must be provided")

            if movie:
                return DeleteMovie(movie=movie, success="true", message="Movie deleted successfully")
            else:
                return DeleteMovie(movie=None, success="false", message="Movie not found")
        except Exception as e:
            return DeleteMovie(movie=None, success="false", message=f"Error deleting movie: {str(e)}")


class Mutation(ObjectType):
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()


from graphene import Schema
schema = Schema(query=Query, mutation=Mutation)
