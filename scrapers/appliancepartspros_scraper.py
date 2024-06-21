import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def scrape_appliancepartspros(part_number):
    url = f"https://www.appliancepartspros.com/search.aspx?searchTerm={part_number}"
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Failed to retrieve page, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for item in soup.select(".product-item"):
        title = item.select_one(".product-title").text.strip() if item.select_one(".product-title") else "No title"
        price = item.select_one(".product-price").text.strip() if item.select_one(".product-price") else "No price"
        stock = item.select_one(".product-stock").text.strip() if item.select_one(".product-stock") else "No stock"
        link = item.select_one("a")['href'] if item.select_one("a") else "No link"
        shipping_info = item.select_one(".product-shipping").text.strip() if item.select_one(".product-shipping") else "No shipping info"
        results.append({
            "title": title,
            "price": price,
            "stock": stock,
            "link": link,
            "shipping_info": shipping_info
        })
    return results
