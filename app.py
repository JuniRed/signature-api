@app.route("/compare", methods=["POST"])
def compare():
    try:
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

        similarity = compare_images(img1, img2)
        return jsonify({"similarity": similarity})

    except Exception as e:
        print("Unexpected error:", e)
        return jsonify({"error": f"Unexpected error occurred: {str(e)}"}), 500
