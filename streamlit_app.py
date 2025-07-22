import streamlit as st
import pandas as pd
import numpy as np
import openpyxl
#import streamlit_pandas as sp

st.title('Test Streamlit App')
uploaded_file = st.file_uploader("Upload a excel file", type=["xlsx", "xls"])

if uploaded_file is None:
    st.write("Please upload a Excel file.")
    if st.checkbox('Show example data'):
        example_data = pd.DataFrame({
            'Commander': ['Vivi', 'Ragnar'],
            'Color Combo': ['Red', 'Naya'],
            'Did you Start?': [False, True],
            'Did you Win?=': [True, False],
            'Did you have Fun?': [True, False],
            'How many oponents': [1, 3],
        })
        st.write(example_data)
else:
    data = pd.read_excel(uploaded_file, usecols="A:F")
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    st.write("Data loaded successfully!")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

st.subheader('Overall Winrate, Funrate and Opponents')
if uploaded_file is None:
    st.write("Please upload a file to see the statistics.")
else:
    winrate = data['did you win?='].mean() * 100
    funrate = data['did you have fun?'].mean() * 100
    opponents = data['how many oponents'].mean()

    st.write(f"Winrate: {winrate:.2f}%")
    st.write(f"Funrate: {funrate:.2f}%")
    st.write(f"Average number of opponents: {opponents:.2f}")