import os
import requests
from dotenv import load_dotenv

load_dotenv()

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT")
VISION_KEY = os.getenv("VISION_KEY")

def analyze_local_image(image_path):
    url = f"{VISION_ENDPOINT}vision/v3.2/analyze"
    
    headers = {
        "Ocp-Apim-Subscription-Key": VISION_KEY,
        "Content-Type": "application/octet-stream"
    }

    params = {
        "visualFeatures": "Description,Tags"
    }

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    response = requests.post(url, headers=headers, params=params, data=image_data)

    if response.status_code != 200:
        print("ERROR:", response.text)
        response.raise_for_status()

    return response.json()


