package chain

import (
	"crypto/sha256"
	"encoding/hex"

	"pentrius-pulseagent/internal/types"
)

// Hasher maintains the rolling SHA-256 chain state.
type Hasher struct {
	previousHash string
}

// New creates a Hasher. Pass empty string for genesis (all-zeros) hash.
func New(seed string) *Hasher {
	if seed == "" {
		seed = "0000000000000000000000000000000000000000000000000000000000000000"
	}
	return &Hasher{previousHash: seed}
}

// ComputeHash implements Equation (1): H_i = SHA256(id_i || ts_i || cmd_i || out_i || H_{i-1})
// pentrius-pulseagent/internal/chain/chain.go:35-53
func (h *Hasher) ComputeHash(event *types.PulseAgentEvent) string {
	input := event.EventID + event.Timestamp

	if event.Command != nil {
		input += event.Command.Raw
	}
	if event.Output != nil {
		input += event.Output.Stdout
	}
	input += h.previousHash

	hash := sha256.Sum256([]byte(input))
	hexHash := hex.EncodeToString(hash[:])
	h.previousHash = hexHash
	return hexHash
}

// PreviousHash returns the current chain tip (persisted across restarts).
func (h *Hasher) PreviousHash() string { return h.previousHash }
