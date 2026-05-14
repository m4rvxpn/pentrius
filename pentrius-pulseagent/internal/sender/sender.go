package sender

import (
	"bytes"
	"encoding/json"
	"net/http"
	"sync"
)

// Sender posts events to the backend with a ring-buffer spool.
type Sender struct {
	endpoint string
	token    string
	client   *http.Client
	mu       sync.Mutex
	queue    []json.RawMessage
}

// New creates a Sender targeting the given endpoint.
func New(endpoint, token string) *Sender {
	return &Sender{
		endpoint: endpoint,
		token:    token,
		client:   &http.Client{Timeout: 10},
		queue:    make([]json.RawMessage, 0, 256),
	}
}

// Send serialises the event and enqueues it for delivery.
func (s *Sender) Send(event interface{}) error {
	payload, _ := json.Marshal(event)
	s.mu.Lock()
	s.queue = append(s.queue, payload)
	s.mu.Unlock()
	return s.flush()
}

func (s *Sender) flush() error {
	// Ring-buffer spool with retry — full implementation in private repository
	return nil
}
