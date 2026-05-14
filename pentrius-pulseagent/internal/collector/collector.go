package collector

import (
	"bufio"
	"context"
	"os"
	"strings"
	"sync"
	"time"
)

// CommandEvent is emitted by the collector for every new shell command.
type CommandEvent struct {
	Raw      string
	Shell    string
	HistFile string
}

// Collector polls shell history files and emits new commands.
type Collector struct {
	events   chan CommandEvent
	mu       sync.Mutex
	seenCmds map[string]bool
}

// New creates a Collector that sends events on the returned channel.
func New(buf int) *Collector {
	return &Collector{
		events:   make(chan CommandEvent, buf),
		seenCmds: make(map[string]bool),
	}
}

// Events returns the read-only channel for consumed commands.
func (c *Collector) Events() <-chan CommandEvent { return c.events }

// monitorHistoryFile implements 500 ms polling with byte-offset tracking.
// pentrius-pulseagent/internal/collector/collector.go:108-136
func (c *Collector) monitorHistoryFile(ctx context.Context, histFile string) {
	fileInfo, _ := os.Stat(histFile)
	lastSize := fileInfo.Size()

	ticker := time.NewTicker(500 * time.Millisecond)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			fileInfo, _ := os.Stat(histFile)
			currentSize := fileInfo.Size()
			if currentSize > lastSize {
				c.readNewCommands(histFile, lastSize, currentSize)
				lastSize = currentSize
			}
		}
	}
}

// readNewCommands reads only the bytes appended since startPos.
// pentrius-pulseagent/internal/collector/collector.go:138-165
func (c *Collector) readNewCommands(histFile string, startPos, endPos int64) {
	file, _ := os.Open(histFile)
	defer file.Close()
	file.Seek(startPos, 0)

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		// Strip zsh history timestamps (": 1234567890:0;command")
		if strings.HasPrefix(line, ":") && strings.Contains(line, ":0;") {
			parts := strings.SplitN(line, ";", 2)
			if len(parts) == 2 {
				line = strings.TrimSpace(parts[1])
			}
		}
		// Deduplicate via seenCmds map
		c.mu.Lock()
		if !c.seenCmds[line] {
			c.seenCmds[line] = true
			c.mu.Unlock()
			c.events <- c.createCommandEvent(line, histFile)
		} else {
			c.mu.Unlock()
		}
	}
}

func (c *Collector) createCommandEvent(line, histFile string) CommandEvent {
	return CommandEvent{Raw: line, HistFile: histFile}
}

// discoverHistoryFiles searches for .bash_history, .zsh_history, .history
// in the current user's home directory (collector.go:80-106).
func discoverHistoryFiles() []string {
	home, _ := os.UserHomeDir()
	var files []string
	for _, name := range []string{".bash_history", ".zsh_history", ".history"} {
		p := home + "/" + name
		if _, err := os.Stat(p); err == nil {
			files = append(files, p)
		}
	}
	return files
}
