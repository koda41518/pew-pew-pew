import pygame
import random

class StarField:
    
    def __init__(self, num_stars=1000, bounds=3000):
        self.stars = [
            {
                "pos": pygame.Vector2(random.randint(-bounds, bounds), random.randint(-bounds, bounds)),
                "depth": random.randint(1, 3)  # ➤ Plus petit = plus loin
            } # les strars ont deux attributs la position et la profondeur
            for _ in range(num_stars)
        ]

    def draw(self, screen, offset, screen_size): #pour avoir l effet de parallaxe l'offset est definie selon la profondeur de chaque objet
        width, height = screen_size
        bounds = 3000
        for star in self.stars:
            # Le fond éloigné bouge moins vite
            rel_x = star["pos"].x - (offset.x / star["depth"])
            rel_y = star["pos"].y - (offset.y / star["depth"])

            render_x = (rel_x + bounds) % (2 * bounds) - bounds
            render_y = (rel_y + bounds) % (2 * bounds) - bounds

            screen_x = render_x + width // 2  #  + WIDTH // 2 pour centrer l'étoile à l'écran
            screen_y = render_y + height // 2

            """parallax_offset = offset * star["depth"]
            screen_pos = star["pos"] - parallax_offset

            if 0 <= screen_pos.x < width and 0 <= screen_pos.y < height:
                radius = max(1, int(2 * (1.1 - star["depth"])))  # ➤ plus proche = plus gros pour pousser l'effet de profondeur
                pygame.draw.circle(screen, (255, 255, 255), (int(screen_pos.x), int(screen_pos.y)), radius)"""
            

            if 0 <= screen_x < width and 0 <= screen_y < height:
                # On ajuste la taille selon la profondeur
                radius = 1 if star["depth"] < 0.6 else 2
                pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), radius)