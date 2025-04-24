from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)

def readb64(uri):
    encoded_data = uri.split(',')[-1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    return img

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
    data = request.json
    img1 = readb64(data['original'])
    img2 = readb64(data['input'])

    similarity = compare_images(img1, img2)
    return jsonify({"similarity": similarity})
