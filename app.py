import streamlit as st
import pickle 
import pandas as pd
import requests

url = "https://drive.google.com/file/d/1MJRf2iQeIcND3xbSWkslQGh_hmx1AyIF/view?usp=sharing"
response = requests.get(url)

with open("sparse_matrix.pkl", "wb") as file:
    file.write(response.content)
    
def fetch_poster(movie_id):
    # Use requests.get to make the API call
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6dd5d25c600b8744fe8363ba7ebfae90&language=en-US".format(movie_id))
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/original/" + data["poster_path"]
    else:
        # Handle the case where the request was not successful
        st.error("Error fetching poster. Please try again.")
        return None

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching poster from API
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open("movies_dict.pkl", "rb")) 
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("sparse_matrix.pkl", "rb"))

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox("Name your movie", movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0], width=150)
    with col2:
        st.text(names[1])
        st.image(posters[1], width=150)
    with col3:
        st.text(names[2])
        st.image(posters[2], width=150)
    with col4:
        st.text(names[3])
        st.image(posters[3], width=150)
    with col5:
        st.text(names[4])
        st.image(posters[4], width=150)
