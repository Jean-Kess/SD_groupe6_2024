#dodger avec armes
#firstly, in order to be able to see the explosion video, you need to write this in your terminal :  pip install opencv-python

import pygame
from choosing_your_character import choose_character, display_the_countdown # Importing functions from choix_personnage.py
import random
import sys
from pygame.locals import *
import cv2

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
ADDNEWBADDIERATE = 15
PLAYERMOVERATE = 5

# Constants for the star and immortality
STAR_APPEAR_FRAMES = FPS_initiale * 10
STAR_EFFECT_FRAMES = FPS_initiale * 10
STAR_SPEED_MULTIPLIER = 3
STAR_SPEED = 5  # Speed of the star

# List for storing projectiles
bullets = []

# Projectile constants
BULLET_SPEED = 10
BULLET_SIZE = (10, 5)
BULLET_COLOR = {
    0: (163, 195, 235),   # Blue for the first character (index 0)
    1: (139, 207, 186),   # Green for the second character (index 1)
    2: (243, 175, 197),   # Pink/Magenta for the third (index 2)
    3: (255, 214, 52)     # Yellow for the fourth (index 3)
}


#Definition of functions
def terminate():
    pygame.quit()
    sys.exit()

# define the function that displays the game rules
def display_rules():
    image = pygame.image.load("Rules.png") # Load the image
    image = pygame.transform.scale(image, (WINDOWWIDTH, WINDOWHEIGHT))  # Adjust the size

    screen_copy = windowSurface.copy() # Create a temporary surface to display the image
    screen_copy.blit(image, (0, 0))    # Display the image on the temporary surface
    windowSurface.blit(screen_copy, (0, 0))  # Display the temporary surface on the main screen
    pygame.display.flip()  # Update display

    #  Wait for the user to press a key to exit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return 1 
            
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    display_rules()
                if event.key == K_ESCAPE:
                    terminate()
                return
    

def playerHasHitBaddie(playerRect, playerImage, baddies):  # Add playerImage argument
    playerMask = pygame.mask.from_surface(playerImage)  # Create player mask
    for b in baddies:
        baddieMask = pygame.mask.from_surface(b['surface'])  # Create baddie mask
        offset = (b['rect'].x - playerRect.x, b['rect'].y - playerRect.y)
        if playerMask.overlap(baddieMask, offset):  # Check for mask overlap
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
    starRect.move_ip(-STAR_SPEED, 0)  # Move the star to the left
    if starRect.right < 0:  # If the star goes off-screen
        starRect.left = WINDOWWIDTH  # Reset its position to the right edge
        
# Projectile firing function
def shoot_bullet(playerRect, color): # Add color parameter
    bullet = {
        'rect': pygame.Rect(playerRect.right, playerRect.centery - BULLET_SIZE[1] // 2, BULLET_SIZE[0], BULLET_SIZE[1]),
        'speed': BULLET_SPEED,
        'color': color # Add color to the bullet dictionary

    }
    bullets.append(bullet)

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')
pygame.mouse.set_visible(False)

# Set up the fonts
small_font = pygame.font.Font('gameFont.ttf', 28)
font = pygame.font.Font('Anton-Regular.ttf', 38)
large_font = pygame.font.Font('Anton-Regular.ttf', 48) 
game_over_font = pygame.font.Font('gameFont.ttf', 64)
retry_font = pygame.font.Font('gameFont.ttf', 35)

# Set up sounds
gameOverSound = pygame.mixer.Sound('GameOver!.wav') # Sound when you lose
pygame.mixer.music.load('Background.wav') # Background sound
immortality_music = pygame.mixer.Sound('Immortality.wav') # Sound when you have the immortality star power
baddie_hit_sound = pygame.mixer.Sound('Boom.wav')  # Sound for hitting a baddie

# Load images of things to avoid
baddieImage1 = pygame.image.load('planet09.png')
baddieImage2 = pygame.image.load('planet05.png')
baddieImage3 = pygame.image.load('planet08.png')
spaceshipImage = pygame.image.load('space.png')

# Load images for superpowers
starImage = pygame.image.load('starImage.png')
starImage = pygame.transform.scale(starImage, (30, 30))

# Define character images for different colors
character_Blue = [
    pygame.image.load("alienBlue.png"),
    pygame.image.load("character_B_damage0.png"),  # 3 lives
    pygame.image.load("character_B_damage1.png"),  # 2 lives
    pygame.image.load("character_B_damage2.png")   # 1 life
]

character_Green = [
    pygame.image.load("alienGreen.png"),
    pygame.image.load("character_G_damage0.png"),  # 3 lives
    pygame.image.load("character_G_damage1.png"),  # 2 lives
    pygame.image.load("character_G_damage2.png")   # 1 life
]

character_Pink = [
    pygame.image.load("alienPink.png"),
    pygame.image.load("character_P_damage0.png"),  # 3 lives
    pygame.image.load("character_P_damage1.png"),  # 2 lives
    pygame.image.load("character_P_damage2.png")   # 1 life
]

character_Yellow = [
    pygame.image.load("alienYellow.png"),
    pygame.image.load("character_Y_damage0.png"),  # 3 lives
    pygame.image.load("character_Y_damage1.png"),  # 2 lives
    pygame.image.load("character_Y_damage2.png")   # 1 life
]

# Group all characters into one variable
character_images = [character_Blue, character_Green, character_Pink, character_Yellow]

#Load image of heart
heartImage = pygame.image.load('heartImage.png')  # Load the heart image
heartImage = pygame.transform.scale(heartImage, (22, 22))  # Adjust size if needed

# Load background image
backgroundImage = pygame.image.load('backgroundsky.png').convert()
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))  # Resize the image
pausedImage = pygame.image.load('pausedImage.png').convert()
pausedImage = pygame.transform.scale(pausedImage, (WINDOWWIDTH, WINDOWHEIGHT))  # Resize the image

# Explosion video
explosion_video = cv2.VideoCapture('explosion2.mp4')
playing_explosion = False  # Flag to indicate if the explosion is playing
explosion_x = 0  # X coordinate for the explosion
explosion_y = 0  # Y coordinate for the explosion

def play_explosion(video, x, y):
    global playing_explosion, explosion_x, explosion_y
    success, frame = video.read()
    if success:
        frame = cv2.resize(frame, (75, 75), interpolation=cv2.INTER_AREA) # Resize the frame to 75x75pixels
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert the frame from BGR to RGB
        frame_surface = pygame.surfarray.make_surface(frame) # Convert the resized frame to a Pygame surface

        # Center the explosion on the baddie
        frame_rect = frame_surface.get_rect()
        frame_rect.center = (x, y)

        windowSurface.blit(frame_surface, frame_rect)
    else:
        playing_explosion = False
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)

#draws hearts on the screen based on remaining lives
def draw_hearts(lives, font, surface, x, y):
    text = "Lives: "
    textobj = font.render(text, True, (255, 255, 255))
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

    heart_spacing = 30  # Adjust spacing between hearts
    heart_y_offset = 18  # Adjust this value to fine-tune vertical alignment
    for i in range(lives):
        windowSurface.blit(heartImage, (x + textrect.width + (i * heart_spacing), y + heart_y_offset)) # Position hearts relative to text

# Show the "Start" screen
windowSurface.fill(BACKGROUNDCOLOR)
drawText('Press a key to start', pygame.font.Font('gameFont.ttf', 40), windowSurface,
         (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 40).size('Press a key to start.')[0]) // 2,
         (WINDOWHEIGHT / 3) + 50)
drawText('Press R to see rules', pygame.font.Font('gameFont.ttf', 25), windowSurface,
         (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 25).size('Press r to see rules')[0]) // 2,
         (WINDOWHEIGHT / 3) + 150)
pygame.display.update()
waitForPlayerToPressKey()

# Using the functions 
# Choose character
character_image, player_name, selected_character = choose_character(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT)
character_index = character_images.index(character_image) # The index of the chosen colour, this is the result of `selected_character`.
selected_character_images = character_images[character_index]  # This is a list of images of the character
playerImage = selected_character_images[0]  # The initial image of the character with 3 lives (damage0)
playerRect = playerImage.get_rect()

display_the_countdown(windowSurface, large_font, playerImage, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT) # Display the countdown to the start of the game
pygame.mouse.set_visible(False)  # Hide the mouse cursor once the game has started
  

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
    bullets = []
    score = 0
    lives = 3  # Number of lives at start
    playerImage = selected_character_images[1]
    playerImage = pygame.transform.scale(playerImage,(70,70))
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
    
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_r: # Pressing 'r' shows the rules of the game
                    display_rules()
                if event.key == K_f: # Pressing 'f' to fire the baddies
                    bullet_color = BULLET_COLOR.get(selected_character, (255, 0, 0)) # default to red if no match
                    shoot_bullet(playerRect, bullet_color)  # Pass bullet color here


                if event.key == K_ESCAPE:  # Pressing ESC quits
                    terminate()
                if event.key == K_p:  # Pressing 'p' pauses/unpauses the game
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
            windowSurface.blit(pausedImage, (0, 0))
            paused_text = 'Paused, press P to continue playing' 
            paused_x = (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 25).size(paused_text)[0]) // 2
            drawText(paused_text, pygame.font.Font('gameFont.ttf', 25), windowSurface, paused_x, WINDOWHEIGHT//3) #when paused, the music stops

            immortality_music.stop()
            pygame.mixer.music.play()
            pygame.display.update()
            continue
        
        # Projectiles update
        for bullet in bullets[:]:
            bullet['rect'].x += bullet['speed']  # Moves the projectile
            if bullet['rect'].left > WINDOWWIDTH:  # Removes off-screen projectiles
                bullets.remove(bullet)

        # Checking for collisions between projectiles and baddies
        for bullet in bullets[:]:
            for baddie in baddies[:]:
                if bullet['rect'].colliderect(baddie['rect']):
                    baddie['health'] -= 1  # Reduces baddie life
                    bullets.remove(bullet)  # Removes the projectile
                    break
                if baddie['health'] <= 0:  # Deletes the baddie if it has no life left
                    baddies.remove(baddie)
                    break


        # Add new baddies at the top of the screen, if needed
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
            prob = random.randint(1, 100)  # Generates a number between 1 and 100
            if prob <= 50:  # 50% probability
                baddieType = 'asteroid'
                baddieImage = baddieImage1
                baddieHealth = 1
            elif prob <= 80:  # 30% probability (50% + 30% = 80%)
                baddieType = 'strong_asteroid'
                baddieImage = baddieImage2
                baddieHealth = 2
            else:  # 20% probability
                baddieType = 'super_strong_asteroid'
                baddieImage = baddieImage3 
                baddieHealth = 3  #  Higher hit points for the super-strong type

        # Create a new baddie
            newBaddie = {
                'rect': pygame.Rect(
                    WINDOWWIDTH - baddieSize,
                    random.randint(0, WINDOWHEIGHT - baddieSize),
                    baddieSize,
                    baddieSize
                ),
                'speed': -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                'type': baddieType,
                'health': baddieHealth
            }
            baddies.append(newBaddie)
            

            for x in range(1, 220):
                if score == 100 * x:
                    baddieSize = random.randint(SPACEMINSIZE, SPACEMAXSIZE)
                    newBaddie = {
                        'rect': pygame.Rect(WINDOWWIDTH + baddieSize, random.randint(0, WINDOWHEIGHT - baddieSize), baddieSize, baddieSize),
                        'speed': -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface': pygame.transform.scale(spaceshipImage, (baddieSize, baddieSize)),
                        'type': 'spaceship',  # Type of baddie
                        'health' : 5  # Gives 5 lives to each spaceship
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
            
        else:
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
        windowSurface.blit(backgroundImage, (0, 0))  
        drawTextWhite('Score: %s' % (score), font, windowSurface, 10, 0)
        drawTextWhite('Top Score: %s' % (topScore), font, windowSurface, 10, 40)
        draw_hearts(lives, font, windowSurface, 10, 80)  #  Pass necessary arguments
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])
        if starRect:
            windowSurface.blit(starImage, starRect)
            
        # Dessin des projectiles
        for bullet in bullets:
            pygame.draw.rect(windowSurface, bullet['color'], bullet['rect'])

        # Display immortality timer
        if star_active:
            immortality_seconds = star_effect_counter // FPS_initiale
            drawTextWhite(f"Immortality: {immortality_seconds}", font, windowSurface, 10, 120)

        pygame.display.update()

        # Play explosion video if it's active
        if playing_explosion:
            play_explosion(explosion_video, explosion_x + 20, explosion_y + 20)  # Offset explosion position

        pygame.display.update()

        # Check if any of the baddies have hit the player
        if not star_active:
            collided_baddie = playerHasHitBaddie(playerRect, playerImage, baddies)  
            immortality_music.stop()  # Stop the immortality music when the effect ends
            
            if collided_baddie:
                pygame.mixer.music.stop() # Stop the game music
                baddie_hit_sound.play()   # Play the explosion sound

                # Decrease lives
                if collided_baddie['type'] == 'asteroid':
                    lives -= 1
                elif collided_baddie['type'] == 'strong_asteroid':
                    lives -= 1
                elif collided_baddie['type'] == 'super_strong_asteroid':
                    lives -= 1
                elif collided_baddie['type'] == 'spaceship':
                    lives -= 2

                # Start playing the explosion (either small or fullscreen)
                playing_explosion = True
                if lives <= 0:  # Fullscreen explosion on game over
                    explosion_x = WINDOWWIDTH // 2
                    explosion_y = WINDOWHEIGHT // 2
                    explosion_size = (WINDOWWIDTH, WINDOWHEIGHT)  # Fullscreen size
                else:  # Small explosion otherwise
                    explosion_x = collided_baddie['rect'].centerx + 20
                    explosion_y = collided_baddie['rect'].centery + 20
                    explosion_size = (75, 75)  # Small explosion size

                while playing_explosion:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()

                    success, frame = explosion_video.read()
                    if success:
                        frame = cv2.resize(frame, explosion_size, interpolation=cv2.INTER_AREA)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_surface = pygame.surfarray.make_surface(frame)
                        windowSurface.blit(frame_surface, (explosion_x - explosion_size[0] // 2, explosion_y - explosion_size[1] // 2))  # Center the explosion
                    else:
                        playing_explosion = False
                        explosion_video.set(cv2.CAP_PROP_POS_FRAMES, 0)

                    pygame.display.update()
                    mainClock.tick(FPS)
            
                if lives <= 0:  # If no lives left, the game ends                 
                    break
                else:
                    playerImage = selected_character_images[4-lives]
                    playerImage = pygame.transform.scale(playerImage,(70,70))
                    playerRect.topleft = (50, WINDOWHEIGHT / 2)  # Reset player position
                    baddies = []  # Clear all baddies on screen
                    
                    pygame.time.wait(1000)  # Pause for a second before continuing
                
                pygame.mixer.music.play()

        mainClock.tick(FPS)

    
    # Stop the game and show the "Game Over" screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    
    game_over_text = 'GAME OVER'
    retry_text = 'Press a key to play again'

    # Calculating positions to centre text
    game_over_x = (WINDOWWIDTH - game_over_font.size(game_over_text)[0]) // 2
    retry_x = (WINDOWWIDTH - retry_font.size(retry_text)[0]) // 2  

    #  Display the text ‘GAME OVER’ centred
    drawTextWhite(game_over_text, game_over_font, windowSurface, game_over_x, (WINDOWHEIGHT / 3))
    drawTextWhite(retry_text, retry_font, windowSurface, retry_x, (WINDOWHEIGHT / 3) + 100)
    pygame.display.update()  # Updates the display to show the message
    pygame.time.wait(2000)  # Wait 2 seconds before continuing
    
    # Display the congratulatory message if we beat our score
    if score > topScore:
        topScore = score  # Update top score
        congrats_y = (WINDOWHEIGHT / 3) + 250
        for text in [f"Congratulations {player_name},", "You've beaten your record!", f"Now your top score is {topScore}"]:
            drawText(text, small_font, windowSurface, (WINDOWWIDTH - small_font.size(text)[0]) / 2, congrats_y)
            congrats_y += 50  # Increment y-position for next line
    
    pygame.display.update()
    FPS = FPS_initiale # reset the initial value

    waitForPlayerToPressKey()

    gameOverSound.stop()