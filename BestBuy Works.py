from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Path to your compatible chromedriver
CHROMEDRIVER_PATH = r'C:\Users\jspuck\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# Correct URL for Best Buy product page
BESTBUY_URL = "https://www.bestbuy.com/site/frigidaire-18-3-cu-ft-top-freezer-refrigerator-white/6369428.p?skuId=6369428"

# Function to scrape Best Buy for a product's price using Selenium
def scrape_best_buy_selenium():
    options = Options()
    # Disable headless mode
    options.headless = False
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(BESTBUY_URL)
    
    try:
        # Wait for the price element to be present
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.priceView-hero-price.priceView-customer-price > span[aria-hidden="true"]'))
        )
        
        # Get the price text
        price_text = price_element.text.strip()
        
        # Print the entire page source for debugging
        page_source = driver.page_source
        with open('bestbuy_page_source.html', 'w', encoding='utf-8') as f:
            f.write(page_source)
        
        # Print the price text for debugging
        print(f"Price text found: {price_text}")
        
        driver.quit()
        
        # Convert the price text to float
        return float(price_text.replace('$', '').replace(',', ''))
    except Exception as e:
        driver.quit()
        print(f"Error fetching data from Best Buy using Selenium: {e}")
        # Keep the browser open for longer to inspect
        time.sleep(300)  # Keep the browser open for 5 minutes
        return None

# Scrape Best Buy for the product's price
best_buy_price = scrape_best_buy_selenium()

# Collect all prices
all_prices = [price for price in [best_buy_price] if price is not None]

# Find the best price
if all_prices:
    best_price = min(all_prices)
    print(f"The best price for the refrigerator is ${best_price:.2f}")
else:
    print(f"No prices found for the refrigerator")

# Optionally, save the results to a CSV file
df = pd.DataFrame(all_prices, columns=['Price'])
df.to_csv('prices.csv', index=False)
