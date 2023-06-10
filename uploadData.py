from google.cloud import bigquery
import Extraction


def upload_data_to_bigquery(api_data):
    # Set the path to the credentials file
    credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

    # Create a BigQuery client with explicit credentials
    client = bigquery.Client.from_service_account_json(credentials_path)

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
    data = Extraction.get_market_data()
    upload_data_to_bigquery(data)
