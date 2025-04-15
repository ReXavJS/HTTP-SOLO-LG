import requests
# changer port si on veut affichage web en 8081 par exemple
#Admin via console
BASE_URL = "http://localhost:6000/admin"

def create():
    print("=== Création de partie ===")
    params = {
        "rows": int(input("Lignes : ")),
        "cols": int(input("Colonnes : ")),
        "nb_obstacles": int(input("Obstacles : ")),
        "max_players": int(input("Joueurs max : ")),
        "nb_turns": int(input("Tours max : ")),
        "turn_timeout": int(input("Temps max/tour (s) : "))
    }
    res = requests.post(f"{BASE_URL}/create", json=params)
    print(res.json())

def list_parties():
    res = requests.get(f"{BASE_URL}/list")
    print(res.json())

def party_status():
    pid = input("ID de la partie : ")
    res = requests.get(f"{BASE_URL}/status/{pid}")
    print(res.json())

def menu():
    while True:
        print("\n=== Console Admin (HTTP) ===")
        print("1. Créer une partie")
        print("2. Lister les parties")
        print("3. Voir l'état d'une partie")
        print("0. Quitter")

        choix = input("Choix : ")
        if choix == "1":
            create()
        elif choix == "2":
            list_parties()
        elif choix == "3":
            party_status()
        elif choix == "0":
            break
        else:
            print("Commande invalide.")

if __name__ == "__main__":
    menu()
