from flask import current_app
import pandas as pd
import re, os, string


def movie_util(title, actor):
    movies = []
    filename = os.path.join(current_app.static_folder, 'data/movie_test.csv')

    df = pd.read_csv(filename)
    df.fillna('', inplace=True)
    title = re.sub('['+string.punctuation+']', '', title).lower()
    actor = re.sub('['+string.punctuation+']', '', actor).lower()

    movies = df[df.title.str.replace('['+string.punctuation+']', '', regex=True).str.contains(title, case=False) &
                df.star_actor.str.replace('['+string.punctuation+']', '', regex=True).str.contains(actor, case=False)]

    movies = movies[['code', 'title', 'summering', 'first_day', 'img']].to_dict('records')

    return movies


def movie_recommand(movie_code):
    filename = os.path.join(current_app.static_folder, 'data/movie_test.csv')
    df = pd.read_csv(filename)
    df.fillna('', inplace=True)
    return df[df.code == movie_code][['code', 'title', 'img', 'm_genre', 'm_nation', 'm_rated', 'synopsis', 'first_day']].to_dict('records')[0]