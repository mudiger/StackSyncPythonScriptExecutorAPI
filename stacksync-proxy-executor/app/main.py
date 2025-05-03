#Saarthak Mudigere Girsh
#saarthakmudigere@gmail.com
#6823923698

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# VM’s external IP
GCE_VM_URL = "http://35.224.20.200:8080/execute"

@app.route("/execute", methods=["POST"])
def forward_to_vm():
    data = request.get_json()
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' key"}), 400

    try:
        response = requests.post(GCE_VM_URL, json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to reach execution server: {str(e)}"}), 500
