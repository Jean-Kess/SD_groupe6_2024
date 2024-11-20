import pygame
import sys
def terminate():
    pygame.quit()
    sys.exit()

def drawText(text, font, surface, x, y, center=False):
    textobj = font.render(text, True, (0, 0, 0))  # Using black for text
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def choose_character(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT):
    selected_character = 0
    player_name = ""
    entering_name = True
    game_started = False
    character_rects = []

    while not game_started:
        windowSurface.fill(WHITE)
        drawText("What's your name?", pygame.font.Font('gameFont.ttf', 55), windowSurface, WINDOWWIDTH // 2, 50, center=True)
        drawText(player_name, font, windowSurface, WINDOWWIDTH // 2, 130, center=True)

        if not entering_name:
            drawText("Choose your character", pygame.font.Font('gameFont.ttf', 45), windowSurface, WINDOWWIDTH // 2, 200, center=True)
            character_rects = []
            for i, img in enumerate(character_images):
                # Display each character's first image (damage0) for the selection screen
                x = WINDOWWIDTH // (len(character_images) + 1) * (i + 1)
                y = WINDOWHEIGHT // 2
                img_rect = img[0].get_rect(center=(x, y))  # Start with the first damage state (3 lives)
                character_rects.append(img_rect)
                windowSurface.blit(img[0], (x - img[0].get_width() // 2, y - img[0].get_height() // 2))
                pygame.draw.rect(windowSurface, (255, 0, 0), img_rect, 1)
                if i == selected_character:
                    pygame.draw.rect(windowSurface, BLACK, img_rect, 3)

            drawText("Press Enter to play", pygame.font.Font('gameFont.ttf', 40), windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)

            if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse click detection
                mouse_x, mouse_y = pygame.mouse.get_pos()

                for i, rect in enumerate(character_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_character = i
                        game_started = True

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
                        game_started = True
                        pygame.mouse.set_visible(False)

        pygame.display.update()

    # Return the selected character's images and the player name
    selected_character_images = character_images[selected_character]  # This gets the full image set for the selected character
    return selected_character_images, player_name


# Define the function to display a countdown timer
def display_the_countdown(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT):
    for count in range(3, 0, -1):
        windowSurface.fill(WHITE)
        drawText(f"{player_name} are you ready?", pygame.font.Font('gameFont.ttf', 35), windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3, center=True)
        windowSurface.blit(character_image, (WINDOWWIDTH // 2 - character_image.get_width() // 2, WINDOWHEIGHT // 2 - character_image.get_height() // 2))
        drawText(f"Start in {count}", pygame.font.Font('gameFont.ttf', 40), windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)
        pygame.display.update()
        pygame.time.wait(1000)

    windowSurface.fill(WHITE)
    drawText("GO!", pygame.font.Font('gameFont.ttf', 85), windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
    pygame.display.update()
    pygame.time.wait(1000)
