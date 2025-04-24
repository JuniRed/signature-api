from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

def decode_base64_image(image_str):
    try:
        image_data = base64.b64decode(image_str)
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("Decode failed:", e)
        return None

def compare_images(img1, img2):
    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))
    diff = cv2.absdiff(img1, img2)
    similarity = 1.0 - (np.sum(diff) / (300 * 100 * 255 * 3))  # normalized diff
    return similarity

@app.route("/compare", methods=["POST"])
def compare_signatures():
    data = request.get_json()
    original = decode_base64_image(data.get("original"))
    input_img = decode_base64_image(data.get("input"))

    if original is None or input_img is None:
        return jsonify({"error": "Image decoding failed"}), 400

    similarity = compare_images(original, input_img)
    return jsonify({"similarity": similarity})
