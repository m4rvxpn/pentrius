package pipeline

import (
	"pentrius-pulseagent/internal/collector"
	"pentrius-pulseagent/internal/chain"
	"pentrius-pulseagent/internal/parser"
	"pentrius-pulseagent/internal/sender"
)

// Pipeline wires together the four-stage sequential agent pipeline:
// Collector -> Parser -> Hasher -> Sender
type Pipeline struct {
	collector *collector.Collector
	parser    *parser.Parser
	hasher    *chain.Hasher
	sender    *sender.Sender
}

// New creates a Pipeline from the constituent components.
func New(c *collector.Collector, p *parser.Parser, h *chain.Hasher, s *sender.Sender) *Pipeline {
	return &Pipeline{collector: c, parser: p, hasher: h, sender: s}
}

// Run starts the pipeline and processes events until the context is cancelled.
func (p *Pipeline) Run(ctx context.Context) error {
	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		case cmd := <-p.collector.Events():
			event := p.parser.Parse(cmd.Raw, "", "")
			chainHash := p.hasher.ComputeHash(event)
			_ = chainHash
			p.sender.Send(event)
		}
	}
}
