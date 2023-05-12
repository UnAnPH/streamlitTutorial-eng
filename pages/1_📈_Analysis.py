import streamlit as st
from utils.utils import *
import pandas as pd


# each tab has a separate function

def create_products_tab(products_tab):
    col1, col2, col3 = products_tab.columns(3)
    payment_info = execute_query(st.session_state["connection"],
                                 "SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments;")
    # create a suitable data structure from the query result
    payment_info_dict = [dict(zip(payment_info.keys(), result)) for result in payment_info]
    # add selected parameters as horizontal metrics
    col1.metric('Total Amount', f"$ {compact_format(payment_info_dict[0]['Total Amount'])}")
    col2.metric('Max Payment', f"$ {compact_format(payment_info_dict[0]['Max Payment'])}")
    col3.metric('Average Payment', f"$ {compact_format(payment_info_dict[0]['Average Payment'])}")

    with products_tab.expander("Product Overview", True):
        # set the desired size, you can generate unused columns to define the spaces in a more pleasant way
        prod_col1, prod_col2, prod_col3 = st.columns([3, 3, 6])
        # query customization
        sort_param = prod_col1.radio("Sort by:", ["code", "name", "quantity", "price"])
        sort_choice = prod_col2.selectbox("Order:", ["Ascending", "Descending"])

        # dictionary for mapping SQL to options shown to the user
        sort_dict = {"Ascending": "ASC", "Descending": "DESC"}

        # the type of the button is purely for graphic taste
        if prod_col1.button("Show", type='primary'):
            # break the query into two strings to facilitate readability of the code: one fixed and the other that adapts to the options you choose
            query_base = "SELECT productCode AS 'code', productName AS 'name', quantityInStock AS quantity, buyPrice AS price, MSRP FROM products"
            query_sort = f"ORDER BY {sort_param} {sort_dict[sort_choice]};"
            products = execute_query(st.session_state["connection"], query_base + " " + query_sort)
            # automatic dataframe creation
            df_products = pd.DataFrame(products)
            st.dataframe(df_products, use_container_width=True)

    with products_tab.expander("Payments", True):
        # enable filtering by date range on which to build the query
        # first query to have the actual range of values in the database
        query = "SELECT MIN(paymentDate), MAX(paymentDate) FROM payments"
        date = execute_query(st.session_state["connection"], query)
        min_max = [dict(zip(date.keys(), result)) for result in date]

        # we know that only one tuple is returned to us
        min_value = min_max[0]['MIN(paymentDate)']
        max_value = min_max[0]['MAX(paymentDate)']
        # specify min_value and max_value to set the widget with the date range
        date_range = st.date_input("Select the date range:", value=(min_value, max_value), min_value=min_value,
                                   max_value=max_value)
        query = f"SELECT paymentDate, SUM(amount) as 'Total Amount' FROM payments WHERE paymentDate >'{date_range[0]}' AND paymentDate <'{date_range[1]}' GROUP BY paymentDate"
        paymentsDate = execute_query(st.session_state["connection"], query)
        df_paymentDate = pd.DataFrame(paymentsDate)

        # check that there is data in the selected period
        if df_paymentDate.empty:
            st.warning("No data found.", icon='⚠️')
        else:
            # transform to float and date type
            df_paymentDate['Total Amount'] = df_paymentDate['Total Amount'].astype(float)
            df_paymentDate['paymentDate'] = pd.to_datetime(df_paymentDate['paymentDate'])

            st.write("Period", date_range[0], '-', date_range[1])
            st.line_chart(df_paymentDate, x="paymentDate", y='Total Amount')


def create_staff_tab(staff_tab):
    # you can use mappings() and first() (expecting only one tuple) to get the desired data from the query result
    # find the name and surname of the president and VP Sales
    president_query = "SELECT lastName,firstName FROM employees WHERE jobTitle='President'"
    president = execute_query(st.session_state["connection"], president_query).mappings().first()
    vp_sales_query = "SELECT lastName,firstName FROM employees WHERE jobTitle='VP Sales'"
    vp_sales = execute_query(st.session_state["connection"], vp_sales_query).mappings().first()

    col1, col2, col3 = staff_tab.columns(3)
    col1.markdown(f"#### :blue[PRESIDENT:] {president['firstName']} {president['lastName']}")
    col3.markdown(f"#### :orange[VP SALES:] {vp_sales['firstName']} {vp_sales['lastName']}")

    # order not present in the bar chart
    staff_query = "SELECT jobTitle,COUNT(*) as numEmployees FROM employees GROUP BY jobTitle ORDER BY numEmployees DESC;"
    staff = execute_query(st.session_state["connection"], staff_query)
    df_staff = pd.DataFrame(staff)
    staff_tab.markdown("### Staff Members")
    # specify which columns in the dataframe should be the x or y axis
    staff_tab.bar_chart(df_staff, x='jobTitle', y='numEmployees', use_container_width=True)


def create_customers_tab(customers_tab):
    col1, col2 = customers_tab.columns(2)
    query = "SELECT COUNT(*) as 'customersNumber',country FROM customers GROUP by country order by `customersNumber` DESC;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    col1.subheader("Worldwide customers distribution")
    # set an equal height for the various elements can make the result more accurate
    col1.dataframe(df, use_container_width=True, height=350)

    query = "SELECT customername, state, creditLimit FROM customers WHERE country = 'USA' AND creditLimit > 100000 ORDER BY creditLimit DESC;"
    result = execute_query(st.session_state["connection"], query)
    df = pd.DataFrame(result)
    col2.subheader("Customers with higher *credit limit* in the USA")
    col2.dataframe(df, use_container_width=True, height=350)


if __name__ == "__main__":
    st.title("📈 Analysis")

    # creation of separate tabs
    products_tab, staff_tab, customers_tab = st.tabs(["Products", "Staff", "Customers"])

    # if the connection to the DB has been successful, show the data
    if check_connection():
        create_products_tab(products_tab=products_tab)
        create_staff_tab(staff_tab=staff_tab)
        create_customers_tab(customers_tab=customers_tab)
