import streamlit as st
from utils.utils import *

#basic query to retrieve all distinct values that an attribute can have
#used to create the list of options to choose from
def get_list(attribute):
    query=f"SELECT DISTINCT {attribute} FROM products"
    result=execute_query(st.session_state["connection"],query)
    result_list=[]
    for row in result.mappings():
        result_list.append(row[attribute])
    return result_list

def get_info():
    return get_list("productLine"),get_list("productScale"),get_list("productVendor")

#check if all text fields have been filled
def check_info(prod_dict):
    for value in prod_dict.values():
        if value=='':
            return False
    return True

#insert the new product
def insert(prod_dict):
    if check_info(prod_dict):
        attributes=", ".join(prod_dict.keys())
        values=tuple(prod_dict.values())
        query=f"INSERT INTO products ({attributes}) VALUES {values};"
        #try-except to verify that the MySQL operation was successful generate an error otherwise
        try:
            execute_query(st.session_state["connection"],query)
            st.session_state["connection"].commit()
        except Exception as e:
            st.error(e)
            return False
        return True
    else:
        return False

def create_form():
    with st.form("New Product"):
        st.header(":blue[Add product:]")

        #parameters
        categories,scales,vendors=get_info()
        code=st.text_input("Product code",placeholder="S**_****")
        name=st.text_input("Product name",placeholder="Enter the name of the product")
        category=st.selectbox("Category",categories)
        scale=st.selectbox("Product scale",scales)
        vendor=st.selectbox("Vendor",vendors)
        description=st.text_area("Description",placeholder="Enter the description of the product")
        quantity=st.slider("Quantity",0,10000)
        price=st.number_input("Price",1.00)
        msrp=st.number_input("MSRP")

        #final dictionary with all parameters
        insert_dict= {"productCode":code, "productName":name,"productLine":category,"productScale":scale,"productVendor":vendor,"productDescription":description,"quantityInStock":quantity,"buyPrice":price,"MSRP":msrp}
        
        #submit button fundamental for the form
        submitted =st.form_submit_button("Submit",type='primary')
    
    if submitted:
        #check that the insertion was successful or not
        if insert(insert_dict):
            st.success("You have added this product: ",icon='✅ ')
            st.write(insert_dict)
        else:
            st.error("Unable to add product.",icon='⚠️')
 

if __name__ == "__main__":
    st.title("🖊 Add")
    if check_connection():
        create_form()