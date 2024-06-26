import os  # Import the os module for environment variable access
import requests  # Import the requests module to handle HTTP requests
import json  # Imports the json module to handle JSON dta
import boto3  # Import the boto3 module to interact with AWS S3
from datetime import datetime  # Import datetime for timestamp generation
import urllib3  # Import urllib3 to manage HTTP requests and suppress SSL warnings
import logging  # Import logging for logging purposes
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set logging level to INFO
logger = logging.getLogger()  # Get the logger instance

# Load environment variables from .env file
load_dotenv()

# Initialize S3 client with AWS credentials and region from environment variables
s3_client = boto3.client('s3', region_name=os.getenv('AWS_DEFAULT_REGION'))
bucket_name = os.getenv('BUCKET_NAME')  # Get the bucket name from environment variables

def get_amazon_part_data(asin):
    params = {
        'api_key': os.getenv('RAINFOREST_API_KEY'),  # Get the Rainforest API key from environment variables
        'amazon_domain': 'amazon.com',  # Specify the Amazon domain
        'asin': asin,  # The ASIN for the product
        'type': 'product'  # The type of request
    }

    try:
        # Make a GET request to the Rainforest API
        response = requests.get('https://api.rainforestapi.com/request', params=params, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()  # Parse the JSON response
        product = data.get('product', {})  # Extract the product data

        # Extract product details
        title = product.get('title', 'No title')
        description = product.get('description', 'No description')
        manufacturer = product.get('brand', 'No manufacturer')
        part_number = product.get('specifications', {})
        part_number_value = next((item['value'] for item in part_number if item['name'] == 'Part Number'), 'No part number')
        
        price = product.get('price', {}).get('value', 'N/A')
        buybox_winner = product.get('buybox_winner', {})
        if price == 'N/A':
            price = buybox_winner.get('price', {}).get('value', 'N/A')

        stock = buybox_winner.get('availability', {}).get('raw', 'N/A')
        ship_date = buybox_winner.get('fulfillment', {}).get('standard_delivery', {}).get('date', 'N/A')
        shipping_cost = buybox_winner.get('shipping', 'N/A')
        add_to_cart_link = f"https://www.amazon.com/gp/aws/cart/add.html?ASIN.1={asin}&Quantity.1=1"

        # Create a result dictionary with product details
        result = {
            "asin": asin,
            "part_number": part_number_value,
            "part_description": description,
            "part_manufacturer": manufacturer,
            "availability": stock,
            "expected_ship_date": ship_date,
            "distributor_site_name": "Amazon",
            "time_of_pull": datetime.utcnow().isoformat(),  # Add timestamp
            "shipping_cost": shipping_cost,
            "add_to_cart_link": add_to_cart_link,
            "price": price,
            "link": product.get('link', 'No link')
        }

        # Create a unique filename with the current timestamp
        file_name = f"{asin}_{datetime.utcnow().isoformat()}.json"
        # Upload the JSON result to the specified S3 bucket
        s3_client.put_object(
            Bucket=bucket_name,
            Key=f"scraped_data/{file_name}",
            Body=json.dumps(result),
            ContentType='application/json'
        )

        logger.info(f"Successfully uploaded data for {asin} to S3.")
        return result

    except requests.exceptions.HTTPError as errh:
        logger.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logger.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logger.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logger.error(f"Oops: Something Else {err}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    # Test the function with a specific ASIN
    asin = 'B091V3LDP9'
    part_data = get_amazon_part_data(asin)
    # Print the result in a formatted JSON string
    print(json.dumps(part_data, indent=2))
