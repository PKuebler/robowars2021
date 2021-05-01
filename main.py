import pygame
from pygame.locals import *
import sys
import pygame_gui
import initializeGame
from objects import *
import gameLogic
import random

MAPSIZE = 10


# BaseGame Initialisierung
def gameWindowInitialisation():
    pygame.init()
    screenSize = 1000, 800    # window width & height
    global screenSurfcace
    screenSurfcace = pygame.display.set_mode(screenSize, DOUBLEBUF)
    global clock
    clock = pygame.time.Clock()


# GraphicFiles Initialisierung
def graphicsInitialisation():
    #initialisiert das gamemap array
    global map_data
    map_data = [[[] for i in range(10)] for i in range(10)]
    for i, row in enumerate(map_data):
        for j, tile in enumerate(row):
            map_data[i][j] = random.randint(0, 2) # füttert die map mit random terraintypen

    # ladet die bildaten
    global wall, grass, ice
    ice = pygame.image.load('ice.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()
    wall = pygame.image.load('wall2.png').convert_alpha()

# rendert den Hintergrund
def renderBackground():
    night = 0, 0, 76
    screenSurfcace.fill(night)
    TILEWIDTH = 64  # holds the tile width and height
    TILEHEIGHT = 64
    factor = 1.5  # größer = näher
    TILEHEIGHT_HALF = TILEHEIGHT / factor
    TILEWIDTH_HALF = TILEWIDTH / factor

    for row_i, row_item in enumerate(map_data):  # for every row_item of the map...
        for col_i, tile_content in enumerate(row_item):
            if tile_content == 1:
                tileImage = wall
            elif tile_content == 2:
                tileImage = ice
            else:
                tileImage = grass
            cart_x = row_i * TILEWIDTH_HALF
            cart_y = col_i * TILEHEIGHT_HALF
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y) / 2
            centered_x = screenSurfcace.get_rect().centerx + iso_x
            centered_y = screenSurfcace.get_rect().centery / 2 + iso_y
            screenSurfcace.blit(tileImage, (centered_x, centered_y))  # display the actual tile


# rendert das Spiel
def renderGameObjects():
    pass # sollte ähnlich funktionieren wie bei renderBackground()


def renderGUI(event):
    global manager
    manager = pygame_gui.UIManager((1000, 800))
    global textBoxGold
    textBoxGold = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((200, 250), (250, 33)),
                                                html_text="Enter Player Name Here",
                                                manager=manager)
    checkForGuiEvent(event)
    manager.draw_ui(screenSurfcace)


def checkForGuiEvent(event):
    clock.tick(60)
    time_delta = clock.tick(60) / 1000.0
    manager.process_events(event)
    manager.update(time_delta)



def startGame():
    gameWindowInitialisation()
    graphicsInitialisation()

    # Host oder nicht?
    host = True
    # wenn host: karte generieren
    if host:
        # beide Kartenlayer
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
        # Host ist Spieler 1
        playerOne = True
        # sendMapsToServer(terrainMap, objectMap)
    else:
        playerOne = False
        # receiveMapsFromServer(terrainMap, objectMap)

    # Variablen zum Start
    playerTurn = True
    moveMode = True

    # GameLoop
    while True:
        for event in pygame.event.get():
            # Aktion auswerten
            playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode, playerOne,
                                                                     playerOneRobot, playerTwoRobot, terrainMap,
                                                                     objectMap)
            #wenn korrektes event wurde befehl erzeugt: spielzug endet
            if order != None:
                # sendOrderToServer(order)
                playerTurn = False
        # Spieler ist nicht am Zug: Warten auf Antwort vom server
        if not playerTurn:
            # receiveOrderFromServer()
            # time.sleep(1)
            #wenn order vom server empfangen:
            #ausführen aller order (in gameLogic.executeOrders(orders))
            #prüfen ob zuende
            #sonst spielerzug wieder starten
            playerTurn = True

        renderBackground()
        renderGameObjects()
        renderGUI(event)
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin