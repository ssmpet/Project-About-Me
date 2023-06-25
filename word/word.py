from flask import Blueprint, render_template, request
from flask import current_app
import os

import word.word_util as wu

word_bp = Blueprint('word_bp', __name__)


@word_bp.route('/naver_news')
def word_cloud():
    return render_template('word/naver_news.html')

@word_bp.route('/word_news', methods=['GET', 'POST'])
def word_news():
    if request.method == 'POST':
        news_id = request.form['news']

        return wu.news_word(news_id)
    

@word_bp.route('/word_text')
def word_text():
    return render_template('word/word_text.html')

@word_bp.route('/text_res', methods=['POST'])
def text_res():
    if request.method == 'POST':

        lang = request.form['lang']
        f_text = request.files['text']
        f_mask = request.files['mask']
        stop_words = request.form['stop_words']
        
        file_text = os.path.join(current_app.static_folder, 'upload/') + f_text.filename
        f_text.save(file_text)

        file_mask = ''
        if f_mask:
            file_mask = os.path.join(current_app.static_folder, 'upload/') + f_mask.filename
            f_mask.save(file_mask)

        mtime = wu.word_text(lang, file_text, file_mask, stop_words)

    return render_template('word/text_res.html', mtime=mtime)
