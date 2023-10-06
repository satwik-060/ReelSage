import requests

# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=0b899975abbf399f2fbe3965c7bfbe76".format(movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

def get_movie_data(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=0b899975abbf399f2fbe3965c7bfbe76".format(movie_id)
    data = requests.get(url)
    print(type(data))
    return data.json()

def get_person_data(person_id):
    url = "https://api.themoviedb.org/3/person/{}?api_key=0b899975abbf399f2fbe3965c7bfbe76".format(person_id)
    data = requests.get(url)
    return data.json()

def get_now_playing():
    url = "https://api.themoviedb.org/3/movie/now_playing?api_key=0b899975abbf399f2fbe3965c7bfbe76"
    data = requests.get(url)
    return data.json()
# print(get_data(100))
# print(get_person_d
# print(get_now_playing())
# data = get_now_playing()
# print(get_person_data(15))
# for i in range(1,100):
#     data = get_person_data(i)
#     if 'name' in data.keys():
#         print(i,get_person_data(i)['name'])
print(get_movie_data(102))