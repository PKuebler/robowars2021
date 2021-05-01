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
    screenSize = 1000, 800  # window width & height
    global screenSurfcace
    screenSurfcace = pygame.display.set_mode(screenSize, DOUBLEBUF)
    global clock
    clock = pygame.time.Clock()


# GraphicFiles Initialisierung
def graphicsInitialisation():
    # initialisiert das gamemap array
    global map_data
    map_data = [[[] for i in range(10)] for i in range(10)]
    for i, row in enumerate(map_data):
        for j, tile in enumerate(row):
            map_data[i][j] = random.randint(0, 2)  # füttert die map mit random terraintypen

    # ladet die bildaten
    global wall, grass, ice
    ice = pygame.image.load('ice.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()
    wall = pygame.image.load('house1.png').convert_alpha()


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
    pass  # sollte ähnlich funktionieren wie bei renderBackground()


def renderGUI():
    pass


def startGame():
    gameWindowInitialisation()
    graphicsInitialisation()

    """variablen:
    host: True für Spieler1, der die Karte erstellt, wenn Spieler2, der über den Server joint False
    playerOneTurn: Bei local Coop relevant: Ist Spieler1 dran, sonst Spieler2
    twoLocalPlayers: lokaler 2-Spieler-Modus
    twoLocalPlayersPlayerOne: nur für lokalen 2-Spieler-Modus: ist Player 1 dran? sonst Player 2
    playerOne: bin ich Spieler1? identische mit host
    playerTurn: Ist der/sind die Spieler am Zug; wenn beide Orders vorliegen, auf False setzen für Abarbeitung
    moveMode: wenn True, bewegungsbefehl ausführen, sonst angriffsbefehl - ggf. später noch um angriffsart erweitern
    playerOneRobot, playerTwoRobot: Die Objekte mit den beiden Spieler-Robotern; eine "KI" könnte noch eine Liste der feind-roboter bekommen
    """

    # Host oder nicht?
    host = True
    playerOneTurn = True
    twoLocalPlayers = True
    twoLocalPlayersPlayerOne = True
    # wenn host: karte generieren
    if host:
        # beide Kartenlayer
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
        # sendMapsToServer(terrainMap, objectMap)
    else:
        pass
        # receiveMapsFromServer(terrainMap, objectMap)

    # Variablen zum Start
    playerTurn = True
    moveMode = True
    orders = []

    # GameLoop
    while True:
        for event in pygame.event.get():
            # Aktion auswerten
            playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode, twoLocalPlayersPlayerOne,
                                                                     playerOneRobot, playerTwoRobot, terrainMap,
                                                                     objectMap)
            #wenn korrektes event wurde befehl erzeugt: spielzug endet
            if order != None:
                if twoLocalPlayers:
                    if twoLocalPlayersPlayerOne:
                        twoLocalPlayersPlayerOne = False
                    else:
                        playerTurn = False
                else:
                    # sendOrderToServer(order)
                    playerTurn = False
                orders.append(order)

        # Spieler ist nicht am Zug: Warten auf Antwort vom server
        if not playerTurn:
            if twoLocalPlayers:
                twoLocalPlayersPlayerOne = True
            else:
                #erstmal überspringen
                pass
                """
                receivedOrders = False
                while not receivedOrders:
                    order = receiveOrderFromServer()
                    if order != None:
                        orders.append(order)
                        receivedOrders = True
                    else:
                        time.sleep(1)"""
            #wenn order vom server empfangen:
            gameLogic.executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot)
            #prüfen ob zuende
            #sonst spielerzug wieder starten
            playerTurn = True

            orders = []

        renderBackground()
        renderGameObjects()
        renderGUI()
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin
