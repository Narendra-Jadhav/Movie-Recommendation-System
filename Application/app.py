import streamlit as st
#Streamlit is an open source app framework in Python language.
# It helps us create web apps for data science and machine learning in a short time
import pickle
import pandas as pd
import requests  # The requests module allows you to send HTTP requests using Python
# used here to hit the API


def fetch_poster(movie_id):  # function to fetch the posters of the recommended movies
    response = requests.get('https://api.themoviedb.org/3/movie/{}'
                            '?api_key=751ff1283f4d9dfa385344db835f2020&language=en-US'.format(movie_id))
    # it contains the API key taken from the TMDB website for movies
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']  # returns the path of the poster of movie


def recommend(movie):  # function which recommends the 5 movies
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # sorted(list(enumerate(similarity[0])),reverse=True,key=lambda x:x[1])[1:6]

    # 1. enumerate -> to make tuple for keeping the index even after sorting
    # 2. [1:6] -> first 5 movies, excluding itself
    # 3. reverse=True for making the sorted list in descending order, for the movie with the most similarity at the top

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies1 = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies1)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')  # to keep the title of the Streamlit app

# st.selectbox is for searching and selecting a movie
selected_movie_name = st.selectbox(
'Enter movie name:',
movies['title'].values
)

# st.button is for creating a button, which on pressing will recommend 5 movies along with their posters
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    # st.columns is to create 5 columns for the 5 recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])  # st.text for the Name of the movie
        st.image(posters[0])  # st.image for the Poster of the movie
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])