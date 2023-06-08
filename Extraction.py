import requests
import csv

# API URL
url = 'https://api.hypixel.net/skyblock/bazaar'

# Make the API request
response = requests.get(url)
data = response.json()

# Extract data from the JSON response
products = data['products']

# Prepare CSV file
csv_file = 'market.csv'
fieldnames = ['product_id', 'buy_price', 'sell_price', 'last_updated']
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write data rows
    for product_id, product_data in products.items():
        buy_summary = product_data.get('buy_summary')
        sell_summary = product_data.get('sell_summary')
        last_updated = product_data['quick_status'].get('lastUpdated')

        if buy_summary and sell_summary:
            buy_price = buy_summary[0]['pricePerUnit']
            sell_price = sell_summary[0]['pricePerUnit']

            writer.writerow({
                'product_id': product_id,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'last_updated': last_updated
            })

print(f"Data has been successfully saved to '{csv_file}'.")
