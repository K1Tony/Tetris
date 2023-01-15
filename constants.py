import os.path
import pygame as pg
pg.init()

"""
PARAMS
"""
RECTS_X = 12
RECTS_Y = 22
RECTS_SCORE = 10
FPS = 60

"""
DIMENSIONS
"""
RECT_SIDE = 25
PAD = 2
WIDTH = (RECT_SIDE + PAD) * RECTS_X
HEIGHT = (RECT_SIDE + PAD) * RECTS_Y
SCOREBOARD = (RECT_SIDE + PAD) * RECTS_SCORE

"""
SURFACES
"""
WIN = pg.display.set_mode((WIDTH + SCOREBOARD, HEIGHT))

"""
COLORS
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PINK = (255, 0, 255)
GREY = (128, 128, 128)
ORANGE = (255, 128, 0)
LIME = (128, 255, 0)
VIOLET = (128, 0, 255)
MAGENTA = (255, 0, 128)
DIMMER = {
    'blue': (0, 0, 72),
    'red': (48, 0, 0),
    'green': (0, 32, 0),
    'orange': (48, 16, 0),
    'yellow': (64, 64, 0),
    'cyan': (0, 48, 48),
    'purple': (32, 0, 64)
}

"""
EVENTS
"""
SCORE = pg.USEREVENT + 1
CRUSH = pg.USEREVENT + 2

"""
FONTS
"""
WELCOME = pg.font.SysFont('Times New Roman', WIDTH // 8)
PLAY = pg.font.SysFont('Arial', 50)
OPTIONS = pg.font.SysFont('Arial', 30)
SCORE_FONT = pg.font.SysFont('Impact', 40)
SUB_FONT = pg.font.SysFont('Impact', 20)
GAME_OVER = pg.font.SysFont('Arial', WIDTH // 4, bold=True)
NEXT_SHAPE = pg.font.SysFont('Arial', 30)
BACK = pg.font.SysFont('Impact', 40)
SPEED = pg.font.SysFont('Arial', 40)
GAME_SPEED = pg.font.SysFont('Arial', 20)

"""
SOUNDS
"""
SMASH = pg.mixer.Sound(os.path.join('Assets', 'laser_shoot.wav'))
REMOVE = pg.mixer.Sound(os.path.join('Assets', 'power_up.wav'))
R = pg.mixer.Sound(os.path.join('Assets', 'power_up1.wav'))

"""
OTHERS
"""
SHAPES = [([1, 4], [1, 5], [1, 6], [1, 7]), ([1, 4], [2, 4], [2, 5], [2, 6]), ([1, 7], [2, 7], [2, 6], [2, 5]),
          ([1, 5], [1, 6], [2, 5], [2, 6]), ([1, 6], [1, 7], [2, 5], [2, 6]), ([1, 4], [1, 5], [2, 5], [2, 6]),
          ([1, 5], [2, 4], [2, 5], [2, 6])]
COLORS = ['blue', 'green', 'red', 'orange', 'yellow', 'cyan', 'purple']
COLOR_RGB = {
    'blue': (0, 0, 255),
    'green': (0, 255, 0),
    'red': (255, 0, 0),
    'orange': (255, 128, 0),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'purple': (128, 0, 255)
}

