# Live Coding Guide

>Step-by-step operations to complete the dashboard on the DB *classicmodels*

## Project presentation
* Folder ```images```
* Folder ```pages```
* Script utils ```utils/utils.py```
* File ```01_🏠_Home``` (homepage)

### Starting the project 
``` pip install pipenv```

```pipenv shell```

```pip install -r requirements.txt```

```python -m streamlit run 01_🏠_Home.py```

## Markdown and page customization
In the Home page:

1. Insert the page configuration
	```st.set_page_config()```
2. Split into columns ```st.columns([3,2])```
3. Insert headings and subheadings ```st.title()``` and ```st.markdown()```
4. (Optional) Customize the theme
5. Load the image ```st.image()```
6. Initialize the session state ```st.session_state["connection"]```

## Connecting to the Database
Define functions and commands to connect to the database.

1. Include functions ```connect_db(dialect,username,password,host,dbname)``` and ```execute_query(conn,query)``` in *utils*
2. Add the function ```check_connection()``` to *utils* and invoke it in the Home
3. Show the button on the sidebar

## Setup of the Analysis page
Define the structure of the page
1. Define tabs ```st.tabs(["Products","Staff","Customers"])```
2. Invoke the check with command to access the database through the button on the sidebar:
```
if check_connection():
	pass
```

### Product Visualization
Overview of the main information regarding the products on sale. Create the function ```create_products_tab(products_tab)```
and add it to *main*:
```
if check_connection():
    create_products_tab(products_tab=products_tab)
```

#### Metrics
Collect payment information: *Total Amount, Max Payment, Average Payment*.

SQL: ```SELECT SUM(amount) AS 'Total Amount', MAX(amount) AS 'Max Payment', AVG(amount) AS 'Average Payment' FROM payments:```

1. Add the function ```compact_format(num)``` to *utils* for a better visualization of large numbers.
2. Define 3 columns with ```products_tab.columns(3)```
3. For each column, define the specific metric with ```col.metric()```

#### Product Overview
View products for sale with query customization widgets about the *sorting*.
1. Define the first expander with the with notation and the flag `expanded=True` or `expanded=False` at will
```
with products_tab.expander("Product Overview",True):
	# Code
```
2. Define the columns within the expander with dimensions to improve the graphic rendering.
3. Define the dictionary for mapping *DESC* and *ASC*
3. Include the *radio button*, *select box*, and *button*
```
prod_col1.radio()
prod_col2.selectbox()
prod_col1.button():
```
4. Run the query and view the resulting dataframe

#### Payments
View the progress of payments with time filter.

1. Define the second expander with notation
```
with products_tab.expander("Payments",True):
	# Code
```
2. Run the query to define the time extremes. SQL: ```SELECT MIN(paymentDate), MAX(paymentDate) FROM payments```
3. Define the widget for selecting dates, passing as default values the tuple ```(min_value,max_value)``` and the maximum and minimum allowed values
```
st.date_input("Select date range:",value=(min_value,max_value),
	min_value=min_value,max_value=max_value)
```
4. Run the query with date filtering and create the dataframe
5. heck if the datafame is empty and handle any errors
```
st.warning("No data found.",icon='⚠️')
```
6. Change the data type for *paymentDate* and *Total Amount*
7. Plot the result
```
st.line_chart(df_paymentDate,x="paymentDate",y='Total Amount')
```

### Staff
Briefly view employee information. Create the function ```create_products_tab(products_tab)```
and add it to *main*:
```
if check_connection():
    create_products_tab(products_tab=products_tab)
    create_staff_tab(staff_tab=staff_tab)
```
1. Retrieve the first and last name of *President* and *VP Sales*. SQL: 
```
SELECT lastName,firstName FROM employees WHERE jobTitle='President'

SELECT lastName,firstName FROM employees WHERE jobTitle='VP Sales'
```
2. Customize markdown
3. Retrieve information about the distribution of employees in different roles. SQL: ```SELECT jobTitle, COUNT(*) as numEmployees FROM employees GROUP by jobTitle order by numEmployees DESC;```

4. Generate the dataframe and plot the result:
```
df_staff=pd.DataFrame(staff)
staff_tab.bar_chart(df_staff,x='jobTitle',y='customersNumber',use_container_width=True)
```

### Customers
Briefly view customer information in relation to country of origin.
Create the function ```create_customers_tab(products_tab)```
and add it to *main*:
```
if check_connection():
    create_products_tab(products_tab=products_tab)
    create_staff_tab(staff_tab=staff_tab)
    create_customers_tab(customers_tab=customers_tab)
```
1. Create columns on the customers tab ```col1,col2=customers_tab.columns(2)```
2. Use the subheader to specify the role of each column
 ```
col1.subheader("Worldwide customers distribution")
col2.subheader("Customers with higher *credit limit* in the USA")
 ```
 3. Retrieve customer origin information sorting them by number. SQL:```
 	SELECT COUNT(*) as 'customersNumber',country FROM customers GROUP by country order by 'customersNumber' DESC;```
 4. Retrieve customer information **USA** with **creditLimit > 100000** sorting them in descending order. (N.B. these values may be additional user input in the future)
5. Set an identical height for the two df and display them
```
col1.dataframe(df,use_container_width=True,height=350)
col2.dataframe(df,use_container_width=True,height=350)
```


## Add a product
Create a form to add a new product to the DB.
### Creating the form
Create the function ```create_form()``` and invoke it in the main
```
if check_connection():
	create_form()
```
Include the form widget to which you want to add the various parameters:
```
with st.form("New Product"):
	st.header(":blue[Add product:]")
```
Create functions ```get_info()``` and ```get_list(attribute)``` which retrieve all possible distinct values for a given attribute and return them as a list. Get the list of *categories, scales, vendors* within the form to create the options to choose from.
#### Input widget
Insert widgets to receive as input *code, name, category, scale, vendor, description, quantity, price, MSRP* using:
```
st.text_input("",placeholder="")
st.selectbox("",)
st.text_area("",placeholder="")
st.slider("",,)
st.number_input("",)
```
Create a dictionary that collects the parameters and **include the submit button**:
```
insert_dict= {"productCode":code, "productName":name,"productLine":category,"productScale":scale,"productVendor":vendor,"productDescription":description,"quantityInStock":quantity,"buyPrice":price,"MSRP":msrp}
submitted =st.form_submit_button("Submit",type='primary')
```
#### Execute the *insert*
Define the function ```insert(prod_dict)``` which takes care of executing the query and the function ```check_info(prod_dict)``` to check that there are no text fields left blank.

#### Check that the insertion was successful

Outside the form, verify that, when the *submit* button is pressed, it was possible to complete the operation successfully and print the status:
```
 if submitted:
        #check that the insertion was successful or not
        if insert(insert_dict):
            st.success("You have added this product: ",icon='✅ ')
            st.write(insert_dict)
        else:
            st.error("Unable to add product.",icon='⚠️')
```

