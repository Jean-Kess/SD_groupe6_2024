import pygame
from choosing_your_character import choose_character, display_the_countdown # Importing functions from choix_personnage.py
import random
import sys
from pygame.locals import *

paused = False 


# Constants
WINDOWWIDTH = 800 
WINDOWHEIGHT = 800
TEXTCOLOR = (255, 255, 255)  # white
BACKGROUNDCOLOR = (255, 255, 255)  # white
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
FPS_initiale = 30
SPACEMINSIZE = 200
SPACEMAXSIZE = 300
BADDIEMINSIZE = 10  # baddie are the enemies
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

# Constants for the star and immortality
STAR_APPEAR_FRAMES = FPS_initiale * 10
STAR_EFFECT_FRAMES = FPS_initiale * 10
STAR_SPEED_MULTIPLIER = 3
STAR_SPEED = 5  # Speed of the star



def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return b
    return None

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, (0, 0, 0))  # Render the text in black
    textrect = textobj.get_rect() # Get the rectangle for the rendered text
    textrect.topleft = (x, y) # Set the position of the text
    surface.blit(textobj, textrect) # Blit the text onto the surface

def drawTextWhite(text, font, surface, x, y):
    textobj = font.render(text, True, (255, 255, 255)) # Render the text in white
    textrect = textobj.get_rect() # Get the rectangle for the rendered text
    textrect.topleft = (x, y) # Set the position of the text
    surface.blit(textobj, textrect) # Blit the text onto the surface

def update_star(starRect):
    """Updates the star's position, moving it horizontally."""
    starRect.move_ip(-STAR_SPEED, 0)  # Move the star to the left
    if starRect.right < 0:  # If the star goes off-screen
        starRect.left = WINDOWWIDTH  # Reset its position to the right edge

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts
font = pygame.font.Font('Anton-Regular.ttf', 38)
large_font = pygame.font.Font('Anton-Regular.ttf', 48) 
game_over_font = pygame.font.Font('Anton-Regular.ttf', 64)

# Set up sounds
gameOverSound = pygame.mixer.Sound('GameOver!.wav') # Sound when you lose
pygame.mixer.music.load('Background.wav') # Background sound
immortality_music = pygame.mixer.Sound('Immortality.wav') # Sound when you have the immortality star power
baddie_hit_sound = pygame.mixer.Sound('Boom.wav')  # Sound for hitting a baddie

# Load images of things to avoid
baddieImage = pygame.image.load('asteroid_.png')
spaceshipImage = pygame.image.load('space.png')

# Load images for superpowers
starImage = pygame.image.load('starImage.png')
starImage = pygame.transform.scale(starImage, (30, 30))

# Load images for characters               
character_image1 = pygame.image.load('character1.png')
character_image2 = pygame.image.load('character2.png')
character_image3 = pygame.image.load('character3.png')
character_images = [character_image1, character_image2, character_image3]

# Load background image
backgroundImage = pygame.image.load('backgroundsky.png').convert()
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))  # Resize the image


# Show the "Start" screen
windowSurface.fill(BACKGROUNDCOLOR)
#drawText('Dodger', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))         #on peut remplacer Dodger par le nom de notre jeu
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# Using the functions          
character_image, player_name = choose_character(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT)
playerImage = character_image   
playerImage = pygame.transform.scale(character_image, (50, 50))
playerRect = playerImage.get_rect() 
display_the_countdown(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT)

# Indicate the speed of play according to the score
def get_game_speed(score):
    if score >= 500:
        return FPS_initiale * 1.5
    elif score >= 1000:
        return FPS_initiale * 2
    elif score >= 2500:
        return FPS_initiale * 3
    else:
        return FPS_initiale
    
# Game loop
topScore = 0
FPS = FPS_initiale
while True:
    baddies = []
    score = 0
    lives = 3  # Number of lives at start
    
    playerRect.topleft = (20, WINDOWHEIGHT / 2)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)


    # Star variables
    star_counter = 0
    starRect = None
    star_active = False
    star_effect_counter = 0



    # Game loop
    while True:  
        if not paused:
            score += 1
            #if score == 500:
              #  FPS *= 1.5
           # if score == 1000:
               # FPS *= 1.5
    
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:  # Pressing ESC quits.
                    terminate()
                if event.key == K_p:  # Pressing 'P' pauses/unpauses the game
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
            pygame.mixer.music.stop() #quand on met pause la musique se coupe
            immortality_music.stop()
            pygame.mixer.music.play()
            pygame.display.update()
            continue

        # Add new baddies at the top of the screen, if needed
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
        # Star appearance logic
        star_counter += 1
        if star_counter >= STAR_APPEAR_FRAMES:
            starRect = pygame.Rect(random.randint(0, WINDOWWIDTH - 30),
                                   random.randint(0, WINDOWHEIGHT - 30), 30, 30)
            star_counter = 0

        # Apply star speed boost
        if star_active:
            pygame.mixer.music.stop()
            immortality_music.play()  # Play immortality music 
            pygame.mixer.music.play()
            FPS = get_game_speed(score) * STAR_SPEED_MULTIPLIER
            #c'est ici qu'il faudra écrie le code pour changer la vitesse quand on a l'étoile je crois
        else:
         # Réinitialisez la vitesse en fonction du score, mais sans l'effet de l'étoile
            FPS = get_game_speed(score)

        # Move the player around
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)

        # Move the baddies
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(b['speed'], 0)
            elif reverseCheat:
                b['rect'].move_ip(-5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

        # Delete baddies that have fallen past the bottom
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Update star position
        if starRect:
            update_star(starRect)    

        # Check for star collision
        if starRect and playerRect.colliderect(starRect):
            star_active = True
            star_effect_counter = STAR_EFFECT_FRAMES
            starRect = None

        # Reduce star effect counter
        if star_active:
            star_effect_counter -= 1
            if star_effect_counter <= 0:
                star_active = False
                
        # Draw the game world on the window
        windowSurface.blit(backgroundImage, (0, 0))   #ici pour modifier l'arrière plan du jeu
        drawTextWhite('Score: %s' % (score), font, windowSurface, 10, 0)
        drawTextWhite('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        drawTextWhite('Lives: %s' % (lives), font, windowSurface, 10, 80)  # Display lives below the score
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        if starRect:
            windowSurface.blit(starImage, starRect)

        pygame.display.update()

        # Display immortality timer
        if star_active:
            immortality_seconds = star_effect_counter // FPS_initiale
            drawTextWhite(f"Immortality: {immortality_seconds}", font, windowSurface, 10, 120)

        pygame.display.update()

        # Check if any of the baddies have hit the player
        if not star_active:
            collided_baddie = playerHasHitBaddie(playerRect, baddies)
            immortality_music.stop()  # Stop the immortality music when the effect ends
            
            if collided_baddie:
                pygame.mixer.music.stop()
                baddie_hit_sound.play()
                
                # Decrease lives based on the type of baddie
                if collided_baddie['type'] == 'asteroid':
                    lives -= 1  # Hitting an asteroid removes 1 life
                elif collided_baddie['type'] == 'spaceship':
                    lives -= 2  # Hitting a spaceship removes 2 livess
            
                if lives <= 0:  # If no lives left, the game ends
                    if score > topScore:
                        topScore = score  # Update top score

                        # Display the congratulatory message if we beat our score
                        congratulation_text = f"Congratulations {player_name}, you've beaten your record!"
                        congratulation_x = (WINDOWWIDTH - font.size(congratulation_text)[0]) // 2
                        drawTextWhite(congratulation_text, font, windowSurface, congratulation_x, 130)
                        pygame.display.update()  # Updates the display to show the message
                        pygame.time.wait(2000)  # Wait 2 seconds before continuing
                    break
                else:
                    playerRect.topleft = (50, WINDOWHEIGHT / 2)  # Reset player position
                    baddies = []  # Clear all baddies on screen
                    pygame.time.wait(1000)  # Pause for a second before continuing
                
                pygame.mixer.music.play()

        mainClock.tick(FPS)

    
    # Stop the game and show the "Game Over" screen
    pygame.mixer.music.stop()
    gameOverSound.play()

    game_over_text = 'GAME OVER'
    retry_text = 'Press a key to play again.'

    # Calculating positions to centre text
    game_over_x = (WINDOWWIDTH - game_over_font.size(game_over_text)[0]) // 2
    retry_x = (WINDOWWIDTH - font.size(retry_text)[0]) // 2

    #  Display the text ‘GAME OVER’ centred
    drawTextWhite(game_over_text, game_over_font, windowSurface, game_over_x, (WINDOWHEIGHT / 3))

    # Display the text ‘GAME OVER’ centred
    drawTextWhite(retry_text, font, windowSurface, retry_x, (WINDOWHEIGHT / 3) + 100)
    
    

    pygame.display.update()
    FPS = FPS_initiale # reset the initial value

    waitForPlayerToPressKey()

    gameOverSound.stop()