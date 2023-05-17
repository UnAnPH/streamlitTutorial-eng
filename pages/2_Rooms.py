import streamlit as st
from utils.utils import *
import pandas as pd

def get_list(attribute,table):
    query=f"SELECT DISTINCT {attribute} FROM {table}"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attribute])
    return result_list

def map_amenity(amenity):
    query=""
    for element in amenity:
        query=query+(f" AND HAS_AMENITIES.AMENITIES_Amenity='{element}'")
    return query


if __name__ == "__main__":

    st.title("🛎 :blue[Rooms]")
    if check_connection():
        with st.expander("Filters",True):
            col1,col2,col3=st.columns(3)
            type=col1.radio("Room type",["Single","Double","Triple","Suite","All"])

            amenityList=get_list("AMENITIES_Amenity","HAS_AMENITIES")
            amenity=col2.multiselect("Amenity:",amenityList)
            kitchenFlag=col1.checkbox("I want the kitchen")
            
            amenityQuery=map_amenity(amenity)
            queryType=f"AND Type='{type.lower()}'" if type!='All' else ''
            #st.write(amenityQuery)
        if kitchenFlag:
            query=f"""SELECT CodR,Floor,SurfaceArea,Type,HAS_AMENITIES.AMENITIES_Amenity, HAS_SPACES.SPACES_Spaces
            FROM `ROOM`, `HAS_AMENITIES`,`HAS_SPACES`
            WHERE CodR=HAS_AMENITIES.ROOM_CodR AND CodR=HAS_SPACES.ROOM_CodR {queryType} {amenityQuery} AND HAS_SPACES.SPACES_Spaces='kitchen' 
            """
        else:
            query=f"""SELECT CodR,Floor,SurfaceArea,Type,HAS_AMENITIES.AMENITIES_Amenity
                FROM `ROOM`, `HAS_AMENITIES`
                WHERE CodR=HAS_AMENITIES.ROOM_CodR {queryType} {amenityQuery}
                """
        result=execute_query(st.session_state["connection"],query)
        df=pd.DataFrame(result)
        st.dataframe(df,use_container_width=True)

        #OPTIONAL
        with st.expander("Rooms"):
            if kitchenFlag:
                query=f"""SELECT DISTINCT CodR,Floor,Type
                FROM `ROOM`, `HAS_AMENITIES`,`HAS_SPACES`
                WHERE CodR=HAS_AMENITIES.ROOM_CodR AND CodR=HAS_SPACES.ROOM_CodR {queryType} {amenityQuery} AND HAS_SPACES.SPACES_Spaces='kitchen' 
                GROUP BY CodR
                """
            else:
                query=f"""SELECT DISTINCT CodR,Floor,Type
                    FROM `ROOM`, `HAS_AMENITIES`
                    WHERE CodR=HAS_AMENITIES.ROOM_CodR {queryType} {amenityQuery}
                    GROUP BY CodR
                    LIMIT 5;
                    """
            result=execute_query(st.session_state["connection"],query)
            df=pd.DataFrame(result)
            for index, row in df.iterrows():
                col1,col2=st.columns(2)
                col1.subheader(f":green[Result {index+1}]")
                col1.text(f"Room Code:{row['CodR']}")
                col1.text(f"Floor:{row['CodR']}")
                col1.text(f"Type:{row['Type']}")
                col2.image(f"images/{row['Type']}.png")

