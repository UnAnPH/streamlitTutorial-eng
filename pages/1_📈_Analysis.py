import streamlit as st
from utils.utils import *
import pandas as pd

# each tab has a separate function

if __name__ == "__main__":
    st.title("📈 Analysis")

    # creation of separate tabs
    products_tab, staff_tab, customers_tab = st.tabs(["Products", "Staff", "Customers"])
