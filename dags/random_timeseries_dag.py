import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import datetime, timedelta
from google.cloud import bigquery
import random
import string
from dotenv import load_dotenv

# Function to generate random timeseries data

load_dotenv()


def generate_random_timeseries_data():
    client = bigquery.Client()
    dataset_id = '1'
    table_id = '1'
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    rows_to_insert = []
    for _ in range(100):  # Generating 100 random records
        random_character = random.choice(string.ascii_uppercase)
        random_digit = random.randint(0, 9)
        rows_to_insert.append((random_character, random_digit))

    errors = client.insert_rows(table, rows_to_insert)
    if errors:
        print(f'Errors occurred: {errors}')
    else:
        print('Data inserted successfully.')

# Function to perform data aggregation


def aggregate_data():
    client = bigquery.Client()
    query = """
        SELECT 
            TIMESTAMP_TRUNC(event_timestamp, MINUTE) AS minute_timestamp,
            random_character,
            SUM(random_digit) AS sum_random_digit,
            MAX(random_digit) AS max_random_digit,
            COUNT(*) AS count
        FROM
            `your_project_id.your_dataset_id.your_table_id`
        GROUP BY
            minute_timestamp, random_character
    """
    query_job = client.query(query)
    results = query_job.result()
    for row in results:
        print(row)
        # Write to another BigQuery table here


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'random_timeseries_aggregation',
    default_args=default_args,
    description='DAG to aggregate random timeseries data',
    schedule_interval='*/5 * * * *',  # Run every 5 minutes
)

generate_data_task = PythonOperator(
    task_id='generate_random_timeseries_data',
    python_callable=generate_random_timeseries_data,
    dag=dag,
)

aggregate_data_task = PythonOperator(
    task_id='aggregate_data',
    python_callable=aggregate_data,
    dag=dag,
)

generate_data_task >> aggregate_data_task
