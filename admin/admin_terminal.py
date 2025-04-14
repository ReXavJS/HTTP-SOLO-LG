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

    print("Paramètres de la partie enregistrés :")
    for k, v in partie.items():
        print(f"  {k} : {v}")

    return partie


if __name__ == "__main__":
    afficher_menu()
