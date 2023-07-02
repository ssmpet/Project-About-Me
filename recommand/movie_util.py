from flask import current_app
import numpy as np
import pandas as pd
import re, os, string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def movie_util(title, actor, director):
    movies = []
    filename = os.path.join(current_app.static_folder, 'data/movie.csv')

    df = pd.read_csv(filename)
    df.fillna('', inplace=True)
    title = re.sub('['+string.punctuation+']', '', title).lower()
    actor = re.sub('['+string.punctuation+']', '', actor).lower()
    director = re.sub('['+string.punctuation+']', '', director).lower()

    movies = df[df.title.str.replace('['+string.punctuation+']', '', regex=True).str.contains(title, case=False) &
                df.star_actor.str.replace('['+string.punctuation+']', '', regex=True).str.contains(actor, case=False) &
                df.movie_director.str.replace('['+string.punctuation+']', '', regex=True).str.contains(director, case=False)]

    movies = movies[['code', 'title', 'summering', 'first_day', 'img']].to_dict('records')

    return movies


def movie_recommand(movie_code):

    MAX_COUNT = 10
    info, movies, directors, actors  = [], [], [], []
    filename = os.path.join(current_app.static_folder, 'data/movie.csv')
    df = pd.read_csv(filename)
    df.code = df.code.astype(str)
    df.fillna('', inplace=True)

    # 해당 무비 정보
    info = df[df.code == movie_code]
    movie_director = info.movie_director.values[0]
    star_actor = info.star_actor.values[0].replace(' | ', '|')
    star_actor = re.sub(r'\([^)]*\)', '', star_actor)   # (역할) 지우기
    info = info[['code', 'title', 'movie_director', 'star_actor', 'img', 'm_genre', 'm_nation', 'm_rated', 'synopsis', 'first_day']].to_dict('records')[0]

    # 추천 영화
    df['total'] = df.morphs + (' ' + df.title) + (' ' + df.m_genre) * 3 + \
                (' ' + df.movie_director) * 2 + (' ' + df.star_actor) * 2
    
    
    indices = pd.Series(df.index, index=df.code)
    cvect = CountVectorizer(stop_words='english')
    total_cv = cvect.fit_transform(df.total)
    cosine_sim_cv = cosine_similarity(total_cv)
    
    index = indices[movie_code]
    sim_scores = pd.Series(cosine_sim_cv[index])
    codes = sim_scores.sort_values(ascending=False).head(7).tail(6).index

    movies = df.iloc[codes][['code', 'title', 'img']].to_dict('records')

    # 같은 감독의 다른 작품 (감독이 없는 경우도 있다.)
    if movie_director != '':
        indexs = df[df.movie_director.str.contains(movie_director) & (~df.code.str.contains(movie_code))].index
        choice_indexs = indexs if len(indexs) < MAX_COUNT else np.random.choice(indexs, MAX_COUNT - 1, replace=False)
        directors = df.iloc[choice_indexs][['code', 'title', 'img']].to_dict('records')
    

    # 같은 배우들의 다른 작품(배우가 없는 경우도 있다.)
    if star_actor != '':
        indexs = df[df.star_actor.str.contains(star_actor) & (~df.code.str.contains(movie_code))].index
        choice_indexs = indexs if len(indexs) < MAX_COUNT else np.random.choice(indexs, MAX_COUNT - 1, replace=False)
        actors = df.iloc[choice_indexs][['code', 'title', 'img']].to_dict('records')

    return info, movies, directors, actors