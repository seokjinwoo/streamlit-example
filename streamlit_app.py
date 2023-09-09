# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np  # 추가

""" 
재정정보원 자료를 이용한 국세진도율입니다. 
"""

plt.style.use('bmh')  # ggplot 스타일 사용

# matplotlib 기본 설정 변경
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Malgun Gothic']  # 'Malgun Gothic' 대신 다른 한글 지원 폰트를 사용할 수 있습니다.
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지



# Load the data
@st.cache_data
def load_data():
    return pd.read_excel('https://raw.githubusercontent.com/seokjinwoo/streamlit-example/master/income_data.xlsx')

df = load_data()

# Preprocessing
df['ISMOK_NM'] = df['ISMOK_NM'].str.strip()
df = df.rename(columns={
    'OJ_YY': 'year',
    'OJ_M': 'month',
    'ISMOK_NM': 'cat',
    'OUT_RT': 'pro'
})

# Title
st.title('세수 진도율 대시보드')

# Sidebar for category selection
selected_cat = st.sidebar.selectbox("세목 선택:", df['cat'].unique())

# Filter data based on selected category
filtered_data = df[df['cat'] == selected_cat]

# Scatter plot
st.write(f"{selected_cat} 산포도")
fig, ax = plt.subplots()
ax.scatter(np.array(filtered_data['month']), np.array(filtered_data['pro']), alpha=0.3, label='산포도')  # numpy 배열로 변환

# Plotting 2023 data with a noticeable color line
data_2023 = filtered_data[filtered_data['year'] == 2023]
ax.plot(np.array(data_2023['month']), np.array(data_2023['pro']), color='magenta', label='2023년')  # numpy 배열로 변환

# Plotting average 'pro' values for years before 2023 with dashed line
avg_pro_before_2023 = filtered_data[filtered_data['year'] <= 2022].groupby('month')['pro'].mean()
ax.plot(np.array(avg_pro_before_2023.index), np.array(avg_pro_before_2023.values), 'b--', label='2022년 전 평균')  # numpy 배열로 변환

ax.set_xlabel('')
ax.set_ylabel('세수 진도율(%)')
ax.set_title(f'{selected_cat}에 대한 세수진도율')
ax.legend()
st.pyplot(fig)
