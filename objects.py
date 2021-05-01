#!/usr/bin/env python3

class Object:

    def __init__(self, name, obtype, health, x, y, player=0, steps=0):
        self.name = name
        self.obtype = obtype
        self.health = health
        self.x = x
        self.y = y
        self.player = player
        self.steps = steps
        self.maxSteps = steps
        self.targetX = None
        self.targetY = None
        self.order = None

    def initNewRound(self):
        steps = maxSteps

    def onDeath(self):
        pass

    def shoot(self, targetX, targetY, terrainMap, objectMap):
        pass

    def melee(self, targetX, targetY, terrainMap, objectMap):
        pass

    def move(self, targetX, targetY, terrainMap, objectMap):
        print("move")
        self.targetX = targetX
        self.targetY = targetY
        self.steps -= 1
        return {"ordertype": "move", "x": self.targetX, "y": self.targetY, "player_nr": self.player}

    def executeMove(self, terrainMap, objectMap):
        #von alter stelle wegbewegen
        objectMap[x][y] = None
        self.x = targetX
        self.y = targetY
        #auf neue stelle in karte setzen
        objectMap[x][y] = self
        #ziele zurücksetzen
        self.targetX = None
        self.targetY = None


    def printInfos(self):
        print(self.name + "," + str(self.health))