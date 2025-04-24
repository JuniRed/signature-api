from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/compare", methods=["POST"])
def compare_signatures():
    data = request.get_json()
    original = data.get("original")
    input_img = data.get("input")
    
    # Do your image comparison here...
    similarity = 0.93  # example value
    return jsonify({"similarity": similarity})
