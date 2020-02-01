BACKGROUND_IMG = 'background.png'
RESOLUTION = 1920, 1080

GOOK_IMG = 'wait.png'
GOOK_RES = (200, 200)
MOVE1_IMG = 'move1.png'
MOVE1_RES = (200, 200)
MOVE2_IMG = 'move2.png'
MOVE2_RES = (200, 200)
SHOOT_FORWARD_IMG = 'shoot_forward.png'
SHOOT_FORWARD_RES = (200, 200)
SHOOT_UP_IMG = 'shoot_up.png'
SHOOT_UP_RES = (200, 200)

CANNON_PROJ_IMG = 'cannon_proj.png'
CANNON_PROJ_RES = (100, 100)
RIFLE_PROJ_IMG = 'rifle_proj.png'
RIFLE_PROJ_RES = (100, 100)
LASER_PROJ_IMG = 'laser_proj.png'
LASER_PROJ_RES = (100, 100)

GRENADE_IMG = 'grenade.png'
GRENADE_RES = (100, 100)
CANNON_IMG = 'cannon.png'
CANNON_RES = (100, 100)
RIFLE_IMG = 'rifle.png'
RIFLE_RES = (100, 100)
LASER_IMG = 'laser.png'
LASER_RES = (100, 100)

PROJECTILES = {'cannon': (CANNON_PROJ_IMG, CANNON_PROJ_RES, 1),
               'rifle': (RIFLE_PROJ_IMG, RIFLE_PROJ_RES, 0.2),
               'grenade': (GRENADE_IMG, GRENADE_RES, 1),
               'laser': (LASER_PROJ_IMG, LASER_PROJ_RES, 0)}
WEAPONS = {'cannon': (CANNON_IMG, CANNON_RES),
           'rifle': (RIFLE_IMG, RIFLE_RES),
           'grenade': (GRENADE_IMG, GRENADE_RES),
           'laser': (LASER_IMG, LASER_RES)}

TEAMS = [['BTS', 'BLUE', [(0, 0), (0, 500), (0, 1000)], ('ChiMin', 'ChinGook', 'Tahyon')],
         ['CHUCHE', 'RED', [(500, 0), (500, 500), (500, 1000)], ('KimChenIn', 'KimChenIr', 'KimIrSen')],
         ['ANIME', 'WHITE', [(1000, 0), (1000, 500), (1000, 1000)], ('Hidetaka', 'Hayao', 'Kodjima')]]

TEAM_LEN = len(TEAMS[0][3])

G = 10

wind = 0
moved_gooks = []
bullets = []
teams = []
cur_gook = None
cur_team = None

POSITIONS = [(100, 400), (200, 400), (300, 400),
             (400, 400), (500, 400), (600, 400),
             (700, 400), (800, 400), (900, 400)]

is_working = True
fullscreen = True
is_shot = False
