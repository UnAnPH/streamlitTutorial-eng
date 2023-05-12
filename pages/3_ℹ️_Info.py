import streamlit as st

if __name__ == "__main__":
    st.title("ℹ️ About the :red[DB]")
    st.subheader("*Database of a scale model car dealer.*")

    col1, col2 = st.columns(2)
    col1.image("images/MySQL-Sample-Database-Schema.png")
    col2.markdown("### 🎯 :blue[Goal]: Create a simple dashboard that collects some of the company's key information.")
    col2.markdown("### 📁 :blue[DB]: This is a sample MySQL Database called *classicmodels* ")
    col2.markdown("### 🔬 :blue[Requirements]: Report an overview of products, staff and customers. Include an interface to add new products to the database.")
    col2.markdown("### 📊 :blue[Visualization]: Run SQL queries through *SQLAlchemy* and display results through :red[Streamlit] widgets.")

    st.markdown("🌐 For further information: https://www.mysqltutorial.org/mysql-sample-database.aspx")
