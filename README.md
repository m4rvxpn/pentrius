# PENTRIUS: Verifiable Penetration Testing Platform

PENTRIUS is a production-grade platform that transforms penetration testing from a trust-based discipline into a cryptographically verifiable one.

## Architecture Overview

The platform comprises four main components:

1. **PulseAgent** - Lightweight Go-based endpoint agent for command telemetry capture
2. **Hash-Chain Ledger** - Cryptographic evidence integrity system with immudb and IPFS anchoring
3. **Command Decision Engine** - AI-powered classification using LangGraph state machines
4. **Coverage Scoring** - Quantified framework compliance metrics across OWASP, MITRE, PTES, and NIST

## Repository Structure

```
pentrius/
├── pentrius-pulseagent/      # Go agent implementation
├── backend/                  # FastAPI backend service
├── pentrius-ai-engine/      # LangGraph AI decision engine
├── pentrius-canvas/         # Next.js frontend dashboard
├── kong/                     # API gateway configuration
└── keycloak/                # Identity provider configuration
```

## Key Features

- 🔐 **Cryptographic Evidence Binding**: SHA-256 hash chains with tamper detection
- 🎯 **AI-Powered Classification**: Two-tier CDE with rule-based triage and LLM classification
- 📊 **Framework Coverage Scoring**: Composite scoring across OWASP (25%), MITRE (30%), PTES (25%), NIST (20%)
- 🔄 **Dynamic Test Case Generation**: Auto-spawning of contextually relevant follow-on tests
- 🌐 **Third-Party Verification**: immudb + IPFS anchoring for audit-ready compliance

## Getting Started

See individual component READMEs for setup instructions:

- [PulseAgent](pentrius-pulseagent/README.md)
- [Backend](backend/README.md)
- [AI Engine](pentrius-ai-engine/README.md)
- [Frontend](pentrius-canvas/README.md)

## License

Proprietary. All rights reserved. See [LICENSE](LICENSE) for details.