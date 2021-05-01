#!/usr/bin/env python3

import pygame
import sys

SIZE = 10

def handleEvents(event, playerTurn, moveMode, playerOne, playerOneRobot, playerTwoRobot, terrainMap, objectMap):
    order = None
    #Mausklick auswerten
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONUP:
        pass
    #Tastatur auswerten
    elif event.type == pygame.KEYUP:
        #ist der Spieler am Zug?
        if playerTurn:
            #bewegen
            if moveMode:
                #oben
                if event.key == pygame.K_UP:
                    #spieler 1 + nicht am rand + nicht schritte verbraucht
                    if (playerOne and playerOneRobot.y-1 >= 0 and playerOneRobot.steps > 0):
                        #feld frei?
                        if objectMap[playerOneRobot.x][playerOneRobot.y-1] == None:
                            #order erzeugen
                            order = playerOneRobot.move(playerOneRobot.x, playerOneRobot.y-1, terrainMap, objectMap)
                            #ascii
                            visualize(terrainMap, objectMap)
                    #spieler 2
                    elif (not playerOne and playerTwoRobot.y-1 >= 0):
                        pass
                #unten
                if event.key == pygame.K_DOWN:
                    if (playerOne and playerOneRobot.y+1 < SIZE and playerOneRobot.steps > 0):
                        if objectMap[playerOneRobot.x][playerOneRobot.y+1] == None:
                            order = playerOneRobot.move(playerOneRobot.x, playerOneRobot.y+1, terrainMap, objectMap)
                            visualize(terrainMap, objectMap)
                    elif (not playerOne and playerTwoRobot.y+1 >= 0):
                        pass
    #NUR ZUM TESTEN - SPAETER AUFRUF NUR AUS MAIN
    #if order != None:
        #orderliste, weil später immer 2 orders
        #orders = [order]
        #ausführen
        #executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot)
        #zurücksetzen für nächste runde
        #order = None
        #orders = None
        #neue runde initialieren (z.B. Schritte zurücksetzen
        #playerOneRobot.initNewRound()
    return playerTurn, moveMode, order

def executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot):
    #nicht vergessen: beide Spieler gehen aufs gleiche feld
    for order in orders:
        #ordertyp
        if order["ordertype"] == "move":
            #spieler
            if order["player_nr"] == 1:
                print("moving")
                #bewegung ausführen über objekt
                playerOneRobot.executeMove(terrainMap, objectMap)
    visualize(terrainMap, objectMap)
    playerOneRobot.initNewRound()

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