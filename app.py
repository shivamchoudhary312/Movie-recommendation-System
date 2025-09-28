import streamlit as st
import pickle
import pandas as pd
import gzip

# Load the data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl.gz', 'rb'))
with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)


movies = pd.DataFrame(movies_dict)

# Page config
st.set_page_config(page_title="Movie Recommender 🎬", page_icon="🎥", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .stSelectbox label {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #333333 !important;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        color: #0077b6;
    }
    .rec-box {
        padding: 12px;
        margin: 8px auto;
        border-radius: 12px;
        background-color: #e3f2fd;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 60%;
        text-align: center;
    }
    .center-text {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='center-text' style='color: #d62828;'>🎬 Movie Recommendation System 🍿</h1>", unsafe_allow_html=True)
st.markdown("<p class='center-text' style='font-size:18px;'>Select a movie from the dropdown to get similar recommendations!</p>", unsafe_allow_html=True)

# Recommendation function
def recommend(movie):
    if movie not in movies['title'].values:
        return ["Movie not found in database"]
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Selectbox for movies
selected_movie = st.selectbox("🎥 Choose a movie", movies['title'].values)

# Button
if st.button("✨ Recommend"):
    recommendations = recommend(selected_movie)
    st.markdown("<h3 class='center-text' style='color:#1d3557;'>🔥 Recommended Movies</h3>", unsafe_allow_html=True)
    
    for rec in recommendations:
        st.markdown(f"<div class='rec-box'>✅ <span class='movie-title'>{rec}</span></div>", unsafe_allow_html=True)
