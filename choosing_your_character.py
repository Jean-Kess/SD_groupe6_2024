import pygame

def drawText(text, font, surface, x, y, center=False):
    textobj = font.render(text, True, (0, 0, 0))  # Using black for text
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Define the function to choose your character
def choose_character(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT):
    selected_character = 0
    player_name = ""
    entering_name = True
    game_started = False
    character_rects = []
      

    while not game_started:
        windowSurface.fill(WHITE)
        drawText("What's your name?", font, windowSurface, WINDOWWIDTH // 2, 50, center=True)
        drawText(player_name, font, windowSurface, WINDOWWIDTH // 2, 100, center=True)

        if not entering_name:
            drawText("Choose your character", large_font, windowSurface, WINDOWWIDTH // 2, 200, center=True)
            character_rects = []
            for i, img in enumerate(character_images):
                x = WINDOWWIDTH // (len(character_images) + 1) * (i + 1)
                y = WINDOWHEIGHT // 2
                img_rect = img.get_rect(center=(x, y))
                character_rects.append(img_rect)
                windowSurface.blit(img, (x - img.get_width() // 2, y - img.get_height() // 2))
                pygame.draw.rect(windowSurface, (255, 0, 0), img_rect, 1)
                if i == selected_character:
                    pygame.draw.rect(windowSurface, BLACK, img_rect, 3)

            drawText("Press Enter to confirm and play", font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                pygame.mouse.set_visible(True)
            if event.type == pygame.MOUSEBUTTONDOWN:  # Détection d'un clic de souris
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

    return character_images[selected_character], player_name


# Define the function to display a countdown timer
def display_the_countdown(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT):
    for count in range(3, 0, -1):
        windowSurface.fill(WHITE)
        drawText(f"{player_name}, Ready?", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3, center=True)
        windowSurface.blit(character_image, (WINDOWWIDTH // 2 - character_image.get_width() // 2, WINDOWHEIGHT // 2 - character_image.get_height() // 2))
        drawText(f"Start in {count}", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)
        pygame.display.update()
        pygame.time.wait(1000)

    windowSurface.fill(WHITE)
    drawText("GO !", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
    pygame.display.update()
    pygame.time.wait(1000)
