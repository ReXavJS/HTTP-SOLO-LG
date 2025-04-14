import random
from joueur import Joueur
from loup import Loup
from obstacle import Obstacle

class Terrain:
    def __init__(self, canvas, rows, cols, wait_time, max_turns, obstacles, role):
        self.canvas = canvas
        self.rows = rows
        self.cols = cols
        self.cell_size = min(600 // rows, 600 // cols)
        self.wait_time = wait_time
        self.max_turns = max_turns
        self.obstacle_count = obstacles
        self.role = role

        self.joueur = None
        self.adversaire = None
        self.obstacles = []
        self.tour = 0

        self.timer_actif = False
        self.timer_id = None

        self.init_elements()

    def init_elements(self):
        positions = [(x, y) for x in range(self.cols) for y in range(self.rows)]
        random.shuffle(positions)

        joueur_pos = positions.pop()
        adversaire_pos = positions.pop()

        if self.role == "villageois":
            self.joueur = Joueur(joueur_pos, couleur="blue")
            self.adversaire = Loup(adversaire_pos)
        else:
            self.joueur = Loup(joueur_pos)
            self.adversaire = Joueur(adversaire_pos, couleur="blue")

        for _ in range(self.obstacle_count):
            self.obstacles.append(Obstacle(positions.pop()))

    def dessiner(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

        for obs in self.obstacles:
            obs.dessiner(self.canvas, self.cell_size)

        if self.role == "villageois":
            self.joueur.dessiner(self.canvas, self.cell_size)
            self.adversaire.dessiner(self.canvas, self.cell_size)
        else:
            self.adversaire.dessiner(self.canvas, self.cell_size)
            self.joueur.dessiner(self.canvas, self.cell_size)

    def deplacer_joueur(self, direction):
        self.joueur.deplacer(direction, self.rows, self.cols)
        self.tour += 1

        if self.joueur.position == self.adversaire.position:
            self.dessiner()
            if self.role == "loup":
                return "Le loup a mangé le villageois ! Victoire."
            else:
                return "Le villageois a été mangé par le loup ! Défaite."

        elif any(obs.position == self.joueur.position for obs in self.obstacles):
            self.dessiner()
            return "Vous avez touché un obstacle ! Défaite."

        self.dessiner()
        return None

    def passer_tour(self):
        self.tour += 1
        self.dessiner()

    def est_fini(self):
        return self.tour >= self.max_turns

    def victoire_par_survie(self):
        if (
            self.joueur.position != self.adversaire.position
            and all(self.joueur.position != obs.position for obs in self.obstacles)
        ):
            return True
        return False
