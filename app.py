from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from skimage.metrics import structural_similarity as ssim

app = Flask(__name__)

def readb64(base64_string):
    encoded_data = base64_string.split(',')[-1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    return img

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    img1 = readb64(data['original'])
    img2 = readb64(data['input'])

    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))

    score, _ = ssim(img1, img2, full=True)
    return jsonify({'similarity': score})
