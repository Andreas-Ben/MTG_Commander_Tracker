import streamlit as st
import pandas as pd
from streamlit_extras.bottom_container import bottom  # Importing the bottom container
from streamlit_extras.dataframe_explorer import dataframe_explorer
# Set the title and description of the app
st.set_page_config(page_title="MTG Commander Tracker", page_icon=":trophy:", layout="wide")
st.title('MTG Commander Tracker and Stats')
st.write("To keep your data between sessions you will need to download it as a CSV file and upload it again next time you use this app.")
st.write("Once you have entered data you can download via the button that shows up at the bottom of the page.")


# Example data
if st.checkbox('Show example data'):
    example_data = pd.DataFrame({
        'Commander': ['Vivi', 'Ragnar'],
#        'Color Combo': ['Red', 'Naya'],
 #       'Did you Start?': [False, True],
        'Did you Win?': [True, False],
        'Did you have Fun?': [True, False],
        'How many opponents': [1, 3],
#        'Date': ['2023-10-01', '2023-10-02'],
    })
    st.write(example_data)


# File uploader for CSV files
uploaded_file = st.file_uploader("Upload an CSV file", type=["csv"])

# Function to load data from a CSV file and add it to the cache
@st.cache_data(persist=True)
def load_data(file):
    data = pd.read_csv(file)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
  #  data['date'] = pd.to_datetime(data['date'], errors='coerce')
    return data

#Function to handle manual data entry being added to the cashe/dataframe
@st.cache_data(persist=True)
def manual_data_entry(commander, color_combo, did_you_start, did_you_win, did_you_have_fun, how_many_opponents, date):

    new_data = pd.DataFrame({
        'commander': [commander],
#        'color combo': [color_combo],
#        'did you start?': [did_you_start],
        'did you win?': [did_you_win],
        'did you have fun?': [did_you_have_fun],
        'how many opponents': [how_many_opponents],
#        'date': [pd.to_datetime(date)]
    })
    return new_data


data = pd.DataFrame()  # Initialize an empty DataFrame


if uploaded_file:
    data = load_data(uploaded_file)
    st.write("Data loaded successfully!")
col1, col2 = st.columns(2)
with col2:
    raw = st.checkbox('Show raw data')
if raw:        
    st.subheader('Raw data')
    if not data.empty:
        filtered_df = dataframe_explorer(data, case=False)
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.write("No data available.") 

with col1:
    manual = st.checkbox('Manual Data Entry')    
if manual:
    st.write("You can enter data manually here:")
    commander = st.selectbox("Commander", options=data, accept_new_options=True)
#    color_combo = st.text_input("Color Combo")
#    did_you_start = st.checkbox("Did you Start?")
    did_you_win = st.checkbox("Did you Win?")
    did_you_have_fun = st.checkbox("Did you have Fun?")
    how_many_opponents = st.slider("How many opponents", min_value=1, max_value=5, value=3)
#    date = st.date_input("Date")

    if st.button('Submit'):
        new_data = manual_data_entry(commander, '''color_combo''', '''did_you_start''', did_you_win, did_you_have_fun, how_many_opponents, '''date''')
        if data.empty:
            data = new_data
        else:
            data = pd.concat([data, new_data], ignore_index=True)
        st.write("Data added successfully!")
        st.write(data)

if data.empty:
    st.write("No data available. Please upload a file or enter data manually.")
else:
    winrate = data['did you win?'].mean() * 100
    funrate = data['did you have fun?'].mean() * 100
    opponents = data['how many opponents'].mean()

    statcol1, statcol2 = st.columns(2)
    with statcol1:
        st.write(f"Winrate: {winrate:.2f}% ({data['did you win?'].sum()} out of {len(data)})")
    with statcol2:
        st.write(f"Funrate: {funrate:.2f}% ({data['did you have fun?'].sum()} out of {len(data)})")
    st.write(f"Average number of opponents: {opponents:.2f}")

    st.subheader('Games played by each commander')
    commander_counts = data['commander'].value_counts()
    st.bar_chart(commander_counts, horizontal=True)

    st.subheader('Winrate by Commander')
    winrate_by_com = data.groupby('commander')['did you win?'].mean() * 100
    st.bar_chart(winrate_by_com, horizontal=True)

    st.subheader('Funrate by Commander')
    funrate_by_com = data.groupby('commander')['did you have fun?'].mean() * 100
    st.bar_chart(funrate_by_com, horizontal=True)

with bottom():
    botcol1, botcol2 = st.columns(2)
    with botcol2:
        if not data.empty:
            #output = BytesIO()
            csv = data.to_csv(index=False)
            st.download_button(
                label="Download Data as CSV file",
                data = csv,
                file_name= 'mtg_data.csv' ,
                mime='text/csv',
                use_container_width=True
            )
    with botcol1:
        st.link_button(
            label="Made with ❤️ by Benée",
            url="https://github.com/Andreas-Ben/MTG_Commander_Tracker",
            use_container_width=True,
            help="Click to visit the GitHub repository"
        )




