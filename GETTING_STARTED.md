# Getting Started with EchoDesk

## Quick Start (5 minutes)

### 1. Start the Server

```bash
# Create environment file
cp .env.example .env

# Start server with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f server
```

The server will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Health Check: http://localhost:8000/health

### 2. Test the Server

```bash
# Check health
curl http://localhost:8000/health

# View API documentation
open http://localhost:8000/api/docs
```

### 3. Register an Agent (Local Development)

```bash
# Install agent dependencies
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Register agent
python -m echodesk_agent register

# Run agent
python -m echodesk_agent
```

### 4. Verify Agent Registration

```bash
# List agents via API
curl http://localhost:8000/api/v1/agents
```

You should see your registered agent in the response.

---

## Development Setup

### Server Development

```bash
cd server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"

# Run server locally (without Docker)
uvicorn app.main:app --reload --port 8000
```

### Agent Development

```bash
cd agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies with Docker support
pip install -e ".[docker,dev]"

# Run agent
python -m echodesk_agent
```

### Running Tests

```bash
# Server tests
cd server
pytest

# Agent tests
cd agent
pytest
```

---

## What's Working Now

✅ **Server**
- FastAPI server with async SQLAlchemy
- Agent registration endpoint
- Database models (Agent, User)
- Health check endpoint
- OpenAPI documentation

✅ **Agent**
- System metrics collection (CPU, memory, disk, network)
- Agent registration with server
- Config file management
- Metrics and heartbeat loops

---

## Next Steps

### Immediate (Next Session)
1. Add WebSocket support for real-time communication
2. Implement heartbeat endpoint on server
3. Add metrics storage endpoint
4. Create basic React frontend

### Milestone 1 Remaining
- [ ] WebSocket server for agent connections
- [ ] Agent status tracking (online/offline)
- [ ] React UI with dashboard layout
- [ ] System stats widget
- [ ] Agent list widget
- [ ] Real-time updates

---

## Project Structure

```
EchoDesk/
├── server/               # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── services/    # Business logic
│   │   └── main.py      # App entry point
│   ├── Dockerfile
│   └── pyproject.toml
│
├── agent/               # Python agent
│   ├── echodesk_agent/
│   │   ├── agent.py     # Main agent class
│   │   ├── config.py    # Configuration
│   │   ├── metrics.py   # Metrics collection
│   │   └── __main__.py  # CLI entry point
│   └── pyproject.toml
│
├── docker-compose.yml   # Development environment
├── ARCHITECTURE.md      # Full architecture spec
└── README.md
```

---

## Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# View server logs
docker-compose logs server
```

### Agent can't connect
```bash
# Verify server is running
curl http://localhost:8000/health

# Check agent config
cat /etc/echodesk-agent/config.yml

# Run agent with debug logging
python -m echodesk_agent
```

### Database issues
```bash
# Reset database
rm -f data/echodesk.db
docker-compose restart server
```

---

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret (change in production!)
- `CORS_ORIGINS` - Allowed frontend origins
- `OLLAMA_URL` - Ollama server URL (optional)

---

## What to Build Next

Based on the [Architecture](./ARCHITECTURE.md), here's the recommended order:

1. **WebSocket Communication** (Week 1)
   - Add python-socketio to server
   - Implement agent connection handling
   - Heartbeat and metrics endpoints

2. **Basic UI** (Week 1-2)
   - Initialize React + Vite
   - Create dashboard layout
   - Add agent list and system stats widgets

3. **Service Discovery** (Week 2)
   - Docker service detection
   - systemd service detection
   - Service status display

4. **Service Control** (Week 3-4)
   - Start/stop/restart actions
   - Command execution framework
   - Audit logging

Continue following the [MVP Roadmap](./ARCHITECTURE.md#mvp-feature-prioritization).
