package pkg

import (
	"encoding/json"
)

// Message wrapper with message type
type Message struct {
	Type    string          `json:"type"`
	Payload json.RawMessage `json:"payload"`
}

func NewMessage(t string, payload json.RawMessage) *Message {
	return &Message{
		Type:    t,
		Payload: payload,
	}
}

func (m *Message) Marshal() []byte {
	msg, _ := json.Marshal(m)

	return msg
}

func Unmarshal(n []byte) (interface{}, string, bool) {
	message := &Message{}
	if err := json.Unmarshal(n, message); err != nil {
		return nil, "", false
	}

	var v interface{}

	switch message.Type {
	case "ConnectCmd":
		v = &ConnectCmd{}
	case "JoinCmd":
		v = &JoinCmd{}
	case "LeaveCmd":
		v = &LeaveCmd{}
	case "StartGameCmd":
		v = &StartGameCmd{}
	case "CommandCmd":
		v = &CommandCmd{}
	default:
		return nil, "", false
	}

	if err := json.Unmarshal(message.Payload, v); err != nil {
		return nil, "", false
	}

	return v, message.Type, true
}

// ConnectCmd send the client name to join the server
type ConnectCmd struct {
	Name string `json:"name"`
}

// PlayerDisconnectEvt notify if a player disconnect from the room
type PlayerDisconnectEvt struct {
	Name string `json:"name"`
}

// PlayerConnectEvt notify if a player connect to the room
type PlayerConnectEvt struct {
	Name string `json:"name"`
}

// JoinCmd send a room code to join
type JoinCmd struct {
	Code string `json:"code"`
}

// LeaveCmd send a leave command
type LeaveCmd struct {
}

// StartGameCmd define the map and round seconds on server
type StartGameCmd struct {
	Map          json.RawMessage `json:"map"`
	RoundSeconds int             `json:"round_seconds"`
}

// GameStartedEvt sned the map and round timer to clients
type GameStartedEvt struct {
	Map          json.RawMessage `json:"map"`
	RoundSeconds int             `json:"round_seconds"`
	Players      []string        `json:"players"`
}

// CommandCmd send a robot command to the server
type CommandCmd struct {
	Type    string `json:"type"`
	TargetX int    `json:"target_x"`
	TargetY int    `json:"target_y"`
}

// CommandEvt round command to move the robot
type CommandEvt struct {
	Player  string `json:"player"`
	Type    string `json:"type"`
	TargetX int    `json:"target_x"`
	TargetY int    `json:"target_y"`
}

// RoundEndEvt send if all clients add a command or round timeout
type RoundEndEvt struct {
	Commands []CommandEvt `json:"commands"`
}
