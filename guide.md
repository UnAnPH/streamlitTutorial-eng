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
3. Insert headings and subheadings ```st.title()``` e ```st.markdown()```
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
3. Per ogni colonna definire la metrica specifica con ```col.metric()```

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

1. Definire il secondo expander con la with notation
```
with tab_prodotti.expander("Pagamenti",True):
	# Codice
```
2. Eseguire la query per definire gli estremi temporali. SQL: ```SELECT MIN(paymentDate), MAX(paymentDate) FROM payments```
3. Definire il widget per la selezione delle date, passando come valori di default la tupla ```(min_value,max_value)``` e i valori di massimo e minimo consentiti
```
st.date_input("Seleziona il range di date:",value=(min_value,max_value),
	min_value=min_value,max_value=max_value)
```
4. Eseguire la query con filtraggio delle date e create il dataframe
5. Verificare se il datafame è vuoto e gestire eventuali errori
```
st.warning("Nessun dato trovato.",icon='⚠️')
```
6. Modificare il tipo di dato per *paymentDate* e *Total Amount*
7. Fare il plot del risultato
```
st.line_chart(df_paymentDate,x="paymentDate",y='Total Amount')
```

### Staff
Visualizzare brevemente informazioni sui dipendenti. Creare la funzione ```create_tab_prodotti(tab_prodotti)```
e aggiungerla al *main*:
```
if check_connection():
    create_tab_prodotti(tab_prodotti=tab_prodotti)
    create_tab_staff(tab_staff=tab_staff)
```
1. Recuperare il nome e cognome di *President* e *VP Sales*. SQL: 
```
SELECT lastName,firstName FROM employees WHERE jobTitle='President'

SELECT lastName,firstName FROM employees WHERE jobTitle='VP Sales'
```
2. Personalizzare il markdown
3. Recuperare le informazioni riguardo la distribuzione dei dipendenti nei vari ruoli. SQL: ```SELECT COUNT(*) as 'numeroClienti',country FROM customers GROUP by country order by `numeroClienti` DESC;```

4. Generare il dataframe e plottare il risultato:
```
df_staff=pd.DataFrame(staff)
tab_staff.bar_chart(df_staff,x='jobTitle',y='numDipendenti',use_container_width=True)
```

### Clienti
Visualizzare brevemente le informazioni sui clienti in relazione al paese di origine.
Creare la funzione ```create_tab_clienti(tab_prodotti)```
e aggiungerla al *main*:
```
if check_connection():
    create_tab_prodotti(tab_prodotti=tab_prodotti)
    create_tab_staff(tab_staff=tab_staff)
    create_tab_clienti(tab_clienti=tab_clienti)
```
1. Creare le colonne nel tab clienti ```col1,col2=tab_clienti.columns(2)```
2. Utilizzare il subheader per specificare il ruolo di ogni colonna
 ```
col1.subheader("Distribuzione clienti nel mondo")
col2.subheader("Clienti con maggior *credit limit* negli USA")
 ```
 3. Recuperare le informazioni sull'origine dei clienti ordinandoli per numero. SQL:```
 	SELECT COUNT(*) as 'numeroClienti',country FROM customers GROUP by country order by ``numeroClienti` DESC;```
 4. Recuperare le informazioni sui clienti **USA** con **creditLimit > 100000** ordinandoli in ordine decrescente. (N.B. questi valori potrebbero essere ulteriori input dell'utente in futuro)
5. Impostare un'altezza identica per i due df e visualizzarli
```
col1.dataframe(df,use_container_width=True,height=350)
col2.dataframe(df,use_container_width=True,height=350)
```


## Aggiungere un prodotto
Creare un form per aggiungere un nuovo prodotto al DB.
### Creazione del form
Creare la funzione ```create_form()``` e richiamarla nel main 
```
if check_connection():
	create_form()
```
Includere il widget del form a cui aggiungere i vari parametri:
```
with st.form("Nuovo Prodotto"):
	st.header(":blue[Aggiungi prodotto:]")
```
Creare le funzioni ```get_info()``` e ```get_list(attributo)``` che recuperano tutti i valori distinti possibili per un dato attributo e li restituisce come lista. Ottenere così la lista di *categorie, scale, venditori* all'interno del form per creare le opzioni tra cui scegliere. 
#### Widget di input
Inserire i widget per ricevere come input *code, nome,categoria,scala,venditore,descerizione,quantità,prezzo,MSRP* utilizzando:
```
st.text_input("",placeholder="")
st.selectbox("",)
st.text_area("",placeholder="")
st.slider("",,)
st.number_input("",)
```
Creare il dizionario che raccolga i parametri e **includere il submit button**:
```
insert_dict= {"productCode":code, "productName":nome,"productLine":categoria,"productScale":scala,"productVendor":venditore,"productDescription":descrizione,"quantityInStock":qta,"buyPrice":prezzo,"MSRP":msrp}
submitted =st.form_submit_button("Submit",type='primary')
```
#### Eseguire l'*insert*
Definire la funzione ```insert(prod_dict)``` che si occupa di eseguire la query e la funzione ```check_info(prod_dict)``` per controllare che non ci siano campi testuali lasciati vuoti.

#### Verifica che l'inserimento sia andato a buon fine

Fuori dal form verificare che, quando il tasto *submit* viene premuto, sia stato possibile completare l'operazione con successo e printare lo status:
```
 if submitted:
        #verificare che l'inserimento sia andato a buon fine oppure no
        if insert(insert_dict):
            st.success("Hai inserito questo prodotto: ",icon='✅ ')
            st.write(insert_dict)
        else:
            st.error("Impossibile aggiungere il prodotto.",icon='⚠️')
```

