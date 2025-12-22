import pygame
import sys

# Imports du projet
from core.GameManager import GameManager
from entities_classes.ship import Ship
from entities_classes.camera import Camera
from entities_classes.background import StarField
from entities_classes.screen_effects import DamageFlash
from ui.hud import HUD
from ui.pause_screen import PauseScreen
from ui.gameover_screen import GameOverScreen
from ui.minimap import MiniMapUI
from ui.main_menu import MainMenu
import settings


def reset_game(ship, manager):
    """Remet le jeu à zéro (vaisseau, score, ennemis, etc.)"""
    manager.reset()
    ship.reset((0, 0))
    ship.has_shield = False


def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    pygame.display.set_caption("Nebula Drift")
    clock = pygame.time.Clock()

    # UI
    hud = HUD(pygame.font.SysFont("Arial", 24))
    pause_screen = PauseScreen(settings.WIDTH, settings.HEIGHT, hud.font)
    gameover_screen = GameOverScreen(settings.WIDTH, settings.HEIGHT, hud.font)
    menu = MainMenu(settings.WIDTH, settings.HEIGHT, pygame.font.SysFont("Arial", 32))

    # Affiche le menu principal
    in_menu = True
    while in_menu:
        screen.fill((0, 0, 0))
        button_rect = menu.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            action = menu.handle_event(event, button_rect)
            if action == "start":
                in_menu = False
            elif action == "quit":
                pygame.quit()
                sys.exit()

    # === Initialisation des objets du jeu ===
    ship = Ship((0, 0), settings.SHIP_SPRITES)
    camera = Camera(ship.pos.copy()) #. hadiiiii ptnnnnn c est .copie qui change tout le vaisseau n est plus clouer au centre
    background = StarField()
    flash = DamageFlash()
    manager = GameManager()
    minimap = MiniMapUI()

    # États du jeu
    paused = False
    running = True
    high_score = 0
    button_rect = None

    # === Boucle principale ===
    while running:
        dt = clock.tick(settings.FPS) / 1000

        # === Gestion des événements ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_SPACE and not paused and not manager.game_over:
                    manager.fire_laser(ship.pos, ship.forward())

            if manager.game_over and button_rect:
                action = gameover_screen.handle_event(event, button_rect)
                if action == "replay":
                    reset_game(ship, manager)
                    paused = False
                    button_rect = None



        # === Dessin à l’écran ===
        screen.fill(settings.BACKGROUND_COLOR)
        offset = camera.get_offset((settings.WIDTH, settings.HEIGHT))
        background.draw(screen, camera.pos, (settings.WIDTH, settings.HEIGHT))

        # === Mise à jour ===
        if not paused and not manager.game_over:
            keys = pygame.key.get_pressed()
            ship.update(keys)
            camera.update(ship.pos, lerp_factor=0.05)
            manager.update(ship, dt)
            flash.update(dt)

        
        # Dessin des entités
        for entity_group in [manager.lasers, manager.enemies, manager.repairs, manager.shield_pickups]:
            for entity in entity_group:
                entity.draw(screen, offset)

        ship.draw(screen, offset)
        manager.flash.draw(screen)

        # UI
        minimap.draw(screen, ship.pos, manager.enemies, manager.repairs, manager.shield_pickups)
        hud.draw(screen, ship.speed, ship.health, manager.score)

        if paused:
            pause_screen.draw(screen)
        elif manager.game_over:
            if manager.score > high_score:
                high_score = manager.score
            button_rect = gameover_screen.draw(screen, manager.score, high_score)
        else:
            button_rect = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()