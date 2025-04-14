import requests

BASE_URL = "http://localhost:5000"

party_id = None
player_id = None

def menu():
    print("Client HTTP Les Loups")
    print("1. Rejoindre une partie")
    print("2. Voir le plateau")
    print("3. Faire un déplacement")
    print("0. Quitter")
    return input("Choix : ")

def join_party():
    global party_id, player_id
    party_id = int(input("ID de la partie à rejoindre : "))
    player_name = input("Votre pseudo : ")

    payload = {"player_name": player_name}
    try:
        response = requests.post(f"{BASE_URL}/parties/{party_id}/join", json=payload)
        data = response.json()
        player_id = data.get("id_player")
        print(f"Inscription réussie en tant que {data.get('role')} (ID joueur : {player_id})")
    except Exception as e:
        print("Erreur lors de l’inscription :", e)

def get_board():
    if not party_id or not player_id:
        print("Vous devez d’abord rejoindre une partie.")
        return

    try:
        response = requests.get(
            f"{BASE_URL}/parties/{party_id}/board",
            params={"player_id": player_id}
        )
        board = response.json()["board"]
        print("Plateau visible :")
        for row in board:
            print(" ".join(str(cell) for cell in row))
    except Exception as e:
        print("Erreur lors de la récupération du plateau :", e)

def move():
    if not party_id or not player_id:
        print("Vous devez d’abord rejoindre une partie.")
        return

    row = int(input("Déplacement ligne (-1, 0, 1) : "))
    col = int(input("Déplacement colonne (-1, 0, 1) : "))

    payload = {
        "player_id": player_id,
        "move": f"{row}{col}"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/parties/{party_id}/move",
            json=payload
        )
        print("Réponse :", response.json())
    except Exception as e:
        print("Erreur lors du déplacement :", e)

while True:
    choix = menu()
    if choix == "1":
        join_party()
    elif choix == "2":
        get_board()
    elif choix == "3":
        move()
    elif choix == "0":
        print("À bientôt !")
        break
    else:
        print("Choix invalide.")
