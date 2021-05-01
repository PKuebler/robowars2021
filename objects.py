#!/usr/bin/env python3
import pygame


class Object:
    if __name__ != '__main__':
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
            self.image = None
            self.rect = None
            self.tileWidth = 64
            self.tileHeight = 64

        def setImage(self, img):
            self.image = pygame.image.load(img).convert_alpha()
            self.image.convert()
            self.setRect()

        def setRect(self):
            self.rect = self.image.get_rect()
            self.rect.center = self.image.get_width() / 2, self.image.get_height() / 2

        def moveRect(self, x, y):
            self.rect.move(x, y)

        def initNewRound(self):
            self.steps = self.maxSteps
            self.targetX = None
            self.targetY = None
            self.shootAtX = self.x
            self.shootAtY = self.y

        def changeHealth(self, damage):
            self.health -= damage
            print("my health: " + str(self.health))
            if self.health <= 0:
                self.onDeath()

        def onDeath(self):
            print("aaaargh")

        def setTarget(self, shootAtX, shootAtY):
            self.shootAtX = shootAtX
            self.shootAtY = shootAtY
            print("Aiming @ " + str(self.shootAtX) + "," + str(self.shootAtY))

        def action_1(self, targetX, targetY, terrainMap, objectMap):
            #basic shooting attack
            BASE_DMG = 5
            if objectMap[targetX][targetY] != None:
                objectMap[targetX][targetY].changeHealth(BASE_DMG)
                print("treffer bei " + objectMap[targetX][targetY].name)

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

        def executeMove(self, terrainMap, objectMap, targetX, targetY):
            self.printInfos()
            #von alter stelle wegbewegen
            objectMap[self.x][self.y] = None
            self.x = targetX
            self.y = targetY
            #auf neue stelle in karte setzen
            objectMap[self.x][self.y] = self
            #ziele zurücksetzen
            self.printInfos()

        def printInfos(self):
            print(self.name + "," + str(self.health) + "@" + str(self.x) + "," + str(self.y))

        def jsonMe(self):
            return {"name": self.name, "obtype": self.obtype, "health": self.health, "x": self.x, "y": self.y,
                    "player": self.player, "steps": self.steps}