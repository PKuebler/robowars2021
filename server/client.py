#!/usr/bin/env python3

import socket
import json

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 3000        # The port used by the server

m = {"type": "ConnectCmd", "payload": {"name": "Philipp"}}

# Commands
# ConnectCmd {"type": "ConnectCmd", "payload": {"name": "Philipp"}}
# JoinCmd {"type": "JoinCmd", "payload": {"code": "room code"}}
# LeaveCmd {"type": "LeaveCmd", "payload": {}}
# StartGameCmd {"type": "StartGameCmd", "payload": {"map": {}, "round_seconds": 60}}
# CommandCmd {"type": "CommandCmd", "payload": {"type": "move", "target_x": 10, "target_y": 5}}

# Events from Server
# PlayerDisconnectEvt {"type": "PlayerDisconnectEvt", "payload": {"name": "player name"}}
# PlayerConnectEvt {"type": "PlayerConnectEvt", "payload": {"name": "player name"}}
# GameStartedEvt {"type": "GameStartedEvt", "payload": {"map": {}, "round_seconds": 60, "players": ["player name 1", "player name 2"]}}
# RoundEndEvt {"type": "RoundEndEvt", "payload": {"commands": [{"player": "player name 1", "type": "move", "target_x": 4, "target_y": 20}]}}

data = json.dumps(m)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    s.sendall(bytes(data+'\n',encoding="utf-8"))
    data = s.recv(1024)

print('Received', repr(data))