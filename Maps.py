#!/usr/bin/env python3

WIDTH = 10
HEIGHT = 10


def createMap():
    """list2d mit Tiles initialisieren"""
    list2d = []
    for x in range(WIDTH):
        ylist = []
        for y in range(HEIGHT):
            #an dieser Stelle Zufallsgenerator fuer Karten
            tileinfo = {"type": "grass"}
            ylist.append(tileinfo)
        list2d.append(ylist)
    return list2d
