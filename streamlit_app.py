import streamlit as st
import pandas as pd
from streamlit_extras.bottom_container import bottom
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Set the title and description of the app
st.set_page_config(page_title="MTG Commander Tracker", page_icon=":trophy:", layout="wide")
st.title('MTG Commander Tracker and Stats')
st.write("To keep your data between sessions you will need to download it as a CSV file and upload it again next time you use this app.")
st.write("Once you have entered data you can download via the button that shows up at the bottom of the page.")

# Initialize session state for data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame()

# File uploader for CSV files
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Function to load data from a CSV file
@st.cache_data(persist=True)
def load_data(file):
    data = pd.read_csv(file)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

if uploaded_file:
    st.session_state.data = load_data(uploaded_file)
    st.write("Data loaded successfully!")

col1, col2, col3 = st.columns(3)

with col2:
    raw = st.checkbox('Show raw data')

if raw:
    st.subheader('Raw data')
    if not st.session_state.data.empty:
        filtered_df = dataframe_explorer(st.session_state.data, case=False)
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.write("No data available.")

with col1:
    manual = st.checkbox('Manual Data Entry')

if manual:
    if st.session_state.data.empty:
        st.session_state.data = pd.DataFrame(columns=['commander', 'did you win?', 'did you have fun?', 'how many opponents'])
    st.write("You can enter data manually here:")
    commander = st.selectbox("Commander", options=st.session_state.data['commander'].unique(), accept_new_options=True)
    did_you_win = st.checkbox("Did you Win?")
    did_you_have_fun = st.checkbox("Did you have Fun?")
    how_many_opponents = st.slider("How many opponents", min_value=1, max_value=5, value=3)

    if st.button('Submit'):
        new_data = pd.DataFrame({
            'commander': [commander],
            'did you win?': [did_you_win],
            'did you have fun?': [did_you_have_fun],
            'how many opponents': [how_many_opponents],
        })

        if st.session_state.data.empty:
            st.session_state.data = new_data
        else:
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

        st.write("Data added successfully!")
        st.write(st.session_state.data)

with col3:
    exdata = st.checkbox('Show example data')

if exdata:
    example_data = pd.DataFrame({
        'Commander': ['Vivi', 'Ragnar'],
        'Did you Win?': [True, False],
        'Did you have Fun?': [True, False],
        'How many opponents': [1, 3],
    })
    st.write(example_data)

if st.session_state.data.empty:
    st.write("No data available. Please upload a file or enter data manually.")
else:
    winrate = st.session_state.data['did you win?'].mean() * 100
    funrate = st.session_state.data['did you have fun?'].mean() * 100
    opponents = st.session_state.data['how many opponents'].mean()

    statcol1, statcol2 = st.columns(2)
    with statcol1:
        st.write(f"Winrate: {winrate:.2f}% ({st.session_state.data['did you win?'].sum()} out of {len(st.session_state.data)})")
    with statcol2:
        st.write(f"Funrate: {funrate:.2f}% ({st.session_state.data['did you have fun?'].sum()} out of {len(st.session_state.data)})")
    st.write(f"Average number of opponents: {opponents:.2f}")

    st.subheader('Games played by each commander')
    commander_counts = st.session_state.data['commander'].value_counts()
    st.bar_chart(commander_counts, horizontal=True)

    st.subheader('Winrate by Commander')
    winrate_by_com = st.session_state.data.groupby('commander')['did you win?'].mean() * 100
    st.bar_chart(winrate_by_com, horizontal=True)

    st.subheader('Funrate by Commander')
    funrate_by_com = st.session_state.data.groupby('commander')['did you have fun?'].mean() * 100
    st.bar_chart(funrate_by_com, horizontal=True)

with bottom():
    botcol1, botcol2 = st.columns(2)
    with botcol2:
        if not st.session_state.data.empty:
            csv = st.session_state.data.to_csv(index=False)
            st.download_button(
                label="Download Data as CSV file",
                data=csv,
                file_name='mtg_data.csv',
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
