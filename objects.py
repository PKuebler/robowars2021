#!/usr/bin/env python3
import pygame


class Object:
    if __name__ != '__main__':
        def __init__(self, name, obtype, health, x, y, player=0, steps=0):
            self.name = name
            self.obtype = obtype
            self.health = health
            self.maxhealth = health
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

        def changeHealth(self, damage, terrainMap, objectMap):
            self.health -= damage
            print("my health: " + str(self.health))
            if self.health <= 0:
                self.onDeath(terrainMap, objectMap)

        def onDeath(self, terrainMap, objectMap):
            print("aaaargh")
            if self.obtype == "wall":
                objectMap[self.x][self.y] = None

        def setTarget(self, shootAtX, shootAtY):
            self.shootAtX = shootAtX
            self.shootAtY = shootAtY
            print("Aiming @ " + str(self.shootAtX) + "," + str(self.shootAtY))

        def action_1(self, targetX, targetY, terrainMap, objectMap):
            #basic shooting attack
            BASE_DMG = 3
            if objectMap[targetX][targetY] != None:
                print("treffer bei " + objectMap[targetX][targetY].name)
                objectMap[targetX][targetY].changeHealth(BASE_DMG, terrainMap, objectMap)

        def action_2(self, targetX, targetY, terrainMap, objectMap):
            #aoe shooting attack
            BASE_DMG = 1
            for x in range(-1,2):
                for y in range(-1,2):
                    if targetX+x >= 0 and targetY+y >= 0 and targetX+x < 10 and targetY+y < 10:
                        if objectMap[targetX+x][targetY+y] != None:
                            print("treffer bei " + objectMap[targetX+x][targetY+y].name)
                            objectMap[targetX+x][targetY+y].changeHealth(BASE_DMG, terrainMap, objectMap)

        def melee(self, targetX, targetY, terrainMap, objectMap):
            pass

        def mouseMove(self, targetX, targetY, objectMap):
            if objectMap[targetX][targetY] != None:
                print("object map belegt mit ",objectMap[targetX][targetY])
                return None
            if self.steps > 0:
                self.steps -= 1
                return {"ordertype": "move", "x": targetX, "y": targetY, "player_nr": self.player}
            else:
                print("steps", self.steps)
                return None

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