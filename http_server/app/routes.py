from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return {"message": "Bienvenue sur le serveur Les Loups"}, 200

@main.route("/parties/<int:party_id>/join", methods=["POST"])
def join_party(party_id):
    data = request.json
    player_name = data.get("player_name", "inconnu")
    return jsonify({
        "status": "OK",
        "id_player": 42,
        "role": "villager"
    })
    

@main.route("/parties/<int:party_id>/board", methods=["GET"])
def get_board(party_id):
    player_id = request.args.get("player_id")
    return jsonify({
        "status": "OK",
        "board": [
            [0, 1, 0],
            [0, 2, 3],
            [0, 0, 0]
        ]
    })

@main.route("/parties/<int:party_id>/move", methods=["POST"])
def make_move(party_id):
    data = request.json
    return jsonify({
        "status": "OK",
        "new_position": {"row": 1, "col": 2}
    })
