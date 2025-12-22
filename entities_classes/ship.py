import pygame
import math

class Ship:
    def __init__(self, pos, sprites):
        self.pos = pygame.Vector2(pos)
        self.angle = 0
        self.speed = pygame.Vector2(0, 0)
        self.acceleration = 0.15
        self.rotation_speed = 3
        self.friction = 0.99

        self.health = 100
        self.max_health = 100
        self.has_shield = False  # bouclier desactivé
        self.invincible_timer = 0

        # 🔁 Chargement des sprites (statiques) 🤸‍♀️
        self.sprites = {
            "idle": pygame.transform.scale(
                pygame.image.load(sprites["idle"]).convert_alpha(), (128, 128)
            ),
            "move": pygame.transform.scale(
                pygame.image.load(sprites["move"]).convert_alpha(), (128, 128)
            )
        }

        # 🔁 Chargement des frames d'animation (thrust / boost)
        self.boost_frames = [
            pygame.transform.scale(
                pygame.image.load(sprites["thrust"]).convert_alpha(), (128, 128)
            ),
            pygame.transform.scale(
                pygame.image.load(sprites["boost"]).convert_alpha(), (128, 128)
            )
        ]
        #sprite du bouclier 
        self.shield_image = pygame.transform.scale(
            pygame.image.load(sprites["shield"]).convert_alpha(), (140, 140)
        )
        # Animation setup 🕺🏼
        self.boost_index = 0
        self.boost_timer = 0
        self.boost_speed = 0.1  # secondes entre deux frames

        # Sprite affiché actuellement
        self.current_sprite = self.sprites["idle"]
    def reset(self, pos):
        self.pos = pygame.Vector2(pos)
        self.angle = 0
        self.speed = pygame.Vector2(0, 0)
        self.current_sprite = self.sprites["idle"]
        self.has_shield = False
        self.invincible_timer = 0
        self.health = self.max_health
        
    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_UP]:
            direction = self.forward()
            self.speed += direction * self.acceleration

            # 🎞️ Animation boost
            self.boost_timer += 1 / 60  # ou dt si on veut passer le temps réel
            if self.boost_timer >= self.boost_speed:
                self.boost_index = (self.boost_index + 1) % len(self.boost_frames)
                self.boost_timer = 0

            self.current_sprite = self.boost_frames[self.boost_index]

        else:
            self.current_sprite = self.sprites["idle"]

        self.speed *= self.friction
        self.pos += self.speed 
        if self.invincible_timer > 0:
            self.invincible_timer -= 1 / 60  # 
        
        
        
    def take_damage(self, amount):
        if self.invincible_timer > 0:
            #print("⏳ Invincible, aucun dégât.")
            return

        #print("Has shield:", self.has_shield)
        if self.has_shield:
            #print("💥 Bouclier absorbé !")
            self.has_shield = False
        else:
            #print("❤️🥀oh nooowh Vie perdue !")
            self.health = max(0, self.health - amount)

        self.invincible_timer = 1.0  # 1 seconde d’invincibilité
    
    def heal(self, amount):
        """Soigne le vaisseau d’un certain montant, sans dépasser la vie max."""
        self.health = min(self.max_health, self.health + amount)

    def is_alive(self):
        return self.health > 0
    
    

    def draw(self, screen, offset):
        center = self.pos - offset

        # 🔁 Dessiner le vaisseau
        rotated_img = pygame.transform.rotate(self.current_sprite, -self.angle)
        rect = rotated_img.get_rect(center=center)
        screen.blit(rotated_img, rect)

        # 🛡️ Dessiner le bouclier par-dessus
        if self.has_shield:
            rotated_shield = pygame.transform.rotate(self.shield_image, -self.angle)
            shield_rect = rotated_shield.get_rect(center=center)
            rotated_shield.set_alpha(150)  # Optionnel : rend le bouclier semi-transparent
            screen.blit(rotated_shield, shield_rect)
    def forward(self):
        """
        Retourne un vecteur directionnel basé sur l'angle du vaisseau.
        Ici, angle 0 = vers le haut.
        """
        angle_rad = math.radians(self.angle)
        return pygame.Vector2(math.sin(angle_rad), -math.cos(angle_rad))