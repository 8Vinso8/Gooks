import pygame
import math
from pygame.constants import *
from locals import *
import random
import itertools
import os
import sys
from PIL import Image

pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()
soundtrack = pygame.mixer.Sound(os.path.join('data', soundtrack_way))
death_sound = pygame.mixer.Sound(os.path.join('data', death_sound_way))
shot_sound = pygame.mixer.Sound(os.path.join('data', shot_sound_way))
explode_sound = pygame.mixer.Sound(os.path.join('data', explode_sound_way))
victory_sound = pygame.mixer.Sound(os.path.join('data', victory_sound_way))


def draw_interface(window, wind_num, fps, cur_team_name, cur_gook_name):
    font = pygame.font.Font(None, 50)
    wind_text = font.render(str(wind_num), True, pygame.Color('white'))
    fps_text = font.render(str(fps), True, pygame.Color('white'))
    cur_team_text = font.render(str(cur_team_name), True, pygame.Color('white'))
    cur_gook_text = font.render(str(cur_gook_name), True, pygame.Color('white'))
    window.blit(wind_text, [10, 10])
    window.blit(fps_text, [910, 10])
    window.blit(cur_team_text, [1700, 10])
    window.blit(cur_gook_text, [1700, 40])
    

def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def get_next_team():
    for team_now in teams:
        yield team_now


team_gen = get_next_team()
gook_gen = itertools.cycle(range(TEAM_LEN))
n_gook = next(gook_gen)


def next_turn():
    global cur_team, cur_gook, team_gen, n_gook, wind
    wind = random.randint(-3, 3)
    print(wind)
    try:
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)
    except StopIteration:
        n_gook = next(gook_gen)
        team_gen = get_next_team()
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)


class Map:
    def __init__(self, map_file, color_zero, color_one):
        self.bitmap = list()
        self.color_zero = color_zero
        self.color_one = color_one
        self.load_map_file(map_file)
        try:
            im = Image.open("data/ground.jpg")
        except FileNotFoundError:
            im = Image.open('data/ground.png')
        self.pixels = im.load()
        try:
            im1 = Image.open('data/fon.jpg')
        except FileNotFoundError:
            im1 = Image.open('data/fon.png')
        self.pixels1 = im1.load()

    def load_map_file(self, map_file):
        fullname = os.path.join('data', map_file)
        with open(fullname, 'r') as f:
            for line in f.readlines():
                line_list = list(map(int, list(line.strip())))
                self.bitmap.append(line_list)

    def draw(self, window):
        for i in range(1920):
            for j in range(1080):
                window.set_at((i, j), self.pixels[i, j] if self.bitmap[j][i] else self.pixels1[i, j])

    def draw_part(self, window, start, size):
        start = tuple(map(int, start))
        for i in range(start[0], start[0] + size[0] + 30):
            for j in range(start[1] - 20, start[1] + size[1]):
                try:
                    window.set_at((i, j), self.pixels[i, j] if self.bitmap[j][i] else self.pixels1[i, j])
                except IndexError:
                    continue


    def explode(self, window, point, size):
        point = tuple(map(round, point))
        for i in range(point[0] - size, point[0] + size):
            for j in range(point[1] - size, point[1] + size):
                try:
                    self.bitmap[j][i] = 0
                    window.set_at((i, j), self.pixels[i, j] if self.bitmap[j][i] else self.pixels1[i, j])
                except IndexError:
                    continue
        explode_sound.play()
        explosions.append(
            Explosion(
                window,
                (point[0] - size, point[1] - size),
                pygame.transform.scale(load_image(EXPLOSION_IMG, -1), (size * 2, size * 2)),
                (size * 2, size * 2)
            )
        )

    def get_bitmap(self):
        return self.bitmap


class Thing:
    def __init__(self, bitmap, pos, image, size):
        self.bitmap = bitmap
        self.position = pos
        self.size = size
        self.image_name = image
        self.image = load_image(image, colorkey=-1)
        self.x_speed = 0
        self.y_speed = 0

    def get_x(self):
        return self.position[0]

    def get_y(self):
        return self.position[1]

    def get_size(self):
        return self.size

    def get_pos(self):
        return self.position

    def change_speed(self, change):  # change - кортеж изменения скорости (x, y)
        self.x_speed += change[0]
        self.y_speed += change[1]

    def change_image(self, image):
        self.image = load_image(image, colorkey=-1)

    def change_size(self, size):
        self.size = size

    def get_rect(self):
        return pygame.Rect(self.get_x(), self.get_y(), self.get_size()[0], self.get_size()[1])

    def check_state(self):
        if self.get_x() >= RESOLUTION[0] or \
                self.get_y() >= RESOLUTION[1] or \
                self.get_x() + self.get_size()[0] < 0 or \
                self.get_y() + self.get_size()[1] < 0:
            return 'delete'

    def draw(self, window):
        self.rect = self.image.get_rect(
            bottomright=(self.get_pos()[0] + self.get_size()[0],
                         self.get_pos()[1] + self.get_size()[1])
        )
        window.blit(self.image, self.rect)

    def move(self, x, y):
        self.position = (self.get_x() + x, self.get_y() + y)

    def passive_move(self):
        changed = False
        last_pos = self.position
        self.change_speed((0, G))
        if self.x_speed > 0:
            collision_check = self.collision('right', self.x_speed)
            if collision_check:
                self.x_speed = collision_check - self.get_x() - self.size[0]
        elif self.x_speed < 0:
            collision_check = self.collision('left', self.x_speed)
            if collision_check:
                self.x_speed = collision_check - self.get_x()
        if self.y_speed > 0:
            collision_check = self.collision('down', self.y_speed)
            if collision_check:
                self.y_speed = collision_check - self.get_y() - self.size[1]
        elif self.y_speed < 0:
            collision_check = self.collision('up', self.y_speed)
            if collision_check:
                self.y_speed = self.get_y() - collision_check - 1
        if self.x_speed or self.y_speed:
            self.move(self.x_speed, self.y_speed)
            changed = True
        if self.x_speed > 0:
            self.x_speed -= self.speed_decrease
            if self.x_speed < 0:
                self.x_speed = 0
        if self.x_speed < 0:
            self.x_speed += self.speed_decrease
            if self.x_speed > 0:
                self.x_speed = 0
        if changed:
            return last_pos

    def collision(self, direction, speed=1, kx=0, ky=0):
        if direction == 'left':
            for i in range(round(self.get_pos()[0]) - kx, round(self.get_pos()[0] - speed) - kx):
                for j in range(round(self.get_pos()[1]) - ky, round(self.get_pos()[1] + self.get_size()[1]) - ky):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return i
                    except IndexError:
                        continue
        if direction == 'right':
            for i in range(round(self.get_pos()[0] + self.get_size()[0]) + kx,
                           round(self.get_pos()[0] + self.get_size()[0] + speed) + kx):
                for j in range(round(self.get_pos()[1]) - ky, round(self.get_pos()[1] + self.get_size()[1]) - ky):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return i
                    except IndexError:
                        continue
        if direction == 'up':
            for j in range(round(self.get_pos()[1]) - 1, round(self.get_pos()[1] - speed) - 1):
                for i in range(round(self.get_pos()[0]), round(self.get_pos()[0] + self.get_size()[0])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return j
                    except IndexError:
                        continue
        if direction == 'down':
            for j in range(round(self.get_pos()[1] + self.get_size()[1]),
                           round(self.get_pos()[1] + self.get_size()[1] + speed)):
                for i in range(round(self.get_pos()[0]), round(self.get_pos()[0] + self.get_size()[0])):
                    try:
                        if self.bitmap.get_bitmap()[j][i]:
                            return j
                    except IndexError:
                        continue


class Bullet(Thing):
    def __init__(self, bitmap, pos, weapon, angle, power):
        super().__init__(bitmap, pos, PROJECTILES[weapon][0], PROJECTILES[weapon][1])
        self.g = PROJECTILES[weapon][2] * G
        speed = PROJECTILES[weapon][3] * power
        self.x_speed = speed * math.cos(angle) + wind
        self.y_speed = speed * math.sin(angle)
        self.explosion = PROJECTILES[weapon][4]
        self.dmg = PROJECTILES[weapon][5]

    def move(self):
        last_pos = self.get_pos()
        super().move(round(self.x_speed), round(self.y_speed))
        self.y_speed += self.g
        return last_pos

    def get_dmg(self):
        return self.dmg

    def check_state(self):
        if super().check_state():
            return super().check_state()
        if self.collision('left', self.x_speed) or self.collision('right', self.x_speed) \
                or self.collision('down', self.y_speed) or self.collision('up', self.y_speed):
            return 'BOOM'
        # Проверка столкновения

    def boom(self, window):
        self.bitmap.explode(
            window,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.explosion
        )
        return pygame.Rect(
            (self.get_x() + self.get_size()[0] // 2 - self.explosion,
             self.get_y() + self.get_size()[1] // 2 - self.explosion),
            (2 * self.explosion, 2 * self.explosion)
        )


class Gook(Thing):
    def __init__(self, bitmap, position, color, name, size, start_image, weapon='cannon'):
        super().__init__(bitmap, position, start_image, size)
        self.name = name
        self.color = color
        self.weapon = weapon
        self.direction = 'right'
        self.x_speed = 0  # Только для перемещения без участия игрока!
        self.y_speed = 0
        self.speed_decrease = 0.5  # Замедление
        self.hp = 100
        self.angle = 0

    def __str__(self):
        return self.name

    def draw(self, window):
        super().draw(window)
        font = pygame.font.Font(None, 30)
        hp_text = font.render(str(self.get_hp()), True, pygame.Color('green'))
        name_text = font.render(self.name, True, pygame.Color(self.color))
        window.blit(hp_text, [self.position[0], self.position[1] - 10])
        window.blit(name_text, [self.position[0], self.position[1] - 20])

    def get_weapon(self):
        return self.weapon

    def get_hp(self):
        return self.hp

    def key_move(self, move):
        last_direction = self.direction
        last_pos = self.get_pos()
        if self.collision('down'):
            if move == 'D':
                self.x_speed = MOVEMENT_SPEED
                self.direction = 'right'
                collision_check = self.collision('right', self.x_speed)
                if collision_check:
                    self.x_speed = collision_check - self.get_x() - self.size[0]
                    if self.x_speed == 0:
                        for i in range(1, 20):
                            collision_check = self.collision('right', kx=1, ky=i)
                            if not collision_check:
                                self.move(1, -i)
                                break
            else:
                self.x_speed = -MOVEMENT_SPEED
                self.direction = 'left'
                collision_check = self.collision('left', self.x_speed)
                if collision_check:
                    self.x_speed = collision_check - self.get_x()
                    if self.x_speed == 0:
                        for i in range(1, 20):
                            collision_check = self.collision('left', kx=1, ky=i, speed=-1)
                            if not collision_check:
                                self.move(-1, -i)
                                break

        self.move(self.x_speed, 0)

        self.x_speed = 0

        if self.direction != last_direction:
            self.image = pygame.transform.flip(self.image, True, False)
        return last_pos

    def jump(self):
        last_pos = self.get_pos()
        if self.collision('down'):
            if self.direction == 'left':
                self.change_speed((10, -20))
            else:
                self.change_speed((-10, -20))
        return last_pos

    def change_get_angle(self, final_cords):
        fin_x, fin_y = final_cords
        st_x, st_y = self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2
        self.angle = math.atan2((fin_y - st_y), (fin_x - st_x))
        return self.angle

    def shoot(self, final_cords, power):
        self.change_get_angle(final_cords)
        return Bullet(
            self.bitmap,
            (self.get_x() + self.get_size()[0] // 2, self.get_y() + self.get_size()[1] // 2),
            self.get_weapon(),
            self.angle,
            power
        )
        playing_sounds.append(shot_sound)


    def make_damage(self, dmg):
        self.hp -= dmg

    def check_state(self):
        if super().check_state() or not self.check_is_alive():
            return 'del'

    def check_is_alive(self):
        return self.get_hp() > 0

    def make_graveyard(self):
        return Graveyard(self.bitmap, self.get_pos(), GRAVEYARD_IMG, GRAVEYARD_RES)


class Graveyard(Thing):
    pass


class Explosion(Thing):
    def __init__(self, bitmap, pos, image, size):
        super().__init__(bitmap, pos, EXPLOSION_IMG, size)
        self.image = image
        self.life_timer = 0

    def increase_life_timer(self):
        self.life_timer += 1

    def check_state(self):
        if self.life_timer >= 10:
            return 'del'


class Team:
    def __init__(self, bitmap, team_name, team_color, positions, names):
        self.gooks = list()
        for i in range(TEAM_LEN):
            self.gooks.append(Gook(bitmap, positions[i], team_color, names[i], GOOK_RES, GOOK_IMG))
        self.team_name = team_name

    def __str__(self):
        return self.team_name

    def get_gook(self, n):
        return self.gooks[n % len(self.gooks)] if self.gooks else None

    def get_gooks(self):
        return self.gooks

    def remove_gook(self, gook):
        self.gooks.remove(gook)

    def check_state(self):
        if not self.get_gooks():
            return False
        else:
            return True


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
    victory_sound.play()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):

                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


def main():
    is_working = True
    fullscreen = True
    is_shot = False
    is_mouse_down = False
    is_jumped = False

    window: pygame.Surface = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption('Gooks')

    clock = pygame.time.Clock()

    start_screen(window, clock)

    map1 = Map('map.txt', (50, 150, 255), pygame.Color('black'))
    map1.draw(window)

    for team in TEAMS:
        teams.append(Team(map1, *team))

    next_turn()
    turn_start_time = pygame.time.get_ticks()

    for team in teams:
        for gook in team.get_gooks():
            gook.draw(window)
    soundtrack.play(-1)
    while is_working:
        timer_fps = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == QUIT:
                is_working = False
            if event.type == KEYDOWN:
                if event.key == K_F1:
                    if fullscreen:
                        window: pygame.Surface = pygame.display.set_mode(RESOLUTION)
                        fullscreen = False
                    else:
                        window: pygame.Surface = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
                        fullscreen = True
                if event.key == K_ESCAPE:
                    is_working = False
                if event.key == K_SPACE:
                    is_jumped = True
                    jump_last_pos = cur_gook.jump()
                    places_for_filling.append(((jump_last_pos[0], jump_last_pos[1] - 30), cur_gook.get_size()))

            if not bullets and not is_mouse_down and event.type == MOUSEBUTTONDOWN:
                start_ticks = pygame.time.get_ticks()
                is_mouse_down = True
                cur_gook.change_image(SHOOT_FORWARD_IMG)
            if is_mouse_down and event.type == MOUSEMOTION:
                angle = cur_gook.change_get_angle(event.pos)
                if angle > 1:
                    cur_gook.change_image(SHOOT_FORWARD_IMG)
                    cur_gook.change_size(SHOOT_FORWARD_RES)
                else:
                    cur_gook.change_image(SHOOT_UP_IMG)
                    cur_gook.change_size(SHOOT_UP_RES)
            if is_mouse_down and event.type == MOUSEBUTTONUP:
                time = pygame.time.get_ticks() - start_ticks
                if time > 2700:
                    time = 2700
                power = time / 3000 + 0.1
                bullets.append(cur_gook.shoot(event.pos, power))
                is_mouse_down = False
                cur_gook.change_image(GOOK_IMG)
                cur_gook.change_size(GOOK_RES)

        if not is_jumped:
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                key_move_last_pos = cur_gook.key_move('A')
                places_for_filling.append((key_move_last_pos, cur_gook.get_size()))
                moved_gooks.append(cur_gook)
            if keys[K_d]:
                key_move_last_pos = cur_gook.key_move('D')
                places_for_filling.append((key_move_last_pos, cur_gook.get_size()))
                moved_gooks.append(cur_gook)
        if cur_gook.collision('down'):
            is_jumped = False

        for graveyard in graveyards:
            graveyard_last_pos = graveyard.passive_move()
            if graveyard_last_pos:
                places_for_filling.append((graveyard_last_pos, graveyard.get_size()))
            if graveyard.check_state():
                graveyards.remove(graveyard)
                places_for_filling.append((graveyard_last_pos, graveyard.get_size()))

        # Отрисовка и проверка состояния пуль
        for bullet in bullets:
            bullet_last_pos = bullet.move()
            state = bullet.check_state()
            if state == 'BOOM':
                boom_rect = bullet.boom(window)
                for team in teams:
                    for gook in team.get_gooks():
                        if gook.get_rect().colliderect(boom_rect):
                            gook.make_damage(bullet.get_dmg())
                playing_sounds.append(explode_sound)

            if state:
                bullets.remove(bullet)
                next_turn()
                places_for_filling.append(((0, 10), (30, 50)))
                places_for_filling.append(((1700, 10), (175, 100)))
                turn_start_time = pygame.time.get_ticks()
            places_for_filling.append((bullet_last_pos, bullet.get_size()))
        # Проверка непроизвольного движения гуков
        for team in teams:
            for gook in team.get_gooks():
                last_pos_or_none = gook.passive_move()
                if last_pos_or_none:
                    places_for_filling.append((last_pos_or_none, gook.get_size()))
                    moved_gooks.append(gook)
                if gook.check_state():
                    if gook == cur_gook:
                        next_turn()
                    places_for_filling.append((gook.get_pos(), gook.get_size()))
                    team.remove_gook(gook)
                    playing_sounds.append(death_sound)
            if not team.check_state():
                teams.remove(team)
                if len(teams) == 1:

                    win_screen(window, clock, teams[0])
        timer = (pygame.time.get_ticks() - turn_start_time) // 1000
        places_for_filling.append(((910, 10), (30, 50)))

        for explosion in explosions:
            if explosion.check_state():
                explosions.remove(explosion)
                places_for_filling.append((explosion.get_pos(), explosion.get_size()))

        for place, size in places_for_filling:
            map1.draw_part(window, place, size)
        places_for_filling.clear()

        for graveyard in graveyards:
            graveyard.draw(window)
        for bullet in bullets:
            bullet.draw(window)
        for team in teams:
            for gook in team.get_gooks():
                gook.draw(window)
        for explosion in explosions:
            explosion.draw(window)
            explosion.increase_life_timer()
        if victory_sound in playing_sounds:
            victory_sound.play()
        elif death_sound in playing_sounds:
            death_sound.play()
        elif explode_sound in playing_sounds:
            explode_sound.play()
        elif shot_sound in playing_sounds:
            shot_sound.play()
        playing_sounds.clear()
        moved_gooks.clear()
        time_passed = pygame.time.get_ticks() - timer_fps
        fps = 1000 // time_passed
        if time_passed < 1000 // FPS:
            pygame.time.wait(1000 // FPS - time_passed)
        draw_interface(window, wind, fps, cur_team, cur_gook)
        pygame.display.flip()


if __name__ == '__main__':
    main()
