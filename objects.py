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
        self.shootAtX = self.x
        self.shootAtY = self.y
        self.order = None

    def initNewRound(self):
        self.steps = self.maxSteps
        self.targetX = None
        self.targetY = None
        self.shootAtX = self.x
        self.shootAtY = self.y

    def onDeath(self):
        pass

    def setTarget(self, shootAtX, shootAtY):
        self.shootAtX = shootAtX
        self.shootAtY = shootAtY
        print("Aiming @ " + str(self.shootAtX) + "," + str(self.shootAtX))

    def shoot(self, targetX, targetY, terrainMap, objectMap):
        pass

    def melee(self, targetX, targetY, terrainMap, objectMap):
        pass

    def move(self, targetX, targetY, terrainMap, objectMap):
        print("move")
        self.printInfos()
        self.targetX = targetX
        self.targetY = targetY
        self.steps -= 1
        return {"ordertype": "move", "x": self.targetX, "y": self.targetY, "player_nr": self.player}

    def executeMove(self, terrainMap, objectMap):
        self.printInfos()
        #von alter stelle wegbewegen
        objectMap[self.x][self.y] = None
        self.x = self.targetX
        self.y = self.targetY
        #auf neue stelle in karte setzen
        objectMap[self.x][self.y] = self
        #ziele zurücksetzen
        self.printInfos()


    def printInfos(self):
        print(self.name + "," + str(self.health) + "@" + str(self.x) + "," + str(self.y))

    def jsonMe(self):
        return {"name": self.name, "obtype": self.obtype, "health": self.health, "x": self.x, "y": self.y, "player": self.player, "steps": self.steps}