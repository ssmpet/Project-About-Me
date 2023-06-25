from flask import current_app

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

from  bs4 import BeautifulSoup
from selenium import webdriver
import time

import warnings
warnings.filterwarnings('ignore')

import nltk, re
from konlpy.tag import Okt
from wordcloud import WordCloud

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from PIL import Image
from wordcloud import ImageColorGenerator

import os

# 네이버 헤드라인 뉴스
def news_word(news_id):

    print("news1")
    options = webdriver.ChromeOptions() # 화면없이
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    url1 = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="
    url2 = "#&date=%2000:00:00&page=1"
    driver_name =  os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\\Downloads\\chromedriver_win32\\chromedriver.exe'

    url = url1 + news_id + url2
    
    print("news2")
    try:
        driver = webdriver.Chrome(driver_name, options=options)
        driver.get(url)
        time.sleep(2)
    except:
        print("except error : webdriver")
        driver.quit()
        return "error1"

    print("news3")
    soup = BeautifulSoup(driver.page_source, "html")

    news_url = []
    # 헤드라인 뉴스 목록
    head_lis = soup.select('.section_headline > ul > li')
    for hli in head_lis :
        news_url.append(hli.select_one('.sh_text > a')['href'])
        
    # 나머지 추가 뉴스 목록
    sec_lis = soup.select('.section_body > ul > li')
    for sli in sec_lis:
        news_url.append(sli.select_one('dt > a')['href'])

    print("news4")
    # 세부 기사 가져오기
    news = ''
    for nurl in news_url:    
        try:
            print("news5")
            driver.get(nurl)
            time.sleep(2)
        except:
            print("execpt error : url")
            driver.quit()
            return "error2"
        
        soup = BeautifulSoup(driver.page_source, 'html')

        # 클래스명이나 규칙에 어긋날 경우 에러 처리
        try :
            title = soup.select_one('.media_end_head_headline').text
            # separator 해 주면 <br>등의 태그들이 들어간 자리를 띄어쓰기 해 준다.
            desc = soup.select_one('#dic_area').get_text(separator=' ', strip=True) 
            news += title + ' '
            news += desc + ' '
        except :
            continue

    driver.quit()
    
    # 한글과 영어도 같이 추출할 수 있는 것이 없어서 따로따로 분리 한다.
    desc_ko, desc_eng = '', ''
    desc_ko = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', news)
    desc_eng = re.sub('[^A-Za-z]', ' ', news)

    # 불용어 정리 
    fname = os.path.join(current_app.static_folder, 'data/한글불용어.txt')
    with open(fname, encoding='utf-8') as st:
        lines = st.readlines()
    stop_words = [line.strip() for line in lines]    

    # 한글 명사 분석
    okt = Okt()
    tokens = okt.nouns(desc_ko)
    tokens =  [word for word in tokens if word not in stop_words]

    # 영문 분석
    stop_words_eng = stopwords.words('english')
    tokens_eng = word_tokenize(desc_eng)
    tokens_eng = [word for word in tokens_eng if word.lower() not in stop_words_eng and len(word) > 1]

    # 영문과 한글 합치기
    tokens.extend(tokens_eng)

    news = nltk.Text(tokens, name="네이버 뉴스")
    fname = os.path.join(current_app.static_folder, 'img/data_science1.jpg')
    mask = np.array(Image.open(fname))
    image_colors = ImageColorGenerator(mask)

    # 워드 클라우드 그리기
    fname = os.path.join(current_app.static_folder, 'img/wordcloud.png')
    wc = WordCloud(
        background_color='white', 
        random_state=2023,
        font_path='C:/Windows/Fonts/HMFMOLD.TTF', 
        mask=mask
    ).generate_from_frequencies(dict(news.vocab().most_common(100)))

    # 이미지 저장
    plt.figure(figsize=(10, 6))
    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis('off')
    plt.savefig(fname, bbox_inches='tight', pad_inches=0.1)

    # cash 방지 : 마지막 저장 시간을 리턴해 준다.
    mtime = str(os.stat(fname).st_mtime)

    return mtime

# 텍스트 파일 워드클라우드 이미지 파일 만들기
def make_wordcloud(tokens, text, f_mask):

    fname = os.path.join(current_app.static_folder, 'img/word_text.png')

    texts = nltk.Text(tokens, text)
    plt.figure(figsize=(10, 10))
    if f_mask:
        mask = mask = np.array(Image.open(f_mask))
        wc = WordCloud(
                background_color='white',
                random_state=2023,
                font_path='C:/windows/fonts/HMFMOLD.TTF',
                mask=mask
            ).generate_from_frequencies(dict(texts.vocab().most_common(300)))
        
        if mask.ndim == 2:
            plt.imshow(wc, interpolation='bilinear')
        else :
            image_colors = ImageColorGenerator(mask)
            plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    else:
        wc = WordCloud(
            background_color='white',
            random_state=2023,
            font_path='C:/windows/fonts/HMFMOLD.TTF'
        ).generate_from_frequencies(dict(texts.vocab().most_common(300)))
        plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(fname, bbox_inches='tight', pad_inches=0.1)

    return str(os.stat(fname).st_mtime)


# 텍스트 파일 워드클라우드
def word_text(lang, f_text, f_mask, stop_words):

    with open(f_text, encoding='utf-8') as f:
        desc = f.read()

    # 불용어 처리 
    # 사용자가 잘못 처리할 경우 한글과 영어 체크
    # 한글 + 영어 인 경우도 분리해서 체크
    sword_ko, sword_en = [], []
    if stop_words !='':
        for word in stop_words.split():
            if word == '': continue
            if re.search('[ㄱ-ㅎㅏ-ㅣ가-힣]', word):
                sword_ko.append(word)           # 한글 
            else:
                sword_en.append(word.lower())   # 영어

    # 한글 분석
    if lang == 'ko':
        desc_ko = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', desc)

        # 한글불용어
        fname = os.path.join(current_app.static_folder, 'data/한글불용어.txt')
        with open(fname, encoding='utf-8') as f:
            lines = f.readlines()
        sword_ko.extend([line.strip() for line in lines])

        # 한글 명사 분석
        okt = Okt()
        tokens = okt.nouns(desc_ko)
        tokens = [word for word in tokens if word not in sword_ko]

        text = '한글 워드클라우드'
 
    # 영어 분석
    elif lang == 'en':
        desc_en = re.sub('[^a-zA-Z]', ' ', desc)
        
        # 영어불용어
        sword_en.extend(stopwords.words('english'))
        tokens = word_tokenize(desc_en)
        tokens = [word for word in tokens if word.lower() not in sword_en]
        text = '영어 워드클라우드'

    # 한글 + 영어 분석
    else:
        desc_ko = re.sub('[^ㄱ-ㅎㅏ-ㅣ가-힣]', ' ', desc)
        desc_en = re.sub('[^a-zA-Z]', ' ', desc)    

        fname = os.path.join(current_app.static_folder, 'data/한글불용어.txt')
        with open(fname, encoding='utf-8') as f:
            lines = f.readlines()
        sword_ko.extend([line.strip() for line in lines])
        sword_en.extend(stopwords.words('english'))

         # 한글 명사 분석
        okt = Okt()
        tokens = okt.nouns(desc_ko)
        tokens = [word for word in tokens if word not in sword_ko]

        # 영어 분석
        tokens_en = word_tokenize(desc_en)
        tokens_en = [word for word in tokens_en if word.lower() not in sword_en]

        # 한글 + 영어
        tokens.extend(tokens_en)

        text = '한글+영어 워드클라우드'
    
    # 워드 클라우드 그리기
    return make_wordcloud(tokens, text, f_mask)

    

    


