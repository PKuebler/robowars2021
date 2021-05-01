#!/usr/bin/env python3

import pygame

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
                if event.key == pygame.K_UP:
                    if (playerOne and playerOneRobot.y-1 >= 0 and playerOneRobot.steps > 0):
                        if objectMap[playerOneRobot.x][playerOneRobot.y-1] == None:
                            order = playerOneRobot.move(playerOneRobot.x, playerOneRobot.y-1, terrainMap, objectMap)
                            if playerOneRobot.steps == 0:
                                playerTurn = not playerTurn
                    elif (not playerOne and playerTwoRobot.y-1 >= 0):
                        pass
    #NUR ZUM TESTEN - SPAETER AUFRUF NUR AUS MAIN
    if order != None:
        executeOrder(order)
    return playerTurn, moveMode, order

def executeOrder(order):
    #nicht vergessen: beide Spieler gehen aufs gleiche feld
    if order["ordertype"] == "move":
        print("move")