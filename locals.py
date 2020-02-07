RESOLUTION = 1920, 1080
BACKGROUND_IMG = 'background.png'
GROUND_IMG = 'ground.png'

death_sound_way = 'death_sound.wav'
explode_sound_way = 'explode_sound.wav'
shot_sound_way = 'shot_sound.wav'
soundtrack_way = 'soundtrack.wav'
victory_sound_way = 'victory_sound.wav'
gook_sounds = ['gook_sound1.wav',
               'gook_sound2.wav',
               'gook_sound3.wav']

GOOK_IMG = 'wait.png'
MOVE1_IMG = 'move1.png'
MOVE2_IMG = 'move2.png'
SHOOT_FORWARD_IMG = 'shoot_front.png'
SHOOT_UP_IMG = 'shoot_up.png'
GOOK_RES = (80, 80)

WIND_IMGS = {
    -5: 'windbox_-5.png',
    -4: 'windbox_-4.png',
    -3: 'windbox_-3.png',
    -2: 'windbox_-2.png',
    -1: 'windbox_-1.png',
    0:  'windbox_0.png',
    1:  'windbox_1.png',
    2:  'windbox_2.png',
    3:  'windbox_3.png',
    4:  'windbox_4.png',
    5:  'windbox_5.png'
}
WIND_RES = (100, 30)

CHARGE_BAR_IMGS = {
    0: 'chargebar0.png',
    1: 'chargebar1.png',
    2: 'chargebar2.png',
    3: 'chargebar3.png',
    4: 'chargebar4.png',
    5: 'chargebar5.png',
    6: 'chargebar6.png',
    7: 'chargebar7.png',
    8: 'chargebar8.png',
    9: 'chargebar9.png',
    10: 'chargebar10.png',
    11: 'chargebar11.png',
    12: 'chargebar12.png'
}
HEALTH_BOX_IMG = 'health_box.png'
HEALTH_BOX_RES = (26, 24)
HEALTH_BOX_POSITIONS = [(100, 100), (1000, 100), (200, 500)]

CANNON_PROJ_IMG = 'cannon_proj.png'
CANNON_PROJ_RES = (30, 14)
RIFLE_PROJ_IMG = 'rifle_proj.png'
RIFLE_PROJ_RES = (28, 10)
LASER_PROJ_IMG = 'laser_proj.png'
LASER_PROJ_RES = (100, 100)

GRENADE_IMG = 'grenade.png'
GRENADE_RES = (100, 100)
CANNON_IMG = 'cannon.png'
CANNON_RES = (60, 22)
RIFLE_IMG = 'rifle.png'
RIFLE_RES = (99, 22)
LASER_IMG = 'laser.png'
LASER_RES = (100, 100)

CANNON_DMG = 60
GRENADE_DMG = 60
RIFLE_DMG = 50
LASER_DMG = 50

GRAVESTONE_IMG = 'gravestone.png'
GRAVESTONE_RES = (53, 59)
EXPLOSION_IMG = 'explosion.png'
EXPLOSION_RES = (150, 150)

# оружие: изображение снаряда, размер изображения, множитель G, макс. скорость, радиус взрыва, урон
PROJECTILES = {'cannon': (CANNON_PROJ_IMG, CANNON_PROJ_RES, 0.25, 20, 150, 30),
               'rifle': (RIFLE_PROJ_IMG, RIFLE_PROJ_RES, 0.1, 100, 20, 40)}

WEAPONS = {'cannon': (CANNON_IMG, CANNON_RES),
           'rifle': (RIFLE_IMG, RIFLE_RES)}

TEAMS = [['BTS', 'blue', [(50, 0)], ('ChiMin',)],
         ['CHUCHE', 'red', [(600, 0)], ('MaoJeDun',)]]
         # ['ANIME', 'white', [(1100, 0)], ('Hidetaka',)]]
TEAM_LEN = len(TEAMS[0][3])

FPS = 30

G = 1
wind = 0

MOVEMENT_SPEED = 5
bullets = []
teams = []
graveyards = []
places_for_filling = []
playing_sounds = []
explosions = []
cur_gook = None
cur_team = None

