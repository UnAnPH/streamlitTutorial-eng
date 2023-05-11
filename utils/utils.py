import streamlit as st
from sqlalchemy import create_engine,text

"""Collects the main functions shared by the various pages"""

#Connect to the engine
def connect_db(dialect,username,password,host,dbname):
    try:
        engine=create_engine(f'{dialect}://{username}:{password}@{host}/{dbname}')
        conn=engine.connect()
        return conn
    except:
        return False

def execute_query(conn,query):
    return conn.execute(text(query))

#Show numbers in a more compact form
def compact_format(num):
    num=float(num)
    if abs(num) >= 1e9:
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)

#Check if the connection to the db has been made
def check_connection():
    if "connection" not in st.session_state.keys():
        st.session_state["connection"]=False

    if st.sidebar.button("Connect to the Database"):
        myconnection=connect_db(dialect="mysql+pymysql",username="root",password="mypassword",host="localhost",dbname="classicmodels")
        if myconnection is not False:
            st.session_state["connection"]=myconnection

        else:
            st.session_state["connection"]=False
            st.sidebar.error("Error connecting to DB")

    if st.session_state["connection"]:
        st.sidebar.success("Connected to DB")
        return True

