package pkg

import (
	"net"

	"github.com/sirupsen/logrus"
)

type Hub struct {
	log *logrus.Entry

	rooms    map[string]*Room
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
	// exists room
	r, ok := h.rooms[cmd.Code]
	if !ok {
		h.log.Debug("Do nothing, room not exists")
	}

	r.Join(client)
}

func (h *Hub) run() {
	h.rooms[DefaultRoomName] = NewRoom(DefaultRoomName, h.log)

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
