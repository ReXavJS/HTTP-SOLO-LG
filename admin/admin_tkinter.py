import tkinter as tk
from tkinter import messagebox

class AdminGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Console Admin - Création de Partie")
        self.geometry("400x400")
        self.entries = {}
        self._build_form()

    def _build_form(self):
        params = [
            ("Lignes", "rows"),
            ("Colonnes", "cols"),
            ("Obstacles", "nb_obstacles"),
            ("Joueurs max", "max_players"),
            ("Tours max", "nb_turns"),
            ("Temps max/tour (s)", "turn_timeout")
        ]

        for i, (label_text, key) in enumerate(params):
            tk.Label(self, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(self)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[key] = entry

        tk.Button(self, text="Créer la partie", command=self.collect_data).grid(columnspan=2, pady=20)

    def collect_data(self):
        try:
            partie = {key: int(entry.get()) for key, entry in self.entries.items()}
            msg = "\n".join(f"{k} : {v}" for k, v in partie.items())
            messagebox.showinfo("Paramètres enregistrés", msg)
            print("Paramètres de la partie :", partie)
        except ValueError:
            messagebox.showerror("Erreur", "Tous les champs doivent contenir des nombres entiers.")

if __name__ == "__main__":
    app = AdminGUI()
    app.mainloop()
