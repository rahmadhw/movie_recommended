import streamlit as st
import pickle
import pandas as pd
import requests
from tmdbv3api import TMDb
from tmdbv3api import Movie
movie_pop = Movie()
tmdb = TMDb()
tmdb.api_key = '661f55b5dc7fb38e982f94e5e6114652'

st.set_page_config(layout="wide")
with open("style.css")as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

movies_dict = pickle.load(open('modelling_pickle/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('modelling_pickle/similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=661f55b5dc7fb38e982f94e5e6114652&languange=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommend_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommend_movies_poster




def main():
    from tmdbv3api import TMDb
    import streamlit as st
    meta = ''' 
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    '''
    title = ''' 

        <div class="title-container">
            <h1>Movie Recommendation system</h1>
        </div>
    
    '''

    title_movie = '''

        <div class="title_movie">
           <div id="heading-dua">
             <h2 class="hd" style="color:black !important">Sinopsis</h2>
           </div>
            <span>    Film, juga dikenal sebagai movie, gambar hidup, film teater atau foto bergerak, adalah serangkaian gambar diam, yang ketika ditampilkan pada layar akan menciptakan ilusi gambar bergerak yang dikarenakan efek fenomena phi. Ilusi optik ini memaksa penonton untuk melihat gerakan berkelanjutan antar objek yang berbeda secara cepat dan berturut-turut. Proses pembuatan film merupakan gabungan dari seni dan industri. Sebuah film dapat dibuat dengan memotret adegan sungguhan dengan kamera film; memotret gambar atau model "miniatur" menggunakan teknik animasi tradisional; dengan CGI dan animasi komputer; atau dengan kombinasi beberapa teknik yang ada dan efek visual lainnya.
            </span>
        </div>
    
    '''
    st.markdown(meta, unsafe_allow_html=True)
    st.markdown(title, unsafe_allow_html=True)
    st.markdown(title_movie, unsafe_allow_html=True)

    st.subheader("Movie Populer Pertahun")
    tahun1 = 1999
    tahun2 = 2000
    tahun3 = 2001
    tahun4 = 2002
    tahun5 = 2003
    tahun6 = 2004
    tahun7 = 2005
    tahun8 = 2006
    tahun9 = 2007
    tahun10 = 2008
    tahun11 = 2009
    tahun12 = 2010
    tahun12 = 2011
    tahun13 = 2012
    tahun14 = 2013
    tahun15 = 2014
    tahun16 = 2015
    tahun17 = 2016
    tahun18 = 2017

    year_select = st.selectbox(
        'Lihat Film berdasarkan tahun',
        (str(tahun1), str(tahun2), str(tahun3), str(tahun4), str(tahun5), str(tahun6), str(tahun7), str(tahun8), str(tahun9), str(tahun10), str(tahun11), str(tahun12), str(tahun13), str(tahun14), str(tahun15), str(tahun16), str(tahun17), str(tahun18))
    )

    if st.button("Search"):
        api_key = '661f55b5dc7fb38e982f94e5e6114652'
        respond = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=661f55b5dc7fb38e982f94e5e6114652&primary_release_year={}'.format(year_select))
        results = respond.json()
        results = results
        results = results["results"][0:6]
        rows = [st.columns(4)]
        cols = [column for row in rows for column in row]
        for col, pop in zip(cols, results):
             col.image("https://image.tmdb.org/t/p/w500/"+ pop["backdrop_path"], width=200)
             col.caption(pop["original_title"])
             col.caption("Overview :  \n" + pop["overview"])
             
    st.subheader("Movie Populer")
    from tmdbv3api import Movie
    movie_pop = Movie()
    popular = movie_pop.popular()
    rows = [st.columns(5)]
    cols = [column for row in rows for column in row]
    for col, pop in zip(cols, popular):
        col.image("https://image.tmdb.org/t/p/w500/"+pop.poster_path, width=200)
        col.caption(pop.title)
        col.caption("Overview:  \n" + pop.overview)

    st.subheader("Best Seller")
    trend = movie_pop.similar(777)
    rows = [st.columns(5)]
    cols = [column for row in rows for column in row]
    for col, pop in zip(cols, trend):
        col.image("https://image.tmdb.org/t/p/w500/"+pop.poster_path, width=200)
        col.caption(pop.title)
        col.caption("Overview:  \n" + pop.overview)

    st.subheader("Tv Show")
    from tmdbv3api import TV
    tv_pop = TV()
    tv =tv_pop.similar(1396)
    rows = [st.columns(5)]
    cols = [column for row in rows for column in row]
    for col, pop in zip(cols, tv):
        col.image("https://image.tmdb.org/t/p/w500/"+pop.poster_path, width=200)
        col.caption(pop.name)
        col.caption("Overview  " + pop.overview)
    selected_movies_name = st.selectbox('silakan inputkan movie', movies['title'][0:100].values)
    if st.button("Recommended"):
        names,poster=recommend(selected_movies_name)
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            st.image(poster[0], width=200)
            st.caption(names[0])
        with col2:
            st.image(poster[1], width=200)
            st.caption(names[1])
        with col3:
            st.image(poster[2], width=200)
            st.caption(names[2])
        with col4:
            st.image(poster[3], width=200)
            st.caption(names[3])
        with col5:
            st.image(poster[4], width=200)
            st.caption(names[4])


if __name__ == '__main__':
	main()
