from flask import Flask, request, jsonify
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
import base64

app = Flask(__name__)

def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

@app.route('/compare', methods=['POST'])
def compare():
    data = request.get_json()
    img1 = readb64(data['image1'])
    img2 = readb64(data['image2'])

    img1 = cv2.resize(img1, (300, 100))
    img2 = cv2.resize(img2, (300, 100))

    score, _ = ssim(img1, img2, full=True)
    return jsonify({'similarity': score, 'match': score > 0.7})

if __name__ == '__main__':
    app.run()
