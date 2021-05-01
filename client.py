#!/usr/bin/env python3

import socket
import json
import select

# Commands
# ConnectCmd {"type": "ConnectCmd", "payload": {"name": "Philipp"}}
# JoinCmd {"type": "JoinCmd", "payload": {"code": "room code"}}
# LeaveCmd {"type": "LeaveCmd", "payload": {}}
# StartGameCmd {"type": "StartGameCmd", "payload": {"terrain": {}, "map": {}, "round_seconds": 60}}
# CommandCmd {"type": "CommandCmd", "payload": {"type": "move", "target_x": 10, "target_y": 5}}

# Events from Server
# PlayerDisconnectEvt {"type": "PlayerDisconnectEvt", "payload": {"name": "player name"}}
# PlayerConnectEvt {"type": "PlayerConnectEvt", "payload": {"name": "player name"}}
# GameStartedEvt {"type": "GameStartedEvt", "payload": {"terrain": {}, "map": {}, "round_seconds": 60, "players": ["player name 1", "player name 2"]}}
# RoundEndEvt {"type": "RoundEndEvt", "payload": {"commands": [{"player": "player name 1", "type": "move", "target_x": 4, "target_y": 20}]}}

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def reconnect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def read(self):
        if self.socket == None:
            self.reconnect()

        read_ready, _, _ = select.select([self.socket], [], [], 0.1)

        if len(read_ready) == 0:
            return

        data = self.socket.recv(1024)
        return data

    def write(self, data):
        if self.socket == None:
            self.reconnect()
        self.socket.sendall(bytes(data+'\n',encoding="utf-8"))
        print("sending:")
        print(data)


    def connect(self, name):
        msg = {"type": "ConnectCmd", "payload": {"name": name}}
        self.write(json.dumps(msg))

    def join(self, code):
        msg = {"type": "JoinCmd", "payload": {"code": code}}
        self.write(json.dumps(msg))

    def leave(self):
        msg = {"type": "LeaveCmd", "payload": {}}
        self.write(json.dumps(msg))

    def startGame(self, t, m, roundSeconds):
        msg = {"type": "StartGameCmd", "payload": {"terrain": t, "map": m, "round_seconds": roundSeconds}}
        self.write(json.dumps(msg))

    def command(self, commandType, targetX, targetY):
        msg = {"type": "CommandCmd", "payload": {"type": "move", "target_x": targetX, "target_y": targety}}
        self.write(json.dumps(msg))

'''
client = Client("pkuebler.de", 3210)
client.connect("Philipp")

client.startGame({"x": ...}, 60)
client.comand("move", 20, 11)

while True {
    evt = client.read()
    if evt.type == "GameStartedEvt":
        print(evt.payload.map)
    if evt.type == "RoundEndEvt":
        print(evt.payload.commands)
}
'''