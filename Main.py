from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib3
import time

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Path to your compatible chromedriver
CHROMEDRIVER_PATH = r'C:\Users\jspuck\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

# URLs for product pages
BESTBUY_URL = "https://www.bestbuy.com/site/frigidaire-18-3-cu-ft-top-freezer-refrigerator-white/6369428.p?skuId=6369428"
PCRICHARD_URL = "https://www.pcrichard.com/frigidaire-30-in-18.3-cu-ft-top-refrigerator-white/FFTR1835VW.html?utm_source=google&utm_medium=organic&utm_campaign=free-shopping&srsltid=AfmBOoprSDaOwQvYin6tW-SSkmul8Ud1YugSCDMeA7fCtli-eVE3o0wLVPk"

# Function to scrape Best Buy for a product's price using Selenium
def scrape_best_buy_selenium():
    options = Options()
    options.headless = True
    options.add_argument("--log-level=3")
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(BESTBUY_URL)
    
    try:
        price_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.priceView-hero-price.priceView-customer-price > span[aria-hidden="true"]'))
        )
        price_text = price_element.text.strip()
        print(f"Best Buy price text found: {price_text}")
        driver.quit()
        return float(price_text.replace('$', '').replace(',', ''))
    except Exception as e:
        driver.quit()
        print(f"Error fetching data from Best Buy using Selenium: {e}")
        return None

# Function to scrape PCRichard for a product's price using requests and BeautifulSoup
def scrape_pcrichard_requests(retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = requests.adapters.Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504)
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        print(f"Making request to PCRichard URL: {PCRICHARD_URL}")
        response = session.get(PCRICHARD_URL, verify=False, timeout=90)
        response.raise_for_status()
        print("Response received from PCRichard")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Attempt to find the price using the provided HTML structure
        price_element = soup.find('span', class_='value')
        if price_element:
            price_text = price_element.get_text(strip=True)
            print(f"PCRichard price text found: {price_text}")
            return float(price_text.replace('$', '').replace(',', ''))
        else:
            print("Price element not found on PCRichard.")
            return None
    except Exception as e:
        print(f"Error fetching data from PCRichard using requests: {e}")
        return None

# Scrape each website for the product's prices
best_buy_price = scrape_best_buy_selenium()
pcrichard_price = scrape_pcrichard_requests()

# Collect all prices
all_prices = [price for price in [best_buy_price, pcrichard_price] if price is not None]

# Find the best price
if all_prices:
    best_price = min(all_prices)
    print(f"The best price for the refrigerator is ${best_price:.2f}")
else:
    print(f"No prices found for the refrigerator")

# Optionally, save the results to a CSV file
df = pd.DataFrame(all_prices, columns=['Price'])
df.to_csv('prices.csv', index=False)
