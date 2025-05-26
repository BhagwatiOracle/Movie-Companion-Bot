import requests
import pickle
from langchain_core.tools import tool
from langchain_community.tools  import DuckDuckGoSearchRun

new_df=pickle.load(open('movies (1).pkl','rb'))
similarity = pickle.load(open('similarity (1).pkl','rb'))

@tool
def get_movie_info(movie:str) -> str:
  """
  This function fetches the movie information from the TMDB API and also recommend movies based on genre.
  """
  movie_id=new_df[new_df['title']==movie]['movie_id'].values[0]
  url=f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&api_key=50c4398053178353b20fb2fd086e3'
  response = requests.get(url)
  return response.json()

@tool
def get_movie_recommendation(movie:str)->list:
  """
  This function recommends movies based on the input movie.
  """
  movie_index= new_df[new_df['title']==movie].index[0]
  distances = similarity[movie_index]
  movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

  movies=[]
  for i in movie_list:
    movies.append(new_df.iloc[i[0]].title)
  return movies


@tool
def get_popular_movies()-> list:
  """
  This function fetches the top 5 popular movies from the TMDB API.
  """
  url='https://api.themoviedb.org/3/movie/popular?language=en-US&page=1&api_key=50c43980e4e53173b20fb2fd086e3'
  response=requests.get(url)
  results=response.json().get('results')[:5]
  return [movie['title'] for movie in results]


@tool
def get_genre_recommendation(genre: str) -> list:
    """
    Recommend top 5 movies from the local dataset based on the input genre.
    Genre should be something like 'Action', 'Comedy', etc.
    """
    genre = genre.strip().lower()

    # Filter movies that contain the genre
    filtered = new_df[new_df['genres'].apply(lambda x: any(genre==genre_item.lower() for genre_item in x))]['title'].head(5).tolist()
    if not filtered:
        return "No movies found for the given genre."

    return filtered

search_tool=DuckDuckGoSearchRun()