package types

// PulseAgentEvent represents a single captured command event.
type PulseAgentEvent struct {
	EventID   string        `json:"event_id"`
	Timestamp string        `json:"timestamp"`
	Command   *CommandBlock `json:"command,omitempty"`
	Output    *OutputBlock  `json:"output,omitempty"`
	AgentID   string        `json:"agent_id"`
	ScopeID   string        `json:"scope_id"`
}

// CommandBlock holds the raw command and parsed metadata.
type CommandBlock struct {
	Raw     string `json:"raw"`
	Tool    string `json:"tool"`
	PID     int    `json:"pid"`
	PPID    int    `json:"ppid"`
	CWD     string `json:"cwd"`
	User    string `json:"user"`
	Shell   string `json:"shell"`
}

// OutputBlock holds captured stdout/stderr previews.
type OutputBlock struct {
	Stdout string `json:"stdout"`
	Stderr string `json:"stderr"`
}
