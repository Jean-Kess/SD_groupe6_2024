# dodger with arms
import pygame
import random
import numpy as np  # Import numpy for mask creation
import sys
from pygame.locals import *
import cv2
from choosing_your_character import choose_character, display_the_countdown

# Constants
WINDOWWIDTH = 800 
WINDOWHEIGHT = 800
TEXTCOLOR = (255, 255, 255)  # White
BACKGROUNDCOLOR = (255, 255, 255)  # White
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)  
FPS_INITIAL = 30
SPACEMINSIZE = 150
SPACEMAXSIZE = 250
BADDIEMINSIZE = 15
BADDIEMAXSIZE = 60
BADDIEMINSPEED = 3
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 15
PLAYERMOVERATE = 5
BULLET_SIZE = (10, 5)
BULLET_SPEED = 10
BULLET_COLOR = {
    0: (163, 195, 235),   # Blue for the first character (index 0)
    1: (139, 207, 186),   # Green for the second character (index 1)
    2: (243, 175, 197),   # Pink/Magenta for the third (index 2)
    3: (255, 214, 52)     # Yellow for the fourth (index 3)
}

# Initialize Pygame
pygame.init()
pygame.mixer.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')


# Fonts
small_font = pygame.font.Font('gameFont.ttf', 28)
font = pygame.font.Font('Anton-Regular.ttf', 38)
large_font = pygame.font.Font('Anton-Regular.ttf', 48) 
game_over_font = pygame.font.Font('gameFont.ttf', 64)
retry_font = pygame.font.Font('gameFont.ttf', 35)

# Sounds
gameOverSound = pygame.mixer.Sound('GameOver!.wav')
pygame.mixer.music.load('Background.wav')
immortality_music = pygame.mixer.Sound('Immortality.wav')
baddie_hit_sound = pygame.mixer.Sound('Boom.wav')
baddie_shoot_sound = pygame.mixer.Sound('Boom.wav')

# Load Images
baddieImage1 = pygame.image.load('planet09.png')
baddieImage2 = pygame.image.load('planet07.png')
baddieImage3 = pygame.image.load('planet01.png')
spaceshipImage = pygame.image.load('spaceship2.png')
starImage = pygame.image.load('starImage.png')
starImage = pygame.transform.scale(starImage, (30, 30))
heartImage = pygame.image.load('heartImage.png')
heartImage = pygame.transform.scale(heartImage, (22, 22))
backgroundImage = pygame.image.load('backgroundsky.png').convert()
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
pausedImage = pygame.image.load('pausedImage.png').convert()
pausedImage = pygame.transform.scale(pausedImage, (WINDOWWIDTH, WINDOWHEIGHT))

# Load Explosion Frames
explosion_frames = [pygame.image.load(f'explosion0{i}.png').convert_alpha() for i in range(9)]

# Characters
character_Blue = [
    pygame.image.load("alienBlue.png"),
    pygame.image.load("character_B_damage0.png"),
    pygame.image.load("character_B_damage1.png"),
    pygame.image.load("character_B_damage2.png")
]

character_Green = [
    pygame.image.load("alienGreen.png"),
    pygame.image.load("character_G_damage0.png"),
    pygame.image.load("character_G_damage1.png"),
    pygame.image.load("character_G_damage2.png")
]

character_Pink = [
    pygame.image.load("alienPink.png"),
    pygame.image.load("character_P_damage0.png"),
    pygame.image.load("character_P_damage1.png"),
    pygame.image.load("character_P_damage2.png")
]

character_Yellow = [
    pygame.image.load("alienYellow.png"),
    pygame.image.load("character_Y_damage0.png"),
    pygame.image.load("character_Y_damage1.png"),
    pygame.image.load("character_Y_damage2.png")
]

character_images = [character_Blue, character_Green, character_Pink, character_Yellow]

# Classes
class Game:
    def __init__(self):
        self.windowSurface = windowSurface
        self.FPS = FPS_INITIAL
        self.mainClock = mainClock
        self.topScore = 0
        self.paused = False
        self.background_x1 = 0
        self.background_x2 = WINDOWWIDTH
        self.scroll_speed = 2
        self.playing_explosion = False
        self.explosion_x = 0
        self.explosion_y = 0
        self.explosion_frames = explosion_frames
        self.current_explosion_frame = 0
        self.explosion_animation_speed = 5
        self.character_images = character_images
        self.selected_character_images = []
        self.player = None
        self.baddies = []
        self.bullets = []
        self.score = 0
        self.lives = 3
        self.nb_baddies_destroyed = 0
        self.baddieAddCounter = 0
        self.reverseCheat = False
        self.slowCheat = False
        self.star_counter = 0
        self.starRect = None
        self.star_active = False
        self.star_effect_counter = 0
        self.star_speed = -3  # Added star_speed attribute
        self.load_assets()
        self.first_run = True
        self.is_playing = False 
    
    def load_assets(self):
        # Load all required assets
        pass  # Assets are already loaded globally
    
    def terminate(self):
        pygame.quit()
        sys.exit()
    
    def run(self):
        if self.first_run:
            self.show_start_screen()
            self.choose_character()
            self.first_run = False  # Set to False after first run
        self.game_loop()
    
    def show_start_screen(self):
        self.windowSurface.fill(BACKGROUNDCOLOR)
        drawText('Press a key to start', pygame.font.Font('gameFont.ttf', 40), self.windowSurface,
                 (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 40).size('Press a key to start.')[0]) // 2,
                 (WINDOWHEIGHT / 3) + 50)
        drawText('Press R to see rules', pygame.font.Font('gameFont.ttf', 25), self.windowSurface,
                 (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 25).size('Press R to see rules')[0]) // 2,
                 (WINDOWHEIGHT / 3) + 150)
        pygame.display.update()
        waitForPlayerToPressKey(self)
    
    def choose_character(self):
        character_image, player_name, selected_character = choose_character(
            self.windowSurface, font, large_font, self.character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT
        )
        character_index = self.character_images.index(character_image)
        self.selected_character_images = self.character_images[character_index]
        self.player = Player(self.selected_character_images, selected_character)
        display_the_countdown(self.windowSurface, large_font, self.player.image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT)
    
    def game_loop(self):
        pygame.mouse.set_visible(False)  # Hide the mouse cursor during gameplay
        pygame.mixer.music.play(-1, 0.0)
        self.is_playing = True  # Set the flag to True when the game starts
        while True:
            if not self.paused:
                self.score += 1
            self.handle_events()
            if self.paused:
                self.show_paused_screen()
                continue
            self.update_game_state()
            self.draw()
            self.check_collisions()
            self.mainClock.tick(self.FPS)
            if self.lives <= 0:
                break  # Exit the game loop when lives are depleted
        self.is_playing = False  # Set the flag to False when the game ends
        self.show_game_over_screen()
        self.reset_game()
        self.run()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.terminate()
                if event.key == K_p:
                    self.paused = not self.paused
                if not self.paused:
                    if event.key == K_LEFT or event.key == K_a:
                        self.player.moveLeft = True
                        self.player.moveRight = False
                    if event.key == K_RIGHT or event.key == K_d:
                        self.player.moveRight = True
                        self.player.moveLeft = False
                    if event.key == K_UP or event.key == K_w:
                        self.player.moveUp = True
                        self.player.moveDown = False
                    if event.key == K_DOWN or event.key == K_s:
                        self.player.moveDown = True
                        self.player.moveUp = False
                    if event.key == K_f:
                        self.player.shoot_bullet(self.bullets)
                if event.key == K_r:
                    pygame.mixer.music.stop()
                    immortality_music.stop()
                    display_rules()
                    if game.is_playing:  # Restart the background music only if the game is running
                        pygame.mixer.music.play()
                    
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_a:
                    self.player.moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    self.player.moveRight = False
                if event.key == K_UP or event.key == K_w:
                    self.player.moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    self.player.moveDown = False
            elif event.type == MOUSEMOTION:
                self.player.rect.centery = event.pos[1]
    
    def show_paused_screen(self):
        self.windowSurface.blit(pausedImage, (0, 0))
        paused_text = 'Paused, press P to continue playing' 
        paused_x = (WINDOWWIDTH - pygame.font.Font('gameFont.ttf', 25).size(paused_text)[0]) // 2
        drawText(paused_text, pygame.font.Font('gameFont.ttf', 25), self.windowSurface, paused_x, WINDOWHEIGHT//3)
        immortality_music.stop()
        pygame.mixer.music.play()
        pygame.display.update()
    
    def update_game_state(self):
        # Background scrolling
        self.background_x1 -= self.scroll_speed
        self.background_x2 -= self.scroll_speed
        if self.background_x1 <= -WINDOWWIDTH:
            self.background_x1 = WINDOWWIDTH
        if self.background_x2 <= -WINDOWWIDTH:
            self.background_x2 = WINDOWWIDTH
        
        # Projectiles update
        for bullet in self.bullets[:]:
            bullet['rect'].x += bullet['speed']
            if bullet['rect'].left > WINDOWWIDTH:
                self.bullets.remove(bullet)
        
        # Baddies spawn
        self.spawn_baddies()
        
        # Star logic
        self.update_star()
        
        # Move player
        self.player.update_position()
        
        # Move baddies
        for baddie in self.baddies:
            baddie.update_position()
            if baddie.rect.right < -baddie.size: #
                self.baddies.remove(baddie)
    
    def spawn_baddies(self):
        if not self.reverseCheat and not self.slowCheat:
            self.baddieAddCounter += 1
        if self.baddieAddCounter == ADDNEWBADDIERATE:
            self.baddieAddCounter = 0
            baddie = Baddie()
            self.baddies.append(baddie)
        # Add spaceships at certain scores
        if self.score % 100 == 0:
            spaceship = Spaceship()
            self.baddies.append(spaceship)
    
    def update_star(self):
        self.star_counter += 1
        STAR_APPEAR_FRAMES = FPS_INITIAL * 10
        if self.star_counter >= STAR_APPEAR_FRAMES:
            self.starRect = pygame.Rect(
                WINDOWWIDTH,  # Start at the right edge
                random.randint(0, WINDOWHEIGHT - 30),
                30, 30
            )
            self.star_counter = 0
        if self.starRect:
            # Move the star to the left
            self.starRect.x += self.star_speed
            if self.starRect.right < 0:
                self.starRect = None  # Remove the star when it goes off-screen
        if self.starRect and self.player.rect.colliderect(self.starRect):
            self.star_active = True
            self.star_effect_counter = FPS_INITIAL * 10
            self.starRect = None
        if self.star_active:
            self.star_effect_counter -= 1
            if self.star_effect_counter <= 0:
                self.star_active = False
        self.FPS = get_game_speed(self.score)
        if self.star_active:
            self.FPS *= 3  # STAR_SPEED_MULTIPLIER
            immortality_music.play()
        else:
            immortality_music.stop()
    
    def draw(self):
        self.windowSurface.blit(backgroundImage, (self.background_x1, 0))
        self.windowSurface.blit(backgroundImage, (self.background_x2, 0))
        drawTextWhite('Score: %s' % (self.score), font, self.windowSurface, 10, 0)
        drawTextWhite('Top Score: %s' % (self.topScore), font, self.windowSurface, 10, 40)
        drawTextWhite(f'Number of baddies destroyed: {self.nb_baddies_destroyed}', font, self.windowSurface, 10, 80)
        draw_hearts(self.lives, font, self.windowSurface, 10, 120)
        self.windowSurface.blit(self.player.image, self.player.rect)
        for baddie in self.baddies:
            self.windowSurface.blit(baddie.surface, baddie.rect)
        if self.starRect:
            self.windowSurface.blit(starImage, self.starRect)
        for bullet in self.bullets:
            pygame.draw.rect(self.windowSurface, bullet['color'], bullet['rect'])
        if self.star_active:
            immortality_seconds = self.star_effect_counter // FPS_INITIAL
            drawTextWhite(f"Immortality: {immortality_seconds}", font, self.windowSurface, 10, 160)
        pygame.display.update()
    
    def check_collisions(self):
        # Bullet collisions
        for bullet in self.bullets[:]:
            for baddie in self.baddies[:]:
                if bullet['rect'].colliderect(baddie.rect):
                    baddie.health -= 1
                    self.bullets.remove(bullet)
                    if baddie.health <= 0:
                        self.baddies.remove(baddie)
                        self.nb_baddies_destroyed += 1
                        baddie_shoot_sound.play()
                        if self.nb_baddies_destroyed == 30:
                            self.lives += 1 #adds a life when you've killed 30 baddies
                    break
        # Player collisions
        if not self.star_active:
            for baddie in self.baddies[:]:
                if baddie.type == 'spaceship':
                    offset = (baddie.rect.x - self.player.rect.x, baddie.rect.y - self.player.rect.y)
                    if self.player.mask.overlap(baddie.mask, offset): # Pixel-perfect collision for spaceship
                        pygame.mixer.music.stop()
                        baddie_hit_sound.play()
                        self.lives -= baddie.damage
                        self.baddies.remove(baddie)
                        self.playing_explosion = True
                        self.explosion_x = baddie.rect.centerx
                        self.explosion_y = baddie.rect.centery
                        self.explosion_size = baddie.size*1.3  # Set explosion size to 1.3 spaceship size
                        while self.playing_explosion:
                            self.play_explosion()
                        if self.lives <= 0:
                            break
                        else:
                            self.player.update_image(4 - self.lives)
                            self.player.rect.topleft = (20, WINDOWHEIGHT / 2)
                            self.baddies.clear()
                            pygame.time.wait(1000)
                        pygame.mixer.music.play()
    
                else:  # Regular baddies (asteroids)
                    if self.player.rect.colliderect(baddie.rect):
                    # Handle regular baddie collision (same logic as before)
                        pygame.mixer.music.stop()
                        baddie_hit_sound.play()
                        self.lives -= baddie.damage
                        self.baddies.remove(baddie)
                        self.playing_explosion = True
                        self.explosion_x = baddie.rect.centerx
                        self.explosion_y = baddie.rect.centery
                        self.explosion_size = baddie.size*2  # Set explosion size to twice the baddie size
                        while self.playing_explosion:
                            self.play_explosion()
                        if self.lives <= 0:
                            break
                        else:
                            self.player.update_image(4 - self.lives)
                            self.player.rect.topleft = (20, WINDOWHEIGHT / 2)
                            self.baddies.clear()
                            pygame.time.wait(1000)
                        pygame.mixer.music.play()


    
    def play_explosion(self):
        for img in self.explosion_frames:
            frame_surface = pygame.transform.scale(img, (self.explosion_size, self.explosion_size))
            frame_rect = frame_surface.get_rect(center=(self.explosion_x, self.explosion_y))
            self.windowSurface.blit(frame_surface, frame_rect)
            pygame.display.update()
            self.mainClock.tick(self.FPS)
        self.playing_explosion = False
    
    def show_game_over_screen(self):
        pygame.mixer.music.stop()
        gameOverSound.play()

        # Load and display the explosion image
        explosion_image = pygame.image.load("explosion08.png")
        original_width, original_height = explosion_image.get_size()
        scaled_width, scaled_height = original_width * 2, original_height * 2
        explosion_image = pygame.transform.scale(explosion_image, (scaled_width, scaled_height))

        # Center the image on the screen
        image_rect = explosion_image.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))
        self.windowSurface.blit(explosion_image, image_rect.topleft)


        # Display "GAME OVER" and "Press a key to play again" text
        game_over_text = 'GAME OVER'
        retry_text = 'Press a key to play again'
        game_over_x = (WINDOWWIDTH - game_over_font.size(game_over_text)[0]) // 2
        retry_x = (WINDOWWIDTH - retry_font.size(retry_text)[0]) // 2  
        drawTextWhite(game_over_text, game_over_font, self.windowSurface, game_over_x, (WINDOWHEIGHT / 3))
        drawTextWhite(retry_text, retry_font, self.windowSurface, retry_x, (WINDOWHEIGHT / 3) + 100)

        pygame.display.update()
        pygame.time.wait(2000)
        
        # Check if the player has beaten the top score
        if self.score > self.topScore:
            self.topScore = self.score
            congrats_y = (WINDOWHEIGHT / 3) + 250
            for text in ["Congratulations,", "You've beaten your record!", f"Now your top score is {self.topScore}"]:
                drawText(text, small_font, self.windowSurface, (WINDOWWIDTH - small_font.size(text)[0]) / 2, congrats_y)
                congrats_y += 50
            pygame.display.update()

        self.FPS = FPS_INITIAL
        waitForPlayerToPressKey(self)
        gameOverSound.stop()

    
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
        self.images = images
        self.selected_character = selected_character
        self.image = self.images[1]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.topleft = (20, WINDOWHEIGHT / 2)
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False
        self.mask = pygame.mask.from_surface(self.image)  # Create mask
    
    def update_position(self):
        if self.moveUp and self.rect.top > 0:
            self.rect.move_ip(0, -1 * PLAYERMOVERATE)
        if self.moveDown and self.rect.bottom < WINDOWHEIGHT:
            self.rect.move_ip(0, PLAYERMOVERATE)
    
    def shoot_bullet(self, bullets):
        bullet_color = BULLET_COLOR.get(self.selected_character, (255, 0, 0))  # Get color based on selected character
        bullet = {
            'rect': pygame.Rect(self.rect.right, self.rect.centery - BULLET_SIZE[1] // 2, BULLET_SIZE[0], BULLET_SIZE[1]),
            'speed': BULLET_SPEED,
            'color': bullet_color
        }
        bullets.append(bullet)
    
    def update_image(self, index):
        self.image = self.images[index]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.mask = pygame.mask.from_surface(self.image)  # Update mask
    
    def reset(self):
        self.image = self.images[1]
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect.topleft = (20, WINDOWHEIGHT / 2)
        self.moveLeft = self.moveRight = self.moveUp = self.moveDown = False
        self.mask = pygame.mask.from_surface(self.image) # Update mask

class Baddie:
    def __init__(self):
        self.size = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
        prob = random.randint(1, 100)
        if prob <= 50:
            self.type = 'asteroid'
            self.image = baddieImage1
            self.health = 1
            self.damage = 1
        elif prob <= 80:
            self.type = 'strong_asteroid'
            self.image = baddieImage2
            self.health = 2
            self.damage = 1
        else:
            self.type = 'super_strong_asteroid'
            self.image = baddieImage3
            self.health = 3
            self.damage = 1
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = self.surface.get_rect()
        self.rect.x = WINDOWWIDTH + self.size
        self.rect.y = random.randint(0, WINDOWHEIGHT - self.size)
        self.speed = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
    
    def update_position(self):
        self.rect.move_ip(self.speed, 0)

class Spaceship(Baddie):
    def __init__(self):
        super().__init__()
        self.size = random.randint(SPACEMINSIZE, SPACEMAXSIZE)
        self.type = 'spaceship'
        self.image = spaceshipImage
        self.health = 5
        self.damage = 2
        self.surface = pygame.transform.scale(self.image, (self.size, self.size))
        self.mask = pygame.mask.from_surface(self.surface)  # Create mask after scaling
        self.rect = self.surface.get_rect()  # Update rect *after* scaling and creating mask
        self.reset_position()  # Reset the position based on the new size
    
    def reset_position(self): # Define reset_position within Spaceship
        self.rect.x = WINDOWWIDTH + self.size
        self.rect.y = random.randint(0, WINDOWHEIGHT - self.size)
        self.speed = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
    

# Utility functions
def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(game):
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                game.terminate()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    display_rules()
                    if game.is_playing:  # Restart the background music only if the game is running
                        pygame.mixer.music.play()
                if event.key == K_ESCAPE:
                    game.terminate()
                return

def drawText(text, font, surface, x, y):
    textobj = font.render(text, True, BLACK)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def drawTextWhite(text, font, surface, x, y):
    textobj = font.render(text, True, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_hearts(lives, font, surface, x, y):
    text = "Lives: "
    textobj = font.render(text, True, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    heart_spacing = 30
    heart_y_offset = 18
    for i in range(lives):
        surface.blit(heartImage, (x + textrect.width + (i * heart_spacing), y + heart_y_offset))

def display_rules():
    pygame.mixer.music.stop()  # Stop the background music
    image = pygame.image.load("Rules_of_game.png")
    image = pygame.transform.scale(image, (WINDOWWIDTH, WINDOWHEIGHT))
    screen_copy = windowSurface.copy()
    screen_copy.blit(image, (0, 0))
    windowSurface.blit(screen_copy, (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                return

def get_game_speed(score):
    if score >= 2500:
        return FPS_INITIAL * 3
    elif score >= 1000:
        return FPS_INITIAL * 2
    elif score >= 500:
        return FPS_INITIAL * 1.5
    else:
        return FPS_INITIAL

# Start the game
if __name__ == '__main__':
    game = Game()
    game.run()