# Data-Pipelines-with-Neo4j-Project
Week 8 Project on Data Pipelines with Neo4j


## Data Pipeline ETL with Neo4j
The pipeline extracts customer subscription data from a Neo4j graph database, transforms it using Pandas, and loads it into a Postgres database.

## Requirements.
Neo4j database 

Python 3.x

Python libraries: neo4j, pandas, psycopg2

## Process setup.
Install the required Python libraries using pip install -r requirements.txt
Set up your Neo4j connection details in the neo4j_uri, neo4j_user, and neo4j_password variables in etl.py.
Set up your Postgres connection details in the host, database, user, and password parameters in the psycopg2.connect() method call in the load_data() function in etl.py.
## Data Schema
The extracted data contains information about customer subscriptions to various services.

These will include:

customer ID

Subscription ID

Service ID

start date

end date

price

Service name

The transformed data will add a new column for the duration of the subscription in days.

## Transformations
The transform_data() function performs the following transformations on the extracted data:

Converts the start_date and end_date columns to datetime format Removes rows where start_date or end_date is missing Drops all NaN values Adds a new column for the duration of the subscription in days

## Running the pipeline

When running the data pipeline, execute the .py file using Python:

The program extracts the data from Neo4j, transforms it, and then loads it into Postgres database.

When the data is successfully loaded into Postgres, the program will log a success message. If there is an error during any of the steps, an error message will be logged.
