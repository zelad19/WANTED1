
import sqlite3
import pandas as pd
import streamlit as st

# Connect to the database
def connect_db():
    return sqlite3.connect('job_portal.db')

# Query the database
def query_jobs(location='', domain='', sub_domain=''):
    conn = connect_db()
    query = "SELECT job_title, location, description, job_number, domain, sub_domain FROM jobs WHERE 1=1"
    params = []
    if location:
        query += " AND location LIKE ?"
        params.append(f"%{location}%")
    if domain:
        query += " AND domain LIKE ?"
        params.append(f"%{domain}%")
    if sub_domain:
        query += " AND sub_domain LIKE ?"
        params.append(f"%{sub_domain}%")
    
    df = pd.read_sql_query(query, conn, params)
    conn.close()
    return df

# Streamlit UI
st.title('פורטל דרושים')

# Filters
location = st.text_input('מיקום')
domain = st.text_input('תחום')
sub_domain = st.text_input('תת-תחום')

# Search button
if st.button('חפש'):
    jobs = query_jobs(location, domain, sub_domain)
    if not jobs.empty:
        st.write(f"נמצאו {len(jobs)} משרות:")
        st.dataframe(jobs)
    else:
        st.write("לא נמצאו משרות התואמות את החיפוש.")

# Display all jobs by default
else:
    st.write("מציג את כל המשרות:")
    all_jobs = query_jobs()
    st.dataframe(all_jobs)
