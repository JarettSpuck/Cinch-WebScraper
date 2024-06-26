import os
import json
from datetime import datetime, timezone
from flask import Flask, request
from s3_upload import upload_to_s3
from scrapers.applianceparts365_scraper import scrape_applianceparts365
from scrapers.appliancepartspros_scraper import scrape_appliancepartspros
from scrapers.partselect_scraper import scrape_partselect
from scrapers.repairclinic_scraper import scrape_repairclinic
from scrapers.amazon_scraper import get_amazon_part_data
from dotenv import load_dotenv
import boto3

# Load environment variables
load_dotenv()


os.environ['AWS_ACCESS_KEY_ID'] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = os.getenv('AWS_SECRET_ACCESS_KEY')
os.environ['AWS_DEFAULT_REGION'] = os.getenv('AWS_DEFAULT_REGION')
bucket_name = os.getenv('BUCKET_NAME')

app = Flask(__name__)

@app.route('/api/scrape', methods=['POST'])
def scrape_and_store():
    data = request.get_json()
    part_number = data.get('part_number')
    asin = data.get('asin')

    # Scrape data
    results = {
        "applianceparts365": scrape_applianceparts365(part_number),
        "appliancepartspros": scrape_appliancepartspros(part_number),
        "partselect": scrape_partselect(part_number),
        "repairclinic": scrape_repairclinic(part_number),
        "amazon": get_amazon_part_data(asin) if asin else {"error": "ASIN not provided"}
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
    try:
        upload_to_s3(file_path, file_name)
    except Exception as e:
        return {"message": f"Failed to upload to S3: {e}"}, 500

    return {"message": "Data scraped and stored successfully."}, 200

if __name__ == '__main__':
    app.run(debug=True)
