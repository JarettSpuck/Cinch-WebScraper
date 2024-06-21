import requests
from bs4 import BeautifulSoup
import certifi

def scrape_appliancepartspros(part_number):
    url = "https://www.appliancepartspros.com/search.aspx?q={part_number}"
    response = requests.get(url, verify=certifi.where())
    print(response.content)
    soup = BeautifulSoup(response.content, "html.parser")
    results = [] 
    for item in soup.select(".search-product"):
        title = item.select_one(".title").text.strip()
        price = item.select_one(".price").text.strip()
        results.append({"title": title, "price": price})
    if not results:
        return {"error": "No results found"}
    return results
