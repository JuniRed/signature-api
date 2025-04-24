from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Function to decode base64 image
def decode_base64_image(data_url):
    try:
        header, encoded = data_url.split(",", 1)
        decoded = base64.b64decode(encoded)
        nparr = np.frombuffer(decoded, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("Image decoding failed:", e)
        return None

# Function to compare two images
def compare_images(img1, img2):
    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))
    diff = cv2.absdiff(img1, img2)
    similarity = 1 - (np.sum(diff) / (img1.size * 255))
    return round(similarity, 2)

# Route for image comparison
@app.route("/compare", methods=["POST"])
def compare():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    original_data = data.get("original")
    input_data = data.get("input")

    if not original_data or not input_data:
        return jsonify({"error": "Both 'original' and 'input' must be provided."}), 400

    img1 = decode_base64_image(original_data)
    img2 = decode_base64_image(input_data)

    if img1 is None or img2 is None:
        return jsonify({"error": "Failed to decode one or both images"}), 400

    try:
        similarity = compare_images(img1, img2)
        return jsonify({"similarity": similarity})
    except Exception as e:
        return jsonify({"error": f"Error comparing images: {str(e)}"}), 500

# Run the Flask application (only for local testing)
if __name__ == "__main__":
    app.run(debug=True)
