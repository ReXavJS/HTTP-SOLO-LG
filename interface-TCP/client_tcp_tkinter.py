import tkinter as tk
from tkinter import ttk, messagebox
import socket
import json

# Paramètres du serveur
HOST = 'host.docker.internal'
PORT = 65432

# Fonction d'envoi de requêtes

def send_request(request):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(json.dumps(request).encode())
            data = s.recv(1024)
            return data.decode()
    except Exception as e:
        return f"Erreur de connexion: {e}"

# Fonction appelée lors du clic sur le bouton Envoyer

def envoyer_commande():
    action = action_var.get()
    request = {"action": action, "parameters": []}

    if action == 'subscribe':
        request['parameters'] = [
            {"player": entry_player.get()},
            {"id_party": entry_party.get()}
        ]
    elif action in ['party_status', 'gameboard_status']:
        request['parameters'] = [
            {"id_party": int(entry_party.get())},
            {"id_player": int(entry_player_id.get())}
        ]
    elif action == 'move':
        request['parameters'] = [
            {"id_party": int(entry_party.get())},
            {"id_player": int(entry_player_id.get())},
            {"move": entry_move.get()}
        ]

    response = send_request(request)
    text_response.delete('1.0', tk.END)
    text_response.insert(tk.END, response)

# Création de la fenêtre principale
root = tk.Tk()
root.title("Client TCP Tkinter")

# Champs de saisie
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Action selection
ttk.Label(frame, text="Action:").grid(row=0, column=0, sticky=tk.W)
action_var = tk.StringVar()
actions = ('list', 'subscribe', 'party_status', 'gameboard_status', 'move')
action_menu = ttk.Combobox(frame, textvariable=action_var, values=actions)
action_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))
action_menu.current(0)

# Player name
ttk.Label(frame, text="Nom du joueur:").grid(row=1, column=0, sticky=tk.W)
entry_player = ttk.Entry(frame)
entry_player.grid(row=1, column=1, sticky=(tk.W, tk.E))

# Player ID
ttk.Label(frame, text="ID du joueur:").grid(row=2, column=0, sticky=tk.W)
entry_player_id = ttk.Entry(frame)
entry_player_id.grid(row=2, column=1, sticky=(tk.W, tk.E))

# Party ID
ttk.Label(frame, text="ID de la partie:").grid(row=3, column=0, sticky=tk.W)
entry_party = ttk.Entry(frame)
entry_party.grid(row=3, column=1, sticky=(tk.W, tk.E))

# Move
ttk.Label(frame, text="Move (ex: 01):").grid(row=4, column=0, sticky=tk.W)
entry_move = ttk.Entry(frame)
entry_move.grid(row=4, column=1, sticky=(tk.W, tk.E))

# Bouton envoyer
send_button = ttk.Button(frame, text="Envoyer", command=envoyer_commande)
send_button.grid(row=5, column=0, columnspan=2, pady=10)

# Zone de réponse
text_response = tk.Text(root, height=10, width=50)
text_response.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()