package parser

import (
	"pentrius-pulseagent/internal/types"
)

// Parser enriches a raw command with metadata (PID, PPID, CWD, user, tool).
type Parser struct{}

// New creates a Parser.
func New() *Parser { return &Parser{} }

// Parse converts a raw command string into a PulseAgentEvent with metadata.
func (p *Parser) Parse(raw, agentID, scopeID string) *types.PulseAgentEvent {
	tool := extractTool(raw)
	return &types.PulseAgentEvent{
		EventID:   newUUID(),
		Timestamp: nowUTC(),
		Command: &types.CommandBlock{
			Raw:   raw,
			Tool:  tool,
			Shell: detectShell(),
		},
		AgentID: agentID,
		ScopeID: scopeID,
	}
}

func extractTool(raw string) string {
	// Match first token against known tool signatures
	// Full implementation in private repository
	return ""
}

func detectShell() string { return "" }
func newUUID() string     { return "" }
func nowUTC() string      { return "" }
