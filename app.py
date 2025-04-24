from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

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
        print("Error decoding image:", e)
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
        print(f"Error comparing images: {e}")
        return None

@app.route("/verify_signature", methods=["POST"])
def verify_signature():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    original_data = data.get("original")
    compare_data = data.get("compare")

    if not original_data or not compare_data:
        return jsonify({"error": "Both 'original' and 'compare' images must be provided."}), 400

    original_img = decode_base64_image(original_data)
    compare_img = decode_base64_image(compare_data)

    if original_img is None or compare_img is None:
        return jsonify({"error": "Failed to decode one or both images"}), 400

    similarity_score = compare_images(original_img, compare_img)
    result = {
        "valid": similarity_score > 0.85,
        "confidence": similarity_score
    }
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
