package pkg

import (
	"bufio"
	"net"

	"github.com/sirupsen/logrus"
)

type Client interface {
	Name() string
	Room() *Room
	Write(msg Message)
	SetRoom(room *Room)
	LeaveRoom()
	Close()
}

type TcpClient struct {
	name string

	hub         *Hub
	currentRoom *Room

	log        *logrus.Entry
	reader     *bufio.Reader
	connection net.Conn
	outgoing   chan Message
}

func NewTcpClient(conn net.Conn, log *logrus.Entry, hub *Hub) *TcpClient {
	client := &TcpClient{
		currentRoom: nil,

		log:        log,
		reader:     bufio.NewReader(conn),
		connection: conn,
		outgoing:   make(chan Message),
	}

	if !client.handshake() {
		return nil
	}

	go client.read()
	go client.write()

	return client
}

func (c *TcpClient) handshake() bool {
	for {
		n, err := c.reader.ReadString('\n')
		if err != nil {
			c.Close()
			return false
		}

		if n == "" {
			continue
		}

		payload, payloadType, ok := Unmarshal([]byte(n))
		if ok {
			c.Close()
			return false
		}

		if payloadType != "connect" {
			c.Close()
			return false
		}

		connectCmd := payload.(ConnectCmd)

		c.name = connectCmd.Name
		c.log = c.log.WithField("name", c.name)
		break
	}

	c.log.Info("client handshake correct")
	return true
}

// read from client
func (c *TcpClient) read() {
	for {
		n, err := c.reader.ReadString('\n')
		if err != nil {
			c.Close()
			return
		}

		if n == "" {
			continue
		}

		payload, payloadType, ok := Unmarshal([]byte(n))
		if !ok {
			c.Close()
			return
		}

		c.log.Debug("client send %s", payloadType)

		switch payloadType {
		case "JoinCmd":
			c.hub.Join(c, payload.(*JoinCmd))
		case "LeaveCmd":
			if c.currentRoom == nil {
				continue
			}
			c.currentRoom.Leave(c, payload.(*LeaveCmd))
		case "StartGameCmd":
			if c.currentRoom == nil {
				continue
			}
			c.currentRoom.Start(c, payload.(*StartGameCmd))
		case "CommandCmd":
			if c.currentRoom == nil {
				continue
			}
			c.currentRoom.Command(c, payload.(*CommandCmd))
		default:
			c.Close()
			return
		}
	}
}

// write to client
func (c *TcpClient) write() {
	for {
		msg := <-c.outgoing
		c.connection.Write(msg.Marshal())
	}
}

// Write to client
func (c *TcpClient) Write(msg Message) {
	c.outgoing <- msg
}

func (c *TcpClient) Close() {
	c.LeaveRoom()
	c.log.Info("client connection closed")
	c.connection.Close()
}

func (c *TcpClient) SetRoom(room *Room) {
	c.currentRoom = room
}

func (c *TcpClient) Room() *Room {
	return c.currentRoom
}

func (c *TcpClient) LeaveRoom() {
	if c.currentRoom == nil {
		return
	}

	c.currentRoom.Leave(c, nil)
	c.currentRoom = nil
}

func (c *TcpClient) Name() string {
	return c.name
}
