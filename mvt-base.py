import pygame
import math
import random

# 🛠 Initialisation globale du jeu
pygame.init()
WIDTH, HEIGHT = 1300, 900  # 📺 Taille de la bigass fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PEW PEW PEW")  # Nom de la fenêtre
clock = pygame.time.Clock() # le frame rate 🏃‍♀️‍➡️
font = pygame.font.SysFont("Arial", 24)  #  Police pour le texte

high_score = 0  # 🏆 Meilleur score stocké en mémoire
# dans ce code koulchi 3la l'offset dinguerie comment il est à la base du gameplay
#les 🤸‍♀️ c est pour ls facteur  ou changer la dificulter  et 🧙‍♂️ les remarques
#on peut essayer de faire un systeme de niveau oula plusieurs type de vaisseau ou d ennemie en changeant les 🤸‍♀️
def main():
    global high_score # comme ça on garde le high score 
    paused = False  # ⏸️ État de pause du jeu

    # 🚀 Variables du joueur (vaisseau)
    ship_pos = pygame.Vector2(0, 0) 
    ship_angle =90 # bach iban kay chouf lfou9 ⬆️
    ship_speed = pygame.Vector2(0, 0) # et oee c est un vecteur 
    acceleration = 0.15 # 🤸‍♀️on peut changer la difficulter du jeu selon l'acceleration
    rotation_speed = 3 # 🤸‍♀️on peut changer le drifting du vaisseau
    friction = 0.99

    camera_pos = ship_pos.copy() # la camera suit le vaisseau
    score = 0
    player_health = 100  # 🤸‍♀️ on peut rajouter un mode extreme ou on met 1 blast 100
    enemy_damage = 25 # dégâts de l'ennemi 🤸‍♀️on peut changer la difficulter
    laser_damage_radius = 20 # la zone de degat  🤸‍♀️ on peut changer la difficulter (ila kber c est plus facile)
    laser_speed = 1000  #  Super rapide 🧙‍♂️ce serait stupid de depasser la "lumière"
    laser_lifetime = 1.5  # ⏱ Temps avant que le laser disparaisse
    damage_flash_timer = 0  #  Durée du flash rouge quand on prend un coup

    #  Listes d’objets en jeu
    enemies = []
    lasers = []
    repairs = []
    repair_timer = 0

    #  Génération aléatoire des étoiles de fond
    stars = [(pygame.Vector2(random.randint(-3000, 3000), random.randint(-3000, 3000)), random.randint(1, 3)) for _ in range(1000)] # cree un liste random de 1000 etoile 
    # 🕺🏼 pour crée un effet de paralaxe jvais modif la liste
    #j ai ajouter une profondeur a chaque etoile au pif de 1 à 3 telle que etoile = (position, profondeur)

    #  Fonction pour faire apparaître un ennemi aléatoirement autour du joueur
    def spawn_enemy():
        angle = random.uniform(0, 2 * math.pi) # 🧙‍♂️ coordonner cylindrique lol (r,θ)
        distance = random.randint(800, 1200)
        offset = pygame.Vector2(math.cos(angle), math.sin(angle)) * distance # cree un vecteur avec les deux variable angle et distance 
        return {"pos": ship_pos + offset, "speed": 1.2} # cree un dic de la position et la vitesse 1.2 🤸‍♀️ on peut la changer pour augmentere la diffuculte
    

    #  Fonction pour faire apparaître un point de réparation
    def spawn_repair():
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(800, 1600)
        offset = pygame.Vector2(math.cos(angle), math.sin(angle)) * distance
        return {"pos": ship_pos + offset} # tout pareil mais sans la vitesse 🤸‍♀️ on peut augmenter la difficulte en changeant la distance 

    spawn_timer = 0
    running = True
    game_over = False

    #  Boucle principale du jeu
    while running:
        dt = clock.tick(60) / 1000  # Temps écoulé depuis la dernière frame (pour mouvements fluides)
        screen.fill((10, 10, 30))  # Fond bleu nuit

        # 🎮 Gestion des entrées (clavier)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # ⏯️ Pause / Reprise
                elif event.key == pygame.K_SPACE and not paused:
                    #  Créer un laser dans la direction du vaisseau
                    angle_rad = math.radians(ship_angle) # converti en rad 🤸‍♀️ si on change l'angle le vaisseau pourra tirer dan d'autre direction
                    direction = pygame.Vector2(math.cos(angle_rad), -math.sin(angle_rad)) # crée un vecteur direction selon l'angle du vaisseau
                    lasers.append({"pos": pygame.Vector2(ship_pos), "dir": direction, "life": 0.0}) # ajoute les info du laser dans la liste 

        # ⏸ Affichage pause
        if paused:
            pause_text = font.render("⏸ JEU EN PAUSE - Appuie sur ÉCHAP pour reprendre", True, (255, 255, 100))
            screen.blit(pause_text, (WIDTH // 2 - 300, HEIGHT // 2))
            pygame.display.flip() # le flip c est pour afficher tout en une fois sans decalage
            continue # le continue saute le reste des instructions et recommence la boucle while 

        #  Contrôles de mouvement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: # ⬅️
            ship_angle += rotation_speed # driftiiing hell yeaah 🧙‍♂️c est l'un des variable initialiser au deeebut du jeu 
        if keys[pygame.K_RIGHT]: # ➡️
            ship_angle -= rotation_speed
        if keys[pygame.K_UP]: # ⬆️
            angle_rad = math.radians(ship_angle)
            direction = pygame.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
            #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            # je vais enlever l'acceleraction :ship_speed += direction  
            #wooooow wa kay tir c est une dinguerie c est le saut  vitesse lumiere star wars kay khrej de l'ecran sbe9 les laser lol
            #dooonc si had l'acceleration quand elle = 1 il se teleporte quasiment si elle est nul en theorie le vaisseau ne bouge pas du centre 
            # nope c est pas ça il reste peut etre au centre mais il avance pas ga3 
            
            ship_speed += direction * acceleration  #  🧙‍♂️formule physique lol 
            
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #  Physique du vaisseau
        ship_speed *= friction # comme ça on avance a  ∞ mec j ai juste mis *2 il a quité le jeu tellement on allait vite bahahaha
        # 🧍‍♀️ ptnnnn cest normale de baaaase c'est pour reduire la vitesse ou ana ki chi kheria ça n'a pas arreter d'accelerer et meme pas  au bout d'une seconde khrej
        ship_pos += ship_speed #le nom est trompeur en sa7 j aurais du l appeler ship_deplacement 
        camera_pos += (ship_pos - camera_pos) * 0.05  #  Caméra qui suit doucement 🧙‍♂️ le fameux decalaaaage 
        offset = camera_pos - pygame.Vector2(WIDTH // 2, HEIGHT // 2) # calcul pour recentrer la camera ,(WIDTH // 2, HEIGHT // 2) c est les coordonner du centre de l'ecran

        #  Affichage des étoiles
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #on va ajouter un effet de parallaxe ila bgha
        bounds = 3000
        for star in stars: # star = (position (x,y), profondeur z)
            pos = star[0] #(x,y)
            profondeur = star[1] # z
            # 1. Calcul de la position relative (avec parallaxe)
            # Plus depth est grand, plus l'étoile est "loin" et bouge lentement
            rel_x = pos.x - (offset.x / profondeur)
            rel_y = pos.y - (offset.y / profondeur)
            # 2. Le Wrapping par Modulo ✨ 
            # On ramène rel_x dans l'intervalle [-3000, 3000]
            render_x = (rel_x + bounds) % (2 * bounds) - bounds # on peut  appeler .x et .y parcequ on a l a definie avec Vector2
            """ (rel_x + bounds) :  on mettant + bounds pour eviter les valeurs negatives
                %(2 * bounds)    :   ensuite on fait le modulo pour ramener dans [0, 6000]
                - bounds         :  et enfin on remet dans [-3000, 3000] en enlevant bounds"""
            render_y = (rel_y + bounds) % (2 * bounds) - bounds
            # 3. Conversion en coordonnées écran (centrage)
            screen_x = render_x + WIDTH // 2  #  + WIDTH // 2 pour centrer l'étoile à l'écran
            screen_y = render_y + HEIGHT // 2
            # 4. Affichage (seulement si c'est dans la vue)
            if 0 <= screen_x < WIDTH and 0 <= screen_y < HEIGHT:
                # On ajuste la taille selon la profondeur
                radius = 1 if profondeur > 2 else 2 
                pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), radius)

        #  Apparition régulière des ennemis
        spawn_timer += dt
        if spawn_timer >= 2: # apparition toutes les 2 secondes 🤸‍♀️ on peut changer la difficulter en changeant cette valeur
            enemies.append(spawn_enemy())
            spawn_timer = 0

        #  Apparition des points de réparation
        repair_timer += dt 
        if repair_timer >= 5: # pareil 🤸‍♀️ on peut augmenter  la difficulter en baisssant  5
            repairs.append(spawn_repair())
            repair_timer = 0

        #  Ennemis : déplacement + collision avec joueur
        for enemy in enemies[:]: # 🧙‍♂️ le [:] c est pour faire une copie et pas endommager la liste de base
            enemy["pos"] += (ship_pos - enemy["pos"]).normalize() * enemy["speed"] # l'ennemi reduit sa distance avec le joueur 🧙‍♂️ normalize c est vrm pour avoir seulement la direction du vecteur sans sa norme
            if enemy["pos"].distance_to(ship_pos) < 30: # 30 px 🧙‍♂️
                player_health -= enemy_damage
                damage_flash_timer = 0.3  # 🧙‍♂️ Déclenche le flash rouge
                enemies.remove(enemy)
                continue # 🧙‍♂️ on sort de la boucle for pour cet ennemi vu qu il s'est suicider mskine en vrai c est des kamikaze 🥀
            screen_pos = enemy["pos"] - offset
            pygame.draw.circle(screen, (255, 50, 50), (int(screen_pos.x), int(screen_pos.y)), 12)

        #  Lasers : déplacement + collisions avec ennemis
        for laser in lasers[:]:
            laser["pos"] += laser["dir"] * laser_speed * dt #la definition du mvt litteralement 🧙‍♂️
            laser["life"] += dt

            for enemy in enemies[:]:
                if laser["pos"].distance_to(enemy["pos"]) < laser_damage_radius:
                    enemies.remove(enemy)
                    if laser in lasers:
                        lasers.remove(laser)
                    score += 1
                    break

            screen_pos = laser["pos"] - offset
            if laser["life"] > laser_lifetime or not (0 <= screen_pos.x < WIDTH and 0 <= screen_pos.y < HEIGHT):
                if laser in lasers:
                    lasers.remove(laser)
            else:
                pygame.draw.line(screen, (255, 80, 80), screen_pos, screen_pos + laser["dir"] * 20, 3)

        #  Réparations : affichage + collisions
        for repair in repairs[:]:
            if ship_pos.distance_to(repair["pos"]) < 30:
                player_health = min(player_health + 20, 100)  #  Ne dépasse pas 100
                repairs.remove(repair)
                continue
            screen_pos = repair["pos"] - offset
            pygame.draw.circle(screen, (50, 255, 50), (int(screen_pos.x), int(screen_pos.y)), 10)

        # 🚀Affichage du vaisseau
        def draw_ship(pos, angle):
            angle_rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(angle_rad), -math.sin(angle_rad))
            perp = direction.rotate(90)
            p1 = pos + direction * 20
            p2 = pos - direction * 10 + perp * 10
            p3 = pos - direction * 10 - perp * 10
            pygame.draw.polygon(screen, (200, 200, 255), [p1, p2, p3])

        draw_ship(ship_pos - offset, ship_angle)

        #  Flash rouge en cas de dégâts
        if damage_flash_timer > 0:
            damage_flash_timer -= dt
            flash_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(255 * (damage_flash_timer / 0.3))
            alpha = max(0, min(255, alpha))
            flash_surface.fill((255, 0, 0, alpha))
            screen.blit(flash_surface, (0, 0))

        #  Interface : vitesse, vie, score
        screen.blit(font.render(f"Vitesse : {ship_speed.length():.2f}", True, (255, 255, 255)), (10, 10))
        screen.blit(font.render(f"Vie : {player_health}", True, (255, 50, 50)), (10, 40))
        screen.blit(font.render(f"Score : {score}", True, (255, 255, 255)), (10, 70))

        #  Mini-map
        minimap_size = 200 # petit carré 🧙‍♂️
        minimap_scale = 0.05 # facteur de reduction 🧙‍♂️
        minimap_surface = pygame.Surface((minimap_size, minimap_size))
        minimap_surface.fill((20, 20, 40))
        center = pygame.Vector2(minimap_size // 2, minimap_size // 2)
        pygame.draw.circle(minimap_surface, (200, 200, 255), center, 5)

        for enemy in enemies:
            rel_pos = (enemy["pos"] - ship_pos) * minimap_scale #  🧙‍♂️tout pareil multiplié par le facteur de reduction
            map_pos = center + rel_pos
            if 0 <= map_pos.x < minimap_size and 0 <= map_pos.y < minimap_size:
                pygame.draw.circle(minimap_surface, (255, 60, 60), (int(map_pos.x), int(map_pos.y)), 3)

        for repair in repairs:
            rel_pos = (repair["pos"] - ship_pos) * minimap_scale
            map_pos = center + rel_pos
            if 0 <= map_pos.x < minimap_size and 0 <= map_pos.y < minimap_size:
                pygame.draw.circle(minimap_surface, (60, 255, 60), (int(map_pos.x), int(map_pos.y)), 3)

        screen.blit(minimap_surface, (WIDTH - minimap_size - 20, HEIGHT - minimap_size - 20))

        pygame.display.flip()

        #  Vérifie si le joueur est mort
        if player_health <= 0:
            game_over = True
            if score > high_score:
                high_score = score
            break

    # Écran de fin
    if game_over:
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50)
        while True:
            screen.fill((0, 0, 0))
            screen.blit(font.render("GAME OVER", True, (255, 0, 0)), (WIDTH // 2 - 100, HEIGHT // 2 - 80))
            screen.blit(font.render(f"Score : {score} ennemis détruits", True, (255, 255, 255)), (WIDTH // 2 - 140, HEIGHT // 2 - 20))
            screen.blit(font.render(f"Meilleur score : {high_score}", True, (200, 200, 255)), (WIDTH // 2 - 140, HEIGHT // 2 + 20))
            screen.blit(font.render("Clique sur 'Rejouer' ou ferme la fenêtre", True, (180, 180, 180)), (WIDTH // 2 - 180, HEIGHT // 2 + 50))
            pygame.draw.rect(screen, (255, 255, 255), button_rect)
            screen.blit(font.render("Rejouer", True, (0, 0, 0)), (button_rect.x + 50, button_rect.y + 10))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        main()
                        return

# Lancement initial
main()
pygame.quit()