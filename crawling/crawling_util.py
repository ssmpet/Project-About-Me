
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote

# 인터파크 베스트셀러 가져오기
def interpark_util():
    base_url = 'https://book.interpark.com'
    url = "http://book.interpark.com/display/collectlist.do?_method=BestsellerHourNew201605&bestTp=1&dispNo=028"
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

    try :
        result = requests.get(url, headers=header)
    except:
        print("URL requests get error")
        return []

    soup = BeautifulSoup(result.text, 'html.parser')

    lis = soup.select('.rankBestContentList > ol > li')

    lines = []
    for li in lis:

        # 웹 페이지 변경시 에러 처리
        try : 
            rank_data = li.select('.rankBtn_ctrl')

            if len(rank_data) == 1:
                rank = int(rank_data[0]['class'][-1][-1])
            else:
                rank = int(rank_data[0]['class'][-1][-1] + rank_data[-1]['class'][-1][-1])

            title_info = base_url + li.select_one('.coverImage > label > a')['href']
            img = li.select_one('.coverImage > label > a > img')['src']
            title = li.select_one('.itemName').get_text().strip()
            author = li.select_one('.author').get_text().strip()
            company = li.select_one('.company').get_text().strip()
            price = li.select_one('.price > em').get_text().strip()
            lines.append({'순위': rank,  '이미지':img, '제목':title, '저자': author, '출판사': company, '판매가': price, '세부정보': title_info})
        except:
            pass

    return lines

# 지니차트 100곡 가져오기
def genie_chart_util():
    info_url = 'https://www.genie.co.kr/detail/songInfo?xgnm='
    base_url = 'https://www.genie.co.kr/chart/top200?ditc=D'
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}

    now = datetime.now()
    ymd = now.strftime('%Y%m%d')
    hh = now.strftime('%H')

    lines = []

    for page in range(1, 3):
        url = f'{base_url}&ymd={ymd}&hh={hh}&rtm=Y&pg={page}'
        try : 
            result = requests.get(url, headers=header)
        except :
            return []
    
        soup = BeautifulSoup(result.text, 'html.parser')

        trs = soup.select('tr.list')

        for tr in trs:
            try : 
                rank = tr.select_one('.number').get_text().split('\n')[0].strip()
                href = info_url + tr.select_one('.link > a')['onclick'].split('\'')[1]
                img = 'http:' + tr.select_one('.cover > img')['src']
                title = tr.select_one('.title.ellipsis').get_text().split('\n')[-1].strip()
                artist = tr.select_one('.artist.ellipsis').string.strip()
                album = tr.select_one('.albumtitle.ellipsis').text.strip()
                lines.append({'rank':rank, 'title':title, 'artist':artist, 'album':album, 'img':img, 'href': href})
            except:
                pass 

    return lines


# 식신 맛집 찾기
def siksin_util(place):

    base_url = "https://www.siksinhot.com/search" 
    url = f'{base_url}?keywords={quote(place)}'
    try :
        result = requests.get(url)
    except:
        return []
    
    soup = BeautifulSoup(result.text, 'html.parser')

    lines = []
    try: 
        lis = soup.select_one('.localFood_list').find_all('li')

        for li in lis:
            href = li.select_one('a')['href']
            title = li.select_one('.textBox > h2').get_text()
            score  = li.select_one('.textBox > .score').get_text()
            location  = li.select('.cate > a')[0].get_text()
            menu = li.select('.cate > a')[1].get_text()
            img = li.find('img')['src']
            lines.append({'title':title, 'score':score, 'location': location, 'menu': menu, 'img':img, 'href':href } )
    except:
        pass

    return lines