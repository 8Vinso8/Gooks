import pygame

start_ticks = pygame.time.get_ticks()  # starter tick
while True:  # mainloop
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000  # calculate how many seconds
    if seconds > 10:  # if more than 10 seconds close the game
        break
    print(seconds)  # print how many seconds
