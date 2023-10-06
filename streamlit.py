import pandas as pd
import streamlit as st

st.title('Welcome to Reel Suggest')
df = pd.read_csv('temp.csv')
# st.dataframe(df.style.highlight_max(axis = 0))
x = st.slider('x')
st.write(x, 'squared is', x * x)

st.text_input("Your name", key = "name")
# st.session_state.name
st.session_state.name