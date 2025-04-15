import socket
import json

def envoyer_au_moteur_tcp(data):
    HOST = '127.0.0.1'
    PORT = 65432
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(data).encode())
            response = s.recv(1024)
            return json.loads(response.decode())
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def afficher_menu():
    print("=== Console d'administration - Création de partie ===")
    rows = int(input("Nombre de lignes du plateau : "))
    cols = int(input("Nombre de colonnes du plateau : "))
    nb_obstacles = int(input("Nombre d'obstacles : "))
    max_players = int(input("Nombre maximum de joueurs : "))
    nb_turns = int(input("Nombre total de tours : "))
    turn_timeout = int(input("Durée max d'un tour (en secondes) : "))

    partie = {
        "rows": rows,
        "cols": cols,
        "nb_obstacles": nb_obstacles,
        "max_players": max_players,
        "nb_turns": nb_turns,
        "turn_timeout": turn_timeout
    }

    request = {
        "action": "create_party",
        "parameters": [partie]
    }

    print("Envoi au moteur d'administration")
    response = envoyer_au_moteur_tcp(request)
    print("Réponse du moteur :", response)

    return partie

if __name__ == "__main__":
    afficher_menu()
