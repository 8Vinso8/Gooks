from pygame.constants import *

from start_screen import start_screen
from win_screen import win_screen
from bitmap import Bitmap
from team import Team
from functions import *
from locals import *
from interface import *
from box import Medicine
from particle import *
import itertools
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
pygame.init()
sounds = {
    'soundtrack': pygame.mixer.Sound(os.path.join('data', soundtrack_way)),
    'death_sound': pygame.mixer.Sound(os.path.join('data', death_sound_way)),
    'shot_sound': pygame.mixer.Sound(os.path.join('data', shot_sound_way)),
    'explode_sound': pygame.mixer.Sound(os.path.join('data', explode_sound_way)),
    'victory_sound': pygame.mixer.Sound(os.path.join('data', victory_sound_way)),
    'turn_sounds': (pygame.mixer.Sound(os.path.join('data', gook_sounds[0])),
                    pygame.mixer.Sound(os.path.join('data', gook_sounds[1])),
                    pygame.mixer.Sound(os.path.join('data', gook_sounds[2])))
}


for i in sounds['turn_sounds']:
    i.set_volume(2)


def get_next_team():
    for team_now in teams:
        yield team_now


team_gen = get_next_team()
gook_gen = itertools.cycle(range(TEAM_LEN))
n_gook = next(gook_gen)


def next_turn():
    global cur_team, cur_gook, team_gen, n_gook, wind
    wind = random.randint(-3, 3)
    try:
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)
    except StopIteration:
        n_gook = next(gook_gen)
        team_gen = get_next_team()
        cur_team = next(team_gen)
        cur_gook = cur_team.get_gook(n_gook)


def main():
    is_working = True
    fullscreen = True
    is_mouse_down = False
    is_jumped = False
    were_walking = False

    window: pygame.Surface = pygame.display.set_mode(RESOLUTION, FULLSCREEN)
    pygame.display.set_caption('Gooks')

    leave = load_image("leave.png", colorkey=(255, 255, 255))
    leaves_images = [leave, pygame.transform.flip(leave, 1, 0)]
    all_sprites = pygame.sprite.Group()
    screen_rect = (0, 0, 1920, 1080)

    wind_indicator = WindIndicator((0, 0))

    clock = pygame.time.Clock()

    start_screen(window, clock)

    map1 = Bitmap('map.txt', (50, 150, 255), pygame.Color('black'))
    map1.draw(window)

    for team1 in TEAMS:
        teams.append(Team(map1, *team1))

    next_turn()

    for team in teams:
        for gook in team.get_gooks():
            gook.draw(window)

    boxes = list(Medicine(map1, pos, HEALTH_BOX_IMG, HEALTH_BOX_RES)
                 for pos in HEALTH_BOX_POSITIONS)
    for box in boxes:
        box.draw(window)

    sounds['soundtrack'].play(-1)
    while is_working:
        cur_gook.is_weapon = True
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
                    jump_last_pos = cur_gook.jump1()
                    places_for_filling.append(cur_gook.get_place_for_filling(jump_last_pos, cur_gook.get_size()))

                if event.key == K_RETURN:
                    is_jumped = True
                    jump_last_pos = cur_gook.jump2()
                    places_for_filling.append(cur_gook.get_place_for_filling(jump_last_pos, cur_gook.get_size()))

            if not bullets and not is_mouse_down and event.type == MOUSEBUTTONDOWN and event.button == 1:
                cur_gook.change_holding_status()
                start_ticks = pygame.time.get_ticks()
                is_mouse_down = True
                cur_gook.change_image_state(SHOOT_FORWARD_IMG)
            if is_mouse_down and event.type == MOUSEMOTION:
                angle = cur_gook.change_get_angle(event.pos)
                if -1.67 < angle < 1.67:
                    cur_gook.change_direction('right')
                else:
                    cur_gook.change_direction('left')
                if 0 < angle < 3.14:
                    cur_gook.change_image_state(SHOOT_FORWARD_IMG)
                else:
                    cur_gook.change_image_state(SHOOT_UP_IMG)
                cur_gook.draw(window)

            if is_mouse_down and event.type == MOUSEBUTTONUP and event.button == 1:
                cur_gook.change_holding_status()
                time = pygame.time.get_ticks() - start_ticks
                if time > 1800:
                    time = 1800
                power = time / 2000 + 0.1
                bullets.append(cur_gook.shoot(event.pos, power))
                is_mouse_down = False
                cur_gook.change_image_state(GOOK_IMG)
                cur_gook.change_size(GOOK_RES)
                places_for_filling.append(cur_gook.get_place_for_filling(cur_gook.get_pos(), cur_gook.get_size()))
                playing_sounds.append(sounds['shot_sound'])

            if not is_mouse_down and event.type == MOUSEBUTTONUP and event.button == 3:
                places_for_filling.append((cur_gook.get_weapon().get_pos(), cur_gook.get_weapon().get_size()))
                cur_gook.change_weapon()

        if not bullets and not is_mouse_down and not is_jumped:
            keys = pygame.key.get_pressed()
            if keys[K_a]:
                key_move_last_pos = cur_gook.key_move('A')
                places_for_filling.append((cur_gook.get_place_for_filling(key_move_last_pos, cur_gook.get_size())))
                were_walking = True
            if keys[K_d]:
                key_move_last_pos = cur_gook.key_move('D')
                places_for_filling.append((cur_gook.get_place_for_filling(key_move_last_pos, cur_gook.get_size())))
                were_walking = True
        if cur_gook.collision('down'):
            is_jumped = False

        for box in boxes:
            box_last_pos = box.passive_move()
            if box_last_pos:
                places_for_filling.append((box.get_pos(), box.get_size()))
            if box.check_state():
                boxes.remove(box)
                places_for_filling.append((box.get_pos(), box.get_size()))

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
            state = bullet.check_state(teams)
            bullet.change_wind(wind)
            if state == 'BOOM':
                boom_rect = bullet.boom(window)
                for team in teams:
                    for gook in team.get_gooks():
                        if gook.get_rect().colliderect(boom_rect):
                            gook.make_damage(bullet.get_dmg())
                playing_sounds.append(sounds['explode_sound'])

            if state:
                bullets.remove(bullet)
                cur_gook.is_weapon = False
                next_turn()
                if random.randint(0, 2) == 2:
                    playing_sounds.append(random.choice(sounds['turn_sounds']))
                places_for_filling.append(((0, 10), (30, 50)))
                places_for_filling.append(((1700, 10), (175, 100)))
            places_for_filling.append((bullet_last_pos, bullet.get_size()))
        # Проверка непроизвольного движения гуков
        for team in teams:
            for gook in team.get_gooks():
                last_pos_or_none = gook.passive_move()
                for box in boxes:
                    if gook.get_rect().colliderect(box.get_rect()):
                        gook.make_damage(-box.get_heal_number())
                        places_for_filling.append((box.get_pos(), box.get_size()))
                        boxes.remove(box)
                if last_pos_or_none:
                    places_for_filling.append((gook.get_place_for_filling(last_pos_or_none, gook.get_size())))
                if gook.check_state():
                    if gook == cur_gook:
                        next_turn()
                    graveyards.append(gook.make_graveyard())
                    places_for_filling.append(gook.get_place_for_filling(gook.get_pos(), gook.get_size()))
                    team.remove_gook(gook)
                    playing_sounds.append(sounds['death_sound'])
                places_for_filling.append((gook.get_weapon().get_pos(), gook.get_weapon().get_size()))
                gook.get_weapon().set_pos(gook.get_pos())
            if not team.check_state():
                teams.remove(team)
                if len(teams) == 1:
                    sounds['victory_sound'].play()
                    win_screen(window, clock, teams[0])
        places_for_filling.append(((910, 10), (50, 50)))

        for explosion in explosions:
            if explosion.check_state():
                explosions.remove(explosion)
                places_for_filling.append((explosion.get_pos(), explosion.get_size()))

        if were_walking:
            cur_gook.change_move_image()
        elif cur_gook.get_image_name() != SHOOT_FORWARD_IMG and cur_gook.get_image_name() != SHOOT_UP_IMG:
            cur_gook.change_image_state(GOOK_IMG)
            if cur_gook.get_place_for_filling(cur_gook.get_pos(), cur_gook.get_size()) not in places_for_filling:
                places_for_filling.append(cur_gook.get_place_for_filling(cur_gook.get_pos(), cur_gook.get_size()))

        all_sprites.update(wind, places_for_filling)
        all_sprites.draw(window)
        if len(all_sprites.sprites()) < 10 and choice((True, False)):
            create_particle(wind, all_sprites, leaves_images, screen_rect)

        for place, size in places_for_filling:
            map1.draw_part(window, place, size)
        places_for_filling.clear()

        for box in boxes:
            box.draw(window)
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
        if playing_sounds:
            playing_sounds[-1].play()
        playing_sounds.clear()
        were_walking = False
        time_passed = pygame.time.get_ticks() - timer_fps
        if time_passed < 1000 // FPS:
            pygame.time.wait(1000 // FPS - time_passed)
        time_passed = pygame.time.get_ticks() - timer_fps
        fps = 1000 // time_passed
        draw_interface(window, wind, fps, cur_team, cur_gook, wind_indicator)
        pygame.display.flip()


if __name__ == '__main__':
    main()
