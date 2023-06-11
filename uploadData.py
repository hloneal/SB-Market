from google.cloud import bigquery
import Extraction
import os
import json


def upload_data_to_bigquery():
    # Generate csv of data to push
    Extraction.data_csv()

    # Set the path to the credentials file
    credentials_path = 'credentials.json'  # Assuming credentials.json is in the same directory as the script

    # Check if the credentials file exists
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file '{credentials_path}' not found.")

    # Load the credentials JSON
    with open(credentials_path, 'r') as credentials_file:
        try:
            credentials_info = json.load(credentials_file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in credentials file: {str(e)}")

    # Create a BigQuery client with explicit credentials
    client = bigquery.Client.from_service_account_info(credentials_info)

    # Define the dataset and table
    dataset_id = 'Items'
    table_id = 'all'

    # Define the file path to the CSV data
    csv_file_path = 'market.csv'  # Assuming market.csv is in the same directory as the script

    # Define the BigQuery table reference
    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    # Load the CSV data into a BigQuery table
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
    )
    with open(csv_file_path, "rb") as file:
        job = client.load_table_from_file(file, table_ref, job_config=job_config)

    # Wait for the job to complete
    job.result()

    print(f"Data from '{csv_file_path}' has been successfully uploaded to BigQuery table '{table_ref}'.")


if __name__ == '__main__':
    # Call the function to upload the data
    upload_data_to_bigquery()
