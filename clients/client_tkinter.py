import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://localhost:5000"

class LesLoupsClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Client Les Loups !")
        self.geometry("500x600")
        
        self.party_id = None
        self.player_id = None

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="ID de la Partie").pack()
        self.entry_party = tk.Entry(self)
        self.entry_party.pack()

        tk.Label(self, text="Nom du Joueur").pack()
        self.entry_player = tk.Entry(self)
        self.entry_player.pack()

        tk.Button(self, text="Rejoindre", command=self.join_party).pack(pady=10)

        self.board_frame = tk.Frame(self)
        self.board_frame.pack(pady=10)

        move_frame = tk.Frame(self)
        move_frame.pack()

        tk.Button(move_frame, text="↑", width=5, command=lambda: self.send_move(-1, 0)).grid(row=0, column=1)
        tk.Button(move_frame, text="←", width=5, command=lambda: self.send_move(0, -1)).grid(row=1, column=0)

        tk.Button(move_frame, text=" ", width=5, command=lambda: self.send_move(0, 0)).grid(row=1, column=1)

        tk.Button(move_frame, text="→", width=5, command=lambda: self.send_move(0, 1)).grid(row=1, column=2)
        tk.Button(move_frame, text="↓", width=5, command=lambda: self.send_move(1, 0)).grid(row=2, column=1)

        self.console = tk.Text(self, height=10)
        self.console.pack(pady=10)

    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

    def join_party(self):
        try:
            party_id = int(self.entry_party.get())
            player_name = self.entry_player.get()

            res = requests.post(f"{BASE_URL}/parties/{party_id}/join", json={"player_name": player_name})
            data = res.json()

            if data["status"] == "OK":
                self.party_id = party_id
                self.player_id = data["id_player"]
                self.log(f"Connecté à la partie {party_id} comme {data['role']} (ID: {self.player_id})")
                self.refresh_board()
            else:
                messagebox.showerror("Erreur", "Impossible de rejoindre la partie")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_board(self):
        try:
            if self.party_id and self.player_id:
                res = requests.get(f"{BASE_URL}/parties/{self.party_id}/board", params={"player_id": self.player_id})
                data = res.json()
                board = data["board"]
                self.display_board(board)
        except Exception as e:
            self.log("Erreur plateau : " + str(e))

    def display_board(self, board):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        for i, row in enumerate(board):
            for j, cell in enumerate(row):
                label = tk.Label(self.board_frame, text=str(cell), borderwidth=1, width=4, height=2, relief="solid")
                label.grid(row=i, column=j)

    def send_move(self, dx, dy):
        if not self.party_id or not self.player_id:
            messagebox.showwarning("Non connecté", "Rejoignez d'abord une partie")
            return

        move = f"{dx}{dy}"
        try:
            res = requests.post(
                f"{BASE_URL}/parties/{self.party_id}/move",
                json={"player_id": self.player_id, "move": move}
            )
            data = res.json()
            if data["status"] == "OK":
                if dx == 0 and dy == 0:
                    self.log("Tour passé.")
                else:
                    self.log(f"Déplacement effectué vers ({dx}, {dy})")
                self.refresh_board()
            else:
                self.log("Action refusée.")
        except Exception as e:
            self.log("Erreur mouvement : " + str(e))


if __name__ == "__main__":
    app = LesLoupsClient()
    app.mainloop()
