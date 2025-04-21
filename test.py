import streamlit as st
import datetime

match_date = st.date_input("Select match date")

# Type and format
st.write("Type:", type(match_date))  # <class 'datetime.date'>
st.write("Date:", match_date)        # e.g., 2025-04-21
