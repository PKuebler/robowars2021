#!/usr/bin/env python3

class Renderer:
    def __init__(self, assets, backgroundColor):
        self.background = backgroundColor
        self.assets = assets
        self.tileWidth = 80 # 128
        self.tileHeight = 40 # 64
        self.tileWidthHalf = self.tileWidth / 2
        self.tileHeightHalf = self.tileHeight / 1.333
        self.cameraX = 0
        self.cameraY = 0

        # gameObjects to draw ground effects
        self.currentRobot = None
        self.currentHover = None

    def draw(self, screenSurfcace, tileObjects, mapObjects):
        screenSurfcace.fill(self.background)

        self.cameraX = screenSurfcace.get_rect().width / 2
        self.cameraY = 64 #screenSurfcace.get_rect().height / 4 + 64

        self.__drawGroundTiles(screenSurfcace, tileObjects)
        self.__drawMapObjects(screenSurfcace, mapObjects)

    def __drawGroundTiles(self, screenSurfcace, tileObjects):
        if tileObjects == None:
            return

        # tileObjects[x][y] = GameObject
        for x, tiles in enumerate(tileObjects):
            for y, tile in enumerate(tiles):

                iso = self.mapToScreen(x,y)

                tileAsset = "grass"
                if tile.obtype == "water":
                    tileAsset = "water"

                image = self.assets.getImage(tileAsset)

                screenSurfcace.blit(image, (iso[0], iso[1]))  # display the actual tile

        # draw ground effects

        if self.currentHover != None:
            hoverGround = self.assets.getImage("hoverGround")
            screen = self.mapToScreen(self.currentHover.x, self.currentHover.y)
            screenSurfcace.blit(hoverGround, (screen[0], screen[1]))

        if self.currentRobot != None:
            selectedCursor = self.assets.getImage("selectedCursor")
            screen = self.mapToScreen(self.currentRobot.x, self.currentRobot.y)
            screenSurfcace.blit(selectedCursor, (screen[0], screen[1]))

    def __drawMapObjects(self, screenSurfcace, mapObjects):
        if mapObjects == None:
            return

        healthbar = self.assets.getImage("healthbar")
        healthstatus = self.assets.getImage("healthstatus")

        # mapObjects[x][y] = GameObject
        for x, tiles in enumerate(mapObjects):
            for y, tile in enumerate(tiles):
                if tile == None:
                    continue

                iso = self.mapToScreen(tile.x, tile.y)

                if tile.obtype == "robot1":
                    tileAsset = "robot1"
                elif tile.obtype == "robot2":
                    tileAsset = "robot2"
                elif tile.obtype == "wall":
                    tileAsset = "wall"

                # nothing to draw
                if tileAsset == None:
                    continue

                image = self.assets.getImage(tileAsset)

                offsetY = -10 # The object images are {offsetY} higher than the tiles with only ground.
                screenSurfcace.blit(image, (iso[0], iso[1]+offsetY))  # display the actual tile

                # render only, if object not max health.
                if tile.health != tile.maxhealth:
                    screenSurfcace.blit(healthbar, (iso[0]+15, iso[1]+offsetY))
                    for i in range(tile.health):
                        screenSurfcace.blit(healthstatus, (iso[0]+15+3+i*9, iso[1]+offsetY+3))

    def mapToScreen(self, mapX, mapY):
        screenX = (mapX - mapY) * self.tileWidthHalf + self.cameraX
        screenY = (mapX + mapY) * self.tileHeightHalf + self.cameraY

        return (screenX, screenY)

    def screenToMap(self, screenX, screenY):
        screenX = screenX - self.cameraX
        screenY = screenY - self.cameraY

        mapX = (screenX / self.tileWidthHalf + screenY / self.tileHeightHalf) / 2
        mapY = (screenY / self.tileHeightHalf - (screenX / self.tileWidthHalf)) / 2

        return (mapX, mapY)

    def setCurrentRobot(self, gameObject):
        self.currentRobot = gameObject
    
    def setCurrentHover(self, gameObject):
        self.currentHover = gameObject