#!/usr/bin/env python3

class Object:

    def __init__(self, name, obtype, health, x, y, player=None):
        self.name = name
        self.obtype = obtype
        self.health = health
        self.x = x
        self.y = y
        self.player = player

    def onDeath(self):
        pass

    def shoot(self, targetX, targetY, terrainMap, objectMap):
        pass

    def melee(self, targetX, targetY, terrainMap, objectMap):
        pass

    def move(self, targetX, targetY, terrainMap, objectMap):
        pass

    def printInfos(self):
        print(self.name + "," + str(self.health))