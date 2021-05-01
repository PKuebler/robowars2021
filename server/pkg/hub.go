package pkg

import (
	"net"
	"sync"

	"github.com/sirupsen/logrus"
)

type Hub struct {
	log *logrus.Entry

	rooms    map[string]*Room
	lock     sync.RWMutex
	register chan Client
}

func NewHub(log *logrus.Entry) *Hub {
	return &Hub{
		log: log,

		rooms:    map[string]*Room{},
		register: make(chan Client),
	}
}

func (h *Hub) Join(client Client, cmd *JoinCmd) {
	// is room empty?
	h.lock.Lock()
	defer h.lock.Unlock()

	for roomCode, room := range h.rooms {
		if roomCode == DefaultRoomName {
			continue
		}

		if room.Empty() {
			h.log.WithField("room", roomCode).Info("Close room")
			delete(h.rooms, roomCode)
		}
	}

	// exists room
	r, ok := h.rooms[cmd.Code]
	if !ok {
		h.log.Debug("room not exists")
		r = NewRoom(cmd.Code, h.log)
		h.rooms[cmd.Code] = r
	}

	r.Join(client)
}

func (h *Hub) run() {
	h.rooms[DefaultRoomName] = NewRoom(DefaultRoomName, h.log)

	h.lock.RLock()
	defer h.lock.RUnlock()

	for {
		client := <-h.register
		h.rooms[DefaultRoomName].Join(client)
	}
}

func (h *Hub) Serve(port string) error {
	server, err := net.Listen("tcp", port)
	if err != nil {
		return err
	}

	log := h.log.WithField("component", "hub")

	log.Infof("server started on %s", port)

	// listen new clients
	go func() {
		for {
			conn, err := server.Accept()
			if err != nil {
				h.log.Error(err)
			}

			go func() {
				log.WithField("addr", conn.RemoteAddr()).Infof("New client")
				if c := NewTcpClient(conn, log, h); c != nil {
					h.register <- c
				}
			}()
		}
	}()

	// parse messages
	h.run()

	return nil
}
