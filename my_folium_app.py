# my_folium_app.py
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 엑셀 파일 로드
file_path = 'updated_DNA_with_y5_ratio___co_last.xlsx'  # 엑셀 파일 경로를 여기에 입력하세요
data = pd.read_excel(file_path, sheet_name='Sheet1')

# 날짜 데이터를 datetime 형식으로 변환
data['x72'] = pd.to_datetime(data['x72'], format='%m월%d일', errors='coerce')

# 사용자 입력: 날짜 선택
st.title("쌍촌동 5G Cov Hol 불량구간")
selected_date = st.date_input("날짜를 선택하세요", value=data['x72'].min())

# 선택한 날짜에 해당하는 데이터 필터링 (합계_y5_비율이 25 이상인 데이터만)
filtered_data = data[(data['x72'] == pd.to_datetime(selected_date)) & (data['합계_y5_비율'] >= 25)]

# 지도 생성
if not filtered_data.empty:
    center_lat = filtered_data['bld_lat'].mean()
    center_lon = filtered_data['bld_lon'].mean()
    map_visual = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # 데이터 추가
    for _, row in filtered_data.iterrows():
        folium.CircleMarker(
            location=(row['bld_lat'], row['bld_lon']),
            radius=5,
            color='green',
            fill=True,
            fill_opacity=0.7,
            tooltip=f'Ratio: {row["합계_y5_비율"]}%'
        ).add_to(map_visual)

    # Streamlit 페이지 설정
    st.write(f"선택한 날짜: {selected_date}")
    st_folium(map_visual, width=700, height=500)
else:
    st.write("선택한 날짜에 해당하는 데이터가 없습니다.")