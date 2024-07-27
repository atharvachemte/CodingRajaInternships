import streamlit as st
import pickle
import pandas as pd
import requests

OMDB_API_KEY = 'ea9fd588'

@st.cache_data
def load_data():
    movies = pickle.load(open('movies.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

@st.cache_data
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title.replace(' ', '+')}&apikey={OMDB_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != 'N/A':
            return poster_url
        else:
            return 'https://via.placeholder.com/500x750?text=No+Image+Available'
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return 'https://via.placeholder.com/500x750?text=Error'

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_titles = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movie_titles.append(movie_title)

    return recommended_movies, recommended_movie_titles

st.title('Movie Recommendation System')

movies_list = movies['title'].values
option = st.selectbox(
    "Select a movie to get recommendations:",
    movies_list
)

if st.button("Recommend"):
    recommendations, movie_titles = recommend(option)

    cols = st.columns(5)
    for i, col in enumerate(cols):
        if i < len(recommendations):
            with col:
                st.text(recommendations[i])
                poster_url = fetch_poster(movie_titles[i])
                st.image(poster_url)

