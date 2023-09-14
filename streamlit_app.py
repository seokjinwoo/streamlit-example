import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background-color: #f4f6f6;
    }
    .big-font {
        font-size:50px !important;
    }
    .small-font {
        font-size:16px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-font">국세 진도율에 대한 산포도</div>', unsafe_allow_html=True)
st.markdown('명지대 경제학과', unsafe_allow_html=True)

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

# Sidebar for category selection
selected_cat = st.sidebar.selectbox("세목:", df['cat'].unique())

# Filter data based on selected category
filtered_data = df[df['cat'] == selected_cat]

# Scatter plot
st.write(f"{selected_cat} Scattergram")
fig, ax = plt.subplots()
ax.scatter(np.array(filtered_data['month']), np.array(filtered_data['pro']), alpha=0.3, label='Scatterplot')

# Plotting 2023 data with a noticeable color line
data_2023 = filtered_data[filtered_data['year'] == 2023]
ax.plot(np.array(data_2023['month']), np.array(data_2023['pro']), color='magenta', label='2023')

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

st.markdown('<div class="small-font">재정정보원 자료를 이용한 국세진도율입니다. 총국세만 1-12월까지 데이터가 있고, 개별 세목은 1-11월까지만 데이터가 존재합니다. 데이터는 재정정보원 데이터가 업데이트 되면 같이 됩니다. 대략, 기재부 발표보다 1달 정도 후행합니다.</div>', unsafe_allow_html=True)
