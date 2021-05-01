package main

import (
	"github.com/pkuebler/robowars2021/server/pkg"
	"github.com/sirupsen/logrus"
)

func main() {
	logger := logrus.StandardLogger()
	logger.Level = logrus.TraceLevel
	log := logrus.NewEntry(logger)

	h := pkg.NewHub(log)

	if err := h.Serve(":3000"); err != nil {
		panic(err)
	}
}

// todo:
// - add timer / command logic
// - add disconnect event
// - client -> current room mutex
// - room -> command and clients mutex
// - hub -> rooms
// - delete room if empty
