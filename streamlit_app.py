import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="국세 진도율 산포도",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Load the data
@st.cache
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

# Title and Subtitle
st.title('국세 진도율에 대한 산포도')
st.subheader('중요한경제문제연구소')

# Category selection below the title
selected_cat = st.selectbox("세목 선택:", df['cat'].unique())

# Filter data based on selected category
filtered_data = df[df['cat'] == selected_cat]

# Scatter plot
st.write(f"{selected_cat} Scattergram")
fig, ax = plt.subplots()
ax.scatter(np.array(filtered_data['month']), np.array(filtered_data['pro']), alpha=0.5, color='#0077B6', label='Scatterplot')

# Plotting 2023 data with a noticeable color line
data_2023 = filtered_data[filtered_data['year'] == 2023]
ax.plot(np.array(data_2023['month']), np.array(data_2023['pro']), color='#FF6347', label='2023')

# Plotting average 'pro' values for years before 2023 with dashed line
avg_pro_before_2023 = filtered_data[filtered_data['year'] <= 2022].groupby('month')['pro'].mean()
ax.plot(np.array(avg_pro_before_2023.index), np.array(avg_pro_before_2023.values), 'b--', label='Average (2014-2022)')

# Setting x-axis labels with abbreviated month names
months_abbrev = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
ax.set_xticks(range(1, 13))
ax.set_xticklabels(months_abbrev, rotation=45)

ax.set_xlabel('')
ax.set_ylabel('Revenue progress rate (%)')
ax.legend()
st.pyplot(fig)

st.markdown(""" 
재정정보원 자료를 이용한 국세진도율입니다. 
총국세만 1-12월까지 데이터가 있고, 개별 세목은 1-11월까지만 데이터가 존재합니다. 
데이터는 재정정보원 데이터가 업데이트 되면 같이 됩니다. 대략, 기재부 발표보다 1달 정도 후행합니다. 
""")
