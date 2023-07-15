from flask import current_app
import pandas as pd
import folium
import re, os

def get_citys():
    filename = os.path.join(current_app.static_folder, 'data/경기도공원전처리완료.csv')
    park = pd.read_csv(filename)
    citys = park.시군구.apply(lambda x: x.split('시')[0] + '시' if x.find('구') >= 0 else x).unique()
    citys.sort()
    return citys



def get_park_map(city_name, park) :
    tmp_park = park[park.시군구.str.contains(city_name)]
    if tmp_park.empty: return tmp_park.empty

    parkmap = folium.Map(location=[tmp_park.위도.mean(), tmp_park.경도.mean()], zoom_start=12)

    for i in tmp_park.index:
        folium.CircleMarker(
            location=[tmp_park.위도[i], tmp_park.경도[i]],
            radius=int(tmp_park['크기'][i]),
            # radius=300,
            tooltip=tmp_park.공원명[i],
            popup=folium.Popup(tmp_park.주소[i], max_width=200),
            color='green', 
            fill=True
        ).add_to(parkmap)
    title_html=f'<h3 align="center" style="font-size:20px;">{city_name} 공원 현황</h3>'
    parkmap.get_root().html.add_child(folium.Element(title_html))
    return parkmap


def show_kyonggi_park(city_name):
    filename = os.path.join(current_app.static_folder, 'data/경기도공원전처리완료.csv')
    park = pd.read_csv(filename)

    park_map = get_park_map(city_name, park)
    if park_map == True: 
        print("없는 도시입니다.")
        return False
        
    filename = os.path.join(current_app.static_folder, 'img/district/kyonggi_park.html')
    park_map.save(filename)

    mtime = int(os.stat(filename).st_mtime)   # 마지막으로 변경된 시간

    return mtime