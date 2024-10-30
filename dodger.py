import pygame
from choix_personnage import choisir_personnage, afficher_compte_a_rebours # Import des fonctions de menu.py
import random
import sys
from pygame.locals import *

paused = False 


# Constants
WINDOWWIDTH = 800 
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0)  # black
BACKGROUNDCOLOR = (255, 255, 255)  # white
FPS_initiale = 30
SPACEMINSIZE = 200
SPACEMAXSIZE = 300
BADDIEMINSIZE = 10  # baddie are the enemies
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5
WHITE = (255, 255, 255)  #TEST
BLACK = (0, 0, 0)  #TEST

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return b  # Return the baddie that hit the player
    return None

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Initialize Pygame
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts.
font = pygame.font.SysFont(None, 48)
large_font = pygame.font.SysFont(None, 48)  

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Load images of things to avoid
baddieImage = pygame.image.load('asteroid_.png')
spaceshipImage = pygame.image.load('space.png')


# Charger les images pour les personnages               
character_image1 = pygame.image.load('character1.png')
character_image2 = pygame.image.load('character2.png')
character_image3 = pygame.image.load('character3.png')
character_images = [character_image1, character_image2, character_image3]

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
#drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))         #on peut remplacer Dodger par le nom de notre jeu
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

#Utilisation des fonctions          
character_image, player_name = choisir_personnage(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT)
playerImage = character_image   
playerImage = pygame.transform.scale(character_image, (50, 50))
playerRect = playerImage.get_rect() 
afficher_compte_a_rebours(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT)

# Game loop
topScore = 0
FPS = FPS_initiale
while True:
    baddies = []
    score = 0
    lives = 3  # Number of lives
    
    playerRect.topleft = (20, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # Game loop
        if not paused:
            score += 1
            if score == 500:
                FPS *= 2
            if score == 1000:
                FPS *= 1.5

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                if event.key == K_p:  # Pressing 'P' pauses/unpauses the game.
                    paused = not paused
                if not paused:
                    if event.key == K_LEFT or event.key == K_a:
                        moveRight = False
                        moveLeft = True
                    if event.key == K_RIGHT or event.key == K_d:
                        moveLeft = False
                        moveRight = True
                    if event.key == K_UP or event.key == K_w:
                        moveDown = False
                        moveUp = True
                    if event.key == K_DOWN or event.key == K_s:
                        moveUp = False
                        moveDown = True 

            if event.type == KEYUP:
                if not paused: 
                    if event.key == K_LEFT or event.key == K_a:
                        moveLeft = False
                    if event.key == K_RIGHT or event.key == K_d:
                        moveRight = False
                    if event.key == K_UP or event.key == K_w:
                        moveUp = False
                    if event.key == K_DOWN or event.key == K_s:
                        moveDown = False

            if event.type == MOUSEMOTION:
                playerRect.centery = event.pos[1]

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 500 <= mouse_pos[0] <= 580 and 10 <= mouse_pos[1] <= 60:  # Adjust these for your button size
                    paused = not paused

        if paused:
            windowSurface.fill(BACKGROUNDCOLOR)
            drawText('Paused', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT // 3)
            pygame.display.update()
            continue

        # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {
                'rect': pygame.Rect(WINDOWWIDTH - baddieSize, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                'speed': -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                'type': 'asteroid'  # Type of baddie
            }
            baddies.append(newBaddie)

            for x in range(1, 120):
                if score == 100 * x:
                    baddieSize = random.randint(SPACEMINSIZE, SPACEMAXSIZE)
                    newBaddie = {
                        'rect': pygame.Rect(WINDOWWIDTH + baddieSize, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(spaceshipImage, (baddieSize, baddieSize)),
                        'type': 'spaceship'  # Type of baddie
                    }
                    baddies.append(newBaddie)

        # Move the player around.
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(-5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Lives: %s' % (lives), font, windowSurface, 10, 80)  # Display lives below the score
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the baddies have hit the player.
        collided_baddie = playerHasHitBaddie(playerRect, baddies)
        if collided_baddie:
            if score > topScore:
                topScore = score  # set new top score

            # Decrease lives based on the type of baddie
            if collided_baddie['type'] == 'asteroid':
                lives -= 1  # Asteroids remove 1 life
            elif collided_baddie['type'] == 'spaceship':
                lives -= 2  # Spaceships remove 2 lives
            
            if lives <= 0:  # If no lives left, the game ends
                break
            else:
                playerRect.topleft = (50, WINDOWHEIGHT / 2)  # Reset player position
                baddies = []  # Clear all baddies on screen
                pygame.time.wait(1000)  # Pause for a second before continuing

        mainClock.tick(FPS)

    
    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    FPS = FPS_initiale #on réinitialise la valeur initiale
    waitForPlayerToPressKey()

    gameOverSound.stop()