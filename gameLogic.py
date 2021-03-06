#!/usr/bin/env python3

import pygame
import sys

SIZE = 10

def returnActivePlayer(playerTurn, twoLocalPlayersPlayerOne, playerOneRobot, playerTwoRobot, host, twoLocalPlayers):
    if playerTurn:
        #lokal:
        if twoLocalPlayers:
            if twoLocalPlayersPlayerOne:
                return playerOneRobot
            else:
                return playerTwoRobot
        #internet
        else:
            if host:
                return playerOneRobot
            else:
                return playerTwoRobot
    return None

def isMoveValid(playerTurn, moveMode, hoverTile, playerRobot, objectMap):
    if not moveMode or not playerTurn or hoverTile == None or playerRobot == None:
        return False
    moveDist = abs(hoverTile.x - playerRobot.x) + abs(hoverTile.y - playerRobot.y)
    if moveDist > 0 and moveDist <= playerRobot.steps and objectMap[hoverTile.x][hoverTile.y] == None:
        return True
    return False

def move(playerRobot, offset_x, offset_y, terrainMap, objectMap):
    #Für Tastatursteuerung
    order = None
    #noch schritte?
    if playerRobot.steps > 0:
        target_x = playerRobot.x + offset_x
        target_y = playerRobot.y + offset_y
        #feld auf Spielfeld?
        if target_x >= 0 and target_x < SIZE and target_y >= 0 and target_y < SIZE:
            #feld frei?
            if objectMap[target_x][target_y] == None:
                #order erzeugen
                order = playerRobot.move(target_x, target_y, terrainMap, objectMap)
    return order

def changeAim(playerRobot, offset_x, offset_y, terrainMap, objectMap):
    #Für Tastatursteuerung
    target_x = playerRobot.shootAtX + offset_x
    target_y = playerRobot.shootAtY + offset_y
    #feld auf Spielfeld?
    if target_x >= 0 and target_x < SIZE and target_y >= 0 and target_y < SIZE:
        playerRobot.setTarget(target_x, target_y)

def handleEvents(event, playerTurn, moveMode, playerOne, playerOneRobot, playerTwoRobot, terrainMap, objectMap, hoverTile, host, twoLocalPlayers):
    order = None
    withinWalkingDistance = False

    if event.type == pygame.QUIT:
        sys.exit()

    #spielfigur und cursor festlegen
    if playerTurn:
        playerRobot = returnActivePlayer(playerTurn, playerOne, playerOneRobot, playerTwoRobot, host, twoLocalPlayers)
        """if moveMode and hoverTile != None:
            moveDist = abs(hoverTile.x - playerRobot.x) + abs(hoverTile.y - playerRobot.y)
            if moveDist > 0 and moveDist <= playerRobot.steps and objectMap[hoverTile.x][hoverTile.y] == None:
                withinWalkingDistance = True
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)"""
        #bewegungscursor und walkingDistance
        if moveMode and isMoveValid(playerTurn, moveMode, hoverTile, playerRobot, objectMap):
            withinWalkingDistance = True
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif moveMode:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
    else:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_NO)
        return playerTurn, moveMode, order

    #Maussteuerung
    if event.type == pygame.MOUSEBUTTONUP:
        if hoverTile != None:
            if moveMode and withinWalkingDistance:
                order = playerRobot.mouseMove(hoverTile.x, hoverTile.y, objectMap)
                print(order)
            else:
                order = {"ordertype": "action_1", "x": hoverTile.x, "y": hoverTile.y, "player_nr": playerRobot.player}
        #print(bu.key)

    #Tastatur auswerten
    elif event.type == pygame.KEYUP:
        ##aktiver roboter
        #if playerOne:
        #    playerRobot = playerOneRobot
        #else:
        #    playerRobot = playerTwoRobot
        #modus umschalten
        if event.key == pygame.K_SPACE:
            moveMode = not moveMode
            if not moveMode:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
            print("movemode: " + str(moveMode))
        #feuerbefehl
        elif event.key == pygame.K_RETURN and not moveMode:
            if playerRobot.shootAtX != playerRobot.x or playerRobot.shootAtY != playerRobot.y:
                print("shoot (action_1)")
                order = {"ordertype": "action_1", "x": playerRobot.shootAtX, "y": playerRobot.shootAtY, "player_nr": playerRobot.player}
        #feuer action 2 aoe
        elif event.key == pygame.K_BACKSPACE and not moveMode:
            if playerRobot.shootAtX != playerRobot.x or playerRobot.shootAtY != playerRobot.y:
                print("shoot (action_2)")
                order = {"ordertype": "action_2", "x": playerRobot.shootAtX, "y": playerRobot.shootAtY, "player_nr": playerRobot.player}
        #bewegen
        else:
            #oben
            input_valid = False
            if event.key == pygame.K_UP:
                #spieler 1 + nicht am rand + nicht schritte verbraucht
                offset_x = 0
                offset_y = -1
                input_valid = True
            #unten
            elif event.key == pygame.K_DOWN:
                offset_x = 0
                offset_y = 1
                input_valid = True
            #links
            elif event.key == pygame.K_LEFT:
                offset_x = -1
                offset_y = 0
                input_valid = True
            #rechts
            elif event.key == pygame.K_RIGHT:
                offset_x = 1
                offset_y = 0
                input_valid = True
            if input_valid:
                if moveMode:
                    order = move(playerRobot, offset_x, offset_y, terrainMap, objectMap)
                else:
                    changeAim(playerRobot, offset_x, offset_y, terrainMap, objectMap)
    return playerTurn, moveMode, order

def executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot):
    print("execute:")
    print(orders)

    #beide Spieler gehen aufs gleiche feld
    if orders[0]["x"] == orders[1]["x"] and orders[0]["y"] == orders[1]["y"] and orders[0]["ordertype"] == "move" and orders[1]["ordertype"] == "move":
        playerOneRobot.changeHealth(2, terrainMap, objectMap)
        playerTwoRobot.changeHealth(2, terrainMap, objectMap)
        #beenden, da kollision
        playerOneRobot.initNewRound()
        playerTwoRobot.initNewRound()
        return

    #Bewegungsbefehle zuerst
    for order in orders:
        #roboter wählen
        if order["player_nr"] == 1:
            playerRobot = playerOneRobot
        else:
            playerRobot = playerTwoRobot
        #ordertyp
        #bewegung
        if order["ordertype"] == "move":
            print("moving")
            #pygame.mixer.music.load("204431__jaraxe__robot-walk.ogg")
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("204431__jaraxe__robot-walk.wav"))
            #bewegung ausführen über objekt
            playerRobot.executeMove(terrainMap, objectMap, order["x"], order["y"])

    #dann Beschuss
    for order in orders:
        #roboter wählen
        if order["player_nr"] == 1:
            playerRobot = playerOneRobot
        else:
            playerRobot = playerTwoRobot
        #action_1
        if order["ordertype"] == "action_1":
            print("action_1")
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("517939__slopemstr__laser-artillery-sound-effect.wav"))
            playerRobot.action_1(order["x"], order["y"], terrainMap, objectMap)
        #action2
        elif order["ordertype"] == "action_2":
            print("action_2")
            playerRobot.action_2(order["x"], order["y"], terrainMap, objectMap)
            pygame.mixer.Channel(3).play(pygame.mixer.Sound("399303__deleted-user-5405837__explosion-012.wav"))
    #Steps zurücksetzen
    playerOneRobot.initNewRound()
    playerTwoRobot.initNewRound()


def checkIfOver(playerOneRobot, playerTwoRobot):
    if playerOneRobot.health <= 0 and playerTwoRobot.health <= 0:
        print("UNENTSCHIEDEN")
        return True
    elif playerOneRobot.health <= 0:
        print("SPIELER 2 GEWINNT!")
        return True
    elif playerTwoRobot.health <= 0:
        print("SPIELER 1 GEWINNT!")
        return True
    print("Weiter geht's...")
    return False

def visualize(terrainMap, objectMap):
    print('**********')
    for i in range(SIZE):
        for j in range(SIZE):
            if objectMap[i][j] != None:
                if objectMap[i][j].obtype == "wall":
                    print('w', end='')
                elif objectMap[i][j].obtype == "robot1":
                    print('r', end='')
            else:
                print('.', end='')
        print()
    print('**********')