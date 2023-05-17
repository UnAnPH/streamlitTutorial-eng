import streamlit as st
from utils.utils import *
import pandas as pd
if __name__ == "__main__":
    st.title("💸 :blue[Reservations]")
    if check_connection():
        query="""WITH monthly_costs AS ( 
                    SELECT ROOM_CodR, EXTRACT(YEAR FROM STR_TO_DATE(StartDate, '%Y-%m-%d')) AS Year, EXTRACT(MONTH FROM STR_TO_DATE(StartDate, '%Y-%m-%d')) AS Month, 
                            Cost/(STR_TO_DATE(EndDate, '%Y-%m-%d') - STR_TO_DATE(StartDate, '%Y-%m-%d')) AS DailyCost 
                    FROM BOOKING 
                ), 
                grouped_monthly_costs AS ( 
                    SELECT Year, Month, ROOM_CodR, AVG(DailyCost) AS DailyAverage 
                    FROM monthly_costs 
                    GROUP BY Year, Month, ROOM_CodR 
                ), 
                max_monthly_costs AS ( 
                    SELECT Year, Month, MAX(DailyAverage) AS MaxDailyAverage 
                    FROM grouped_monthly_costs 
                    GROUP BY Year, Month 
                ) 
                SELECT gmc.Month, gmc.ROOM_CodR, r.Floor, r.SurfaceArea, r.Type, gmc.DailyAverage 
                FROM grouped_monthly_costs gmc 
                JOIN max_monthly_costs mmx ON gmc.Year = mmx.Year AND gmc.Month = mmx.Month AND gmc.DailyAverage = mmx.MaxDailyAverage 
                JOIN ROOM r ON r.CodR = gmc.ROOM_CodR;
            """
        result=execute_query(st.session_state["connection"],query)
        df=pd.DataFrame(result)
        col1,col2,col3=st.columns([2,3,2])
        col2.dataframe(df)
        st.line_chart(df,x="Month",y="DailyAverage")