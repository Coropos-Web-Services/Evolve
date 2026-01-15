# EchoDesk

**Local-first infrastructure command center for your digital and physical systems.**

EchoDesk enables you to observe, control, automate, and orchestrate your homelab, servers, containers, services, and AI workflows from a unified interface.

## Features

- **System Monitoring**: Real-time metrics from all your nodes
- **Service Control**: Manage Docker containers and systemd services
- **Automation Engine**: Create rules and workflows to automate operations
- **AI Orchestration**: Use local LLMs (Ollama) to control your infrastructure
- **Hardware Ready**: Built for future integration with physical controls (DeskMate)

## Architecture

See [ARCHITECTURE.md](./ARCHITECTURE.md) for complete technical specification.

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for development)
- Node.js 18+ (for frontend development)

### Development Setup

1. **Clone and enter directory**
   ```bash
   cd EchoDesk
   ```

2. **Start development environment**
   ```bash
   docker-compose up -d
   ```

3. **Access UI**
   - Web Interface: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Install Agent on a Node

```bash
curl -fsSL https://echodesk.local:8443/install.sh | sudo bash -s -- --token YOUR_INSTALL_TOKEN
```

## Project Structure

```
EchoDesk/
├── server/          # FastAPI backend
├── agent/           # Python agent for nodes
├── web/             # React frontend
├── docs/            # Documentation
└── docker-compose.yml
```

## Development Status

🚧 **Currently in active development - MVP Phase**

See [Milestone 1](./ARCHITECTURE.md#milestone-1-core-foundation-weeks-1-2) for current progress.

## License

TBD

## Contributing

TBD
