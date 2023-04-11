import argparse
import base64
import io
import os
import requests
import json

import re


def extract_ingredients(text):
    start = text.find("INGREDIENTS:")
    if start == -1:
        return []

    # Find the end of the ingredients list
    end = text.find(".", start)

    # Extract the ingredients
    ingredients_str = text[start+len("INGREDIENTS:"):end]
    ingredients = [ing.strip().replace("\n", "") for ing in ingredients_str.split(",")]

    return ingredients


# Set up the Vision API endpoint URL
url = 'https://vision.googleapis.com/v1/images:annotate'

# Set up the API key and request headers

headers = {'Content-Type': 'application/json'}
api_key = 'AIzaSyAyyNJxYrS6QG4KpZUi91NiW1vCAFLF15c'
# Set up argument parser to get filename from command line input
parser = argparse.ArgumentParser(description='Extract nutrition information from an image')
parser.add_argument('-i', '--input', type=str, required=True, help='Input file name')
args = parser.parse_args()
file_name = args.input

# Get the directory of the current script
directory = os.path.dirname(os.path.abspath(__file__))

# Load the image file
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

# Encode the image content as base64 string
content_base64 = base64.b64encode(content).decode('utf-8')
# Set up the request body with the image content
request_body = {
    'requests': [{
        'image': {
            'content': content_base64
        },
        'features': [{
            'type': 'TEXT_DETECTION'
        }]
    }]
}

# Send the POST request to the API and get the response
try:
    response = requests.post(url=url, params={'key': api_key}, headers=headers, json=request_body)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    response = None

if response is not None:
    response_json = json.loads(response.text)
    # print(response_json['responses'][0]['fullTextAnnotation']['text'])
    nutrition_text=response_json['responses'][0]['fullTextAnnotation']['text']
    ingredients = extract_ingredients(nutrition_text)
    print(ingredients)
