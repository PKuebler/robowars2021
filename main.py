import pygame
from pygame.locals import *
import sys
import pygame_gui
import initializeGame
import objects
import gameLogic
import random
import math

import player
from client import *
import time
import renderer
import assets

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
    global mapRenderer, assetManager

    assetManager = assets.AssetManager()
    assetManager.addImage("grass", "assets/images/test8060.png")
    assetManager.addImage("water", "assets/images/test8060water.png")
    assetManager.addImage("wall", "assets/images/test80Object.png")
    assetManager.addImage("robot1", "assets/images/test80robot1.png")
    assetManager.addImage("robot2", "assets/images/test80robot2.png")
    assetManager.addImage("hoverGround", "assets/images/test80Hover.png")
    assetManager.addImage("healthbar", "assets/images/healthbar.png")
    assetManager.addImage("healthstatus", "assets/images/healthstatus.png")
    assetManager.addImage("selectedCursor", "assets/images/test80Cursor.png")
    assetManager.load()

    backgroundColor = 16, 17, 18
    mapRenderer = renderer.Renderer(assetManager, backgroundColor)

def tileOnPos(screenX, screenY, tileMap):
    mapPos = mapRenderer.screenToMap(screenX, screenY)

    mapX = round(mapPos[0])-1
    mapY = round(mapPos[1])

    if mapX < 0 or mapX >= len(tileMap):
        return None

    if mapY < 0 or mapY >= len(tileMap[mapX]):
        return None

    tile = tileMap[mapX][mapY]

    return tile

def renderGUI(time_delta):
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screenSurfcace)

def guiInitialisation():
    global ui_manager
    ui_manager = pygame_gui.UIManager(screenSize)
    global clock
    clock = pygame.time.Clock()
    clock.tick(30)  # FPS Cap

    global playersessionID
    playersessionID = ""

    global loginTextBox
    loginTextBox = pygame_gui.elements.UITextEntryLine(pygame.Rect((screenSurfcace.get_width() / 2 - 200, 200),
                                                                   (400, 50)), ui_manager)
    loginTextBox.set_text("Enter your name")

    global sessionIDTextBox
    sessionIDTextBox = pygame_gui.elements.UITextEntryLine(pygame.Rect((screenSurfcace.get_width()/2-200, 260),
                                                                   (400, 50)), ui_manager)
    sessionIDTextBox.set_text("Enter your Session ID")
    global connectButton
    connectButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((screenSurfcace.get_width() / 2 - 200, 320), (400, 50)),
                                                 text='Conect to Server',
                                                 manager=ui_manager)


def checkForGuiEvents(event, playerOne):
    if event.type == pygame.USEREVENT:
        if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == connectButton:
                playerOne.name = loginTextBox.get_text()
                playerOne.sessionID = sessionIDTextBox.get_text()
                return True
    return False


def startGame():
    gameWindowInitialisation()
    graphicsInitialisation()
    guiInitialisation()
    soundMusic = pygame.mixer.Sound('mechanoid.wav')
    soundMusic.play(-1)
    soundMusic.set_volume(0.3)

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

    # Variablen zum Start
    playerTurn = True
    moveMode = True
    orders = []
    hoverTile = None
    playerOne = player.Player("Lars", "1234")

    print("starte GUI-Credential Loop")
    while True:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            flag = checkForGuiEvents(event, playerOne)
            if flag:
                break
            ui_manager.process_events(event)
        renderGUI(time_delta)
        pygame.display.flip()
        if flag:
            break


    print("starte Gameloop")

    # Host oder nicht?
    host = True  # ÄNDERN FÜR SPIELER 2 (False)
    playerOneTurn = True
    twoLocalPlayers = True  # ÄNDERN FÜR ONLINE (False)
    twoLocalPlayersPlayerOne = True
    # online?
    if not twoLocalPlayers:
        sv = Client("pkuebler.de", 3210)
        sv.connect(playerOne.name)
        sv.join(playerOne.sessionID)
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
                        if data["payload"]["name"] != playerOne.name:
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
                        terrainMap = initializeGame.createMapWithObjFromJson(jsonTerrMap, MAPSIZE)[0]
                        objectMap, playerOneRobot, playerTwoRobot = initializeGame.createMapWithObjFromJson(
                            jsonObjMap, MAPSIZE)
                        print("Karten und GameStartedEvt empfangen")
                        waitingForPlayerOne = False
                    else:
                        print("kein GameStartedEvt")
                        print(data)
                time.sleep(1)
    # offline
    else:
        terrainMap, objectMap, playerOneRobot, playerTwoRobot = initializeGame.initGame(MAPSIZE)
    # GameLoop
    while True:
        time_delta = clock.tick(60) / 1000.0

        #aktiver Roboter
        playerRobot = gameLogic.returnActivePlayer(playerTurn, twoLocalPlayersPlayerOne, playerOneRobot, playerTwoRobot, host, twoLocalPlayers)
        mapRenderer.setCurrentRobot(playerRobot)
        #events abarbeiten
        for event in pygame.event.get():
            #tile unter der Maus
            if event.type == MOUSEMOTION:
                tile = tileOnPos(event.pos[0], event.pos[1], terrainMap)
                if tile != None:
                    mapRenderer.setCurrentHover(tile)
                    hoverTile = tile
                    #print(("hit", tile.x, tile.y))
                else:
                    mapRenderer.setCurrentHover(None)
                    hoverTile = None

            # Aktion auswerten
            playerTurn, moveMode, order = gameLogic.handleEvents(event, playerTurn, moveMode, twoLocalPlayersPlayerOne,
                                                                 playerOneRobot, playerTwoRobot, terrainMap,
                                                                 objectMap, hoverTile, host, twoLocalPlayers)
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
                            if o["player"] != playerOne.name:
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

        mapRenderer.draw(screenSurfcace, time_delta, terrainMap, objectMap)
        pygame.display.flip()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    startGame()  # hier steckt die GameLoop drin