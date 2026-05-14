package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"

	"pentrius-pulseagent/internal/chain"
	"pentrius-pulseagent/internal/collector"
	"pentrius-pulseagent/internal/parser"
	"pentrius-pulseagent/internal/pipeline"
	"pentrius-pulseagent/internal/sender"
)

func main() {
	cfg := loadConfig()

	col := collector.New(1024)
	p := parser.New()
	h := chain.New(cfg.ChainSeed)
	s := sender.New(cfg.BackendURL, cfg.JWTToken)

	pipe := pipeline.New(col, p, h, s)

	ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer cancel()

	log.Println("pulseagent: starting pipeline")
	if err := pipe.Run(ctx); err != nil {
		log.Fatalf("pulseagent: %v", err)
	}
}

type config struct {
	BackendURL string
	JWTToken   string
	ChainSeed  string
}

func loadConfig() *config {
	return &config{
		BackendURL: os.Getenv("PULSEAGENT_BACKEND_URL"),
		JWTToken:   os.Getenv("PULSEAGENT_JWT_TOKEN"),
		ChainSeed:  os.Getenv("PULSEAGENT_CHAIN_SEED"),
	}
}
