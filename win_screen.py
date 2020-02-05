from functions import *
from locals import *


def win_screen(window, clock, winner):
    intro_text = f"Победили {winner}"
    fon = pygame.transform.scale(load_image('win_screen.png'), (1920, 1080))
    window.blit(fon, (0, 0))
    title_font = pygame.font.Font(None, 200)
    text = title_font.render(intro_text, True, pygame.Color('red'))
    window.blit(text, [250, 250])
    exit_button = pygame.Rect([800, 500, 200, 100])
    pygame.draw.rect(window, pygame.Color('red'), exit_button, 2)
    button_font = pygame.font.Font(None, 50)
    exit_text = button_font.render('Выйти', True, pygame.Color('red'))
    window.blit(exit_text, [810, 510])
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)

