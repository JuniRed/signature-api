from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
import logging  # Import logging

# Initialize the Flask app
app = Flask(__name__)

# Function to encode an image as base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/png;base64,{base64_image}"

# Function to decode a base64 image
def decode_base64_image(data_url):
    try:
        header, encoded = data_url.split(",", 1)
        decoded = base64.b64decode(encoded)
        nparr = np.frombuffer(decoded, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        logging.error(f"Error decoding image: {e}")  # Log error
        return None

# Function to compare two images
def compare_images(img1, img2):
    try:
        img1 = cv2.resize(img1, (300, 100))
        img2 = cv2.resize(img2, (300, 100))
        diff = cv2.absdiff(img1, img2)
        similarity = 1 - (np.sum(diff) / (img1.size * 255))
        return round(similarity, 2)
    except Exception as e:
        logging.error(f"Error comparing images: {e}")  # Log error
        return None

@app.route("/verify_signature", methods=["POST"])
def verify_signature():
    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("verify_signature endpoint called")

    # Validate request format
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400

    # Parse request data
    data = request.get_json()
    logging.debug(f"Received JSON Payload: {data}")

    original_data = data.get("original")
    compare_data = data.get("compare")

    # Check if both original and comparison images are provided
    if not original_data or not compare_data:
        logging.warning("Missing 'original' or 'compare' data in the payload")
        return jsonify({"error": "Both 'original' and 'compare' images must be provided."}), 400

    # Decode images
    original_img = decode_base64_image(original_data)
    compare_img = decode_base64_image(compare_data)

    if original_img is None or compare_img is None:
        logging.warning("Failed to decode one or both images")
        return jsonify({"error": "Failed to decode one or both images"}), 400

    # Compare images
    similarity_score = compare_images(original_img, compare_img)
    logging.debug(f"Similarity score: {similarity_score}")

    result = {
        "valid": similarity_score > 0.85,  # Valid if similarity score exceeds 85%
        "confidence": similarity_score
    }
    logging.info(f"Verification result: {result}")
    return jsonify(result)

# Example usage within this file
if __name__ == "__main__":
    original_image_path = "path/to/original_image.png"
    compare_image_path = "path/to/comparison_image.png"

    original_base64 = encode_image(original_image_path)
    compare_base64 = encode_image(compare_image_path)

    print("Original Base64:", original_base64)
    print("Comparison Base64:", compare_base64)

    app.run(debug=True)
