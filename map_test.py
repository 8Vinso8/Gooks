import pygame
map = [[0] * 1920] * 1080
for i in range(900, 1080):
    map[i] = [1] * 1920
pygame.init()
RESOLUTION = 1920, 1080
window: pygame.Surface = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
pygame.display.set_caption('Gooks')
is_working = True
pl_pos = (900, 500)
pl_size = 100


def place_to_update():
    pass


def collision(pos):
    for i in range(pos[0], pos[0] + pl_size):
        for j in range(pos[1], pos[1] + pl_size):
            if map[j][i]:
                return True
    return False


for i in range(1920):
    for j in range(1080):
        window.set_at((i, j), (0, 255, 0) if map[j][i] else (0, 0, 0))
while is_working:
    last_pos = pl_pos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_working = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                if fullscreen:
                    window: pygame.Surface = pygame.display.set_mode(RESOLUTION)
                    fullscreen = False
                else:
                    window: pygame.Surface = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
                    fullscreen = True
            if event.key == pygame.K_ESCAPE:
                is_working = False
    if not collision(pl_pos):
        pl_pos = pl_pos[0], pl_pos[1] + 1
    for i in range(last_pos[0], last_pos[0] + pl_size):
        for j in range(last_pos[1], last_pos[1] + pl_size):
            window.set_at((i, j), (0, 255, 0) if map[j][i] else (0, 0, 0))
    pygame.draw.rect(window, (255, 0, 0), pygame.Rect(pl_pos, (pl_size, pl_size)))
    pygame.display.update()

