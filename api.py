from flask import Flask, request, jsonify
import json                          # ← manquait
from pipeline import normalize

app = Flask(__name__)

@app.route("/normalize", methods=["POST"])
def normalize_endpoint():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Champ 'text' manquant"}), 400
    
    candidates = normalize(data["text"])
    
    response = app.response_class(
        response=json.dumps({"candidates": candidates, "count": len(candidates)}, ensure_ascii=False),
        mimetype='application/json; charset=utf-8'
    )
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)