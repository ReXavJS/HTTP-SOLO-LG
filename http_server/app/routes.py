from flask import Blueprint, request, jsonify
from tcp_client_admin import send_tcp_request

main = Blueprint("main", __name__)

@main.route("/", methods=["GET"])
def home():
    return {"message": "Bienvenue sur le serveur Les Loups"}, 200


@main.route("/parties", methods=["POST"])
def create_party():
    req = {
        "action": "create",
        "parameters": [request.json]
    }
    res = send_tcp_request(req)
    return jsonify(res)


@main.route("/parties", methods=["GET"])
def list_parties():
    req = {
        "action": "list",
        "parameters": []
    }
    res = send_tcp_request(req)
    return jsonify(res)


@main.route("/parties/<int:party_id>/join", methods=["POST"])
def join_party(party_id):
    player_name = request.json.get("player")
    req = {
        "action": "subscribe",
        "parameters": [
            {"player": player_name},
            {"id_party": party_id}
        ]
    }
    res = send_tcp_request(req)
    return jsonify(res)


@main.route("/parties/<int:party_id>/board", methods=["GET"])
def get_board(party_id):
    player_id = request.args.get("player_id")
    req = {
        "action": "gameboard_status",
        "parameters": [
            {"id_party": int(party_id)},
            {"id_player": int(player_id)}
        ]
    }
    res = send_tcp_request(req)
    return jsonify(res)


@main.route("/parties/<int:party_id>/move", methods=["POST"])
def make_move(party_id):
    data = request.json
    req = {
        "action": "move",
        "parameters": [
            {"id_party": party_id},
            {"id_player": data.get("player_id")},
            {"move": data.get("move")}
        ]
    }
    res = send_tcp_request(req)
    return jsonify(res)
