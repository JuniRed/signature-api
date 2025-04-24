from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

def readb64(uri):
    try:
        import base64
        import numpy as np
        import cv2

        encoded_data = uri.split(",")[-1]
        missing_padding = len(encoded_data) % 4
        if missing_padding:
            encoded_data += "=" * (4 - missing_padding)

        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

        return img
    except Exception as e:
        print("Error decoding image:", e)
        return None


def compare_images(img1, img2):
    # Resize to same size for fair comparison
    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))

    # Use Structural Similarity Index (SSIM)
    from skimage.metrics import structural_similarity as ssim
    score, _ = ssim(img1, img2, full=True)
    return score

@app.route("/compare", methods=["POST"])
def compare():
    data = request.get_json()
    original = data.get("original")
    input_img = data.get("input")

    print("Original image length:", len(original) if original else "None")
    print("Input image length:", len(input_img) if input_img else "None")

    img1 = readb64(original)
    img2 = readb64(input_img)

    if img1 is None or img2 is None:
        return jsonify({"error": "One or both images could not be decoded"}), 400

    similarity = compare_images(img1, img2)
    return jsonify({"similarity": similarity})

