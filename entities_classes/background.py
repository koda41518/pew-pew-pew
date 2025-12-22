import pygame
import random

class StarField:
    def __init__(self, num_stars=1000, bounds=3000):
        self.stars = [
            {
                "pos": pygame.Vector2(random.randint(-bounds, bounds), random.randint(-bounds, bounds)),
                "depth": random.uniform(0.2, 1.0)  # ➤ Plus petit = plus loin
            } # les strars ont deux attributs la position et la profondeur
            for _ in range(num_stars)
        ]

    def draw(self, screen, offset, screen_size): #pour avoir l effet de parallaxe l'offset est definie selon la profondeur de chaque objet
        width, height = screen_size
        for star in self.stars:
            # Le fond éloigné bouge moins vite
            parallax_offset = offset * star["depth"]
            screen_pos = star["pos"] - parallax_offset

            if 0 <= screen_pos.x < width and 0 <= screen_pos.y < height:
                radius = max(1, int(2 * (1.1 - star["depth"])))  # ➤ plus proche = plus gros pour pousser l'effet de profondeur
                pygame.draw.circle(screen, (255, 255, 255), (int(screen_pos.x), int(screen_pos.y)), radius)