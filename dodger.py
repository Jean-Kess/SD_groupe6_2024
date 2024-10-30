import pygame, random, sys #random crée des valeurs random, sys permet de terminer le système.
from pygame.locals import *

paused = False 
#bonne version

#when it's in upper letter it mean it's frome de pygame
WINDOWWIDTH = 800 
WINDOWHEIGHT = 800
TEXTCOLOR = (0, 0, 0) #red, green, blue
BACKGROUNDCOLOR = (255, 255, 255)
FPS_initiale = 30
BADDIEMINSIZE = 10 #baddie are the enemies
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(): #we name the function for what it done
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # Pressing ESC quits.
                    terminate()
                return

#playerRect is your side, baddies is the dictionnaries of obstacle
def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

#create the text for your games
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#part were we setting our game
# Set up pygame, the window, and the mouse cursor.
pygame.init()
mainClock = pygame.time.Clock() #clock inside your game
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #you set the side of the window
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False) #if you want or not to show the mouse

# Set up the fonts.
font = pygame.font.SysFont(None, 48)

# Set up sounds.
gameOverSound = pygame.mixer.Sound('gameover.wav') #music when you loose
pygame.mixer.music.load('background.mid') #music in the game

# Set up images.
playerImage = pygame.image.load('player.png') #image of the player
playerRect = playerImage.get_rect() #everyone are rectangle
baddieImage = pygame.image.load('asteroid.png') #image of the ennemies

# Show the "Start" screen.
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

#how the score is calculated
topScore = 0
FPS = FPS_initiale
while True:
    # Set up the start of the game.
    baddies = []
    score = 0
    lives = 3  # Nombre de vies
    
    playerRect.topleft = (20, WINDOWHEIGHT/2) #where the player start
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0 #counter of the obstacle
    pygame.mixer.music.play(-1, 0.0)

    while True: # The game loop runs while the game part is playing.
        if not paused:
            score += 1 # Increase score.
            if score == 500: #quand le joueur atteint 500 le jeu s'accelère 
                FPS = FPS*2
            if score == 1000:#quand le joueur atteint 1000 points le jeu accelère à nouveau
                FPS = FPS*1.5

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # if event.type == KEYDOWN:
            #    if event.key == K_z: #how you write the key the player press
             #       reverseCheat = True
              #  if event.key == K_x:
               #     slowCheat = True
                #if event.key == K_LEFT or event.key == K_a:
                 #   moveRight = False
                  #  moveLeft = True
                #if event.key == K_RIGHT or event.key == K_d:
                 #   moveLeft = False
                  #  moveRight = True
                #if event.key == K_UP or event.key == K_w:
                 #   moveDown = False
                  #  moveUp = True
                #if event.key == K_DOWN or event.key == K_s:
                #    moveUp = False
                 #   moveDown = True

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                if event.key == K_p:  # Pressing 'P' pauses/unpauses the game.
                    paused = not paused
                # Handle player movement keys when not paused
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

            #if event.type == KEYUP:
             #   if event.key == K_z:
              #      reverseCheat = False
               #     score = 0
                #if event.key == K_x:
                 #   slowCheat = False
                  #  score = 0
                #if event.key == K_ESCAPE:
                #        terminate()

                #if event.key == K_LEFT or event.key == K_a:
                 #   moveLeft = False
                #if event.key == K_RIGHT or event.key == K_d:
                 #   moveRight = False
                #if event.key == K_UP or event.key == K_w:
                 #   moveUp = False
                #if event.key == K_DOWN or event.key == K_s:
                  #  moveDown = False

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
                # If the mouse moves, move the player where to the cursor.
                #playerRect.centerx = event.pos[0]  #onveut bloquer les déplacements horizontaux
                playerRect.centery = event.pos[1]
            
            if event.type == MOUSEBUTTONDOWN:
                playerRect.centery = event.pos[0]
                mouse_pos = event.pos
                if 500 <= mouse_pos[0] <= 580 and 10 <= mouse_pos[1] <= 60:  # Adjust these for your button size
                    paused = not paused

            
        if paused:  # Si le jeu est en pause
            windowSurface.fill(BACKGROUNDCOLOR)  # Remplit l'écran avec la couleur de fond
            drawText('Paused', font, windowSurface, WINDOWWIDTH // 3, WINDOWHEIGHT // 3)  # Affiche le texte "Paused"
            pygame.display.update()  # Mets à jour l'écran
            continue  # Passe directement au prochain tour de boucle sans exécuter la logique du jeu
        if not paused:
        # Code to move the player and baddies, add baddies, etc.
            pass
        
        # Dessiner le bouton pause
        pygame.draw.rect(windowSurface, (200, 200, 200), (500, 10, 80, 50))  # Bouton Pause/Resume
        drawText('Pause' if not paused else 'Resume', font, windowSurface,510,20)


        # Add new baddies at the top of the screen, if needed. how ennemies are created
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            newBaddie = {'rect': pygame.Rect(WINDOWWIDTH - baddieSize, random.randint(0,WINDOWWIDTH - baddieSize),baddieSize, baddieSize),
                        'speed': -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                        }

            baddies.append(newBaddie)

        # Move the player around.
        #have we the place to move more or are we in the wall
       # if moveLeft and playerRect.left > 0:
          #  playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        #if moveRight and playerRect.right < WINDOWWIDTH:
           # playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies down.
        for b in baddies:
            if not reverseCheat and not slowCheat:
                 b['rect'].move_ip(b['speed'],0) #pour que les méchants viennent de la droite
            elif reverseCheat:
                b['rect'].move_ip(-5) #the baddies moove back
            elif slowCheat:
                b['rect'].move_ip(0, 1) #the baddies go slowly

        # Delete baddies that have fallen past the bottom.
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawText('Lives: %s' % (lives), font, windowSurface, 10, 80)  # Affiche les vies en dessous du score

        # Draw the player's rectangle.
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie.
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update() #when you add something new you need to refresh it

    
        # Check if any of the baddies have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score  # set new top score

            lives -= 1  # Réduit le nombre de vies de 1
            if lives == 0:  # Si plus de vies, le jeu se termine
                break
            else:
                # Réinitialiser la position du joueur
                playerRect.topleft = (50, WINDOWHEIGHT / 2)  # Retourne le joueur à sa position initiale
                baddies = []  # Efface tous les baddies à l'écran
                pygame.time.wait(1000)  # Pause d'une seconde avant de continuer



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

