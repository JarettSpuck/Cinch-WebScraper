import requests
from bs4 import BeautifulSoup

def scrape_applianceparts365(part_number):
    url = f"https://applianceparts365.com/search?query={part_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for item in soup.select(".product-item"):
        title = item.select_one(".product-title").text.strip()
        price = item.select_one(".product-price").text.strip()
        results.append({"title": title, "price": price})
    if not results:
        return {"error": "No results found"}
    return results
