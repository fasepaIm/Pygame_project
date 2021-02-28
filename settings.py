from os import path


#Объявляем переменные
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (20, 20, 20)

TOTAL_LEVEL_WIDTH = 0
TOTAL_LEVEL_HEIGHT = 0

GAME_OFF = False
ENEMIES_SPAWN_COORDINATES = []
WIN_WIDTH = 800 #Ширина создаваемого окна
WIN_HEIGHT = 640 # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
SHIFT = 0
NIGHT = False
SELECTED_MODE = 'mode: NORMAL'
NIGHT_COLOR = (0, 0, 0)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"

MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png',
                  'whitePuff17.png', 'whitePuff18.png']

BACKGROUND_MUSIC = 'second.ogg'
PLAYER_SHOT_SOUND = 'player_shot.wav'
PLAYER_RIDE_SOUND = 'player_ride.wav'
PLAYER_STAY_SOUND = 'player_stay.wav'
LEVEL_START_SOUND = 'level_start.wav'
ENEMY_HIT_SOUND = 'enemy_hit.wav'
EXPLOSION_SOUND = 'explosion.wav'
RICARDO_SOUND = 'ricardo.wav'
MUSIC_VOLUME = 0.05

game_folder = path.dirname(__file__)
map_folder = path.join(game_folder, 'maps')
music_folder = path.join(game_folder, 'assets/music')
sounds_folder = path.join(game_folder, 'assets/sounds')
images_folder = path.join(game_folder, 'assets/images')
fonts_folder = path.join(game_folder, 'assets/fonts')

FPS = 60

MOVE_SPEED = 1
PLAYER_HEALTH = 100
ENEMIES_KILLED = 0

POINT_PRICE = 10

game_folder = path.dirname(__file__)
PLAYERS_TANK_IMAGE = path.join(images_folder, 'players_tank.png')
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

AMMUNITION = 5
BULLET_SPEED = 6
BULLET_LIFETIME = 1000

BULLET_X, BULLET_Y = 1, 0
KICKBACK = 3

BULLET_IMAGE = path.join(images_folder, 'bullet.png')

ENEMY_SPEED = 2
ENEMY_KICK = 15
ENEMY_DAMAGE = 20

ENEMY_TANK_IMAGE = path.join(images_folder, 'enemies_tank.png')

FLASH_DURATION = 40
KILL_FLASH_DURATION = 150
EFFECTS_LAYER = 4

BOOM_FLASHES = ['boom_flashes_1.png', 'boom_flashes_2.png',
                'boom_flashes_3.png', 'boom_flashes_4.png']
kill_flashes = []

RICARDO_IMAGE = path.join(images_folder, 'ricardo.png')
