ANCHO_GRILLA = 11 # NO EDITAR
LARGO_GRILLA = 16 # NO EDITAR

# Complete con los demás parámetros

# celdas
CELL_SIZE = 32 + 2

# general
CANTIDAD_VIDAS = 7
TIEMPO_CUENTA_REGRESIVA = 120
MULTIPLICADOR_PUNTAJE = 3

# nombre
MIN_CARACTERES = 3
MAX_CARACTERES = 11

VELOCIDAD_LUIGI = 0
# fantasmas
MIN_VELOCIDAD = 1
MAX_VELOCIDAD = 9

MAXIMO_FANTASMAS_VERTICAL = 5
MAXIMO_FANTASMAS_HORIZONTAL = 14

# bloques
MAXIMO_PARED = 7
MAXIMO_ROCA = 5
MAXIMO_FUEGO = 3

# current path
from os.path import dirname, abspath
PATH = dirname(abspath(__file__))


# frames
REFRESH_RATE = .100

###### sprites routes ######
from os.path import join

# elements
BORDER_SPRITE = join(PATH, 'sprites', 'Elementos', 'bordermap.png')
WALL_SPRITE = join(PATH, 'sprites', 'Elementos', 'wall.png')
ROCK_SPRITE = join(PATH, 'sprites', 'Elementos', 'rock.png')
FIRE_SPRITE = join(PATH, 'sprites', 'Elementos', 'fire.png')
STAR_SPRITE = join(PATH, 'sprites', 'Elementos', 'osstar.png')

# luigi
LUIGI_SPRITE = join(PATH, 'sprites', 'Personajes', 'luigi_front.png')
LUIGI_DOWN_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'luigi_down_1.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_down_2.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_down_3.png')
]
LUIGI_UP_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'luigi_up_1.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_up_2.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_up_3.png')
]
LUIGI_LEFT_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'luigi_left_1.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_left_2.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_left_3.png')
]
LUIGI_RIGTH_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'luigi_rigth_1.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_rigth_2.png'),
    join(PATH, 'sprites', 'Personajes', 'luigi_rigth_3.png')
]

# fantasma vertical
RED_GHOST_DOWN_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'red_ghost_vertical_1.png'),
    join(PATH, 'sprites', 'Personajes', 'red_ghost_vertical_2.png'),
    join(PATH, 'sprites', 'Personajes', 'red_ghost_vertical_3.png')
]
RED_GHOST_UP_SPRITES = RED_GHOST_DOWN_SPRITES

# fantasma horizontal
WHITE_GHOST_LEFT_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'white_ghost_left_1.png'),
    join(PATH, 'sprites', 'Personajes', 'white_ghost_left_2.png'),
    join(PATH, 'sprites', 'Personajes', 'white_ghost_left_3.png')
]
WHITE_GHOST_RIGTH_SPRITES = [
    join(PATH, 'sprites', 'Personajes', 'white_ghost_rigth_1.png'),
    join(PATH, 'sprites', 'Personajes', 'white_ghost_rigth_2.png'),
    join(PATH, 'sprites', 'Personajes', 'white_ghost_rigth_3.png')
]

# sounds
VICTORY_SOUND = join(PATH, 'sounds', 'stageClear.wav')
GAME_OVER_SOUND = join(PATH, 'sounds', 'gameOver.wav')

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
GET_STAR = (0, 0)

DIRECTIONS = {
    65: LEFT,
    68: RIGHT,
    87: UP,
    83: DOWN,
    71: GET_STAR
}