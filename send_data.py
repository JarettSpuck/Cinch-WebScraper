import json
import requests
import json
import requests

with open('data.json', 'r') as file:
    jsonData = json.load(file)

def replace_nan_with_none(data):
    if isinstance(data, list):
        return [replace_nan_with_none(item) for item in data]
    elif isinstance(data, dict):
        return {key: replace_nan_with_none(value) for key, value in data.items()}
    elif data == "NaN":
        return None
    return data

jsonData = replace_nan_with_none(jsonData)

response = requests.post('http://localhost:5000/api/scrape', json=jsonData)
print('Response from API:', response.json())
with open('data.json', 'r') as file:
    jsonData = json.load(file)


def replace_nan_with_none(data):
    if isinstance(data, list):
        return [replace_nan_with_none(item) for item in data]
    elif isinstance(data, dict):
        return {key: replace_nan_with_none(value) for key, value in data.items()}
    elif data == "NaN":
        return None
    return data

jsonData = replace_nan_with_none(jsonData)


response = requests.post('http://localhost:5000/api/data', json=jsonData)
print('Response from API:', response.json())
