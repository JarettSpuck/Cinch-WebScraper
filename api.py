from flask import Flask, jsonify, request
import json
import boto3
from datetime import datetime

# Import scraper functions from the scrapers directory
from scrapers.applianceparts365_scraper import scrape_applianceparts365
from scrapers.appliancepartspros_scraper import scrape_appliancepartspros
from scrapers.partselect_scraper import scrape_partselect
from scrapers.repairclinic_scraper import scrape_repairclinic

app = Flask(__name__)

s3 = boto3.client('s3')
BUCKET_NAME = 'your-s3-bucket-name'

@app.route('/')
def home():
    return "Welcome to the API. Use /api/scrape to send part numbers."

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/api/scrape', methods=['POST'])
def scrape_and_store():
    data = request.get_json()
    if not data or 'part_number' not in data:
        return jsonify({"error": "part_number is required"}), 400

    part_number = data['part_number']

    # Scrape data
    results = {
        "applianceparts365": scrape_applianceparts365(part_number),
        "appliancepartspros": scrape_appliancepartspros(part_number),
        "partselect": scrape_partselect(part_number),
        "repairclinic": scrape_repairclinic(part_number),
    }

    timestamp = datetime.utcnow().isoformat()
    file_name = f"{part_number}_{timestamp}.json"

    # Save data to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(results),
        ContentType='application/json'
    )

    return jsonify({"message": "Data scraped and stored successfully", "file_name": file_name})

if __name__ == '__main__':
    app.run(debug=True)
