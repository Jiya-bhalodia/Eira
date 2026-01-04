from flask import Flask, request, jsonify, send_from_directory # Added send_from_directory
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# SAFE LOADING - Prevents 'NoneType' errors during startup
VISION_KEY = os.getenv("VISION_KEY")
VISION_ENDPOINT = (os.getenv("VISION_ENDPOINT") or "").strip().rstrip("/")
LANG_KEY = os.getenv("LANGUAGE_KEY")
LANG_ENDPOINT = (os.getenv("LANGUAGE_ENDPOINT") or "").strip().rstrip("/")

@app.route("/")
def home():
    # Serves the index.html from your static folder
    return send_from_directory(app.static_folder, 'index.html')

# --- VISION HELPER ---
def analyze_image(image_file):
    # vision_endpoint = os.getenv("VISION_ENDPOINT").rstrip("/")
    endpoint_raw = os.getenv("VISION_ENDPOINT")
    vision_endpoint = endpoint_raw.rstrip("/") if endpoint_raw else ""
    vision_key = os.getenv("VISION_KEY")
    url = f"{vision_endpoint}/vision/v3.2/analyze"
    params = {"visualFeatures": "Tags"}
    headers = {"Ocp-Apim-Subscription-Key": vision_key, "Content-Type": "application/octet-stream"}
    
    image_bytes = image_file.read()
    response = requests.post(url, params=params, headers=headers, data=image_bytes)
    response.raise_for_status()
    return response.json()

@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"})
    try:
        image = request.files["image"]
        vision_data = analyze_image(image)
        tags = [t["name"] for t in vision_data.get("tags", [])]
        
        conditions = ["General skin analysis completed"]
        if any(x in tags for x in ["acne", "pimple", "rash"]):
            conditions = ["Active skin congestion / Acne"]
        
        return jsonify({"severity": "Moderate", "confidence": 0.88, "conditions": conditions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/extract", methods=["POST"])
def extract_entities():
    data = request.json
    text = data.get("text", "").lower()

    endpoint = os.getenv("LANGUAGE_ENDPOINT").rstrip("/")
    key = os.getenv("LANGUAGE_KEY")
    url = f"{endpoint}/language/:analyze-text?api-version=2023-04-01"
    
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    payload = {
        "kind": "EntityRecognition",
        "analysisInput": {"documents": [{"id": "1", "language": "en", "text": text}]}
    }

    extracted = {"age": "", "skin_type": "", "concern": "", "budget": "", "allergies": ""}

    skin_types = ["oily", "dry", "combination", "sensitive"]
    for s in skin_types:
        if s in text: extracted["skin_type"] = s
        
    budgets = ["low", "balanced", "premium"]
    for b in budgets:
        if b in text: extracted["budget"] = b

    concerns = ["acne", "pigmentation", "dullness", "dark spots"]
    for c in concerns:
        if c in text: extracted["concern"] = c

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            entities = result["results"]["documents"][0]["entities"]
            
            for ent in entities:
                val = ent["text"].lower()
                cat = ent["category"]
                
                if cat in ["Age", "Quantity"] and any(char.isdigit() for char in val):
                    extracted["age"] = val
                elif cat == "MedicalCondition":
                    if not extracted["concern"]:
                        extracted["concern"] = val
                    else:
                        extracted["allergies"] = val
    except Exception as e:
        print(f"Azure Error: {e}")

    return jsonify(extracted)

if __name__ == "__main__":
    # Azure likes Port 8000 or the environment PORT
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)