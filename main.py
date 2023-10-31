# from pathlib import Path
#
# import streamlit as st
# from streamlit_multipage import MultiPage
#
# from pages import pages
#
#
# def landing_page(st):
#     st.markdown(Path("README.md").read_text())
#
#
# def header(st):
#     snippet = """
#     <div style="display: flex; justify-content: space-between">
#         <div>🡠 Check the sidebar for more apps</div>
#         <div><a href="https://github.com/ELC/finance-tools" target="_blank" style="text-decoration: none; color: goldenrod">Give it a ★ on Github</a></div>
#     </div>
#     """
#     st.markdown(snippet, unsafe_allow_html=True)
#
#
# def footer(st):
#     snippet = """
#     <div style="text-align: center; line-height: 2.5em;">
#         Developed using
#         <a href="https://streamlit.io/" target="_blank" style="text-decoration: none">streamlit</a>
#         by <a href="https://elc.github.io" target="_blank" style="text-decoration: none">Ezequiel Leonardo Castaño</a>
#         - Python Code available at <a href="https://github.com/ELC/finance-tools" target="_blank" style="text-decoration: none">Github</a>.
#         <br>
#         If you like the app, consider <a href="https://elc.github.io/donate" target="_blank" style="text-decoration: none">donating</a>.
#         <br>
#         For contact information, reach out by <a href="https://www.linkedin.com/in/ezequielcastano/" target="_blank" style="text-decoration: none">LinkedIn</a>
#     </div>
#     """
#     st.markdown(snippet, unsafe_allow_html=True)
#
#
# st.set_page_config(layout="wide")
#
# app = MultiPage()
# app.st = st
# app.navbar_name = "Other Apps"
# app.start_button = "Start App"
# app.navbar_style = "VerticalButton"
#
# app.header = header
# app.footer = footer
# app.hide_navigation = True
# app.hide_menu = True
#
# app.add_app("Landing", landing_page, initial_page=True)
#
# for name, function in pages.items():
#     app.add_app(name, function)
#
# app.run()

import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)