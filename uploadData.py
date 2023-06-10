from google.cloud import bigquery
import Extraction
import os
import json


def upload_data_to_bigquery():

    api_data = Extraction.get_market_data()

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

    # Retrieve the existing table schema
    table = client.get_table(f"{client.project}.{dataset_id}.{table_id}")
    schema = table.schema

    # Insert the new data into the table
    client.insert_rows(table, api_data, selected_fields=schema)


if __name__ == '__main__':
    # Call the function to upload the data
    upload_data_to_bigquery()
