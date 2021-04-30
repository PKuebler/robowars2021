import pygame
import sys
import pygame_gui
import Maps


# BaseGame Initialisierung
def gameWindowInitialisation():
    pygame.init()
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()


# GraphicFiles Initialisierung
def graphicsInitialisation():
    map_data = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]  # the data for the map expressed as [row[tile]].

    TILEWIDTH = 64  # holds the tile width and height
    TILEHEIGHT = 64
    TILEHEIGHT_HALF = TILEHEIGHT / 2
    TILEWIDTH_HALF = TILEWIDTH / 2

    wall = pygame.image.load('wall.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()


# rendert das Spiel
def renderGame():
    pass


# startet das Spiel
class GameLogic(object):
    pass


def startGame():
    gameWindowInitialisation()
    graphicsInitialisation()

    # GameLoop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        GameLogic()
        renderGame()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin
