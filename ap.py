import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index= movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x: x[1])[1:11]

    recommended_movies=[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommendation System')
selected_movie_name=st.selectbox('x',movies['title'].values)

if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    num_rows = 2
    num_cols = 5

    for row in range(num_rows):
        cols = st.columns(num_cols)
        for i, col in enumerate(cols):
            movie_index = row * num_cols + i
            if movie_index < len(recommended_movie_names):
                col.text(recommended_movie_names[movie_index])
                col.image(recommended_movie_posters[movie_index])
