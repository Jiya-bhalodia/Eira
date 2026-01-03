from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Eira backend running"


# Vision helper
def analyze_image(image_file):
    vision_endpoint = os.getenv("VISION_ENDPOINT")
    vision_key = os.getenv("VISION_KEY")

    url = f"{vision_endpoint}/vision/v3.2/analyze"
    params = {"visualFeatures": "Tags"}
    headers = {
        "Ocp-Apim-Subscription-Key": vision_key,
        "Content-Type": "application/octet-stream"
    }

    image_bytes = image_file.read()

    response = requests.post(
        url,
        params=params,
        headers=headers,
        data=image_bytes
    )

    response.raise_for_status()
    return response.json()


# SINGLE analyze route
@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})

    image = request.files["image"]

    vision_data = analyze_image(image)
    tags = [t["name"] for t in vision_data.get("tags", [])]

    #TEMP LOGIC (later AI-powered)
    conditions = []
    if "acne" in tags or "pimple" in tags:
        conditions.append("Moderate acne")
    if "skin" in tags:
        conditions.append("Post-inflammatory hyperpigmentation")
    if "face" in tags:
        conditions.append("Enlarged pores")

    if not conditions:
        conditions = ["General skin analysis completed"]

    return jsonify({
        "severity": "Moderate",
        "confidence": 0.92,
        "conditions": conditions,
        "products": [
            "Minimalist Salicylic Acid Cleanser",
            "Dot & Key Niacinamide Serum",
            "The Derma Co Sunscreen SPF 50"
        ]
    })

if __name__ == "__main__":
    app.run(port=3001, debug=True)

