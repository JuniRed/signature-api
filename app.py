from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

# Initialize the Flask app
app = Flask(__name__)

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
        # Resize images to the same size for comparison
        img1 = cv2.resize(img1, (300, 100))
        img2 = cv2.resize(img2, (300, 100))

        # Calculate the absolute difference between the images
        diff = cv2.absdiff(img1, img2)

        # Calculate similarity: (1 - normalized difference)
        similarity = 1 - (np.sum(diff) / (img1.size * 255))
        return round(similarity, 2)
    except Exception as e:
        print(f"Error comparing images: {e}")
        return None

# Example function to perform signature verification
def verify_signature(original_image, compare_image):
    # Compare the original and comparison images
    similarity_score = compare_images(original_image, compare_image)

    # Placeholder verification logic
    result = {
        "valid": similarity_score > 0.85,  # Set a threshold for validity (e.g., 85% similarity)
        "confidence": similarity_score
    }
    return result

@app.route("/verify_signature", methods=["POST"])
def verify_signature_endpoint():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    original_data = data.get("original")
    compare_data = data.get("compare")

    if not original_data or not compare_data:
        return jsonify({"error": "Both 'original' and 'compare' images must be provided."}), 400

    # Decode the base64 images
    original_img = decode_base64_image(original_data)
    compare_img = decode_base64_image(compare_data)

    if original_img is None or compare_img is None:
        return jsonify({"error": "Failed to decode one or both images"}), 400

    # Perform verification and return results
    verification_result = verify_signature(original_img, compare_img)
    return jsonify(verification_result)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
