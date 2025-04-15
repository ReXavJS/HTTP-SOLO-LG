from flask import Flask, request, jsonify
from core_admin import AdminEngine

app = Flask(__name__)
engine = AdminEngine()

@app.route("/admin/create", methods=["POST"])
def create_party():
    data = request.json
    result = engine.create_party(data)
    return jsonify({"status": "OK", "response": result})

@app.route("/admin/list", methods=["GET"])
def list_parties():
    return jsonify({"status": "OK", "response": engine.list_parties()})

@app.route("/admin/status/<int:party_id>", methods=["GET"])
def party_status(party_id):
    return jsonify({"status": "OK", "response": engine.get_party(party_id)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000, debug=True)
