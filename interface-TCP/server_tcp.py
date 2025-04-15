import socket
import threading
import json
from engines.admin_engine import AdminEngine
from engines.game_engine import GameEngine


HOST = '0.0.0.0'
PORT = 65432

admin_engine = AdminEngine()
game_engine = GameEngine()

def handle_client(conn, addr):
    print(f"[INFO] Connexion depuis {addr}")
    with conn:
        data = conn.recv(4096)
        if not data:
            return
        try:
            request = json.loads(data.decode())
            action = request.get("action")
            params = request.get("parameters", [])

            print(f"[REQUETE] Action: {action} | Params: {params}")

            if action == "create_party":
                response = admin_engine.create_party(params[0])
            elif action == "list":
                response = {"parties": admin_engine.list_parties()}
            elif action == "party_status":
                response = admin_engine.get_party(params[0].get("id_party"))

            elif action == "move":
                response = game_engine.move_player(params[0])
            else:
                response = {"error": f"Action inconnue : {action}"}

            conn.sendall(json.dumps({"status": "OK", "response": response}).encode())
        except Exception as e:
            print(f"[ERREUR] {e}")
            conn.sendall(json.dumps({"status": "ERROR", "message": str(e)}).encode())

def start_server():
    print(f"[INFO] Serveur TCP démarré sur {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
