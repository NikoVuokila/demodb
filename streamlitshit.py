import streamlit as st
import pandas as pd

@st.cache_data
def get_data():
    df = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/refs/heads/master/titanic.csv")
    st.write("import done")
    return df

df = get_data()

st.dataframe(df.head(5))

option = st.selectbox("Select column", ("survived", "sex", "class"))

selected = df[option].value_counts()

st.write(option)
st.bar_chart(selected, horizontal=True)

# st.line_chart(df[["fare"]])