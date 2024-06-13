import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to scrape Lowe's for a product's price
def scrape_lowes():
    url = "https://www.lowes.com/pd/Frigidaire-18-3-Cu-Ft-Top-Freezer-Refrigerator/5013015811"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Locate the price elements based on provided HTML structure
        price_dollar = soup.find('span', class_='item-price-dollar')
        price_cent = soup.find('span', class_='item-price-cent')
        if price_dollar and price_cent:
            price = price_dollar.text.strip() + price_cent.text.strip()
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Lowe's.")
            return None
    except Exception as e:
        print(f"Error fetching data from Lowe's: {e}")
        return None

# Function to scrape Best Buy for a product's price
def scrape_best_buy():
    url = "https://www.bestbuy.com/site/frigidaire-18-3-cu-ft-top-freezer-refrigerator-white/6369428.p?skuId=6369428"
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Locate the price element based on provided HTML structure
        price_container = soup.find('span', {'aria-hidden': 'true'})
        if price_container:
            price = price_container.text.strip()
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Best Buy.")
            return None
    except Exception as e:
        print(f"Error fetching data from Best Buy: {e}")
        return None

# Scrape each website for the product's prices
lowes_price = scrape_lowes()
best_buy_price = scrape_best_buy()

# Collect all prices
all_prices = [price for price in [lowes_price, best_buy_price] if price is not None]

# Find the best price
if all_prices:
    best_price = min(all_prices)
    print(f"The best price for the refrigerator is ${best_price:.2f}")
else:
    print(f"No prices found for the refrigerator")

# Optionally, save the results to a CSV file
df = pd.DataFrame(all_prices, columns=['Price'])
df.to_csv('prices.csv', index=False)
