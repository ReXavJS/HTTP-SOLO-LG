class Joueur:
    def __init__(self, position, couleur="blue"):
        self.position = position
        self.couleur = couleur

    def deplacer(self, direction, rows, cols):
        x, y = self.position
        if direction == "haut" and y > 0:
            y -= 1
        elif direction == "bas" and y < rows - 1:
            y += 1
        elif direction == "gauche" and x > 0:
            x -= 1
        elif direction == "droite" and x < cols - 1:
            x += 1
        self.position = (x, y)

    def dessiner(self, canvas, taille):
        x, y = self.position
        x1 = x * taille
        y1 = y * taille
        x2 = x1 + taille
        y2 = y1 + taille
        canvas.create_oval(x1, y1, x2, y2, fill=self.couleur)
