import requests
import csv

# API URL
url = 'https://api.hypixel.net/skyblock/bazaar'

# Make the API request
response = requests.get(url)
data = response.json()

# Extract data from the JSON response
products = data['products']

# Get the last updated timestamp
last_updated = data['lastUpdated']

# Prepare CSV file
csv_file = 'market.csv'
fieldnames = ['product_id', 'buy_price', 'sell_price', 'last_updated', 'sell_volume', 'buy_volume', 'sell_orders', 'buy_orders']
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write data rows
    for product_id, product_data in products.items():
        buy_summary = product_data.get('buy_summary')
        sell_summary = product_data.get('sell_summary')
        quick_status = product_data.get('quick_status')

        if buy_summary and sell_summary and quick_status:
            buy_price = buy_summary[0]['pricePerUnit']
            sell_price = sell_summary[0]['pricePerUnit']
            sell_volume = quick_status.get('sellVolume')
            buy_volume = quick_status.get('buyVolume')
            sell_orders = quick_status.get('sellOrders')
            buy_orders = quick_status.get('buyOrders')

            writer.writerow({
                'product_id': product_id,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'last_updated': last_updated,
                'sell_volume': sell_volume,
                'buy_volume': buy_volume,
                'sell_orders': sell_orders,
                'buy_orders': buy_orders
            })

print(f"Data has been successfully saved to '{csv_file}'.")