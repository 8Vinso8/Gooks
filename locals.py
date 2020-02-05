RESOLUTION = 1920, 1080
BACKGROUND_IMG = 'background.png'
GROUND_IMG = 'ground.png'

death_sound_way = 'death_sound.wav'
explode_sound_way = 'explode_sound.wav'
shot_sound_way = 'shot_sound.wav'
soundtrack_way = 'soundtrack.wav'
victory_sound_way = 'victory_sound.wav'

GOOK_IMG = 'wait.png'
MOVE1_IMG = 'move1.png'
MOVE2_IMG = 'move2.png'
SHOOT_FORWARD_IMG = 'shoot_front.png'
SHOOT_UP_IMG = 'shoot_up.png'
GOOK_RES = (80, 80)

CANNON_PROJ_IMG = 'cannon_proj.png'
CANNON_PROJ_RES = (30, 14)
RIFLE_PROJ_IMG = 'rifle_proj.png'
RIFLE_PROJ_RES = (100, 100)
LASER_PROJ_IMG = 'laser_proj.png'
LASER_PROJ_RES = (100, 100)

GRENADE_IMG = 'grenade.png'
GRENADE_RES = (100, 100)
CANNON_IMG = 'cannon.png'
CANNON_RES = (60, 22)
RIFLE_IMG = 'rifle.png'
RIFLE_RES = (100, 100)
LASER_IMG = 'laser.png'
LASER_RES = (100, 100)

CANNON_DMG = 60
GRENADE_DMG = 60
RIFLE_DMG = 50
LASER_DMG = 50

GRAVEYARD_IMG = 'graveyard.png'
GRAVEYARD_RES = (53, 59)
EXPLOSION_IMG = 'explosion.png'
EXPLOSION_RES = (150, 150)


PROJECTILES = {'cannon': (CANNON_PROJ_IMG, CANNON_PROJ_RES, 0.25, 20, 150, 60),
               'rifle': (RIFLE_PROJ_IMG, RIFLE_PROJ_RES, 0.2, 10, 5, 60),
               'grenade': (GRENADE_IMG, GRENADE_RES, 1, 2, 150, 40),
               'laser': (LASER_PROJ_IMG, LASER_PROJ_RES, 0, 20, 5, 40)}
WEAPONS = {'cannon': (CANNON_IMG, CANNON_RES),
           'rifle': (RIFLE_IMG, RIFLE_RES),
           'grenade': (GRENADE_IMG, GRENADE_RES),
           'laser': (LASER_IMG, LASER_RES)}

TEAMS = [['BTS', 'blue', [(0, 0)], ('ChiMin',)],
         ['CHUCHE', 'red', [(500, 0)], ('KimChenIn',)],
         ['ANIME', 'white', [(1700, 0)], ('Hidetaka',)]]
TEAM_LEN = len(TEAMS[0][3])

FPS = 30

G = 1

MOVEMENT_SPEED = 5
wind = 0
moved_gooks = []
bullets = []
teams = []
graveyards = []
places_for_filling = []
playing_sounds = []
explosions = []
cur_gook = None
cur_team = None

