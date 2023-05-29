import streamlit as st
from utils.utils import *
import pandas as pd

# each tab has a separate function


def create_products_tab(products_tab):
    col1, col2, col3 = products_tab.columns(3)
    
    payment_info = execute_query(st.session_state["connection"],
                                 "SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments")
    
    payment_infos = [dict(zip(payment_info.keys(), result)) for result in payment_info]
    
    col1.metric("Total Amount", compact_num(payment_infos[0]["Total Amount"]))
    col2.metric("Max Payment", compact_num(payment_infos[0]["Max Payment"]))
    col3.metric("Average Payment", compact_num(payment_infos[0]["Average Payment"]))
    
    with products_tab.expander("Product Overview",True):
        prod_col1, prod_col2, prod_col3 = products_tab.columns(3)
        sort_param = prod_col1.radio("Sort by", ["code", "name", "quantity", "price"])
        sort_choice = prod_col2.selectbox("Order", ["ASC", "DESC"])
        
        if prod_col1.button("Show", type = "primary"):
            query = f"SELECT productCode AS 'code', productName AS 'name', quantityInStock AS quantity, buyPrice AS price, MSRP FROM products ORDER BY {sort_param} {sort_choice}"
            products = execute_query(st.session_state["connection"], query)
            df_products = pd.DataFrame(products, columns = products.keys())
            st.dataframe(df_products)
    return

if __name__ == "__main__":
    st.title("📈 Analysis")

    # creation of separate tabs
    products_tab, staff_tab, customers_tab = st.tabs(["Products", "Staff", "Customers"])

    if check_connection():
        create_products_tab(products_tab)
 
