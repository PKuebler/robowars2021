#!/usr/bin/env python3

import pygame
import sys

SIZE = 10

def move(playerRobot, offset_x, offset_y, terrainMap, objectMap):
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
                #ascii
                visualize(terrainMap, objectMap)
    return order

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
            #aktiver roboter
            if playerOne:
                playerRobot = playerOneRobot
            else:
                playerRobot = playerTwoRobot

            #bewegen
            if moveMode:
                #oben
                if event.key == pygame.K_UP:
                    #spieler 1 + nicht am rand + nicht schritte verbraucht
                    offset_x = 0
                    offset_y = -1
                    order = move(playerRobot, offset_x, offset_y, terrainMap, objectMap)
                #unten
                elif event.key == pygame.K_DOWN:
                    offset_x = 0
                    offset_y = 1
                    order = move(playerRobot, offset_x, offset_y, terrainMap, objectMap)
                #links
                elif event.key == pygame.K_LEFT:
                    offset_x = -1
                    offset_y = 0
                    order = move(playerRobot, offset_x, offset_y, terrainMap, objectMap)
                #rechts
                elif event.key == pygame.K_RIGHT:
                    offset_x = 1
                    offset_y = 0
                    order = move(playerRobot, offset_x, offset_y, terrainMap, objectMap)
    return playerTurn, moveMode, order

def executeOrders(orders, terrainMap, objectMap, playerOneRobot, playerTwoRobot):
    #TODO
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