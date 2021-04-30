#!/usr/bin/env python3

import random

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
            #an dieser Stelle Zufallsgenerator fuer Karten
            if random.randint(0,4) == 0:
                tileinfo = {"type": "wall", "health": 10}
            else:
                tileinfo = {"type": None}
            ylist.append(tileinfo)
        list2d.append(ylist)
    return list2d