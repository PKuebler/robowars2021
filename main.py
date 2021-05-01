import pygame
from pygame.locals import *
import sys
import pygame_gui
import initializeGame
from objects import *
import gameLogic

MAPSIZE = 10

# BaseGame Initialisierung
def gameWindowInitialisation():
    pygame.init()
    size = 1000, 800
    global screen
    #screen = pygame.display.set_mode(size)
    global DISPLAYSURFACE
    DISPLAYSURFACE = pygame.display.set_mode(size, DOUBLEBUF)
    global clock
    clock = pygame.time.Clock()


# GraphicFiles Initialisierung
def graphicsInitialisation():
    global map_data
    map_data = [
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]  # the data for the map expressed as [row[tile]].

    global wall, grass
    wall = pygame.image.load('wall2.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()


# rendert das Spiel
def renderGame():
    TILEWIDTH = 64  # holds the tile width and height
    TILEHEIGHT = 64
    factor = 2 #größer = näher
    TILEHEIGHT_HALF = TILEHEIGHT / factor
    TILEWIDTH_HALF = TILEWIDTH / factor

    for row_i, row_item in enumerate(map_data):  # for every row_item of the map...
        for col_i, tile_content in enumerate(row_item):
            if tile_content == 1:
                tileImage = wall
            else:
                tileImage = grass
            cart_x = row_i * TILEWIDTH_HALF
            cart_y = col_i * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = DISPLAYSURFACE.get_rect().centerx + iso_x
            centered_y = DISPLAYSURFACE.get_rect().centery / 2 + iso_y
            DISPLAYSURFACE.blit(tileImage, (centered_x, centered_y))  # display the actual tile
    pygame.display.flip()
    clock.tick(30)


def startGame():
    gameWindowInitialisation()
    #graphicsInitialisation()


    #Host oder nicht?
    host = True
    #wenn host: karte generieren
    if host:
        #beide Kartenlayer
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
        #Host ist Spieler 1
        playerOne = True
        #sendMapsToServer(terrainMap, objectMap)
    else:
        playerOne = False
        #receiveMapsFromServer(terrainMap, objectMap)

    #Variablen zum Start
    playerTurn = True
    moveMode = True

    # GameLoop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            #Spieler ist am Zug
            elif playerTurn:
                #Aktion auswerten
                playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode, playerOne, playerOneRobot, playerTwoRobot, terrainMap, objectMap)
                if order != None:
                    pass
                    #sendOrderToServer(order)
                    playerTurn = False
        #Spieler ist nicht am Zug: Warten auf Antwort
        if not playerTurn:
            #receiveOrderFromServer()
            time.sleep(1)
        renderGame()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin