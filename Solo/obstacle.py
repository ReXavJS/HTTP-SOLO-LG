



class Obstacle:
    def __init__(self, position):
        self.position = position

    def dessiner(self, canvas, taille):
        x, y = self.position
        x1 = x * taille
        y1 = y * taille
        x2 = x1 + taille
        y2 = y1 + taille
        canvas.create_oval(x1, y1, x2, y2, fill="black")
