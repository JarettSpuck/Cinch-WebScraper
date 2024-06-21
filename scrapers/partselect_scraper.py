
import requests
from bs4 import BeautifulSoup
import certifi

def scrape_partselect(part_number):
    url = f"https://www.partselect.com/Search.aspx?SearchTerm={part_number}"
    response = requests.get(url, verify=certifi.where())
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for item in soup.select(".search-result"):
        title = item.select_one(".title").text.strip()
        price = item.select_one(".price").text.strip()
        results.append({"title": title, "price": price})
    if not results:
        return {"error": "No results found"}
    return results