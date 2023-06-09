# -*- coding: utf-8 -*-
"""Project Assignment on Data Pipelines with Neo4j Week8_GMumbo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cH9wTQaPyya9cIcTCe8jLQZe9PHKmrB9
"""

!pip install neo4j

# Import required libraries
from neo4j import GraphDatabase
import pandas as pd
import psycopg2
from datetime import datetime
import logging

# connection details
neo4j_uri = "neo4j+s://165aa35c.databases.neo4j.io"
neo4j_user = "neo4j"
neo4j_password = "j6m_KaXq4DSNfZTbLUvxfqldPdVUdT4ysEnd1XnL694"

# query to extract data
neo4j_query = """
MATCH (c:Customer)-[:HAS_SUBSCRIPTION]->(s:Subscription)-[:USES]->(sr:Service)
RETURN c.customer_id, s.subscription_id, sr.service_id, s.start_date, s.end_date, s.price
"""

# function to extract data from Neo4j and return a Pandas DataFrame
def extract_data():
    # Connect to Neo4j
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    # Define a Cypher query to retrieve the data
    query = """
    MATCH (c:Customer)-[s:SUBSCRIBES_TO]->(sv:Service)
    RETURN c.id AS customer_id, s.start_date AS start_date, s.end_date AS end_date, s.price AS price,
          sv.id AS service_id, sv.name AS service_name
    """

    # Execute the query and retrieve the data
    with driver.session() as session:
        results = session.run(query)
        data = [dict(row) for row in results]

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)
    return df

# function to transform data
def transform_data(df):
    # Convert start_date and end_date columns to datetime format
    df['start_date'] = df['start_date'].apply(lambda x: datetime.fromisoformat(str(x)))
    df['end_date'] = df['end_date'].apply(lambda x: datetime.fromisoformat(str(x)) if x else pd.NaT)
    
    # Remove rows where start_date or end_date is NaT
    df = df.dropna(subset=['start_date', 'end_date'], how='any')

    #drop all NaN values
    df.dropna(inplace=True)

    # Create a new column for the duration of the service in days
    df['duration_days'] = (df['end_date'] - df['start_date']).dt.days
    
    return df

# function to load data into Postgres

def load_data(df):
    try:
        conn = psycopg2.connect(
            host = "34.170.193.146",
            database = "RwandaMTNDB",
            user = "admin",
            password = "admin1"
        )
        cursor = conn.cursor()

        # create table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS customer_service (
                            customer_id TEXT,
                            start_date DATE,
                            end_date DATE,
                            price FLOAT,
                            service_id TEXT,
                            service_name TEXT,
                            duration_days INT
                        )''')

        # insert data into table
        for index, row in df.iterrows():
            cursor.execute('''INSERT INTO customer_service (customer_id, start_date, end_date, price, service_id, service_name, duration_days)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''', (row['customer_id'], row['start_date'], row['end_date'], row['price'], row['service_id'], row['service_name'], row['duration_days']))

        conn.commit()
        cursor.close()
        conn.close()
        logging.info('Data loaded successfully into Postgres.')
    except Exception as e:
        logging.error(f'Error while loading data into Postgres: {e}')

# define main function
def main():
    # Extract data from Neo4j
    df = extract_data()
    
    # Transform data using Pandas
    transformed_df = transform_data(df)
   
    # Load data into Postgres
    load_data(transformed_df)

# Call main function
if __name__ == "__main__":
    main()