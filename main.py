import pygame
from pygame.locals import *
import sys
import pygame_gui
import initializeGame
#from objects import *
import gameLogic
import random
from client import *
import time

MAPSIZE = 10


# BaseGame Initialisierung
def gameWindowInitialisation():
    pygame.init()
    global screenSize
    screenSize = 1000, 800  # window width & height
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
    global wall, grass, ice, underGround
    ice = pygame.image.load('ice.png').convert_alpha()  # load images
    grass = pygame.image.load('grass.png').convert_alpha()
    wall = pygame.image.load('house1.png').convert_alpha()
    underGround = pygame.image.load('underGroundBackGround.png').convert_alpha()

# rendert den Hintergrund
def renderBackground():
    night = 0, 0, 76
    screenSurfcace.fill(night)
    screenSurfcace.blit(underGround, (-2, -32))  # display the actual tile

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
    pass


def renderGUI():
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screenSurfcace)


def guiInitialisation():
    global ui_manager
    ui_manager = pygame_gui.UIManager(screenSize)
    global clock
    clock = pygame.time.Clock()
    clock.tick(30)  # FPS Cap

    global playerName
    playerName = ""
    global playerPassword
    playerPassword = ""

    global playerNameLabel
    playerNameLabel = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (400, 100)),
                                                    html_text=str("Enter your name"),
                                                    manager=ui_manager)
    global loginTextBox
    loginTextBox = pygame_gui.elements.UITextEntryLine(pygame.Rect((0, 110),
                                                                 (400, 200)), ui_manager)
    global loginButton
    loginButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 160), (400, 50)),
                                               text='Confirm Name',
                                               manager=ui_manager)


def checkForGuiEvents(event):
    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == loginButton:
                global playerName
                global playerPassword
                if playerName == "":
                    playerName = loginTextBox.get_text()
                    loginTextBox.set_text("")
                    playerNameLabel = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (400, 100)),
                                                                    html_text="Your Name is: " + str(playerName) + ". Password please!",
                                                                    manager=ui_manager)
                elif playerName != "" and playerPassword == "":
                    playerPassword = loginTextBox.get_text()
                    loginButton.set_text("Confirm Password")
                    playerNameLabel = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (400, 100)),
                                                                    html_text="Your Name is: " + str(
                                                                    playerName) + ", Your Password is: " + str(playerPassword),
                                                                    manager=ui_manager)
                    loginTextBox.set_text("Thank You.")
                    loginButton.set_text("Connect!")
                elif playerName != "" and playerPassword != "":
                    print("Connect to Server")
                    # print(playerName)


def startGame():
    gameWindowInitialisation()
    graphicsInitialisation()
    guiInitialisation()

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
    #für Server
    playerName = "Lars"         #ÄNDERN FÜR SPIELER 2
    sessionId = 12345
    # Host oder nicht?
    host = True                 #ÄNDERN FÜR SPIELER 2 (False)
    playerOneTurn = True
    twoLocalPlayers = True     #ÄNDERN FÜR ONLINE (False)
    twoLocalPlayersPlayerOne = True
    #online?
    if not twoLocalPlayers:
        sv = Client("pkuebler.de", 3210)
        sv.connect(playerName)
        sv.join(sessionId)
        # wenn host: karte generieren
        if host:
            terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
            jsonObjMap = initializeGame.returnObjMapWithDicts(objectMap, MAPSIZE)
            waitingForPlayerTwo = True
            while waitingForPlayerTwo:
                data = sv.read()
                if data != None and "type" in data:
                    if data["type"] == "PlayerConnectEvt":
                        if data["payload"]["name"] != playerName:
                            print(data["payload"]["name"] + " joined")
                            sv.startGame(terrainMap, jsonObjMap, 60)
                            waitingForPlayerTwo = False
                        else:
                            print(data["payload"])
                time.sleep(1)
        else:
            waitingForPlayerOne = True
            while waitingForPlayerOne:
                data = sv.read()
                if data != None:
                    if "StartGameCmd" in data:
                        terrainMap = data["terrain"]
                        objMapJson = data["map"]
                        objectMap, playerOneRobot, playerTwoRobot = initializeGame.createMapWithObjFromJson(objMapJson, MAPSIZE)
                    else:
                        print(data["payload"])
                time.sleep(1)
    #offline
    else:
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)

    # Variablen zum Start
    playerTurn = True
    moveMode = True
    orders = []

    # GameLoop
    while True:
        global time_delta
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            checkForGuiEvents(event)
            ui_manager.process_events(event)
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
                    #order an server senden
                    sv.command(order)
                    playerTurn = False
                orders.append(order)

        # Spieler ist nicht am Zug
        if not playerTurn:
            #local: beide Befehle liegen vor
            if twoLocalPlayers:
                twoLocalPlayersPlayerOne = True
            #online: Warten auf Antwort vom server
            else:
                receivedOrders = False
                while not receivedOrders:
                    data = sv.read()
                    if data != None and "type" in data:
                        if data["type"] == "CommandCmd":
                            order = data["payload"]
                            receivedOrders = True
                        else:
                            print(data["payload"])
                    time.sleep(1)
                if order != None:
                    orders.append(order)
                    receivedOrders = True
                else:
                    time.sleep(1)
            #wenn order vom server empfangen:
            gameLogic.executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot)
            #prüfen ob zuende
            finished = gameLogic.checkIfOver(playerOneRobot, playerTwoRobot)
            if finished and not twoLocalPlayers:
                sv.leave()
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