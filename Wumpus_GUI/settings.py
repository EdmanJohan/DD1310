"""Settings File. Here imports, variables, constants and standard paths are stored for easy
    within functions and methods.

    Simplifies for the user in-case something should be changed."""

# Imports
import pygame as pg
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, K_RETURN, K_UP, K_DOWN, K_BACKSPACE, K_SPACE
import sys
import os
from random import randint, choice

pg.init()

# Game settings
DIFFICULTY = 2
ARROWS = 5
BATS = 3
PITS = 4

# Keys
MOVEKEYS = {
    273: (0, -1),
    274: (0, 1),
    275: (1, 0),
    276: (-1, 0)
}

# #====================# #
# #====================# #

# Window settings
WIDTH = 1024
HEIGHT = 512
TITLE = "Wumpus"

TILESIZE = 128
GRIDWIDTH = WIDTH / TILESIZE - 3
GRIDHEIGHT = HEIGHT / TILESIZE

SYS_INFO = pg.display.Info()
X_POS = SYS_INFO.current_w / 2 - WIDTH / 2
Y_POS = SYS_INFO.current_h / 2 - HEIGHT / 2
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X_POS, Y_POS)

# Colors & Light
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 20, 60)
BLUE = (95, 158, 160)
GREEN = (0, 250, 154)
LIGHTGREY = (100, 100, 100)
DARKGREY = (40, 40, 40)
YELLOW = (173, 255, 47)
PINK = (218, 112, 214)

LIGHT_FULL = 255
LIGHT_NULL = 0

# Assets, PATH's and standard files.
MAIN = os.path.dirname(os.path.relpath(__file__))
ASSETS = os.path.join(MAIN, "assets/")
FILE = ASSETS
IMAGE = os.path.join(ASSETS, "images/")
HIGHSCORE = "Highscore.txt"
WUMPUS = "WUMPUS_GLOW.png"
WUMPUSDEAD = "WUMPUSDEAD_GLOW.png"
PLAYER = "Player.png"
PIT = "Pit.png"
BAT = "Bat.png"
TILE = "tile.png"
BACKGROUND = "Dungeon.jpg"
BACKGROUND_GO_LOST = "Monster.png"
BACKGROUND_GO_WON = "Slayed.jpg"
WELCOME = "WelcomeLabel.png"
GAMEOVER = "GameOverLabel.png"
ARROW_RIGHT = "Arrow-Right.png"
ARROW_UP = "Arrow-Up.png"
ARROW_LEFT = "Arrow-Left.png"
ARROW_DOWN = "Arrow-Down.png"


