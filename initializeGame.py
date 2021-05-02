#!/usr/bin/env python3

import random
from objects import *


def initGame(SIZE):
    terrainMap = createTerrainMap(SIZE)
    objectMap, pl1, pl2 = createObjectMap(SIZE)
    return terrainMap, objectMap, pl1, pl2


def createTerrainMap(SIZE):
    """list2d mit Terrain-Tiles initialisieren"""
    list2d = []
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            # an dieser Stelle Zufallsgenerator fuer Karten
            tileinfo = Object("grass", "grass", 1, x, y)
            ylist.append(tileinfo)
        list2d.append(ylist)
    return list2d


def createObjectMap(SIZE):
    """list2d mit Object-Tiles initialisieren"""
    list2d = []
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            # an dieser Stelle Zufallsgenerator fuer Objekte (außer Spieler)=
            if random.randint(0, 4) == 0:
                tileinfo = Object("wall", "wall", 5, x, y)
            else:
                tileinfo = None
            ylist.append(tileinfo)
        list2d.append(ylist)
    # remove blocking objects
    list2d = removeBrockingObjects(list2d, SIZE)
    # start der 2 spieler
    list2d[4][1] = Object("Roboter von Spieler 1", "robot1", 5, 4, 1, 1, 1)
    list2d[5][8] = Object("Roboter von Spieler 2", "robot1", 5, 5, 8, 2, 1)
    return list2d, list2d[4][1], list2d[5][8]

def returnObjMapWithDicts(objectMap, SIZE):
    list2d=[]
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            if objectMap[x][y] != None:
                ylist.append(objectMap[x][y].jsonMe())
            else:
                ylist.append(None)
        list2d.append(ylist)
    return list2d

def createMapWithObjFromJson(jsonmap, SIZE):
    list2d=[]
    playerOne = None
    playerTwo = None
    for x in range(SIZE):
        ylist = []
        for y in range(SIZE):
            if jsonmap[x][y] != None:
                obj = jsonmap[x][y]
                tileinfo = Object(obj["name"], obj["obtype"], obj["health"], obj["x"], obj["y"], obj["player"], obj["steps"])
                if tileinfo.player == 1:
                    playerOne = tileinfo
                elif tileinfo.player == 2:
                    playerTwo = tileinfo
            else:
                tileinfo = None
            ylist.append(tileinfo)
        list2d.append(ylist)
    return list2d, playerOne, playerTwo


def removeBrockingObjects(list2d, size):
    list2dWorker = []
    for x in range(size):
        yList = []
        for y in range(size):
            if list2d[x][y] is not None:
                yList.append(0)
            else:
                yList.append(None)
        list2dWorker.append(yList)
    list2d[4][1] = None
    list2d[5][8] = None
    noneX, noneY = findFirstNone(list2dWorker, size)
    if noneX == noneY and noneY == size:
        # error
        return list2d
    done = False
    color = 0
    while not done:  # floodFill groups until no Nones left
        color = color+1
        floodFill(list2dWorker, color, noneX, noneY, size)
        noneX, noneY = findFirstNone(list2dWorker, size)
        if noneX == noneY and noneY == size:
            done = True

    if color > 1:
        list2d[random.randint(0, size-1)][random.randint(0, size-1)] = None
        list2d = removeBrockingObjects(list2d, size)

    return list2d


def findFirstNone(list2d, size):
    for x in range(size):
        for y in range(size):
            if list2d[x][y] is None:
                return x, y
    return size, size


def floodFill(array, color, x, y, size):
    original = array[x][y]
    array[x][y] = color
    if x > 0 and array[x-1][y] is original:
        array = floodFill(array, color, x-1, y, size)
    if x < size-1 and array[x+1][y] is original:
        array = floodFill(array, color, x+1, y, size)
    if y > 0 and array[x][y-1] is original:
        array = floodFill(array, color, x, y-1, size)
    if y < size-1 and array[x][y+1] is original:
        array = floodFill(array, color, x, y+1, size)
    return array