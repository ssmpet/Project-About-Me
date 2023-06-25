from flask import Flask, render_template
from word.word import word_bp
from user.user import user_bp
from aboutme.aboutme import aboutme_bp
from crawling.crawling import crawling_bp


app = Flask(__name__)
app.secret_key = 'qwert12345'
app.config['SESSION_COOKIE_PATH'] = '/'


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(word_bp, url_prefix='/word')
app.register_blueprint(aboutme_bp, url_prefix='/aboutme')
app.register_blueprint(crawling_bp, url_prefix='/crawling')
# app.register_blueprint(schedule_bp, url_prefix='/schedule')


###########################################
## 서버를 처음 실행시킬 때 한번 실행된다.

# with app.test_request_context():

#     print('app_context')
#     global g_quote
#     global g_quotes   # 전역변수
#     global g_addr
#     global g_weathers

#     g_quotes = get_saying(app)
#     g_quote = random.sample(g_quotes, 1)[0]
#     g_addr = '수원시 장안구'
#     g_weathers = ''
   
# # @app.before_request_funcs(test_request())

@app.route('/')
def index():

    menu = {'ho': 1, 'us': 0, 'cr': 0, 'ai': 0, 'sc': 0, 'bb': 0}
    return render_template('main/home.html')


if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        print('main end')