from flask import Blueprint, render_template

word_bp = Blueprint('word_bp', __name__)


@word_bp.route('/word_cloud')
def word_cloud():
    return render_template('word/wordcloud.html')