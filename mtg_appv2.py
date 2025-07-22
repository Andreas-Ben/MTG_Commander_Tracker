import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

st.title('MTG Commander Tracker and Stats')
if st.checkbox('Show example data'):
        example_data = pd.DataFrame({
            'Commander': ['Vivi', 'Ragnar'],
            'Color Combo': ['Red', 'Naya'],
            'Did you Start?': [False, True],
            'Did you Win?': [True, False],
            'Did you have Fun?': [True, False],
            'How many opponents': [1, 3],
            'Date' : ['2023-10-01', '2023-10-02'],
            })
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])
@st.cache_data
def load_data():
    if uploaded_file:
        data = pd.read_excel(uploaded_file, usecols="A:G")
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        st.write("Data loaded successfully!")
    else:
        st.write("Please upload an Excel file.")
    return data

data = load_data()

if raw_data := st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

if manualData := st.checkbox('Manual Data Entry'):
    st.write("You can enter data manually here:")
    commander = st.text_input("Commander")
    color_combo = st.text_input("Color Combo")
    did_you_start = st.checkbox("Did you Start?")
    did_you_win = st.checkbox("Did you Win?")
    did_you_have_fun = st.checkbox("Did you have Fun?")
    how_many_opponents = st.number_input("How many opponents", min_value=0, max_value=3, value=1)
    date = st.date_input("Date")

    
    if st.button('Submit'):
        new_data = pd.DataFrame({
            'commander': [commander],
            'color combo': [color_combo],
            'did you start?': [did_you_start],
            'did you win?': [did_you_win],
            'did you have fun?': [did_you_have_fun],
            'how many oponents': [how_many_opponents],
            'date': [date]
        })
        if data.empty:
            data = new_data
        else:
            data = pd.concat([data , new_data], ignore_index=True)
        st.write("Data added successfully!")
        st.write(data)



if data.empty:
    st.write("No data available. Please upload a file or enter data manually.")
else:
    winrate = data['did you win?'].mean() * 100
    funrate = data['did you have fun?'].mean() * 100
    opponents = data['how many oponents'].mean()

    st.write(f"Winrate: {winrate:.2f}%" , "(" + str(data['did you win?'].sum()) + " out of " + str(len(data)) + ")")
    st.write(f"Funrate: {funrate:.2f}%" , "(" + str(data['did you have fun?'].sum()) + " out of " + str(len(data)) + ")")
    st.write(f"Average number of opponents: {opponents:.2f}")


    st.subheader('Games played by each commander')
    # Example analysis: Count of games played by each commander
    commander_counts = data['commander'].value_counts()
    st.bar_chart(commander_counts, horizontal=True)
    st.subheader ('Winrate by Commander')
    # Example analysis: Winrate by color combo
    winrate_by_com = data.groupby('commander')['did you win?'].mean() * 100
    st.bar_chart(winrate_by_com, horizontal=True)
    st.subheader('Funrate by Commander')
    # Example analysis: Funrate by color combo
    funrate_by_com = data.groupby('commander')['did you have fun?'].mean() * 100
    st.bar_chart(funrate_by_com, horizontal=True)