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
                if event.key == pygame.K_UP:
                    if (playerOne and playerOneRobot.y-1 >= 0 and playerOneRobot.steps > 0):
                        if objectMap[playerOneRobot.x][playerOneRobot.y-1] == None:
                            order = playerOneRobot.move(playerOneRobot.x, playerOneRobot.y-1, terrainMap, objectMap)
                            visualize(terrainMap, objectMap)
                    elif (not playerOne and playerTwoRobot.y-1 >= 0):
                        pass
                if event.key == pygame.K_DOWN:
                    if (playerOne and playerOneRobot.y+1 < SIZE and playerOneRobot.steps > 0):
                        if objectMap[playerOneRobot.x][playerOneRobot.y+1] == None:
                            order = playerOneRobot.move(playerOneRobot.x, playerOneRobot.y+1, terrainMap, objectMap)
                            visualize(terrainMap, objectMap)
                    elif (not playerOne and playerTwoRobot.y+1 >= 0):
                        pass
    #NUR ZUM TESTEN - SPAETER AUFRUF NUR AUS MAIN
    if order != None:
        orders = [order]
        executeOrder(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot)
        order = None
        orders = None
        playerOneRobot.initNewRound()
    return playerTurn, moveMode, order

def executeOrder(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot):
    #nicht vergessen: beide Spieler gehen aufs gleiche feld
    for order in orders:
        if order["ordertype"] == "move":
            if order["player_nr"] == 1:
                print("moving")
                playerOneRobot.executeMove(terrainMap, objectMap)
    visualize(terrainMap, objectMap)

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