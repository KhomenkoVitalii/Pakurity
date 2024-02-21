from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from google.cloud import storage, bigquery
import re

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 20),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'parse_text_files_and_store_in_bigquery',
    default_args=default_args,
    description='A DAG to parse text files and store data in BigQuery',
    schedule_interval=timedelta(days=1),
)


def parse_text_files_and_store_in_bigquery():
    """
    Task to parse text files from GCS and store data in BigQuery.
    """
    gcs_client = storage.Client()
    bq_client = bigquery.Client()

    bucket_name = 'my-gcs-bucket'
    prefix = 'data/'

    # Regular expression pattern for parsing the text files
    # that matches IP addresses
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    # Fetch the list of files from GCS
    bucket = gcs_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        # Download the file contents
        content = blob.download_as_string().decode('utf-8')

        # Parse the content
        parsed_data = re.findall(pattern, content)

        # Insert the parsed data into BigQuery
        table_ref = bq_client.dataset('main').table('ip_addresses')
        table = bq_client.get_table(table_ref)
        errors = bq_client.insert_rows(table, parsed_data)

        if errors:
            raise Exception(
                f'Errors occurred while inserting rows into BigQuery: {errors}')


# Define the PythonOperator to execute the parsing and storing task
parse_and_store_task = PythonOperator(
    task_id='parse_and_store_task',
    python_callable=parse_text_files_and_store_in_bigquery,
    dag=dag,
)
