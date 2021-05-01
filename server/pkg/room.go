package pkg

import (
	"encoding/json"

	"github.com/sirupsen/logrus"
)

const DefaultRoomName = "lobby"

type Room struct {
	name         string
	clients      map[Client]bool
	commands     map[Client]CommandCmd
	log          *logrus.Entry
	roundSeconds int
}

func NewRoom(name string, log *logrus.Entry) *Room {
	log = log.WithField("component", "room")
	log = log.WithField("room", name)

	log.Info("Create room")

	return &Room{
		name:         name,
		clients:      map[Client]bool{},
		commands:     map[Client]CommandCmd{},
		log:          log,
		roundSeconds: 60,
	}
}

func (r *Room) Join(client Client) {
	r.log.WithField("name", client.Name()).Info("Join room")
	if _, ok := r.clients[client]; ok {
		// already joined
		return
	}

	// leave current room
	client.LeaveRoom()
	client.SetRoom(r)

	r.clients[client] = true

	payload, _ := json.Marshal(PlayerConnectEvt{
		Name: client.Name(),
	})

	r.Broadcast("PlayerConnectEvt", payload)
}

func (r *Room) Start(client Client, cmd *StartGameCmd) {
	players := []string{}
	for c := range r.clients {
		players = append(players, c.Name())
	}

	r.roundSeconds = cmd.RoundSeconds

	payload, _ := json.Marshal(GameStartedEvt{
		Map:          cmd.Map,
		RoundSeconds: cmd.RoundSeconds,
		Players:      players,
	})

	r.Broadcast("GameStartedEvt", payload)
}

func (r *Room) Command(client Client, cmd *CommandCmd) {
	if _, ok := r.commands[client]; ok {
		return
	}

	r.commands[client] = *cmd

	r.Finish()
}

func (r *Room) Finish() {
	for client := range r.clients {
		if _, ok := r.commands[client]; !ok {
			// waiting for commands
			return
		}
	}

	r.finishRound()
}

func (r *Room) finishRound() {
	// copy commands
	cmds := r.commands
	r.commands = map[Client]CommandCmd{}

	// create events
	events := []CommandEvt{}
	for client, cmd := range cmds {
		events = append(events, CommandEvt{
			Player:  client.Name(),
			Type:    cmd.Type,
			TargetX: cmd.TargetX,
			TargetY: cmd.TargetY,
		})
	}

	round := RoundEndEvt{
		Commands: events,
	}

	payload, _ := json.Marshal(round)
	r.Broadcast("RoundEndEvt", payload)
}

func (r *Room) Broadcast(payloadType string, payload json.RawMessage) {
	msg := NewMessage(payloadType, payload)

	for client := range r.clients {
		client.Write(*msg)
	}
}

func (r *Room) Leave(client Client, cmd *LeaveCmd) {
	delete(r.clients, client)
	delete(r.commands, client)

	payload, _ := json.Marshal(PlayerDisconnectEvt{
		Name: client.Name(),
	})

	r.Broadcast("PlayerDisconnectEvt", payload)
}
