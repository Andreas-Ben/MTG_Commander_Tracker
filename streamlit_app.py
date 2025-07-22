import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
st.title('Test Streamlit App')

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is None:
    st.write("Please upload a CSV file.")
else:
    data = pd.read_csv(uploaded_file, delimiter=';')
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    st.write("Data loaded successfully!")


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


