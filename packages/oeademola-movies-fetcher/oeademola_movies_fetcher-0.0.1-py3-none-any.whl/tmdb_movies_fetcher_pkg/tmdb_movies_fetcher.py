import random
import requests

def fetch_movies_from_tmdb(api_base_url, bearer_token, movie_base_url, movie_models):
    """
    Fetches movies from TMDB API and saves them into the database.

    Args:
    - api_base_url (str): Base URL of the TMDB API.
    - bearer_token (str): Bearer token for authorization.
    - movie_base_url (str): Base URL for movie poster paths.
    - movie_models: Module containing movie models.

    Returns:
    - None
    """
    query_list = ['now_playing', 'popular', 'top_rated', 'upcoming']
    movie_list_query = random.choice(query_list)
    url = f"{api_base_url}/movie/{movie_list_query}"
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "accept": "application/json"
    }
    response = requests.get(url=url, headers=headers)
    response_data = response.json().get("results", [])
    for data in response_data:
        movie_data = {
            "title": data["title"],
            "tag": movie_list_query,
            "overview": data["overview"],
            "poster_path": f"{movie_base_url}/w200{data['poster_path']}",
            "release_date": data["release_date"],
            "rating": data["vote_average"]
        }
        instance, created = movie_models.objects.get_or_create(title=movie_data.get("title"), defaults=movie_data)
        if not created:
            patch_existing_movie(instance, movie_data)

def patch_existing_movie(instance, movie_data):
    """
    Updates existing movie instance with new data.

    Args:
    - instance: Existing movie instance.
    - movie_data (dict): New movie data.

    Returns:
    - None
    """
    for key, value in movie_data.items():
        setattr(instance, key, value)
    instance.save()
