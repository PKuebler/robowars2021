import pygame
from pygame.locals import *
import sys
import pygame_gui
import initializeGame
import objects
import gameLogic
import random
import math
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
    # initialisiert das gamemap array
    global map_data
    map_data = [[[] for i in range(10)] for j in range(10)]
    for i, row in enumerate(map_data):
        for j, tile in enumerate(row):
            map_data[i][j] = objects.Object("grass", "terrain", 10, i, j)  # füttert die map mit terraintypen
            map_data[i][j].setImage("test80.png")

    # ladet die bildaten
    global wall, robot1, robot2, grass, ice, underGround, hoverGround
    ice = pygame.image.load('ice.png').convert_alpha()  # load images
    grass = pygame.image.load('test8060.png').convert_alpha()
    wall = pygame.image.load('test80Object.png').convert_alpha()
    robot1 = pygame.image.load('test80robot1.png').convert_alpha()
    robot2 = pygame.image.load('test80robot2.png').convert_alpha()
    underGround = pygame.image.load('underGroundBackGround.png').convert_alpha()
    hoverGround = pygame.image.load('test80Hover.png').convert_alpha()

TILE_WIDTH = 80 # 128
TILE_HEIGHT = 40 # 64
TILE_WIDTH_HALF = TILE_WIDTH / 2
TILE_HEIGHT_HALF = TILE_HEIGHT / 1.333

def mapToScreen(mapX, mapY):
    CAMERA_X = screenSurfcace.get_rect().width / 2
    CAMERA_Y = 64 #screenSurfcace.get_rect().height / 4 + 64

    screenX = (mapX - mapY) * TILE_WIDTH_HALF + CAMERA_X
    screenY = (mapX + mapY) * TILE_HEIGHT_HALF + CAMERA_Y

    return (screenX, screenY)

def screenToMap(screenX, screenY):
    CAMERA_X = screenSurfcace.get_rect().width / 2
    CAMERA_Y = 64 #screenSurfcace.get_rect().height / 4 + 64

    screenX = screenX - CAMERA_X
    screenY = screenY - CAMERA_Y

    mapX = (screenX / TILE_WIDTH_HALF + screenY / TILE_HEIGHT_HALF) / 2
    mapY = (screenY / TILE_HEIGHT_HALF - (screenX / TILE_WIDTH_HALF)) / 2

    return (mapX, mapY)

def tileOnPos(screenX, screenY, tileMap):
    mapPos = screenToMap(screenX, screenY)

    mapX = round(mapPos[0])-1
    mapY = round(mapPos[1])

    if mapX < 0 or mapX >= len(tileMap):
        return None

    if mapY < 0 or mapY >= len(tileMap[mapX]):
        return None

    tile = tileMap[mapX][mapY]

    return tile

# rendert den Hintergrund
def renderBackground(terrainMap, hoverTile):
    night = 0, 0, 76
    screenSurfcace.fill(night)

    if terrainMap == None:
        return

    for row_i, row_item in enumerate(terrainMap):  # for every row_item of the map. row_i = index of loop
        for col_i, tile in enumerate(row_item): # for every tileObject on the map col_i = index of loop
            iso = mapToScreen(row_i, col_i)
            screenSurfcace.blit(grass, (iso[0], iso[1]))  # display the actual tile

    if hoverTile != None:
        screen = mapToScreen(hoverTile.x, hoverTile.y)
        screenSurfcace.blit(hoverGround, (screen[0], screen[1]))

# renders GameObjects
def renderGameObjects(objectMap):
    if objectMap == None:
        return

    for row_i, row_item in enumerate(objectMap):  # for every row_item of the map. row_i = index of loop
        for col_i, tile in enumerate(row_item): # for every tileObject on the map col_i = index of loop
            if tile == None:
                continue

            iso = mapToScreen(tile.x, tile.y)

            if tile.obtype == "robot1":
                image = robot1
            if tile.obtype == "robot1":
                image = robot2
            elif tile.obtype == "wall":
                image = wall

            screenSurfcace.blit(image, (iso[0], iso[1]-10))  # display the actual tile

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
                                                                    html_text="Your Name is: " + str(
                                                                        playerName) + ". Password please!",
                                                                    manager=ui_manager)
                elif playerName != "" and playerPassword == "":
                    playerPassword = loginTextBox.get_text()
                    loginButton.set_text("Confirm Password")
                    playerNameLabel = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 0), (400, 100)),
                                                                    html_text="Your Name is: " + str(
                                                                        playerName) + ", Your Password is: " + str(
                                                                        playerPassword),
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
    #mixer = pygame.mixer.init()
    soundMusic = pygame.mixer.Sound('mechanoid.wav')
    soundMusic.play(-1)
    soundMusic.set_volume(0.1)

    roboto1 = pygame.image.load('robot1.png')
    roboto1_mask = pygame.mask.from_surface(roboto1, 50)

    roboto1.convert()
    rect = roboto1.get_rect()
    rect.center = roboto1.get_width() / 2, roboto1.get_height() / 2

    roboto2 = pygame.image.load('robot2.png')
    roboto2_mask = pygame.mask.from_surface(roboto2, 50)
    roboto2.convert()
    rect = roboto2.get_rect()
    rect.center = roboto2.get_width() / 2, roboto2.get_height() / 2

    hoverTile = None

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
    sessionId = "12345"

    # Host oder nicht?
    host = False                 #ÄNDERN FÜR SPIELER 2 (False)
    playerOneTurn = True
    twoLocalPlayers = True     #ÄNDERN FÜR ONLINE (False)
    twoLocalPlayersPlayerOne = True
    # online?
    if not twoLocalPlayers:
        sv = Client("pkuebler.de", 3210)
        sv.connect(playerName)
        sv.join(sessionId)
        # wenn host: karte generieren
        if host:
            terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
            jsonObjMap = initializeGame.returnObjMapWithDicts(objectMap, MAPSIZE)
            jsonTerrMap = initializeGame.returnObjMapWithDicts(terrainMap, MAPSIZE)
            waitingForPlayerTwo = True
            while waitingForPlayerTwo:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                data = sv.read()
                if data != None:
                    if "type" in data and data["type"] == "PlayerConnectEvt":
                        if data["payload"]["name"] != playerName:
                            print(data["payload"]["name"] + " joined")
                            sv.startGame(jsonTerrMap, jsonObjMap, 60)
                            print("StartGameCmd gesendet")
                            waitingForPlayerTwo = False
                        else:
                            print("kein join:")
                            print(data["payload"])
                time.sleep(1)
        else:
            waitingForPlayerOne = True
            while waitingForPlayerOne:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                data = sv.read()
                if data != None:
                    if "type" in data and data["type"] == "GameStartedEvt":
                        jsonTerrMap = data["payload"]["terrain"]
                        jsonObjMap = data["payload"]["map"]
                        terrainMap = initializeGame.createMapWithObjFromJson(jsonTerrMap, MAPSIZE)
                        objectMap, playerOneRobot, playerTwoRobot = initializeGame.createMapWithObjFromJson(jsonObjMap, MAPSIZE)
                        print(objectMap)
                        print("Karten und GameStartedEvt empfangen")
                        waitingForPlayerOne = False
                    else:
                        print("kein GameStartedEvt")
                        print(data)
                time.sleep(1)
    # offline
    else:
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)

    # Variablen zum Start
    playerTurn = True
    moveMode = True
    orders = []

    hoverTile = None


    print("starte Gameloop")
    # GameLoop
    while True:
        global time_delta
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            checkForGuiEvents(event)
            ui_manager.process_events(event)


            if event.type == MOUSEMOTION:
                tile = tileOnPos(event.pos[0], event.pos[1], terrainMap)

                if tile != None:
                    hoverTile = tile
                    print(("hit", tile.x, tile.y))
                else:
                    hoverTile = None

            # Aktion auswerten
            playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode, twoLocalPlayersPlayerOne,
                                                                 playerOneRobot, playerTwoRobot, terrainMap,
                                                                 objectMap, hoverTile)
            # wenn korrektes event wurde befehl erzeugt: spielzug endet
            if order != None:
                if twoLocalPlayers:
                    if twoLocalPlayersPlayerOne:
                        twoLocalPlayersPlayerOne = False
                    else:
                        playerTurn = False
                        receivedOrders = True ###
                else:
                    # order an server senden
                    sv.command(order)
                    print("Befehl an Server geschickt")
                    playerTurn = False
                    receivedOrders = False ###
                orders.append(order)

        # Spieler ist nicht am Zug
        if not playerTurn:
            # local: beide Befehle liegen vor
            if twoLocalPlayers:
                twoLocalPlayersPlayerOne = True
            # online: Warten auf Antwort vom server
            else:
                order = None
                ##receivedOrders = False
                #while not receivedOrders:
                print("Warte auf Befehl vom Server")
                data = sv.read()
                if data != None:
                    if "type" in data and data["type"] == "RoundEndEvt":
                        for o in data["payload"]["commands"]:
                            if o["player"] != playerName:
                                ##order = o
                                orders.append(o)
                                receivedOrders = True
                                print(o)
                        print("Befehl erhalten")
                    else:
                        print("Kein RoundEndEvt")
                        print(data["payload"])
                        time.sleep(1)
                else:
                    time.sleep(1)
                #if order != None:
                #    orders.append(order)
                #    receivedOrders = True
                #else:
                #    time.sleep(1)
            #wenn order vom server empfangen:
            if receivedOrders:
                print("führe befehle aus")
                gameLogic.executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot)
                #prüfen ob zuende
                finished = gameLogic.checkIfOver(playerOneRobot, playerTwoRobot)
                if finished and not twoLocalPlayers:
                    sv.leave()
                #sonst spielerzug wieder starten
                playerTurn = True
                orders = []

        renderBackground(terrainMap, hoverTile)
        renderGameObjects(objectMap)
        renderGUI()
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin