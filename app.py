from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import re
import os


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def extract_medicines_from_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)

    # Regex to capture the medicine formats
    medicine_regex = r"\b([A-Za-z]+)(?:\s+\d+\s*(mg|tablet|capsules|ml|dose|gram)|\s+(syrup|injection))\b"
    medicines = re.findall(medicine_regex, extracted_text)

    # Extract only medicine names
    medicine_list = [match[0] for match in medicines]
    return medicine_list

@app.route('/extract-medicines', methods=['POST'])
def extract_medicines():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    try:
        # Save the uploaded file temporarily
        temp_path = "./temp_image.png"
        file.save(temp_path)

        # Extract medicines from the image
        medicines = extract_medicines_from_image(temp_path)
        return jsonify({"medicines": medicines})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host='0.0.0.0', port=port)
