import pygame
import sys
import os
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOWWIDTH, WINDOWHEIGHT = 800, 800
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption("Dodger")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXTCOLOR = BLACK
BACKGROUNDCOLOR = WHITE

# Variables de sélection de personnage
selected_character = 0
player_name = ""
game_started = False
in_game = False
character_images = []
characterimage = None
entering_name = True

# Charger les images de personnages
for i in range(1, 4):
    image_path = f"character{i}.png"
    if os.path.exists(image_path):
        character_images.append(pygame.image.load(image_path))
    else:
        print(f"Erreur : L'image {image_path} est introuvable.")
        sys.exit()

# Redimensionner les images des personnages
character_images = [pygame.transform.scale(img, (50, 50)) for img in character_images]

# Initialiser les paramètres de jeu
paused = False
FPS_initiale = 30
FPS = FPS_initiale
mainClock = pygame.time.Clock()

# Charger les sons
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Charger les images pour le jeu
baddieImage = pygame.image.load('baddie.png')
spaceshipImage = pygame.image.load('space.png')

# Polices
font = pygame.font.SysFont(None, 48)
large_font = pygame.font.SysFont(None, 72)

# Fonctions utilitaires
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def drawText(text, font, surface, x, y, center=False):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Boucle de sélection de personnage et saisie de nom
while not game_started:
    windowSurface.fill(WHITE)
    drawText("Entrez votre nom:", font, windowSurface, WINDOWWIDTH // 2, 50, center=True)
    drawText(player_name, font, windowSurface, WINDOWWIDTH // 2, 100, center=True)

    if not entering_name:
        drawText("Choisissez votre personnage", large_font, windowSurface, WINDOWWIDTH // 2, 200, center=True)
        for i, img in enumerate(character_images):
            x = WINDOWWIDTH // (len(character_images) + 1) * (i + 1)
            y = WINDOWHEIGHT // 2
            windowSurface.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
            if i == selected_character:
                pygame.draw.rect(windowSurface, BLACK, (x - img.get_width() // 2, y - img.get_height() // 2, img.get_width(), img.get_height()), 3)

        drawText("Appuyez sur Entrée pour confirmer", font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        elif event.type == pygame.KEYDOWN:
            if entering_name:
                if event.key == pygame.K_RETURN:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode
            else:
                if event.key == pygame.K_LEFT:
                    selected_character = (selected_character - 1) % len(character_images)
                elif event.key == pygame.K_RIGHT:
                    selected_character = (selected_character + 1) % len(character_images)
                elif event.key == pygame.K_RETURN:
                    characterimage = character_images[selected_character]
                    game_started = True
                    in_game = True

    pygame.display.update()

# Affichage du compte à rebours avant le début du jeu
def countdown():
    for count in range(3, 0, -1):
        windowSurface.fill(WHITE)
        drawText(f"{player_name}, prêt(e) ?", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3, center=True)
        windowSurface.blit(characterimage, (WINDOWWIDTH // 2 - characterimage.get_width() // 2, WINDOWHEIGHT // 2 - characterimage.get_height() // 2))
        drawText(f"Début dans {count}", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)
        pygame.display.update()
        pygame.time.wait(1000)

    windowSurface.fill(WHITE)
    drawText("GO !", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
    pygame.display.update()
    pygame.time.wait(1000)

countdown()

# Variables de jeu
playerImage = characterimage
playerRect = playerImage.get_rect()
baddies = []
score = 0
topScore = 0
lives = 3
paused = False

# Boucle principale du jeu
while True:
    if not in_game:
        # Écran de pause
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText("Dodger", font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3, center=True)
        drawText("Press a key to start.", font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3 + 50, center=True)
        pygame.display.update()
        waitForPlayerToPressKey()
        in_game = True

    baddies = []
    score = 0
    lives = 3
    playerRect.topleft = (20, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    # Boucle du jeu
    while in_game:
        if not paused:
            score += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        terminate()
                    elif event.key == pygame.K_p:
                        paused = not paused
                    if event.key == pygame.K_LEFT:
                        moveLeft = True
                    if event.key == pygame.K_RIGHT:
                        moveRight = True
                    if event.key == pygame.K_UP:
                        moveUp = True
                    if event.key == pygame.K_DOWN:
                        moveDown = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        moveLeft = False
                    if event.key == pygame.K_RIGHT:
                        moveRight = False
                    if event.key == pygame.K_UP:
                        moveUp = False
                    if event.key == pygame.K_DOWN:
                        moveDown = False

            # Génération des ennemis
            baddieAddCounter += 1
            if baddieAddCounter == 6:
                baddieAddCounter = 0
                baddieSize = random.randint(10, 30)
                newBaddie = {
                    'rect': pygame.Rect(WINDOWWIDTH - baddieSize, random.randint(0, WINDOWWIDTH - baddieSize), baddieSize, baddieSize),
                    'speed': -random.randint(1, 8),
                    'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize))
                }
                baddies.append(newBaddie)

            # Déplacer le joueur
            if moveLeft and playerRect.left > 0:
                playerRect.move_ip(-5, 0)
            if moveRight and playerRect.right < WINDOWWIDTH:
                playerRect.move_ip(5, 0)
            if moveUp and playerRect.top > 0:
                playerRect.move_ip(0, -5)
            if moveDown and playerRect.bottom < WINDOWHEIGHT:
                playerRect.move_ip(0, 5)

            # Déplacer les ennemis
            for b in baddies[:]:
                b['rect'].move_ip(b['speed'], 0)
                if b['rect'].left < 0:
                    baddies.remove(b)

            # Vérifier collision
            for b in baddies:
                if playerRect.colliderect(b['rect']):
                    lives -= 1
                    if lives == 0:
                        in_game = False
                        break
                    playerRect.topleft = (20, WINDOWHEIGHT / 2)
                    baddies.clear()
                    pygame.time.wait(1000)

            # Affichage du jeu
            windowSurface.fill(BACKGROUNDCOLOR)
            drawText(f'Score: {score}', font, windowSurface, 10, 0)
            drawText(f'Top Score: {topScore}', font, windowSurface, 10, 40)
            drawText(f'Lives: {lives}', font, windowSurface, 10, 80)
            windowSurface.blit(playerImage, playerRect)
            for b in baddies:
                windowSurface.blit(b['surface'], b['rect'])

            pygame.display.update()
            mainClock.tick(FPS)
        
        else:  # Mode pause
            drawText('Paused', font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
            pygame.display.update()

    # Écran de fin de jeu
    if score > topScore:
        topScore = score
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
    drawText('Press a key to play again.', font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2 + 50, center=True)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()
    in_game = True
