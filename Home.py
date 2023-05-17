import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *

if __name__ == "__main__":
    st.set_page_config(
        page_title="My App",
		layout="wide",
		initial_sidebar_state="expanded",
		menu_items={
			'Get Help': 'https://dbdmg.polito.it/',
			'Report a bug': "https://dbdmg.polito.it/",
			'About': "# *Introduction to Databases* course"
		}
    )
    st.title("📈 Hotel Rooms Management")

    if "connection" not in st.session_state.keys():
        st.session_state["connection"]=False

    check_connection()
