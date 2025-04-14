import tkinter as tk
from terrain import Terrain

class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Jeu du Loup")

        self.config_frame = tk.Frame(self.root)
        self.config_frame.pack()

        self.entries = {}
        self.role_var = tk.StringVar()
        self.role_var.set("villageois")

        self.create_config_inputs()
        self.start_button = tk.Button(self.root, text="Lancer le jeu", command=self.start_game)
        self.start_button.pack()

        self.canvas = None
        self.terrain = None
        self.timer_label = None
        self.remaining_time = 0
        self.countdown_id = None

    def create_config_inputs(self):
        fields = [
            ("Nombre de lignes", "rows"),
            ("Nombre de colonnes", "cols"),
            ("Temps max par tour (secondes)", "wait_time"),
            ("Nombre de tours", "max_turns"),
            ("Nombre d'obstacles", "obstacles"),
        ]
        for label, key in fields:
            tk.Label(self.config_frame, text=label).pack()
            entry = tk.Entry(self.config_frame)
            entry.pack()
            self.entries[key] = entry

        tk.Label(self.config_frame, text="Choisir votre rôle").pack()
        tk.OptionMenu(self.config_frame, self.role_var, "villageois", "loup").pack()

    def start_game(self):
        config = {key: int(entry.get()) for key, entry in self.entries.items()}
        config["wait_time"] *= 1000
        config["role"] = self.role_var.get()

        self.config_frame.pack_forget()
        self.start_button.pack_forget()

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14), fg="green")
        self.timer_label.pack()

        self.terrain = Terrain(self.canvas, **config)
        self.terrain.dessiner()

        self.root.bind("<Up>", lambda e: self.jouer_tour("haut"))
        self.root.bind("<Down>", lambda e: self.jouer_tour("bas"))
        self.root.bind("<Left>", lambda e: self.jouer_tour("gauche"))
        self.root.bind("<Right>", lambda e: self.jouer_tour("droite"))
        self.root.bind("<space>", lambda e: self.passer_tour_manu())

        self.demarrer_tour()

    def jouer_tour(self, direction):
        if self.terrain.timer_actif:
            if self.terrain.timer_id is not None:
                self.root.after_cancel(self.terrain.timer_id)
            if self.countdown_id is not None:
                self.root.after_cancel(self.countdown_id)

            self.terrain.timer_actif = False
            result = self.terrain.deplacer_joueur(direction)
            if result:
                self.timer_label.config(text=result)

            if self.terrain.est_fini():
                if self.terrain.etat_partie == "victoire":
                    self.timer_label.config(text="Victoire ! Le loup a mangé le villageois !")
                elif self.terrain.etat_partie == "defaite":
                    self.timer_label.config(text="Défaite ! Le villageois a été mangé par le loup.")
                elif self.terrain.victoire_par_survie():
                    self.timer_label.config(text="Victoire ! Le villageois a survécu !")
                else:
                    self.timer_label.config(text="Défaite ! Le villageois a survécu.")
            elif result is None or ("Victoire" not in result and "Défaite" not in result):
                self.demarrer_tour()

    def passer_tour_manu(self):
        if self.terrain.timer_actif:
            if self.terrain.timer_id:
                self.root.after_cancel(self.terrain.timer_id)
            if self.countdown_id:
                self.root.after_cancel(self.countdown_id)

            self.terrain.timer_actif = False
            self.terrain.passer_tour()

            if self.terrain.est_fini():
                if self.terrain.etat_partie == "victoire":
                    self.timer_label.config(text="Victoire ! Le loup a mangé le villageois !")
                elif self.terrain.etat_partie == "defaite":
                    self.timer_label.config(text="Défaite ! Le villageois a été mangé par le loup.")
                elif self.terrain.victoire_par_survie():
                    self.timer_label.config(text="Victoire ! Le villageois a survécu !")
                else:
                    self.timer_label.config(text="Défaite ! Le villageois a survécu.")
            else:
                self.demarrer_tour()

    def demarrer_tour(self):
        if self.terrain.est_fini():
            if self.terrain.etat_partie == "victoire":
                self.timer_label.config(text="Victoire ! Le loup a mangé le villageois !")
            elif self.terrain.etat_partie == "defaite":
                self.timer_label.config(text="Défaite ! Le villageois a été mangé par le loup.")
            elif self.terrain.victoire_par_survie():
                self.timer_label.config(text="Victoire ! Le villageois a survécu !")
            else:
                self.timer_label.config(text="Défaite ! Le villageois a survécu.")
            return

        self.terrain.timer_actif = True
        self.remaining_time = self.terrain.wait_time // 1000
        self.update_timer_display()
        self.countdown()

        self.terrain.timer_id = self.root.after(self.terrain.wait_time, self.tour_expire)

    def countdown(self):
        if self.remaining_time > 0:
            self.update_timer_display()
            self.remaining_time -= 1
            self.countdown_id = self.root.after(1000, self.countdown)
        else:
            self.timer_label.config(text="⏳ Temps écoulé !")

    def update_timer_display(self):
        self.timer_label.config(
            text=f"⏳ Temps : {self.remaining_time}s | Tour : {self.terrain.tour + 1}/{self.terrain.max_turns}"
        )

    def tour_expire(self):
        self.terrain.passer_tour()
        self.terrain.timer_actif = False

        if self.terrain.est_fini():
            if self.terrain.etat_partie == "victoire":
                self.timer_label.config(text="Victoire ! Le loup a mangé le villageois !")
            elif self.terrain.etat_partie == "defaite":
                self.timer_label.config(text="Défaite ! Le villageois a été mangé par le loup.")
            elif self.terrain.victoire_par_survie():
                self.timer_label.config(text="Victoire ! Le villageois a survécu !")
            else:
                self.timer_label.config(text="Défaite ! Le villageois a survécu.")
        else:
            self.demarrer_tour()

    def run(self):
        self.root.mainloop()
