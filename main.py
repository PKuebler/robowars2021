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

    wall = pygame.image.load('wall.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()

    TILEWIDTH = 64  # holds the tile width and height
    TILEHEIGHT = 64
    TILEHEIGHT_HALF = TILEHEIGHT / 2
    TILEWIDTH_HALF = TILEWIDTH / 2

    for row_nb, row in enumerate(map_data):    #for every row of the map...
        for col_nb, tile in enumerate(row):
            if tile == 1:
                tileImage = wall
            else:
                tileImage = grass
            cart_x = row_nb * TILEWIDTH_HALF
            cart_y = col_nb * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y)/2
            centered_x = DISPLAYSURF.get_rect().centerx + iso_x
            centered_y = DISPLAYSURF.get_rect().centery/2 + iso_y
            DISPLAYSURF.blit(tileImage, (centered_x, centered_y)) #display the actual tile


# rendert das Spiel
def renderGame():
    #pygame.display.flip()
    FPSCLOCK.tick(30)


def startGame():
    gameWindowInitialisation()
    #graphicsInitialisation()


    #Host oder nicht?
    host = True
    #wenn host: karte generieren
    if host:
        #beide Kartenlayer
        terrainMap, objectMap = initializeGame.initGame(MAPSIZE)
        #sendMapsToServer(terrainMap, objectMap)
    else:
        pass
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
                playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode)
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