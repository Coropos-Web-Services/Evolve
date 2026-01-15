# EchoDesk Project Structure

```
EchoDesk/
│
├── 📄 ARCHITECTURE.md          # Complete technical architecture (40k words)
├── 📄 README.md                # Project overview
├── 📄 GETTING_STARTED.md       # Quick start guide
├── 📄 STATUS.md                # Current development status
├── 📄 .gitignore               # Git ignore rules
├── 📄 .env.example             # Environment configuration template
├── 📄 docker-compose.yml       # Docker Compose configuration
├── 📄 Makefile                 # Development commands
│
├── 📁 server/                  # FastAPI Backend
│   ├── 📄 Dockerfile
│   ├── 📄 pyproject.toml       # Python dependencies
│   │
│   └── 📁 app/
│       ├── 📄 __init__.py
│       ├── 📄 main.py          # Application entry point
│       │
│       ├── 📁 core/            # Core modules
│       │   ├── 📄 __init__.py
│       │   ├── 📄 config.py    # Configuration (Pydantic Settings)
│       │   └── 📄 database.py  # Database setup (SQLAlchemy async)
│       │
│       ├── 📁 models/          # Database models
│       │   ├── 📄 __init__.py
│       │   ├── 📄 agent.py     # Agent model
│       │   └── 📄 user.py      # User model
│       │
│       ├── 📁 api/             # API routes
│       │   ├── 📄 __init__.py
│       │   └── 📁 v1/
│       │       ├── 📄 __init__.py
│       │       └── 📄 agents.py # Agent endpoints
│       │
│       ├── 📁 services/        # Business logic (TODO)
│       └── 📁 utils/           # Utilities (TODO)
│
├── 📁 agent/                   # Python Agent
│   ├── 📄 pyproject.toml       # Python dependencies
│   │
│   └── 📁 echodesk_agent/
│       ├── 📄 __init__.py
│       ├── 📄 __main__.py      # CLI entry point
│       ├── 📄 agent.py         # Main agent class
│       ├── 📄 config.py        # Agent configuration
│       └── 📄 metrics.py       # System metrics collection
│
├── 📁 web/                     # React Frontend (TODO)
│   └── 📁 src/                 # Source code (pending)
│
├── 📁 docs/                    # Additional documentation
│
├── 📁 scripts/                 # Custom scripts directory
│
├── 📁 data/                    # Data directory (SQLite DB)
│   └── echodesk.db             # Created on first run
│
├── 📁 logs/                    # Log files
│
└── 📁 secrets/                 # Secrets directory (git-ignored)
```

---

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `ARCHITECTURE.md` | Complete system architecture specification |
| `README.md` | Project overview and features |
| `GETTING_STARTED.md` | Quick start guide for developers |
| `STATUS.md` | Current development progress tracking |
| `Makefile` | Development commands (make start, make logs, etc.) |
| `docker-compose.yml` | Docker services configuration |
| `.env.example` | Environment variables template |

### Server (`server/`)

**Core Modules** (`app/core/`):
- `config.py` - Application settings using Pydantic Settings
- `database.py` - SQLAlchemy async setup, session management

**Models** (`app/models/`):
- `agent.py` - Agent database model
- `user.py` - User database model

**API** (`app/api/v1/`):
- `agents.py` - Agent CRUD endpoints
  - POST /api/v1/agents/register
  - GET /api/v1/agents
  - GET /api/v1/agents/{id}
  - DELETE /api/v1/agents/{id}

**Main**:
- `main.py` - FastAPI app initialization, middleware, routes

### Agent (`agent/`)

**Core Modules** (`echodesk_agent/`):
- `agent.py` - Main agent class, connection management
- `config.py` - Configuration management with Pydantic
- `metrics.py` - System metrics collection (CPU, RAM, disk, network)
- `__main__.py` - CLI entry point

**Usage**:
```bash
# Register agent
python -m echodesk_agent register

# Run agent
python -m echodesk_agent
```

---

## API Endpoints (Current)

### Health & Info
- `GET /` - Root endpoint (name, version, status)
- `GET /health` - Health check

### Agents
- `POST /api/v1/agents/register` - Register new agent
  - Body: `{name, hostname, os, os_version, architecture, capabilities}`
  - Returns: `{agent_id, api_key, message}`
- `GET /api/v1/agents` - List all agents
  - Query: `skip`, `limit`
  - Returns: `{agents: [...], total: N}`
- `GET /api/v1/agents/{id}` - Get agent details
- `DELETE /api/v1/agents/{id}` - Delete agent

### Documentation
- `GET /api/docs` - Swagger UI (interactive API docs)
- `GET /api/redoc` - ReDoc (alternative API docs)
- `GET /api/openapi.json` - OpenAPI schema

---

## Database Schema (Current)

### agents
```sql
id              UUID PRIMARY KEY
name            VARCHAR(255)
hostname        VARCHAR(255)
os              VARCHAR(100)
os_version      VARCHAR(100)
architecture    VARCHAR(50)
api_key_hash    VARCHAR(255)
last_seen_at    TIMESTAMP
status          VARCHAR(50)      -- online, offline, error
capabilities    JSON
metadata        JSON
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

### users
```sql
id              UUID PRIMARY KEY
username        VARCHAR(255) UNIQUE
email           VARCHAR(255) UNIQUE
password_hash   VARCHAR(255)
role            VARCHAR(50)      -- admin, operator, viewer
is_active       BOOLEAN
last_login_at   TIMESTAMP
created_at      TIMESTAMP
updated_at      TIMESTAMP
```

---

## Configuration

### Server Environment Variables
```bash
# Server
SECRET_KEY=<random-string>
DEBUG=false
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./data/echodesk.db
# or
DATABASE_URL=postgresql://user:pass@host/db

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Ollama (optional)
OLLAMA_URL=http://ollama:11434
```

### Agent Configuration
Location: `/etc/echodesk-agent/config.yml`

```yaml
server_url: http://localhost:8000
agent_id: <uuid>
api_key: <key>
name: my-agent
capabilities:
  - system.metrics
```

---

## Development Workflow

### Start Development Environment
```bash
make setup          # First time setup
make start          # Start server
make logs           # View logs
```

### Develop Server
```bash
cd server
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Develop Agent
```bash
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
python -m echodesk_agent
```

---

## Technology Stack

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy 2.0** - ORM (async)
- **aiosqlite** - Async SQLite driver
- **Pydantic v2** - Data validation
- **Uvicorn** - ASGI server
- **passlib** - Password hashing

### Agent
- **httpx** - Async HTTP client
- **psutil** - System metrics
- **pyyaml** - Config file parsing

### Future
- **python-socketio** - WebSocket (next session)
- **React 18** - Frontend UI
- **TypeScript** - Type safety
- **shadcn/ui** - UI components

---

## What's Next?

See [STATUS.md](./STATUS.md) for current progress and next steps.

Priority items:
1. WebSocket implementation
2. Real-time metrics streaming
3. React frontend initialization
4. Dashboard UI

---

**Last Updated**: 2026-01-15
