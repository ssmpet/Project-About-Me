from flask import Blueprint, render_template, request
from flask import current_app
import recommand.movie_util as rm

recommand_bp = Blueprint('recommand_bp', __name__)

# 영화 추천 검색
@recommand_bp.route('/movie_search')
def movie_search():
    return render_template('/recommand/movie_search.html')
    
# 영화 검색 리스트
@recommand_bp.route('/movie_list', methods=['GET', 'POST'])
def movie_list():
    if request.method == 'POST':
        title = request.form['title']
        actor = request.form['actor']
        movies = rm.movie_util(title, actor)
        return render_template('/recommand/movie_list.html', movies=movies)

@recommand_bp.route('/movie_res', methods=['GET', 'POST'])
def movie_res():
    if request.method == 'POST':
        movie_code = request.form['movie_code'] 
        info, recommand_movies, directors, actors = rm.movie_recommand(movie_code)
        return render_template('/recommand/movie_res.html', info=info, recommand_movies=recommand_movies, directors=directors, actors=actors)
