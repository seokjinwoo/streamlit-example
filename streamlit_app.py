# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # 추가

plt.style.use('bmh')  # ggplot 스타일 사용
plt.rc('font', family='NanumGothic')  # For Windows


"""
# 국세 진도율 대쉬보드에 오신 것을 환영합니다. 

한국재정정보원의 국세 진도율 자료를 이용하여 2023년의 국세 진도율을 시각화 하여 보여주고 있습니다. 

"""


import pandas as pd
import requests
import xml.etree.ElementTree as ET

url = 'https://openapi.openfiscaldata.go.kr/IncomeTax'
key = ""

years = [str(year) for year in range(2014, 2024)]

df_list = []

for year in years:
    params = {
        'Type': 'xml',
        'pIndex': '1',
        'pSize': '100',
        'OJ_YY': year,
        'Key': key
    }

    response = requests.get(url, params=params)
    root = ET.fromstring(response.text)

    for item in root.findall('.//row'):
        data = {elem.tag: elem.text for elem in item}
        df_list.append(data)

df = pd.DataFrame(df_list)

# Remove white spaces in the "ISMOK_NM" column
df['ISMOK_NM'] = df['ISMOK_NM'].str.strip()

# Export DataFrame to Excel
output_file = "income_data.xlsx"
df.to_excel(output_file, index=False)

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel('income_data.xlsx')

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




