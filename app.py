import streamlit as st
import pickle
import pandas as pd
import numpy as np
import difflib
import requests
from sklearn.metrics.pairwise import cosine_similarity

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

movies_data = pickle.load(open('movie_df.pkl','rb'))
movie_df= pd.DataFrame(movies_data)

ratings_data = pickle.load(open('ratings_df.pkl','rb'))
ratings_df = pd.DataFrame(ratings_data)

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

linked_dict = pickle.load(open('linked_dict.pkl','rb'))
linked = pd.DataFrame(linked_dict)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=be50118a8d6106595a0efd14a11701dd&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend(movie):
    movie_name = movie.capitalize()

    # creating a list with all the movies given in the data set
    list_of_all_titles = movies['title'].tolist()

    # finding the close match for the movie name given by the user
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    name = find_close_match[0]

    a1= np.array(movie_df.loc[name]).reshape(1,-1)
    a2= np.array(ratings_df.loc[name]).reshape(1,-1)

    score1=cosine_similarity(movie_df, a1).reshape(-1)
    score2=cosine_similarity(ratings_df, a2).reshape(-1)

    hybrid=((score1+score2)/2.0)

    dictDf = {'content': score1, 'collabarative': score2, 'hybrid': hybrid }
    similar=pd.DataFrame(dictDf, index=movie_df.index)


    similar.sort_values('hybrid', ascending=False, inplace=True)


    recommended_movies = []
    recommended_movies_poster = []
    for i in range(len(similar.head(11))):
        recommended_movies.append(similar.index[i])
        match = linked[linked['title'].isin(recommended_movies)]
        movie_id = match['tmdbId'].tolist()[i]
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster    


st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Choose or Type the movie name',
    movies['title'].values
)

if st.button('Recommend'):
    names , posters = recommend(selected_movie_name)
    
    col1 , col2 , col3  = st.columns(3)
    with col1:
        st.subheader(names[0])
        st.image(posters[0], width=150)
    with col2:
        st.subheader(names[1])
        st.image(posters[1], width=150)
    with col3:
        st.subheader(names[2])
        st.image(posters[2], width=150)
    with col1:
        st.subheader(names[3])
        st.image(posters[3], width=150)
    with col2:
        st.subheader(names[4])
        st.image(posters[4], width=150)
    with col3:
        st.subheader(names[5])
        st.image(posters[4], width=150)
        

   