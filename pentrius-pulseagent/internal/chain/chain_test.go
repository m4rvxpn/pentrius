package chain

import (
	"crypto/sha256"
	"fmt"
	"testing"

	"pentrius-pulseagent/internal/types"
	"github.com/stretchr/testify/assert"
)

// pentrius-pulseagent/internal/chain/chain_test.go
func TestChainContinuityAcrossRestart(t *testing.T) {
	h1 := New("") // empty string -> genesis (all-zeros) hash
	evt1 := &types.PulseAgentEvent{
		EventID: "e1", Timestamp: "2025-01-01T00:00:00Z",
		Command: &types.CommandBlock{Raw: "nmap -sV target"},
		Output:  &types.OutputBlock{Stdout: "22/tcp open ssh"},
	}
	hash1 := h1.ComputeHash(evt1)
	savedHash := h1.PreviousHash() // simulate persisting to credentials file

	// New session: restore from saved hash
	h2 := New(savedHash)
	evt2 := &types.PulseAgentEvent{
		EventID: "e2", Timestamp: "2025-01-01T00:01:00Z",
		Command: &types.CommandBlock{Raw: "sqlmap -u http://target"},
		Output:  &types.OutputBlock{Stdout: "[*] testing parameter"},
	}
	hash2 := h2.ComputeHash(evt2)

	// Verify chain is contiguous
	raw := "e2" + "2025-01-01T00:01:00Z" + "sqlmap -u http://target" +
		"[*] testing parameter" + hash1
	expected := fmt.Sprintf("%x", sha256.Sum256([]byte(raw)))
	assert.Equal(t, expected, hash2)
}
