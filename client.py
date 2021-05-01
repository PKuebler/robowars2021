#!/usr/bin/env python3

import socket
import json
import select

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

    def write(self, data):
        if self.socket == None:
            self.reconnect()
        self.socket.sendall(bytes(data+'\n',encoding="utf-8"))
    
    def connect(self, name):
        msg = {"type": "ConnectCmd", "payload": {"name": name}}
        client.write(json.dumps(msg))

    def join(self, code):
        msg = {"type": "JoinCmd", "payload": {"code": code}}
        client.write(json.dumps(msg))

    def leave(self):
        msg = {"type": "LeaveCmd", "payload": {}}
        client.write(json.dumps(msg))

    def startGame(self, m, roundSeconds):
        msg = {"type": "StartGameCmd", "payload": {"map": m, "round_seconds": roundSeconds}}
        client.write(json.dumps(msg))

    def command(self, commandType, targetX, targetY):
        msg = {"type": "CommandCmd", "payload": {"type": "move", "target_x": targetX, "target_y": targety}}
        client.write(json.dumps(msg))

client = Client("localhost", 3000)
client.connect("Philipp")

client.read()
client.read()
client.read()
