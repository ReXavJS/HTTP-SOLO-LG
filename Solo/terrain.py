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

        self.etat_partie = None
        self.timer_actif = False
        self.timer_id = None

        self.init_elements()

    def init_elements(self):
        def adjacent(pos):
            x, y = pos
            return {(x+dx, y+dy) for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)] if 0 <= x+dx < self.cols and 0 <= y+dy < self.rows}

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

        forbidden = {joueur_pos, adversaire_pos} | adjacent(adversaire_pos)
        free_positions = [p for p in positions if p not in forbidden]
        for _ in range(self.obstacle_count):
            if free_positions:
                self.obstacles.append(Obstacle(free_positions.pop()))

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

        if isinstance(self.joueur, Loup):
            self.adversaire.dessiner(self.canvas, self.cell_size)
            self.joueur.dessiner(self.canvas, self.cell_size)
        else:
            self.joueur.dessiner(self.canvas, self.cell_size)
            self.adversaire.dessiner(self.canvas, self.cell_size)

    def deplacer_joueur(self, direction):
        x, y = self.joueur.position
        nx, ny = x, y

        if direction == "haut":
            ny -= 1
        elif direction == "bas":
            ny += 1
        elif direction == "gauche":
            nx -= 1
        elif direction == "droite":
            nx += 1
        else:
            self.tour += 1
            self.dessiner()
            return "Tour perdu (commande invalide)."

        if not (0 <= nx < self.cols and 0 <= ny < self.rows):
            self.tour += 1
            self.dessiner()
            return "Tour perdu (hors de la carte)."

        if any((nx, ny) == obs.position for obs in self.obstacles):
            self.tour += 1
            self.dessiner()
            return "Tour perdu (case occupée par un obstacle)."

        if (nx, ny) == self.adversaire.position:
            self.joueur.position = (nx, ny)
            self.tour += 1
            self.dessiner()
            if self.role == "loup":
                self.etat_partie = "victoire"
                return "Victoire ! Le loup a mangé le villageois !"
            else:
                self.etat_partie = "defaite"
                return "Défaite ! Le villageois a été mangé par le loup !"

        self.joueur.position = (nx, ny)
        self.tour += 1
        self.dessiner()
        return None

    def passer_tour(self):
        self.tour += 1
        self.dessiner()

    def est_fini(self):
        return self.tour >= self.max_turns or self.etat_partie is not None

    def victoire_par_survie(self):
        return self.etat_partie is None and self.role == "villageois"
