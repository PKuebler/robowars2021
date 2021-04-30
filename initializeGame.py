#!/usr/bin/env python3

import random
from objects import *

def initGame(SIZE):
    terrainMap = createTerrainMap(SIZE)
    objectMap = createObjectMap(SIZE)
    return terrainMap, objectMap

def createTerrainMap(SIZE):
    """list2d mit Terrain-Tiles initialisieren"""
    list2d=[]
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            #an dieser Stelle Zufallsgenerator fuer Karten
            tileinfo = {"type": "grass"}
            ylist.append(tileinfo)
        list2d.append(ylist)
    return list2d

def createObjectMap(SIZE):
    """list2d mit Object-Tiles initialisieren"""
    list2d=[]
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            #an dieser Stelle Zufallsgenerator fuer Objekte (außer Spieler)=
            if random.randint(0,4) == 0:
                tileinfo = Object("wall", "wall", 5, x, y)
            else:
                tileinfo = None
            ylist.append(tileinfo)
        list2d.append(ylist)
    #start der 2 spieler
    list2d[4][1] = Object("Roboter von Spieler 1", "robot1", 10, 4, 1, 1, 2)
    list2d[5][8] = Object("Roboter von Spieler 2", "robot1", 10, 4, 1, 1, 1)
    return list2d