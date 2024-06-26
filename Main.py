import json  # Add this import
from scrapers import amazon_scraper
# Import other scrapers

def main():
    amazon_part_number = 'B091V3LDP9'
    amazon_data = amazon_scraper.get_amazon_part_data(amazon_part_number)
    print(json.dumps(amazon_data, indent=2))

    # Call other scrapers similarly

if __name__ == "__main__":
    main()
