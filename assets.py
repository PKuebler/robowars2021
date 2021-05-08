#!/usr/bin/env python3

import pygame

class AssetManager:
    def __init__(self):
        self.loadingImages = {}
        self.images = {}
    
    def addImage(self, name, imagePath):
        self.loadingImages[name] = imagePath

    def load(self):
        for name in list(self.loadingImages.keys()): # use a list to delete keys and not break
            path = self.loadingImages[name]
            
            print(f'[Assets] loading image {path} as {name}...')
            
            self.images[name] = pygame.image.load(path).convert_alpha()
            del self.loadingImages[name]
            
            print(f'[Assets] image {path} loaded as {name}')
    
    def getImage(self, name):
        return self.images[name]