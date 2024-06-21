import os
import json
from datetime import datetime, timezone
from flask import Flask, request
from s3_upload import upload_to_s3
from scrapers.applianceparts365_scraper import scrape_applianceparts365
from scrapers.appliancepartspros_scraper import scrape_appliancepartspros
from scrapers.partselect_scraper import scrape_partselect
from scrapers.repairclinic_scraper import scrape_repairclinic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def scrape_and_store():
    data = request.get_json()
    part_number = data['part_number']

    # Scrape data
    results = {
        "applianceparts365": scrape_applianceparts365(part_number),
        "appliancepartspros": scrape_appliancepartspros(part_number),
        "partselect": scrape_partselect(part_number),
        "repairclinic": scrape_repairclinic(part_number)
    }

    # Save data locally
    timestamp = datetime.now(timezone.utc).isoformat().replace(":", "-")
    file_name = f"{part_number}_{timestamp}.json"
    directory = 'scraped_data'
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        json.dump(results, file)

    # Upload to S3
    upload_to_s3(file_path, file_name)

    return {"message": "Data scraped and stored successfully."}, 200

if __name__ == '__main__':
    app.run(debug=True)
