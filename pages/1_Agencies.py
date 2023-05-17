import streamlit as st
from utils.utils import *
import pandas as pd

if __name__ == "__main__":
    st.title("🏢 :blue[Agencies]")
    col1, col2, col3 = st.columns(3)
    if check_connection():
        query = "SELECT COUNT(*) AS 'numAgencies' FROM TRAVEL_AGENCY;"
        agenzieN = execute_query(st.session_state["connection"], query)
        query = "SELECT COUNT(DISTINCT City_Address) AS numCities FROM `TRAVEL_AGENCY`;"
        agenzieCity = execute_query(st.session_state["connection"], query)
        query = "SELECT City_Address,COUNT(*) AS num FROM `TRAVEL_AGENCY` GROUP BY City_Address ORDER BY `num` DESC LIMIT 1;"
        city = execute_query(st.session_state["connection"], query)
        col1.metric("Number of Agencies", agenzieN.mappings().first()['numAgencies'])
        col2.metric("Number of Cities", agenzieCity.mappings().first()["numCities"])
        col3.metric("City with highest number of agencies", city.mappings().first()["City_Address"])

        query = "SELECT TRAVEL_AGENCY.City_Address,CITY.Latitude AS 'LAT', CITY.Longitude AS 'LON' FROM `TRAVEL_AGENCY`,CITY WHERE TRAVEL_AGENCY.City_Address=CITY.Name;"
        citygeo = execute_query(st.session_state["connection"], query)
        df_map = pd.DataFrame(citygeo)
        st.map(df_map)

        cityName = st.text_input("Filter by city")
        if cityName == '':
            query = "SELECT City_Address,CONCAT(Street_Address,' ',Num_Address) AS 'Address' FROM `TRAVEL_AGENCY`;"
        else:
            query = f"SELECT City_Address,CONCAT(Street_Address,' ',Num_Address) AS 'Address' FROM `TRAVEL_AGENCY` WHERE City_Address='{cityName}'"

        cityInfo = execute_query(st.session_state["connection"], query)
        df_info = pd.DataFrame(cityInfo)
        st.dataframe(df_info, use_container_width=True)
