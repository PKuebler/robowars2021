#!/usr/bin/env python3

import pygame

def handleEvents(event, playerTurn, moveMode, playerOne, playerOneRobot, playerTwoRobot):
    #Mausklick auswerten
    if event.type == pygame.MOUSEBUTTONUP:
        pass
    #Tastatur auswerten
    elif event.type == pygame.KEYUP:
        #bewegen
        if moveMode:
            if event.key == K_UP:

    return playerTurn, moveMode, None