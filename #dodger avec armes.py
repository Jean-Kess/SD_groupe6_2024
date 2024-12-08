# dodger_with_arms.py

# Imports
import pygame                                                 # Import the Pygame library
import random                                                 # Import the random module
import sys                                                    # Import the sys module
from pygame.locals import *                                   # Import the Pygame constants

# Constants class
class Constants:
    # Window settings
    WINDOWWIDTH = 800                                         # Set the window width
    WINDOWHEIGHT = 800                                        # Set the window height

    # Colors
    WHITE = (255, 255, 255)                                   # Set the white color
    BLACK = (0, 0, 0)                                         # Set the black color

    # Game settings
    MAX_NAME_LENGTH = 15                                      # Set the maximum name length
    FPS_INITIAL = 30                                          # Set the initial frames per second
    SPACE_MIN_SIZE = 150                                      # Set the minimum size for the spaceship
    SPACE_MAX_SIZE = 250                                      # Set the maximum size for the spaceship
    BADDIE_MIN_SIZE = 15                                      # Set the minimum size for the baddies
    BADDIE_MAX_SIZE = 60                                      # Set the maximum size for the baddies
    BADDIE_MIN_SPEED = 3                                      # Set the minimum speed for the baddies
    BADDIE_MAX_SPEED = 8                                      # Set the maximum speed for the baddies
    ADD_NEW_BADDIE_RATE = 15                                  # Set the rate to add new baddies
    PLAYER_MOVE_RATE = 5

    # Bullet settings
    BULLET_SIZE = (10, 5)                                     # Set the bullet size
    BULLET_SPEED = 10                                         # Set the bullet speed
    BULLET_COLOR = {
        0: (163, 195, 235),                                   # Blue for the first character (index 0)
        1: (139, 207, 186),                                   # Green for the second character (index 1)
        2: (243, 175, 197),                                   # Pink/Magenta for the third character (index 2)
        3: (255, 214, 52)                                     # Yellow for the fourth character (index 3)

    }

    # Character settings
    CHARACTER_SIZE = (70, 90)                                 # Set the character size

# Fonts class
class Fonts:
    small_font = None                                         # Font for small text     
    font = None                                               # Font for regular text
    large_font = None                                         # Font for large text
    big_font = None                                           # Font for big text
    game_over_font = None                                     # Font for game over text
    retry_font = None                                         # Font for retry text


    @classmethod
    def load_assets(cls):
        cls.small_font = pygame.font.Font('gameFont.ttf', 28)           # Load the small font
        cls.font = pygame.font.Font('Anton-Regular.ttf', 38)            # Load the regular font
        cls.large_font = pygame.font.Font('gameFont.ttf', 48)           # Load the large font
        cls.big_font = pygame.font.Font('gameFont.ttf', 74)             # Load the big font
        cls.game_over_font = pygame.font.Font('gameFont.ttf', 64)       # Load the game over font
        cls.retry_font = pygame.font.Font('gameFont.ttf', 35)           # Load the retry font

# Sounds class
class Sounds:
    gameOverSound = None    
    immortality_music = None
    baddie_hit_sound = None
    baddie_shoot_sound = None

    @classmethod
    def load_assets(cls):
        cls.gameOverSound = pygame.mixer.Sound('GameOver!.wav')         # Load the game over sound
        pygame.mixer.music.load('Background.wav')                       # Load the background music
        cls.immortality_music = pygame.mixer.Sound('Immortality.wav')   # Load the immortality music
        cls.baddie_hit_sound = pygame.mixer.Sound('Boom.wav')           # Load the baddie hit sound
        cls.baddie_shoot_sound = pygame.mixer.Sound('Boom.wav')         # Load the baddie shoot sound       

# Images class
class Images:
    baddie_images = {}
    spaceshipImage = None
    starImage = None
    heartImage = None
    backgroundImage = None
    pausedImage = None
    startImage = None
    rulesImage = None
    smokeImage = None
    explosion_frames = []
    character_images = []

    @classmethod
    def load_and_scale(cls, path, size=None):              # Function to load and scale images
        image = pygame.image.load(path).convert_alpha()    # Load the image
        if size:                                           # If the size is provided
            image = pygame.transform.scale(image, size)    # Scale the image
        return image                                       # Return the image


    @classmethod
    def load_assets(cls):
        cls.baddie_images = {
            'planet': cls.load_and_scale('planet09.png'),                                                                      # Load and scale the planet image
            'strong_planet': cls.load_and_scale('planet07.png'),                                                               # Load and scale the strong planet image
            'super_strong_planet': cls.load_and_scale('planet01.png')                                                          # Load and scale the super strong planet image
        }
        cls.spaceshipImage = cls.load_and_scale('spaceship2.png')                                                              # Load and scale the spaceship image
        cls.starImage = cls.load_and_scale('starImage.png', (30, 30))                                                          # Load and scale the star image
        cls.heartImage = cls.load_and_scale('heartImage.png', (22, 22))                                                        # Load and scale the heart image
        cls.backgroundImage = cls.load_and_scale('backgroundImage.png', (Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))       # Load and scale the background image
        cls.pausedImage = cls.load_and_scale('paused.png', (Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))                    # Load and scale the paused image
        cls.startImage = cls.load_and_scale('startImage.png', (Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))                 # Load and scale the start image
        cls.rulesImage = cls.load_and_scale('rules.png', (Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))                      # Load and scale the rules image
        cls.explosion_frames = [cls.load_and_scale(f'explosion0{i}.png') for i in range(9)]                                    # Load and scale the explosion frames
        cls.smokeImage = cls.load_and_scale('smoke.png')                                                                       # Load and scale the smoke image
        colors = ['Blue', 'Green', 'Pink', 'Yellow']    
        cls.character_images = []
        for color in colors:        
            images = [
                cls.load_and_scale(f"alien{color}.png", Constants.CHARACTER_SIZE),                                             # Load and scale the character image
                cls.load_and_scale(f"character_{color[0]}_damage0.png", Constants.CHARACTER_SIZE),                             # Load and scale the damaged 0 character image
                cls.load_and_scale(f"character_{color[0]}_damage1.png", Constants.CHARACTER_SIZE),                             # Load and scale the damaged 1 character image
                cls.load_and_scale(f"character_{color[0]}_damage2.png", Constants.CHARACTER_SIZE)                              # Load and scale the damaged 2 character image
            ]
            cls.character_images.append(images)                                                                                # Append the character images to the list

# Initialize Pygame
pygame.init()                                                           # Initialize Pygame
pygame.mixer.init()                                                     # Initialize the mixer module
mainClock = pygame.time.Clock()                                         # Create a clock object to control the frame rate
windowSurface = pygame.display.set_mode((Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT))        # Set the window size
pygame.display.set_caption('OurGame')                                   # Set the window caption



# Create the smoke trail behind our character (inspired by this video "How to program a Cool Smoke effect using #Pygame - Code king : https://youtu.be/onecEtoqdtg?si=s92NcBqXpAGXLXVL) "
def scale(img: pygame.Surface, factor):                                                  # Function to scale an image
    w, h = img.get_width() * factor, img.get_height() * factor                           # Calculate the new width and height
    return pygame.transform.scale(img, (int(w), int(h)))                                 # Return the scaled image

class SmokeParticle:
    def __init__(self, x=Constants.WINDOWWIDTH // 2, y=Constants.WINDOWHEIGHT // 2):     # Initialize the smoke particle
        self.x = x                                                                       # Set the x-coordinate
        self.y = y                                                                       # Set the y-coordinate
        self.scale_k = 0.07                                                              # Set the scale factor
        self.img = scale(Images.smokeImage, self.scale_k)                                # Scale the smoke image
        self.alpha = 255                                                                 # Set the alpha value
        self.alpha_rate = 3                                                              # Set the alpha rate
        self.alive = True                                                                # Set the alive status
        self.vy = 0                                                                      # Set the vertical velocity
        self.vx = -4 + random.randint(-10, -7) / 10                                      # Set the horizontal velocity
        self.k = 0.01 * random.random() * random.choice([-1, 1])                         # Set the random horizontal acceleration

    def update(self):
        self.x += self.vx                                                                # Update the x-coordinate
        self.scale_k += 0.0035                                                           # Increase the scale factor
        self.alpha -= self.alpha_rate                                                    # Decrease the alpha value
        if self.alpha < 0:
            self.alpha = 0                                                               # Ensure alpha does not go below 0
            self.alive = False                                                           # Mark the particle as not alive
        self.alpha_rate -= 0.1                                                           # Decrease the alpha rate
        if self.alpha_rate < 1.5:
            self.alpha_rate = 1.5                                                        # Ensure alpha rate does not go below 1.5
        self.img = scale(Images.smokeImage, self.scale_k)                                # Scale the smoke image
        self.img.set_alpha(self.alpha)                                                   # Set the alpha value of the image

    def draw(self):
        windowSurface.blit(self.img, self.img.get_rect(center=(self.x, self.y)))         # Draw the smoke particle on the window surface

class Smoke:
    def __init__(self, x=Constants.WINDOWWIDTH // 2, y=Constants.WINDOWHEIGHT // 2 + 150): 
        self.x = x                                                                       # Set the x-coordinate
        self.y = y                                                                       # Set the y-coordinate
        self.particles = []                                                              # Initialize the list of smoke particles
        self.frames = 0                                                                  # Initialize the frame counter

    def update(self):
        self.particles = [i for i in self.particles if i.alive]                          # Remove dead particles
        self.frames += 1                                                                 # Increment the frame counter
        if self.frames % 2 == 0:
            self.frames = 0                                                              # Reset the frame counter
            self.particles.append(SmokeParticle(self.x, self.y))                         # Add a new smoke particle
        for i in self.particles:
            i.update()                                                                   # Update each smoke particle

    def draw(self):
        for i in self.particles:
            i.draw()                                                                     # Draw each smoke particle


# Load assets
Fonts.load_assets()                                                     # Load the fonts
Sounds.load_assets()                                                    # Load the sounds
Images.load_assets()                                                    # Load the images


class GameUtils:
    @staticmethod
    def terminate():
        pygame.quit()                                                   # Quit Pygame
        sys.exit()                                                      # Exit the program

    @staticmethod
    def waitForPlayerToPressKey(game):
        while True:
            for event in pygame.event.get():    
                if event.type == QUIT:                                  # If the event type is QUIT
                    game.terminate_game()                               # Terminate the game
                if event.type == KEYDOWN:                               # If the event type is KEYDOWN (if a key is pressed)
                    if event.key == K_r:                                # If the key pressed is R
                        game.display_rules()                            # Display the rules
                        if game.is_playing:                             # Restart the background music only if the game is running (so it doesn't play during the "write name, chosing charcaters" screen)
                            pygame.mixer.music.play()                   # Play the background music
                    if event.key == K_ESCAPE:                           # If the key pressed is ESCAPE
                        game.terminate_game()                           # Terminate the game
                    return

    @staticmethod       
    def drawText(text, font, surface, x, y, center=False, color=Constants.BLACK):           # Function to draw text on the screen   
        textobj = font.render(text, True, color)                                            # Render the text
        textrect = textobj.get_rect()                                                       # Get the rectangle for the text
        if center:                                                                          # If the text is centered
            textrect.center = (x, y)                                                        # Center the text   
        else:
            textrect.topleft = (x, y)                                                       # Set the text position
        surface.blit(textobj, textrect)                                                     # Blit the text on the surface

    @staticmethod
    def drawTextWhite(text, font, surface, x, y, center=False):
        GameUtils.drawText(text, font, surface, x, y, center=center, color=Constants.WHITE)

    @staticmethod
    def draw_hearts(lives, font, surface, x, y):
        text = "Lives: "
        textobj = font.render(text, True, Constants.WHITE)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        heart_spacing = 30                                            # Spacing between hearts
        heart_y_offset = 18                                           # Vertical offset for the hearts
        for i in range(lives):
            surface.blit(Images.heartImage, (x + textrect.width + (i * heart_spacing), y + heart_y_offset))     # Draw a heart for each life

    @staticmethod
    def display_rules(windowSurface):
        pygame.mixer.music.stop()                                    # Stop the background music
        screen_copy = windowSurface.copy()                           # Create a copy of the window surface
        screen_copy.blit(Images.rulesImage, (0, 0))                              # Blit the rules image on the copy
        windowSurface.blit(screen_copy, (0, 0))                      # Blit the copy on the window surface
        pygame.display.flip()                                        # Update the display
        while True:
            for event in pygame.event.get():                         # Get all the events
                if event.type == pygame.QUIT:                        # If the event type is QUIT
                    GameUtils.terminate()                            # Terminate the game
                elif event.type == pygame.KEYDOWN:                   # If the event type is KEYDOWN (if a key is pressed)
                    return                                           # Return from the function

    @staticmethod
    def get_game_speed(score):                                       # Function to get the game speed based on the score
        if score >= 2500:                                            # If the score is greater than or equal to 2500
            return Constants.FPS_INITIAL * 3                         # Triple the initial FPS if score is 2500 or more
        elif score >= 1000:                                          # If the score is greater than or equal to 1000
            return Constants.FPS_INITIAL * 2                         # Double the initial FPS if score is 1000 or more
        elif score >= 500:                                           # If the score is greater than or equal to 500
            return int(Constants.FPS_INITIAL * 1.5)                  # Return 1.5 times the initial FPS
        else:
            return Constants.FPS_INITIAL                             # Return the initial FPS for scores less than 500


class CharacterSelection:
    @staticmethod
    def choose_character_window(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT):
        selected_character = 0                                       # Initialize the selected character index
        player_name = ""                                             # Initialize the player name
        entering_name = True                                         # Flag to check if the player is entering the name
        game_started = False                                         # Flag to check if the game has started
        with_weapons = False                                         # Initialize the with_weapons variable

        # Pre-calculate the positions of the characters that will be displayed when we have to make our character choice
        num_characters = len(character_images)                      # Number of characters
        spacing = WINDOWWIDTH // (num_characters + 1)               # Calculate the spacing between characters
        y_position = WINDOWHEIGHT // 2                              # Calculate the y position for the characters images
        character_rects = []                                        # Initialize the list to hold character rectangles
        margin = 10                                                 # Margin around the character image

        for i, img in enumerate(character_images):
            x = spacing * (i + 1)                                   # Calculate the x position for the character image
            img_rect = img[0].get_rect(center=(x, y_position))      # Create a rectangle for the character image
            img_rect.inflate_ip(margin, margin)                     # Inflate the rectangle by the margin
            character_rects.append(img_rect)                        # Append the rectangle to the list

    
        while not game_started:
            windowSurface.blit(Images.backgroundImage, (0, 0))      # Blit the background image
            GameUtils.drawTextWhite("What's your name?", large_font, windowSurface, WINDOWWIDTH // 2, 50, center=True)                # Draw the prompt for the player's name
            GameUtils.drawTextWhite(player_name, font, windowSurface, WINDOWWIDTH // 2, 130, center=True)                             # Draw the player's name

            if not entering_name:
                GameUtils.drawTextWhite("Choose your character", large_font, windowSurface, WINDOWWIDTH // 2, 200, center=True)       # Draw the prompt to choose a character
                for i, img in enumerate(character_images):
                    img_rect = character_rects[i]                                                                                     # Get the rectangle for the character image
                    windowSurface.blit(img[0], img_rect.inflate(-margin, -margin).topleft)                                            # Blit the character image on the window
                    pygame.draw.rect(windowSurface, Constants.BLACK, img_rect, 3)                                                     # Draw a black border around the character image
                    if i == selected_character:
                        character_color = Constants.BULLET_COLOR.get(i, Constants.BLACK)                                              # Get the color associated with the character (Black if not found)
                        pygame.draw.rect(windowSurface, character_color, img_rect, 5)                                                 # Draw a thicker rectangle with the character's color

                    # Draw the choose button
                    selected_img_rect = character_rects[selected_character]
                    choose_button_rect = pygame.Rect(
                        selected_img_rect.centerx - 75, selected_img_rect.bottom + 10, 150, 50
                    )  # Adjust the positions to be just below the selected image
                    choose_button_color = Constants.BULLET_COLOR.get(selected_character, Constants.BLACK)                                                                          # Get the color associated with the selected character (Black if not found)
                    pygame.draw.rect(windowSurface, choose_button_color, choose_button_rect)                                                                                      # Draw the choose button with the selected color
                    GameUtils.drawText("Choose", Fonts.small_font, windowSurface, choose_button_rect.centerx, choose_button_rect.centery, center=True, color=Constants.WHITE)    # Draw the text on the choose button

            for event in pygame.event.get():
                if event.type == pygame.QUIT:                      # If the event type is QUIT
                    GameUtils.terminate()                          # Terminate the game if the event type is QUIT
                elif event.type == pygame.MOUSEMOTION:      
                    pygame.mouse.set_visible(True)                 # Set the mouse cursor to be visible

                elif event.type == pygame.MOUSEBUTTONDOWN and not entering_name:    
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if a character was clicked
                    for i, rect in enumerate(character_rects):
                        if rect.collidepoint(mouse_x, mouse_y):
                            selected_character = i
                            break  
                    
                    # Check if the choose button was clicked
                    if choose_button_rect.collidepoint(mouse_x, mouse_y):  
                        with_weapons = CharacterSelection.ask_weapons_choice(windowSurface) 
                        game_started = True                      # Set the flag to indicate the game has started
                        pygame.mouse.set_visible(False)          # Hide the mouse cursor

                elif event.type == pygame.KEYDOWN:
                    if entering_name:
                        if event.key == pygame.K_RETURN:
                            if player_name == "":
                                player_name = "Unknown player"   # Set the default name if the player doesn't enter a name
                            entering_name = False                # Set the flag to False to stop entering the name
                        elif event.key == pygame.K_BACKSPACE:    # If the backspace key is pressed
                            player_name = player_name[:-1]       # Remove the last character from the player's name
                        elif len(player_name) < Constants.MAX_NAME_LENGTH: # Check length before adding
                            player_name += event.unicode

                    else:   
                        if event.key == pygame.K_LEFT:
                            selected_character = (selected_character - 1) % len(character_images)       # Select the previous character
                        elif event.key == pygame.K_RIGHT:
                            selected_character = (selected_character + 1) % len(character_images)       # Select the next character
                        elif event.key == pygame.K_RETURN:
                            with_weapons = CharacterSelection.ask_weapons_choice(windowSurface)
                            game_started = True                                                         # Set the flag to indicate the game has started
                            pygame.mouse.set_visible(False)                                             # Hide the mouse cursor

            pygame.display.update()

        selected_character_images = character_images[selected_character]                                # Get the images for the selected character
        return selected_character_images, player_name, selected_character, with_weapons                 # Return the selected character images, player name, selected character index, and with_weapons flag
   
    @staticmethod
    def ask_weapons_choice(windowSurface):
        weapons_question = True
        while weapons_question:
            GameUtils.drawTextWhite('Do you want to play with a weapon?', Fonts.small_font, windowSurface,                          # Draw the question text
                              Constants.WINDOWWIDTH // 2, (Constants.WINDOWHEIGHT / 3) + 350, center=True)                          # Center the text
            GameUtils.drawTextWhite('Press Y for Yes, N for No', Fonts.small_font, windowSurface,                                   # Draw the instructions text
                              Constants.WINDOWWIDTH // 2, (Constants.WINDOWHEIGHT / 3) + 400, center=True)                          # Center the text
            pygame.display.update()
            for event_q in pygame.event.get():
                if event_q.type == pygame.QUIT:                                                                                     # If the event type is QUIT
                    GameUtils.terminate()                                                                                           # Terminate the game
                if event_q.type == pygame.KEYDOWN:
                    if event_q.key == pygame.K_y:                                                                                   # If the key pressed is Y
                        return True                                                                                                 # Return True (play with weapons)
                    elif event_q.key == pygame.K_n:                                                                                 # If the key pressed is N
                        return False                                                                                                # Return False (play without weapons)
class Countdown:
    @staticmethod
    def display_the_countdown(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT):       
        for count in range(3, 0, -1):
            windowSurface.blit(Images.backgroundImage, (0, 0))                                                                                                          # Blit the background image
            GameUtils.drawTextWhite(f"{player_name}, are you ready?", Fonts.small_font, windowSurface, WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 3, center=True)      # Draw the prompt for the player's name
            windowSurface.blit(character_image, (WINDOWWIDTH // 2 - character_image.get_width() // 2, WINDOWHEIGHT // 2 - character_image.get_height() // 2))           # Blit the character image on the window
            GameUtils.drawTextWhite(f"Starting in {count}", Fonts.small_font, windowSurface, WINDOWWIDTH // 2, Constants.WINDOWHEIGHT - 100, center=True)               # Draw the countdown text
            pygame.display.update()                                                                                                                                     # Update the display
            pygame.time.wait(1000)                                                                                                                                      # Wait for 1 second
                                                                                                                                                                        
        windowSurface.blit(Images.backgroundImage, (0, 0))                                                                                                              # Blit the background image
        GameUtils.drawTextWhite("GO!", Fonts.large_font, windowSurface, Constants.WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 2, center=True)                           # Draw the "GO!" text
        pygame.display.update()                                                                                                                                         # Update the display
        pygame.time.wait(1000)                                                                                                                                          # Wait for 1 second


# Game class
class Game:
    def __init__(self):         
        self.windowSurface = windowSurface                        # Set the window surface
        self.FPS = Constants.FPS_INITIAL                          # Set the frames per second (FPS)
        self.mainClock = mainClock                                # Set the main clock
        self.topScore = 0                                         # Initialize the top score
        self.paused = False                                       # Set the paused flag to False
        self.background_x1 = 0                                    # Set the x-coordinate of the first background image
        self.background_x2 = Constants.WINDOWWIDTH                # Initialize the second background x position
        self.scroll_speed = 2                                     # Set the scroll speed
        self.playing_explosion = False                            # Initialize the explosion playing state
        self.explosion_x = 0                                      # Initialize the explosion x position
        self.explosion_y = 0                                      # Initialize the explosion y position
        self.explosion_frames = Images.explosion_frames           # Get the explosion frames
        self.current_explosion_frame = 0                          # Initialize the current explosion frame
        self.explosion_animation_speed = 5                        # Set the explosion animation speed
        self.character_images = Images.character_images           # Get the character images
        self.selected_character_images = []                       # Initialize the selected character images
        self.player = None                                        # Initialize the player
        self.baddies = []                                         # Initialize the list of baddies
        self.bullets = []                                         # Initialize the list of bullets
        self.score = 0                                            # Initialize the score
        self.lives = 3                                            # Initialize the number of lives at the start of the game
        self.nb_baddies_destroyed = 0                             # Initialize the number of baddies destroyed
        self.baddieAddCounter = 0                                 # Initialize the baddie add counter
        self.reverseCheat = False                                 # Initialize the reverse cheat state
        self.slowCheat = False                                    # Initialize the slow cheat state
        self.star_counter = 0                                     # Initialize the star counter
        self.starRect = None                                      # Initialize the star rectangle
        self.star_active = False                                  # Initialize the star active state
        self.star_effect_counter = 0                              # Initialize the star effect counter
        self.star_speed = -3                                      # Set the star speed (negative to move to the left)
        self.first_run = True                                     # Initialize the first run state
        self.is_playing = False                                   # Initialize the playing state
        self.with_weapons = False                                 # Track if the player wants to play with weapons
        self.smoke = Smoke()                                      # Initialize the smoke object

    def terminate_game(self):
        GameUtils.terminate()                                     # Terminate the game

    def display_rules(self):                                      # Function to display the rules
        GameUtils.display_rules(self.windowSurface)               # Call the display_rules function 

    def run(self):
        if self.first_run:
            self.show_start_screen()                              # Show the start screen
            self.choose_character()                               # Choose the character
            self.first_run = False                                # Set to False after first run
        self.game_loop()                                          # Start the game loop

    def show_start_screen(self):                                  # Function to show the start screen
        self.windowSurface.blit(Images.startImage, (0, 0))        # Blit the start image as the background
        GameUtils.drawTextWhite('Press a key to start', Fonts.large_font, self.windowSurface,                                  # Draw the prompt to start the game
                           Constants.WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 3, center=True)                          # Center the text
        GameUtils.drawTextWhite('Press R to see rules', Fonts.small_font, self.windowSurface,                                  # Draw the prompt to see the rules
                           Constants.WINDOWWIDTH // 2, (Constants.WINDOWHEIGHT // 3) + 400, center=True)                  # Center the text
        pygame.display.update()                                  # Update the display
        GameUtils.waitForPlayerToPressKey(self)                  # Wait for the player to press a key

    def choose_character(self):
        selected_character_images, player_name, selected_character, self.with_weapons = CharacterSelection.choose_character_window(
            self.windowSurface, Fonts.font, Fonts.large_font, self.character_images, Constants.WHITE, Constants.BLACK, Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT
        )   
        self.selected_character_images = selected_character_images
        self.player = Player(self.selected_character_images, selected_character)                                           # Create the player object
        Countdown.display_the_countdown(self.windowSurface, Fonts.large_font, self.player.image, player_name, Constants.WHITE, Constants.WINDOWWIDTH, Constants.WINDOWHEIGHT)   # Display the countdown

    def game_loop(self):
        pygame.mouse.set_visible(False)                         # Hide the mouse cursor during gameplay
        pygame.mixer.music.play(-1, 0.0)                        # Play the background music
        self.is_playing = True                                  # Set the flag to True when the game starts
        while True:
            if not self.paused:
                self.score += 1                                 # Increment the score
            self.handle_events()
            if self.paused:                                     # If the game is paused
                self.show_paused_screen()                       # Show the paused screen
                continue    
            self.update_game_state()
            self.draw()
            self.check_collisions()
            self.mainClock.tick(self.FPS)
            if self.lives <= 0:
                break                                          # Exit the game loop when lives are depleted
        self.is_playing = False                                # Set the flag to False when the game ends
        self.show_game_over_screen()                           # Show the game over screen
        self.reset_game()                                      # Reset the game
        self.run()                                             # Restart the game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate_game()       
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate_game()
                if event.key == K_p:
                    self.paused = not self.paused
                if not self.paused:
                    if event.key in (K_LEFT, K_a):             # If the left arrow key is pressed
                        self.player.moveLeft = True            # Move the player left
                        self.player.moveRight = False
                    if event.key in (K_RIGHT, K_d):            # If the right arrow key is pressed
                        self.player.moveRight = True           # Move the player right
                        self.player.moveLeft = False
                    if event.key in (K_UP, K_w):               # If the up arrow key is pressed
                        self.player.moveUp = True              # Move the player up
                        self.player.moveDown = False    
                    if event.key in (K_DOWN, K_s):             # If the down arrow key is pressed
                        self.player.moveDown = True            # Move the player down
                        self.player.moveUp = False
                    if event.key == K_f and self.with_weapons:   # If the F key is pressed and the player is playing with weapons
                        self.player.shoot_bullet(self.bullets)   # Shoot a bullet
                if event.key == K_r:                           # If the key pressed is R
                    pygame.mixer.music.stop()                  # Stop the background music
                    Sounds.immortality_music.stop()            # Stop the immortality music
                    self.display_rules()                       # Display the rules
                    if self.is_playing:                        # Restart the background music only if the game is running
                        pygame.mixer.music.play()

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    self.player.moveLeft = False                # Stop moving the player left
                if event.key in (K_RIGHT, K_d):
                    self.player.moveRight = False               # Stop moving the player right
                if event.key in (K_UP, K_w):
                    self.player.moveUp = False                  # Stop moving the player up
                if event.key in (K_DOWN, K_s):
                    self.player.moveDown = False                # Stop moving the player down
            elif event.type == MOUSEMOTION:     
                self.player.rect.centery = event.pos[1]         # Move the player with the mouse

    def show_paused_screen(self):
        self.windowSurface.blit(Images.pausedImage, (0, 0))     # Blit the paused image on the window
        GameUtils.drawTextWhite('Game Paused', Fonts.big_font, self.windowSurface, Constants.WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 2 - 30, center=True)     # Draw the paused text
        GameUtils.drawTextWhite('Press P to continue', Fonts.small_font, self.windowSurface, Constants.WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 2 + 30, center=True)   # Draw the prompt to continue
        Sounds.immortality_music.stop()                         # Stop the immortality music
        pygame.mixer.music.play()                               # Play the background music
        pygame.display.update()

    def update_game_state(self):
        # Background scrolling
        self.background_x1 -= self.scroll_speed                 # Scroll the first background
        self.background_x2 -= self.scroll_speed                 # Scroll the second background
        if self.background_x1 <= -Constants.WINDOWWIDTH:
            self.background_x1 = Constants.WINDOWWIDTH          # Reset the first background position
        if self.background_x2 <= -Constants.WINDOWWIDTH:
            self.background_x2 = Constants.WINDOWWIDTH          # Reset the second background position
        
        # Projectiles update
        for bullet in self.bullets[:]:
            bullet['rect'].x += bullet['speed']                 # Move the bullet
            if bullet['rect'].left > Constants.WINDOWWIDTH:     # If the bullet goes off the screen
                self.bullets.remove(bullet)                     # Remove the bullet
        
        # Baddies spawn
        self.spawn_baddies()                                    # Spawn baddies

        
        # Star logic
        self.update_star()                                      # Update the star

        # Move player
        self.player.update_position()                           # Update the player position
        
        # Move baddies
        for baddie in self.baddies[:]:
            baddie.update_position()
            if baddie.rect.right < -baddie.size:
                self.baddies.remove(baddie)

    def spawn_baddies(self):
        if not self.reverseCheat and not self.slowCheat:
            self.baddieAddCounter += 1                              # Increment the baddie add counter
        if self.baddieAddCounter == Constants.ADD_NEW_BADDIE_RATE:  # If the baddie add counter reaches the rate
            self.baddieAddCounter = 0                               # Reset the baddie add counter
            baddie = Baddie()                                       # Create a new baddie
            self.baddies.append(baddie)                             # Add the baddie to the list of baddies
        # Add spaceships at certain scores  
        if self.score % 100 == 0:                                   # If the score is a multiple of 100
            spaceship = Spaceship()                                 # Create a spaceship
            self.baddies.append(spaceship)                          # Add the spaceship to the list of baddies

    def update_star(self):
        self.star_counter += 1                                      # Increment the star counter
        STAR_APPEAR_FRAMES = Constants.FPS_INITIAL * 10             # Set the number of frames for the star to appear
        if self.star_counter >= STAR_APPEAR_FRAMES:                 # If the star counter reaches the number of frames
            self.starRect = pygame.Rect(                            # Create a star rectangle
                Constants.WINDOWWIDTH,                              # Start at the right edge       
                random.randint(0, Constants.WINDOWHEIGHT - 30),
                30, 30                                              # Set the star size to 30x30 pixels
            )
            self.star_counter = 0                                   # Reset the star counter
        if self.starRect:
            self.starRect.x += self.star_speed                      # Move the star to the left
            if self.starRect.right < 0:                             # If the star goes off the screen
                self.starRect = None                                # Remove the star when it goes off-screen
        if self.starRect and self.player.rect.colliderect(self.starRect):   # If the player collides with the star
            self.star_active = True                                 # Set the star active state to True
            self.star_effect_counter = Constants.FPS_INITIAL * 10   # Set the star effect counter 
            self.starRect = None                                    # Remove the star when the player collides with it
        if self.star_active:                                        # If the star is active
            self.star_effect_counter -= 1                           # Decrement the star effect counter
            if self.star_effect_counter <= 0:                       # If the star effect counter reaches 0
                self.star_active = False                            # Set the star active state to False
        self.FPS = GameUtils.get_game_speed(self.score)             # Get the game speed based on the score
        if self.star_active:                                        # If the star is active
            self.FPS *= 3                                           # Triple the game speed
            Sounds.immortality_music.play()                         # Play the immortality music
        else:
            Sounds.immortality_music.stop()                         # Stop the immortality music if the star is not active

        # Update smoke position
        self.smoke.x = self.player.rect.centerx                     # Set the smoke x position (on the player)
        self.smoke.y = self.player.rect.centery                     # Set the smoke y position (on the player)
        self.smoke.update()

    
    def draw(self):
        self.windowSurface.blit(Images.backgroundImage, (self.background_x1, 0))    # Blit the first background image
        self.windowSurface.blit(Images.backgroundImage, (self.background_x2, 0))    # Blit the second background image
        
        self.smoke.draw()                                                            # Draw the smoke behind the player


        if self.with_weapons:                                                       # If the player is playing with weapons
            GameUtils.drawTextWhite('Score: %s' % (self.score), Fonts.font, self.windowSurface, 10, 0)                                      # Draw the score
            GameUtils.drawTextWhite('Top Score: %s' % (self.topScore), Fonts.font, self.windowSurface, 10, 40)                              # Draw the top score
            GameUtils.drawTextWhite(f'Number of baddies destroyed: {self.nb_baddies_destroyed}', Fonts.font, self.windowSurface, 10, 80)    # Draw the number of baddies destroyed (Line that won't be there if you play without a weapon)
            GameUtils.draw_hearts(self.lives, Fonts.font, self.windowSurface, 10, 120)                                                      # Draw the hearts for the number of lives
        else:
            GameUtils.drawTextWhite('Score: %s' % (self.score), Fonts.font, self.windowSurface, 10, 0)                                      # Draw the score
            GameUtils.drawTextWhite('Top Score: %s' % (self.topScore), Fonts.font, self.windowSurface, 10, 40)                              # Draw the top score
            GameUtils.draw_hearts(self.lives, Fonts.font, self.windowSurface, 10, 80)                                                       # Draw the hearts for the number of lives
        self.windowSurface.blit(self.player.image, self.player.rect)                                                                        # Blit the player image
        for baddie in self.baddies: 
            self.windowSurface.blit(baddie.surface, baddie.rect)                                                                            # Blit the baddie image
        if self.starRect:   
            self.windowSurface.blit(Images.starImage, self.starRect)                                                                        # Blit the star image
        for bullet in self.bullets:
            pygame.draw.rect(self.windowSurface, bullet['color'], bullet['rect'])
        if self.star_active:
            immortality_seconds = self.star_effect_counter // Constants.FPS_INITIAL                                                         # Calculate the number of seconds the star effect will last
            if self.with_weapons:
                GameUtils.drawTextWhite(f"Immortality: {immortality_seconds}", Fonts.font, self.windowSurface, 10, 160)                     # Draw the immortality display
            else:
                GameUtils.drawTextWhite(f"Immortality: {immortality_seconds}", Fonts.font, self.windowSurface, 10, 120)                     # Draw the immortality display (adjust the height of the imortality display if you're playing without a weapon)
        pygame.display.update()

    def check_collisions(self):
        # Bullet collisions
        for bullet in self.bullets[:]:
            for baddie in self.baddies[:]:
                if bullet['rect'].colliderect(baddie.rect):
                    baddie.health -= 1                          # Decrement the baddie's health
                    self.bullets.remove(bullet)                 # Remove the bullet
                    if baddie.health <= 0:                      # If the baddie's health is less than or equal to 0
                        self.remove_baddie(baddie)              # Remove the baddie
                    break
        # Player collisions
        if not self.star_active:                                # If the immortality star is not active
            for baddie in self.baddies[:]:
                if baddie.type == 'spaceship':      
                    if self.detect_pixel_collision(baddie):     # If the player collides with the spaceship
                        self.lives -= baddie.damage             # Decrement the player's lives
                        self.handle_explosion(baddie, explosion_scale=1.3, is_destroyed=False)      # Handle the explosion
                        if self.lives <= 0:
                            break
                else:
                    if self.player.rect.colliderect(baddie.rect):
                        self.lives -= baddie.damage            # Decrement the player's lives
                        self.handle_explosion(baddie, explosion_scale=2, is_destroyed=False)        # Handle the explosion
                        if self.lives <= 0:
                            break

    def detect_pixel_collision(self, baddie):                                                      # Function to detect pixel collision
        offset = (baddie.rect.x - self.player.rect.x, baddie.rect.y - self.player.rect.y)          # Calculate the offset
        return self.player.mask.overlap(baddie.mask, offset)                                       # Check for pixel collision

    def handle_explosion(self, baddie, explosion_scale, is_destroyed=True):
        if baddie in self.baddies:
            self.remove_baddie(baddie, is_destroyed)                                               # Remove the baddie
            self.playing_explosion = True                                                          # Set the playing explosion state to True
            self.explosion_x = baddie.rect.centerx                                                 # Set the explosion x position
            self.explosion_y = baddie.rect.centery                                                 # Set the explosion y position
            self.explosion_size = baddie.size * explosion_scale                                    # Set the explosion size
            pygame.mixer.music.stop()                                                              # Stop the background music
            Sounds.baddie_hit_sound.play()                                                         # Play the baddie hit sound
            self.play_explosion()
            if self.lives > 0:
                self.player.update_image(4 - self.lives)                                           # Update the player image
                self.player.rect.topleft = (20, Constants.WINDOWHEIGHT / 2)                        # Reset the player position
                self.baddies.clear()                                                               # Clear the baddies list
                pygame.time.wait(1000)                                                             # Wait for 1 second
            pygame.mixer.music.play()                                                              # Play the background music

    def play_explosion(self):
        for img in self.explosion_frames:                                                          # For each explosion frame
            frame_surface = pygame.transform.scale(img, (int(self.explosion_size), int(self.explosion_size)))       # Scale the explosion frame
            frame_rect = frame_surface.get_rect(center=(self.explosion_x, self.explosion_y))       # Set the explosion frame position
            self.windowSurface.blit(frame_surface, frame_rect)                                     # Blit the explosion frame
            pygame.display.update()                                                                # Update the display
            self.mainClock.tick(self.FPS)                                                          # Tick the clock
        self.playing_explosion = False                                                             # Set the playing explosion state to False

    def remove_baddie(self, baddie, is_destroyed=True):     
        if baddie in self.baddies:                                                                # If the baddie is in the baddies list
            self.baddies.remove(baddie)                                                           # Remove the baddie
            if is_destroyed:                                                                      # If the baddie is destroyed
                self.nb_baddies_destroyed += 1                                                    # Increment the number of baddies destroyed
                Sounds.baddie_shoot_sound.play()                                                  # Play the baddie shoot sound
                if self.nb_baddies_destroyed == 30:                                               # If 30 baddies are destroyed
                    self.lives += 1                                                               # Add a life when 30 baddies are destroyed

    def show_game_over_screen(self):        
        pygame.mixer.music.stop()                                                                 # Stop the background music
        Sounds.gameOverSound.play()                                                               # Play the game over sound

        # Load and display the explosion image
        explosion_image = pygame.image.load("explosion08.png")                                   # Load the explosion image                  
        original_width, original_height = explosion_image.get_size()                             # Get the original width and height 
        scaled_width, scaled_height = original_width * 2, original_height * 2                    # Scale the width and height
        explosion_image = pygame.transform.scale(explosion_image, (scaled_width, scaled_height))    
        image_rect = explosion_image.get_rect(center=(Constants.WINDOWWIDTH // 2, Constants.WINDOWHEIGHT // 2))
        self.windowSurface.blit(explosion_image, image_rect.topleft)

        # Display "GAME OVER" and "Press a key to play again" text
        game_over_text = 'GAME OVER'                                                                                                    # Set the game over text
        retry_text = 'Press a key to play again'                                                                                        # Set the retry text
        game_over_x = (Constants.WINDOWWIDTH - Fonts.game_over_font.size(game_over_text)[0]) // 2                                       # Calculate the x position to center the game over text                     
        retry_x = (Constants.WINDOWWIDTH - Fonts.retry_font.size(retry_text)[0]) // 2                                                   # Calculate the x position to center the retry text
        GameUtils.drawTextWhite(game_over_text, Fonts.game_over_font, self.windowSurface, game_over_x, (Constants.WINDOWHEIGHT / 3))    # Draw the game over text     
        GameUtils.drawTextWhite(retry_text, Fonts.retry_font, self.windowSurface, retry_x, (Constants.WINDOWHEIGHT / 3) + 100)          # Draw the retry text

        pygame.display.update()
        pygame.time.wait(2000)                                                                 # Wait for 2 seconds
        
        # Check if the player has beaten the top score
        print(f"Score: {self.score}, Top Score: {self.topScore}")  # Debug
        if self.score > self.topScore:                                                        # If the score is greater than the top score
            self.topScore = self.score                                                        # Set the top score to the score
            congrats_y = (Constants.WINDOWHEIGHT / 3) + 250                                   # Set the y position for the congratulations text
            for text in ["Congratulations,", "You've beaten your record!", f"Now your top score is {self.topScore}"]:   
                GameUtils.drawText(text, Fonts.small_font, self.windowSurface, (Constants.WINDOWWIDTH - Fonts.small_font.size(text)[0]) / 2, congrats_y)        # Draw the congratulations text
                congrats_y += 50                                                                                                                                # Increment the y position
            pygame.display.update()

        self.FPS = Constants.FPS_INITIAL                                                      # Reset the frames per second
        GameUtils.waitForPlayerToPressKey(self)                                               # Wait for the player to press a key
        Sounds.gameOverSound.stop()                                                           # Stop the game over sound

    def reset_game(self):
        self.baddies.clear()
        self.bullets.clear()
        self.score = 0
        self.lives = 3
        self.nb_baddies_destroyed = 0
        self.baddieAddCounter = 0
        self.star_counter = 0
        self.starRect = None
        self.star_active = False
        self.star_effect_counter = 0
        self.player.reset()

class Player:
    def __init__(self, images, selected_character):
        self.images = images                                         # Store the images for the player
        self.selected_character = selected_character                 # Store the selected character index
        self.image = self.images[1]                                  # Set the initial image for the player
        self.image = pygame.transform.scale(self.image, (70, 70))    # Scale the image
        self.rect = self.image.get_rect()                            # Get the rectangle for the image
        self.rect.topleft = (20, Constants.WINDOWHEIGHT / 2)         # Set the initial position of the player
        self.moveLeft = False                                        # Initialize the move left flag
        self.moveRight = False                                       # Initialize the move right flag
        self.moveUp = False                                          # Initialize the move up flag
        self.moveDown = False                                        # Initialize the move down flag
        self.mask = pygame.mask.from_surface(self.image)             # Create a mask for pixel-perfect collision detection

    def update_position(self):
        if self.moveUp and self.rect.top > 0:   
            self.rect.move_ip(0, -1 * Constants.PLAYER_MOVE_RATE)     # Move the player up
        if self.moveDown and self.rect.bottom < Constants.WINDOWHEIGHT:
            self.rect.move_ip(0, Constants.PLAYER_MOVE_RATE)          # Move the player down

    def shoot_bullet(self, bullets):
        bullet_color = Constants.BULLET_COLOR.get(self.selected_character, (255, 0, 0))  # Get the bullet color based on the selected character
        bullet = {
            'rect': pygame.Rect(self.rect.right, self.rect.centery - Constants.BULLET_SIZE[1] // 2, Constants.BULLET_SIZE[0], Constants.BULLET_SIZE[1]),  # Create the bullet rectangle
            'speed': Constants.BULLET_SPEED,                        # Set the bullet speed
            'color': bullet_color                                   # Set the bullet color
        }
        bullets.append(bullet)                                      # Add the bullet to the bullets list

    def update_image(self, index):
        self.image = self.images[index]                             # Update the player image
        self.image = pygame.transform.scale(self.image, (70, 70))   # Scale the image
        self.mask = pygame.mask.from_surface(self.image)            # Update the mask

    def reset(self):
        self.image = self.images[1]                                 # Reset the player image
        self.image = pygame.transform.scale(self.image, (70, 70))   # Scale the image
        self.rect.topleft = (20, Constants.WINDOWHEIGHT / 2)        # Reset the player position
        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False  # Reset movement flags
        self.mask = pygame.mask.from_surface(self.image)            # Update the mask

class Baddie:
    BADDIE_TYPES = {
        'planet': {
            'probability': 50,                                     # Probability of the baddie type
            'image': 'planet',                                     # Image name   
            'health': 1,                                           # Set the health to 1 (you need to shoot the planet once to destroy it)
            'damage': 1                                            # Set the damage to 1 (if you collide with the planet, you lose 1 life)
        },
        'strong_planet': {
            'probability': 30,                                     # Probability of the baddie type
            'image': 'strong_planet',                              # Image name     
            'health': 2,                                           # Set the health to 2 (you need to shoot the planet twice to destroy it)   
            'damage': 1                                            # Set the damage to 1 (if you collide with the planet, you lose 1 life)
        },
        'super_strong_planet': {
            'probability': 20,                                     # Probability of the baddie type
            'image': 'super_strong_planet',                        # Image name
            'health': 3,                                           # Set the health to 3 (you need to shoot the planet three times to destroy it)
            'damage': 1                                            # Set the damage to 1 (if you collide with the planet, you lose 1 life)
        }
    }

    def __init__(self):
        self.size = random.randint(Constants.BADDIE_MIN_SIZE, Constants.BADDIE_MAX_SIZE)            # Set the size of the baddie (random size between BADDIE_MIN_SIZE and BADDIE_MAX_SIZE)
        prob = random.randint(1, 100)                                                               # Generate a random number between 1 and 100    
        cumulative_prob = 0                                                                         # Initialize the cumulative probability
        for baddie_type, properties in self.BADDIE_TYPES.items():                                   # For each baddie type
            cumulative_prob += properties['probability']                                            # Increment the cumulative probability
            if prob <= cumulative_prob:                                                             # If the random number is less than or equal to the cumulative probability
                self.type = baddie_type                                                             # Set the baddie type
                self.image = Images.baddie_images[properties['image']]                              # Set the baddie image        
                self.health = properties['health']                                                  # Set the health
                self.damage = properties['damage']                                                  # Set the damage
                break
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))                   # Scale the image according to the baddie's size
        self.rect = self.surface.get_rect()                                                         # Get the rectangle for the image
        self.rect.x = Constants.WINDOWWIDTH + self.size                                             # Position the baddie off-screen to the right
        self.rect.y = random.randint(0, Constants.WINDOWHEIGHT - self.size)                         # Randomize the vertical position within the window height
        self.speed = -random.randint(Constants.BADDIE_MIN_SPEED, Constants.BADDIE_MAX_SPEED)        # Set the movement speed towards the left (between BADDIE_MIN_SPEED and BADDIE_MAX_SPEED) 
        self.mask = pygame.mask.from_surface(self.surface)

    def update_position(self):                                                                      # Function to update the baddie's position    
        self.rect.move_ip(self.speed, 0)                                                            # Move the baddie
       
class Spaceship(Baddie):
    def __init__(self):
        size = random.randint(Constants.SPACE_MIN_SIZE, Constants.SPACE_MAX_SIZE)                  # Set the size of the spaceship (random size between SPACE_MIN_SIZE and SPACE_MAX_SIZE)
        super().__init__()
        self.size = size                                                                           # Set the size of the spaceship    
        self.type = 'spaceship'                                                                    # Set the type to 'spaceship'
        self.image = Images.spaceshipImage                                                         # Set the spaceship image 
        self.health = 5                                                                            # Set the health to 5 (you need to shoot the spaceship 5 times to destroy it)
        self.damage = 2                                                                            # Set the damage to 2 (if you collide with the spaceship, you lose 2 lives)
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))                  # Scale the image according to the spaceship's size
        self.mask = pygame.mask.from_surface(self.surface)                                         # Create a mask for pixel-perfect collision detection
        self.rect = self.surface.get_rect()                                                        # Get the rectangle for the image
        self.reset_position()                                                                      # Reset the position of the spaceship

    def reset_position(self):
        self.rect.x = Constants.WINDOWWIDTH + self.size                                            # Position the spaceship off-screen to the right
        self.rect.y = random.randint(0, Constants.WINDOWHEIGHT - self.size)                        # Randomize the vertical position within the window height
        self.speed = -random.randint(Constants.BADDIE_MIN_SPEED, Constants.BADDIE_MAX_SPEED)       # Set the movement speed towards the left (between BADDIE_MIN_SPEED and BADDIE_MAX_SPEED) 

# Start the game
if __name__ == '__main__':  # If the script is run directly
    game = Game()           # Create a new game instance
    game.run()              # Run the game