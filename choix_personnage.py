import pygame

def drawText(text, font, surface, x, y, center=False):
    textobj = font.render(text, True, (0, 0, 0))  # Utilisation de noir pour le texte
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def choisir_personnage(windowSurface, font, large_font, character_images, WHITE, BLACK, WINDOWWIDTH, WINDOWHEIGHT):
    selected_character = 0
    player_name = ""
    entering_name = True
    game_started = False
      

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
                        game_started = True

        pygame.display.update()

    return character_images[selected_character], player_name


def afficher_compte_a_rebours(windowSurface, large_font, character_image, player_name, WHITE, WINDOWWIDTH, WINDOWHEIGHT):
    for count in range(3, 0, -1):
        windowSurface.fill(WHITE)
        drawText(f"{player_name}, prêt(e) ?", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 3, center=True)
        windowSurface.blit(character_image, (WINDOWWIDTH // 2 - character_image.get_width() // 2, WINDOWHEIGHT // 2 - character_image.get_height() // 2))
        drawText(f"Début dans {count}", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT - 100, center=True)
        pygame.display.update()
        pygame.time.wait(1000)

    windowSurface.fill(WHITE)
    drawText("GO !", large_font, windowSurface, WINDOWWIDTH // 2, WINDOWHEIGHT // 2, center=True)
    pygame.display.update()
    pygame.time.wait(1000)
