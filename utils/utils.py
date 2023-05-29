import streamlit as st
from sqlalchemy import create_engine,text

"""Collects the main functions shared by the various pages"""

def connect_db(dialect,username,password,host,dbname):
    try:
        engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")
        conn = engine.connect()
        return conn
    except:
        st.error("Unable to connect to database")
        return False
        
    
def execute_query(conn,query):
    return conn.execute(text(query))

def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"]= False
    
    if st.sidebar.button("Connect to the database"):
        myconnection = connect_db("mysql+pymysql","root","mypassword","localhost","classicmodels")
        if myconnection is not False:
            st.session_state["connection"]= myconnection
        else:
            st.session_state["connection"]= False
            st.sidebar.error("Unable to connect to database")
            
    if st.session_state["connection"]:
        st.sidebar.success("Connected to database")
        return True
    
def compact_num(number):
    if number < 1000:
        return number
    elif number < 1000000:
        return str(round(number/1000,1))+"K"
    elif number < 1000000000:
        return str(round(number/1000000,1))+"M"
    else:
        return str(round(number/1000000000,1))+"B"