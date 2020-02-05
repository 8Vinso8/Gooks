from functions import *
from locals import *


def start_screen(window, clock):
    intro_text = "Gooks"
    fon = pygame.transform.scale(load_image('vietnam_war.png'), (1920, 1080))
    window.blit(fon, (0, 0))
    title_font = pygame.font.Font(None, 200)
    text = title_font.render(intro_text, True, pygame.Color('red'))
    window.blit(text, [250, 250])
    start_button = pygame.Rect([500, 500, 200, 100])
    exit_button = pygame.Rect([800, 500, 200, 100])
    pygame.draw.rect(window, pygame.Color('white'), exit_button, 2)
    pygame.draw.rect(window, pygame.Color('white'), start_button, 2)

    button_font = pygame.font.Font(None, 50)
    start_text = button_font.render('Начать!', True, pygame.Color('red'))
    exit_text = button_font.render('Выйти', True, pygame.Color('red'))
    window.blit(start_text, [510, 510])
    window.blit(exit_text, [810, 510])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return
                elif exit_button.collidepoint(event.pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)

