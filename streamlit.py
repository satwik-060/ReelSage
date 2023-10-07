import pandas as pd
import streamlit as st
import pickle
import requests
import ast
from sklearn.metrics.pairwise import cosine_similarity

#setting up
st.set_page_config(
    page_title="ReelSuggest",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "### If you are in a dialemma about what movie to watch, yeah you've come to the correct place."
    }
)

with open('count_matrix.pkl','rb') as f:
    count_matrix = pickle.load(f)

st.title('Welcome to ReelSuggest')
df = pd.read_csv('final_movie_data.csv')

df['comb_title'] = df['title'] + " (" + df['release_date'] + ")"
# print(df.iloc[0])
movies_list = df['comb_title'].values

option = st.selectbox('Searching For A Movie?',movies_list)

#defining functions
def recommend(movie, release_date = None):
    rec_movies = []
    if release_date != None:
        index = df[(df['title'] == movie) & (df['release_date'] == release_date)].index[0]
    else:
        index = df[(df['title'] == movie)].index[0]
    distances = sorted(list(enumerate(cosine_similarity(count_matrix[index], count_matrix)[0])), reverse = True, key = lambda x : x[1])
    
    ctr = 0
    for i in distances[1:]:
        if 'title' not in df.iloc[i[0]].keys() or df.iloc[i[0]].title == "":
            continue
        rec_movies.append([df.iloc[i[0]].id ,df.iloc[i[0]].title])
        ctr += 1
        if ctr == 10:
            break
    return rec_movies

def get_movie_data(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0b899975abbf399f2fbe3965c7bfbe76".format(movie_id)
    data = requests.get(url)
    return data.json()

def get_person_data(person_id):
    url = "https://api.themoviedb.org/3/person/{}?api_key=0b899975abbf399f2fbe3965c7bfbe76".format(person_id)
    data = requests.get(url)
    return data.json()

movie_name = option[:-13]
release_date = option[-11:-1]
movie_id = df[df['comb_title'] == option].iloc[0]['id']

#current movie data
curr_movie_grid = st.columns([2,6,2])
current_movie_data = get_movie_data(movie_id)

st.write('---')
#movie Poster
with curr_movie_grid[0]:
    poster_path = "https://image.tmdb.org/t/p/w500/" + current_movie_data['poster_path']
    st.image(poster_path)

#movie meta data
with curr_movie_grid[1]:
    st.markdown('## *{}*'.format(option))
    st.markdown('**Original Title** : {}'.format(current_movie_data['original_title']))
    st.markdown('**Tag Line** : {}'.format(current_movie_data['tagline']))
    genres = []
    st.markdown('**Overview** : {}'.format(current_movie_data['overview']))
    st.markdown('**Language** : {}'.format(current_movie_data['original_language']))
    
    for genre in current_movie_data['genres']:
        genres.append(genre['name'])
    genres = ', '.join(genres)
    st.markdown('**Genres** : {}'.format(genres))
    st.markdown('**Status** : {}'.format(current_movie_data['status']))
    if 'homepage' in current_movie_data.keys() and current_movie_data['homepage'] != None and current_movie_data['homepage'] != "":
        st.markdown('**Homepage** : {}'.format(current_movie_data['homepage']))
 
 
#director data       
with curr_movie_grid[2]:
    directors = df[df['id'] == movie_id]['crew']

    if len(ast.literal_eval(directors.iloc[0])) == 0:
        director_image = 'static/Image Not Found - Imgur.png'
        st.image(director_image)
    else :
        director_data = get_person_data(ast.literal_eval(directors.iloc[0])[0]['id'])
        st.markdown('#### *Director*'.format(option))
        if('profile_path' in director_data.keys() and director_data['profile_path'] != None):
            director_image = "https://image.tmdb.org/t/p/w500/" + director_data['profile_path']
            st.image(director_image)
        else:
            director_image = 'static/Image Not Found - Imgur.png'
            st.image(director_image)
        st.text(director_data['name'])
    

#current movie cast data
cast_data = ast.literal_eval(df[df['id'] == movie_id].iloc[0]['cast'])
cast_count = len(cast_data)

if cast_count > 0:
    cast_grid = st.columns(min(10, cast_count))
    st.markdown("### Top Cast of {}".format(option))
    for i in range(min(10, cast_count)):
        with cast_grid[i]:
            cast_id = cast_data[i]['char_id']
            cast_data_req = get_person_data(cast_id)
            st.text(cast_data[i]['name'])
            if('profile_path' in cast_data_req.keys() and cast_data_req['profile_path'] != None):
                cast_image = "https://image.tmdb.org/t/p/w500/" + cast_data_req['profile_path']
                st.image(cast_image)
            else:
                cast_image = 'static/Image Not Found - Imgur.png'
                st.image(cast_image)
            st.text(cast_data[i]['character'])
    
# Recommendations
st.write('----')
recommended_movies = recommend(movie_name, release_date)
st.markdown("# Movies You Might Like!")
recommendation_grid = [st.columns(5) for i in range(2)]

k = 0
for i in range(2):
    for j in range(5):
        movie_data = get_movie_data(recommended_movies[k][0])
        with recommendation_grid[i][j]:
            if('title' in movie_data.keys() and movie_data['title'] != None):
                movie_name = movie_data['title'] + " (" + movie_data['release_date'] + ")"
                st.text(movie_name)
            if 'poster_path' in movie_data.keys() and movie_data['poster_path'] != None:
                poster_path = "https://image.tmdb.org/t/p/w500/" + movie_data['poster_path']
                st.image(poster_path)
            
            k+= 1


# Define a function to create the footer
def create_footer():
    st.write('---')
    st.write("🔗 Connect me on [LinkedIn](https://www.linkedin.com/in/sri-satwik-perisetla/)")
    st.write("📦 Official [GitHub Repository](https://github.com/satwik-060/ReelSuggest)")

# Call the function to display the footer
create_footer()