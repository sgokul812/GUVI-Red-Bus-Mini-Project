import streamlit as st
import mysql.connector
import pandas as pd

def get_db_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="23569",
        database="red_bus"
    )
    return conn

st.title('Bus Information Filter')

# Fetch unique route names for filtering
conn = get_db_connection()
route_query = "SELECT DISTINCT route_name FROM bus_info WHERE route_name IS NOT NULL"
route_names = pd.read_sql(route_query, conn)
conn.close()

# Convert route names to a list for selection
route_names_list = route_names['route_name'].tolist()
route_names_list.insert(0, 'All')  # Add 'All' option

# Filter widgets
selected_route = st.selectbox('Route Name:', route_names_list)
bus_type = st.selectbox('Bus Type:', ['All', 'AC', 'NON-AC', 'NA'])  # Adjust bus types accordingly
min_price = st.number_input('Minimum Price:', min_value=0)
max_price = st.number_input('Maximum Price:', min_value=0)


if st.button('Filter'):
    conn = get_db_connection()
    query = "SELECT * FROM bus_info WHERE 1=1"

    if selected_route != 'All':
        query += f" AND route_name = '{selected_route}'"
    if bus_type != 'All':
        query += f" AND bus_type = '{bus_type}'"
    if min_price > 0:
        query += f" AND price >= {min_price}"
    if max_price > 0:
        query += f" AND price <= {max_price}"


    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No results found.")
