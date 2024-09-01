import pickle
import streamlit as st
import requests

# Function to fetch movie posters from The Movie Database API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6a01be7bf28e922772d4d743b22cfae8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else ""
    return full_path, data.get('vote_average', 'N/A'), data.get('overview', 'No description available.')

# Function to recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    movie_ratings = []
    movie_overviews = []
    
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating, overview = fetch_poster(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        movie_ratings.append(rating)
        movie_overviews.append(overview)
    
    return recommended_movie_names, recommended_movie_posters, movie_ratings, movie_overviews

# Streamlit App UI
st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Movie Recommender System</h1>", unsafe_allow_html=True)

movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Search bar for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list,
    index=0,
    help="Search for a movie you like to get recommendations!"
)

# Button to show recommendations
if st.button('Show Recommendation', key="recommend"):
    recommended_movie_names, recommended_movie_posters, movie_ratings, movie_overviews = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_column_width=True)
            st.markdown(f"**{recommended_movie_names[idx]}**")
            st.markdown(f"Rating: {movie_ratings[idx]}/10")
            st.markdown(f"*{movie_overviews[idx][:150]}...*")  # Display a brief overview

# Adding some additional styling
st.markdown("""
    <style>
    .stButton button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 12px;
    }
    .stButton button:hover {
        background-color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)
