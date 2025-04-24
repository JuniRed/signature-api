from flask import Flask, request, jsonify
import base64
import cv2
import numpy as np

app = Flask(__name__)

def compare_images(img1_b64, img2_b64):
    try:
        img1_data = base64.b64decode(img1_b64.split(',')[-1])
        img2_data = base64.b64decode(img2_b64.split(',')[-1])
        img1_np = np.frombuffer(img1_data, np.uint8)
        img2_np = np.frombuffer(img2_data, np.uint8)
        img1 = cv2.imdecode(img1_np, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imdecode(img2_np, cv2.IMREAD_GRAYSCALE)

        img1 = cv2.resize(img1, (300, 100))
        img2 = cv2.resize(img2, (300, 100))

        similarity = np.sum(img1 == img2) / img1.size
        return similarity
    except Exception as e:
        print(f"Error comparing images: {e}")
        return None

@app.route("/compare", methods=["POST"])
def compare():
    try:
        data = request.get_json()
        original = data.get("original")
        input_img = data.get("input")
        similarity = compare_images(original, input_img)

        if similarity is None:
            return jsonify({"error": "Comparison failed"}), 500

        return jsonify({"similarity": similarity})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
